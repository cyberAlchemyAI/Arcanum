# Stage 9: Invoke Plan

## Verdict

`pass`

## Non-Executed Implementation Plan

### 1. Add Shared Runtime Runner

Create:

```text
tools/arcanum-runtime-run
framework/runtime/
framework/runtime/README.md
framework/runtime/templates/runtime-handoff.md
framework/runtime/development/fixtures/
```

V1 adapters:

- `dry-run`
- `codex-exec`

### 2. Define Durable Run Schema

Add templates or documented schemas for:

- `RUN.json`
- `STATUS.json`
- `events.jsonl`
- `HANDOFF.md`
- `RESULT.md`

### 3. Route `tools/arcanum --exec`

Modify `tools/arcanum --exec` so it:

1. resolves the command,
2. creates a generated runtime handoff,
3. calls `tools/arcanum-runtime-run --adapter codex-exec`,
4. copies or links runtime `RESULT.md` to `--output`,
5. preserves the existing observer envelope.

### 4. Update Refine

Update refine docs/templates/fixtures/validation:

- replace `GOAL-HANDOFF.md` with `RUNTIME-HANDOFF.md`,
- replace `codex-goal` context-builder handoff language with generic runtime handoff language,
- require runtime run evidence for command-backed stages,
- preserve the canonical ten-stage loop.

### 5. Update Task Session

Replace `codex-goal` as the canonical adapter with generic runtime handoff:

```text
task-session -> runtime handoff -> runtime runner -> adapter
```

Keep the old Codex Goal material only as historical/deprecated until migrated.

### 6. Validate

Add fixture checks:

- runtime dry-run creates complete run folder,
- codex-exec uses isolated per-run state,
- refine fixture requires `RUNTIME-HANDOFF.md`,
- no required refine runtime path depends on `/goal`,
- non-blocked stage rows include runtime run ids and adapter evidence.

## First Working Slice

Build `tools/arcanum-runtime-run` with `dry-run` first, then wire `tools/arcanum --exec` to the runner behind a feature flag or compatibility path. After that, update refine validation to consume runtime evidence.
