# TASK-GOAL-RUNTIME-SKELETON

## Objective

Build the smallest read-only runtime skeleton: bind a goal, read a frontier,
classify risk, and emit a non-mutating Goal Loop Result.

## Layer And Slice Mapping

- Layer: L1
- Slice: S-002
- Wave: W1
- Gate status: blocked-after-W0

## Source Contracts

- `arcanum/spells/goal/README.md` Execution Phases and Output Contract
- `arcanum/spells/goal/decision-profile.schema`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/schemas/frontier-snapshot.schema.json`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/schemas/goal-loop-result.schema.json`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md`

## Dependencies

- SWU-GOAL-001 pass or accepted repair.
- Runtime write scope selected by Spellcraft or the first Task Session.

## Blocker And Gap State

| ID | State | Handling |
| --- | --- | --- |
| G-GOAL-RUNTIME-SOURCE | open | Select exact source or implementation files before mutation-capable execution. |
| B-GOAL-W0-VALIDATION | active | Do not start until W0 exits pass or accepted repair. |

## Implementation Detail

### Inputs

- Goal intent or selected Craft context.
- Public decision-profile schema defaults or a consuming runtime profile
  reference.
- Read-only Craft frontier source.

### Outputs

- Bound source authority or source-authority block.
- Frontier snapshot.
- Risk classification per node.
- Goal Loop Result with no source mutation.

### Ordered Rules

1. Bind exactly one source authority.
2. If source authority is ambiguous, return `source-authority` stop.
3. Read frontier in read-only mode.
4. Classify every node.
5. Assign unknown work to protected tier.
6. Stop before route or mutation for protected work.
7. Emit Goal Loop Result with frontier counts, risk counts, stop reason, and
   telemetry state.

### Edge Cases And Failure Modes

- Empty frontier: return pass/stop without inventing work unless gap discovery
  is enabled in a later layer.
- Unreadable frontier: block with source authority or read failure.
- Filled profile unavailable: use neutral defaults and remain fail-closed.
- Protected operation found: stop before dispatch.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GOAL-003 | Implement or specify goal bind and frontier read skeleton. | SWU-GOAL-001 | future runtime source contract or implementation files selected by Spellcraft | Bound scope or block; frontier snapshot shape available. | Read-only fixture or dry-run result. | Frontier snapshot schema parse plus source-authority review. | task-session | Use neutral defaults; no source mutation. |
| SWU-GOAL-004 | Implement or specify risk classification and non-mutating result output. | SWU-GOAL-003 | future runtime source contract or implementation files selected by Spellcraft | Unknown/protected work stops; Goal Loop Result emitted. | T3 stop case and no-mutation evidence. | Goal loop result schema parse plus protected-operation scenario. | task-session | Preserve fail-closed behavior before dispatch exists. |

## Expected Result Shape

```yaml
swu_id: SWU-GOAL-003
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage
receipt_artifact: <path or none>
files_touched:
  - <path>
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

- SWU-GOAL-004 cannot start until SWU-GOAL-003 defines frontier shape.
- Any new schema need routes back through Spellcraft or a plan refresh.

## Completion Evidence

Pending.
