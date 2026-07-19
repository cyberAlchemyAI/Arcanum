#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


class EventContractError(ValueError):
    pass


EXPECTED_BOUNDARIES = [
    ("capability_probe", None),
    ("role_start", "proposer"),
    ("role_result", "proposer"),
    ("role_start", "balancer"),
    ("role_result", "balancer"),
    ("reconciliation", None),
    ("termination", None),
]


def load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise EventContractError(f"blank JSONL line at {line_number}")
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise EventContractError(f"invalid JSON at line {line_number}: {error.msg}") from error
    return events


def _validator(schema: dict[str, Any]) -> Draft202012Validator:
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_event(event: dict[str, Any], schema: dict[str, Any]) -> None:
    errors = sorted(_validator(schema).iter_errors(event), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "event"
        raise EventContractError(f"schema error at {location}: {error.message}")


def resolve_events(events: list[dict[str, Any]], schema: dict[str, Any]) -> dict[str, Any]:
    if not events:
        raise EventContractError("event sequence is empty")

    for event in events:
        validate_event(event, schema)

    event_ids = [event["event_id"] for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise EventContractError("event IDs must be unique")

    sequences = [event["sequence"] for event in events]
    if sequences != list(range(len(events))):
        raise EventContractError("sequence numbers must be contiguous, zero-based, and append ordered")

    run_ids = {event["run_id"] for event in events}
    if len(run_ids) != 1:
        raise EventContractError("all events must share one run ID")

    execution_paths = {event["execution_path"] for event in events}
    if len(execution_paths) != 1:
        raise EventContractError("all events must share one execution path")

    timestamps = [event["emitted_at"] for event in events]
    if timestamps != sorted(timestamps):
        raise EventContractError("emission timestamps must be monotonic")

    boundaries = [(event["event_type"], event["role"]) for event in events]
    if boundaries != EXPECTED_BOUNDARIES:
        raise EventContractError(f"unexpected event boundary sequence: {boundaries}")

    execution_path = events[0]["execution_path"]
    role_refs: dict[str, set[str]] = {"proposer": set(), "balancer": set()}
    for event in events:
        if event["role"] in role_refs and event["invocation_ref"] is not None:
            role_refs[event["role"]].add(event["invocation_ref"])

    if execution_path == "true_subagent":
        if any(len(refs) != 1 for refs in role_refs.values()):
            raise EventContractError("each true-subagent role must use one stable invocation reference")
        proposer_ref = next(iter(role_refs["proposer"]))
        balancer_ref = next(iter(role_refs["balancer"]))
        if proposer_ref == balancer_ref:
            raise EventContractError("true-subagent roles require distinct invocation references")
    elif any(event["invocation_ref"] is not None for event in events):
        raise EventContractError("role simulation must not claim native invocation references")

    role_trace = []
    for role in ("proposer", "balancer"):
        role_events = [event for event in events if event["role"] == role]
        role_trace.append(
            {
                "role": role,
                "invocation_ref": role_events[0]["invocation_ref"],
                "event_ids": [event["event_id"] for event in role_events],
                "payload_refs": [event["payload_ref"] for event in role_events],
            }
        )

    return {
        "resolution": "resolved",
        "authority": "runtime_evidence_only",
        "verdict_authority": False,
        "run_id": events[0]["run_id"],
        "execution_path": execution_path,
        "event_count": len(events),
        "role_trace": role_trace,
        "reconciliation_event_id": events[-2]["event_id"],
        "termination_event_id": events[-1]["event_id"],
    }


def ledger_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def append_event(
    ledger_path: Path,
    event: dict[str, Any],
    schema: dict[str, Any],
    expected_ledger_sha256: str,
) -> str:
    existing = ledger_path.read_bytes() if ledger_path.exists() else b""
    if ledger_sha256(existing) != expected_ledger_sha256:
        raise EventContractError("ledger bytes changed since the caller observed them")
    if existing and not existing.endswith(b"\n"):
        raise EventContractError("existing ledger must end with a newline")

    validate_event(event, schema)
    existing_events = load_jsonl(ledger_path) if existing else []
    if any(previous["event_id"] == event["event_id"] for previous in existing_events):
        raise EventContractError("event IDs must be unique")

    expected_sequence = len(existing_events)
    if event["sequence"] != expected_sequence:
        raise EventContractError(f"next sequence must be {expected_sequence}")
    if existing_events and event["run_id"] != existing_events[0]["run_id"]:
        raise EventContractError("appended event must preserve the run ID")
    if existing_events and event["execution_path"] != existing_events[0]["execution_path"]:
        raise EventContractError("appended event must preserve the execution path")

    encoded = json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("ab") as ledger:
        ledger.write(encoded)
        ledger.flush()
        os.fsync(ledger.fileno())
    return ledger_sha256(existing + encoded)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append or resolve Invoke-side Distill runtime events")
    parser.add_argument("--schema", required=True, type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("ledger", type=Path)

    append_parser = subparsers.add_parser("append")
    append_parser.add_argument("ledger", type=Path)
    append_parser.add_argument("event", type=Path)
    append_parser.add_argument("--expected-ledger-sha256", required=True)

    args = parser.parse_args()
    schema = load_schema(args.schema)
    try:
        if args.command == "resolve":
            result = resolve_events(load_jsonl(args.ledger), schema)
        else:
            event = json.loads(args.event.read_text(encoding="utf-8"))
            result = {
                "ledger_sha256": append_event(
                    args.ledger,
                    event,
                    schema,
                    args.expected_ledger_sha256,
                ),
                "authority": "runtime_evidence_only",
            }
    except EventContractError as error:
        print(json.dumps({"resolution": "block", "diagnostic": str(error)}, sort_keys=True))
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
