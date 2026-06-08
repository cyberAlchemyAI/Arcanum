---
name: MOGT Harness 001 Context Pack
description: Strict local context for SWU-MOGT-HARNESS-001.
created: 2026-06-07
coverage: pass
---

# MOGT Harness 001 Context Pack

## Selected Unit

`SWU-MOGT-HARNESS-001` from `research/mogt-agentic-conversation/development/WORK-PACK.md`.

Objective: define a MOGT experiment-run JSONL schema and validator for S4
dry-run fixtures.

## Source Evidence

- `research/mogt-agentic-conversation/development/HARNESS-FEASIBILITY.md`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/MARS-IMPORT-ABSORPTION.md`
- `research/mogt-agentic-conversation/development/refinement-runs/20260607T204404Z-mars-import-absorption/RESULT.md`
- `../implementation/mars/templates/schema-foundation-template.json`
- `../implementation/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- `../implementation/mars/definitions/MARS-PIPELINE.md`
- `arcana/research-evidence-harness/SKILL.md`

## Required Common Fields

The schema must cover at least:

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

## First-Wave Experiment Fields

- E1: `traceability_coverage`, `acceptance_score`.
- E2: `dominated_selection`, `decision_quality_score`, `regret_or_proxy`, `frontier_membership`.
- E3: `convergence_status`, `cycle_count`, `escalation_events`, `conflict_resolution_quality`.
- E4: `overhead_acceptability_ratio`, `quality_retention`, `reviewer_burden`.

## Write Scope

- `research/mogt-agentic-conversation/experiments/schema/`
- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`

## Guardrails

- Do not run live experiments.
- Do not update `results/MOGT-EVIDENCE-STATUS.md` to supported or partially supported.
- Do not rewrite paper result sections.
- Do not mutate canonical Experiment Harness, Dispatch Spec, Whisper, Refine, Invoke, Research Tower, or Research Evidence Harness contracts during SWU execution.
- MARS assets are reference evidence. Derive a MOGT-specific schema rather than copying MARS DomainSpec fields unchanged.

## Verification Surface

The runtime result must show:

1. Validator passes at least one synthetic valid JSONL fixture.
2. Validator rejects at least one synthetic invalid JSONL fixture.
3. Rejection covers missing run metadata, missing objective vector, missing policy regime, or malformed metric fields.
4. The result records exact commands and outputs.
