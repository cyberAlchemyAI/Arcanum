---
name: MOGT Harness Feasibility
description: S3 feasibility decision for using Experiment Harness on MOGT dry-run fixtures.
created: 2026-06-07
status: block
---

# MOGT Harness Feasibility

## Verdict

Result: BLOCK.

The current Experiment Harness is usable as a lifecycle evidence harness for Arcanum spells and sigils, and it can create layouts, select prompts, run one bounded runtime example, validate profile metadata, write reports, and emit observability. It is not yet sufficient as the execution engine for MOGT S4 dry-run fixtures because MOGT requires research-experiment mechanics that the harness does not currently own: JSONL run schemas, objective-vector validation, Pareto/frontier scoring, reviewer-rubric integration, and experiment result-summary generation.

## Evidence Inspected

- `research/mogt-agentic-conversation/development/scaffold-readiness.md`
- `research/mogt-agentic-conversation/development/mogt-publication-research.dispatch.json`
- `research/mogt-agentic-conversation/runbooks/PUBLICATION-RESEARCH-STRATEGY.md`
- `research/mogt-agentic-conversation/experiments/EXPERIMENTS.md`
- `research/mogt-agentic-conversation/experiments/E1-tradeoff-traceability-baseline/protocol.md`
- `research/mogt-agentic-conversation/experiments/E2-pareto-arbitration-quality/protocol.md`
- `research/mogt-agentic-conversation/experiments/E3-negotiation-stability-under-conflict/protocol.md`
- `research/mogt-agentic-conversation/experiments/E4-overhead-feasibility-envelope/protocol.md`
- `arcana/experiment-harness/SKILL.md`
- `arcana/experiment-harness/scripts/init-harness.sh`
- `arcana/experiment-harness/scripts/validate-harness.sh`
- `arcana/experiment-harness/scripts/report-harness.sh`
- `arcana/experiment-harness/scripts/run-with-codex.sh`
- `arcana/experiment-harness/development/GENERALIZATION-PROFILE-CONTRACT.md`
- `arcana/experiment-harness/development/PROFILE-PROOF-REPORT.md`

## Required MOGT Run-Data Fields

Minimum fields for S4/S5 readiness:

- `experiment_id`
- `run_id`
- `timestamp`
- `project_id`
- `scenario_id`
- `policy_regime`
- `model`
- `model_temperature`
- `system_prompt_hash`
- `operator`
- `objective_vector`
- `candidate_actions`
- `selected_action`
- `policy_trace`
- `reviewer_scores`
- `token_cost`
- `latency_ms`
- `turn_count`
- `tool_calls`
- `protocol_deviations`

Experiment-specific fields:

- E1: `traceability_coverage`, `acceptance_score`.
- E2: `dominated_selection`, `decision_quality_score`, `regret_or_proxy`, `frontier_membership`.
- E3: `convergence_status`, `cycle_count`, `escalation_events`, `conflict_resolution_quality`.
- E4: `overhead_acceptability_ratio`, `quality_retention`, `reviewer_burden`.

## Harness Capabilities Found

| Capability | Evidence | Feasibility Impact |
| --- | --- | --- |
| Initialize a standard development harness | `init-harness.sh` creates profile, prompts, regimes, fixtures, outputs, runs | useful for runner layout patterns |
| Preserve existing files | `init-harness.sh` writes only missing harness files | safe for scoped setup |
| Select and run one prompt | `run-with-codex.sh` supports `next`, task id, and explicit `--all` gating | useful for bounded prompt execution |
| Reject empty/save-summary outputs | `run-with-codex.sh` validates output body shape | useful for artifact-output discipline |
| Validate profile metadata and fixture outputs | `validate-harness.sh` checks profile, prompts, regimes, fixtures, output quality | useful for lifecycle contracts |
| Write timestamped reports and observability | `report-harness.sh` writes reports and can observe | useful for audit trail |
| Deterministic profile proof exists | `PROFILE-PROOF-REPORT.md` passed sigil/spell profile proofs | supports trust in generic mechanics |

## Harness Gaps

| Gap | Why It Blocks S4 | Needed Development |
| --- | --- | --- |
| No research-project profile | Harness initializes only `spell` or `sigil` artifact types | Add MOGT project/runner profile or use a MOGT-local runner wrapper |
| No MOGT JSONL schema validator | E1-E4 require append-only experiment data with reproducible metadata | Add `tools/validate-mogt-run-jsonl.*` or equivalent |
| No objective-vector validator | MOGT claims depend on explicit multi-objective fields | Define and validate objective vector fields before dry-runs |
| No Pareto/frontier metric calculator | E2 requires dominated-selection and frontier/regret analysis | Add metric calculator or analysis script |
| No reviewer-rubric integration | E1/E3 require blinded review or reviewer scores | Add rubric schema and score ingestion |
| No result-summary generator | Experiments require `results/*.md` summaries with stats and claim impact | Add summary generator tied to data JSONL |
| No protocol-to-run mapping | Current protocols are draft plans, not executable prompt/scenario fixtures | Create scenario fixtures and policy-regime prompts |

## S4 Readiness Decision

S4 dry-run fixtures cannot proceed yet.

The current harness can be reused for layout, bounded run discipline, validation/report patterns, and observability. It cannot, by itself, produce valid MOGT experiment evidence. The next route is a MOGT-local development pack that either extends Experiment Harness through a research-project profile or creates a thin local runner that preserves Experiment Harness-style reports and observability.

## Reroute

Reroute to:

- `research/mogt-agentic-conversation/development/WORK-PACK.md`

Minimum implementation slices:

1. Define MOGT run JSONL schema and validator.
2. Define objective-vector and policy-regime fixtures for E1/E2/E4 first wave.
3. Implement Pareto/frontier and overhead metric calculator.
4. Implement result-summary generator.
5. Create one dry-run fixture per policy regime without live experiment claims.

## Dispatch Validation

Publication dispatch validation command:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py research/mogt-agentic-conversation/development/mogt-publication-research.dispatch.json --json
```

Latest result:

```json
{
  "validation": "pass",
  "blocks": [],
  "flags": []
}
```
