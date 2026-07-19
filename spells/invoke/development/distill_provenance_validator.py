#!/usr/bin/env python3
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from distill_runtime_events import load_jsonl, load_schema
from distill_semantic_validator import SemanticValidationError, validate_semantic_case


def _schema_errors(document: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} schema invalid: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path))
    ]


def _exact_ref(path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": str(path.name),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def _validation_result(case: dict[str, Any], receipt_ref: dict[str, Any], checks: list[str], diagnostics: list[str]) -> dict[str, Any]:
    status = "pass" if not diagnostics else "block"
    return {
        "schema_version": "1.0.0",
        "validation_result_id": case["validation_result_id"],
        "validator_version": "0.2.0",
        "receipt_ref": receipt_ref,
        "status": status,
        "checks": [
            {"check_id": check, "status": "pass" if not diagnostics else "block", "evidence_refs": []}
            for check in checks
        ],
        "diagnostics": diagnostics,
        "owned_gaps": ["DEE-005-PROVENANCE"] if diagnostics else [],
        "mutation_handoff_allowed": status == "pass",
    }


def validate_provenance_case(
    case: dict[str, Any],
    schema_dir: Path,
    fixture_dir: Path,
    reviewed_root: Path,
) -> dict[str, Any]:
    base_case = json.loads((fixture_dir / case["semantic_case"]).read_text(encoding="utf-8"))
    provenance_ref = case["reviewed_input_ref"]
    base_case = copy.deepcopy(base_case)
    base_case["request"]["reviewed_inputs"] = [provenance_ref]
    base_case["receipt"]["reviewed_input_provenance"] = [provenance_ref]
    receipt_ref = case["receipt_ref"]
    result_schema = load_schema(schema_dir / "distill-validation-result.schema.json")
    request_schema = load_schema(schema_dir / "distill-run-request.schema.json")
    receipt_schema = load_schema(schema_dir / "distill-execution-receipt.schema.json")
    diagnostics: list[str] = []
    checks = [
        "semantic_result_passes",
        "reviewed_input_digest_and_size",
        "request_receipt_provenance_agrees",
        "run_identity_agrees",
        "verdict_agrees",
        "event_count_agrees",
        "work_pack_binding_agrees",
    ]

    for label, document, schema in (
        ("request", base_case["request"], request_schema),
        ("receipt", base_case["receipt"], receipt_schema),
    ):
        diagnostics.extend(_schema_errors(document, schema, label))

    try:
        semantic_result = validate_semantic_case(base_case, schema_dir, fixture_dir)
        if semantic_result["semantic_status"] != "pass":
            diagnostics.append("semantic result did not pass")
    except SemanticValidationError as error:
        diagnostics.append(f"semantic validation failed: {error}")

    request_refs = base_case["request"]["reviewed_inputs"]
    receipt_refs = base_case["receipt"]["reviewed_input_provenance"]
    if request_refs != receipt_refs:
        diagnostics.append("request and receipt provenance sets disagree")

    for reference in request_refs:
        target = reviewed_root / reference["path"]
        if not target.is_file():
            diagnostics.append(f"unresolved reviewed input: {reference['path']}")
            continue
        actual = _exact_ref(target)
        if actual["sha256"] != reference["sha256"] or actual["size_bytes"] != reference["size_bytes"]:
            diagnostics.append(f"reviewed input digest mismatch: {reference['path']}")

    events = load_jsonl(fixture_dir / base_case["events_fixture"])
    invoke_result = case["invoke_result"]
    observability = case["observability"]
    work_pack = case["work_pack_state"]
    expected_run_id = base_case["receipt"]["run_id"]
    if invoke_result.get("run_id") != expected_run_id or observability.get("run_id") != expected_run_id:
        diagnostics.append("cross-artifact run identity mismatch")
    if base_case["receipt"]["verdict"] != invoke_result.get("verdict"):
        diagnostics.append("receipt and Invoke verdict mismatch")
    if invoke_result.get("event_count") != len(events) or observability.get("event_count") != len(events):
        diagnostics.append("cross-artifact event count mismatch")
    if work_pack.get("work_pack_id") != "distill-execution-evidence" or work_pack.get("selected_swu") != "SWU-DEE-005":
        diagnostics.append("stale Work Pack binding")

    result = _validation_result(case, receipt_ref, checks, diagnostics)
    result_errors = _schema_errors(result, result_schema, "validation result")
    if result_errors:
        raise SemanticValidationError(result_errors[0])
    return result


def load_case(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
