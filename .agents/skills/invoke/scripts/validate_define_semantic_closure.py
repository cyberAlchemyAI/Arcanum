#!/usr/bin/env python3
"""Validate one exact pre-Define semantic context and emit a closure receipt.

The validator is deliberately read-only except for exclusive creation of the
requested receipt.  It verifies an independent assessor's proposed semantic
classification; it never invents or promotes terminology.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator


SCHEMA_URI = "https://arcanum.dev/schemas/invoke/define-semantic-closure-receipt/v1"
SCHEMA_VERSION = "invoke.define-semantic-closure-receipt.v1"
VALIDATOR_ID = "invoke.validate-define-semantic-closure.v1"
VALIDATOR_OWNER = "invoke-define-semantic-closure-validator"
VALIDATOR_PATH = ".agents/skills/invoke/scripts/validate_define_semantic_closure.py"
CHECK_IDS = (
    "check:authority-resolution",
    "check:source-freshness",
    "check:probe-coverage",
    "check:canonical-index-parity",
    "check:normalized-collision",
    "check:semantic-overlap",
    "check:consumer-coverage",
    "check:independent-owner",
)
SCOPE_RANK = {"repository": 0, "project": 1, "feature": 2, "artifact": 3}
GLOB_META = re.compile(r"[*?\[\]]")
DEF_HEADING = re.compile(r"^(?:##|###)\s+((?:DEF-ARC|DS)-[A-Z0-9-]+):\s*(.+?)\s*$")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")


class InvocationError(Exception):
    """An invocation or schema failure for which no receipt may be written."""


class DuplicateKeyError(ValueError):
    pass


def json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=json_object)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise InvocationError(f"cannot read valid JSON from {path}: {exc}") from exc


def load_json_bytes(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=json_object)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise InvocationError(f"cannot read valid JSON from {label}: {exc}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def exact_ref(path: str, data: bytes) -> dict[str, Any]:
    return {"path": path, "sha256": sha256_bytes(data), "size": len(data)}


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def contains_label(text: str, label: str) -> bool:
    return re.search(rf"(?<![\w-]){re.escape(label)}(?![\w-])", text) is not None


def markdown_anchor(value: str) -> str:
    value = normalize(value).replace(" ", "-")
    return re.sub(r"[^a-z0-9_-]", "", value)


def selector_names_definition(match: dict[str, Any], entry: dict[str, Any]) -> bool:
    definition_id = match.get("definition_id")
    if not isinstance(definition_id, str):
        return False
    ref = match["source_ref"]
    if ref["selector_type"] == "heading":
        selected = ref["selector"].lstrip("#").strip()
        return normalize(selected) == normalize(f"{definition_id}: {entry['heading']}")
    if ref["selector_type"] == "anchor":
        return ref["selector"].lstrip("#") == entry["anchor"]
    return False


def validate_schema(document: Any, schema: dict[str, Any], label: str) -> None:
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        rendered = "; ".join(
            f"/{'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
            for error in errors
        )
        raise InvocationError(f"{label} schema validation failed: {rendered}")


def repo_path(root: Path, relative: str) -> Path:
    candidate = root / relative
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ValueError(f"path is missing or escapes repository: {relative}") from exc
    if not resolved.is_file():
        raise ValueError(f"path is not a regular file: {relative}")
    return resolved


def strict_json_bytes(data: bytes) -> Any:
    return json.loads(data.decode("utf-8"), object_pairs_hook=json_object)


def yaml_value(data: bytes) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        raise ValueError("YAML selector requires PyYAML") from exc

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader: Any, node: Any, deep: bool = False) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError(f"duplicate YAML key: {key}")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    return yaml.load(data.decode("utf-8"), Loader=UniqueLoader)


def resolve_pointer(value: Any, pointer: str) -> Any:
    current = value
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise KeyError(token)
    return current


def resolve_yaml_path(value: Any, selector: str) -> Any:
    current = value
    for token in selector.split("."):
        if not token:
            raise KeyError(selector)
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise KeyError(token)
    return current


def validate_selector(ref: dict[str, Any], data: bytes) -> None:
    source_format = ref["format"]
    selector_type = ref["selector_type"]
    selector = ref["selector"]
    text: str | None = None
    if source_format in {"markdown", "text", "yaml"}:
        text = data.decode("utf-8")
    if source_format == "json":
        parsed = strict_json_bytes(data)
    elif source_format == "yaml":
        parsed = yaml_value(data)
    else:
        parsed = None

    if selector_type == "whole-file":
        if selector != "$":
            raise ValueError("whole-file selector must be $")
    elif selector_type == "heading":
        assert text is not None
        wanted = normalize(selector.lstrip("#").strip())
        headings = [normalize(match.group(1)) for line in text.splitlines() if (match := HEADING.match(line))]
        if wanted not in headings:
            raise ValueError(f"Markdown heading not found: {selector}")
    elif selector_type == "anchor":
        assert text is not None
        anchors = [markdown_anchor(match.group(1)) for line in text.splitlines() if (match := HEADING.match(line))]
        if selector.lstrip("#") not in anchors:
            raise ValueError(f"Markdown anchor not found: {selector}")
    elif selector_type == "json-pointer":
        try:
            resolve_pointer(parsed, selector)
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise ValueError(f"JSON Pointer not found: {selector}") from exc
    elif selector_type == "yaml-path":
        try:
            resolve_yaml_path(parsed, selector)
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise ValueError(f"YAML path not found: {selector}") from exc
    elif selector_type == "symbol":
        if text is None or selector not in text:
            raise ValueError(f"symbol not found: {selector}")
    else:  # protected by schema, retained as fail-closed defense
        raise ValueError(f"unsupported selector type: {selector_type}")


def iter_material_refs(context: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    discovery = context["discovery"]
    if discovery["kind"] == "artifact":
        yield "discovery-source", discovery["ref"]
    for probe in context["concept_probes"]:
        for ref in probe["evidence_refs"]:
            yield "probe-evidence", ref
        for match in probe["claimed_matches"]:
            yield "probe-evidence", match["source_ref"]
    boundary = context["authority_boundary"]
    for ref in boundary["canonical_source_refs"]:
        yield "canonical-source", ref
    for ref in boundary["index_refs"]:
        yield "canonical-index", ref
    for ref in boundary["resolution_evidence_refs"]:
        yield "resolution-evidence", ref
    for registry in context["adjacent_registries"]:
        role = "candidate-registry" if registry["authority_class"] == "candidate" else "local-glossary"
        yield role, registry["source_ref"]
    for consumer in context["consumer_boundary"]["consumers"]:
        yield "consumer", consumer["source_ref"]
    for exclusion in context["exclusions"]:
        yield "exclusion-evidence", exclusion["evidence_ref"]


def parse_definitions(data: bytes) -> tuple[dict[str, dict[str, Any]], str | None]:
    lines = data.decode("utf-8").splitlines()
    owner = None
    document_status = None
    for line in lines[:20]:
        if line.startswith("Owner:"):
            owner = line.split(":", 1)[1].strip()
        elif line.startswith("Status:"):
            document_status = line.split(":", 1)[1].strip()
    definitions: dict[str, dict[str, Any]] = {}
    positions = [(index, match) for index, line in enumerate(lines) if (match := DEF_HEADING.match(line))]
    for offset, (start, match) in enumerate(positions):
        end = positions[offset + 1][0] if offset + 1 < len(positions) else len(lines)
        section = lines[start + 1 : end]
        definition_id, heading_term = match.groups()
        status = None
        term = None
        aliases: list[str] = []
        index = 0
        while index < len(section):
            line = section[index]
            if line.startswith("Status:"):
                status = line.split(":", 1)[1].strip()
            elif line.startswith("Term:"):
                term = line.split(":", 1)[1].strip()
            elif line.startswith("Aliases:"):
                chunks = [line.split(":", 1)[1].strip()]
                index += 1
                while index < len(section) and section[index].strip() and not section[index].startswith("#"):
                    chunks.append(section[index].strip())
                    index += 1
                aliases = [part.strip() for part in " ".join(chunks).split(",") if part.strip()]
                continue
            index += 1
        if definition_id in definitions:
            raise ValueError(f"duplicate canonical definition ID: {definition_id}")
        definitions[definition_id] = {
            "id": definition_id,
            "term": term or heading_term,
            "status": status or document_status or "",
            "aliases": aliases,
            "heading": heading_term,
            "anchor": markdown_anchor(f"{definition_id} {heading_term}"),
        }
    if not definitions:
        raise ValueError("canonical source contains no supported definition sections")
    return definitions, owner


def parse_index(data: bytes) -> tuple[dict[str, dict[str, str]], list[tuple[str, str]]]:
    lines = data.decode("utf-8").splitlines()
    mode = None
    terms: dict[str, dict[str, str]] = {}
    aliases: list[tuple[str, str]] = []
    for line in lines:
        if line == "## Terms":
            mode = "terms"
            continue
        if line == "## Alias Lookup":
            mode = "aliases"
            continue
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if mode == "terms" and cells[0] != "ID" and len(cells) >= 4:
            definition_id, term, status, link = cells[:4]
            anchor_match = re.search(r"\]\([^#]+#([^)]+)\)", link)
            if definition_id in terms:
                raise ValueError(f"duplicate index definition ID: {definition_id}")
            terms[definition_id] = {
                "term": term,
                "status": status,
                "anchor": anchor_match.group(1) if anchor_match else "",
            }
        elif mode == "aliases" and cells[0] != "Alias" and len(cells) >= 2:
            aliases.append((cells[0], cells[1]))
    return terms, aliases


def registry_entries(data: bytes, format_profile: str) -> list[dict[str, Any]]:
    value = strict_json_bytes(data)
    if not isinstance(value, dict):
        raise ValueError(f"{format_profile} registry must be an object")
    expected_schema = {
        "definitions-json-v1": "https://arcanum.dev/schemas/invoke/definitions/v1",
        "definitions-json-v2": "https://arcanum.dev/schemas/invoke/definitions/v2",
    }[format_profile]
    if "$schema" in value and value["$schema"] != expected_schema:
        raise ValueError(f"{format_profile} registry declares the wrong $schema")
    entries = value.get("definitions", [])
    if not isinstance(entries, list):
        raise ValueError("registry definitions must be an array")
    result = []
    for entry in entries:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("id"), str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{2,127}", entry["id"])
            or not isinstance(entry.get("term"), str)
            or not entry["term"].strip()
        ):
            raise ValueError(f"{format_profile} registry definition lacks a stable ID or non-empty term")
        aliases = entry.get("aliases", [])
        if not isinstance(aliases, list) or any(not isinstance(alias, str) for alias in aliases):
            raise ValueError("registry aliases must be strings")
        result.append({"id": entry.get("id"), "term": entry["term"], "aliases": aliases})
    ids = [entry["id"] for entry in result]
    duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise ValueError(f"{format_profile} registry contains duplicate definition IDs: {duplicates}")
    return result


def path_for_glob(root: Path, base: str, pattern: str) -> list[str]:
    base_path = root / base
    try:
        resolved_base = base_path.resolve(strict=True)
        resolved_base.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ValueError(f"discovery root is missing or escapes repository: {base}") from exc
    if not resolved_base.is_dir():
        raise ValueError(f"discovery root is not a directory: {base}")
    paths: list[str] = []
    for candidate in resolved_base.glob(pattern):
        if not candidate.is_file():
            continue
        resolved = candidate.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"discovered path escapes repository: {candidate}") from exc
        paths.append(candidate.relative_to(root).as_posix())
    return sorted(set(paths))


def main(
    argv: list[str] | None = None,
    *,
    _return_receipt: bool = False,
) -> int | dict[str, Any]:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--context-schema", type=Path, required=True)
    parser.add_argument("--receipt-schema", type=Path, required=True)
    parser.add_argument("--discovery-root", action="append", required=True, help="Trusted repository-relative discovery root; repeat as needed.")
    parser.add_argument("--public-root", action="append", default=[], help="Trusted repository-relative public root; required for public targets.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    output = args.output.absolute()
    if not _return_receipt and output.exists():
        print(f"error: output already exists: {output}", file=sys.stderr)
        return 2

    try:
        root = args.repository_root.resolve(strict=True)
        if not root.is_dir():
            raise InvocationError("repository root is not a directory")
        context_path = args.context.resolve(strict=True)
        context_path.relative_to(root)
        context_schema_path = args.context_schema.resolve(strict=True)
        context_schema_path.relative_to(root)
        receipt_schema_path = args.receipt_schema.resolve(strict=True)
        receipt_schema_path.relative_to(root)
        if not _return_receipt:
            try:
                output_parent = output.parent.resolve(strict=True)
                output_parent.relative_to(root)
            except OSError as exc:
                raise InvocationError("output parent must already exist") from exc
            except ValueError as exc:
                raise InvocationError("output must remain inside the repository root") from exc
        context_data = context_path.read_bytes()
        context_schema_data = context_schema_path.read_bytes()
        receipt_schema_data = receipt_schema_path.read_bytes()
        context = load_json_bytes(context_data, str(context_path))
        context_schema = load_json_bytes(context_schema_data, str(context_schema_path))
        receipt_schema = load_json_bytes(receipt_schema_data, str(receipt_schema_path))
        validate_schema(context, context_schema, "context")
    except (InvocationError, OSError, ValueError) as exc:
        if _return_receipt:
            raise InvocationError(str(exc)) from exc
        print(f"error: {exc}", file=sys.stderr)
        return 2

    context_rel = context_path.relative_to(root).as_posix()
    context_schema_rel = context_schema_path.relative_to(root).as_posix()
    receipt_schema_rel = receipt_schema_path.relative_to(root).as_posix()
    validator_data = Path(__file__).read_bytes()

    blockers: list[dict[str, Any]] = []
    blocker_ids: set[str] = set()

    def block(code: str, message: str, owner: str, route: str) -> str:
        seed = f"{code}\0{message}\0{owner}\0{route}".encode("utf-8")
        blocker_id = f"blocker:{code.lower().replace('_', '-')}:{sha256_bytes(seed)[:12]}"
        if blocker_id not in blocker_ids:
            blocker_ids.add(blocker_id)
            blockers.append({
                "blocker_id": blocker_id,
                "code": code,
                "message": message,
                "owner": owner,
                "repair_route": route,
            })
        return blocker_id

    inspections: list[dict[str, Any]] = []
    inspection_keys: set[tuple[Any, ...]] = set()
    source_blockers: list[str] = []
    source_blockers_by_path: dict[str, list[str]] = defaultdict(list)
    observed_data: dict[str, bytes] = {}

    configured_discovery_roots: list[str] = []
    configured_public_roots: list[str] = []
    try:
        for configured, destination in (
            (args.discovery_root, configured_discovery_roots),
            (args.public_root, configured_public_roots),
        ):
            for relative in configured:
                if Path(relative).is_absolute() or ".." in Path(relative).parts:
                    raise ValueError(f"configured root is not repository-relative: {relative}")
                resolved = (root / relative).resolve(strict=True)
                resolved.relative_to(root)
                if not resolved.is_dir():
                    raise ValueError(f"configured root is not a directory: {relative}")
                destination.append(Path(relative).as_posix())
    except (OSError, ValueError) as exc:
        if _return_receipt:
            raise InvocationError(f"invalid trusted root configuration: {exc}") from exc
        print(f"error: invalid trusted root configuration: {exc}", file=sys.stderr)
        return 2
    configured_discovery_roots = sorted(set(configured_discovery_roots))
    configured_public_roots = sorted(set(configured_public_roots))
    if context["target"]["visibility"] == "public" and not configured_public_roots:
        if _return_receipt:
            raise InvocationError("public contexts require at least one --public-root")
        print("error: public contexts require at least one --public-root", file=sys.stderr)
        return 2
    public_roots = [(root / relative).resolve() for relative in configured_public_roots]

    for role, ref in iter_material_refs(context):
        key = (
            role,
            ref["path"],
            ref["sha256"],
            ref["size"],
            ref["format"],
            ref["selector_type"],
            ref["selector"],
            ref["visibility"],
        )
        if key in inspection_keys:
            continue
        inspection_keys.add(key)
        causal: list[str] = []
        observed = None
        status = "current"
        try:
            path = repo_path(root, ref["path"])
            if ref["path"] in observed_data:
                data = observed_data[ref["path"]]
            else:
                data = path.read_bytes()
                observed_data[ref["path"]] = data
            observed = exact_ref(ref["path"], data)
            if ref["sha256"] != observed["sha256"] or ref["size"] != observed["size"]:
                raise ValueError("declared digest or size does not match observed bytes")
            validate_selector(ref, data)
            if context["target"]["visibility"] == "public":
                resolved = path.resolve()
                if not any(resolved == base or resolved.is_relative_to(base) for base in public_roots):
                    raise ValueError("declared-public source is outside every public discovery root")
        except (OSError, UnicodeError, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError, DuplicateKeyError) as exc:
            status = "missing" if "missing" in str(exc) else "stale"
            blocker_id = block(
                "SOURCE_FRESHNESS_FAILURE",
                f"{role} {ref['path']} failed exact inspection: {exc}",
                "semantic-context-author",
                "Repair the exact source reference or selector and rerun semantic closure.",
            )
            causal.append(blocker_id)
            source_blockers.append(blocker_id)
            source_blockers_by_path[ref["path"]].append(blocker_id)
        inspection_seed = "\0".join(str(part) for part in key).encode("utf-8")
        inspections.append({
            "inspection_id": f"inspection:{sha256_bytes(inspection_seed)[:20]}",
            "role": role,
            "declared_path": ref["path"],
            "format": ref["format"],
            "selector_type": ref["selector_type"],
            "selector": ref["selector"],
            "visibility": ref["visibility"],
            "observed_ref": observed,
            "status": status,
            "causal_blocker_ids": sorted(set(causal)),
        })

    snapshots: list[dict[str, Any]] = []
    discovered_registries: set[str] = set()
    discovered_consumers: set[str] = set()
    discovery_blockers: list[str] = []
    excluded_selectors = {item["selector"]: item for item in context["exclusions"]}
    excluded_paths: set[str] = set()
    declared_discovery_roots = sorted({item["path"] for item in context["discovery_contract"]["roots"]})
    if declared_discovery_roots != configured_discovery_roots:
        discovery_blockers.append(block(
            "DISCOVERY_ROOT_CONFIGURATION_MISMATCH",
            f"Context discovery roots {declared_discovery_roots} do not equal trusted invocation roots {configured_discovery_roots}.",
            "invoke-owner",
            "Make the context roots equal the independently configured discovery roots.",
        ))
    if context["target"]["visibility"] == "public":
        for relative in configured_discovery_roots:
            resolved = (root / relative).resolve()
            if not any(resolved == public or resolved.is_relative_to(public) for public in public_roots):
                discovery_blockers.append(block(
                    "DISCOVERY_ROOT_OUTSIDE_PUBLIC_BOUNDARY",
                    f"Configured discovery root {relative} is outside every trusted public root.",
                    "invoke-owner",
                    "Choose a discovery root inside the trusted public boundary.",
                ))
    root_ids = [item["root_id"] for item in context["discovery_contract"]["roots"]]
    duplicate_root_ids = sorted(item for item, count in Counter(root_ids).items() if count > 1)
    if duplicate_root_ids:
        discovery_blockers.append(block(
            "DUPLICATE_DISCOVERY_ROOT_ID",
            f"Discovery root IDs are not unique: {duplicate_root_ids}",
            "semantic-context-author",
            "Assign one unique identity to every discovery root.",
        ))
    root_paths = [item["path"] for item in context["discovery_contract"]["roots"]]
    duplicate_root_paths = sorted(item for item, count in Counter(root_paths).items() if count > 1)
    if duplicate_root_paths:
        discovery_blockers.append(block(
            "DUPLICATE_DISCOVERY_ROOT_PATH",
            f"Discovery root paths are not unique: {duplicate_root_paths}",
            "semantic-context-author",
            "Declare each configured discovery root exactly once.",
        ))
    for selector, exclusion in sorted(excluded_selectors.items()):
        if GLOB_META.search(selector):
            discovery_blockers.append(block(
                "INVALID_EXCLUSION_SELECTOR",
                f"Exclusion {exclusion['exclusion_id']} is not an exact file path: {selector}",
                exclusion["owner"],
                "Replace wildcard or collection exclusions with exact file exclusions.",
            ))
            continue
        try:
            repo_path(root, selector)
            excluded_paths.add(selector)
        except ValueError as exc:
            discovery_blockers.append(block(
                "INVALID_EXCLUSION_SELECTOR",
                f"Exclusion {exclusion['exclusion_id']} is unresolved: {exc}",
                exclusion["owner"],
                "Repair or remove the exact exclusion and rerun semantic closure.",
            ))

    non_consumer_material = {context_rel} | {
        ref["path"]
        for role, ref in iter_material_refs(context)
        if role != "consumer"
    }
    probe_labels = {
        normalize(label)
        for probe in context["concept_probes"]
        for label in [probe["term"], *probe["aliases"]]
    }
    discovered_data: dict[str, bytes] = dict(observed_data)

    def read_discovered(path: str) -> bytes:
        if path not in discovered_data:
            discovered_data[path] = repo_path(root, path).read_bytes()
        return discovered_data[path]

    for item in context["discovery_contract"]["roots"]:
        registry_paths: set[str] = set()
        consumer_paths: set[str] = set()
        try:
            for pattern in item["registry_globs"]:
                registry_paths.update(path_for_glob(root, item["path"], pattern))
            for pattern in item["consumer_globs"]:
                for path in path_for_glob(root, item["path"], pattern):
                    if path in non_consumer_material:
                        continue
                    try:
                        text = read_discovered(path).decode("utf-8")
                    except (OSError, UnicodeError, ValueError) as exc:
                        discovery_blockers.append(block(
                            "CONSUMER_DISCOVERY_READ_FAILURE",
                            f"Discovered consumer candidate {path} could not be read safely: {exc}",
                            "semantic-context-assessor",
                            "Repair or exactly exclude the unreadable consumer candidate.",
                        ))
                        continue
                    normalized_text = normalize(text)
                    if any(contains_label(normalized_text, label) for label in probe_labels):
                        consumer_paths.add(path)
        except ValueError as exc:
            discovery_blockers.append(block(
                "DISCOVERY_ENUMERATION_FAILURE",
                f"Discovery root {item['root_id']} could not be enumerated: {exc}",
                "semantic-context-author",
                "Repair the declared discovery root and rerun semantic closure.",
            ))
        excluded_here = {path for path in registry_paths | consumer_paths if path in excluded_paths}
        registry_paths -= excluded_here
        consumer_paths -= excluded_here
        discovered_registries.update(registry_paths)
        discovered_consumers.update(consumer_paths)
        membership = {
            "root_id": item["root_id"],
            "path": item["path"],
            "registry_paths": sorted(registry_paths),
            "consumer_paths": sorted(consumer_paths),
            "excluded_paths": sorted(excluded_here),
            "content_refs": [],
        }
        for path in sorted(registry_paths | consumer_paths | excluded_here):
            try:
                membership["content_refs"].append(exact_ref(path, read_discovered(path)))
            except (OSError, ValueError) as exc:
                discovery_blockers.append(block(
                    "DISCOVERY_CONTENT_BINDING_FAILURE",
                    f"Discovered path {path} could not be bound exactly: {exc}",
                    "semantic-context-assessor",
                    "Repair the discovered path and rerun semantic closure.",
                ))
        membership["membership_digest"] = sha256_bytes(canonical_bytes(membership))
        snapshots.append(membership)

    declared_registry_paths = {
        ref["path"] for ref in context["authority_boundary"]["canonical_source_refs"]
    } | {
        ref["path"] for ref in context["authority_boundary"]["index_refs"]
    } | {
        item["source_ref"]["path"] for item in context["adjacent_registries"]
    }
    undeclared_registries = sorted(discovered_registries - declared_registry_paths)
    missing_registry_discovery = sorted(declared_registry_paths - discovered_registries)
    if undeclared_registries or missing_registry_discovery:
        discovery_blockers.append(block(
            "REGISTRY_COVERAGE_MISMATCH",
            f"Declared/discovered registry mismatch; undeclared={undeclared_registries}, undiscovered={missing_registry_discovery}",
            "semantic-context-assessor",
            "Make the declared-root registry projection and registry declarations equal.",
        ))

    declared_consumer_paths = {
        item["source_ref"]["path"] for item in context["consumer_boundary"]["consumers"]
    }
    hidden_consumers = sorted(discovered_consumers - declared_consumer_paths)
    missing_consumers = sorted(declared_consumer_paths - discovered_consumers)
    consumer_blockers: list[str] = []
    consumer_ids = [item["consumer_id"] for item in context["consumer_boundary"]["consumers"]]
    duplicate_consumer_ids = sorted(item for item, count in Counter(consumer_ids).items() if count > 1)
    if duplicate_consumer_ids:
        consumer_blockers.append(block(
            "DUPLICATE_CONSUMER_ID",
            f"Consumer IDs are not unique: {duplicate_consumer_ids}",
            "semantic-context-assessor",
            "Assign one unique identity to every declared consumer.",
        ))
    exclusion_ids = [item["exclusion_id"] for item in context["exclusions"]]
    duplicate_exclusion_ids = sorted(item for item, count in Counter(exclusion_ids).items() if count > 1)
    if duplicate_exclusion_ids:
        consumer_blockers.append(block(
            "DUPLICATE_EXCLUSION_ID",
            f"Exclusion IDs are not unique: {duplicate_exclusion_ids}",
            "semantic-context-assessor",
            "Assign one unique identity to every exact exclusion.",
        ))
    if hidden_consumers or missing_consumers:
        consumer_blockers.append(block(
            "CONSUMER_COVERAGE_MISMATCH",
            f"Declared/discovered consumer mismatch; undeclared={hidden_consumers}, undiscovered={missing_consumers}",
            "semantic-context-assessor",
            "Catalogue each discovered consumer or add an exact evidenced exclusion.",
        ))
    unused_exclusions = sorted(excluded_paths - {
        path for snapshot in snapshots for path in snapshot["excluded_paths"]
    })
    if unused_exclusions:
        consumer_blockers.append(block(
            "UNUSED_EXCLUSION",
            f"Exact exclusions did not remove a discovered registry or consumer: {unused_exclusions}",
            "semantic-context-assessor",
            "Remove unused exclusions or repair the discovery patterns they are intended to constrain.",
        ))

    authority_blockers: list[str] = []
    authority_status = "resolved"
    canonical_definitions: dict[str, dict[str, Any]] = {}
    canonical_owner = context["authority_boundary"]["declared_owner"]
    index_terms: dict[str, dict[str, str]] = {}
    index_aliases: list[tuple[str, str]] = []
    boundary = context["authority_boundary"]
    authority_paths = [
        ref["path"]
        for ref in boundary["canonical_source_refs"] + boundary["index_refs"] + boundary["resolution_evidence_refs"]
    ]
    canonical_index_paths = [
        ref["path"] for ref in boundary["canonical_source_refs"] + boundary["index_refs"]
    ]
    authority_source_blockers = [
        blocker_id for path in authority_paths for blocker_id in source_blockers_by_path[path]
    ]
    canonical_index_source_blockers = [
        blocker_id for path in canonical_index_paths for blocker_id in source_blockers_by_path[path]
    ]
    if boundary["declaration"] != "configured":
        authority_status = "absent" if boundary["declaration"] == "no-canonical-source" else "ambiguous"
        authority_blockers.append(block(
            "AUTHORITY_UNRESOLVED",
            f"Authority declaration is {boundary['declaration']}; Define v3 requires one resolved authority.",
            "definitions-governance",
            "Resolve the definitions authority before Define v3 authoring.",
        ))
    else:
        if authority_source_blockers:
            authority_status = "ambiguous"
        if not canonical_index_source_blockers:
            try:
                canonical_ref = boundary["canonical_source_refs"][0]
                index_ref = boundary["index_refs"][0]
                canonical_definitions, observed_owner = parse_definitions(observed_data[canonical_ref["path"]])
                index_terms, index_aliases = parse_index(observed_data[index_ref["path"]])
                if observed_owner != boundary["declared_owner"]:
                    raise ValueError(f"declared owner {boundary['declared_owner']} != observed owner {observed_owner}")
                canonical_owner = observed_owner or canonical_owner
            except (ValueError, KeyError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
                authority_status = "ambiguous"
                authority_blockers.append(block(
                    "AUTHORITY_RESOLUTION_FAILURE",
                    f"Configured definitions authority could not be resolved: {exc}",
                    "definitions-governance",
                    "Repair the authority declaration or canonical source and rerun semantic closure.",
                ))

    parity_blockers: list[str] = []
    if canonical_definitions:
        expected_terms = {
            definition_id: {
                "term": entry["term"],
                "status": entry["status"],
                "anchor": entry["anchor"],
            }
            for definition_id, entry in canonical_definitions.items()
        }
        duplicate_aliases = [alias for alias, count in Counter(normalize(a) for a, _ in index_aliases).items() if count > 1]
        expected_aliases = sorted(
            (normalize(alias), definition_id)
            for definition_id, entry in canonical_definitions.items()
            for alias in entry["aliases"]
        )
        observed_aliases = sorted((normalize(alias), definition_id) for alias, definition_id in index_aliases)
        term_parity = set(expected_terms) == set(index_terms) and all(
            normalize(expected_terms[definition_id]["term"]) == normalize(index_terms[definition_id]["term"])
            and expected_terms[definition_id]["status"] == index_terms[definition_id]["status"]
            and expected_terms[definition_id]["anchor"] == index_terms[definition_id]["anchor"]
            for definition_id in expected_terms
        )
        if not term_parity or expected_aliases != observed_aliases or duplicate_aliases:
            parity_blockers.append(block(
                "CANONICAL_INDEX_PARITY_FAILURE",
                "Canonical definition IDs, terms, statuses, anchors, or aliases differ from the index.",
                "definitions-governance",
                "Regenerate or repair the canonical definitions index.",
            ))

    probe_blockers: list[str] = []
    probe_ids = [probe["probe_id"] for probe in context["concept_probes"]]
    duplicate_probe_ids = sorted(item for item, count in Counter(probe_ids).items() if count > 1)
    if duplicate_probe_ids:
        probe_blockers.append(block(
            "DUPLICATE_PROBE_ID",
            f"Probe IDs are not unique: {duplicate_probe_ids}",
            "semantic-context-assessor",
            "Assign one unique identity to every concept probe.",
        ))
    match_ids = [
        match["match_id"]
        for probe in context["concept_probes"]
        for match in probe["claimed_matches"]
    ]
    duplicate_match_ids = sorted(item for item, count in Counter(match_ids).items() if count > 1)
    if duplicate_match_ids:
        probe_blockers.append(block(
            "DUPLICATE_MATCH_ID",
            f"Claimed match IDs are not unique: {duplicate_match_ids}",
            "semantic-context-assessor",
            "Assign one unique identity to every claimed semantic match.",
        ))

    adjacent_entries: list[tuple[dict[str, Any], dict[str, Any]]] = []
    adjacent_parse_blockers: list[str] = []
    registry_ids = [registry["registry_id"] for registry in context["adjacent_registries"]]
    duplicate_registry_ids = sorted(item for item, count in Counter(registry_ids).items() if count > 1)
    if duplicate_registry_ids:
        adjacent_parse_blockers.append(block(
            "DUPLICATE_REGISTRY_ID",
            f"Adjacent registry IDs are not unique: {duplicate_registry_ids}",
            "semantic-context-assessor",
            "Assign one unique identity to every adjacent registry.",
        ))
    for registry in context["adjacent_registries"]:
        path = registry["source_ref"]["path"]
        if path not in observed_data or source_blockers_by_path[path]:
            continue
        try:
            for entry in registry_entries(observed_data[path], registry["format_profile"]):
                adjacent_entries.append((registry, entry))
        except (ValueError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
            adjacent_parse_blockers.append(block(
                "ADJACENT_REGISTRY_PARSE_FAILURE",
                f"Adjacent registry {path} is not parseable: {exc}",
                "semantic-context-assessor",
                "Repair the adjacent registry and rerun semantic closure.",
            ))

    collision_blockers: list[str] = list(discovery_blockers) + adjacent_parse_blockers
    actual_labels: dict[str, list[tuple[str | None, str, str]]] = defaultdict(list)
    for definition_id, entry in canonical_definitions.items():
        for label in [entry["term"], *entry["aliases"]]:
            actual_labels[normalize(label)].append((definition_id, "canonical", entry["term"]))
    for registry, entry in adjacent_entries:
        for label in [entry["term"], *entry["aliases"]]:
            actual_labels[normalize(label)].append((entry["id"], registry["authority_class"], entry["term"]))
    for label, owners in sorted(actual_labels.items()):
        unique_owners = {(owner_id, authority) for owner_id, authority, _ in owners}
        if len(unique_owners) > 1:
            collision_blockers.append(block(
                "NORMALIZED_REGISTRY_COLLISION",
                f"Normalized label {label!r} is owned by multiple registry entries: {sorted(unique_owners, key=str)}",
                "definitions-governance",
                "Resolve the normalized label collision through Definitions Governance.",
            ))
    probe_label_owner: dict[str, str] = {}
    for probe in context["concept_probes"]:
        claimed_keys = {
            (match["definition_id"], match["authority_class"])
            for match in probe["claimed_matches"]
        }
        for label in [probe["term"], *probe["aliases"]]:
            normalized = normalize(label)
            if normalized in probe_label_owner and probe_label_owner[normalized] != probe["probe_id"]:
                collision_blockers.append(block(
                    "CROSS_PROBE_COLLISION",
                    f"Normalized label {normalized!r} is shared by probes {probe_label_owner[normalized]} and {probe['probe_id']}.",
                    "semantic-context-assessor",
                    "Merge or distinguish the colliding concept probes.",
                ))
            probe_label_owner[normalized] = probe["probe_id"]
            hidden = [owner for owner in actual_labels.get(normalized, []) if (owner[0], owner[1]) not in claimed_keys]
            if hidden:
                collision_blockers.append(block(
                    "UNDECLARED_NORMALIZED_MATCH",
                    f"Probe {probe['probe_id']} label {label!r} has undeclared normalized matches: {hidden}",
                    "semantic-context-assessor",
                    "Declare and assess every normalized registry match.",
                ))

    semantic_paths = {
        ref["path"]
        for role, ref in iter_material_refs(context)
        if role in {"canonical-source", "canonical-index", "candidate-registry", "local-glossary", "probe-evidence"}
    }
    semantic_source_blockers = [
        blocker_id for path in semantic_paths for blocker_id in source_blockers_by_path[path]
    ]
    semantic_dependencies = semantic_source_blockers + probe_blockers + adjacent_parse_blockers + (authority_blockers if not canonical_definitions else [])
    semantic_evaluable = not semantic_dependencies and bool(canonical_definitions)
    semantic_blockers: list[str] = []
    probe_results: list[dict[str, Any]] = []
    canonical_source_paths = {ref["path"] for ref in boundary["canonical_source_refs"]}
    for probe in context["concept_probes"]:
        local_causal: list[str] = []
        disposition = probe["proposed_disposition"]
        canonical_matches = [match for match in probe["claimed_matches"] if match["authority_class"] == "canonical"]
        if semantic_evaluable:
            for match in probe["claimed_matches"]:
                supported = False
                if (
                    match["authority_class"] == "canonical"
                and match["definition_id"] in canonical_definitions
                and match["source_ref"]["path"] in canonical_source_paths
                and match["authority_scope"] == boundary["canonical_scope"]
                and selector_names_definition(match, canonical_definitions[match["definition_id"]])
                ):
                    entry = canonical_definitions[match["definition_id"]]
                    supported = normalize(match["term"]) in {normalize(entry["term"]), *(normalize(alias) for alias in entry["aliases"])}
                elif match["authority_class"] in {"candidate", "local"}:
                    supported = any(
                        entry["id"] == match["definition_id"]
                        and normalize(entry["term"]) == normalize(match["term"])
                        and registry["source_ref"]["path"] == match["source_ref"]["path"]
                        and registry["authority_class"] == match["authority_class"]
                        for registry, entry in adjacent_entries
                    )
                if not supported:
                    local_causal.append(block(
                        "UNSUPPORTED_SEMANTIC_MATCH",
                        f"Probe {probe['probe_id']} claims an unsupported match {match['match_id']}.",
                        context["assessed_by"],
                        "Correct the claimed match or its exact source evidence.",
                    ))
            if disposition in {"reuse-existing", "specialize-existing", "canonical-change-proposal"}:
                canonical_ids = {match["definition_id"] for match in canonical_matches}
                if len(canonical_ids) != 1 or probe["proposed_basis_ids"] != sorted(canonical_ids):
                    local_causal.append(block(
                        "INVALID_SEMANTIC_BASIS",
                        f"Probe {probe['probe_id']} does not bind exactly one verified canonical basis.",
                        context["assessed_by"],
                        "Bind the proposal to one exact source-owned canonical definition ID.",
                    ))
            if disposition == "reuse-existing":
                labels = {normalize(probe["term"]), *(normalize(alias) for alias in probe["aliases"])}
                basis_labels = {
                    normalize(label)
                    for match in canonical_matches
                    for entry in [canonical_definitions.get(match["definition_id"], {})]
                    for label in [entry.get("term", ""), *entry.get("aliases", [])]
                }
                if not labels.intersection(basis_labels):
                    local_causal.append(block(
                        "UNSUPPORTED_REUSE",
                        f"Probe {probe['probe_id']} has no exact term or alias match with its canonical basis.",
                        context["assessed_by"],
                        "Use specialization or provide a verified exact canonical label match.",
                    ))
            elif disposition == "new-scoped-term" and probe["claimed_matches"]:
                local_causal.append(block(
                    "NEW_TERM_HAS_MATCH",
                    f"Probe {probe['probe_id']} is classified new but carries claimed matches.",
                    context["assessed_by"],
                    "Reclassify the probe or remove unsupported matches.",
                ))
            elif disposition == "specialize-existing" and canonical_matches:
                canonical_scope = canonical_matches[0]["authority_scope"]
                if SCOPE_RANK[probe["intended_scope"]["kind"]] <= SCOPE_RANK[canonical_scope["kind"]]:
                    local_causal.append(block(
                        "SPECIALIZATION_NOT_NARROWER",
                        f"Probe {probe['probe_id']} does not narrow its canonical authority scope.",
                        context["assessed_by"],
                        "Choose a strictly narrower intended scope or reuse the canonical term.",
                    ))
        if disposition == "blocked-conflict":
            local_causal.append(block(
                "DECLARED_SEMANTIC_CONFLICT",
                f"Assessor classified probe {probe['probe_id']} as a semantic conflict.",
                context["assessed_by"],
                "Resolve the conflict before Define authoring.",
            ))
        semantic_blockers.extend(local_causal)
        probe_results.append({
            "probe_id": probe["probe_id"],
            "matches": probe["claimed_matches"],
            "disposition": disposition,
            "basis_ids": probe["proposed_basis_ids"],
            "rationale": probe["assessment_rationale"],
            "causal_blocker_ids": sorted(set(local_causal)),
        })

    independent_blockers: list[str] = []
    owner_identities = [context["authored_by"], context["assessed_by"], canonical_owner, VALIDATOR_OWNER]
    duplicate_owners = sorted(item for item, count in Counter(owner_identities).items() if count > 1)
    if duplicate_owners:
        independent_blockers.append(block(
            "INDEPENDENT_OWNER_REQUIRED",
            f"Context author, semantic assessor, canonical owner, and validator owner must be distinct; repeated={duplicate_owners}.",
            "invoke-owner",
            "Assign an independent semantic assessor and rerun closure.",
        ))

    def refs_for(paths: Iterable[str]) -> list[dict[str, Any]]:
        result = []
        for path in sorted(set(paths)):
            data = observed_data.get(path)
            if data is not None:
                result.append(exact_ref(path, data))
        return result

    context_ref = exact_ref(context_rel, context_data)
    all_material_paths = [ref["path"] for _, ref in iter_material_refs(context)]
    checks: list[dict[str, Any]] = []

    def add_check(check_id: str, causal: Iterable[str], evidence: list[dict[str, Any]], dependencies: Iterable[str] = ()) -> None:
        causal_ids = sorted(set(causal))
        dependency_ids = sorted(set(dependencies))
        if causal_ids:
            status = "block"
        elif dependency_ids:
            status = "not_evaluable"
            causal_ids = dependency_ids
        else:
            status = "pass"
        checks.append({
            "check_id": check_id,
            "status": status,
            "evidence_refs": evidence,
            "causal_blocker_ids": causal_ids,
        })

    authority_dependencies = authority_source_blockers if authority_status == "ambiguous" and not authority_blockers else []
    add_check(CHECK_IDS[0], authority_blockers, refs_for(
        [ref["path"] for ref in boundary["canonical_source_refs"] + boundary["index_refs"] + boundary["resolution_evidence_refs"]]
    ), authority_dependencies)
    add_check(CHECK_IDS[1], source_blockers, refs_for(all_material_paths))
    add_check(CHECK_IDS[2], probe_blockers, [context_ref])
    parity_dependencies = canonical_index_source_blockers + authority_blockers if not canonical_definitions else []
    add_check(CHECK_IDS[3], parity_blockers, refs_for([ref["path"] for ref in boundary["canonical_source_refs"] + boundary["index_refs"]]), parity_dependencies)
    registry_paths_for_collision = declared_registry_paths
    registry_source_blockers = [
        blocker_id for path in registry_paths_for_collision for blocker_id in source_blockers_by_path[path]
    ]
    collision_dependencies = registry_source_blockers + (authority_blockers if not canonical_definitions else [])
    add_check(CHECK_IDS[4], collision_blockers, refs_for(list(discovered_registries) + [context_rel]), collision_dependencies)
    add_check(CHECK_IDS[5], semantic_blockers, [context_ref, *refs_for(declared_registry_paths)], semantic_dependencies)
    consumer_source_paths = {
        ref["path"]
        for role, ref in iter_material_refs(context)
        if role in {"consumer", "exclusion-evidence", "discovery-source"}
    }
    consumer_source_blockers = [
        blocker_id for path in consumer_source_paths for blocker_id in source_blockers_by_path[path]
    ]
    add_check(CHECK_IDS[6], consumer_blockers + discovery_blockers, refs_for(declared_consumer_paths), consumer_source_blockers)
    add_check(CHECK_IDS[7], independent_blockers, [context_ref])

    all_check_blockers = {blocker_id for check in checks for blocker_id in check["causal_blocker_ids"]}
    for result in probe_results:
        all_check_blockers.update(result["causal_blocker_ids"])
    unused_blockers = blocker_ids - all_check_blockers
    if unused_blockers:
        # This is an internal fail-closed condition; attach it to source freshness.
        checks[1]["status"] = "block"
        checks[1]["causal_blocker_ids"] = sorted(set(checks[1]["causal_blocker_ids"]) | unused_blockers)

    has_failure = any(check["status"] != "pass" for check in checks) or any(
        result["disposition"] == "blocked-conflict" or result["causal_blocker_ids"]
        for result in probe_results
    )
    if has_failure:
        outcome, route = "blocked", "stop"
    elif any(result["disposition"] == "canonical-change-proposal" for result in probe_results):
        outcome, route = "definitions-governance-required", "definitions-governance"
    else:
        outcome, route = "ready-for-define", "define-v3"

    receipt: dict[str, Any] = {
        "$schema": SCHEMA_URI,
        "schema_version": SCHEMA_VERSION,
        "receipt_id": "receipt:pending",
        "validator": {
            "identity": VALIDATOR_ID,
            "owner": VALIDATOR_OWNER,
            "path": VALIDATOR_PATH,
            "sha256": sha256_bytes(validator_data),
        },
        "schema_bindings": {
            "context_schema_ref": exact_ref(context_schema_rel, context_schema_data),
            "receipt_schema_ref": exact_ref(receipt_schema_rel, receipt_schema_data),
        },
        "context_ref": context_ref,
        "assessment": {
            "authored_by": context["authored_by"],
            "assessed_by": context["assessed_by"],
        },
        "claim_scope": context["discovery_contract"]["claim_scope"],
        "visibility_boundary": {
            "repository_root": ".",
            "discovery_roots": configured_discovery_roots,
            "public_roots": configured_public_roots,
            "source": "validator-invocation",
        },
        "discovery_snapshots": sorted(snapshots, key=lambda item: item["root_id"]),
        "authority_resolution": {
            "status": authority_status,
            "owner": canonical_owner,
            "canonical_source_refs": refs_for(ref["path"] for ref in boundary["canonical_source_refs"]),
            "index_refs": refs_for(ref["path"] for ref in boundary["index_refs"]),
            "evidence_refs": refs_for(ref["path"] for ref in boundary["resolution_evidence_refs"]),
        },
        "inspected_sources": sorted(inspections, key=lambda item: item["inspection_id"]),
        "probe_results": probe_results,
        "checks": checks,
        "blockers": sorted(blockers, key=lambda item: item["blocker_id"]),
        "outcome": outcome,
        "next_route": route,
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    identity_material = {key: value for key, value in receipt.items() if key not in {"receipt_id", "receipt_digest"}}
    receipt["receipt_id"] = f"receipt:{sha256_bytes(canonical_bytes(identity_material))[:32]}"
    digest_material = {key: value for key, value in receipt.items() if key != "receipt_digest"}
    receipt["receipt_digest"] = sha256_bytes(canonical_bytes(digest_material))

    try:
        validate_schema(receipt, receipt_schema, "receipt")
    except InvocationError as exc:
        if _return_receipt:
            raise InvocationError(f"internally generated receipt is invalid: {exc}") from exc
        print(f"error: internally generated receipt is invalid: {exc}", file=sys.stderr)
        return 2

    if _return_receipt:
        return receipt

    output_data = canonical_bytes(receipt)
    try:
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(output_data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        print(f"error: output already exists: {output}", file=sys.stderr)
        return 2
    except OSError as exc:
        try:
            output.unlink(missing_ok=True)
        except OSError:
            pass
        print(f"error: could not create receipt exclusively: {exc}", file=sys.stderr)
        return 2

    print(f"{outcome}: {output}")
    return 0 if outcome == "ready-for-define" else 1


def evaluate_context(
    *,
    context_path: Path,
    repository_root: Path,
    context_schema_path: Path,
    receipt_schema_path: Path,
    discovery_roots: Iterable[str],
    public_roots: Iterable[str] = (),
) -> dict[str, Any]:
    """Replay semantic closure entirely in memory.

    The returned object is byte-identical to the receipt the CLI would create
    for the same inputs.  The API performs no filesystem mutation and raises
    :class:`InvocationError` for invocation failures instead of printing or
    returning a process exit status.
    """

    discovery_roots = tuple(discovery_roots)
    public_roots = tuple(public_roots)
    if not discovery_roots:
        raise InvocationError("in-memory semantic closure requires at least one discovery root")
    arguments = [
        str(context_path),
        "--repository-root",
        str(repository_root),
        "--context-schema",
        str(context_schema_path),
        "--receipt-schema",
        str(receipt_schema_path),
    ]
    for root in discovery_roots:
        arguments.extend(["--discovery-root", root])
    for root in public_roots:
        arguments.extend(["--public-root", root])
    # argparse requires a destination, but evaluation returns before every
    # output-path check and write.
    arguments.extend(["--output", str(repository_root / ".define-semantic-closure.in-memory.json")])
    result = main(arguments, _return_receipt=True)
    if not isinstance(result, dict):  # pragma: no cover - defensive boundary
        raise InvocationError("in-memory semantic closure did not return a receipt")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
