#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from distill_runtime_events import load_jsonl, load_schema, resolve_events


class SemanticValidationError(ValueError):
    pass


ALLOWED_TERMINATION_REASONS = {
    "round_budget_satisfied",
    "reconciled",
    "blocked",
    "cycle_guard",
}
ALLOWED_CATEGORIES = {
    "authority",
    "coverage",
    "process",
    "provenance",
    "role",
    "scope",
    "technique",
    "other",
}
ALLOWED_DISPOSITIONS = {"accept", "revise", "reject", "defer", "route"}


def _validate_document(document: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or label
        raise SemanticValidationError(f"{label} schema invalid at {location}: {error.message}")


def validate_semantic_case(
    case: dict[str, Any],
    schema_dir: Path,
    fixture_dir: Path,
) -> dict[str, Any]:
    request = case["request"]
    receipt = case["receipt"]
    request_schema = load_schema(schema_dir / "distill-run-request.schema.json")
    receipt_schema = load_schema(schema_dir / "distill-execution-receipt.schema.json")
    event_schema = load_schema(schema_dir / "distill-runtime-event.schema.json")
    _validate_document(request, request_schema, "request")
    _validate_document(receipt, receipt_schema, "receipt")

    events = load_jsonl(fixture_dir / case["events_fixture"])
    resolved = resolve_events(events, event_schema)
    event_ids = {event["event_id"] for event in events}

    if request["run_id"] != receipt["run_id"] or receipt["run_id"] != resolved["run_id"]:
        raise SemanticValidationError("run identity disagreement")
    if set(receipt["event_refs"]) != event_ids:
        raise SemanticValidationError("receipt event references do not cover the resolved event sequence")
    if receipt["termination"]["round_count"] > request["round_budget"]["max_rounds"]:
        raise SemanticValidationError("termination round_count exceeds round budget")
    if receipt["termination"]["reason"] not in ALLOWED_TERMINATION_REASONS:
        raise SemanticValidationError("termination reason is not allowed")

    objection_ids = []
    for objection in receipt["objections"]:
        objection_id = objection.get("objection_id")
        category = objection.get("category")
        if not objection_id:
            raise SemanticValidationError("objection_id required for every objection")
        if not category or category not in ALLOWED_CATEGORIES:
            raise SemanticValidationError(f"objection category required for {objection_id}")
        objection_ids.append(objection_id)
    if len(objection_ids) != len(set(objection_ids)):
        raise SemanticValidationError("objection IDs must be unique")

    reconciliations = receipt["reconciliations"]
    for objection_id in objection_ids:
        matches = [item for item in reconciliations if item.get("objection_ref") == objection_id]
        if len(matches) != 1:
            raise SemanticValidationError(f"exactly one reconciliation required for {objection_id}")
        if matches[0].get("disposition") not in ALLOWED_DISPOSITIONS:
            raise SemanticValidationError(f"reconciliation disposition required for {objection_id}")

    requested_techniques = set(request["requested_techniques"])
    traced_techniques = {item["technique"]: item["status"] for item in receipt["technique_trace"]}
    missing_techniques = sorted(requested_techniques - set(traced_techniques))
    if missing_techniques:
        raise SemanticValidationError(f"missing technique trace: {','.join(missing_techniques)}")
    failed_techniques = sorted(
        technique for technique in requested_techniques if traced_techniques[technique] == "failed"
    )
    if failed_techniques:
        raise SemanticValidationError(f"failed technique trace: {','.join(failed_techniques)}")

    return {
        "semantic_status": "pass",
        "authority": "semantic_evidence_only",
        "diagnostics": [],
        "checks": [
            "schemas_valid",
            "identity_agrees",
            "event_references_complete",
            "role_process_resolved",
            "round_budget_valid",
            "objections_categorized",
            "reconciliations_complete",
            "techniques_traced",
        ],
        "resolved_event_count": len(events),
        "role_trace": resolved["role_trace"],
    }


def load_case(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
