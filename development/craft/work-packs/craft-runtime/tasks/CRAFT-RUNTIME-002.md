# Task CRAFT-RUNTIME-002: Expose Runtime Handoff Command Route

## Objective

Add or repair the bare `runtime-handoff` command route so Refine can resolve it through `tools/arcanum`.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L1 |
| Slice | S-RUNTIME-002 |
| Wave | W1 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `arcana/task-session/runtime-adapters/runtime-handoff.md`
- `arcana/refine/templates/runtime-handoff.md`
- `.codex/commands`
- `tools/arcanum`
- `development/craft/CRAFT-RUNTIME-DESIGN.md`

## Dependencies

- CRAFT-RUNTIME-001 must pass.

## Smallest Working Units

### SWU-CRAFT-RUNTIME-002

Goal: make `tools/arcanum --resolve runtime-handoff` pass.

Write scope:

- `.codex/commands/runtime-handoff.md` or the smallest equivalent command-route file.
- Task-session evidence folder.

Implementation detail:

1. Inspect the task-session runtime-handoff adapter and Refine runtime-handoff template.
2. Create a bare command route that exposes runtime handoff validation/contract behavior.
3. Preserve that this route validates or emits handoff contracts; it does not implement every runtime adapter.
4. Do not mutate runtime adapter internals unless command-route inspection proves an alias is insufficient.

Done criteria:

- `tools/arcanum --resolve runtime-handoff` passes.
- Command file names source owner and non-adapter-implementation boundary.

Validation:

```text
tools/arcanum --resolve runtime-handoff
```

Execution owner: local-fallback.

## Completion Evidence

| Check | Result |
| --- | --- |
| Dependency `CRAFT-RUNTIME-001` | pass: `tools/arcanum --resolve dispatch-spec` resolves |
| `tools/arcanum --resolve runtime-handoff` | pass: `COMMAND_FILE=.codex/commands/runtime-handoff.md` |
| Source owner named | pass: command file cites `arcana/task-session/runtime-adapters/runtime-handoff.md` and Refine/runtime templates |
| Non-adapter-implementation boundary | pass: command file states it exposes and validates handoff contracts, not every runtime adapter |
