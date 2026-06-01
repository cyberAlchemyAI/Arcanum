# Task CRAFT-RUNTIME-003: Command Surface Smoke

## Objective

Prove the command-surface blocker is cleared enough for Craft to retry Refine validation.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L2 |
| Slice | S-RUNTIME-003 |
| Wave | W2 |
| Complexity | low |
| Status | completed |

## Source Contracts

- `development/craft/refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `.codex/commands/dispatch-spec.md`
- `.codex/commands/runtime-handoff.md`

## Dependencies

- CRAFT-RUNTIME-001 must pass.
- CRAFT-RUNTIME-002 must pass.

## Smallest Working Units

### SWU-CRAFT-RUNTIME-003

Goal: run command-surface smoke validation.

Write scope:

- Task-session evidence folder only.

Done criteria:

- `dispatch-spec` resolves.
- `runtime-handoff` resolves.
- Craft Refine dispatch validates.

Validation:

```text
tools/arcanum --resolve dispatch-spec
tools/arcanum --resolve runtime-handoff
python3 formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json
```

Execution owner: manual.

## Completion Evidence

| Check | Result |
| --- | --- |
| `tools/arcanum --resolve dispatch-spec` | pass: `COMMAND_FILE=.codex/commands/dispatch-spec.md` |
| `tools/arcanum --resolve runtime-handoff` | pass: `COMMAND_FILE=.codex/commands/runtime-handoff.md` |
| Craft Refine dispatch validation | pass: `VALIDATION=pass` for `development/craft/refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json` |
