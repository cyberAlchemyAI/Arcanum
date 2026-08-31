#!/usr/bin/env python3
"""Validate Design input closure v2 with admitted Define and Design predecessors."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

from define_stage_contract import (
    validate_admission_receipt as validate_define_admission,
    validate_stage_receipt as validate_define_stage,
)
from design_stage_contract_v2 import (
    OUTPUTS as DESIGN_OUTPUTS,
    validate_admission_receipt as validate_design_admission,
    validate_stage_receipt as validate_design_stage,
)
from design_successor_support import canonical_digest, load_module, load_store


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR_ID = "invoke.validate-design-input-closure.v2"
VALIDATOR_OWNER = "invoke-design-input-closure-validator"
VALIDATOR_PATH = "arcanum/spells/invoke/scripts/validate_design_input_closure_v2.py"
CHECK_ORDER = (
    "closure-schema", "closure-digest", "process-binding", "boundary-approval",
    "define-predecessor-admission", "path-safety", "boundary-freshness",
    "discovery-enumeration", "catalog-closure", "input-freshness", "visibility",
    "conditional-resolution", "conflict-closure", "prior-design",
    "design-predecessor-admission", "scope-signal-coverage", "manifest-projection",
)


def _exact_ref(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.resolve().relative_to(root.resolve()).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def _load_bound(ref: dict[str, Any], root: Path, old: Any) -> tuple[Path, dict[str, Any]]:
    path = old.resolve_inside(root, ref["path"])
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"regular exact-ref file required: {ref['path']}")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != ref["sha256"] or len(data) != ref["size"]:
        raise ValueError(f"exact ref is stale: {ref['path']}")
    value = json.loads(data)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {ref['path']}")
    return path, value


def _blocker(code: str, message: str, selector: str | None, index: int) -> dict[str, Any]:
    return {
        "blocker_id": f"successor-blocker:{index:03d}:{code.lower()}",
        "code": code,
        "message": message,
        "selector": selector,
        "owner": "design-input-owner",
        "repair_route": "Supply the exact current admitted predecessor and rerun Design input closure validation.",
    }


def validate_input_closure(
    closure: dict[str, Any],
    closure_path: Path,
    repository_root: Path,
    schema_dir: Path,
) -> dict[str, Any]:
    old = load_module("invoke_design_input_v1_compat", SCRIPT_DIR / "validate_design_input_closure.py")
    store = load_store(schema_dir)
    schema = store.get("https://arcanum.dev/schemas/invoke/design-input-closure/v2")
    receipt_schema = store.get("https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v2")
    if schema is None or receipt_schema is None:
        raise RuntimeError("Design input successor schemas are unavailable")
    resolver = RefResolver.from_schema(schema, store=store)
    source_errors = [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema, resolver=resolver).iter_errors(closure), key=lambda item: list(item.absolute_path))
    ]
    if source_errors:
        raise ValueError("Design input closure v2 schema invalid: " + "; ".join(source_errors[:12]))
    if canonical_digest(closure, "closure_digest") != closure["closure_digest"]:
        raise ValueError("Design input closure v2 digest mismatch")

    predecessor_blockers: list[dict[str, Any]] = []
    define_stage_ref = define_admission_ref = None
    prior_stage_ref = prior_admission_ref = None
    activation = closure["activation"]
    if activation["kind"] == "normal":
        diagnostics: list[str] = []
        stage_path: Path | None = None
        admission_path: Path | None = None
        stage: dict[str, Any] | None = None
        admission: dict[str, Any] | None = None
        try:
            stage_path, stage = _load_bound(
                activation["define_stage_receipt_ref"], repository_root, old
            )
        except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
            diagnostics.append(f"Define stage receipt unavailable or stale: {error}")
        try:
            admission_path, admission = _load_bound(
                activation["define_admission_receipt_ref"], repository_root, old
            )
        except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
            diagnostics.append(f"Define admission receipt unavailable or stale: {error}")
        if stage is not None:
            diagnostics.extend(validate_define_stage(stage, repository_root, schema_dir))
        if stage is not None and admission is not None and stage_path is not None:
            diagnostics.extend(
                validate_define_admission(admission, stage, repository_root, schema_dir)
            )
            if admission.get("stage_receipt_ref") != _exact_ref(
                stage_path, repository_root
            ):
                diagnostics.append(
                    "Define admission stage_receipt_ref differs from the activation stage ref"
                )
        if stage is not None and stage_path is not None:
            try:
                source_path, define_source = _load_bound(
                    stage["source_ref"], repository_root, old
                )
                context_path, define_context = _load_bound(
                    stage["semantic_evidence"]["context_ref"], repository_root, old
                )
                if define_context.get("target", {}).get("id") != closure["target"]["id"]:
                    diagnostics.append("Define and Design target identities differ")
                define_outputs = [
                    item
                    for item in stage.get("outputs", [])
                    if item.get("kind") == "definitions"
                ]
                if len(define_outputs) != 1:
                    diagnostics.append(
                        "Define stage must expose exactly one definitions output"
                    )
                else:
                    definitions_path = stage_path.parent / define_outputs[0]["path"]
                    definitions_ref = _exact_ref(definitions_path, repository_root)
                    included = [
                        item
                        for item in closure["input_catalog"]
                        if item["kind"] == "define-artifact"
                        and item["classification"] != "excluded"
                    ]
                    if len(included) != 1 or {
                        key: included[0]["source_ref"][key]
                        for key in ("path", "sha256", "size")
                    } != definitions_ref:
                        diagnostics.append(
                            "normal activation must catalog exactly the admitted Define definitions artifact"
                        )
                del source_path, context_path, define_source
            except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
                diagnostics.append(f"Define source or definitions binding invalid: {error}")
        define_stage_ref = (
            _exact_ref(stage_path, repository_root) if stage_path is not None else None
        )
        define_admission_ref = (
            _exact_ref(admission_path, repository_root)
            if admission_path is not None
            else None
        )
        if diagnostics:
            predecessor_blockers.append(_blocker("ACTIVATION_RECEIPT_INVALID", "; ".join(diagnostics[:12]), activation["define_stage_receipt_ref"]["path"], 1))

    design_kind = closure["design_kind"]
    if design_kind["kind"] == "evolution":
        diagnostics = []
        stage_path = None
        admission_path = None
        stage = None
        admission = None
        try:
            stage_path, stage = _load_bound(
                design_kind["prior_design_stage_receipt_ref"], repository_root, old
            )
        except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
            diagnostics.append(f"prior Design stage receipt unavailable or stale: {error}")
        try:
            admission_path, admission = _load_bound(
                design_kind["prior_design_admission_receipt_ref"], repository_root, old
            )
        except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
            diagnostics.append(
                f"prior Design admission receipt unavailable or stale: {error}"
            )
        if stage is not None and stage_path is not None:
            diagnostics.extend(
                validate_design_stage(
                    stage, repository_root, schema_dir, stage_path.parent
                )
            )
        if stage is not None and admission is not None and stage_path is not None:
            diagnostics.extend(
                validate_design_admission(
                    admission, stage, repository_root, schema_dir
                )
            )
            if admission.get("stage_receipt_ref") != _exact_ref(
                stage_path, repository_root
            ):
                diagnostics.append(
                    "Design admission stage_receipt_ref differs from the selected predecessor"
                )
        if stage is not None and stage.get("target_id") != closure["target"]["id"]:
            diagnostics.append(
                "prior Design and successor Design target identities differ"
            )
        prior_stage_ref = (
            _exact_ref(stage_path, repository_root) if stage_path is not None else None
        )
        prior_admission_ref = (
            _exact_ref(admission_path, repository_root)
            if admission_path is not None
            else None
        )
        if diagnostics:
            predecessor_blockers.append(_blocker("PRIOR_DESIGN_RECEIPT_INVALID", "; ".join(diagnostics[:12]), design_kind["prior_design_stage_receipt_ref"]["path"], 2))

    projected = copy.deepcopy(closure)
    projected["$schema"] = "https://arcanum.dev/schemas/invoke/design-input-closure/v1"
    projected["schema_version"] = "invoke.design-input-closure.v1"
    if activation["kind"] == "normal":
        projected["activation"] = {"kind": "discovery", "approval_ref": copy.deepcopy(activation["approval_ref"]), "rationale": "Compatibility projection; Define v3 admission was evaluated by the successor validator."}
    if projected["design_kind"]["kind"] == "evolution":
        projected["design_kind"].pop("prior_design_admission_receipt_ref", None)
    projected["closure_digest"] = canonical_digest(projected, "closure_digest")

    original_schema_messages = old.schema_messages
    original_load_json = old.load_json
    original_stage_validator = old.validate_stage_receipt
    original_outputs = old.DESIGN_STAGE_OUTPUTS

    def schema_messages(document: dict[str, Any], selected: dict[str, Any], selected_store: dict[str, dict[str, Any]] | None = None) -> list[str]:
        if document.get("schema_version") == "invoke.design-stage-receipt.v3" and selected.get("$id") == "https://arcanum.dev/schemas/invoke/design-result/v2":
            current = store["https://arcanum.dev/schemas/invoke/design-result/v3"]
            resolver = RefResolver.from_schema(current, store=store)
            return [error.message for error in Draft202012Validator(current, resolver=resolver).iter_errors(document)]
        if selected.get("$id") == "https://arcanum.dev/schemas/invoke/definitions/v2":
            resolver = RefResolver.from_schema(selected, store=store)
            return [error.message for error in Draft202012Validator(selected, resolver=resolver).iter_errors(document)]
        return original_schema_messages(document, selected, selected_store)

    old.schema_messages = schema_messages
    old.load_json = lambda path: original_load_json(
        schema_dir / "definitions-v2.schema.json"
        if path.parent.resolve() == schema_dir.resolve() and path.name == "definitions.schema.json"
        else path
    )
    old.validate_stage_receipt = validate_design_stage
    old.DESIGN_STAGE_OUTPUTS = DESIGN_OUTPUTS
    try:
        base = old.validate_input_closure(projected, closure_path, repository_root, schema_dir)
    finally:
        old.schema_messages = original_schema_messages
        old.load_json = original_load_json
        old.validate_stage_receipt = original_stage_validator
        old.DESIGN_STAGE_OUTPUTS = original_outputs

    base_checks = {item["check_id"]: copy.deepcopy(item) for item in base["checks"]}
    external = {
        "define-predecessor-admission": [item for item in predecessor_blockers if item["code"] == "ACTIVATION_RECEIPT_INVALID"],
        "design-predecessor-admission": [item for item in predecessor_blockers if item["code"] == "PRIOR_DESIGN_RECEIPT_INVALID"],
    }
    checks = []
    for check_id in CHECK_ORDER:
        if check_id in external:
            causes = [item["blocker_id"] for item in external[check_id]]
            checks.append({"check_id": check_id, "status": "block" if causes else "pass", "evidence_refs": [], "causal_blocker_ids": causes})
        else:
            checks.append(base_checks[check_id])
    blockers = copy.deepcopy(base["blockers"]) + predecessor_blockers
    receipt = copy.deepcopy(base)
    receipt["$schema"] = "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v2"
    receipt["schema_version"] = "invoke.design-input-closure-receipt.v2"
    receipt["validator"] = {"identity": VALIDATOR_ID, "owner": VALIDATOR_OWNER, "path": VALIDATOR_PATH, "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    receipt["bindings"] = {
        **base["bindings"],
        "design_input_closure_ref": _exact_ref(closure_path, repository_root),
        "define_stage_receipt_ref": define_stage_ref,
        "define_admission_receipt_ref": define_admission_ref,
        "prior_design_stage_receipt_ref": prior_stage_ref,
        "prior_design_admission_receipt_ref": prior_admission_ref,
        "closure_digest": closure["closure_digest"],
        "discovery_boundary_digest": closure["discovery_boundary"]["boundary_digest"],
    }
    receipt["activation_kind"] = activation["kind"]
    receipt["design_kind"] = design_kind["kind"]
    receipt["checks"] = checks
    receipt["blockers"] = sorted(blockers, key=lambda item: (item["code"], item.get("selector") or "", item["blocker_id"]))
    receipt["verdict"] = "block" if blockers else "pass"
    receipt["receipt_digest"] = canonical_digest(receipt, "receipt_digest")
    resolver = RefResolver.from_schema(receipt_schema, store=store)
    errors = [error.message for error in Draft202012Validator(receipt_schema, resolver=resolver).iter_errors(receipt)]
    if errors:
        raise RuntimeError("Design input closure receipt v2 schema invalid: " + "; ".join(errors[:12]))
    return receipt


def _write_absent(path: Path, document: dict[str, Any]) -> None:
    path = Path(os.path.abspath(path))
    if path.exists() or path.is_symlink() or not path.parent.is_dir():
        raise ValueError("output must be one absent file with an existing parent")
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("closure", type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    schema_dir = args.schema_dir or SCRIPT_DIR.parent / "schemas"
    try:
        closure = json.loads(args.closure.read_text(encoding="utf-8"))
        receipt = validate_input_closure(closure, args.closure.resolve(), args.repository_root.resolve(), schema_dir.resolve())
        _write_absent(args.output, receipt)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
