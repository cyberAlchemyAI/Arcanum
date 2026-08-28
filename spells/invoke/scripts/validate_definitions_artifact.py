#!/usr/bin/env python3
"""Validate one definition artifact beyond portable JSON Schema constraints."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_errors(document: Any, schema: dict[str, Any]) -> list[str]:
    return [
        f"schema invalid at {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def _headings(text: str) -> list[str]:
    return [
        match.group(1).strip().rstrip("#").strip()
        for match in re.finditer(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    ]


def _resolve_json_pointer(document: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise ValueError("JSON pointer must start with '/'")
    current = document
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise KeyError(token)
    return current


def _resolve_yaml_path(document: Any, selector: str) -> Any:
    tokens: list[str | int] = []
    for segment in selector.split("."):
        match = re.fullmatch(r"([^\[\]]+)((?:\[[0-9]+\])*)", segment)
        if not match:
            raise ValueError(f"unsupported YAML path segment: {segment}")
        tokens.append(match.group(1))
        tokens.extend(int(value) for value in re.findall(r"\[([0-9]+)\]", match.group(2)))
    current = document
    for token in tokens:
        current = current[token]
    return current


def _verify_selector(path: Path, source_ref: dict[str, Any]) -> str | None:
    selector_type = source_ref["selector_type"]
    selector = source_ref["selector"]
    text = path.read_text(encoding="utf-8")
    if selector_type == "line-span":
        start = source_ref["start_line"]
        end = source_ref["end_line"]
        line_count = len(text.splitlines())
        if not isinstance(start, int) or not isinstance(end, int):
            return "line-span selector is missing integer bounds"
        if start > end:
            return f"line-span selector is reversed: {start}>{end}"
        if end > line_count:
            return f"line-span selector ends after line {line_count}: {end}"
        return None
    if selector_type == "heading":
        headings = _headings(text)
        if selector not in headings and _slug(selector) not in {_slug(item) for item in headings}:
            return f"heading selector does not resolve: {selector}"
        return None
    if selector_type == "anchor":
        anchor = selector.lstrip("#")
        if anchor not in {_slug(item) for item in _headings(text)}:
            return f"anchor selector does not resolve: {selector}"
        return None
    if selector_type == "symbol":
        if selector not in text:
            return f"symbol selector does not resolve: {selector}"
        return None
    if selector_type == "json-pointer":
        try:
            _resolve_json_pointer(json.loads(text), selector)
        except (ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
            return f"JSON pointer does not resolve: {selector}: {error}"
        return None
    if selector_type == "yaml-path":
        try:
            import yaml

            _resolve_yaml_path(yaml.safe_load(text), selector)
        except (ImportError, ValueError, KeyError, IndexError, TypeError) as error:
            return f"YAML path does not resolve: {selector}: {error}"
        return None
    return f"unsupported selector type: {selector_type}"


def _resolve_local_path(repo_root: Path, value: str) -> Path:
    if value.startswith("https://"):
        raise ValueError("remote source verification is unsupported in the deterministic compiler")
    resolved = (repo_root / value).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as error:
        raise ValueError("source path escapes repository") from error
    return resolved


def _inline(value: str) -> str:
    return " ".join(value.replace("|", "\\|").split())


def _section(title: str, value: str | None) -> str:
    if value is None:
        return ""
    return f"### {title}\n\n{value.strip()}\n\n"


def render_definitions_markdown(document: dict[str, Any]) -> str:
    lines = [
        f"# {document['title']}",
        "",
        f"- Registry: `{document['registry_id']}`",
        f"- Status: `{document['registry_status']}`",
        f"- Owner route: `{document['owner_route']}`",
        f"- Authority scope: `{document['authority_scope']['kind']}:{document['authority_scope']['ref']}`",
        f"- Visibility: `{document['visibility']}`",
        f"- Authority effect: `{document['authority_effect']}`",
        "",
    ]
    for definition in document["definitions"]:
        aliases = ", ".join(f"`{item}`" for item in definition["aliases"]) or "none"
        lines.extend(
            [
                f"## {definition['id']}: {definition['term']}",
                "",
                f"- Status: `{definition['status']}`",
                f"- Version: `{definition['definition_version']}`",
                f"- Aliases: {aliases}",
                f"- Source kinds: {', '.join(f'`{item}`' for item in definition['source_kinds'])}",
                "",
                _section("Normative Voice", definition["voices"]["normative"]).rstrip(),
                _section("Formal Voice", definition["voices"]["formal"]).rstrip(),
                _section("Operational Voice", definition["voices"]["operational"]).rstrip(),
                _section("Plain-Language Voice", definition["voices"]["plain_language"]).rstrip(),
                _section("Domain-Context Voice", definition["voices"]["domain_context"]).rstrip(),
                "### Boundary",
                "",
            ]
        )
        for key, label in (("includes", "Includes"), ("excludes", "Excludes"), ("conditions", "Conditions")):
            values = definition["boundary"][key]
            lines.append(f"#### {label}")
            lines.append("")
            lines.extend(f"- {item}" for item in values) if values else lines.append("- none")
            lines.append("")
        if definition["notation"]:
            lines.extend(["### Notation", "", "| Symbol | Meaning |", "| --- | --- |"])
            lines.extend(f"| {_inline(item['symbol'])} | {_inline(item['meaning'])} |" for item in definition["notation"])
            lines.append("")
        lines.extend(["### Sources", "", "| Role | Path | Selector | SHA-256 | Size |", "| --- | --- | --- | --- | ---: |"])
        for source in definition["source_refs"]:
            digest = source["sha256"] or "not-bound"
            size = source["size"] if source["size"] is not None else "-"
            lines.append(
                f"| {source['role']} | `{source['path']}` | {source['selector_type']}: `{_inline(source['selector'])}` | `{digest}` | {size} |"
            )
        lines.extend(["", "### Primary Consumers", ""])
        lines.extend(f"- `{item}`" for item in definition["primary_consumers"])
        lines.append("")
        if definition["relations"]:
            lines.extend(["### Related Definitions", ""])
            lines.extend(f"- `{item['type']}` → `{item['id']}`" for item in definition["relations"])
            lines.append("")
        for label, key in (("Use Carefully", "use_carefully"), ("Misuse Warning", "misuse_warning"), ("Promotion Boundary", "promotion_boundary")):
            value = definition[key]
            if value is not None:
                lines.extend([f"### {label}", "", value, ""])
        if definition["challenge_contract"] is not None:
            lines.extend(
                [
                    "### Challenge Contract",
                    "",
                    "```json",
                    json.dumps(definition["challenge_contract"], indent=2, sort_keys=True, ensure_ascii=False),
                    "```",
                    "",
                ]
            )
        if definition["structural_schema"] is not None:
            structural = definition["structural_schema"]
            lines.extend(
                [
                    "### Structural Schema",
                    "",
                    f"- Handle: `{structural['handle']}`",
                    f"- Status: `{structural['status']}`",
                    f"- Reference: `{structural['ref'] or 'none'}`",
                    "",
                ]
            )
        lines.extend(["### Drift Route", "", f"`{definition['drift_route']}`", ""])
    return "\n".join(item for item in lines if item is not None).rstrip() + "\n"


def render_glossary_markdown(document: dict[str, Any]) -> str:
    rows = [
        "# Glossary",
        "",
        "| ID | Term | Status | Plain-language definition | Aliases |",
        "| --- | --- | --- | --- | --- |",
    ]
    for definition in document["definitions"]:
        aliases = ", ".join(definition["aliases"]) or "-"
        rows.append(
            f"| `{definition['id']}` | {_inline(definition['term'])} | {definition['status']} | "
            f"{_inline(definition['voices']['plain_language'])} | {_inline(aliases)} |"
        )
    return "\n".join(rows) + "\n"


def validate_artifact(
    document: dict[str, Any],
    repo_root: Path,
    schema: dict[str, Any],
    bundle_root: Path | None = None,
) -> list[str]:
    errors = schema_errors(document, schema)
    if errors:
        return errors

    definitions = document["definitions"]
    by_id: dict[str, dict[str, Any]] = {}
    labels: dict[str, tuple[str, str]] = {}
    for definition in definitions:
        definition_id = definition["id"]
        if definition_id in by_id:
            errors.append(f"duplicate definition id: {definition_id}")
        by_id[definition_id] = definition
        for label in [definition["term"], *definition["aliases"]]:
            if not label.strip():
                errors.append(f"{definition_id} has an empty term or alias after trimming")
            normalized = " ".join(unicodedata.normalize("NFKC", label).casefold().split())
            owner = labels.get(normalized)
            if owner is not None:
                errors.append(
                    "term or alias collision: "
                    f"{label!r} on {definition_id} normalizes to {owner[1]!r} on {owner[0]}"
                )
            else:
                labels[normalized] = (definition_id, label)

    public_root = repo_root / "arcanum" if (repo_root / "arcanum").is_dir() else repo_root
    for definition in definitions:
        definition_id = definition["id"]
        for voice, value in definition["voices"].items():
            if value is not None and not value.strip():
                errors.append(f"{definition_id} voice is empty after trimming: {voice}")
        for relation in definition["relations"]:
            if relation["id"] == definition_id:
                errors.append(f"{definition_id} has a self relation: {relation['type']}")
            if relation["id"] not in by_id:
                errors.append(f"{definition_id} relation target is unresolved: {relation['id']}")
        for target in definition["supersedes"]:
            if target == definition_id:
                errors.append(f"{definition_id} cannot supersede itself")
            if target not in by_id:
                errors.append(f"{definition_id} supersedes unresolved definition: {target}")
        successor = definition["superseded_by"]
        if successor is not None:
            if successor == definition_id:
                errors.append(f"{definition_id} cannot be superseded by itself")
            elif successor not in by_id:
                errors.append(f"{definition_id} successor is unresolved: {successor}")
            elif definition_id not in by_id[successor]["supersedes"]:
                errors.append(f"{definition_id} successor {successor} does not reciprocate supersedes")

        for index, source_ref in enumerate(definition["source_refs"]):
            label = f"{definition_id} source_refs[{index}]"
            try:
                path = _resolve_local_path(repo_root, source_ref["path"])
            except ValueError as error:
                errors.append(f"{label}: {error}")
                continue
            if not path.is_file():
                errors.append(f"{label}: source file is missing: {source_ref['path']}")
                continue
            if document["visibility"] == "public":
                try:
                    path.relative_to(public_root.resolve())
                except ValueError:
                    errors.append(f"{label}: public registry source is outside the public repository root")
            data = path.read_bytes()
            if source_ref["sha256"] is not None and hashlib.sha256(data).hexdigest() != source_ref["sha256"]:
                errors.append(f"{label}: source SHA-256 is stale")
            if source_ref["size"] is not None and len(data) != source_ref["size"]:
                errors.append(f"{label}: source size is stale")
            selector_error = _verify_selector(path, source_ref)
            if selector_error:
                errors.append(f"{label}: {selector_error}")

        structural = definition["structural_schema"]
        if structural is not None and structural["status"] == "machine-checkable":
            try:
                schema_path = _resolve_local_path(repo_root, structural["ref"])
                structural_document = load_json(schema_path)
                Draft202012Validator.check_schema(structural_document)
            except (ValueError, OSError, json.JSONDecodeError) as error:
                errors.append(f"{definition_id} structural schema is invalid: {error}")

    if bundle_root is not None:
        expected_views = {
            "DEFINITIONS.md": render_definitions_markdown(document),
            "GLOSSARY.md": render_glossary_markdown(document),
        }
        for name, expected in expected_views.items():
            path = bundle_root / name
            if not path.is_file():
                errors.append(f"generated view is missing: {name}")
            elif path.read_text(encoding="utf-8") != expected:
                errors.append(f"generated view drift: {name}")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--bundle-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        artifact = load_json(args.artifact)
        schema = load_json(args.schema)
        errors = validate_artifact(
            artifact,
            args.repo_root.resolve(),
            schema,
            args.bundle_root.resolve() if args.bundle_root else None,
        )
    except (OSError, json.JSONDecodeError) as error:
        errors = [str(error)]
    result = {
        "schema_version": "invoke.definitions-validation.v1",
        "result": "pass" if not errors else "block",
        "errors": errors,
        "authority_effect": "none",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
