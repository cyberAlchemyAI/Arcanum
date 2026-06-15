# S10 Final Interrogation And Synthesis

## Final Interrogation

- Mode: refine-final.
- Verdict: pass.
- Remaining blocker ambiguity: none.
- Remaining non-blocking residue: CLI naming and direct apply mode remain deferred.

## Final Synthesis

Craft should create a deterministic row update planner, but not a direct row
mutator and not necessarily a public CLI in the first slice.

The useful primitive is:

```text
ledger + schema + row selector + proposed delta + expected hash
  -> pass | flag | block
  -> deterministic patch plan or no-op/block report
```

This primitive should be fixture-proven before `import-csv --dry-run` grows
writeback behavior. CSV import should call the row-update planner for each
normalized CSV delta instead of owning reconciliation semantics itself.

## Final Verdict

Pass.

## Recommended Next Route

Run a bounded `task-session` or Codex goal for `SWU-CRU-001`: add the row update
planner contract and public-safe toy fixture. Do not implement direct YAML
mutation in that route.
