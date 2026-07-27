#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
arcanum_root="$(cd "$script_dir/../../.." && pwd)"

python3 - "$arcanum_root" <<'PY'
import copy
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

arcanum_root = pathlib.Path(sys.argv[1])
emitter = arcanum_root / "arcana/distill/scripts/emit-runtime-event.py"
schema_path = arcanum_root / "spells/invoke/schemas/distill-runtime-event.schema.json"
fixture_dir = arcanum_root / "spells/invoke/development/fixtures/distill-evidence"
sys.path.insert(0, str(arcanum_root / "spells/invoke/development"))

from distill_runtime_events import (  # noqa: E402
    EventContractError,
    load_jsonl,
    load_schema,
    resolve_events,
)

schema = load_schema(schema_path)
failures = []
checks = 0


def digest(data=b""):
    return hashlib.sha256(data).hexdigest()


def pass_check(label, condition=True):
    global checks
    checks += 1
    if condition:
        print(f"PASS {label}")
    else:
        failures.append(label)
        print(f"FAIL {label}")


def emit(event, ledger, expected_digest, temporary_directory):
    event_path = temporary_directory / f"{event.get('event_id', 'invalid')}.json"
    event_path.write_text(json.dumps(event), encoding="utf-8")
    process = subprocess.run(
        [
            sys.executable,
            str(emitter),
            "--schema",
            str(schema_path),
            "--ledger",
            str(ledger),
            "--event",
            str(event_path),
            "--expected-ledger-sha256",
            expected_digest,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(f"emitter returned invalid JSON: {process.stdout!r}") from error
    return process.returncode, result


def emit_sequence(events, ledger, temporary_directory):
    current_digest = digest()
    for event in events:
        returncode, result = emit(event, ledger, current_digest, temporary_directory)
        if returncode != 0:
            raise AssertionError(result)
        if result["authority"] != "runtime_evidence_only":
            raise AssertionError("emitter returned forbidden authority")
        if result["verdict_authority"] is not False:
            raise AssertionError("emitter claimed verdict authority")
        current_digest = result["ledger_sha256"]
    return current_digest


true_events = load_jsonl(fixture_dir / "valid-runtime-events-true-subagents.jsonl")
simulation_events = load_jsonl(fixture_dir / "valid-runtime-events-role-simulation.jsonl")

with tempfile.TemporaryDirectory(prefix="distill-emitter-") as raw_directory:
    temporary_directory = pathlib.Path(raw_directory)

    single_ledger = temporary_directory / "single.jsonl"
    returncode, result = emit(true_events[0], single_ledger, digest(), temporary_directory)
    pass_check(
        "DRE-001 one accepted capability-probe event appends",
        returncode == 0
        and result.get("emission_status") == "complete"
        and result.get("event_id") == true_events[0]["event_id"]
        and len(single_ledger.read_text(encoding="utf-8").splitlines()) == 1,
    )

    invalid = copy.deepcopy(true_events[0])
    invalid.pop("run_id")
    invalid_ledger = temporary_directory / "invalid.jsonl"
    returncode, result = emit(invalid, invalid_ledger, digest(), temporary_directory)
    pass_check(
        "DRE-001 schema-invalid event fails without a write",
        returncode == 1
        and result.get("emission_status") == "failed"
        and not invalid_ledger.exists(),
    )

    stale_ledger = temporary_directory / "stale.jsonl"
    returncode, result = emit(true_events[0], stale_ledger, "0" * 64, temporary_directory)
    pass_check(
        "DRE-001 stale ledger digest fails without a write",
        returncode == 1
        and "ledger bytes changed" in result.get("diagnostic", "")
        and not stale_ledger.exists(),
    )

    true_ledger = temporary_directory / "true.jsonl"
    emit_sequence(true_events, true_ledger, temporary_directory)
    true_resolution = resolve_events(load_jsonl(true_ledger), schema)
    pass_check(
        "DRE-002 producer-created true-subagent sequence resolves",
        true_resolution["execution_path"] == "true_subagent"
        and true_resolution["event_count"] == 7,
    )
    role_refs = {
        entry["role"]: entry["invocation_ref"]
        for entry in true_resolution["role_trace"]
    }
    pass_check(
        "DRE-002 true-subagent roles retain distinct stable invocation IDs",
        role_refs["proposer"]
        and role_refs["balancer"]
        and role_refs["proposer"] != role_refs["balancer"],
    )

    same_events = load_jsonl(fixture_dir / "invalid-runtime-events-same-invocation.jsonl")
    same_ledger = temporary_directory / "same.jsonl"
    emit_sequence(same_events, same_ledger, temporary_directory)
    try:
        resolve_events(load_jsonl(same_ledger), schema)
    except EventContractError as error:
        same_id_blocked = "distinct invocation references" in str(error)
    else:
        same_id_blocked = False
    pass_check("DRE-002 same true-subagent invocation ID blocks", same_id_blocked)

    sequence_ledger = temporary_directory / "sequence.jsonl"
    emit_sequence([true_events[0]], sequence_ledger, temporary_directory)
    sequence_gap = copy.deepcopy(true_events[1])
    sequence_gap["sequence"] = 2
    returncode, result = emit(
        sequence_gap, sequence_ledger, digest(sequence_ledger.read_bytes()), temporary_directory
    )
    pass_check(
        "DRE-002 non-contiguous producer sequence blocks",
        returncode == 1 and "next sequence must be 1" in result.get("diagnostic", ""),
    )

    changed_run = copy.deepcopy(true_events[1])
    changed_run["run_id"] = "changed-run"
    returncode, result = emit(
        changed_run, sequence_ledger, digest(sequence_ledger.read_bytes()), temporary_directory
    )
    pass_check(
        "DRE-002 changed run ID blocks",
        returncode == 1 and "preserve the run ID" in result.get("diagnostic", ""),
    )

    changed_path = copy.deepcopy(true_events[1])
    changed_path["execution_path"] = "role_simulation"
    changed_path["invocation_ref"] = None
    returncode, result = emit(
        changed_path, sequence_ledger, digest(sequence_ledger.read_bytes()), temporary_directory
    )
    pass_check(
        "DRE-002 changed execution path blocks",
        returncode == 1 and "preserve the execution path" in result.get("diagnostic", ""),
    )

    simulation_ledger = temporary_directory / "simulation.jsonl"
    emit_sequence(simulation_events, simulation_ledger, temporary_directory)
    simulation_resolution = resolve_events(load_jsonl(simulation_ledger), schema)
    pass_check(
        "DRE-003 producer-created role-simulation sequence resolves",
        simulation_resolution["execution_path"] == "role_simulation"
        and simulation_resolution["event_count"] == 7,
    )
    pass_check(
        "DRE-003 role simulation carries no native invocation IDs",
        all(
            entry["invocation_ref"] is None
            for entry in simulation_resolution["role_trace"]
        ),
    )

    native_events = load_jsonl(
        fixture_dir / "invalid-runtime-events-simulated-native-id.jsonl"
    )
    native_ledger = temporary_directory / "native.jsonl"
    current_digest = digest()
    native_id_blocked = False
    for event in native_events:
        returncode, result = emit(
            event, native_ledger, current_digest, temporary_directory
        )
        if returncode != 0:
            native_id_blocked = "invocation_ref" in result.get("diagnostic", "")
            break
        current_digest = result["ledger_sha256"]
    pass_check("DRE-003 simulated native invocation IDs block", native_id_blocked)

    missing_events = load_jsonl(
        fixture_dir / "invalid-runtime-events-missing-boundary.jsonl"
    )
    missing_ledger = temporary_directory / "missing.jsonl"
    emit_sequence(missing_events, missing_ledger, temporary_directory)
    try:
        resolve_events(load_jsonl(missing_ledger), schema)
    except EventContractError as error:
        missing_blocked = "unexpected event boundary sequence" in str(error)
    else:
        missing_blocked = False
    pass_check("DRE-003 missing role boundary blocks at resolution", missing_blocked)

    true_shape = [
        (entry["role"], len(entry["event_ids"]))
        for entry in true_resolution["role_trace"]
    ]
    simulation_shape = [
        (entry["role"], len(entry["event_ids"]))
        for entry in simulation_resolution["role_trace"]
    ]
    pass_check(
        "DRE-003 both paths preserve one role-boundary shape",
        true_shape == simulation_shape,
    )

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} of {checks} checks failed)")
    raise SystemExit(1)

print(f"SUMMARY: PASS ({checks} of {checks} checks satisfied expectations)")
print("AUTHORITY: producer and resolver evidence only; no verdict or mutation readiness is established")
PY
