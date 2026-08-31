#!/usr/bin/env python3
"""Independently admit one exact closure-bound Define v3 candidate bundle.

The validator is read-only except for exclusive creation of its receipt.  It
replays the installed Define v3 producer in a temporary directory, validates
the submitted bundle through every reachable consumer, and reports typed
semantic drift.  It never activates, promotes, or mutates the submitted
bundle.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, RefResolver


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from compile_define_source_v3 import (  # noqa: E402
    CompileError,
    IDENTITY as PRODUCER_IDENTITY,
    OUTPUT_ORDER,
    PRODUCER_PATH,
    compile_source,
    render_definitions,
    render_glossary,
    semantic_outcome,
)
from validate_define_semantic_closure import (  # noqa: E402
    DuplicateKeyError,
    InvocationError,
    canonical_bytes,
    evaluate_context,
    json_object,
    repo_path,
    sha256_bytes,
)


SCHEMA_URI = "https://arcanum.dev/schemas/invoke/define-bundle-admission-receipt/v1"
SCHEMA_VERSION = "invoke.define-bundle-admission-receipt.v1"
IDENTITY = "invoke.validate-define-bundle-admission.v1"
VALIDATOR_PATH = ".agents/skills/invoke/scripts/validate_define_bundle_admission.py"
PROFILE = "invoke.generic-definitions-baseline.v3"
STAGE_RECEIPT_NAME = "INVOKE-DEFINE-STAGE-RECEIPT.json"
SCHEMA_NAMES = {
    "admission": "define-bundle-admission-receipt-v1.schema.json",
    "result": "define-result-v3.schema.json",
    "definitions_v1": "definitions.schema.json",
    "definitions": "definitions-v2.schema.json",
    "context": "define-semantic-context-v1.schema.json",
    "closure": "define-semantic-closure-receipt-v1.schema.json",
    "source": "define-source-v3.schema.json",
    "profile": "define-profile-v3.schema.json",
}
CHECK_IDS = (
    "check:bundle-shape",
    "check:stage-receipt",
    "check:producer-identity",
    "check:schema-bindings",
    "check:ordered-inventory",
    "check:semantic-closure",
    "check:clean-replay",
    "check:definitions",
    "check:generated-views",
    "check:structural-schemas",
    "check:semantic-outcome",
    "check:authority-effect",
    "check:prior-admission",
)


class AdmissionInvocationError(Exception):
    """An invocation failure for which no receipt may be written."""


def strict_json_bytes(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=json_object)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise ValueError(f"{label} is not strict JSON: {exc}") from exc


def load_json(path: Path, label: str) -> tuple[Any, bytes]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc
    return strict_json_bytes(data, label), data


def digest_without(document: dict[str, Any], field: str) -> str:
    projected = copy.deepcopy(document)
    projected.pop(field, None)
    # Define stage/admission receipts use the compiler's newline-free digest
    # material.  Semantic-closure receipts retain their W1 newline-bearing
    # contract and are checked explicitly at that boundary below.
    return sha256_bytes(canonical_bytes(projected).rstrip(b"\n"))


def schema_errors(
    document: Any,
    schema: dict[str, Any],
    store: dict[str, Any],
) -> list[str]:
    try:
        resolver = RefResolver.from_schema(schema, store=store)
        errors = Draft202012Validator(schema, resolver=resolver).iter_errors(document)
        return [
            f"/{'/'.join(map(str, error.absolute_path))}: {error.message}"
            for error in sorted(errors, key=lambda item: tuple(str(part) for part in item.absolute_path))
        ]
    except Exception as exc:
        return [f"schema evaluation failed: {exc}"]


def confined(root: Path, path: Path, label: str, *, require_file: bool = False) -> Path:
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise AdmissionInvocationError(f"{label} is missing or escapes repository") from exc
    if require_file and (not resolved.is_file() or resolved.is_symlink()):
        raise AdmissionInvocationError(f"{label} is not a regular non-symlink file")
    return resolved


def relative(root: Path, path: Path) -> str:
    return path.resolve(strict=True).relative_to(root).as_posix()


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": relative(root, path), "sha256": sha256_bytes(data), "size": len(data)}


def nullable_exact_ref(root: Path, path: Path | None) -> dict[str, Any] | None:
    return exact_ref(root, path) if path is not None and path.is_file() and not path.is_symlink() else None


def inventory_digest(items: list[dict[str, Any]]) -> str:
    return sha256_bytes(canonical_bytes(items))


def verify_ref(root: Path, ref: Any) -> tuple[Path | None, bytes | None, str | None]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256", "size"}:
        return None, None, "reference shape is invalid"
    try:
        path = repo_path(root, ref["path"])
        data = path.read_bytes()
    except (OSError, ValueError, KeyError) as exc:
        return None, None, str(exc)
    if sha256_bytes(data) != ref["sha256"] or len(data) != ref["size"]:
        return path, data, "exact reference is stale"
    return path, data, None


def json_pointer(parts: Iterable[str | int]) -> str:
    encoded = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(encoded)


def definition_category(pointer: str) -> tuple[str, str, str]:
    """Return category, semantic effect, and repair route for a changed field."""

    parts = [part for part in pointer.split("/") if part]
    field = parts[2] if len(parts) > 2 and parts[0] == "definitions" else None
    if pointer.startswith("/semantic_evidence"):
        return "source_evidence", "review_required", "rerun_semantic_closure"
    if pointer == "/definitions" or field == "id" or pointer == "/registry_id":
        return "registry_topology", "topology_changed", "rerun_semantic_closure"
    if pointer.startswith("/authority_bindings") or pointer in {
        "/authority_kind",
        "/authority_effect",
        "/registry_status",
        "/visibility",
    } or any(
        token in pointer for token in ("/authority_scope", "/authority_status", "/owner_route")
    ):
        return "authority", "authority_changed", "definitions_governance"
    if pointer.startswith("/semantic_applications"):
        return "semantic_application", "meaning_changed", "reauthor_define_source"
    if field == "structural_schema":
        return "structural_schema", "review_required", "reauthor_define_source"
    if field == "primary_consumers":
        return "consumer_topology", "topology_changed", "rerun_semantic_closure"
    if field == "source_refs":
        if any(token in pointer for token in ("/selector", "/selector_type", "/from_line", "/to_line")):
            return "selector", "review_required", "rerun_semantic_closure"
        return "source_evidence", "review_required", "rerun_semantic_closure"
    if field in {"term", "aliases"}:
        return "label_alias", "meaning_changed", "reauthor_define_source"
    if field == "voices":
        return "definition_meaning", "meaning_changed", "reauthor_define_source"
    if field in {"boundary", "applicability", "invariants"}:
        return "boundary", "meaning_changed", "reauthor_define_source"
    if field == "relations":
        return "relation", "meaning_changed", "reauthor_define_source"
    if field in {"status", "status_detail", "deferred_as", "supersedes", "superseded_by", "definition_version"}:
        return "definition_meaning", "review_required", "reauthor_define_source"
    return "definition_meaning", "review_required", "reauthor_define_source"


def recursive_changes(before: Any, after: Any, parts: tuple[str | int, ...] = ()) -> list[tuple[str, str]]:
    """Return changed JSON pointers and change kinds without inferring equivalence."""

    if type(before) is not type(after):
        return [(json_pointer(parts), "modified")]
    if isinstance(before, dict):
        result: list[tuple[str, str]] = []
        for key in sorted(set(before) | set(after)):
            if key not in before:
                result.append((json_pointer((*parts, key)), "added"))
            elif key not in after:
                result.append((json_pointer((*parts, key)), "removed"))
            else:
                result.extend(recursive_changes(before[key], after[key], (*parts, key)))
        return result
    if isinstance(before, list):
        if before == after:
            return []
        if len(before) != len(after):
            # Membership changes are meaning-bearing at the collection edge.
            return [(json_pointer(parts), "modified")]
        result: list[tuple[str, str]] = []
        for index, (left, right) in enumerate(zip(before, after, strict=True)):
            result.extend(recursive_changes(left, right, (*parts, index)))
        return result
    return [] if before == after else [(json_pointer(parts), "modified")]


class AdmissionEvaluation:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.checks: dict[str, dict[str, str]] = {
            check_id: {"check_id": check_id, "status": "not_evaluable", "detail": "not evaluated"}
            for check_id in CHECK_IDS
        }
        self.blockers: list[dict[str, Any]] = []
        self.differences: list[dict[str, Any]] = []

    def check(self, check_id: str, status: str, detail: str) -> None:
        self.checks[check_id] = {"check_id": check_id, "status": status, "detail": detail}

    def block(self, code: str, message: str, *caused_by: str) -> None:
        item = {"code": code, "message": message, "caused_by": sorted(set(caused_by))}
        if item not in self.blockers:
            self.blockers.append(item)

    def difference(
        self,
        category: str,
        locator: str,
        change: str,
        semantic_effect: str,
        invalidates: list[str],
        repair_route: str,
        before_ref: dict[str, Any] | None = None,
        after_ref: dict[str, Any] | None = None,
    ) -> None:
        identity = f"drift:{len(self.differences) + 1:03d}:{category}"
        self.differences.append(
            {
                "drift_id": identity,
                "category": category,
                "locator": locator,
                "before_ref": before_ref,
                "after_ref": after_ref,
                "change": change,
                "semantic_effect": semantic_effect,
                "invalidates": invalidates,
                "repair_route": repair_route,
            }
        )

    def summary(self) -> dict[str, str]:
        effects = {item["semantic_effect"] for item in self.differences}
        categories = {item["category"] for item in self.differences}
        not_evaluable = {
            check_id for check_id, check in self.checks.items() if check["status"] == "not_evaluable"
        }
        evidence = "current"
        evidence_categories = {"source_evidence", "selector"}
        if any(
            item["change"] == "missing" and item["category"] in evidence_categories
            for item in self.differences
        ):
            evidence = "missing"
        elif categories & evidence_categories:
            evidence = "stale"
        elif "check:semantic-closure" in not_evaluable:
            evidence = "not_evaluable"
        semantic = "unchanged"
        if "meaning_changed" in effects:
            semantic = "changed"
        elif "review_required" in effects:
            semantic = "review_required"
        elif "not_evaluable" in effects or not_evaluable & {
            "check:semantic-closure",
            "check:definitions",
            "check:semantic-outcome",
        }:
            semantic = "not_evaluable"
        authority = "changed" if "authority_changed" in effects else "unchanged"
        if authority == "unchanged" and not_evaluable & {
            "check:semantic-closure",
            "check:definitions",
            "check:authority-effect",
        }:
            authority = "not_evaluable"
        topology = "changed" if "topology_changed" in effects else "unchanged"
        if topology == "unchanged" and "check:semantic-closure" in not_evaluable:
            topology = "not_evaluable"
        projection_categories = {"generated_projection", "bundle_inventory"}
        projection = "changed" if categories & projection_categories else "unchanged"
        if projection == "unchanged" and not_evaluable & {
            "check:bundle-shape",
            "check:ordered-inventory",
            "check:definitions",
            "check:generated-views",
            "check:clean-replay",
        }:
            projection = "not_evaluable"

        prior_basis_blocked = self.checks["check:prior-admission"]["status"] == "block"
        if semantic in {"changed", "review_required"} or authority in {"changed", "unresolved"} or topology == "changed":
            overall = "semantic_reassessment_required"
        elif prior_basis_blocked:
            overall = "blocked"
        elif evidence == "stale":
            overall = "closure_refresh_required"
        elif projection == "changed":
            overall = "recompile_required"
        elif evidence in {"missing", "not_evaluable"} or "not_evaluable" in {
            semantic,
            authority,
            topology,
            projection,
        }:
            overall = "blocked"
        else:
            overall = "current"
        return {
            "evidence_state": evidence,
            "semantic_state": semantic,
            "authority_state": authority,
            "topology_state": topology,
            "projection_state": projection,
            "overall": overall,
        }


def load_schemas(
    root: Path, schema_dir: Path
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    refs: dict[str, dict[str, Any]] = {}
    for key, name in SCHEMA_NAMES.items():
        path = schema_dir / name
        try:
            path = path.resolve(strict=True)
            path.relative_to(root)
            document, _data = load_json(path, f"{key} schema")
            if not isinstance(document, dict) or not isinstance(document.get("$id"), str):
                raise ValueError("schema lacks $id")
            Draft202012Validator.check_schema(document)
        except Exception as exc:
            raise AdmissionInvocationError(f"invalid required {key} schema: {exc}") from exc
        schemas[key] = document
        refs[key] = exact_ref(root, path)
    store = {schema["$id"]: schema for schema in schemas.values()}
    store["https://arcanum.dev/schemas/invoke/definitions.schema.json"] = schemas["definitions_v1"]
    store["definitions.schema.json"] = schemas["definitions_v1"]
    return schemas, refs, store


def classify_bundle_file_drift(
    evaluation: AdmissionEvaluation,
    kind: str,
    submitted_path: Path,
    clean_path: Path,
) -> None:
    before = exact_ref(evaluation.root, submitted_path)
    # The replay directory is destroyed before this receipt is returned.  Its
    # complete contents are bound by replay.clean_bundle_digest, while this
    # difference truthfully leaves the non-durable after_ref unavailable.
    after = None
    locator = before["path"]
    if kind == "definitions":
        try:
            left = strict_json_bytes(submitted_path.read_bytes(), "submitted definitions")
            right = strict_json_bytes(clean_path.read_bytes(), "clean definitions")
            changes = recursive_changes(left, right)
        except ValueError:
            changes = [("/", "modified")]
        for pointer, change in changes or [("/", "modified")]:
            category, effect, route = definition_category(pointer)
            evaluation.difference(
                category,
                f"{locator}#{pointer}",
                change,
                effect,
                ["bundle", "admission", "artifact_pass"],
                route,
                before,
                after,
            )
    elif kind == "identity-denominator":
        evaluation.difference(
            "identity_denominator",
            locator,
            "modified",
            "review_required",
            ["bundle", "admission", "artifact_pass"],
            "identity_denominator",
            before,
            after,
        )
    elif kind in {"semantic-context", "semantic-closure-receipt"}:
        evaluation.difference(
            "source_evidence",
            locator,
            "modified",
            "review_required",
            ["semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
            "rerun_semantic_closure",
            before,
            after,
        )
    elif kind == "stage-receipt":
        evaluation.difference(
            "bundle_inventory",
            locator,
            "modified",
            "none",
            ["admission", "artifact_pass"],
            "recompile",
            before,
            after,
        )
    else:
        evaluation.difference(
            "generated_projection",
            locator,
            "modified",
            "none",
            ["bundle", "admission", "artifact_pass"],
            "recompile",
            before,
            after,
        )


def evaluate_admission(
    repository_root: Path,
    bundle_root: Path,
    schema_dir: Path,
    prior_admission: Path | None = None,
) -> dict[str, Any]:
    root = repository_root.resolve(strict=True)
    if not root.is_dir():
        raise AdmissionInvocationError("repository root is not a directory")
    bundle = confined(root, bundle_root, "bundle root")
    if not bundle.is_dir() or bundle.is_symlink():
        raise AdmissionInvocationError("bundle root is not a regular directory")
    schema_dir = confined(root, schema_dir, "schema directory")
    if not schema_dir.is_dir() or schema_dir.is_symlink():
        raise AdmissionInvocationError("schema directory is not a regular directory")
    prior_path = confined(root, prior_admission, "prior admission", require_file=True) if prior_admission else None
    schemas, schema_refs, store = load_schemas(root, schema_dir)
    evaluation = AdmissionEvaluation(root)
    bundle_relative = relative(root, bundle)

    entries = sorted(bundle.iterdir(), key=lambda item: item.name)
    regular = [item for item in entries if item.is_file() and not item.is_symlink()]
    unexpected = [item for item in entries if not item.is_file() or item.is_symlink()]
    if len(entries) == 13 and len(regular) == 13 and not unexpected:
        evaluation.check("check:bundle-shape", "pass", "bundle contains exactly thirteen regular non-symlink files")
    else:
        evaluation.check("check:bundle-shape", "block", f"found {len(entries)} entries and {len(regular)} regular files")
        evaluation.block("DEFINE_ADMISSION_BUNDLE_SHAPE", "bundle must contain exactly thirteen regular non-symlink files", "check:bundle-shape")
        for item in entries:
            if item in unexpected:
                evaluation.difference(
                    "bundle_inventory", f"{bundle_relative}/{item.name}", "not_evaluable", "not_evaluable",
                    ["bundle", "admission", "artifact_pass"], "stop"
                )

    stage_path = bundle / STAGE_RECEIPT_NAME
    stage: dict[str, Any] | None = None
    stage_data: bytes | None = None
    if stage_path in regular:
        try:
            value, stage_data = load_json(stage_path, "Define stage receipt")
            if not isinstance(value, dict):
                raise ValueError("stage receipt is not an object")
            errors = schema_errors(value, schemas["result"], store)
            if errors:
                raise ValueError("; ".join(errors))
            if digest_without(value, "receipt_digest") != value["receipt_digest"]:
                raise ValueError("receipt_digest is invalid")
            stage = value
            evaluation.check("check:stage-receipt", "pass", "stage receipt is strict, schema-valid, and digest-valid")
        except ValueError as exc:
            evaluation.check("check:stage-receipt", "block", str(exc))
            evaluation.block("DEFINE_ADMISSION_STAGE_RECEIPT", str(exc), "check:stage-receipt")
    else:
        evaluation.check("check:stage-receipt", "block", "fixed stage receipt is missing")
        evaluation.block("DEFINE_ADMISSION_STAGE_RECEIPT_MISSING", "INVOKE-DEFINE-STAGE-RECEIPT.json is missing", "check:stage-receipt")

    producer_binding: dict[str, Any] | None = None
    if stage is not None:
        try:
            installed_producer = repo_path(root, stage["producer"]["path"])
            producer_data = installed_producer.read_bytes()
            producer_error = None
            if sha256_bytes(producer_data) != stage["producer"]["sha256"]:
                producer_error = "producer digest is stale"
        except (OSError, ValueError, KeyError) as exc:
            producer_data = None
            producer_error = str(exc)
        identity_ok = (
            producer_error is None
            and stage["producer"]["identity"] == PRODUCER_IDENTITY
            and stage["producer"]["path"] == PRODUCER_PATH
            and producer_data == (SCRIPT_DIR / "compile_define_source_v3.py").read_bytes()
            and stage["profile_id"] == PROFILE
        )
        if identity_ok:
            evaluation.check("check:producer-identity", "pass", "stage receipt binds the installed Define v3 producer and profile")
            producer_binding = {
                "receipt_id": stage["receipt_id"],
                "receipt_digest": stage["receipt_digest"],
                "profile_id": stage["profile_id"],
                "producer": copy.deepcopy(stage["producer"]),
            }
        else:
            evaluation.check("check:producer-identity", "block", producer_error or "producer identity or bytes do not match the installed v3 producer")
            evaluation.block("DEFINE_ADMISSION_PRODUCER_IDENTITY", "producer identity, profile, or installed bytes do not match", "check:producer-identity")
    else:
        evaluation.check("check:producer-identity", "not_evaluable", "stage receipt is unavailable")

    if stage is not None:
        expected_stage_schema_refs = {
            "source_schema_ref": schema_refs["source"],
            "profile_schema_ref": schema_refs["profile"],
            "definitions_v1_schema_ref": schema_refs["definitions_v1"],
            "definitions_v2_schema_ref": schema_refs["definitions"],
            "result_schema_ref": schema_refs["result"],
        }
        if stage["schema_bindings"] == expected_stage_schema_refs:
            evaluation.check("check:schema-bindings", "pass", "stage receipt binds every current structural contract exactly")
        else:
            evaluation.check("check:schema-bindings", "block", "stage schema bindings differ from the current exact schema set")
            evaluation.block("DEFINE_ADMISSION_SCHEMA_BINDING", "stage schema bindings are stale or mismatched", "check:schema-bindings")
            evaluation.difference(
                "structural_schema", "stage_receipt.schema_bindings", "modified", "review_required",
                ["define_source", "bundle", "admission", "artifact_pass"], "reauthor_define_source",
                nullable_exact_ref(root, stage_path), nullable_exact_ref(root, schema_dir / SCHEMA_NAMES["result"])
            )
    else:
        evaluation.check("check:schema-bindings", "not_evaluable", "stage receipt is unavailable")

    kinds_by_name: dict[str, str] = {}
    if stage is not None:
        kinds_by_name = {item["path"]: item["kind"] for item in stage["outputs"]}
    kinds_by_name[STAGE_RECEIPT_NAME] = "stage-receipt"
    inventory = [
        {"kind": kinds_by_name.get(path.name, "unexpected"), **exact_ref(root, path)}
        for path in regular
    ]
    ordered_inventory: list[dict[str, Any]] = []
    if stage is not None:
        expected_names = [item["path"] for item in stage["outputs"]] + [STAGE_RECEIPT_NAME]
        actual_names = [path.name for path in regular]
        inventory_by_name = {Path(item["path"]).name: item for item in inventory}
        ordered_inventory = [inventory_by_name[name] for name in expected_names if name in inventory_by_name]
        ordered_inventory.extend(item for item in inventory if Path(item["path"]).name not in expected_names)
        digest_match = True
        for expected in stage["outputs"]:
            actual = inventory_by_name.get(expected["path"])
            if actual is None or {key: actual[key] for key in ("kind", "sha256", "size")} != {
                key: expected[key] for key in ("kind", "sha256", "size")
            }:
                digest_match = False
        if len(expected_names) == 13 and set(actual_names) == set(expected_names) and digest_match:
            evaluation.check("check:ordered-inventory", "pass", "stage and bundle inventories agree on order, kind, digest, and size")
        else:
            evaluation.check("check:ordered-inventory", "block", "stage and bundle inventories differ")
            evaluation.block("DEFINE_ADMISSION_INVENTORY", "stage and bundle inventories do not agree exactly", "check:ordered-inventory")
            evaluation.difference(
                "bundle_inventory", bundle_relative, "modified", "none",
                ["bundle", "admission", "artifact_pass"], "recompile",
                nullable_exact_ref(root, stage_path), None
            )
    else:
        ordered_inventory = inventory
        evaluation.check("check:ordered-inventory", "not_evaluable", "stage receipt is unavailable")

    source_path: Path | None = None
    source: dict[str, Any] | None = None
    context: dict[str, Any] | None = None
    closure: dict[str, Any] | None = None
    discovery_roots: list[str] = []
    public_roots: list[str] = []
    source_ref: dict[str, Any] | None = None
    if stage is not None:
        source_path, source_data, source_error = verify_ref(root, stage["source_ref"])
        if source_error is not None:
            evaluation.check("check:semantic-closure", "block", f"source reference: {source_error}")
            evaluation.block("DEFINE_ADMISSION_SOURCE_STALE", source_error, "check:semantic-closure")
            evaluation.difference(
                "source_evidence", stage["source_ref"].get("path", "stage.source_ref"),
                "missing" if source_path is None else "modified", "review_required",
                ["semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                "rerun_semantic_closure", stage["source_ref"], nullable_exact_ref(root, source_path)
            )
        else:
            source_ref = copy.deepcopy(stage["source_ref"])
            try:
                value = strict_json_bytes(source_data or b"", "Define source")
                if not isinstance(value, dict):
                    raise ValueError("source is not an object")
                source = value
                context_path, context_data, context_error = verify_ref(root, stage["semantic_evidence"]["context_ref"])
                closure_path, closure_data, closure_error = verify_ref(root, stage["semantic_evidence"]["closure_receipt_ref"])
                if context_error or closure_error or context_path is None or closure_path is None:
                    if context_error and context_path is not None and (bundle / "DEFINE-SEMANTIC-CONTEXT.json").is_file():
                        try:
                            old_context = strict_json_bytes(
                                (bundle / "DEFINE-SEMANTIC-CONTEXT.json").read_bytes(), "bundled semantic context"
                            )
                            new_context = strict_json_bytes(context_data or b"", "current semantic context")
                            context_changes = recursive_changes(old_context, new_context)
                        except ValueError:
                            context_changes = [("/", "modified")]
                        for pointer, change in context_changes or [("/", "modified")]:
                            category = "selector" if "selector" in pointer else "source_evidence"
                            evaluation.difference(
                                category,
                                f"{stage['semantic_evidence']['context_ref']['path']}#{pointer}",
                                change,
                                "review_required",
                                ["semantic_context", "semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                                "rerun_semantic_closure",
                                stage["semantic_evidence"]["context_ref"],
                                nullable_exact_ref(root, context_path),
                            )
                    if closure_error:
                        evaluation.difference(
                            "source_evidence",
                            stage["semantic_evidence"]["closure_receipt_ref"].get("path", "semantic closure"),
                            "missing" if closure_path is None else "modified",
                            "review_required",
                            ["semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                            "rerun_semantic_closure",
                            stage["semantic_evidence"]["closure_receipt_ref"],
                            nullable_exact_ref(root, closure_path),
                        )
                    raise ValueError(f"semantic evidence is stale: {context_error or closure_error}")
                context = strict_json_bytes(context_data or b"", "semantic context")
                closure = strict_json_bytes(closure_data or b"", "semantic closure")
                if schema_errors(context, schemas["context"], store):
                    raise ValueError("semantic context is not schema-valid")
                if schema_errors(closure, schemas["closure"], store):
                    raise ValueError("semantic closure is not schema-valid")
                closure_material = {key: value for key, value in closure.items() if key != "receipt_digest"}
                if sha256_bytes(canonical_bytes(closure_material)) != closure["receipt_digest"]:
                    raise ValueError("semantic closure digest is invalid")
                discovery_roots = list(closure["visibility_boundary"]["discovery_roots"])
                public_roots = list(closure["visibility_boundary"]["public_roots"])
                bound_context_schema, _bound_context_data, bound_context_error = verify_ref(
                    root, closure["schema_bindings"]["context_schema_ref"]
                )
                bound_closure_schema, _bound_closure_data, bound_closure_error = verify_ref(
                    root, closure["schema_bindings"]["receipt_schema_ref"]
                )
                if bound_context_error or bound_closure_error or bound_context_schema is None or bound_closure_schema is None:
                    raise ValueError(f"closure-bound schema is stale: {bound_context_error or bound_closure_error}")
                replayed_closure = evaluate_context(
                    context_path=context_path,
                    repository_root=root,
                    context_schema_path=bound_context_schema,
                    receipt_schema_path=bound_closure_schema,
                    discovery_roots=discovery_roots,
                    public_roots=public_roots,
                )
                if canonical_bytes(replayed_closure) != (closure_data or b""):
                    old_authority = closure.get("authority_resolution")
                    new_authority = replayed_closure.get("authority_resolution")
                    if old_authority != new_authority:
                        evaluation.difference(
                            "authority", "semantic_closure.authority_resolution", "modified", "authority_changed",
                            ["semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                            "definitions_governance", stage["semantic_evidence"]["closure_receipt_ref"], None
                        )
                    old_registries = {
                        path
                        for snapshot in closure.get("discovery_snapshots", [])
                        for path in snapshot.get("registry_paths", [])
                    }
                    new_registries = {
                        path
                        for snapshot in replayed_closure.get("discovery_snapshots", [])
                        for path in snapshot.get("registry_paths", [])
                    }
                    if old_registries != new_registries:
                        evaluation.difference(
                            "registry_topology", "semantic_closure.discovery_snapshots", "modified", "topology_changed",
                            ["semantic_context", "semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                            "rerun_semantic_closure", stage["semantic_evidence"]["closure_receipt_ref"], None
                        )
                    old_consumers = {
                        path
                        for snapshot in closure.get("discovery_snapshots", [])
                        for path in snapshot.get("consumer_paths", [])
                    }
                    new_consumers = {
                        path
                        for snapshot in replayed_closure.get("discovery_snapshots", [])
                        for path in snapshot.get("consumer_paths", [])
                    }
                    if old_consumers != new_consumers:
                        evaluation.difference(
                            "consumer_topology", "semantic_closure.discovery_snapshots", "modified", "topology_changed",
                            ["semantic_context", "semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                            "rerun_semantic_closure", stage["semantic_evidence"]["closure_receipt_ref"], None
                        )
                    if not evaluation.differences:
                        evaluation.difference(
                            "source_evidence", "semantic_closure.replay", "modified", "review_required",
                            ["semantic_closure", "define_source", "bundle", "admission", "artifact_pass"],
                            "rerun_semantic_closure", stage["semantic_evidence"]["closure_receipt_ref"], None
                        )
                    raise ValueError("semantic closure differs from current clean replay")
                if closure["outcome"] != "ready-for-define" or closure["next_route"] != "define-v3":
                    raise ValueError("semantic closure is not ready for Define v3")
                evaluation.check("check:semantic-closure", "pass", "context and closure are exact, current, and ready for Define v3")
            except (ValueError, InvocationError, KeyError, TypeError) as exc:
                evaluation.check("check:semantic-closure", "block", str(exc))
                evaluation.block("DEFINE_ADMISSION_SEMANTIC_CLOSURE", str(exc), "check:semantic-closure")
    else:
        evaluation.check("check:semantic-closure", "not_evaluable", "stage receipt is unavailable")

    definitions_path = bundle / "DEFINITIONS.json"
    artifact: dict[str, Any] | None = None
    if definitions_path in regular:
        try:
            value, _ = load_json(definitions_path, "DEFINITIONS.json")
            if not isinstance(value, dict):
                raise ValueError("DEFINITIONS.json is not an object")
            errors = schema_errors(value, schemas["definitions"], store)
            if errors:
                raise ValueError("; ".join(errors))
            artifact = value
            evaluation.check("check:definitions", "pass", "DEFINITIONS.json is strict and schema-valid")
        except ValueError as exc:
            evaluation.check("check:definitions", "block", str(exc))
            evaluation.block("DEFINE_ADMISSION_DEFINITIONS", str(exc), "check:definitions")
    else:
        evaluation.check("check:definitions", "block", "DEFINITIONS.json is missing")
        evaluation.block("DEFINE_ADMISSION_DEFINITIONS_MISSING", "DEFINITIONS.json is missing", "check:definitions")

    if artifact is not None and (bundle / "DEFINITIONS.md") in regular and (bundle / "GLOSSARY.md") in regular:
        view_ok = (
            render_definitions(artifact) == (bundle / "DEFINITIONS.md").read_bytes()
            and render_glossary(artifact) == (bundle / "GLOSSARY.md").read_bytes()
        )
        if view_ok:
            evaluation.check("check:generated-views", "pass", "both views equal clean deterministic renders")
        else:
            evaluation.check("check:generated-views", "block", "one or more generated views differ from deterministic rendering")
            evaluation.block("DEFINE_ADMISSION_VIEW_DRIFT", "generated view drift detected", "check:generated-views")
            evaluation.difference(
                "generated_projection", bundle_relative, "modified", "none",
                ["bundle", "admission", "artifact_pass"], "recompile"
            )
    else:
        evaluation.check("check:generated-views", "not_evaluable", "definitions artifact or generated views are unavailable")

    structural_refs: list[dict[str, Any]] = []
    if artifact is not None:
        structural_failures: list[str] = []
        for definition in artifact.get("definitions", []):
            structural = definition.get("structural_schema")
            if structural is None or structural.get("status") != "machine-checkable":
                continue
            try:
                structural_path = repo_path(root, structural["ref"])
                schema, _ = load_json(structural_path, f"structural schema {definition['id']}")
                Draft202012Validator.check_schema(schema)
                structural_refs.append({"definition_id": definition["id"], **exact_ref(root, structural_path)})
            except Exception as exc:
                structural_failures.append(f"{definition.get('id')}: {exc}")
        if structural_failures:
            evaluation.check("check:structural-schemas", "block", "; ".join(structural_failures))
            evaluation.block("DEFINE_ADMISSION_STRUCTURAL_SCHEMA", "; ".join(structural_failures), "check:structural-schemas")
        elif stage is None:
            evaluation.check("check:structural-schemas", "not_evaluable", "stage receipt is unavailable")
        elif structural_refs != stage["structural_schema_refs"]:
            evaluation.check(
                "check:structural-schemas",
                "block",
                "live structural schemas differ from the compile-time stage binding",
            )
            evaluation.block(
                "DEFINE_ADMISSION_STRUCTURAL_SCHEMA_DRIFT",
                "live structural schemas differ from the compile-time stage binding",
                "check:structural-schemas",
            )
            evaluation.difference(
                "structural_schema",
                "stage_receipt.structural_schema_refs",
                "modified",
                "review_required",
                ["define_source", "bundle", "admission", "artifact_pass"],
                "reauthor_define_source",
                nullable_exact_ref(root, stage_path),
                (
                    {key: structural_refs[0][key] for key in ("path", "sha256", "size")}
                    if structural_refs
                    else None
                ),
            )
        else:
            evaluation.check(
                "check:structural-schemas",
                "pass",
                "all machine-checkable structural schemas are valid and equal their compile-time stage bindings",
            )
    else:
        evaluation.check("check:structural-schemas", "not_evaluable", "DEFINITIONS.json is unavailable")

    if artifact is not None and stage is not None:
        actual_outcome = semantic_outcome(artifact)
        if actual_outcome == stage["semantic_outcome"]:
            evaluation.check("check:semantic-outcome", "pass", f"semantic outcome is independently derived as {actual_outcome}")
        else:
            evaluation.check("check:semantic-outcome", "block", f"derived {actual_outcome}, stage declares {stage['semantic_outcome']}")
            evaluation.block("DEFINE_ADMISSION_SEMANTIC_OUTCOME", "semantic outcome does not match the Definitions payload", "check:semantic-outcome")
    else:
        evaluation.check("check:semantic-outcome", "not_evaluable", "stage receipt or DEFINITIONS.json is unavailable")

    authority_ok = stage is not None and artifact is not None and stage.get("authority_effect") == "none" and artifact.get("authority_effect") == "none"
    if authority_ok:
        evaluation.check("check:authority-effect", "pass", "stage and Definitions artifact both preserve authority_effect=none")
    elif stage is not None or artifact is not None:
        evaluation.check("check:authority-effect", "block", "authority_effect=none is not proven across both artifacts")
        evaluation.block("DEFINE_ADMISSION_AUTHORITY_EFFECT", "authority_effect=none is not proven", "check:authority-effect")
    else:
        evaluation.check("check:authority-effect", "not_evaluable", "stage receipt and Definitions artifact are unavailable")

    clean_digest: str | None = None
    compile_window = "not_evaluable"
    clean_dir: Path | None = None
    if source_path is not None and source is not None and discovery_roots:
        clean_dir = Path(tempfile.mkdtemp(prefix=".define-admission-parent.", dir=bundle.parent))
        shutil.rmtree(clean_dir)
        try:
            compile_source(
                source_path=source_path,
                output_dir=clean_dir,
                repo_root=root,
                schema_dir=schema_dir,
                discovery_roots=discovery_roots,
                public_roots=public_roots,
            )
            clean_entries = sorted(clean_dir.iterdir(), key=lambda item: item.name)
            clean_kinds = {
                item["path"]: item["kind"]
                for item in json.loads((clean_dir / STAGE_RECEIPT_NAME).read_text())["outputs"]
            } | {STAGE_RECEIPT_NAME: "stage-receipt"}
            clean_inventory = [
                {
                    "kind": clean_kinds[path.name],
                    "path": path.name,
                    "sha256": sha256_bytes(path.read_bytes()),
                    "size": path.stat().st_size,
                }
                for path in clean_entries
            ]
            clean_digest = inventory_digest(clean_inventory)
            submitted_by_name = {path.name: path for path in regular}
            clean_by_name = {path.name: path for path in clean_entries}
            for name in sorted(set(submitted_by_name) | set(clean_by_name)):
                left = submitted_by_name.get(name)
                right = clean_by_name.get(name)
                if left is None:
                    evaluation.difference(
                        "bundle_inventory", f"{bundle_relative}/{name}", "added", "none",
                        ["bundle", "admission", "artifact_pass"], "recompile", None, None
                    )
                elif right is None:
                    evaluation.difference(
                        "bundle_inventory", f"{bundle_relative}/{name}", "removed", "none",
                        ["bundle", "admission", "artifact_pass"], "recompile", exact_ref(root, left), None
                    )
                elif left.read_bytes() != right.read_bytes():
                    kind = kinds_by_name.get(name, "unexpected")
                    classify_bundle_file_drift(evaluation, kind, left, right)
            compile_window = "current" if not evaluation.differences else "changed"
            if compile_window == "current":
                evaluation.check("check:clean-replay", "pass", "submitted bundle is byte-identical to a clean installed-producer replay")
            else:
                evaluation.check("check:clean-replay", "block", "submitted bundle differs from clean replay")
                evaluation.block("DEFINE_ADMISSION_REPLAY_DRIFT", "submitted bundle differs from clean replay", "check:clean-replay")
        except (CompileError, InvocationError, OSError, ValueError) as exc:
            evaluation.check("check:clean-replay", "block", str(exc))
            evaluation.block("DEFINE_ADMISSION_REPLAY", f"clean replay failed: {exc}", "check:clean-replay")
        finally:
            if clean_dir is not None:
                shutil.rmtree(clean_dir, ignore_errors=True)
    else:
        evaluation.check("check:clean-replay", "not_evaluable", "source or closure-bound replay roots are unavailable")

    prior_state = "not_provided"
    if prior_path is None:
        evaluation.check("check:prior-admission", "pass", "no prior admission was supplied")
    else:
        try:
            prior, _ = load_json(prior_path, "prior admission")
            errors = schema_errors(prior, schemas["admission"], store)
            if errors or digest_without(prior, "receipt_digest") != prior.get("receipt_digest"):
                raise ValueError("prior admission is not schema-valid and digest-valid")
            old_inventory = prior["output_inventory"]
            current_projection = [
                {key: item[key] for key in ("kind", "sha256", "size")} for item in ordered_inventory
            ]
            old_projection = [
                {key: item[key] for key in ("kind", "sha256", "size")} for item in old_inventory
            ]
            old_structural = prior["structural_schema_refs"]
            if current_projection == old_projection and structural_refs == old_structural:
                prior_state = "current"
                evaluation.check("check:prior-admission", "pass", "current bundle and structural schema bindings equal the prior admission")
            else:
                prior_state = "changed"
                evaluation.check("check:prior-admission", "block", "current bundle or structural schemas differ from prior admission")
                evaluation.block("DEFINE_ADMISSION_PRIOR_DRIFT", "current material differs from prior admission", "check:prior-admission")
                if structural_refs != old_structural:
                    evaluation.difference(
                        "structural_schema", "prior_admission.structural_schema_refs", "modified", "review_required",
                        ["define_source", "bundle", "admission", "artifact_pass"], "reauthor_define_source",
                        exact_ref(root, prior_path), None
                    )
                elif old_projection != current_projection:
                    evaluation.difference(
                        "bundle_inventory", "prior_admission.output_inventory", "modified", "review_required",
                        ["bundle", "admission", "artifact_pass"], "stop", exact_ref(root, prior_path), None
                    )
        except ValueError as exc:
            prior_state = "not_evaluable"
            evaluation.check("check:prior-admission", "block", str(exc))
            evaluation.block("DEFINE_ADMISSION_PRIOR_INVALID", str(exc), "check:prior-admission")

    summary = evaluation.summary()
    result = "pass" if (
        all(check["status"] == "pass" for check in evaluation.checks.values())
        and not evaluation.blockers
        and summary["overall"] == "current"
        and compile_window == "current"
    ) else "block"
    stage_ref = nullable_exact_ref(root, stage_path)
    bundle_digest = inventory_digest(ordered_inventory)
    receipt: dict[str, Any] = {
        "$schema": SCHEMA_URI,
        "schema_version": SCHEMA_VERSION,
        "receipt_id": "admission:pending",
        "validator": {
            "identity": IDENTITY,
            "path": VALIDATOR_PATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "schema_bindings": {
            "admission_schema_ref": schema_refs["admission"],
            "result_schema_ref": schema_refs["result"],
            "definitions_schema_ref": schema_refs["definitions"],
            "context_schema_ref": schema_refs["context"],
            "closure_schema_ref": schema_refs["closure"],
        },
        "bundle_root": bundle_relative,
        "bundle_digest": bundle_digest,
        "stage_receipt_ref": stage_ref,
        "producer_binding": producer_binding,
        "output_inventory": ordered_inventory,
        "structural_schema_refs": structural_refs,
        "replay": {
            "source_ref": source_ref,
            "discovery_roots": discovery_roots,
            "public_roots": public_roots,
            "clean_bundle_digest": clean_digest,
            "comparison": "pass" if compile_window == "current" else ("block" if compile_window == "changed" else "not_evaluable"),
        },
        "drift_analysis": {
            "compile_window": compile_window,
            "prior_admission": prior_state,
            "summary": summary,
            "differences": evaluation.differences,
        },
        "checks": [evaluation.checks[check_id] for check_id in CHECK_IDS],
        "blockers": sorted(evaluation.blockers, key=lambda item: (item["code"], item["message"])),
        "result": result,
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    identity_material = {key: value for key, value in receipt.items() if key not in {"receipt_id", "receipt_digest"}}
    receipt["receipt_id"] = f"admission:{sha256_bytes(canonical_bytes(identity_material))[:32]}"
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    errors = schema_errors(receipt, schemas["admission"], store)
    if errors:
        raise AdmissionInvocationError(f"internally generated admission receipt is invalid: {'; '.join(errors)}")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--bundle-root", required=True, type=Path)
    parser.add_argument("--schema-dir", required=True, type=Path)
    parser.add_argument("--prior-admission", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.repo_root.resolve(strict=True)
        requested_output = args.output.absolute()
        if requested_output.exists() or requested_output.is_symlink():
            raise AdmissionInvocationError("receipt output must be absent")
        try:
            output_parent = requested_output.parent.resolve(strict=True)
            output_parent.relative_to(root)
        except (OSError, ValueError) as exc:
            raise AdmissionInvocationError("receipt output parent is missing or escapes repository") from exc
        output = output_parent / requested_output.name
        bundle = args.bundle_root.resolve(strict=True)
        try:
            output.relative_to(bundle)
        except ValueError:
            pass
        else:
            raise AdmissionInvocationError("receipt output must be outside the submitted bundle")
        receipt = evaluate_admission(
            repository_root=root,
            bundle_root=args.bundle_root,
            schema_dir=args.schema_dir,
            prior_admission=args.prior_admission,
        )
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(canonical_bytes(receipt))
            handle.flush()
            os.fsync(handle.fileno())
    except (AdmissionInvocationError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
