---
stage: 01-context-builder
status: pass
---

# Context Builder: MARS Import Evidence

## MARS Reusable Core

`../implementation/mars/README.md` defines MARS as a reusable research-orchestration framework for gated, reproducible experiments. It owns governance definitions, contracts, templates, reusable skill assets, method exports, and implementation scaffolding.

`../implementation/mars/OWNERSHIP-MIGRATION.md` separates canonical implementation assets from project execution state:

- canonical: `../implementation/mars/definitions/*`
- canonical: `../implementation/mars/templates/*`
- canonical reusable skills: `../implementation/mars/copilot/skills/*`
- project evidence/projection: `../research/projects/mars/**`

## MOGT Gap

`research/mogt-agentic-conversation/development/HARNESS-FEASIBILITY.md` blocks S4 dry-run fixtures because the current Experiment Harness lacks research-project mechanics:

- MOGT JSONL schema validation
- objective-vector validation
- Pareto/frontier metric calculation
- reviewer-rubric integration
- result-summary generation
- protocol-to-run fixture mapping

`research/mogt-agentic-conversation/development/WORK-PACK.md` defines `SWU-MOGT-HARNESS-001` as the next ready unit: define MOGT run JSONL schema and validator.

## Strong MARS Matches

| MOGT Need | MARS Evidence | Reuse Assessment |
| --- | --- | --- |
| Experiment bundle layout | `definitions/EXPERIMENT-BUNDLE-CONTRACT.md` | Directly reusable as MOGT bundle discipline. |
| Methodology profiles | `definitions/METHODOLOGY-PROFILE-CONTRACT.md`, `templates/methodology-profile-template.md` | Already present in MOGT, useful as authority for gap checks. |
| Research-stage gates | `definitions/MARS-PIPELINE.md` | Strong S0-S12/G0-G4 model for research-harness planning. |
| Context bundles | `definitions/MULTI-SOURCE-CONTEXT-PATTERN.md`, `templates/context-bundle-template.md` | Directly useful for MOGT web/prior-art and experiment context. |
| JSON schema starter | `templates/schema-foundation-template.json` | Useful template, but MOGT needs a new schema. |
| Paper derivation | `definitions/PAPER-DERIVATION-RULES.md`, paper templates | Already aligned with MOGT paper artifacts. |
| Telemetry | `templates/telemetry-signal-schema-template.md` | Useful for MOGT experiment/harness signals. |
| Dry-run style | `../research/projects/mars/experiments/MARS-DRY-RUN-E1-foundation/protocol.md` | Good tabletop gate-walkthrough example, not a canonical template. |

## Non-Reusable Without Adaptation

- MARS `schema-foundation-template.json` uses DomainSpec-oriented fields such as `domainspec_version`, `feature_id`, `sample_id`, `metric_name`, and `criteria_*`; MOGT needs `project_id`, `scenario_id`, `policy_regime`, `objective_vector`, `candidate_actions`, `selected_action`, `policy_trace`, `reviewer_scores`, `token_cost`, `latency_ms`, `turn_count`, `tool_calls`, and `protocol_deviations`.
- MARS gates do not define MOGT-specific game-theoretic scoring or bargaining semantics.
- MARS project telemetry and evidence snapshots are project execution artifacts, not reusable Arcanum contracts.
