#!/usr/bin/env python3
"""Pure, phase-bounded pre-execution prerequisite classifier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


TASK_SESSION_ROOT = Path(__file__).resolve().parents[1]
PREREQUISITE_SCHEMA = json.loads(
    (TASK_SESSION_ROOT / "schemas" / "pre-execution-owner-prerequisite.schema.json").read_text(encoding="utf-8")
)
RECEIPT_SCHEMA = json.loads(
    (TASK_SESSION_ROOT / "schemas" / "pre-execution-prerequisite-receipt.schema.json").read_text(encoding="utf-8")
)
PREREQUISITE_VALIDATOR = Draft202012Validator(PREREQUISITE_SCHEMA)
RECEIPT_VALIDATOR = Draft202012Validator(RECEIPT_SCHEMA)


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def prerequisite_fingerprint(prerequisite: dict[str, Any]) -> str:
    fields = prerequisite["fingerprint_inputs"]
    return canonical_digest({field: prerequisite[field] for field in fields})


def json_pointer(document: Any, pointer: str) -> Any:
    value = document
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def phase_trace() -> dict[str, Any]:
    return {
        "resolved": True,
        "prerequisite_classified": True,
        "context_builder_entered": False,
        "mutation_admission_entered": False,
        "implementation_inspected": False,
        "target_mutation_entered": False,
        "owner_hops_dispatched": 0,
    }


def build_receipt(
    *,
    selected_unit: dict[str, Any],
    prerequisite_id: str,
    classification: str,
    fingerprint: str,
    inputs_read: list[str],
    authorization_status: str,
    authorization_ref: dict[str, Any] | None,
    permitted_next_action: str,
    reasons: list[str],
) -> dict[str, Any]:
    receipt = {
        "schema_version": "task-session.pre-execution-prerequisite-receipt.v1",
        "receipt_id": f"pep-classification:{selected_unit['attempt_id']}:{fingerprint[:16]}",
        "prerequisite_id": prerequisite_id,
        "task_id": selected_unit["task_id"],
        "swu_id": selected_unit["swu_id"],
        "attempt_id": selected_unit["attempt_id"],
        "classification": classification,
        "prerequisite_fingerprint": fingerprint,
        "inputs_read": inputs_read,
        "authorization": {"status": authorization_status, "evidence_ref": authorization_ref},
        "permitted_next_action": permitted_next_action,
        "phase_trace": phase_trace(),
        "reasons": reasons,
    }
    errors = list(RECEIPT_VALIDATOR.iter_errors(receipt))
    if errors:
        raise ValueError("classifier produced invalid receipt: " + "; ".join(error.message for error in errors))
    return receipt


def classify(payload: dict[str, Any]) -> dict[str, Any]:
    work_pack = payload["work_pack"]
    selected_unit = payload["selected_unit"]
    prerequisite = payload.get("prerequisite")
    satisfaction_receipt = payload.get("satisfaction_receipt")
    authorization = payload.get("authorization")
    consumed = set(payload.get("consumed_attempt_fingerprints", []))

    common_reasons: list[str] = []
    identity_current = (
        work_pack.get("work_pack_id") == selected_unit.get("work_pack_id")
        and bool(work_pack.get("current"))
        and bool(selected_unit.get("entry_contract_current"))
    )

    if prerequisite is None:
        fingerprint = canonical_digest({
            "work_pack_id": selected_unit["work_pack_id"],
            "task_id": selected_unit["task_id"],
            "swu_id": selected_unit["swu_id"],
            "attempt_id": selected_unit["attempt_id"],
            "entry_contract_current": selected_unit.get("entry_contract_current"),
            "plan_once_selection_ready": selected_unit.get("plan_once_selection_ready", False),
        })
        if not identity_current:
            classification, entry_state, action = "stale", "blocked", "block"
            common_reasons.append("work-pack or selected-unit identity is stale")
        elif selected_unit.get("plan_once_selection_ready"):
            classification, entry_state, action = "satisfied", "plan-once-selection-ready", "continue-context-build"
        else:
            classification, entry_state, action = "satisfied", "context-ready", "continue-context-build"
        receipt = build_receipt(
            selected_unit=selected_unit,
            prerequisite_id="none",
            classification=classification,
            fingerprint=fingerprint,
            inputs_read=["work-pack", "selected-unit"],
            authorization_status="not-required" if classification == "satisfied" else "missing",
            authorization_ref=None,
            permitted_next_action=action,
            reasons=common_reasons,
        )
        return {"execution_entry_state": entry_state, "owner_route": None, "control_inputs": [], "classification_receipt": receipt}

    inputs_read = ["work-pack", "selected-unit", "prerequisite"]
    schema_errors = list(PREREQUISITE_VALIDATOR.iter_errors(prerequisite))
    if schema_errors:
        fingerprint = canonical_digest(prerequisite)
        receipt = build_receipt(
            selected_unit=selected_unit,
            prerequisite_id=str(prerequisite.get("prerequisite_id", "invalid")),
            classification="invalid",
            fingerprint=fingerprint,
            inputs_read=inputs_read,
            authorization_status="missing",
            authorization_ref=None,
            permitted_next_action="block",
            reasons=["prerequisite schema validation failed"],
        )
        return {"execution_entry_state": "blocked", "owner_route": None, "control_inputs": [], "classification_receipt": receipt}

    fingerprint = prerequisite_fingerprint(prerequisite)
    route = prerequisite["owner_route"]
    identity_matches = (
        identity_current
        and prerequisite["task_id"] == selected_unit["task_id"]
        and prerequisite["swu_id"] == selected_unit["swu_id"]
        and prerequisite["attempt_id"] == selected_unit["attempt_id"]
    )
    scope_matches = (
        prerequisite["target_inventory"] == selected_unit.get("target_inventory")
        and prerequisite["validation_contracts"] == selected_unit.get("validation_contracts")
    )
    repeated = f"{prerequisite['attempt_id']}:{fingerprint}" in consumed
    ambiguous = len(prerequisite["trigger"]["source_selectors"]) != 1

    if repeated:
        classification, entry_state, action = "invalid", "blocked", "block"
        common_reasons.append("attempt and prerequisite fingerprint were already consumed")
    elif ambiguous:
        classification, entry_state, action = "ambiguous", "blocked", "block"
        common_reasons.append("prerequisite source selector is not unique")
    elif not identity_matches or not scope_matches:
        classification, entry_state, action = "stale", "blocked", "block"
        common_reasons.append("prerequisite identity, target inventory, or validation contract is stale")
    elif satisfaction_receipt is not None:
        inputs_read.append("satisfaction-receipt")
        expected = prerequisite["expected_owner_receipt"]
        receipt_identity_matches = (
            satisfaction_receipt.get("schema_id") == expected["schema_id"]
            and satisfaction_receipt.get("owner_capability") == expected["owner_capability"]
            and satisfaction_receipt.get("task_id") == selected_unit["task_id"]
            and satisfaction_receipt.get("swu_id") == selected_unit["swu_id"]
            and satisfaction_receipt.get("attempt_id") == selected_unit["attempt_id"]
            and satisfaction_receipt.get("prerequisite_fingerprint") == fingerprint
        )
        try:
            observed = json_pointer(satisfaction_receipt, prerequisite["satisfaction_predicate"]["receipt_pointer"])
        except (KeyError, IndexError, TypeError, ValueError):
            observed = object()
        if receipt_identity_matches and observed in prerequisite["satisfaction_predicate"]["accepted_values"]:
            classification, entry_state, action = "satisfied", "context-ready", "continue-context-build"
        else:
            classification, entry_state, action = "stale", "blocked", "block"
            common_reasons.append("owner receipt identity or satisfaction predicate did not match")
    else:
        classification, entry_state = "unmet", "owner-prerequisite"
        authorization_matches = (
            authorization is not None
            and authorization.get("owner_route") == route
            and authorization.get("task_id") == selected_unit["task_id"]
            and authorization.get("swu_id") == selected_unit["swu_id"]
            and authorization.get("attempt_id") == selected_unit["attempt_id"]
            and authorization.get("target_inventory") == prerequisite["target_inventory"]
            and authorization.get("validation_contracts") == prerequisite["validation_contracts"]
            and authorization.get("allowed_effect") == prerequisite["allowed_effect"]
            and authorization.get("evidence_ref") is not None
        )
        control_inputs = ["authorization-evidence"] if authorization is not None else []
        if authorization_matches:
            action = "route-one-owner-hop"
        elif authorization is not None:
            action = "block"
            common_reasons.append("supplied prerequisite authorization does not match the exact route and scope")
        else:
            action = "block-missing-authorization"
            common_reasons.append("exact prerequisite authorization is absent")

    if classification != "unmet":
        control_inputs = []

    if classification == "satisfied":
        authorization_status, authorization_ref = "not-required", None
    elif classification == "unmet" and action == "route-one-owner-hop":
        authorization_status, authorization_ref = "matched", authorization["evidence_ref"]
    elif classification == "unmet" and authorization is None:
        authorization_status, authorization_ref = "missing", None
    elif classification == "unmet":
        authorization_status = "mismatch"
        authorization_ref = authorization.get("evidence_ref") if authorization else None
    else:
        authorization_status, authorization_ref = "mismatch", authorization.get("evidence_ref") if authorization else None

    receipt = build_receipt(
        selected_unit=selected_unit,
        prerequisite_id=prerequisite["prerequisite_id"],
        classification=classification,
        fingerprint=fingerprint,
        inputs_read=inputs_read,
        authorization_status=authorization_status,
        authorization_ref=authorization_ref,
        permitted_next_action=action,
        reasons=common_reasons,
    )
    return {
        "execution_entry_state": entry_state,
        "owner_route": route if classification == "unmet" else None,
        "control_inputs": control_inputs,
        "classification_receipt": receipt,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = classify(json.loads(args.input.read_text(encoding="utf-8")))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
