#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "arcanum.native-dispatch-runner.evidence-validation.v0.1"
VALIDATOR_NAME = "validate_run_evidence.py"
HOST_RESULTS = {"host_spawn_returned", "host_spawn_failed"}
EVENT_KINDS = {
    "action_attempted",
    "host_spawn_returned",
    "host_spawn_failed",
    "agent_terminal",
    "receipt_joined",
    "gate_decided",
}
BASE_FIELDS = {"schema_version", "sequence", "event", "dispatch_id", "run_id", "wave_id", "action_id", "agent_id", "operation"}


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        value = json.loads(raw_line)
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number}: event must be a JSON object")
        events.append(value)
    return events


def event_shape_violation(event: dict[str, Any]) -> str | None:
    missing = sorted(BASE_FIELDS - set(event))
    if missing:
        return "missing required fields: " + ", ".join(missing)
    if event.get("schema_version") != "arcanum.native-dispatch-runner.run-event.v0.1":
        return "unsupported schema_version"
    if event.get("event") not in EVENT_KINDS:
        return "unsupported event kind"
    if not isinstance(event.get("sequence"), int) or isinstance(event.get("sequence"), bool) or event["sequence"] < 1:
        return "sequence must be a positive integer"
    for field in ("dispatch_id", "run_id", "wave_id", "operation"):
        if not isinstance(event.get(field), str) or not event[field]:
            return f"{field} must be a non-empty string"
    kind = event["event"]
    if kind == "gate_decided":
        if event.get("action_id") is not None or event.get("agent_id") is not None:
            return "gate_decided action_id and agent_id must be null"
        if not isinstance(event.get("gate_id"), str) or not event["gate_id"]:
            return "gate_decided requires gate_id"
        if event.get("decision") not in {"gate_pass", "gate_block"}:
            return "gate_decided requires a supported decision"
        for field in ("required_action_ids", "admitted_receipt_action_ids"):
            value = event.get(field)
            if not isinstance(value, list) or (field == "required_action_ids" and not value) or any(not isinstance(item, str) or not item for item in value):
                return f"gate_decided requires valid {field}"
        return None
    if not isinstance(event.get("action_id"), str) or not event["action_id"]:
        return f"{kind} requires action_id"
    if kind == "action_attempted":
        if event.get("agent_id") is not None or "depends_on_gate_id" not in event:
            return "action_attempted requires null agent_id and depends_on_gate_id"
    elif kind == "host_spawn_failed":
        if event.get("agent_id") is not None:
            return "host_spawn_failed requires null agent_id"
    elif not isinstance(event.get("agent_id"), str) or not event["agent_id"]:
        return f"{kind} requires agent_id"
    if kind == "receipt_joined" and event.get("receipt_status") not in {"pass", "block", "fail", "timed_out"}:
        return "receipt_joined requires a supported receipt_status"
    return None


def validate_events(events: list[dict[str, Any]], source: str) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    attempts: dict[str, dict[str, Any]] = {}
    host_results: dict[str, dict[str, Any]] = {}
    joined: dict[str, dict[str, Any]] = {}
    gate_passes: dict[str, int] = {}
    dispatch_id: str | None = None
    run_id: str | None = None

    def reject(code: str, event: dict[str, Any] | None, message: str, action_id: str | None = None) -> None:
        errors.append(
            {
                "code": code,
                "sequence": event.get("sequence") if event else None,
                "action_id": action_id if action_id is not None else (event.get("action_id") if event else None),
                "message": message,
            }
        )

    for expected_sequence, event in enumerate(events, start=1):
        if event.get("sequence") != expected_sequence:
            reject("sequence_mismatch", event, f"expected sequence {expected_sequence}")

        shape_violation = event_shape_violation(event)
        if shape_violation:
            reject("event_schema_violation", event, shape_violation)
            continue

        if dispatch_id is None:
            dispatch_id = event.get("dispatch_id")
            run_id = event.get("run_id")
        elif event.get("dispatch_id") != dispatch_id or event.get("run_id") != run_id:
            reject("run_identity_mismatch", event, "event dispatch_id/run_id differs from the first event")

        kind = event.get("event")
        action_id = event.get("action_id")

        if kind == "action_attempted":
            if not isinstance(action_id, str) or not action_id:
                reject("invalid_action_identity", event, "action attempt requires a non-empty action_id")
                continue
            if action_id in attempts:
                reject("duplicate_action_attempt", event, "action was attempted more than once")
            else:
                attempts[action_id] = event
            dependency = event.get("depends_on_gate_id")
            if dependency is not None and dependency not in gate_passes:
                reject("dependent_action_before_gate", event, f"gate {dependency} has no earlier valid gate_pass")

        elif kind in HOST_RESULTS:
            if action_id not in attempts:
                reject("missing_action_attempt", event, "host result has no earlier action_attempted event")
            if action_id in host_results:
                reject("duplicate_host_result", event, "action has more than one host result")
            else:
                host_results[action_id] = event

        elif kind == "agent_terminal":
            host_result = host_results.get(action_id)
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject("terminal_without_host_result", event, "terminal agent has no earlier successful host result")
            elif event.get("agent_id") != host_result.get("agent_id"):
                reject("terminal_agent_mismatch", event, "terminal agent_id differs from the host result")

        elif kind == "receipt_joined":
            host_result = host_results.get(action_id)
            if host_result is None or host_result.get("event") != "host_spawn_returned":
                reject("join_without_host_result", event, "joined receipt has no earlier successful host result")
            elif event.get("agent_id") != host_result.get("agent_id"):
                reject("joined_agent_mismatch", event, "joined receipt agent_id differs from the host result")
            if action_id in joined:
                reject("duplicate_joined_receipt", event, "action has more than one joined receipt")
            else:
                joined[action_id] = event

        elif kind == "gate_decided":
            gate_error_count = len(errors)
            gate_id = event.get("gate_id")
            required = event.get("required_action_ids", [])
            admitted = event.get("admitted_receipt_action_ids", [])
            if gate_id in gate_passes:
                reject("duplicate_gate_decision", event, f"gate {gate_id} was already decided")
            for required_action_id in required:
                if required_action_id not in attempts:
                    reject("gate_missing_attempt", event, "required action has no earlier attempt", required_action_id)
                if required_action_id not in host_results:
                    reject("gate_missing_host_result", event, "required action has no earlier host result", required_action_id)
                if required_action_id not in joined:
                    reject("gate_missing_joined_receipt", event, "required action has no earlier joined receipt", required_action_id)
            if event.get("decision") == "gate_pass":
                if set(admitted) != set(required):
                    reject("gate_receipt_set_mismatch", event, "gate_pass must admit exactly its required action receipts")
                for required_action_id in required:
                    receipt = joined.get(required_action_id)
                    if receipt is not None and receipt.get("receipt_status") != "pass":
                        reject("gate_admitted_non_pass", event, "gate_pass admitted a non-pass receipt", required_action_id)
                if len(errors) == gate_error_count and isinstance(gate_id, str):
                    gate_passes[gate_id] = event.get("sequence")

    for action_id, attempt in attempts.items():
        host_result = host_results.get(action_id)
        if host_result is None:
            reject("missing_host_result", attempt, "attempted action has no host result", action_id)
        elif host_result.get("event") == "host_spawn_returned" and action_id not in joined:
            reject("missing_joined_receipt", host_result, "successful host result has no joined receipt", action_id)

    valid = not errors
    return {
        "schema_version": SCHEMA_VERSION,
        "validator": VALIDATOR_NAME,
        "source": source,
        "event_count": len(events),
        "valid": valid,
        "status": "pass" if valid else "block",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate causal ordering in a native dispatch JSONL event stream.")
    parser.add_argument("events", type=Path, help="Path to events.jsonl")
    parser.add_argument("--output", type=Path, required=True, help="Path for the validation receipt")
    args = parser.parse_args()

    try:
        receipt = validate_events(load_events(args.events), str(args.events))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        receipt = {
            "schema_version": SCHEMA_VERSION,
            "validator": VALIDATOR_NAME,
            "source": str(args.events),
            "event_count": 0,
            "valid": False,
            "status": "block",
            "errors": [{"code": "unreadable_event_stream", "sequence": None, "action_id": None, "message": str(exc)}],
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"valid": receipt["valid"], "status": receipt["status"], "receipt": str(args.output)}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
