#!/usr/bin/env python3
"""Materialize closeout evidence and evaluate one native canary scenario."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parent
REPO_ROOT = RUN_ROOT.parents[5]
VALIDATOR = REPO_ROOT / "arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py"
PREFIX = (
    "arcanum/formulae/dispatch-spec/development/runtime-integration/"
    "20260722T063407Z-native-host-canary"
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, events: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(event, separators=(",", ":")) + "\n" for event in events),
        encoding="utf-8",
    )


def lifecycle_agent(receipt: dict, lane_name: str) -> dict:
    return {
        "agent_id": receipt["agent_id"],
        "role_id": receipt["role_id"],
        "capability_ref": receipt["capability_ref"],
        "capability_target": receipt["capability_target"],
        "capability_mode": receipt["capability_mode"],
        "wave_id": receipt["wave_id"],
        "write_scope": receipt["write_scope"],
        "lane_name": lane_name,
        "spawn_status": "spawned",
        "join_status": "completed",
        "receipt_artifact": receipt["artifacts"][0],
        "close_status": "closed",
        "residue": receipt["residue"],
        "reroute": receipt["reroute"],
    }


def validate(closeout: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), str(closeout.relative_to(REPO_ROOT))],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    status = "unknown"
    for line in output.splitlines():
        if line.startswith("VALIDATION="):
            status = line.split("=", 1)[1].strip()
            break
    return {
        "command": f"python3 {VALIDATOR.relative_to(REPO_ROOT)} {closeout.relative_to(REPO_ROOT)}",
        "exit_code": completed.returncode,
        "status": status,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def finalize_failure() -> bool:
    root = RUN_ROOT / "failure"
    source = read_json(root / "source.dispatch.json")
    xray = read_json(root / "receipts/xray.json")
    whisper = read_json(root / "receipts/whisper.json")
    gate = read_json(root / "gate-decision.json")

    events = [
        {"seq": 1, "event": "scenario_started", "dispatch_id": source["dispatch_id"]},
        {"seq": 2, "event": "subagent_spawned", "role_id": "xray-lifecycle", "agent_id": xray["agent_id"]},
        {"seq": 3, "event": "subagent_spawned", "role_id": "whisper-lifecycle", "agent_id": whisper["agent_id"]},
        {"seq": 4, "event": "subagent_joined_closed", "role_id": "xray-lifecycle", "status": xray["status"]},
        {"seq": 5, "event": "subagent_joined_closed", "role_id": "whisper-lifecycle", "status": whisper["status"]},
        {"seq": 6, "event": "wave_joined", "wave_id": "lifecycle-checks", "join_policy": "all"},
        {"seq": 7, "event": "lifecycle_gate_blocked", "gate_id": gate["gate_id"]},
        {"seq": 8, "event": "artifact_spawn_withheld", "role_id": "artifact-repair"},
    ]
    write_jsonl(root / "run-events.jsonl", events)

    closeout = copy.deepcopy(source)
    closeout["subagent_lifecycle"] = {
        "status": "block",
        "agents": [
            lifecycle_agent(xray, "Failure X-Ray lifecycle observation"),
            lifecycle_agent(whisper, "Failure Whisper lifecycle reflection"),
        ],
    }
    closeout["native_stage_receipts"] = [xray, whisper]
    closeout_path = root / "closeout.dispatch.json"
    write_json(closeout_path, closeout)
    validation = validate(closeout_path)
    write_json(root / "validation.json", validation)

    artifact_spawn_events = [
        event
        for event in events
        if event["event"] == "subagent_spawned" and event.get("role_id") == "artifact-repair"
    ]
    assertions = {
        "xray_receipt_is_block": xray.get("status") == "block",
        "whisper_receipt_is_pass": whisper.get("status") == "pass",
        "gate_is_block": gate.get("decision") == "block",
        "artifact_spawn_event_count_is_zero": len(artifact_spawn_events) == 0,
        "artifact_spawn_withheld_event_exists": any(
            event["event"] == "artifact_spawn_withheld" for event in events
        ),
        "artifact_receipt_absent": not (root / "receipts/artifact.json").exists(),
        "artifact_output_absent": not (root / "artifact/output.json").exists(),
        "dispatch_validator_is_block": validation["status"] == "block",
    }
    passed = all(assertions.values())
    write_json(
        root / "result.json",
        {
            "scenario": "failure-withholding",
            "expected": "failed required receipt withholds artifact worker",
            "assertions": assertions,
            "scenario_status": "pass" if passed else "fail",
            "evidence": [
                f"{PREFIX}/failure/gate-decision.json",
                f"{PREFIX}/failure/run-events.jsonl",
                f"{PREFIX}/failure/closeout.dispatch.json",
                f"{PREFIX}/failure/validation.json",
            ],
        },
    )
    return passed


def finalize_success() -> bool:
    root = RUN_ROOT / "success"
    source = read_json(root / "source.dispatch.json")
    xray = read_json(root / "receipts/xray.json")
    whisper = read_json(root / "receipts/whisper.json")
    artifact = read_json(root / "receipts/artifact.json")
    gate = read_json(root / "gate-decision.json")

    events = [
        {"seq": 1, "event": "scenario_started", "dispatch_id": source["dispatch_id"]},
        {"seq": 2, "event": "subagent_spawned", "role_id": "xray-lifecycle", "agent_id": xray["agent_id"]},
        {"seq": 3, "event": "subagent_spawned", "role_id": "whisper-lifecycle", "agent_id": whisper["agent_id"]},
        {"seq": 4, "event": "subagent_joined_closed", "role_id": "xray-lifecycle", "status": xray["status"]},
        {"seq": 5, "event": "subagent_joined_closed", "role_id": "whisper-lifecycle", "status": whisper["status"]},
        {"seq": 6, "event": "wave_joined", "wave_id": "lifecycle-checks", "join_policy": "all"},
        {"seq": 7, "event": "lifecycle_gate_passed", "gate_id": gate["gate_id"]},
        {"seq": 8, "event": "subagent_spawned", "role_id": "artifact-repair", "agent_id": artifact["agent_id"]},
        {"seq": 9, "event": "artifact_repair_started", "role_id": "artifact-repair"},
        {"seq": 10, "event": "subagent_joined_closed", "role_id": "artifact-repair", "status": artifact["status"]},
        {"seq": 11, "event": "wave_joined", "wave_id": "artifact-repair", "join_policy": "all"},
    ]
    write_jsonl(root / "run-events.jsonl", events)

    closeout = copy.deepcopy(source)
    closeout["subagent_lifecycle"] = {
        "status": "pass",
        "agents": [
            lifecycle_agent(xray, "Success X-Ray lifecycle observation"),
            lifecycle_agent(whisper, "Success Whisper lifecycle reflection"),
            lifecycle_agent(artifact, "Success bounded artifact execution"),
        ],
    }
    closeout["native_stage_receipts"] = [xray, whisper, artifact]
    closeout_path = root / "closeout.dispatch.json"
    write_json(closeout_path, closeout)
    validation = validate(closeout_path)
    write_json(root / "validation.json", validation)

    gate_seq = next(event["seq"] for event in events if event["event"] == "lifecycle_gate_passed")
    artifact_spawn_seq = next(
        event["seq"]
        for event in events
        if event["event"] == "subagent_spawned" and event.get("role_id") == "artifact-repair"
    )
    assertions = {
        "xray_receipt_is_pass": xray.get("status") == "pass",
        "whisper_receipt_is_pass": whisper.get("status") == "pass",
        "gate_is_pass": gate.get("decision") == "pass",
        "artifact_spawn_occurs_after_gate": artifact_spawn_seq > gate_seq,
        "artifact_receipt_is_pass": artifact.get("status") == "pass",
        "artifact_consumed_both_receipts": set(artifact.get("consumed_receipts", []))
        == {xray["artifacts"][0], whisper["artifacts"][0]},
        "artifact_output_exists": (root / "artifact/output.json").exists(),
        "dispatch_validator_is_pass": validation["status"] == "pass",
    }
    passed = all(assertions.values())
    write_json(
        root / "result.json",
        {
            "scenario": "success-path",
            "expected": "two passing required receipts unlock one ordered artifact worker",
            "assertions": assertions,
            "scenario_status": "pass" if passed else "fail",
            "evidence": [
                f"{PREFIX}/success/gate-decision.json",
                f"{PREFIX}/success/run-events.jsonl",
                f"{PREFIX}/success/closeout.dispatch.json",
                f"{PREFIX}/success/validation.json",
            ],
        },
    )
    return passed


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"failure", "success"}:
        raise SystemExit("usage: finalize-canary.py failure|success")
    passed = finalize_failure() if sys.argv[1] == "failure" else finalize_success()
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
