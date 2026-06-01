# Stage 9: Invoke Plan

## Verdict

`pass`

## Implementation Plan

### 1. Add Runtime Package

Create:

```text
framework/runtime/README.md
framework/runtime/templates/RUNTIME-HANDOFF.md
framework/runtime/templates/RUN.json
framework/runtime/templates/STATUS.json
framework/runtime/development/fixtures/dry-run/
```

### 2. Add Tools Runner

Create:

```text
tools/arcanum-runtime-run
```

Required options:

```bash
tools/arcanum-runtime-run \
  --handoff <path> \
  --run-dir <path> \
  --adapter dry-run|codex-exec
```

### 3. Implement Dry-Run Adapter

Dry-run should:

- validate handoff exists,
- create runtime folder,
- write `RUN.json`,
- write `STATUS.json`,
- write `RESULT.md`,
- append `events.jsonl`,
- never call Codex.

### 4. Implement Codex-Exec Adapter

Codex-exec should:

- create isolated runtime `CODEX_HOME`,
- symlink auth/config from source Codex home,
- run `codex exec`,
- write output to runtime `RESULT.md`,
- record adapter failure without losing status.

### 5. Route Arcanum Exec

Update `tools/arcanum --exec` to delegate to runtime runner behind a feature flag first.

### 6. Update Refine

Update active refine paths:

- `SKILL.md`
- `REFINEMENT-LOOP.md`
- README/templates/examples/fixtures
- validation scripts
- installed global refine skill

Required change:

```text
GOAL-HANDOFF.md -> RUNTIME-HANDOFF.md
codex-goal -> runtime handoff
Codex Goal -> runtime adapter
```

### 7. Update Task-Session

Add or replace adapter documentation:

```text
arcana/task-session/runtime-adapters/runtime-handoff.md
```

Deprecate `codex-goal.md` as historical or legacy.

### 8. Validate

Run:

```bash
jq empty <runtime-run>/RUN.json
jq empty <runtime-run>/STATUS.json
tools/arcanum-runtime-run --adapter dry-run --handoff <fixture>/RUNTIME-HANDOFF.md --run-dir <tmp-run>
tools/arcanum --resolve refine
tools/arcanum --resolve context-builder
tools/arcanum --resolve invoke
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
arcana/refine/development/run-validation-fixtures.sh
```

Add stale-language check for active refine paths:

```bash
rg -n "GOAL-HANDOFF|Codex Goal|codex-goal|/goal" arcana/refine .codex/commands/refine.md
```

The check may need exceptions for historical migration notes only.
