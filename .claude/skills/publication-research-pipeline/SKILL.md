---
name: publication-research-pipeline
description: "Publication Research Pipeline composes Arcanum research capabilities into a governed path from research question to publishable paper package. It keeps source understanding, evidence execution, claim adjudication, paper rewriting, and export packaging in separate owner lanes."
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: spells/publication-research-pipeline/README.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
---

# Publication Research Pipeline

## Identity

- Canonical ID: `publication-research-pipeline`
- Aliases: none
- Scope: library
- Status: draft candidate, not promoted

## Purpose

Publication Research Pipeline composes Arcanum research capabilities into a
governed path from research question to publishable paper package. It keeps
source understanding, evidence execution, claim adjudication, paper rewriting,
and export packaging in separate owner lanes.

## Trigger Conditions

Use this spell when:

- a project aims to produce a publishable research paper;
- local source understanding and empirical evidence both matter;
- experiment outputs must update a paper without overclaiming;
- multiple sigils and task sessions need one route, gate model, and evidence
  boundary.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| --- | --- | --- |
| `refine` | Shape route, ambiguity, and next owner decisions. | strategy/design |
| `dispatch-spec` | Validate the route DAG and handoff boundaries. | validate |
| `research-tower` | Build or validate source-backed understanding and bridge decisions. | standard/full |
| `context-builder` | Build compact source/evidence packs for execution. | standard |
| `research-evidence-harness` | Validate run schemas, fixtures, metrics, and result summaries. | dry-run/validate |
| `task-session` | Execute bounded SWUs. | task/SWU |

## Optional Sigils

| Sigil | Use When | Notes |
| --- | --- | --- |
| `inventory` | Source library/provenance coverage is incomplete. | Feeds source/context readiness. |
| `definitions-governance` | Terms or metrics risk drift. | Keeps definitions canonical within the project. |
| `ontology-vault` | A research graph or typed relationship model drives paper sections. | Useful for graph-derived paper contracts. |
| `codex-goal-profile` | A ready SWU needs native Codex Goal execution. | Emits compact goal command/profile. |
| `spellcraft` | The spell itself is being revised or validated. | Lifecycle owner for this spell. |

## Prerequisites

- Research project root exists.
- Claims, definitions, and at least one protocol or experiment candidate exist.
- Write scope for any execution SWU is bounded.
- Evidence-status upgrades require live analysis, not dry-run fixtures.

## Shared State

| State | Owner | Updated By | Consumed By |
| --- | --- | --- | --- |
| Research route dispatch | `dispatch-spec` | phase 1 | all phases |
| Tower learning pack | `research-tower` | phase 2 | source and paper phases |
| Context/evidence pack | `context-builder` | phase 3 | task-session and goal profile |
| Run schema and fixtures | `research-evidence-harness` | phase 4 | dry-run and analysis phases |
| Evidence status | research project | analysis task | paper rewrite/export |
| Paper package | research project | paper rewrite/export phase | publication package |

## Execution Phases

| Phase | Capability | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1 Route | `refine` + `dispatch-spec` | project objective | dispatch route and owner decisions | route validates | block on invalid route |
| 2 Learning Tower | `research-tower` | sources/corpus/question | local learning tower or recognition report | source boundaries pass | block if source claims collapse into local inference |
| 3 Source Context | `context-builder` + `inventory` | tower/source artifacts | context pack and source obligations | coverage sufficient | flag or block by missing authority |
| 4 Evidence Harness | `research-evidence-harness` | protocols/work-pack | schema, validator, fixtures, result-summary plan | dry-run validation passes | block before live runs |
| 5 Bounded Execution | `task-session` + optional `codex-goal-profile` | ready SWU | runtime task result | acceptance evidence present | stop with BLOCK report |
| 6 Claim Adjudication | project-specific analysis | live result data | evidence status updates | live data supports update | preserve insufficient evidence |
| 7 Paper Rewrite | project paper contract | evidence status and graph | paper sections and review | claims match evidence | block overclaims |
| 8 Export | project export gate | paper/data/protocols | publication package | reproducibility package complete | defer missing pieces |

## Local Customization

- Spell root: `spells/publication-research-pipeline/`
- Gate strictness: strict for evidence and claims, standard for planning
- Interaction mode: guided-auto for planning; explicit approval for live runs

## Observability

Record spell-level telemetry when `.arcanum/observability/` exists:

- project root;
- phases attempted;
- route validation result;
- tower status;
- evidence-harness validation;
- live-run authorization state;
- evidence-status changes;
- publication blockers.

## Output Contract

Return:

```markdown
## Publication Research Pipeline Result

- Project: <path>
- Status: pass | flag | block
- Dispatch route: <path>
- Tower status: pass | partial | block | not-needed
- Evidence harness: pass | partial | block
- Ready SWUs: <list>
- Goal profiles: <paths or none>
- Paper readiness: draft | evidence-blocked | publishable
- Exports: <paths or none>
- Next route: task-session | codex-goal | research-tower | research-evidence-harness | deferred
```
