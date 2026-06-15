# S05 Distill: Row-Writeback Strategy

## Distill Result

- Target context: Craft ledger projection writeback.
- Objective and output artifact: select smallest coherent row update unit and produce a plan-ready recommendation.
- Mode and budget: compact.
- Proposal tracks: 3 route-menu alternatives reviewed.
- Recursive rounds: 1 / 1.
- Verdict: pass.
- Current smallest coherent unit: `row_update_plan`.
- Next route: invoke design.

## Route Menu Evaluation

| Option | Result | Reason |
| --- | --- | --- |
| No new tool | rejected | Leaves safety-critical reconciliation buried inside CSV import. |
| Dedicated row updater | selected | Smallest testable unit that can recompose into CSV import and other future edit sources. |
| Broad import first | rejected | Couples parsing, reconciliation, validation, and reporting too early. |

## Smallest Coherent Unit

`row_update_plan`:

```text
Input:
  ledger bytes
  schema contract
  row selector: family + row id
  proposed field deltas
  expected ledger hash

Output:
  verdict: pass | flag | block
  no-op status when applicable
  deterministic patch operations
  blocker reasons
  validation evidence
```

## Closure And Recomposition Proof

The unit closes because it can be tested without CSV parsing and without YAML
mutation. It recomposes upward because `import-csv --dry-run` can produce many
row deltas and call the same planner for each row.

## Deferred Complexity

- Multi-row transaction planning.
- Direct YAML apply mode.
- Arbitrary nested object edits.
- User-facing CLI command.
- Generated projection commit policy.

## Frame Expiry Note

This optimization expires if Craft chooses to make generated projections
authoritative, or if the ledger schema moves away from stable row families and
IDs. Current Craft evidence says the opposite.
