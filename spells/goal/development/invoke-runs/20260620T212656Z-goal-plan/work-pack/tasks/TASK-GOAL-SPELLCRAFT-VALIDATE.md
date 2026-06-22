# TASK-GOAL-SPELLCRAFT-VALIDATE

## Objective

Validate the goal spell source/design/plan packet through the spell lifecycle
owner, then prepare source-state synchronization only as a staged proposal.

## Layer And Slice Mapping

- Layer: L0
- Slice: S-001
- Wave: W0
- Gate status: ready

## Source Contracts

- `arcanum/spells/goal/README.md`
- `arcanum/spells/goal/decision-profile.schema`
- `../20260620T202601Z-goal-spec-definitions/SPEC.md`
- `../20260620T202601Z-goal-spec-definitions/DEFINITIONS.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md`
- `WORK-PACK.md`

## Dependencies

None for SWU-GOAL-001. SWU-GOAL-002 depends on SWU-GOAL-001 because the sync
proposal should reflect Spellcraft's accepted or blocked packet view.

## Blocker And Gap State

| ID | State | Handling |
| --- | --- | --- |
| G-GOAL-SCHEMA-HOME | open | Spellcraft decides whether design schemas stay in the invoke run or move. |
| G-GOAL-CRAFT-SYNC | open | Prepare staged proposal only; do not mutate active ledger rows from plan mode. |

## Implementation Detail

Validation should compare source contract, define behavior, design rules,
schemas, contracts, and plan decomposition. It should answer:

1. Does the packet preserve router-only authority?
2. Are public/private boundaries explicit and sufficient?
3. Are generated surfaces clearly installer-owned?
4. Are runtime SWUs gated behind validation?
5. Are schema location and source-state sync gaps owned?

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GOAL-001 | Run Spellcraft validation on the goal source/design/plan packet. | none | `arcanum/spells/goal/development/spellcraft-runs/` or equivalent validation report path | Report pass, flag, or block with evidence and repair route. | Spellcraft validation report. | `spellcraft validate arcanum/spells/goal` or reviewable lifecycle validation result. | manual | Use the listed source contracts and do not execute runtime SWUs. |
| SWU-GOAL-002 | Prepare staged source-state sync proposal for Craft rows that lag authored artifacts. | SWU-GOAL-001 | staged proposal artifact only; no active ledger mutation | Proposal names rows to update, reason, framed diff, approval route, or defers. | Staged proposal or deferral note. | Review for no active Craft mutation and no private path leakage. | local-fallback | Treat Craft source mutation as protected; proposal only. |

## Expected Result Shape

```yaml
swu_id: SWU-GOAL-001
result: pass | flag | block | interrupted
capability_ref: spellcraft
receipt_kind: native-stage
receipt_artifact: <path or none>
files_touched:
  - <path or none>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
residue:
  - <residue or none>
reroute: <next owner or none>
handoff_note: <what the parent coordinator needs next>
```

## Synchronization Rules

- If SWU-GOAL-001 blocks, do not start runtime SWUs.
- If SWU-GOAL-002 produces a staged proposal, approval remains outside Invoke
  plan mode.
- Update `WORK-PACK.md` only through a future refresh if Spellcraft materially
  changes the packet.

## Completion Evidence

Pending.
