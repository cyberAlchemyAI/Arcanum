# TASK-GOAL-DELEGATION-STAGING

## Objective

Add the L2 behavior that makes `goal` a governed router: dispatch route
validation, delegated receipt closeout, audit, and staged-delta creation without
active source mutation.

## Layer And Slice Mapping

- Layer: L2
- Slice: S-003
- Wave: W2
- Gate status: blocked-after-W1

## Source Contracts

- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/schemas/execution-receipt.schema.json`
- `../20260620T205253Z-goal-architecture-rules-schemas-contracts/schemas/staged-delta.schema.json`
- `arcanum/formulae/dispatch-spec/dispatch.schema.yml`

## Dependencies

- SWU-GOAL-004 pass.
- Owner map and route validation surface selected.

## Blocker And Gap State

| ID | State | Handling |
| --- | --- | --- |
| G-GOAL-RUNTIME-SOURCE | open | Runtime write scope must be explicit before edits. |
| route validation failure | possible | Block and reroute to Dispatch Spec or Spellcraft. |

## Implementation Detail

### Inputs

- Routable node from risk classifier.
- Owner capability map.
- Dispatch technique selection.
- Done criteria for the node.

### Outputs

- Dispatch route.
- Terminal execution receipt.
- Audit verdict.
- Staged delta for source-changing progress.

### Ordered Rules

1. Accept only nodes classified as eligible for routing.
2. Build a dispatch route with owner, technique, inputs, receipt fields, gate,
   and fallback.
3. Validate the route shape before delegation.
4. Join delegated receipt; open lanes cannot synthesize as success.
5. Audit receipt against done criteria.
6. Let veto override apparent success.
7. For source-changing progress, emit staged delta with framed diff and
   validation expectation.
8. Do not apply staged deltas.

### Edge Cases And Failure Modes

- No owner fits: block with invalid route.
- Owner returns partial or open result: block with residue and reroute.
- Audit evidence is weak: block or flag according to severity.
- Delta lacks framed diff: block staging.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GOAL-005 | Implement or specify dispatch route adapter and terminal receipt validation. | SWU-GOAL-004 | future runtime route adapter and receipt checks selected by Spellcraft | Route validates; receipt closes terminally. | Valid dispatch route and receipt artifact. | dispatch-spec validator plus receipt shape review. | task-session | Do not redefine owner internals. |
| SWU-GOAL-006 | Implement or specify audit gate and staged-delta creation. | SWU-GOAL-005 | future audit/staging implementation selected by Spellcraft | Audit verdict recorded; source-changing progress stages only. | Audit verdict and staged delta artifact. | staged delta schema parse plus no-active-mutation review. | task-session | Veto overrides success; staged delta is not applied. |

## Expected Result Shape

```yaml
swu_id: SWU-GOAL-005
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

- SWU-GOAL-006 cannot start until SWU-GOAL-005 defines receipt shape.
- Any active source mutation attempt becomes a block or staged proposal.

## Completion Evidence

Pending.
