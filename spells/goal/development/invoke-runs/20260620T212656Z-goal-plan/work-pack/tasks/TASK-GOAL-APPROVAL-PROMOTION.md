# TASK-GOAL-APPROVAL-PROMOTION

## Objective

Add L3 protected operation behavior: batch-specific approval token handling,
durable decision linkage, Craft apply boundary, gap discovery termination, and
proportionality control.

## Layer And Slice Mapping

- Layer: L3
- Slice: S-004
- Wave: W3
- Gate status: blocked-after-W2

## Source Contracts

- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/schemas/approval-token.schema.json`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/schemas/telemetry-signal.schema.json`
- `arcanum/spells/goal/README.md` Gap Discovery and Proportionality Guard
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md`

## Dependencies

- SWU-GOAL-006 pass.
- Decision Gate and Craft apply boundaries remain explicit.

## Blocker And Gap State

| ID | State | Handling |
| --- | --- | --- |
| approval-token missing | possible | Hold batch; route to decision-gate. |
| gap loop | possible | Stop at budget or dedupe violation. |

## Implementation Detail

### Inputs

- Staged batch.
- Approval token or approval request.
- Decision record reference.
- Empty frontier signal for gap discovery.
- Budget counters and configured ceilings.

### Outputs

- Approved, rejected, held, or blocked batch state.
- Craft apply request only when approved.
- Gap proposals or no-new-gap result.
- Budget stop or down-route evidence.

### Ordered Rules

1. Group staged deltas into a batch.
2. Require batch-specific approval token before apply.
3. Require durable decision record link.
4. Reject ambient approval for unrelated operations.
5. Apply only through Craft source owner after approval.
6. Run gap discovery only after active frontier is empty and module is enabled.
7. Deduplicate gaps by `(kind, target)`.
8. Stop before budget ceiling.
9. Emit telemetry or explicit skipped reason.

### Edge Cases And Failure Modes

- Approval token scope mismatch: block.
- Partial apply risk: block.
- Gap discovery produces duplicates: flag or block.
- Budget ceiling reached: stop with budget reason.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GOAL-007 | Implement or specify approval token and Craft apply boundary. | SWU-GOAL-006 | future approval/apply boundary selected by Spellcraft | Batch apply requires exact approval token and durable decision record. | Approval scenario plus ambient-approval rejection. | approval-token schema parse plus decision-record link review. | task-session | Do not treat approval as ambient authority. |
| SWU-GOAL-008 | Implement or specify gap discovery and proportionality guard. | SWU-GOAL-007 | future gap/budget module selected by Spellcraft | Gap discovery waits for empty frontier and terminates by dedupe/budget. | Gap termination and budget stop evidence. | reviewable fixture or Experiment Harness scenario. | task-session | Gap discovery queues proposals; it does not reopen active frontier. |

## Expected Result Shape

```yaml
swu_id: SWU-GOAL-007
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

- SWU-GOAL-008 cannot start until approval boundary is explicit.
- Any Craft apply behavior must cite the owning Craft validation path.

## Completion Evidence

Pending.
