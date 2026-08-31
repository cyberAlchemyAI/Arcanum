#!/usr/bin/env python3
"""Prepare a confirmation-pending capability-bound tournament dispatch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DISPATCH_DIR = ROOT / "dispatch"
PREFIX = "spells/invoke/development/define-v2-documentation/tournament"
CANDIDATES = ("alpha", "beta", "gamma")


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def trial_ids() -> list[str]:
    return [f"trial-{candidate}-{replicate:02d}" for replicate in (1, 2) for candidate in CANDIDATES]


def inputs_for(trial_id: str, candidate: str) -> list[str]:
    return [
        f"{PREFIX}/guides/guide-{candidate}.md",
        f"{PREFIX}/cases/case-01-simple",
        f"{PREFIX}/cases/case-02-relations",
        f"{PREFIX}/cases/case-03-structural",
        f"{PREFIX}/runs/{trial_id}/TRIAL.json",
    ]


def briefing_for(trial_id: str, candidate: str) -> dict[str, Any]:
    own_write = f"{PREFIX}/runs/{trial_id}/sources"
    other_guides = [
        f"{PREFIX}/guides/guide-{item}.md" for item in CANDIDATES if item != candidate
    ]
    other_trials = [f"{PREFIX}/runs/{item}" for item in trial_ids() if item != trial_id]
    forbidden_reads = [
        f"{PREFIX}/content",
        f"{PREFIX}/oracle",
        f"{PREFIX}/dispatch",
        f"{PREFIX}/render_candidates.py",
        f"{PREFIX}/build_oracle_sources.py",
        f"{PREFIX}/prepare_dispatch.py",
        f"{PREFIX}/score_tournament.py",
        "spells/invoke/schemas",
        "spells/invoke/scripts/compile_define_source_v2.py",
        "spells/invoke/scripts/validate_definitions_artifact.py",
        "spells/invoke/development/test_compile_define_source_v2.py",
        *other_guides,
        *other_trials,
    ]
    forbidden_writes = [
        f"{PREFIX}/content",
        f"{PREFIX}/oracle",
        f"{PREFIX}/dispatch",
        f"{PREFIX}/guides",
        f"{PREFIX}/cases",
        *[f"{PREFIX}/runs/{item}/sources" for item in trial_ids() if item != trial_id],
        "spells/invoke/schemas",
        "spells/invoke/scripts",
    ]
    instructions = (
        f"Run the blinded Invoke Define v2 documentation trial {trial_id}. Read only the assigned "
        f"guide guide-{candidate}.md, the three declared case directories, and this trial's manifest "
        "and source directory. Treat the three cases as the explicit all-case experiment set. Use "
        "ordinary local tools to inspect allowed files and compute exact repository-relative paths, "
        "SHA-256 digests, byte sizes, selectors, and line bounds. Do not read any other candidate, "
        "oracle, scorer, renderer, dispatch artifact, Invoke schema, compiler, validator, test, or "
        "prior trial. Do not run the Invoke compiler or validators. Author exactly case-01.json, "
        "case-02.json, and case-03.json in the declared write scope. Stop after the first complete "
        "source bytes; do not repair them from compiler feedback. If any forbidden read occurs, "
        "return task_status=blocked and name it in blockers. Return the required receipt fields and "
        "do not claim semantic truth, acceptance, promotion, publication, deployment, or production readiness."
    )
    return {
        "agent_identity": f"Blinded documentation trial {trial_id}",
        "angle": f"Use only opaque candidate {candidate} to author the same three first-attempt sources.",
        "instructions": instructions,
        "status_semantics": {
            "task_status_field": "task_status",
            "task_complete_value": "completed",
            "task_blocked_value": "blocked",
            "domain_gate_status_field": "domain_gate_status",
            "domain_gate_is_separate": True,
        },
        "read_policy": {
            "input_refs": inputs_for(trial_id, candidate),
            "allowed_read_scopes": [
                f"{PREFIX}/guides/guide-{candidate}.md",
                f"{PREFIX}/cases/case-01-simple",
                f"{PREFIX}/cases/case-02-relations",
                f"{PREFIX}/cases/case-03-structural",
                f"{PREFIX}/runs/{trial_id}/TRIAL.json",
                own_write,
            ],
            "forbidden_read_scopes": forbidden_reads,
            "required_input_refs_readable": True,
        },
        "write_policy": {
            "mutation_policy": "proposal-only",
            "write_scope": [own_write],
            "forbidden_write_scopes": forbidden_writes,
        },
        "receipt_shape": {
            "required_fields": [
                "task_status",
                "domain_gate_status",
                "artifacts",
                "validation",
                "blockers",
                "residue",
                "handoff_note",
            ],
            "completion_requires_all_fields": True,
        },
        "authority_ceiling": {
            "summary": "Author only three candidate-local first-attempt source proposals for one blinded trial.",
            "allowed_actions": [
                "read_declared_inputs",
                "compute_exact_evidence",
                "write_declared_source_proposals",
                "return_trial_receipt",
            ],
            "forbidden_actions": [
                "read_forbidden_inputs",
                "run_define_compiler_or_validator",
                "repair_after_scoring",
                "acceptance",
                "promotion",
                "publication",
                "deployment",
                "production_claim",
            ],
        },
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    briefings = {"roles": {}}
    role_specs: list[dict[str, Any]] = []
    receipt_refs: list[str] = []
    for replicate in (1, 2):
        for candidate in CANDIDATES:
            trial_id = f"trial-{candidate}-{replicate:02d}"
            briefing = briefing_for(trial_id, candidate)
            briefings["roles"][trial_id] = briefing

    briefings_path = DISPATCH_DIR / "briefings.json"
    write_json(briefings_path, briefings)
    artifact_sha = hashlib.sha256(briefings_path.read_bytes()).hexdigest()

    for replicate in (1, 2):
        for candidate in CANDIDATES:
            trial_id = f"trial-{candidate}-{replicate:02d}"
            briefing = briefings["roles"][trial_id]
            receipt = f"receipts/{trial_id}.json"
            receipt_refs.append(receipt)
            role_specs.append(
                {
                    "role_id": trial_id,
                    "purpose": f"Produce three first-attempt Define v2 sources using opaque guide {candidate}.",
                    "owns": f"The source proposals and receipt for {trial_id} only.",
                    "capability_ref": "experiment-harness",
                    "capability_target": f"{PREFIX}/runs/{trial_id}",
                    "capability_mode": "run-all",
                    "agent_count": 1,
                    "mutation_policy": "proposal-only",
                    "write_scope": briefing["write_policy"]["write_scope"],
                    "forbidden_write_scopes": briefing["write_policy"]["forbidden_write_scopes"],
                    "briefing_binding": {
                        "contract_version": "arcanum.confirmed-role-briefing.v0.1",
                        "source_binding": {
                            "artifact_path": "briefings.json",
                            "artifact_sha256": artifact_sha,
                            "selector": f"/roles/{trial_id}",
                            "selected_payload_sha256": canonical_digest(briefing),
                        },
                        "briefing": briefing,
                        "briefing_sha256": canonical_digest(briefing),
                    },
                    "depends_on_roles": [],
                    "input_refs": inputs_for(trial_id, candidate),
                    "output_refs": [receipt],
                    "applies_to_steps": ["run-blinded-trials"],
                }
            )

    step_inputs = [{"kind": "intent", "ref": "intent.raw"}]
    seen_inputs: set[str] = set()
    for role in role_specs:
        for ref in role["input_refs"]:
            if ref not in seen_inputs:
                step_inputs.append({"kind": "artifact", "ref": ref})
                seen_inputs.add(ref)

    dispatch = {
        "dispatch_id": "invoke-define-v2-documentation-order-tournament-v1",
        "intent": {
            "raw": "Run a real blinded tournament to determine whether documentation order changes first-attempt Invoke Define v2 authoring quality.",
            "objective": "Compare schema-order, tutorial-first, and ownership-first guides using six isolated agents, three satisfiable authoring cases, the canonical compiler, and a frozen deterministic scorer.",
            "target_artifact": f"{PREFIX}/SCORECARD.json",
            "arcanum_vocabulary": ["invoke", "whisper", "experiment-harness", "dispatch-spec", "orchestrate"],
        },
        "mode": "tournament",
        "techniques": [
            "tournament",
            "toy_game",
            "validation_loop",
            "role_projection_boundary",
            "execution_receipt_handoff",
            "concrete_path_evidence",
            "owner_boundary_check",
            "artifact_contract_bridge",
            "observability_grouping",
        ],
        "subagent_strategy": {
            "status": "required",
            "trigger": "Six independent first-attempt outputs are required, and alternative guides must remain isolated to avoid cross-candidate contamination.",
            "explanation": "Two replicas per candidate provide directional behavioral evidence while two balanced waves respect the host concurrency limit.",
            "context": [
                "All candidates contain identical rendered section bytes; only order changes.",
                "Each trial authors the same three satisfiable public Define v2 cases.",
                "The parent alone compiles and scores frozen first-attempt bytes.",
            ],
            "binding_mode": "capability-bound",
            "execution_owner": "orchestrate",
            "roles": role_specs,
            "execution_waves": [
                {
                    "wave_id": "replicate-01",
                    "role_ids": ["trial-alpha-01", "trial-beta-01", "trial-gamma-01"],
                    "parallel": True,
                    "join_policy": "all",
                    "gate_after": "wave-01-complete",
                    "on_incomplete": "block",
                },
                {
                    "wave_id": "replicate-02",
                    "role_ids": ["trial-alpha-02", "trial-beta-02", "trial-gamma-02"],
                    "parallel": True,
                    "join_policy": "all",
                    "depends_on_waves": ["replicate-01"],
                    "on_incomplete": "block",
                },
            ],
            "parallelism": "tournament",
            "join_policy": "all",
            "authorization": "requires_user_permission",
            "permission_prompt": "Confirm the frozen criterion and run six blinded trials: two agents per guide, each authoring all three cases, followed by one root-owned first-attempt score?",
            "receipt_requirements": [
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
            ],
        },
        "subagent_lifecycle": {"status": "none", "agents": []},
        "steps": [
            {
                "step_id": "run-blinded-trials",
                "name": "Run six isolated first-attempt documentation trials",
                "capability_ref": "experiment-harness",
                "capability_status": "local-extension",
                "mode": "run-all",
                "pattern": "tournament",
                "parallel": True,
                "roles": [role["role_id"] for role in role_specs],
                "techniques": [
                    "tournament",
                    "toy_game",
                    "validation_loop",
                    "role_projection_boundary",
                    "execution_receipt_handoff",
                    "concrete_path_evidence",
                    "owner_boundary_check",
                ],
                "inputs": step_inputs,
                "outputs": [{"kind": "receipt", "ref": ref} for ref in receipt_refs],
                "join_policy": "all",
                "convergence_criteria": [
                    "all six agents return terminal receipts",
                    "each completed trial returns exactly three first-attempt source paths",
                    "no receipt discloses a forbidden read or compiler-assisted repair",
                    "the unchanged deterministic scorer produces one re-derivable verdict",
                ],
                "evidence_artifact": f"{PREFIX}/SCORECARD.json",
                "stop_conditions": [
                    "stop if the criterion is not frozen before the first spawn",
                    "stop if any briefing digest, guide manifest, oracle, compiler, or scorer changed after freeze",
                    "stop if any agent reads a forbidden scope or repairs a source after parent compilation",
                    "stop if a wave is incomplete; do not substitute a new trial implicitly",
                ],
            }
        ],
        "gates": [
            {
                "gate_id": "criterion-frozen",
                "kind": "human_approval",
                "owner": "human",
                "condition": "The human confirms the exact hypothesis, candidates, cases, first-attempt rule, outcome rule, and six-trial strategy before any spawn.",
                "on_fail": "block",
            },
            {
                "gate_id": "wave-01-complete",
                "kind": "validation",
                "owner": "orchestrate",
                "condition": "All three replicate-01 trials are joined and closed with complete, non-contaminated receipts before replicate-02 starts.",
                "applies_after_wave": "replicate-01",
                "requires_role_receipts": [
                    "receipts/trial-alpha-01.json",
                    "receipts/trial-beta-01.json",
                    "receipts/trial-gamma-01.json",
                ],
                "on_fail": "block",
            },
            {
                "gate_id": "score-frozen-bytes",
                "kind": "validation",
                "owner": "experiment-harness",
                "condition": "The parent compiles each returned source exactly once and scores all frozen bytes with the unchanged oracle and scorer.",
                "on_fail": "block",
            },
            {
                "gate_id": "no-promotion",
                "kind": "promotion_guardrail",
                "owner": "invoke",
                "condition": "Tournament evidence remains development evidence and cannot directly promote the guide, transport, registry, or any generated definition.",
                "on_fail": "block",
            },
        ],
        "boundary_evidence": {
            "boundaries": [
                {
                    "boundary_id": "trial-read-isolation",
                    "kind": "artifact_import",
                    "from_owner": "experiment-harness",
                    "to_owner": "trial agents",
                    "applies_to_steps": ["run-blinded-trials"],
                    "contract": "Each trial receives one guide, three cases, and its own manifest; other candidates, oracles, implementation contracts, and results remain forbidden reads.",
                    "on_violation": "block",
                },
                {
                    "boundary_id": "first-attempt-receipt",
                    "kind": "evidence_return",
                    "from_owner": "trial agents",
                    "to_owner": "experiment-harness",
                    "applies_to_steps": ["run-blinded-trials"],
                    "contract": "Agents return source paths and receipts; the parent alone compiles and scores immutable first-attempt bytes.",
                    "on_violation": "block",
                },
            ],
            "authority": {
                "lifecycle": "invoke",
                "execution": "orchestrate",
                "validation": "experiment-harness and canonical Invoke compiler",
                "evidence": "experiment-harness",
                "promotion": "owning Invoke and Whisper lifecycle gates",
            },
            "receipts": [
                {
                    "receipt_id": "trial-receipts",
                    "producer": "six blinded trial agents",
                    "required_fields": [
                        "dispatch_id",
                        "step_id",
                        "capability_ref",
                        "status",
                        "artifacts",
                        "validation",
                        "blockers",
                        "residue",
                        "handoff_note",
                    ],
                    "stores": receipt_refs,
                    "on_missing": "block",
                }
            ],
        },
        "observability": {
            "dispatch_id_required": True,
            "trace_events": [
                "criterion_frozen",
                "trial_spawned",
                "trial_joined",
                "trial_closed",
                "wave_gate_decided",
                "frozen_sources_scored",
                "tournament_adjudicated",
            ],
            "signal_grouping": "dispatch_id, wave_id, role_id, and trial_id",
        },
        "promotion_guardrails": [
            "A winning guide remains a documentation candidate until its owning lifecycle accepts it.",
            "Trial compile passes establish producer acceptance of sources, not semantic truth or active definition authority.",
            "The candidate Whisper transport remains unproven by this bounded tournament.",
        ],
    }
    write_json(DISPATCH_DIR / "RUN-DISPATCH.candidate.json", dispatch)
    print("DISPATCH_PREPARE=pass")
    print("AUTHORIZATION=requires_user_permission")
    print(f"ROLE_COUNT={len(role_specs)}")
    print("WAVE_COUNT=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
