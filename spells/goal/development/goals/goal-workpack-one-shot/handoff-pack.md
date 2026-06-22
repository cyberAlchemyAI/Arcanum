# Handoff Pack: Goal Work-Pack One-Shot

## Strict Coverage

Status: pass

This pack covers the full ordered work-pack stream for `arcanum/spells/goal`.
It is intentionally compact and points to indexed source contracts for details.

## Selected Stream

| Field | Value |
| --- | --- |
| Stream ID | `GOAL-WORKPACK-ONE-SHOT` |
| Work-pack | `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md` |
| Execution pack | `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/EXECUTION-PACK.md` |
| Dispatch | `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/PLAN-DISPATCH.json` |
| SWUs | `SWU-GOAL-001` through `SWU-GOAL-010` |
| Waves | W0, W1, W2, W3 |

## Ordered Stream

| Order | Wave | SWU | Owner Lane | Gate |
| --- | --- | --- | --- | --- |
| 1 | W0 | SWU-GOAL-001 | spellcraft | ready |
| 2 | W0 | SWU-GOAL-002 | local-fallback | after SWU-GOAL-001 |
| 3 | W1 | SWU-GOAL-003 | task-session | after W0 |
| 4 | W1 | SWU-GOAL-004 | task-session | after SWU-GOAL-003 |
| 5 | W2 | SWU-GOAL-005 | task-session | after W1 |
| 6 | W2 | SWU-GOAL-006 | task-session | after SWU-GOAL-005 |
| 7 | W3 | SWU-GOAL-007 | task-session | after W2 |
| 8 | W3 | SWU-GOAL-008 | task-session | after SWU-GOAL-007 |
| 9 | W3 | SWU-GOAL-009 | experiment-harness | after SWU-GOAL-008 |
| 10 | W3 | SWU-GOAL-010 | runtime-installer | after SWU-GOAL-009 |

## Source Contracts

| Source | Coverage |
| --- | --- |
| `arcanum/spells/goal/README.md` | Source spell contract. |
| `arcanum/spells/goal/decision-profile.schema` | Public neutral profile shape. |
| `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/SPEC.md` | Required behavior and validation matrix. |
| `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | Local and canonical vocabulary. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md` | Architecture views and design gaps. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md` | Rule families and enforcement order. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md` | Contract matrix and boundary contracts. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md` | Schema inventory. |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md` | SWU manifest, blockers, and gates. |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/EXECUTION-PACK.md` | Wave choreography. |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/PLAN-DISPATCH.json` | Capability and authority boundaries. |

## Gate Rules

- W0 must close before runtime SWUs.
- Runtime source/write scope must be selected before mutating runtime/source
  files.
- Source-changing progress must stage before approval.
- Protected apply requires batch-specific approval token and durable decision
  record.
- Experiment Harness evidence is required before registry readiness.
- Generated runtime surfaces must come from installer paths.

## Stop Rule

Stop blocked rather than widening scope when any gate lacks owner, evidence,
write scope, approval, or terminal receipt.
