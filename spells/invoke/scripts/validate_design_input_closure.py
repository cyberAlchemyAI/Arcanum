#!/usr/bin/env python3
"""Validate approved-boundary-relative Design inputs and bind one manifest projection."""

from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import importlib.util
import json
import os
import tempfile
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from design_stage_contract import OUTPUTS as DESIGN_STAGE_OUTPUTS, STAGE_NAME as DESIGN_STAGE_NAME, validate_stage_receipt  # noqa: E402


VALIDATOR_ID = "invoke.validate-design-input-closure.v1"
VALIDATOR_OWNER = "invoke-design-input-closure-validator"
VALIDATOR_PATH = "arcanum/spells/invoke/scripts/validate_design_input_closure.py"
CHECK_IDS = (
    "closure-schema",
    "closure-digest",
    "process-binding",
    "boundary-approval",
    "path-safety",
    "boundary-freshness",
    "discovery-enumeration",
    "catalog-closure",
    "input-freshness",
    "visibility",
    "conditional-resolution",
    "conflict-closure",
    "prior-design",
    "scope-signal-coverage",
    "manifest-projection",
)
ZERO_DIGEST = "0" * 64


class ClosureFailure(ValueError):
    def __init__(self, code: str, message: str, selector: str | None = None):
        super().__init__(message)
        self.code = code
        self.selector = selector


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_without(document: dict[str, Any], field: str) -> str:
    return canonical_digest({key: value for key, value in document.items() if key != field})


def normalized_relative_path(raw: str) -> str:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or raw != normalized
        or path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
        or ".." in path.parts
        or str(path) in ("", ".")
        or str(path) != normalized
    ):
        raise ClosureFailure("BOUNDARY_REF_ESCAPE", f"unsafe path: {raw}", raw)
    return str(path)


def resolve_inside(repository_root: Path, raw: str, must_exist: bool = True) -> Path:
    relative = normalized_relative_path(raw)
    root = repository_root.resolve()
    candidate = root / relative
    cursor = candidate
    while cursor != root:
        if cursor.is_symlink():
            raise ClosureFailure("SYMLINK_UNSUPPORTED", f"symlink is unsupported: {raw}", raw)
        cursor = cursor.parent
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ClosureFailure(
            "BOUNDARY_REF_ESCAPE", f"path resolves outside repository root: {raw}", raw
        ) from error
    if must_exist and not candidate.exists():
        raise ClosureFailure("BOUNDARY_REF_MISSING", f"missing path: {raw}", raw)
    return candidate


def exact_ref(path: Path, base: Path, label: str | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": label or path.resolve().relative_to(base.resolve()).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def strong_tree_inventory(path: Path) -> tuple[list[dict[str, Any]], str, int]:
    if path.is_symlink():
        raise ClosureFailure("SYMLINK_UNSUPPORTED", f"symlink is unsupported: {path}")
    if not path.is_dir():
        raise ClosureFailure("BOUNDARY_REF_MISSING", f"discovery root is not a directory: {path}")
    records: list[dict[str, Any]] = []
    for child in sorted(path.rglob("*")):
        if child.is_symlink():
            raise ClosureFailure("SYMLINK_UNSUPPORTED", f"symlink is unsupported: {child}")
        if child.is_file():
            data = child.read_bytes()
            records.append(
                {
                    "relative_path": child.relative_to(path).as_posix(),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                }
            )
    return records, canonical_digest(records), sum(item["size"] for item in records)


def schema_messages(
    document: dict[str, Any],
    schema: dict[str, Any],
    store: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store or {})
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, resolver=resolver).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def load_projection_module(script_dir: Path) -> Any:
    path = script_dir / "project_design_scope_manifest.py"
    spec = importlib.util.spec_from_file_location("invoke_design_scope_projector", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load projector: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def boundary_material(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "observation_epoch": document["observation_epoch"],
        "roots": document["roots"],
        "discovery_rules": document["discovery_rules"],
        "required_input_classes": document["required_input_classes"],
        "permitted_exclusions": document["permitted_exclusions"],
    }


def repair_for(code: str) -> str:
    if code.startswith("BOUNDARY_") or code.startswith("DISCOVERY_"):
        return "Repair the approved discovery boundary and regenerate exact refs."
    if code.startswith("INPUT_") or code.startswith("CONDITIONAL_"):
        return "Repair the exact input catalog and rerun closure validation."
    if code.startswith("PRIOR_") or code == "GREENFIELD_CONTRADICTED":
        return "Repair the prior-Design determination without implicit predecessor selection."
    if code.startswith("MANIFEST_") or code.startswith("SCOPE_"):
        return "Repair the typed scope signals and restart from input closure."
    return "Repair the named contract and rerun the W1 producer."


def validate_input_closure(
    closure: dict[str, Any],
    closure_path: Path,
    repository_root: Path,
    schema_dir: Path,
) -> dict[str, Any]:
    installed_root = Path(__file__).resolve().parents[4]
    script_dir = Path(__file__).resolve().parent
    schemas = {
        path.name: load_json(path)
        for path in [
            schema_dir / "design-input-boundary-approval-v1.schema.json",
            schema_dir / "design-input-closure-v1.schema.json",
            schema_dir / "design-input-closure-receipt-v1.schema.json",
            schema_dir / "design-production-process-v1.schema.json",
            schema_dir / "design-scope-manifest.schema.json",
            schema_dir / "define-result-v2.schema.json",
            schema_dir / "define-source-v2.schema.json",
            schema_dir / "definitions.schema.json",
            schema_dir / "design-source-v1.schema.json",
            schema_dir / "design-profile-v1.schema.json",
            schema_dir / "design-artifact-v1.schema.json",
            schema_dir / "design-result-v2.schema.json",
        ]
    }
    schemas_by_id = {
        schema["$id"]: schema
        for schema in schemas.values()
        if isinstance(schema.get("$id"), str)
    }
    process_path = (
        installed_root
        / "arcanum/spells/invoke/development/whole-invoke-repair-plan/design-process/DESIGN-PRODUCTION-PROCESS.json"
    )
    process_ref = exact_ref(process_path, installed_root)
    closure_ref = exact_ref(closure_path, repository_root)
    script_ref = exact_ref(Path(__file__).resolve(), installed_root, VALIDATOR_PATH)

    direct: dict[str, list[str]] = {check_id: [] for check_id in CHECK_IDS}
    blockers: list[dict[str, Any]] = []

    def add(check_id: str, code: str, message: str, selector: str | None = None) -> str:
        blocker_id = f"blocker:{len(blockers) + 1:03d}:{code.lower()}"
        blockers.append(
            {
                "blocker_id": blocker_id,
                "code": code,
                "message": message,
                "selector": selector,
                "owner": "design-input-owner",
                "repair_route": repair_for(code),
            }
        )
        direct[check_id].append(blocker_id)
        return blocker_id

    activation_kind = closure.get("activation", {}).get("kind", "invalid")
    closure_id = closure.get("closure_id", "invalid:design-input-closure")
    declared_closure_digest = closure.get("closure_digest", ZERO_DIGEST)
    boundary = closure.get("discovery_boundary", {})
    declared_boundary_digest = boundary.get("boundary_digest", ZERO_DIGEST)
    approval_ref: dict[str, Any] | None = None
    approval: dict[str, Any] | None = None
    root_receipt_refs: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    cataloged_paths: list[str] = []
    excluded_paths: list[str] = []
    unclassified_paths: list[str] = []
    ambiguous_paths: list[str] = []
    per_class: list[dict[str, Any]] = []
    conditional_results: list[dict[str, Any]] = []
    expected_manifest: dict[str, str] | None = None
    prior_result: dict[str, Any] = {
        "kind": closure.get("design_kind", {}).get("kind", "invalid"),
        "status": "not_evaluable",
        "candidate_paths": [],
        "evidence_refs": [],
    }

    closure_errors = schema_messages(
        closure, schemas["design-input-closure-v1.schema.json"]
    )
    if closure_errors:
        add(
            "closure-schema",
            "CLOSURE_SCHEMA_INVALID",
            "; ".join(closure_errors),
            "$",
        )
    if not closure_errors and digest_without(closure, "closure_digest") != declared_closure_digest:
        add(
            "closure-digest",
            "CLOSURE_DIGEST_MISMATCH",
            "closure_digest does not equal the canonical closure projection",
            "closure_digest",
        )

    try:
        process = load_json(process_path)
        process_errors = schema_messages(
            process, schemas["design-production-process-v1.schema.json"]
        )
        if process_errors or digest_without(process, "process_digest") != process.get(
            "process_digest"
        ):
            add(
                "process-binding",
                "PROCESS_REF_STALE",
                "; ".join(process_errors) or "process self-digest is stale",
                process_ref["path"],
            )
    except (OSError, json.JSONDecodeError) as error:
        add("process-binding", "PROCESS_REF_STALE", str(error), process_ref["path"])

    if not closure_errors:
        try:
            manifest_contract_ref = closure["scope_manifest_contract_ref"]
            manifest_contract_path = resolve_inside(
                installed_root, manifest_contract_ref["path"]
            )
            data = manifest_contract_path.read_bytes()
            manifest_contract = load_json(manifest_contract_path)
            if (
                hashlib.sha256(data).hexdigest() != manifest_contract_ref["sha256"]
                or len(data) != manifest_contract_ref["size"]
            ):
                raise ClosureFailure(
                    "PROCESS_REF_STALE",
                    "scope manifest contract exact ref is stale",
                    manifest_contract_ref["path"],
                )
            installed_version = (
                manifest_contract.get("properties", {})
                .get("schema_version", {})
                .get("const")
            )
            if manifest_contract.get("$id") != manifest_contract_ref["expected_schema_id"]:
                raise ClosureFailure(
                    "INPUT_SCHEMA_ID_MISMATCH",
                    "scope manifest contract $id differs from the declared identity",
                    manifest_contract_ref["path"],
                )
            if installed_version != manifest_contract_ref["expected_schema_version"]:
                raise ClosureFailure(
                    "INPUT_SCHEMA_VERSION_MISMATCH",
                    "scope manifest contract version differs from the declared identity",
                    manifest_contract_ref["path"],
                )
        except (OSError, json.JSONDecodeError, ClosureFailure) as error:
            code = error.code if isinstance(error, ClosureFailure) else "PROCESS_REF_STALE"
            selector = (
                error.selector
                if isinstance(error, ClosureFailure)
                else closure.get("scope_manifest_contract_ref", {}).get("path")
            )
            add("process-binding", code, str(error), selector)

    if closure_errors:
        causal = [item["blocker_id"] for item in blockers]
        checks = []
        for check_id in CHECK_IDS:
            if direct[check_id]:
                status = "block"
                ids = direct[check_id]
            elif check_id == "closure-schema":
                status = "pass"
                ids = []
            else:
                status = "not_evaluable"
                ids = causal
            checks.append(
                {"check_id": check_id, "status": status, "evidence_refs": [], "causal_blocker_ids": ids}
            )
        receipt = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1",
            "schema_version": "invoke.design-input-closure-receipt.v1",
            "receipt_id": f"closure-receipt:{canonical_digest(closure)[:20]}",
            "validator": {"identity": VALIDATOR_ID, "owner": VALIDATOR_OWNER, "path": VALIDATOR_PATH, "sha256": script_ref["sha256"]},
            "bindings": {"process_ref": process_ref, "design_input_closure_ref": closure_ref, "boundary_approval_ref": None, "closure_digest": declared_closure_digest if isinstance(declared_closure_digest, str) and len(declared_closure_digest) == 64 else ZERO_DIGEST, "discovery_boundary_digest": declared_boundary_digest if isinstance(declared_boundary_digest, str) and len(declared_boundary_digest) == 64 else ZERO_DIGEST},
            "activation_kind": "invalid",
            "inspected_boundary": {"root_refs": [], "rule_ids": [], "required_input_classes": []},
            "discovery": {"inventory": [], "inventory_digest": canonical_digest([]), "cataloged_paths": [], "excluded_paths": [], "unclassified_paths": [], "ambiguous_paths": [], "per_class": []},
            "conditional_resolutions": [],
            "prior_design_determination": prior_result,
            "expected_manifest": None,
            "checks": checks,
            "verdict": "block",
            "blockers": blockers,
            "authority_effect": "none",
            "receipt_digest": ZERO_DIGEST,
        }
        receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
        return receipt

    def validate_file_ref(
        ref: dict[str, Any],
        check_id: str,
        stale_code: str = "INPUT_REF_STALE",
        base: Path | None = None,
    ) -> Path | None:
        target_base = base or repository_root
        try:
            if (
                closure["target"]["visibility"] == "public"
                and ref.get("visibility") == "private"
            ):
                raise ClosureFailure(
                    "INPUT_VISIBILITY_LEAK",
                    f"public target binds private reference: {ref['path']}",
                    ref["path"],
                )
            path = resolve_inside(target_base, ref["path"])
            if not path.is_file() or path.is_symlink():
                raise ClosureFailure(stale_code, f"regular file required: {ref['path']}", ref["path"])
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != ref["sha256"] or len(data) != ref["size"]:
                raise ClosureFailure(stale_code, f"stale exact ref: {ref['path']}", ref["path"])
            expected_id = ref.get("expected_schema_id")
            expected_version = ref.get("expected_schema_version")
            if expected_id is not None:
                schema = schemas_by_id.get(expected_id)
                if schema is None:
                    raise ClosureFailure(
                        "INPUT_SCHEMA_ID_MISMATCH",
                        f"installed schema id is unavailable: {expected_id}",
                        ref["path"],
                    )
                document = load_json(path)
                errors = schema_messages(document, schema, schemas_by_id)
                if errors:
                    raise ClosureFailure(
                        "INPUT_SCHEMA_ID_MISMATCH",
                        "; ".join(errors),
                        ref["path"],
                    )
                if expected_version is not None and document.get("schema_version") != expected_version:
                    raise ClosureFailure(
                        "INPUT_SCHEMA_VERSION_MISMATCH",
                        f"expected schema_version {expected_version}",
                        ref["path"],
                    )
            return path
        except (OSError, json.JSONDecodeError, ClosureFailure) as error:
            code = error.code if isinstance(error, ClosureFailure) else stale_code
            selector = error.selector if isinstance(error, ClosureFailure) else ref.get("path")
            actual_check = "visibility" if code == "INPUT_VISIBILITY_LEAK" else check_id
            add(actual_check, code, str(error), selector)
            return None

    approval_path = validate_file_ref(
        closure["activation"]["approval_ref"], "boundary-approval"
    )
    if approval_path is not None:
        approval_ref = exact_ref(approval_path, repository_root)
        try:
            approval = load_json(approval_path)
            errors = schema_messages(
                approval, schemas["design-input-boundary-approval-v1.schema.json"]
            )
            if errors or digest_without(approval, "approval_digest") != approval.get(
                "approval_digest"
            ):
                raise ClosureFailure(
                    "BOUNDARY_APPROVAL_INVALID",
                    "; ".join(errors) or "approval self-digest is stale",
                    approval_ref["path"],
                )
            if approval.get("boundary_digest") != canonical_digest(
                boundary_material(approval)
            ):
                raise ClosureFailure(
                    "BOUNDARY_APPROVAL_INVALID",
                    "approval boundary_digest is stale",
                    approval_ref["path"],
                )
            approved_projection = boundary_material(approval)
            if (
                approval.get("target_id") != closure["target"]["id"]
                or approval.get("target_visibility") != closure["target"]["visibility"]
                or approval.get("approved_by") != closure["target"]["owner"]
                or approved_projection != boundary_material(boundary)
                or approval.get("boundary_digest") != boundary["boundary_digest"]
            ):
                raise ClosureFailure(
                    "BOUNDARY_APPROVAL_MISMATCH",
                    "closure boundary is not exactly the approved boundary",
                    approval_ref["path"],
                )
        except (OSError, json.JSONDecodeError, ClosureFailure) as error:
            code = error.code if isinstance(error, ClosureFailure) else "BOUNDARY_APPROVAL_INVALID"
            selector = error.selector if isinstance(error, ClosureFailure) else approval_ref["path"]
            add("boundary-approval", code, str(error), selector)

    if boundary["boundary_digest"] != canonical_digest(boundary_material(boundary)):
        add(
            "boundary-freshness",
            "BOUNDARY_REF_STALE",
            "closure boundary_digest is stale",
            "discovery_boundary.boundary_digest",
        )

    roots: dict[str, tuple[dict[str, Any], Path, list[dict[str, Any]]]] = {}
    root_paths: set[str] = set()
    for root in boundary["roots"]:
        if root["root_id"] in roots:
            add("path-safety", "INPUT_DUPLICATE", f"duplicate root id: {root['root_id']}", root["root_id"])
            continue
        try:
            normalized_root = normalized_relative_path(root["path"])
            if normalized_root in root_paths:
                raise ClosureFailure(
                    "INPUT_DUPLICATE",
                    f"duplicate normalized root path: {normalized_root}",
                    normalized_root,
                )
            root_paths.add(normalized_root)
            path = resolve_inside(repository_root, root["path"])
            records, digest, size = strong_tree_inventory(path)
            if digest != root["sha256"] or size != root["size"]:
                raise ClosureFailure(
                    "BOUNDARY_REF_STALE", f"stale directory root: {root['path']}", root["path"]
                )
            roots[root["root_id"]] = (root, path, records)
            root_receipt_refs.append(
                {"path": root["path"], "sha256": root["sha256"], "size": root["size"]}
            )
        except ClosureFailure as error:
            check = "path-safety" if error.code in {"BOUNDARY_REF_ESCAPE", "SYMLINK_UNSUPPORTED", "INPUT_DUPLICATE"} else "boundary-freshness"
            add(check, error.code, str(error), error.selector)

    matches: dict[str, list[tuple[str, str]]] = {}
    rule_ids: set[str] = set()
    for rule in boundary["discovery_rules"]:
        if rule["rule_id"] in rule_ids:
            add("discovery-enumeration", "INPUT_DUPLICATE", f"duplicate rule id: {rule['rule_id']}", rule["rule_id"])
            continue
        rule_ids.add(rule["rule_id"])
        for pattern in rule["include_globs"]:
            if (
                "\\" in pattern
                or pattern.startswith(("/", "./"))
                or "//" in pattern
                or "/./" in pattern
                or ".." in PurePosixPath(pattern).parts
            ):
                add(
                    "path-safety",
                    "BOUNDARY_REF_ESCAPE",
                    f"unsafe or non-normal discovery glob: {pattern}",
                    pattern,
                )
        root_value = roots.get(rule["root_id"])
        if root_value is None:
            add("discovery-enumeration", "BOUNDARY_REF_MISSING", f"unknown root id: {rule['root_id']}", rule["rule_id"])
            continue
        root, _, records = root_value
        matched = 0
        for record in records:
            if any(fnmatch.fnmatchcase(record["relative_path"], pattern) for pattern in rule["include_globs"]):
                matched += 1
                path = f"{root['path'].rstrip('/')}/{record['relative_path']}"
                matches.setdefault(path, []).append((rule["rule_id"], rule["input_class"]))
        if matched == 0:
            add("discovery-enumeration", "DISCOVERY_RULE_EMPTY", f"discovery rule matched no files: {rule['rule_id']}", rule["rule_id"])

    for path in sorted(matches):
        path_matches = sorted(matches[path])
        if len(path_matches) != 1:
            ambiguous_paths.append(path)
            add("discovery-enumeration", "DISCOVERY_INPUT_AMBIGUOUS", f"candidate matched multiple rules: {path}", path)
        rule_id, input_class = path_matches[0]
        file_path = resolve_inside(repository_root, path)
        data = file_path.read_bytes()
        inventory.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "input_class": input_class, "rule_id": rule_id})

    approved_exclusions = {
        normalized_relative_path(item["path"]): item
        for item in boundary["permitted_exclusions"]
    }
    declared_exclusions = {
        normalized_relative_path(item["path"]): item for item in closure["exclusions"]
    }
    if len(approved_exclusions) != len(boundary["permitted_exclusions"]):
        add(
            "catalog-closure",
            "INPUT_DUPLICATE",
            "duplicate normalized path in permitted exclusions",
            "discovery_boundary.permitted_exclusions",
        )
    if len(declared_exclusions) != len(closure["exclusions"]):
        add(
            "catalog-closure",
            "INPUT_DUPLICATE",
            "duplicate normalized path in closure exclusions",
            "exclusions",
        )
    if set(approved_exclusions) != set(declared_exclusions):
        add(
            "catalog-closure",
            "EXCLUSION_UNJUSTIFIED",
            "closure exclusions must equal the approved exact exclusion set",
            "exclusions",
        )
    for path, approved in sorted(approved_exclusions.items()):
        declared = declared_exclusions.get(path)
        validate_file_ref(
            {
                **approved["evidence_ref"],
                "visibility": closure["target"]["visibility"],
                "expected_schema_id": None,
                "expected_schema_version": None,
            },
            "input-freshness",
        )
        if declared is not None:
            validate_file_ref(declared["evidence_ref"], "input-freshness")
            exact = {
                key: declared["evidence_ref"][key] for key in ("path", "sha256", "size")
            }
            if exact != approved["evidence_ref"]:
                add(
                    "catalog-closure",
                    "EXCLUSION_UNJUSTIFIED",
                    f"closure exclusion evidence differs from approval: {path}",
                    path,
                )
    catalog_by_path: dict[str, dict[str, Any]] = {}
    input_ids: set[str] = set()
    for item in closure["input_catalog"]:
        path = normalized_relative_path(item["source_ref"]["path"])
        if item["input_id"] in input_ids or path in catalog_by_path:
            add("catalog-closure", "INPUT_DUPLICATE", f"duplicate input id or path: {item['input_id']} / {path}", path)
        input_ids.add(item["input_id"])
        catalog_by_path[path] = item
        if item["selector"] != f"file:{path}":
            add("catalog-closure", "INPUT_REF_STALE", f"whole-file selector does not match path: {path}", item["selector"])

    inventory_by_path = {item["path"]: item for item in inventory}
    for path, candidate in sorted(inventory_by_path.items()):
        catalog_item = catalog_by_path.get(path)
        if catalog_item is None:
            if path in approved_exclusions:
                excluded_paths.append(path)
            else:
                unclassified_paths.append(path)
                add("catalog-closure", "DISCOVERY_INPUT_UNDECLARED", f"discovered candidate is neither cataloged nor exactly excluded: {path}", path)
            continue
        if catalog_item["kind"] != candidate["input_class"]:
            add("catalog-closure", "DISCOVERY_INPUT_AMBIGUOUS", f"catalog class differs from discovery rule: {path}", path)
    for path in sorted(set(catalog_by_path) - set(inventory_by_path)):
        add("catalog-closure", "CATALOG_INPUT_OUTSIDE_BOUNDARY", f"catalog input is outside the approved discovery set: {path}", path)
    for path in sorted(set(approved_exclusions) - set(inventory_by_path)):
        add(
            "catalog-closure",
            "EXCLUSION_UNJUSTIFIED",
            f"approved exclusion is outside the discovered candidate set: {path}",
            path,
        )

    conditional_by_id = {
        item["input_id"]: item for item in closure["conditional_input_resolutions"]
    }
    if len(conditional_by_id) != len(closure["conditional_input_resolutions"]):
        add("conditional-resolution", "INPUT_DUPLICATE", "duplicate conditional input resolution", "conditional_input_resolutions")
    selected_ids: set[str] = set()
    for item in closure["input_catalog"]:
        ref_path = validate_file_ref(item["source_ref"], "input-freshness")
        if item["classification"] in {"required", "conditional"} and (
            item["freshness"]["status"] != "current"
            or item["freshness"]["observed_epoch"] != boundary["observation_epoch"]
        ):
            add("input-freshness", "INPUT_REF_STALE", f"applicable input is not current at the approved epoch: {item['input_id']}", item["source_ref"]["path"])
        if item["classification"] == "required":
            selected_ids.add(item["input_id"])
        elif item["classification"] == "conditional":
            resolution = conditional_by_id.get(item["input_id"])
            if resolution is None:
                add("conditional-resolution", "CONDITIONAL_INPUT_UNRESOLVED", f"conditional input lacks resolution: {item['input_id']}", item["input_id"])
            else:
                evidence_path = validate_file_ref(resolution["evidence_ref"], "conditional-resolution")
                if resolution["owner"] != item["applicability_owner"]:
                    add("conditional-resolution", "INPUT_AUTHORITY_UNRESOLVED", f"conditional resolution owner differs: {item['input_id']}", item["input_id"])
                if evidence_path is not None:
                    conditional_results.append({"input_id": item["input_id"], "outcome": resolution["outcome"], "evidence_ref": exact_ref(evidence_path, repository_root), "owner": resolution["owner"]})
                if resolution["outcome"] == "included":
                    selected_ids.add(item["input_id"])
                else:
                    excluded_paths.append(item["source_ref"]["path"])
        else:
            excluded_paths.append(item["source_ref"]["path"])
            evidence = item.get("exclusion_evidence_ref")
            permitted = {entry["path"]: entry for entry in boundary["permitted_exclusions"]}
            declared = {entry["path"]: entry for entry in closure["exclusions"]}
            if item["source_ref"]["path"] not in permitted or item["source_ref"]["path"] not in declared or evidence is None:
                add("catalog-closure", "EXCLUSION_UNJUSTIFIED", f"excluded input lacks approved exact exclusion: {item['input_id']}", item["source_ref"]["path"])
            else:
                validate_file_ref(evidence, "input-freshness")
        if ref_path is None:
            continue

    extra_resolutions = set(conditional_by_id) - {
        item["input_id"] for item in closure["input_catalog"] if item["classification"] == "conditional"
    }
    for input_id in sorted(extra_resolutions):
        add("conditional-resolution", "CONDITIONAL_INPUT_UNRESOLVED", f"resolution names a non-conditional input: {input_id}", input_id)

    for item in closure["input_catalog"]:
        path = normalized_relative_path(item["source_ref"]["path"])
        if item["input_id"] in selected_ids:
            if path in approved_exclusions:
                add(
                    "catalog-closure",
                    "EXCLUSION_UNJUSTIFIED",
                    f"included input is also exactly excluded: {path}",
                    path,
                )
            cataloged_paths.append(path)
        else:
            excluded_paths.append(path)
            approved = approved_exclusions.get(path)
            declared = declared_exclusions.get(path)
            if approved is None or declared is None:
                add(
                    "catalog-closure",
                    "EXCLUSION_UNJUSTIFIED",
                    f"non-included input lacks an approved exact exclusion: {path}",
                    path,
                )
            evidence = item.get("exclusion_evidence_ref")
            if item["classification"] == "excluded" and evidence is not None and approved is not None:
                exact = {key: evidence[key] for key in ("path", "sha256", "size")}
                if exact != approved["evidence_ref"]:
                    add(
                        "catalog-closure",
                        "EXCLUSION_UNJUSTIFIED",
                        f"catalog exclusion evidence differs from approval: {path}",
                        path,
                    )

    effective_catalog = set(cataloged_paths)
    effective_exclusions = set(excluded_paths)
    inventory_paths = set(inventory_by_path)
    if effective_catalog & effective_exclusions:
        add(
            "catalog-closure",
            "INPUT_DUPLICATE",
            "a discovered candidate cannot be both included and excluded",
            sorted(effective_catalog & effective_exclusions)[0],
        )
    if inventory_paths != effective_catalog | effective_exclusions:
        add(
            "catalog-closure",
            "DISCOVERY_INPUT_UNDECLARED",
            "discovered candidates do not equal the included and approved-exclusion sets",
            "discovery.inventory",
        )

    counts: dict[str, dict[str, int]] = {}
    catalog_by_id = {item["input_id"]: item for item in closure["input_catalog"]}
    for required_class in boundary["required_input_classes"]:
        counts.setdefault(
            required_class, {"candidate": 0, "included": 0, "excluded": 0}
        )
    for candidate in inventory:
        counts.setdefault(candidate["input_class"], {"candidate": 0, "included": 0, "excluded": 0})["candidate"] += 1
    for item in closure["input_catalog"]:
        if item["input_id"] in selected_ids:
            counts.setdefault(
                item["kind"], {"candidate": 0, "included": 0, "excluded": 0}
            )["included"] += 1
    for path in effective_exclusions:
        candidate = inventory_by_path.get(path)
        if candidate is not None:
            counts.setdefault(
                candidate["input_class"],
                {"candidate": 0, "included": 0, "excluded": 0},
            )["excluded"] += 1
    for input_class in sorted(counts):
        values = counts[input_class]
        required = input_class in boundary["required_input_classes"]
        status = "pass" if not required or values["included"] > 0 else "block"
        if status == "block":
            add("catalog-closure", "REQUIRED_INPUT_CLASS_MISSING", f"required input class has no included input: {input_class}", input_class)
        per_class.append({"input_class": input_class, "candidate_count": values["candidate"], "included_count": values["included"], "excluded_count": values["excluded"], "status": status})

    for conflict in closure["input_conflicts"]:
        if any(input_id not in input_ids for input_id in conflict["input_ids"]):
            add("conflict-closure", "INPUT_AUTHORITY_UNRESOLVED", f"conflict names unknown input: {conflict['conflict_id']}", conflict["conflict_id"])
        if conflict["resolution_status"] != "resolved":
            add("conflict-closure", "CONFLICT_UNRESOLVED", f"input conflict is unresolved: {conflict['conflict_id']}", conflict["conflict_id"])
        elif conflict.get("decision_ref") is not None:
            validate_file_ref(conflict["decision_ref"], "conflict-closure")

    current_design_paths = sorted(
        item["source_ref"]["path"]
        for item in closure["input_catalog"]
        if item["kind"] == "current-design" and item["input_id"] in selected_ids
    )
    prior_result["candidate_paths"] = current_design_paths
    kind = closure["design_kind"]["kind"]
    if kind == "greenfield":
        evidence_path = validate_file_ref(
            closure["design_kind"]["no_prior_design_determination_ref"], "prior-design"
        )
        if current_design_paths:
            add("prior-design", "GREENFIELD_CONTRADICTED", "greenfield closure contains an applicable current Design", current_design_paths[0])
        if evidence_path is not None:
            try:
                determination = load_json(evidence_path)
                required_keys = {
                    "schema_version",
                    "target_id",
                    "observation_epoch",
                    "applicable_prior_design_paths",
                    "determined_by",
                    "authority_effect",
                    "determination_digest",
                }
                if set(determination) != required_keys:
                    raise ClosureFailure(
                        "GREENFIELD_CONTRADICTED",
                        "no-prior determination has an unexpected field set",
                        closure["design_kind"]["no_prior_design_determination_ref"]["path"],
                    )
                if (
                    determination["schema_version"]
                    != "invoke.design-no-prior-determination.v1"
                    or determination["target_id"] != closure["target"]["id"]
                    or determination["observation_epoch"]
                    != boundary["observation_epoch"]
                    or determination["applicable_prior_design_paths"] != []
                    or determination["determined_by"] != closure["target"]["owner"]
                    or determination["authority_effect"] != "none"
                    or digest_without(determination, "determination_digest")
                    != determination["determination_digest"]
                ):
                    raise ClosureFailure(
                        "GREENFIELD_CONTRADICTED",
                        "no-prior determination does not bind this target, epoch, owner, and zero candidates",
                        closure["design_kind"]["no_prior_design_determination_ref"]["path"],
                    )
            except (OSError, json.JSONDecodeError, ClosureFailure) as error:
                code = error.code if isinstance(error, ClosureFailure) else "GREENFIELD_CONTRADICTED"
                selector = (
                    error.selector
                    if isinstance(error, ClosureFailure)
                    else closure["design_kind"]["no_prior_design_determination_ref"]["path"]
                )
                add("prior-design", code, str(error), selector)
            prior_result["evidence_refs"] = [exact_ref(evidence_path, repository_root)]
        prior_result["status"] = "pass" if not direct["prior-design"] else "block"
    else:
        if not current_design_paths:
            add("prior-design", "PRIOR_DESIGN_MISSING", "evolution closure has no applicable current Design")
        elif len(current_design_paths) > 1:
            add("prior-design", "PRIOR_DESIGN_AMBIGUOUS", "evolution closure has multiple applicable current Designs", current_design_paths[0])
        artifact_path = validate_file_ref(closure["design_kind"]["prior_design_artifact_ref"], "prior-design")
        receipt_path = validate_file_ref(closure["design_kind"]["prior_design_stage_receipt_ref"], "prior-design")
        if artifact_path is not None and current_design_paths and closure["design_kind"]["prior_design_artifact_ref"]["path"] != current_design_paths[0]:
            add("prior-design", "PRIOR_DESIGN_RECEIPT_INVALID", "selected predecessor differs from the applicable current Design", current_design_paths[0])
        if receipt_path is not None:
            prior_receipt = load_json(receipt_path)
            errors = schema_messages(prior_receipt, schemas["design-result-v2.schema.json"])
            if errors:
                add("prior-design", "PRIOR_DESIGN_RECEIPT_INVALID", "; ".join(errors), closure["design_kind"]["prior_design_stage_receipt_ref"]["path"])
            else:
                bundle_dir = receipt_path.parent
                contract_errors = validate_stage_receipt(
                    prior_receipt, installed_root, schema_dir, bundle_dir
                )
                if contract_errors:
                    add(
                        "prior-design",
                        "PRIOR_DESIGN_RECEIPT_INVALID",
                        "; ".join(contract_errors),
                        closure["design_kind"]["prior_design_stage_receipt_ref"]["path"],
                    )
                elif prior_receipt["target_id"] != closure["target"]["id"]:
                    add("prior-design", "PRIOR_DESIGN_RECEIPT_INVALID", "prior Design target differs from this evolution target", "target_id")
                else:
                    expected_artifact = {
                        "path": (PurePosixPath(closure["design_kind"]["prior_design_stage_receipt_ref"]["path"]).parent / DESIGN_STAGE_OUTPUTS[0][1]).as_posix(),
                        "sha256": prior_receipt["outputs"][0]["sha256"],
                        "size": prior_receipt["outputs"][0]["size"],
                    }
                    closure_prior_artifact = {
                        key: closure["design_kind"]["prior_design_artifact_ref"][key]
                        for key in ["path", "sha256", "size"]
                    }
                    if closure_prior_artifact != expected_artifact:
                        add("prior-design", "PRIOR_DESIGN_RECEIPT_INVALID", "prior Design artifact does not match the v2 stage output binding", closure["design_kind"]["prior_design_artifact_ref"]["path"])
            prior_result["evidence_refs"].append(exact_ref(receipt_path, repository_root))
        if artifact_path is not None:
            prior_result["evidence_refs"].append(exact_ref(artifact_path, repository_root))
        prior_result["status"] = "pass" if not direct["prior-design"] else "block"

    if activation_kind == "normal":
        define_receipt_path = validate_file_ref(
            closure["activation"]["define_stage_receipt_ref"],
            "boundary-approval",
            "ACTIVATION_RECEIPT_INVALID",
        )
        if define_receipt_path is not None:
            try:
                define_receipt = load_json(define_receipt_path)
                errors = schema_messages(define_receipt, schemas["define-result-v2.schema.json"])
                if (
                    errors
                    or define_receipt.get("result") != "pass"
                    or digest_without(define_receipt, "receipt_digest")
                    != define_receipt.get("receipt_digest")
                ):
                    raise ClosureFailure("ACTIVATION_RECEIPT_INVALID", "; ".join(errors) or "Define receipt does not pass or has a stale digest", closure["activation"]["define_stage_receipt_ref"]["path"])
                producer = define_receipt["producer"]
                producer_path = installed_root / producer["path"]
                if not producer_path.is_file() or hashlib.sha256(producer_path.read_bytes()).hexdigest() != producer["sha256"]:
                    raise ClosureFailure("ACTIVATION_RECEIPT_INVALID", "Define producer is unavailable or stale", producer["path"])
                source_path = resolve_inside(repository_root, define_receipt["source_ref"]["path"])
                source_data = source_path.read_bytes()
                if (
                    not source_path.is_file()
                    or source_path.is_symlink()
                    or hashlib.sha256(source_data).hexdigest()
                    != define_receipt["source_ref"]["sha256"]
                    or len(source_data) != define_receipt["source_ref"]["size"]
                ):
                    raise ClosureFailure(
                        "ACTIVATION_RECEIPT_INVALID",
                        "Define source exact ref is stale",
                        define_receipt["source_ref"]["path"],
                    )
                define_source = load_json(source_path)
                definitions_schema = schemas["definitions.schema.json"]
                source_errors = schema_messages(
                    define_source,
                    schemas["define-source-v2.schema.json"],
                    {
                        definitions_schema["$id"]: definitions_schema,
                        "https://arcanum.dev/schemas/invoke/definitions.schema.json": definitions_schema,
                        "definitions.schema.json": definitions_schema,
                    },
                )
                if source_errors or define_source.get("target", {}).get("id") != closure["target"]["id"]:
                    raise ClosureFailure("ACTIVATION_RECEIPT_INVALID", "; ".join(source_errors) or "Define target differs from Design target", define_receipt["source_ref"]["path"])
                expected_define_kinds = {
                    "spec",
                    "definitions",
                    "definitions-view",
                    "glossary",
                    "layering",
                    "template-selection",
                    "dispatch-trace",
                    "distill",
                    "identity-denominator",
                    "transport",
                }
                actual_define_kinds = {
                    item["kind"] for item in define_receipt["outputs"]
                }
                if actual_define_kinds != expected_define_kinds:
                    raise ClosureFailure(
                        "ACTIVATION_RECEIPT_INVALID",
                        "Define receipt output kinds do not equal the v2 inventory",
                        closure["activation"]["define_stage_receipt_ref"]["path"],
                    )
                output_paths: set[str] = set()
                for output in define_receipt["outputs"]:
                    output_path = resolve_inside(
                        define_receipt_path.parent, output["path"]
                    )
                    output_data = output_path.read_bytes()
                    if (
                        not output_path.is_file()
                        or output_path.is_symlink()
                        or hashlib.sha256(output_data).hexdigest() != output["sha256"]
                        or len(output_data) != output["size"]
                    ):
                        raise ClosureFailure(
                            "ACTIVATION_RECEIPT_INVALID",
                            f"Define output exact ref is stale: {output['path']}",
                            output["path"],
                        )
                    normalized_output = output_path.relative_to(
                        define_receipt_path.parent
                    ).as_posix()
                    if normalized_output in output_paths:
                        raise ClosureFailure(
                            "ACTIVATION_RECEIPT_INVALID",
                            f"Define output path is duplicated: {output['path']}",
                            output["path"],
                        )
                    output_paths.add(normalized_output)
                definitions_output = next((item for item in define_receipt["outputs"] if item["kind"] == "definitions"), None)
                if definitions_output is None:
                    raise ClosureFailure("ACTIVATION_RECEIPT_INVALID", "Define receipt lacks definitions output")
                output_path = resolve_inside(
                    define_receipt_path.parent, definitions_output["path"]
                )
                define_catalog = [item for item in closure["input_catalog"] if item["kind"] == "define-artifact" and item["input_id"] in selected_ids]
                expected_path = output_path.resolve().relative_to(repository_root.resolve()).as_posix()
                if len(define_catalog) != 1 or define_catalog[0]["source_ref"]["path"] != expected_path:
                    raise ClosureFailure("ACTIVATION_RECEIPT_INVALID", "normal activation must bind exactly the produced definitions artifact", expected_path)
            except (OSError, json.JSONDecodeError, ClosureFailure) as error:
                code = error.code if isinstance(error, ClosureFailure) else "ACTIVATION_RECEIPT_INVALID"
                selector = error.selector if isinstance(error, ClosureFailure) else closure["activation"]["define_stage_receipt_ref"]["path"]
                add("boundary-approval", code, str(error), selector)

    signal_ids: set[str] = set()
    covered_inputs: set[str] = set()
    for field, records in closure["scope_signals"].items():
        for record in records:
            if record["signal_id"] in signal_ids:
                add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", f"duplicate scope signal id: {record['signal_id']}", record["signal_id"])
            signal_ids.add(record["signal_id"])
            if record["source_input_id"] not in selected_ids:
                add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", f"scope signal source is not included: {record['signal_id']}", record["source_input_id"])
            covered_inputs.add(record["source_input_id"])
            if field == "acceptance_and_readiness_claims" and record["evidence_state"] != "authored-complete":
                add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", "W1 cannot author validator-pass readiness evidence", record["signal_id"])
    for obligation in closure["constraints"] + closure["invariants"]:
        covered_inputs.update(obligation["source_input_ids"])
        for input_id in obligation["source_input_ids"]:
            if input_id not in selected_ids:
                add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", f"obligation binds a non-included input: {obligation['obligation_id']}", input_id)

    concerns = {item["concern_id"]: item for item in closure["selection_inputs"]["authored_concerns"]}
    predicates = closure["selection_inputs"]["predicate_inputs"]
    predicate_by_concern = {item["concern_id"]: item for item in predicates}
    if len(predicate_by_concern) != len(predicates):
        add("scope-signal-coverage", "INPUT_DUPLICATE", "duplicate predicate assertion for one concern", "selection_inputs.predicate_inputs")
    if set(predicate_by_concern) != set(concerns):
        add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", "every authored concern requires exactly one predicate assertion", "selection_inputs.predicate_inputs")
    for concern_id, predicate in predicate_by_concern.items():
        concern = concerns.get(concern_id)
        if concern is not None and predicate["expected"] != concern["required_predicate"]:
            add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", f"predicate assertion differs from authored concern: {concern_id}", concern_id)
        covered_inputs.update(predicate["source_input_ids"])
        if any(input_id not in selected_ids for input_id in predicate["source_input_ids"]):
            add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", f"predicate assertion binds a non-included input: {concern_id}", concern_id)
    for input_id in sorted(selected_ids - covered_inputs):
        add("scope-signal-coverage", "SCOPE_SIGNAL_INVALID", f"included input has no typed signal, obligation, or predicate use: {input_id}", input_id)

    if not any(direct[check_id] for check_id in CHECK_IDS[:-1]):
        try:
            provisional = {
                "verdict": "pass",
                "expected_manifest": None,
            }
            projector = load_projection_module(script_dir)
            manifest = projector.project_scope_manifest(
                closure,
                provisional,
                repository_root,
                schemas["design-scope-manifest.schema.json"],
                enforce_receipt_binding=False,
            )
            expected_manifest = {
                "manifest_id": manifest["manifest_id"],
                "input_digest": manifest["input_digest"],
            }
        except Exception as error:
            add("manifest-projection", "MANIFEST_PROJECTION_MISMATCH", str(error), "scope_signals")

    all_blocker_ids = [item["blocker_id"] for item in blockers]
    checks = []
    for check_id in CHECK_IDS:
        if direct[check_id]:
            status = "block"
            causal = direct[check_id]
        elif check_id == "manifest-projection" and all_blocker_ids:
            status = "not_evaluable"
            causal = all_blocker_ids
        else:
            status = "pass"
            causal = []
        checks.append({"check_id": check_id, "status": status, "evidence_refs": [], "causal_blocker_ids": causal})

    verdict = "block" if blockers else "pass"
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1",
        "schema_version": "invoke.design-input-closure-receipt.v1",
        "receipt_id": f"closure-receipt:{closure_id}:{declared_closure_digest[:16]}",
        "validator": {"identity": VALIDATOR_ID, "owner": VALIDATOR_OWNER, "path": VALIDATOR_PATH, "sha256": script_ref["sha256"]},
        "bindings": {"process_ref": process_ref, "design_input_closure_ref": closure_ref, "boundary_approval_ref": approval_ref, "closure_digest": declared_closure_digest, "discovery_boundary_digest": declared_boundary_digest},
        "activation_kind": activation_kind,
        "inspected_boundary": {"root_refs": sorted(root_receipt_refs, key=lambda item: item["path"]), "rule_ids": sorted(rule_ids), "required_input_classes": sorted(boundary["required_input_classes"])},
        "discovery": {"inventory": sorted(inventory, key=lambda item: item["path"]), "inventory_digest": canonical_digest(sorted(inventory, key=lambda item: item["path"])), "cataloged_paths": sorted(set(cataloged_paths)), "excluded_paths": sorted(set(excluded_paths)), "unclassified_paths": sorted(set(unclassified_paths)), "ambiguous_paths": sorted(set(ambiguous_paths)), "per_class": per_class},
        "conditional_resolutions": sorted(conditional_results, key=lambda item: item["input_id"]),
        "prior_design_determination": prior_result,
        "expected_manifest": expected_manifest,
        "checks": checks,
        "verdict": verdict,
        "blockers": sorted(blockers, key=lambda item: (item["code"], item["selector"] or "", item["blocker_id"])),
        "authority_effect": "none",
        "receipt_digest": ZERO_DIGEST,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    receipt_errors = schema_messages(
        receipt, schemas["design-input-closure-receipt-v1.schema.json"]
    )
    if receipt_errors:
        raise RuntimeError("closure receipt schema invalid: " + "; ".join(receipt_errors))
    return receipt


def atomic_write_json(path: Path, document: dict[str, Any]) -> None:
    if path.exists():
        raise ValueError(f"output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("closure", type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    schema_dir = args.schema_dir or Path(__file__).resolve().parent.parent / "schemas"
    try:
        closure = load_json(args.closure)
        receipt = validate_input_closure(
            closure,
            args.closure.resolve(),
            args.repository_root.resolve(),
            schema_dir.resolve(),
        )
        atomic_write_json(args.output.resolve(), receipt)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as error:
        print(f"ERROR: {error}")
        return 2
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
