# Shared Context: Goal Spell Plan

## Boundary

This plan concerns `arcanum/spells/goal` only. It prepares lifecycle validation
and future SWUs for the public spell package. It does not authorize private
profile copying, active Craft ledger mutation, generated runtime surface edits,
commit, push, publication, PR creation, or parent gitlink movement.

## Source Anchors

| Anchor | Use |
| --- | --- |
| `arcanum/spells/goal/README.md` | Source spell contract, phases, gates, output contract, registry readiness. |
| `arcanum/spells/goal/decision-profile.schema` | Public neutral profile shape. |
| `../20260620T202601Z-goal-spec-definitions/SPEC.md` | Required behavior, interfaces, events, validation matrix. |
| `../20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | Local and canonical vocabulary. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md` | Six-view architecture and design gaps. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md` | Rule families and enforcement order. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md` | Owner, boundary, and output contracts. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md` | Schema inventory and schema location questions. |

## Stable Assumptions

- `goal` is a router-only spell.
- `spellcraft` owns spell lifecycle validation.
- `task-session` owns later bounded execution.
- `experiment-harness` owns reusable behavior proof.
- `decision-gate` owns durable approval records.
- `arcana/craft` owns Craft ledger mutation and validation.
- Unknown risk defaults to a protected stop.
- Staged deltas are proposals, not active source truth.

## Do Not Copy

- Filled decision profiles.
- Private source corpus or operator-specific decision data.
- Absolute private paths from local Craft provenance.
- Generated runtime packages as hand-authored source.

## Execution-Time Context Builder Notes

For any future Task Session, select only the source anchors named by that SWU.
Do not include this whole invoke run unless the SWU specifically needs plan
context. The preferred execution unit is one SWU.
