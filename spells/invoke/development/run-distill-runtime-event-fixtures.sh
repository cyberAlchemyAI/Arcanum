#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema="$script_dir/../schemas/distill-runtime-event.schema.json"
fixtures="$script_dir/fixtures/distill-evidence"

python3 - "$script_dir" "$schema" "$fixtures" <<'PY'
import copy
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
from distill_runtime_events import (  # noqa: E402
    EventContractError,
    append_event,
    ledger_sha256,
    load_jsonl,
    load_schema,
    resolve_events,
    validate_event,
)

schema = load_schema(pathlib.Path(sys.argv[2]))
fixtures = pathlib.Path(sys.argv[3])
failures = []
checks = 0


def expect_pass(label, operation):
    global checks
    checks += 1
    try:
        value = operation()
    except Exception as error:
        failures.append(f"{label}: {error}")
        print(f"FAIL {label}: {error}")
        return None
    print(f"PASS {label}")
    return value


def expect_block(label, expected, operation):
    global checks
    checks += 1
    try:
        operation()
    except EventContractError as error:
        if expected in str(error):
            print(f"PASS {label}: blocked ({expected})")
            return
        failures.append(f"{label}: expected {expected}; got {error}")
        print(f"FAIL {label}: wrong diagnostic: {error}")
        return
    failures.append(f"{label}: unexpectedly passed")
    print(f"FAIL {label}: unexpectedly passed")


true_events = load_jsonl(fixtures / "valid-runtime-events-true-subagents.jsonl")
simulation_events = load_jsonl(fixtures / "valid-runtime-events-role-simulation.jsonl")
true_result = expect_pass("true-subagent sequence resolves", lambda: resolve_events(true_events, schema))
simulation_result = expect_pass("role-simulation sequence resolves", lambda: resolve_events(simulation_events, schema))

if true_result and simulation_result:
    true_shape = [(entry["role"], len(entry["event_ids"])) for entry in true_result["role_trace"]]
    simulation_shape = [(entry["role"], len(entry["event_ids"])) for entry in simulation_result["role_trace"]]
    expect_pass(
        "execution paths preserve one role-boundary shape",
        lambda: true_shape == simulation_shape or (_ for _ in ()).throw(EventContractError("role shapes differ")),
    )
    expect_pass(
        "resolver disclaims verdict and mutation authority",
        lambda: (
            true_result["authority"] == "runtime_evidence_only"
            and true_result["verdict_authority"] is False
            and "mutation_handoff_allowed" not in true_result
        )
        or (_ for _ in ()).throw(EventContractError("resolver returned forbidden authority")),
    )

invalid_cases = [
    ("same invocation IDs", "invalid-runtime-events-same-invocation.jsonl", "distinct invocation references"),
    ("missing role boundary", "invalid-runtime-events-missing-boundary.jsonl", "unexpected event boundary sequence"),
    ("invalid role ordering", "invalid-runtime-events-out-of-order.jsonl", "unexpected event boundary sequence"),
    ("simulated native IDs", "invalid-runtime-events-simulated-native-id.jsonl", "invocation_ref"),
]
for label, fixture, diagnostic in invalid_cases:
    expect_block(label, diagnostic, lambda fixture=fixture: resolve_events(load_jsonl(fixtures / fixture), schema))

for required_field in ("event_id", "sequence", "execution_path", "role", "payload_ref", "emitted_at"):
    malformed = copy.deepcopy(true_events[0])
    del malformed[required_field]
    expect_block(
        f"schema omission {required_field}",
        f"'{required_field}' is a required property",
        lambda malformed=malformed: validate_event(malformed, schema),
    )

with tempfile.TemporaryDirectory() as temporary_directory:
    ledger = pathlib.Path(temporary_directory) / "events.jsonl"
    digest = ledger_sha256(b"")
    digest = expect_pass("append first event", lambda: append_event(ledger, true_events[0], schema, digest))

    duplicate = copy.deepcopy(true_events[1])
    duplicate["event_id"] = true_events[0]["event_id"]
    expect_block("append duplicate event ID", "event IDs must be unique", lambda: append_event(ledger, duplicate, schema, digest))

    sequence_gap = copy.deepcopy(true_events[1])
    sequence_gap["sequence"] = 2
    expect_block("append non-monotonic sequence", "next sequence must be 1", lambda: append_event(ledger, sequence_gap, schema, digest))

    changed_run = copy.deepcopy(true_events[1])
    changed_run["run_id"] = "different-run"
    expect_block("append changed run", "preserve the run ID", lambda: append_event(ledger, changed_run, schema, digest))

    changed_path = copy.deepcopy(true_events[1])
    changed_path["execution_path"] = "role_simulation"
    changed_path["invocation_ref"] = None
    expect_block("append changed execution path", "preserve the execution path", lambda: append_event(ledger, changed_path, schema, digest))

    ledger.write_bytes(ledger.read_bytes() + b"\n")
    expect_block(
        "append after ledger rewrite",
        "ledger bytes changed",
        lambda: append_event(ledger, true_events[1], schema, digest),
    )

with tempfile.TemporaryDirectory() as temporary_directory:
    round_trip_ledger = pathlib.Path(temporary_directory) / "round-trip.jsonl"

    def append_and_resolve_round_trip():
        digest = ledger_sha256(b"")
        for event in true_events:
            digest = append_event(round_trip_ledger, event, schema, digest)
        result = resolve_events(load_jsonl(round_trip_ledger), schema)
        if result["event_count"] != len(true_events):
            raise EventContractError("round-trip event count differs")
        return result

    expect_pass("append and resolve complete ledger", append_and_resolve_round_trip)

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} of {checks} checks failed)")
    raise SystemExit(1)

print(f"SUMMARY: PASS ({checks} of {checks} checks satisfied expectations)")
print("AUTHORITY: runtime evidence only; no verdict or mutation readiness is established")
PY
