#!/usr/bin/env python3
"""Evaluate one Task Session governance request against an exact policy."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SCHEMA_VERSION = "task-session.governance-evaluation-receipt.v1"
ALLOWED_OUTCOMES = {
    "series-intent": {
        "ROUTE_TASK_SESSION_UNTIL_BLOCKER",
        "CONTINUE_SINGLE_TASK_SESSION",
    },
    "automatic-choice": {"PROCEED", "BLOCK"},
    "closeout-preflight": {"PROCEED", "BLOCK"},
    "validation": {"PASS", "FLAG", "BLOCK"},
    "closeout-sync": {"PASS", "NO_OP", "BLOCK"},
}


class EvaluationError(ValueError):
    """Raised when an evaluation must fail closed."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EvaluationError(f"cannot load JSON {path}: {error}") from error
    if not isinstance(document, dict):
        raise EvaluationError(f"JSON document must be an object: {path}")
    return document


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_ref(path: Path, display_path: str) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": display_path,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return sha256_bytes(encoded)


def validate_schema(
    document: dict[str, Any], schema: dict[str, Any], label: str
) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        messages = [
            f"{label} invalid at "
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: "
            f"{error.message}"
            for error in errors
        ]
        raise EvaluationError("; ".join(messages))


def evaluate_automatic_choice(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    required = policy["automatic_choice"]["required_classification"]
    admitted = all(fixture_input.get(key) == value for key, value in required.items())
    outcome_key = "admitted_outcome" if admitted else "rejected_outcome"
    return str(policy["automatic_choice"][outcome_key])


def evaluate_series_intent(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    series = policy["series_intent"]
    request = str(fixture_input.get("request", "")).casefold()
    detected = any(term.casefold() in request for term in series["explicit_terms"])
    outcome_key = "detected_outcome" if detected else "not_detected_outcome"
    return str(series[outcome_key])


def evaluate_closeout_preflight(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    preflight = policy["closeout_preflight"]
    if fixture_input.get("sync_expected") is False:
        return str(preflight["no_sync_outcome"])

    for field in preflight["required_inputs"]:
        value = fixture_input.get(field)
        if value is None or value == "" or value == [] or value == {}:
            return str(preflight["rejected_outcome"])

    delta_classes = fixture_input.get("allowed_delta_classes")
    if not isinstance(delta_classes, list) or not delta_classes:
        return str(preflight["rejected_outcome"])
    if any(item not in preflight["admitted_delta_classes"] for item in delta_classes):
        return str(preflight["rejected_outcome"])

    successor = fixture_input.get("successor_selection", {})
    if successor.get("requested") is True and preflight[
        "unique_declared_successor_only"
    ]:
        if not (
            successor.get("declared") is True
            and successor.get("dependency_ready") is True
            and successor.get("candidate_count") == 1
        ):
            return str(preflight["rejected_outcome"])

    return str(preflight["admitted_outcome"])


def accepted_equivalent_passes(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> bool:
    equivalent = fixture_input.get("accepted_equivalent")
    if not isinstance(equivalent, dict):
        return False
    equivalent_policy = policy["validation"]["accepted_equivalent"]
    if equivalent_policy["must_be_named_and_accepted"] and not (
        equivalent.get("named") is True and equivalent.get("accepted") is True
    ):
        return False
    if equivalent_policy["must_pass"]:
        return equivalent.get("result") == policy["validation"]["passing_result"]
    return True


def evaluate_validation(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    validation = policy["validation"]
    result = fixture_input.get("result")
    if result == validation["passing_result"] or accepted_equivalent_passes(
        policy, fixture_input
    ):
        return "PASS"

    criticality = fixture_input.get(
        "criticality", validation["default_criticality"]
    )
    if criticality not in validation["criticality_values"]:
        return "BLOCK"
    if criticality == "acceptance-critical":
        return str(validation["acceptance_critical_unmet_outcome"])

    residue = fixture_input.get("residue")
    residue_policy = validation["noncritical_residue"]
    admitted = isinstance(residue, dict)
    if admitted and residue_policy["must_be_named"]:
        admitted = residue.get("named") is True
    if admitted and residue_policy["must_not_falsify_done_criterion"]:
        admitted = residue.get("can_falsify_done_criterion") is False
    outcome_key = "admitted_outcome" if admitted else "rejected_outcome"
    return str(residue_policy[outcome_key])


def evaluate_closeout_sync(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    closeout = policy["closeout_sync"]
    if fixture_input.get("sync_required") is False:
        return str(closeout["no_op_outcome"])

    if fixture_input.get("route_tuple") != closeout["route_tuple"]:
        return str(closeout["rejected_outcome"])
    for field in closeout["required_inputs"]:
        value = fixture_input.get(field)
        if value is None or value == "" or value == []:
            return str(closeout["rejected_outcome"])

    delta_classes = fixture_input.get("delta_classes")
    if not isinstance(delta_classes, list) or not delta_classes:
        return str(closeout["rejected_outcome"])
    if any(item not in closeout["allowed_delta_classes"] for item in delta_classes):
        return str(closeout["rejected_outcome"])

    scopes = fixture_input.get("scopes", [])
    if not isinstance(scopes, list):
        return str(closeout["rejected_outcome"])
    if any(item in closeout["forbidden_scopes"] for item in scopes):
        return str(closeout["rejected_outcome"])

    successor = fixture_input.get("successor_selection", {})
    if successor.get("requested") is True and closeout[
        "unique_declared_successor_only"
    ]:
        if not (
            successor.get("declared") is True
            and successor.get("dependency_ready") is True
            and successor.get("candidate_count") == 1
        ):
            return str(closeout["rejected_outcome"])

    owner_receipt = fixture_input.get("owner_receipt")
    if not isinstance(owner_receipt, dict) or owner_receipt.get("joined") is not True:
        return str(closeout["rejected_outcome"])
    if owner_receipt.get("result") not in closeout["passing_owner_results"]:
        return str(closeout["rejected_outcome"])
    return str(closeout["admitted_outcome"])


EVALUATORS = {
    "series-intent": evaluate_series_intent,
    "automatic-choice": evaluate_automatic_choice,
    "closeout-preflight": evaluate_closeout_preflight,
    "validation": evaluate_validation,
    "closeout-sync": evaluate_closeout_sync,
}


def evaluate(
    request: dict[str, Any],
    policy: dict[str, Any],
    policy_ref: dict[str, Any],
    evaluator_path: Path,
) -> dict[str, Any]:
    kind = request["evaluation_kind"]
    if kind not in EVALUATORS:
        raise EvaluationError(f"unknown evaluation kind: {kind}")
    try:
        outcome = EVALUATORS[kind](policy, request["input"])
    except (KeyError, TypeError) as error:
        raise EvaluationError(f"policy cannot evaluate {kind}: {error}") from error
    allowed = ALLOWED_OUTCOMES[kind]
    if outcome not in allowed:
        raise EvaluationError(
            f"policy emitted invalid outcome for {kind}: {outcome}"
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "request_id": request["request_id"],
        "evaluation_kind": kind,
        "policy_ref": policy_ref,
        "input_sha256": canonical_json_sha256(request["input"]),
        "outcome": outcome,
        "allowed_outcomes": sorted(allowed),
        "evaluator_sha256": sha256_bytes(evaluator_path.read_bytes()),
        "diagnostics": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--request-schema", required=True)
    parser.add_argument("--receipt-schema", required=True)
    args = parser.parse_args()

    request_path = Path(args.request)
    policy_path = Path(args.policy)
    request_schema_path = Path(args.request_schema)
    receipt_schema_path = Path(args.receipt_schema)
    try:
        request = load_json(request_path)
        policy = load_json(policy_path)
        request_schema = load_json(request_schema_path)
        receipt_schema = load_json(receipt_schema_path)
        validate_schema(request, request_schema, "request")

        expected_policy_ref = exact_ref(policy_path, args.policy)
        if request["policy_ref"] != expected_policy_ref:
            raise EvaluationError("request policy_ref does not match the supplied policy")

        output_path = Path(request["output_path"])
        protected_inputs = {
            path.resolve()
            for path in (
                request_path,
                policy_path,
                request_schema_path,
                receipt_schema_path,
                Path(__file__),
            )
        }
        if output_path.resolve() in protected_inputs:
            raise EvaluationError("output_path may not overwrite an evaluator input")
        if not output_path.parent.is_dir():
            raise EvaluationError("output_path parent must already exist")

        receipt = evaluate(
            request,
            policy,
            expected_policy_ref,
            Path(__file__).resolve(),
        )
        validate_schema(receipt, receipt_schema, "receipt")
        output_path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (EvaluationError, OSError) as error:
        print(f"BLOCK {error}", file=sys.stderr)
        return 1
    print(f"PASS request_id={request['request_id']} outcome={receipt['outcome']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
