#!/usr/bin/env python3
"""Prepare deterministic inputs and pre-execution Dispatch Specs for this canary."""

from __future__ import annotations

import json
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parent
REPO_PREFIX = (
    "arcanum/formulae/dispatch-spec/development/runtime-integration/"
    "20260722T063407Z-native-host-canary"
)


def rel(scenario: str, suffix: str) -> str:
    return f"{REPO_PREFIX}/{scenario}/{suffix}"


def role(
    scenario: str,
    role_id: str,
    capability_ref: str,
    capability_target: str,
    capability_mode: str,
    step_id: str,
    input_refs: list[str],
    output_ref: str,
    write_scope: list[str],
    *,
    mutation_policy: str,
    depends_on_roles: list[str],
    forbidden_write_scopes: list[str],
) -> dict:
    return {
        "role_id": role_id,
        "purpose": f"Run the {scenario} canary lane for {capability_target}.",
        "owns": output_ref,
        "capability_ref": capability_ref,
        "capability_target": capability_target,
        "capability_mode": capability_mode,
        "agent_count": 1,
        "mutation_policy": mutation_policy,
        "write_scope": write_scope,
        "forbidden_write_scopes": forbidden_write_scopes,
        "depends_on_roles": depends_on_roles,
        "input_refs": input_refs,
        "output_refs": [output_ref],
        "applies_to_steps": [step_id],
    }


def build_dispatch(scenario: str) -> dict:
    dispatch_id = f"native-host-canary-{scenario}"
    xray_input = rel(scenario, "inputs/xray-pass.json")
    whisper_input = rel(scenario, "inputs/whisper-pass.json")
    xray_receipt = rel(scenario, "receipts/xray.json")
    whisper_receipt = rel(scenario, "receipts/whisper.json")
    artifact_receipt = rel(scenario, "receipts/artifact.json")
    artifact_output = rel(scenario, "artifact/output.json")

    roles = [
        role(
            scenario,
            "xray-lifecycle",
            "sigil-development",
            "x-ray",
            "observe",
            "s1",
            [xray_input],
            xray_receipt,
            [xray_receipt],
            mutation_policy="lifecycle-owned",
            depends_on_roles=[],
            forbidden_write_scopes=["arcanum/arcana/x-ray/"],
        ),
        role(
            scenario,
            "whisper-lifecycle",
            "spellcraft",
            "whisper",
            "reflect",
            "s2",
            [whisper_input],
            whisper_receipt,
            [whisper_receipt],
            mutation_policy="lifecycle-owned",
            depends_on_roles=[],
            forbidden_write_scopes=["arcanum/spells/whisper/"],
        ),
        role(
            scenario,
            "artifact-repair",
            "task-session",
            artifact_output,
            "execute",
            "s3",
            [xray_receipt, whisper_receipt],
            artifact_receipt,
            [artifact_output, artifact_receipt],
            mutation_policy="artifact-only",
            depends_on_roles=["xray-lifecycle", "whisper-lifecycle"],
            forbidden_write_scopes=["arcanum/arcana/x-ray/", "arcanum/spells/whisper/"],
        ),
    ]

    receipt_requirements = [
        "agent_id",
        "role_id",
        "spawn_status",
        "join_status",
        "close_status",
        "dispatch_id",
        "step_id",
        "capability_ref",
        "capability_target",
        "capability_mode",
        "wave_id",
        "write_scope",
        "status",
        "artifacts",
        "validation",
        "observer_status",
        "blockers",
        "residue",
        "reroute",
        "handoff_note",
    ]

    return {
        "dispatch_id": dispatch_id,
        "intent": {
            "raw": f"Execute the {scenario} half of the native Dispatch Spec canary.",
            "objective": "Test native host receipt joining and downstream spawn gating.",
            "target_artifact": artifact_output,
        },
        "mode": "mixed",
        "techniques": ["sequence", "observability_grouping"],
        "subagent_strategy": {
            "status": "required",
            "trigger": "Two independent capability receipts gate one downstream artifact worker.",
            "explanation": "The parent owns spawn, join, gate evaluation, and closeout.",
            "context": [
                "Wave one has disjoint receipt write scopes.",
                "Wave two must not start until both wave-one receipts pass.",
            ],
            "binding_mode": "capability-bound",
            "execution_owner": "parent-orchestrator",
            "roles": roles,
            "execution_waves": [
                {
                    "wave_id": "lifecycle-checks",
                    "role_ids": ["xray-lifecycle", "whisper-lifecycle"],
                    "parallel": True,
                    "join_policy": "all",
                    "gate_after": "g-lifecycle-receipts",
                    "on_incomplete": "block",
                },
                {
                    "wave_id": "artifact-repair",
                    "role_ids": ["artifact-repair"],
                    "parallel": False,
                    "join_policy": "all",
                    "depends_on_waves": ["lifecycle-checks"],
                    "on_incomplete": "block",
                },
            ],
            "parallelism": "mixed",
            "join_policy": "parent_synthesis",
            "authorization": "approved",
            "permission_prompt": "Execute the user-approved failure-first native canary?",
            "receipt_requirements": receipt_requirements,
        },
        "subagent_lifecycle": {"status": "none", "agents": []},
        "steps": [
            {
                "step_id": "s1",
                "name": "Run X-Ray lifecycle canary lane",
                "capability_ref": "sigil-development",
                "mode": "observe",
                "pattern": "sequential",
                "parallel": True,
                "inputs": [{"kind": "external_context", "ref": xray_input}],
                "outputs": [{"kind": "receipt", "ref": xray_receipt}],
                "join_policy": "all",
                "stop_conditions": ["stop when the deterministic sentinel is absent or invalid"],
            },
            {
                "step_id": "s2",
                "name": "Run Whisper lifecycle canary lane",
                "capability_ref": "spellcraft",
                "mode": "reflect",
                "pattern": "sequential",
                "parallel": True,
                "inputs": [{"kind": "external_context", "ref": whisper_input}],
                "outputs": [{"kind": "receipt", "ref": whisper_receipt}],
                "join_policy": "all",
                "stop_conditions": ["stop when the deterministic sentinel is absent or invalid"],
            },
            {
                "step_id": "s3",
                "name": "Run bounded artifact worker",
                "capability_ref": "task-session",
                "mode": "execute",
                "pattern": "sequential",
                "parallel": False,
                "depends_on_steps": ["s1", "s2"],
                "techniques": ["sequence", "observability_grouping"],
                "inputs": [
                    {"kind": "receipt", "ref": xray_receipt},
                    {"kind": "receipt", "ref": whisper_receipt},
                ],
                "outputs": [{"kind": "receipt", "ref": artifact_receipt}],
                "stop_conditions": [
                    "stop unless both required receipts pass",
                    "stop if a write would escape the declared run folder",
                ],
            },
        ],
        "gates": [
            {
                "gate_id": "g-lifecycle-receipts",
                "kind": "validation",
                "owner": "parent-orchestrator",
                "condition": "Both required lifecycle receipts pass and their workers are joined and closed before the artifact worker starts.",
                "applies_after_wave": "lifecycle-checks",
                "requires_role_receipts": [xray_receipt, whisper_receipt],
                "on_fail": "block",
            },
            {
                "gate_id": "g-artifact-scope",
                "kind": "quality",
                "owner": "task-session",
                "condition": "The artifact worker consumes both passing receipts and writes only within the scenario folder.",
                "on_fail": "block",
            },
        ],
        "native_stage_receipts": [],
        "observability": {
            "dispatch_id_required": True,
            "trace_events": [
                "subagent_spawned",
                "wave_joined",
                "lifecycle_gate_passed_or_blocked",
                "artifact_spawned_or_withheld",
                "subagent_closed",
            ],
            "signal_grouping": "dispatch_id and wave_id",
        },
        "promotion_guardrails": [
            "The canary receipt is execution evidence, not lifecycle authority.",
            "No canary worker may write outside the declared runtime-integration run folder.",
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for scenario in ("failure", "success"):
        scenario_root = RUN_ROOT / scenario
        (scenario_root / "inputs").mkdir(parents=True, exist_ok=True)
        (scenario_root / "receipts").mkdir(parents=True, exist_ok=True)
        (scenario_root / "artifact").mkdir(parents=True, exist_ok=True)
        write_json(
            scenario_root / "inputs" / "whisper-pass.json",
            {
                "scenario": scenario,
                "capability_target": "whisper",
                "expected_status": "pass",
                "sentinel": "present",
            },
        )
        if scenario == "success":
            write_json(
                scenario_root / "inputs" / "xray-pass.json",
                {
                    "scenario": scenario,
                    "capability_target": "x-ray",
                    "expected_status": "pass",
                    "sentinel": "present",
                },
            )
        write_json(scenario_root / "source.dispatch.json", build_dispatch(scenario))


if __name__ == "__main__":
    main()
