# Task CRAFT-RUNTIME-004: Sync Craft Runtime State

## Objective

Synchronize Craft package state after command-surface smoke passes.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L3 |
| Slice | S-RUNTIME-004 |
| Wave | W3 |
| Complexity | low |
| Status | completed |

## Source Contracts

- `development/craft/CRAFT-RUNTIME-WORK-PACK.md`
- task-session evidence from CRAFT-RUNTIME-001 through CRAFT-RUNTIME-003
- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- `development/craft/CRAFT-VALIDATION.md`

## Dependencies

- CRAFT-RUNTIME-003 must pass.

## Smallest Working Units

### SWU-CRAFT-RUNTIME-004

Goal: update Craft state to name the next validation route.

Write scope:

- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- `development/craft/CRAFT-RUNTIME-WORK-PACK.md`
- Task-session evidence folder.

Done criteria:

- README and session ledger say the command-surface blocker is cleared.
- Next route is to rerun Refine validation for Craft.
- Promotion remains deferred.

Validation:

```text
rg -n "dispatch-spec|runtime-handoff|refine|promotion.*defer" development/craft/README.md development/craft/SESSION-LEDGER.md
```

Execution owner: manual.

## Completion Evidence

| Check | Result |
| --- | --- |
| README names blocker cleared | pass |
| Session ledger names blocker cleared | pass |
| Next route names Refine validation | pass: `$refine development/craft/CRAFT-VALIDATION.md --preset standard --research no` |
| Promotion remains deferred | pass |
