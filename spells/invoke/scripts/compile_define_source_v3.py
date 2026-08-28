#!/usr/bin/env python3
"""Compile one closure-bound Define v3 source into an atomic candidate bundle.

The producer has no activation or promotion authority.  It replays the exact
W1 semantic closure against the caller-supplied discovery boundary before it
derives any output, and publishes only a complete, validator-clean bundle.
"""

from __future__ import annotations

import argparse
import copy
import ctypes
import errno
import hashlib
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable

from jsonschema import Draft202012Validator, RefResolver


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_define_semantic_closure import (  # noqa: E402
    DuplicateKeyError,
    InvocationError,
    SCOPE_RANK,
    canonical_bytes,
    evaluate_context,
    exact_ref as material_ref,
    json_object,
    normalize,
    repo_path,
    sha256_bytes,
)


IDENTITY = "invoke.compile-define-source.v3"
PROFILE = "invoke.generic-definitions-baseline.v3"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_define_source_v3.py"
SCHEMA_FILES = {
    "source": "define-source-v3.schema.json",
    "profile": "define-profile-v3.schema.json",
    "definitions_v1": "definitions.schema.json",
    "definitions_v2": "definitions-v2.schema.json",
    "result": "define-result-v3.schema.json",
}
EXPECTED_SCHEMA_IDS = {
    "source": "https://arcanum.dev/schemas/invoke/define-source/v3",
    "profile": "https://arcanum.dev/schemas/invoke/define-profile/v3",
    "definitions_v1": "https://arcanum.dev/schemas/invoke/definitions/v1",
    "definitions_v2": "https://arcanum.dev/schemas/invoke/definitions/v2",
    "result": "https://arcanum.dev/schemas/invoke/define-result/v3",
}
OUTPUT_ORDER = (
    ("semantic_context", "semantic-context"),
    ("semantic_closure_receipt", "semantic-closure-receipt"),
    ("spec", "spec"),
    ("definitions", "definitions"),
    ("definitions_view", "definitions-view"),
    ("glossary", "glossary"),
    ("layering", "layering"),
    ("template_selection", "template-selection"),
    ("dispatch_trace", "dispatch-trace"),
    ("distill", "distill"),
    ("identity_denominator", "identity-denominator"),
    ("transport", "transport"),
)


class CompileError(ValueError):
    """A fail-closed v3 compilation error."""


def load_json_bytes(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=json_object)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise CompileError(f"{label} is not strict JSON: {exc}") from exc


def load_json(path: Path, label: str) -> tuple[Any, bytes]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CompileError(f"cannot read {label}: {exc}") from exc
    return load_json_bytes(data, label), data


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_without(document: dict[str, Any], field: str) -> str:
    projected = copy.deepcopy(document)
    projected.pop(field, None)
    return sha256_bytes(canonical_bytes(projected).rstrip(b"\n"))


def relative_file(root: Path, path: Path, label: str) -> tuple[Path, str]:
    try:
        resolved = path.resolve(strict=True)
        relative = resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise CompileError(f"{label} is missing or escapes repository") from exc
    if not resolved.is_file():
        raise CompileError(f"{label} is not a regular file")
    return resolved, relative.as_posix()


def exact_path_ref(root: Path, path: Path, label: str) -> dict[str, Any]:
    resolved, relative = relative_file(root, path, label)
    return material_ref(relative, resolved.read_bytes())


def verify_exact_ref(root: Path, ref: dict[str, Any], label: str) -> tuple[Path, bytes]:
    try:
        path = repo_path(root, ref["path"])
        data = path.read_bytes()
    except (OSError, ValueError, KeyError) as exc:
        raise CompileError(f"{label} is missing or escapes repository: {exc}") from exc
    if material_ref(ref["path"], data) != ref:
        raise CompileError(f"{label} exact reference is stale")
    return path, data


def schema_errors(
    document: Any,
    schema: dict[str, Any],
    store: dict[str, Any],
) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
        resolver = RefResolver.from_schema(schema, store=store)
        errors = Draft202012Validator(schema, resolver=resolver).iter_errors(document)
        return [
            f"/{'/'.join(map(str, error.absolute_path))}: {error.message}"
            for error in sorted(errors, key=lambda item: tuple(str(part) for part in item.absolute_path))
        ]
    except Exception as exc:  # jsonschema may raise on an unresolved local ref
        raise CompileError(f"schema evaluation failed: {exc}") from exc


def require_schema_valid(
    document: Any,
    schema: dict[str, Any],
    store: dict[str, Any],
    label: str,
) -> None:
    errors = schema_errors(document, schema, store)
    if errors:
        raise CompileError(f"{label} schema invalid: {'; '.join(errors)}")


def project_definition_source(ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": ref["path"],
        "sha256": ref["sha256"],
        "size": ref["size"],
        "selector_type": ref["selector_type"],
        "selector": ref["selector"],
        "visibility": ref["visibility"],
    }


def project_probe_source(ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": ref["path"],
        "sha256": ref["sha256"],
        "size": ref["size"],
        "selector_type": ref["selector_type"],
        "selector": ref["selector"],
        "visibility": ref["visibility"],
    }


def project_authority_ref(ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": ref["path"],
        "sha256": ref["sha256"],
        "size": ref["size"],
        "selector": ref["selector"],
        "visibility": ref["visibility"],
    }


def validate_projection(
    source: dict[str, Any],
    context: dict[str, Any],
    closure: dict[str, Any],
) -> None:
    probes = context["concept_probes"]
    results = closure["probe_results"]
    applications = source["semantic_applications"]
    if [item["probe_id"] for item in probes] != [item["probe_id"] for item in results]:
        raise CompileError("closure probe order does not equal semantic context probe order")
    if [item["probe_id"] for item in probes] != [item["probe_id"] for item in applications]:
        raise CompileError("semantic applications do not exactly cover probes in source order")

    registry = source["definition_registry"]
    if registry["authority_scope"] != context["target"]["authority_scope"]:
        raise CompileError("definition registry scope does not equal semantic target scope")
    for probe in probes:
        if probe["intended_scope"] != context["target"]["authority_scope"]:
            raise CompileError(
                f"probe intended scope differs from semantic target scope for {probe['probe_id']}"
            )
    if registry["visibility"] != context["target"]["visibility"]:
        raise CompileError("definition registry visibility does not equal semantic target visibility")
    if registry["owner_route"] != closure["authority_resolution"]["owner"]:
        raise CompileError("definition registry owner route does not equal resolved authority owner")

    definitions = registry["definitions"]
    bindings = registry["authority_bindings"]
    definition_by_id = {item["id"]: item for item in definitions}
    binding_by_id = {item["binding_id"]: item for item in bindings}
    if len(definition_by_id) != len(definitions):
        raise CompileError("candidate definition IDs are not unique")
    if len(binding_by_id) != len(bindings):
        raise CompileError("authority binding IDs are not unique")

    claimed_definition_ids = [
        definition_id
        for application in applications
        for definition_id in application["definition_ids"]
    ]
    claimed_binding_ids = [
        binding_id
        for application in applications
        for binding_id in application["authority_binding_ids"]
    ]
    if Counter(claimed_definition_ids) != Counter({key: 1 for key in definition_by_id}):
        raise CompileError("applications do not assign every candidate definition to exactly one probe")
    if Counter(claimed_binding_ids) != Counter({key: 1 for key in binding_by_id}):
        raise CompileError("applications do not assign every authority binding to exactly one probe")

    normalized_labels: dict[str, tuple[str, str]] = {}
    for definition in definitions:
        for kind, label in [("term", definition["term"]), *[("alias", item) for item in definition["aliases"]]]:
            key = normalize(label)
            prior = normalized_labels.get(key)
            if prior is not None:
                raise CompileError(
                    f"normalized candidate label collision between {prior[1]} and {definition['id']}"
                )
            normalized_labels[key] = (kind, definition["id"])
        for relation in definition["relations"]:
            if relation["id"] == definition["id"]:
                raise CompileError(f"candidate definition {definition['id']} has a self relation")
            if relation["id"] not in definition_by_id:
                raise CompileError(
                    f"candidate definition {definition['id']} relates to an unknown candidate {relation['id']}"
                )

    for probe, result, application in zip(probes, results, applications, strict=True):
        disposition = result["disposition"]
        if application["disposition"] != disposition:
            raise CompileError(f"application disposition differs from closure for {probe['probe_id']}")
        if application["rationale"] != result["rationale"]:
            raise CompileError(f"application rationale differs from closure for {probe['probe_id']}")
        definition_ids = application["definition_ids"]
        binding_ids = application["authority_binding_ids"]
        if disposition == "reuse-existing" and (definition_ids or len(binding_ids) != 1):
            raise CompileError(f"reuse application has the wrong ownership shape for {probe['probe_id']}")
        if disposition == "new-scoped-term" and (len(definition_ids) != 1 or binding_ids):
            raise CompileError(f"new-term application has the wrong ownership shape for {probe['probe_id']}")
        if disposition == "specialize-existing" and (len(definition_ids) != 1 or len(binding_ids) != 1):
            raise CompileError(f"specialization application has the wrong ownership shape for {probe['probe_id']}")

        for definition_id in definition_ids:
            definition = definition_by_id[definition_id]
            if definition["term"] != probe["term"] or definition["aliases"] != probe["aliases"]:
                raise CompileError(f"candidate term or aliases differ from probe {probe['probe_id']}")
            expected_refs = [project_probe_source(item) for item in probe["evidence_refs"]]
            actual_refs = [project_definition_source(item) for item in definition["source_refs"]]
            if actual_refs != expected_refs:
                raise CompileError(f"candidate source references differ from probe {probe['probe_id']}")
            if any(
                item["start_line"] is not None or item["end_line"] is not None
                for item in definition["source_refs"]
            ):
                raise CompileError(f"candidate source range adds undeclared evidence for {probe['probe_id']}")

        for binding_id in binding_ids:
            binding = binding_by_id[binding_id]
            if binding["probe_id"] != probe["probe_id"]:
                raise CompileError(f"authority binding {binding_id} belongs to a different probe")
            expected_role = "reuse" if disposition == "reuse-existing" else "specialization-basis"
            if binding["role"] != expected_role:
                raise CompileError(f"authority binding {binding_id} has the wrong role")
            matches = result["matches"]
            if len(matches) != 1 or result["basis_ids"] != [matches[0]["definition_id"]]:
                raise CompileError(f"closure does not name one exact canonical basis for {probe['probe_id']}")
            match = matches[0]
            expected_binding = {
                "definition_id": match["definition_id"],
                "term": match["term"],
                "authority_scope": match["authority_scope"],
                "authority_ref": project_authority_ref(match["source_ref"]),
            }
            actual_binding = {key: binding[key] for key in expected_binding}
            if actual_binding != expected_binding:
                raise CompileError(f"authority binding {binding_id} differs from the canonical match")
            if disposition == "specialize-existing":
                target_kind = context["target"]["authority_scope"]["kind"]
                basis_kind = binding["authority_scope"]["kind"]
                if SCOPE_RANK[target_kind] <= SCOPE_RANK[basis_kind]:
                    raise CompileError(f"specialization {probe['probe_id']} does not narrow authority scope")


def validate_structural_schemas(
    root: Path,
    definitions: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Validate and exact-bind every machine-checkable candidate schema."""

    refs: list[dict[str, Any]] = []
    for definition in definitions:
        structural = definition["structural_schema"]
        if structural is None or structural["status"] != "machine-checkable":
            continue
        try:
            schema_path = repo_path(root, structural["ref"])
            schema = load_json_bytes(
                schema_path.read_bytes(),
                f"structural schema for {definition['id']}",
            )
            Draft202012Validator.check_schema(schema)
            refs.append(
                {
                    "definition_id": definition["id"],
                    **exact_path_ref(
                        root,
                        schema_path,
                        f"structural schema for {definition['id']}",
                    ),
                }
            )
        except Exception as exc:
            raise CompileError(
                f"candidate definition {definition['id']} structural schema is invalid: {exc}"
            ) from exc
    return refs


def build_definitions_artifact(
    source: dict[str, Any],
    context_ref: dict[str, Any],
    closure_ref: dict[str, Any],
    definitions_schema: dict[str, Any],
) -> dict[str, Any]:
    registry = source["definition_registry"]
    return {
        "$schema": definitions_schema["$id"],
        "schema_version": "definitions/v2",
        "registry_id": registry["registry_id"],
        "title": registry["title"],
        "registry_status": "candidate",
        "owner_route": registry["owner_route"],
        "authority_kind": "kind.definition",
        "authority_scope": copy.deepcopy(registry["authority_scope"]),
        "visibility": registry["visibility"],
        "semantic_evidence": {
            "context_ref": copy.deepcopy(context_ref),
            "closure_receipt_ref": copy.deepcopy(closure_ref),
        },
        "definitions": copy.deepcopy(registry["definitions"]),
        "authority_bindings": copy.deepcopy(registry["authority_bindings"]),
        "semantic_applications": copy.deepcopy(source["semantic_applications"]),
        "authority_effect": "none",
    }


def semantic_outcome(artifact: dict[str, Any]) -> str:
    if artifact["definitions"] and artifact["authority_bindings"]:
        return "mixed"
    if artifact["definitions"]:
        return "candidate-definitions"
    return "reference-only"


def render_spec(source: dict[str, Any], context: dict[str, Any]) -> bytes:
    declarations = "\n\n".join(
        f"## {item['title']}\n\n{item['statement']}" for item in source["spec_declarations"]
    )
    return (
        f"# {context['target']['id']}\n\n"
        f"{context['target']['objective']}\n\n"
        f"{declarations}\n"
    ).encode("utf-8")


def render_definitions(artifact: dict[str, Any]) -> bytes:
    lines = [
        f"# {artifact['title']}",
        "",
        f"Status: {artifact['registry_status']}",
        f"Owner route: {artifact['owner_route']}",
        f"Scope: {artifact['authority_scope']['kind']}:{artifact['authority_scope']['ref']}",
        "Authority effect: none",
    ]
    if artifact["definitions"]:
        lines.extend(["", "## Candidate Definitions"])
        for definition in artifact["definitions"]:
            lines.extend(
                [
                    "",
                    f"### {definition['id']}: {definition['term']}",
                    "",
                    f"Aliases: {', '.join(definition['aliases']) or 'none'}",
                    "Status: candidate",
                    "",
                    "#### Normative voice",
                    "",
                    definition["voices"]["normative"],
                    "",
                    "#### Plain-language voice",
                    "",
                    definition["voices"]["plain_language"],
                    "",
                    "#### Domain context",
                    "",
                    definition["voices"]["domain_context"],
                    "",
                    "#### Evidence",
                    "",
                ]
            )
            lines.extend(
                f"- {ref['role']}: `{ref['path']}` ({ref['selector_type']} `{ref['selector']}`; sha256 `{ref['sha256']}`)"
                for ref in definition["source_refs"]
            )
    if artifact["authority_bindings"]:
        lines.extend(
            [
                "",
                "## Canonical Authority Bindings",
                "",
                "These entries are exact references. Canonical normative prose remains at the authority source and is not copied here.",
                "",
                "| Binding | Probe | Role | Canonical ID | Term | Scope | Authority source |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for binding in artifact["authority_bindings"]:
            ref = binding["authority_ref"]
            lines.append(
                f"| {binding['binding_id']} | {binding['probe_id']} | {binding['role']} | "
                f"{binding['definition_id']} | {binding['term']} | "
                f"{binding['authority_scope']['kind']}:{binding['authority_scope']['ref']} | "
                f"`{ref['path']}` selector `{ref['selector']}` sha256 `{ref['sha256']}` |"
            )
    lines.extend(
        [
            "",
            "## Semantic Applications",
            "",
            "| Probe | Disposition | Candidate definitions | Authority bindings |",
            "| --- | --- | --- | --- |",
        ]
    )
    for application in artifact["semantic_applications"]:
        lines.append(
            f"| {application['probe_id']} | {application['disposition']} | "
            f"{', '.join(application['definition_ids']) or 'none'} | "
            f"{', '.join(application['authority_binding_ids']) or 'none'} |"
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_glossary(artifact: dict[str, Any]) -> bytes:
    lines = [
        "# Glossary",
        "",
        "| Term | Status | Meaning or authority reference |",
        "| --- | --- | --- |",
    ]
    for definition in artifact["definitions"]:
        lines.append(
            f"| {definition['term']} | candidate | {definition['voices']['plain_language']} |"
        )
    for binding in artifact["authority_bindings"]:
        ref = binding["authority_ref"]
        lines.append(
            f"| {binding['term']} | canonical reference ({binding['role']}) | "
            f"See `{ref['path']}` selector `{ref['selector']}`; normative prose is not copied. |"
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def derived_output_bytes(
    source: dict[str, Any],
    context: dict[str, Any],
    context_data: bytes,
    closure_data: bytes,
    artifact: dict[str, Any],
) -> dict[str, bytes]:
    expected_layer = (
        "IMPLEMENTATION-LAYERING.md"
        if source["layering"]["kind"] == "seed"
        else "LAYERING-GAP.md"
    )
    if source["output_contracts"]["layering"] != expected_layer:
        raise CompileError("layering output contract does not match the layering classification")
    if source["layering"]["kind"] == "seed":
        layering = (
            "# Implementation Layering Seed\n\n"
            f"- Decision: {source['layering']['decision']}\n"
            f"- Minimum unit: {source['layering']['minimum_unit']}\n"
        ).encode("utf-8")
    else:
        layering = (
            "# Implementation Layering Gap\n\n"
            f"{source['layering']['rationale']}\n"
        ).encode("utf-8")
    documents = {
        source["output_contracts"]["template_selection"]: {
            "schema_version": "invoke.define-template-selection.v3",
            **source["template_selection"],
            "result": "pass",
        },
        source["output_contracts"]["dispatch_trace"]: {
            "schema_version": "invoke.define-dispatch-trace.v3",
            **source["dispatch_trace"],
            "result": "pass",
        },
        source["output_contracts"]["distill"]: {
            "schema_version": "invoke.define-distill-classification.v3",
            **source["distill"],
            "result": "pass",
        },
        source["output_contracts"]["identity_denominator"]: {
            "schema_version": "invoke.define-identity-classification.v3",
            **source["identity_denominator"],
            "result": "pass",
        },
        source["output_contracts"]["transport"]: {
            "schema_version": "invoke.define-transport.v3",
            "policy": source["transport_policy"],
            "result": "no-op",
            "authority_effect": "none",
        },
    }
    outputs = {
        source["output_contracts"]["semantic_context"]: context_data,
        source["output_contracts"]["semantic_closure_receipt"]: closure_data,
        source["output_contracts"]["spec"]: render_spec(source, context),
        source["output_contracts"]["definitions"]: pretty_bytes(artifact),
        source["output_contracts"]["definitions_view"]: render_definitions(artifact),
        source["output_contracts"]["glossary"]: render_glossary(artifact),
        expected_layer: layering,
    }
    outputs.update({name: pretty_bytes(document) for name, document in documents.items()})
    if len(outputs) != 12:
        raise CompileError("output contracts do not resolve to twelve distinct pre-receipt paths")
    return outputs


def validate_staged_outputs(
    stage: Path,
    expected: dict[str, bytes],
    artifact: dict[str, Any],
    source: dict[str, Any],
    context: dict[str, Any],
    closure: dict[str, Any],
    definitions_schema: dict[str, Any],
    store: dict[str, Any],
) -> None:
    names = sorted(path.name for path in stage.iterdir() if path.is_file())
    if names != sorted(expected):
        raise CompileError("staging directory does not contain the exact twelve output files")
    if any(path.is_dir() for path in stage.iterdir()):
        raise CompileError("staging directory contains an unexpected subdirectory")
    for name, data in expected.items():
        if (stage / name).read_bytes() != data:
            raise CompileError(f"late output drift detected in {name}")
    staged_artifact = load_json_bytes(
        (stage / source["output_contracts"]["definitions"]).read_bytes(),
        "staged DEFINITIONS.json",
    )
    if staged_artifact != artifact:
        raise CompileError("staged definitions payload differs from the derived artifact")
    require_schema_valid(staged_artifact, definitions_schema, store, "staged definitions")
    staged_source = copy.deepcopy(source)
    staged_source["definition_registry"]["definitions"] = copy.deepcopy(staged_artifact["definitions"])
    staged_source["definition_registry"]["authority_bindings"] = copy.deepcopy(staged_artifact["authority_bindings"])
    staged_source["semantic_applications"] = copy.deepcopy(staged_artifact["semantic_applications"])
    validate_projection(staged_source, context, closure)
    if render_definitions(staged_artifact) != (stage / source["output_contracts"]["definitions_view"]).read_bytes():
        raise CompileError("definitions Markdown does not equal a clean deterministic render")
    if render_glossary(staged_artifact) != (stage / source["output_contracts"]["glossary"]).read_bytes():
        raise CompileError("glossary Markdown does not equal a clean deterministic render")


def publish_no_replace(stage: Path, output_dir: Path) -> None:
    """Atomically rename one directory without replacing a competing target."""

    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    if renameat2 is None:  # pragma: no cover - fail closed on non-Linux hosts
        raise CompileError("atomic no-replace directory publication is unavailable")
    renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        -100,
        os.fsencode(stage),
        -100,
        os.fsencode(output_dir),
        1,
    )
    if result == 0:
        return
    error = ctypes.get_errno()
    if error == errno.EEXIST:
        raise CompileError("output directory appeared during publication and was not overwritten")
    if error in {errno.EINVAL, errno.ENOSYS, errno.EOPNOTSUPP}:
        # Some WSL and older filesystems expose renameat2 but reject its
        # no-replace flag. Serialize cooperating publishers with an exclusive
        # sibling lock, then recheck the target immediately before a same-
        # filesystem rename. Existing targets are never removed.
        lock = output_dir.parent / f".{output_dir.name}.publish-lock"
        descriptor: int | None = None
        try:
            descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            if output_dir.exists() or output_dir.is_symlink():
                raise CompileError("output directory appeared during publication and was not overwritten")
            os.rename(stage, output_dir)
            return
        except FileExistsError as exc:
            raise CompileError("another publisher owns the output publication lock") from exc
        except OSError as exc:
            raise CompileError(f"fallback publication failed: {exc}") from exc
        finally:
            if descriptor is not None:
                os.close(descriptor)
                lock.unlink(missing_ok=True)
    raise CompileError(f"atomic no-replace publication failed: {os.strerror(error)}")


def compile_source(
    source_path: Path,
    output_dir: Path,
    repo_root: Path,
    schema_dir: Path,
    discovery_roots: Iterable[str],
    public_roots: Iterable[str] = (),
    late_validator: Callable[[Path], None] | None = None,
) -> dict[str, Any]:
    root = repo_root.resolve(strict=True)
    discovery_roots = tuple(discovery_roots)
    public_roots = tuple(public_roots)
    if not discovery_roots:
        raise CompileError("at least one trusted discovery root is required")
    if not root.is_dir():
        raise CompileError("repository root is not a directory")
    source_path, source_relative = relative_file(root, source_path, "Define source")
    schema_dir = schema_dir.resolve(strict=True)
    try:
        schema_dir.relative_to(root)
    except ValueError as exc:
        raise CompileError("schema directory escapes repository") from exc
    output_dir = output_dir.absolute()
    if output_dir.exists():
        raise CompileError("output directory must be absent")
    try:
        output_parent = output_dir.parent.resolve(strict=True)
        output_parent.relative_to(root)
    except (OSError, ValueError) as exc:
        raise CompileError("output parent is missing or escapes repository") from exc

    source, source_data = load_json(source_path, "Define v3 source")
    schemas: dict[str, dict[str, Any]] = {}
    schema_refs: dict[str, dict[str, Any]] = {}
    for key, filename in SCHEMA_FILES.items():
        path = schema_dir / filename
        schema, data = load_json(path, f"{key} schema")
        if not isinstance(schema, dict) or not isinstance(schema.get("$id"), str):
            raise CompileError(f"{key} schema lacks a stable $id")
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            raise CompileError(f"{key} schema is invalid: {exc}") from exc
        if schema["$id"] != EXPECTED_SCHEMA_IDS[key]:
            raise CompileError(f"{key} schema declares an unexpected $id")
        schemas[key] = schema
        schema_refs[key] = exact_path_ref(root, path, f"{key} schema")
    store = {schema["$id"]: schema for schema in schemas.values()}
    store["https://arcanum.dev/schemas/invoke/definitions.schema.json"] = schemas["definitions_v1"]
    store["definitions.schema.json"] = schemas["definitions_v1"]
    require_schema_valid(source, schemas["source"], store, "Define source")
    profile_document = {
        "$schema": EXPECTED_SCHEMA_IDS["profile"],
        "schema_version": "invoke.define-profile.v3",
        "profile_id": PROFILE,
        "public_contract": True,
        "v2_compatibility_policy": "preserve-byte-and-validate-only",
        "outputs": [kind for _key, kind in OUTPUT_ORDER] + ["stage-receipt"],
    }
    require_schema_valid(profile_document, schemas["profile"], store, "Define profile")
    if source["profile_id"] != PROFILE:
        raise CompileError("unsupported Define v3 profile")
    if source["template_selection"]["selected"] not in source["template_selection"]["eligible"]:
        raise CompileError("selected profile is not eligible")

    context_path, context_data = verify_exact_ref(
        root,
        source["upstream_bindings"]["semantic_context_ref"],
        "semantic context",
    )
    closure_path, closure_data = verify_exact_ref(
        root,
        source["upstream_bindings"]["semantic_closure_receipt_ref"],
        "semantic closure receipt",
    )
    context = load_json_bytes(context_data, "semantic context")
    closure = load_json_bytes(closure_data, "semantic closure receipt")
    context_schema_path, _ = verify_exact_ref(
        root,
        closure["schema_bindings"]["context_schema_ref"],
        "closure-bound context schema",
    )
    receipt_schema_path, _ = verify_exact_ref(
        root,
        closure["schema_bindings"]["receipt_schema_ref"],
        "closure-bound receipt schema",
    )
    context_schema, _ = load_json(context_schema_path, "closure-bound context schema")
    receipt_schema, _ = load_json(receipt_schema_path, "closure-bound receipt schema")
    require_schema_valid(context, context_schema, {context_schema["$id"]: context_schema}, "semantic context")
    require_schema_valid(closure, receipt_schema, {receipt_schema["$id"]: receipt_schema}, "semantic closure receipt")
    if closure["context_ref"] != source["upstream_bindings"]["semantic_context_ref"]:
        raise CompileError("closure context reference differs from source binding")
    if closure["receipt_digest"] != sha256_bytes(
        canonical_bytes({key: value for key, value in closure.items() if key != "receipt_digest"})
    ):
        raise CompileError("semantic closure receipt digest is invalid")
    validator_path, validator_data = verify_exact_ref(
        root,
        {
            "path": closure["validator"]["path"],
            "sha256": closure["validator"]["sha256"],
            "size": len(repo_path(root, closure["validator"]["path"]).read_bytes()),
        },
        "closure validator",
    )
    if closure["validator"]["identity"] != "invoke.validate-define-semantic-closure.v1":
        raise CompileError("closure validator identity is not supported")
    if validator_data != (SCRIPT_DIR / "validate_define_semantic_closure.py").read_bytes():
        raise CompileError("closure validator bytes differ from the installed replay implementation")

    try:
        replayed = evaluate_context(
            context_path=context_path,
            repository_root=root,
            context_schema_path=context_schema_path,
            receipt_schema_path=receipt_schema_path,
            discovery_roots=list(discovery_roots),
            public_roots=list(public_roots),
        )
    except InvocationError as exc:
        raise CompileError(f"semantic closure replay failed: {exc}") from exc
    if canonical_bytes(replayed) != closure_data:
        raise CompileError("supplied semantic closure does not equal current in-memory replay")
    if replayed["outcome"] != "ready-for-define" or replayed["next_route"] != "define-v3":
        raise CompileError("semantic closure is not ready for Define v3")

    validate_projection(source, context, replayed)
    structural_schema_refs = validate_structural_schemas(
        root,
        source["definition_registry"]["definitions"],
    )
    if source["identity_denominator"]["classification"] == "required":
        _, _ = verify_exact_ref(root, source["identity_denominator"]["request_ref"], "identity request")
        result_path, result_data = verify_exact_ref(root, source["identity_denominator"]["result_ref"], "identity result")
        identity_result = load_json_bytes(result_data, str(result_path))
        if not isinstance(identity_result, dict) or identity_result.get("verdict") != "pass":
            raise CompileError("identity denominator result is not pass")

    context_ref = source["upstream_bindings"]["semantic_context_ref"]
    closure_ref = source["upstream_bindings"]["semantic_closure_receipt_ref"]
    artifact = build_definitions_artifact(source, context_ref, closure_ref, schemas["definitions_v2"])
    require_schema_valid(artifact, schemas["definitions_v2"], store, "definitions artifact")
    outputs = derived_output_bytes(source, context, context_data, closure_data, artifact)

    stage = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_parent))
    try:
        # The two semantic evidence documents are materialized first and retain
        # their upstream bytes exactly.
        first = source["output_contracts"]["semantic_context"]
        second = source["output_contracts"]["semantic_closure_receipt"]
        (stage / first).write_bytes(outputs[first])
        (stage / second).write_bytes(outputs[second])
        for key, _kind in OUTPUT_ORDER[2:]:
            name = source["output_contracts"][key]
            (stage / name).write_bytes(outputs[name])

        validate_staged_outputs(
            stage,
            outputs,
            artifact,
            source,
            context,
            replayed,
            schemas["definitions_v2"],
            store,
        )
        if late_validator is not None:
            late_validator(stage)
        if source_path.read_bytes() != source_data:
            raise CompileError("Define source changed during compilation")
        if closure_path.read_bytes() != closure_data:
            raise CompileError("semantic closure receipt changed during compilation")
        for key, filename in SCHEMA_FILES.items():
            if exact_path_ref(root, schema_dir / filename, f"{key} schema") != schema_refs[key]:
                raise CompileError(f"{key} schema changed during compilation")
        try:
            late_replay = evaluate_context(
                context_path=context_path,
                repository_root=root,
                context_schema_path=context_schema_path,
                receipt_schema_path=receipt_schema_path,
                discovery_roots=list(discovery_roots),
                public_roots=list(public_roots),
            )
        except InvocationError as exc:
            raise CompileError(f"late semantic closure replay failed: {exc}") from exc
        if canonical_bytes(late_replay) != closure_data:
            raise CompileError("semantic topology changed during compilation")
        if validate_structural_schemas(
            root,
            source["definition_registry"]["definitions"],
        ) != structural_schema_refs:
            raise CompileError("structural schema changed during compilation")
        validate_staged_outputs(
            stage,
            outputs,
            artifact,
            source,
            context,
            replayed,
            schemas["definitions_v2"],
            store,
        )

        contracts = source["output_contracts"]
        result_outputs = [
            {
                "kind": kind,
                **material_ref(contracts[key], (stage / contracts[key]).read_bytes()),
            }
            for key, kind in OUTPUT_ORDER
        ]
        receipt = {
            "$schema": schemas["result"]["$id"],
            "schema_version": "invoke.define-stage-receipt.v3",
            "receipt_id": f"define-v3:{source['source_id']}:{sha256_bytes(canonical_bytes(source))[:16]}",
            "owner_capability": "invoke",
            "mode": "define",
            "producer": {
                "identity": IDENTITY,
                "path": PRODUCER_PATH,
                "sha256": sha256_bytes(Path(__file__).read_bytes()),
            },
            "schema_bindings": {
                "source_schema_ref": schema_refs["source"],
                "profile_schema_ref": schema_refs["profile"],
                "definitions_v1_schema_ref": schema_refs["definitions_v1"],
                "definitions_v2_schema_ref": schema_refs["definitions_v2"],
                "result_schema_ref": schema_refs["result"],
            },
            "profile_id": PROFILE,
            "source_ref": material_ref(source_relative, source_data),
            "semantic_evidence": {
                "context_ref": copy.deepcopy(context_ref),
                "closure_receipt_ref": copy.deepcopy(closure_ref),
            },
            "structural_schema_refs": structural_schema_refs,
            "semantic_outcome": semantic_outcome(artifact),
            "outputs": result_outputs,
            "result": "pass",
            "next_route": source["next_route"],
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
        require_schema_valid(receipt, schemas["result"], store, "Define stage receipt")
        receipt_name = contracts["stage_receipt"]
        (stage / receipt_name).write_bytes(pretty_bytes(receipt))
        final_names = sorted(path.name for path in stage.iterdir() if path.is_file())
        if final_names != sorted([*outputs, receipt_name]) or len(final_names) != 13:
            raise CompileError("successful staging directory does not contain exactly thirteen files")
        publish_no_replace(stage, output_dir)
        return receipt
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--schema-dir", required=True, type=Path)
    parser.add_argument("--discovery-root", action="append", required=True)
    parser.add_argument("--public-root", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        receipt = compile_source(
            source_path=args.source,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
            schema_dir=args.schema_dir,
            discovery_roots=args.discovery_root,
            public_roots=args.public_root,
        )
    except (CompileError, InvocationError, OSError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
