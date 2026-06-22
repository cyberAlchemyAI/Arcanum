# Handoff Pack: SWU-GOAL-001 Spellcraft Validate

## Strict Coverage

Status: pass

This pack covers the selected SWU only. It is enough to start lifecycle
validation without reopening the broader plan.

## Selected Unit

| Field | Value |
| --- | --- |
| SWU | `SWU-GOAL-001` |
| Parent task | `TASK-GOAL-SPELLCRAFT-VALIDATE` |
| Goal | Run Spellcraft validation on the goal source/design/plan packet. |
| Dependencies | none |
| Write scope | `arcanum/spells/goal/development/spellcraft-runs/` or equivalent public-safe validation report path |
| Done criteria | Report pass, flag, or block with evidence and repair route. |
| Acceptance evidence | Spellcraft validation report. |
| Validation surface | `spellcraft validate arcanum/spells/goal` or reviewable lifecycle validation result. |
| Execution owner | manual |

## Source Contracts

| Source | Obligation |
| --- | --- |
| `arcanum/spells/goal/README.md` | Source spell contract, lifecycle owner, gates, failure policy, output contract. |
| `arcanum/spells/goal/decision-profile.schema` | Public neutral decision-profile shape. |
| `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/SPEC.md` | Required behavior, scope, interfaces, events, validation matrix. |
| `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | Local and canonical vocabulary for validation language. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md` | Six-view architecture and design gaps. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md` | Rule families and enforcement order. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md` | Contract matrix, output contracts, and boundary contracts. |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md` | Schema inventory and open schema-home question. |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md` | Selected SWU, blockers, gaps, and gate checks. |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/PLAN-DISPATCH.json` | Owner handoff and authority-split boundaries. |

## Validation Checklist

- Router-only authority preserved.
- Public/private boundary preserved.
- Runtime SWUs remain gated after W0.
- Generated runtime surfaces remain installer-owned.
- Schema-home gap is owned by Spellcraft.
- Craft-sync gap is not turned into active mutation.
- Promotion evidence remains future Experiment Harness work.

## Fallback Exploration

Allowed only for:

- `G-GOAL-SCHEMA-HOME`: inspect schema inventory or schema files.
- `G-GOAL-CRAFT-SYNC`: inspect Craft view or ledger to decide whether a staged
  proposal is needed.

Fallback exploration must not mutate source state.

## Stop Rule

Stop blocked if validation requires runtime implementation, private profile
contents, active Craft mutation, generated runtime file edits, or unowned
promotion evidence.
