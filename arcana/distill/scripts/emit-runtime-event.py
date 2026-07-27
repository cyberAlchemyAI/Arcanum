#!/usr/bin/env python3
"""Append one non-authoritative Distill runtime evidence event."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


class EmissionError(ValueError):
    """A fail-closed producer-side event emission error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_schema(path: Path) -> dict[str, Any]:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EmissionError(f"cannot load event schema: {error}") from error
    Draft202012Validator.check_schema(schema)
    return schema


def load_event(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EmissionError(f"cannot load event: {error}") from error
    if not isinstance(value, dict):
        raise EmissionError("event must be a JSON object")
    return value


def validate_event(event: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(event), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "event"
        raise EmissionError(f"schema error at {location}: {error.message}")


def load_ledger(data: bytes) -> list[dict[str, Any]]:
    if not data:
        return []
    if not data.endswith(b"\n"):
        raise EmissionError("existing ledger must end with a newline")

    events: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(data.splitlines(), start=1):
        if not raw_line:
            raise EmissionError(f"blank JSONL line at {line_number}")
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as error:
            raise EmissionError(
                f"invalid ledger JSON at line {line_number}: {error.msg}"
            ) from error
        if not isinstance(value, dict):
            raise EmissionError(f"ledger event at line {line_number} is not an object")
        events.append(value)
    return events


def append_event(
    *,
    schema_path: Path,
    ledger_path: Path,
    event_path: Path,
    expected_ledger_sha256: str,
) -> dict[str, Any]:
    schema = load_schema(schema_path)
    event = load_event(event_path)
    validate_event(event, schema)

    existing = ledger_path.read_bytes() if ledger_path.exists() else b""
    actual_digest = sha256_bytes(existing)
    if actual_digest != expected_ledger_sha256:
        raise EmissionError("ledger bytes changed since the caller observed them")

    existing_events = load_ledger(existing)
    for previous in existing_events:
        validate_event(previous, schema)

    if any(previous["event_id"] == event["event_id"] for previous in existing_events):
        raise EmissionError("event IDs must be unique")

    expected_sequence = len(existing_events)
    if event["sequence"] != expected_sequence:
        raise EmissionError(f"next sequence must be {expected_sequence}")

    if existing_events:
        first = existing_events[0]
        if event["run_id"] != first["run_id"]:
            raise EmissionError("appended event must preserve the run ID")
        if event["execution_path"] != first["execution_path"]:
            raise EmissionError("appended event must preserve the execution path")
        if event["emitted_at"] < existing_events[-1]["emitted_at"]:
            raise EmissionError("emission timestamps must be monotonic")

    encoded = json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8")
    encoded += b"\n"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("ab") as ledger:
        ledger.write(encoded)
        ledger.flush()
        os.fsync(ledger.fileno())

    return {
        "authority": "runtime_evidence_only",
        "emission_status": "complete",
        "event_id": event["event_id"],
        "execution_path": event["execution_path"],
        "ledger_path": str(ledger_path),
        "ledger_sha256": sha256_bytes(existing + encoded),
        "run_id": event["run_id"],
        "sequence": event["sequence"],
        "verdict_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append one schema-validated Distill runtime evidence event"
    )
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--event", required=True, type=Path)
    parser.add_argument("--expected-ledger-sha256", required=True)
    args = parser.parse_args()

    try:
        result = append_event(
            schema_path=args.schema,
            ledger_path=args.ledger,
            event_path=args.event,
            expected_ledger_sha256=args.expected_ledger_sha256,
        )
    except (EmissionError, OSError, KeyError) as error:
        print(
            json.dumps(
                {
                    "authority": "runtime_evidence_only",
                    "diagnostic": str(error),
                    "emission_status": "failed",
                    "verdict_authority": False,
                },
                sort_keys=True,
            )
        )
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
