#!/usr/bin/env python3
"""Mutation checks for capability-bound Dispatch Spec invariants."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable


PACKAGE = Path(__file__).resolve().parents[1]
VALIDATOR = PACKAGE / "scripts" / "validate-dispatch.py"
BASE_FIXTURE = PACKAGE / "examples" / "capability-bound-artifact-repair.json"
SOURCE_FIXTURE = PACKAGE / "examples" / "capability-bound-artifact-repair-briefings.json"


def role(doc: dict[str, Any], role_id: str) -> dict[str, Any]:
    for candidate in doc["subagent_strategy"]["roles"]:
        if candidate["role_id"] == role_id:
            return candidate
    raise KeyError(role_id)


def step(doc: dict[str, Any], step_id: str) -> dict[str, Any]:
    for candidate in doc["steps"]:
        if candidate["step_id"] == step_id:
            return candidate
    raise KeyError(step_id)


def remove_whisper_receipt(doc: dict[str, Any]) -> None:
    role(doc, "artifact-repair")["input_refs"] = ["receipts/xray-iteration.json"]
    step(doc, "s3")["inputs"] = [
        item for item in step(doc, "s3")["inputs"] if item["ref"] != "receipts/whisper-iteration.json"
    ]


def overlap_parallel_writes(doc: dict[str, Any]) -> None:
    role(doc, "whisper-lifecycle")["write_scope"] = ["arcana/x-ray/review/"]


def remove_authorization(doc: dict[str, Any]) -> None:
    doc["subagent_strategy"]["authorization"] = "requires_user_permission"


def remove_artifact_agent(doc: dict[str, Any]) -> None:
    doc["subagent_lifecycle"]["agents"] = [
        agent
        for agent in doc["subagent_lifecycle"]["agents"]
        if agent["role_id"] != "artifact-repair"
    ]


def mismatch_capability(doc: dict[str, Any]) -> None:
    role(doc, "xray-lifecycle")["capability_ref"] = "task-session"


def replace_receipt_output(doc: dict[str, Any]) -> None:
    step(doc, "s1")["outputs"][0]["kind"] = "artifact"


def duplicate_receipt_producer(doc: dict[str, Any]) -> None:
    role(doc, "whisper-lifecycle")["output_refs"] = ["receipts/xray-iteration.json"]
    step(doc, "s2")["outputs"][0]["ref"] = "receipts/xray-iteration.json"


def mismatch_lifecycle_scope(doc: dict[str, Any]) -> None:
    for agent in doc["subagent_lifecycle"]["agents"]:
        if agent["role_id"] == "artifact-repair":
            agent["write_scope"] = ["examples/"]
            return
    raise KeyError("artifact-repair")


def block_upstream_receipt(doc: dict[str, Any]) -> None:
    doc["native_stage_receipts"][0]["status"] = "block"
    doc["native_stage_receipts"][0]["blockers"] = ["synthetic upstream failure"]
    doc["native_stage_receipts"][0]["residue"] = "X-Ray receipt did not pass."


def remove_native_receipts(doc: dict[str, Any]) -> None:
    doc["native_stage_receipts"] = []


def point_wave_at_unrelated_gate(doc: dict[str, Any]) -> None:
    doc["subagent_strategy"]["execution_waves"][0]["gate_after"] = "g-artifact-scope"


def alias_parallel_scope(doc: dict[str, Any]) -> None:
    aliased_scope = "arcana/other/../x-ray/review/"
    role(doc, "whisper-lifecycle")["write_scope"] = [aliased_scope]
    for agent in doc["subagent_lifecycle"]["agents"]:
        if agent["role_id"] == "whisper-lifecycle":
            agent["write_scope"] = [aliased_scope]
            return
    raise KeyError("whisper-lifecycle")


def block_required_spawn(doc: dict[str, Any]) -> None:
    for agent in doc["subagent_lifecycle"]["agents"]:
        if agent["role_id"] == "xray-lifecycle":
            agent["spawn_status"] = "blocked"
            agent["spawn_error"] = "synthetic thread cap"
            agent["residue"] = "X-Ray worker did not run."
            agent["reroute"] = "return dispatch status block"
            agent.pop("join_status", None)
            agent.pop("close_status", None)
            agent.pop("receipt_artifact", None)
            return
    raise KeyError("xray-lifecycle")


CASES: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
    (
        "missing dependency receipt",
        remove_whisper_receipt,
        "input_refs do not consume any output_ref from dependency 'whisper-lifecycle'",
    ),
    (
        "overlapping parallel writes",
        overlap_parallel_writes,
        "concurrent write scopes overlap",
    ),
    (
        "unapproved lifecycle closeout",
        remove_authorization,
        "capability-bound lifecycle closeout requires subagent_strategy.authorization=approved",
    ),
    (
        "missing declared agent",
        remove_artifact_agent,
        "pass closeout expected 1 agent records, found 0",
    ),
    (
        "role and step capability mismatch",
        mismatch_capability,
        "capability_ref 'task-session' does not match step 's1' capability_ref 'sigil-development'",
    ),
    (
        "role output is not a receipt",
        replace_receipt_output,
        "output_refs are not declared as receipt outputs by applied steps",
    ),
    (
        "duplicate receipt producer",
        duplicate_receipt_producer,
        "is produced by multiple roles",
    ),
    (
        "lifecycle write scope mismatch",
        mismatch_lifecycle_scope,
        "write_scope does not match role",
    ),
    (
        "blocked upstream receipt",
        block_upstream_receipt,
        "receipt status is block",
    ),
    (
        "missing native receipts",
        remove_native_receipts,
        "capability-bound pass closeout requires native_stage_receipts",
    ),
    (
        "wave points at unrelated gate",
        point_wave_at_unrelated_gate,
        "must declare applies_after_wave='lifecycle-updates'",
    ),
    (
        "aliased parallel scope",
        alias_parallel_scope,
        "scope must be a safe repository-relative path",
    ),
    (
        "blocked required spawn",
        block_required_spawn,
        "capability-bound pass requires successful spawn",
    ),
]


def main() -> int:
    base = json.loads(BASE_FIXTURE.read_text(encoding="utf-8"))
    failures: list[str] = []

    baseline = subprocess.run(
        [str(VALIDATOR), str(BASE_FIXTURE), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    baseline_result = json.loads(baseline.stdout)
    if baseline_result.get("validation") != "pass":
        print(f"CAPABILITY_BOUND_MUTATIONS=block BASELINE={baseline_result}")
        return 1
    print("MUTATION_BASELINE=pass")

    with tempfile.TemporaryDirectory(prefix="dispatch-spec-mutations-") as temp_dir:
        temp_root = Path(temp_dir)
        for index, (name, mutate, expected_block) in enumerate(CASES, start=1):
            candidate = copy.deepcopy(base)
            candidate["dispatch_id"] = f"mutation-{index}"
            mutate(candidate)
            candidate_path = temp_root / f"case-{index}.json"
            shutil.copyfile(
                SOURCE_FIXTURE,
                temp_root / "capability-bound-artifact-repair-briefings.json",
            )
            candidate_path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
            completed = subprocess.run(
                [str(VALIDATOR), str(candidate_path), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            try:
                result = json.loads(completed.stdout)
            except json.JSONDecodeError:
                failures.append(f"{name}: validator did not return JSON: {completed.stdout or completed.stderr}")
                continue
            matched = any(expected_block in block for block in result.get("blocks", []))
            if result.get("validation") != "block" or not matched:
                failures.append(
                    f"{name}: expected block containing {expected_block!r}, got {result}"
                )
            else:
                print(f"MUTATION=pass CASE={name}")

    if failures:
        for failure in failures:
            print(f"MUTATION=block {failure}")
        print("CAPABILITY_BOUND_MUTATIONS=block")
        return 1

    print("CAPABILITY_BOUND_MUTATIONS=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
