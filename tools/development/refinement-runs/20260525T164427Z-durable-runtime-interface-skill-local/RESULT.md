# Durable Arcanum Runtime Interface: Local Skill Refined Handoff

## Summary

This pass reran the refinement loop locally from the current Codex session instead of using `tools/arcanum --exec`. The result confirms the same direction as the command-backed pass, but sharpens the runtime model:

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor -> adapter
```

Codex is not the runtime model. Codex is one adapter, `codex-exec`, behind a generic durable executor.

## Proposed Runtime Architecture

Arcanum should introduce a shared durable runtime package and runner.

The orchestrator owns workflow meaning:

- refine owns loop topology, seed, stage manifest, evidence index, and final synthesis.
- task-session owns selected task/SWU, gates, context pack, done criteria, validation, and work-pack sync.

The runtime owns execution mechanics:

- run folder creation,
- status,
- events,
- adapter invocation,
- adapter-local state,
- result capture,
- blocked/failure evidence.

The adapter owns only concrete execution.

## Durable Run Folder Contract

Runtime-owned folder:

```text
.arcanum/runtime/runs/<runtime-run-id>/
  RUN.json
  HANDOFF.md
  STATUS.json
  RESULT.md
  events.jsonl
  artifacts/
  children/
```

Required `RUN.json` concepts:

- `run_id`
- `parent_run_id`
- `orchestrator_id`
- `orchestrator_run_id`
- `adapter_id`
- `target_kind`
- `target_id`
- `loop_role`
- `loop_id`
- `parent_loop_id`
- `stage_number`
- `stage_name`
- `handoff_path`
- `result_path`

Required `STATUS.json` concepts:

- `status`: `queued`, `running`, `passed`, `flagged`, `blocked`, or `failed`
- `adapter_status`
- `output_paths`
- `blocked_reason`
- `started_at`
- `completed_at`

`HANDOFF.md` is immutable run intent. Runtime status belongs in `STATUS.json` and `events.jsonl`.

## Refine Integration

Refine should replace:

```text
GOAL-HANDOFF.md
```

with:

```text
RUNTIME-HANDOFF.md
```

Target-local refine folder:

```text
<target>/development/refinement-runs/<run-id>/
  RUN-MANIFEST.md
  evidence-index.json
  REFINE-SEED-PROPOSAL.md
  RUNTIME-HANDOFF.md
  RESULT.md
  stages/
```

Each command-backed stage should reference a runtime child run:

- runtime run id,
- adapter id,
- command/skill target,
- resolved command file when applicable,
- output artifact,
- verdict,
- blocked reason when applicable.

Refine should never depend on native `/goal` to prove execution.

## Task-Session Integration

Task-session should stop using `codex-goal` as its canonical runtime path.

Replace:

```text
task-session -> codex-goal adapter -> native /goal
```

with:

```text
task-session -> RUNTIME-HANDOFF.md -> tools/arcanum-runtime-run -> adapter
```

Task-session still owns selection and safety. Runtime owns execution evidence.

Add:

```text
arcana/task-session/runtime-adapters/runtime-handoff.md
```

Then deprecate the current `codex-goal.md` adapter as legacy/historical.

## Multiple-Loop Model

A refine loop is a parent orchestrator run with stage child runs.

Each runtime run should declare:

- `loop_role`: `root`, `stage`, `candidate`, `nested`, `repair`, or `continuation`
- `loop_id`
- `parent_loop_id`
- `stage_number`
- `stage_name`

Use cases:

- **candidate loops**: sibling loops for different template/design structures.
- **nested loops**: child loops for sub-objects discovered during a larger refinement.
- **repair loops**: bounded loops for named failed interrogation/distill verdicts.
- **continuation loops**: resumed loops using existing durable status.

This keeps multiple loops inspectable without turning `RESULT.md` into a tangled mega-report.

## Adapter Model

V1 adapters:

- `dry-run`
- `codex-exec`

`dry-run` validates the handoff and creates complete run artifacts without external execution.

`codex-exec` runs Codex CLI through `codex exec`.

Codex adapter rules:

- no native `/goal`,
- no shared `.arcanum/codex-home` for runtime runs,
- create per-run adapter state,
- symlink only stable auth/config from source Codex home,
- record backend/network/runtime failures in `STATUS.json`,
- write final output to runtime `RESULT.md`,
- never mutate orchestrator manifests directly.

## Validation Plan

Required validation:

- `RUNTIME-HANDOFF.md` exists in active refine run folders.
- `GOAL-HANDOFF.md` is not required by active refine validation.
- every non-blocked runtime-backed stage has runtime run evidence.
- every blocked stage has exact blocked reason.
- runtime `RUN.json` and `STATUS.json` are valid JSON.
- `codex-exec` creates isolated per-run state.
- nested runs preserve parent/child ids.
- candidate loops are separate sibling runs, not merged prose.

Validation commands:

```bash
tools/arcanum-runtime-run --adapter dry-run --handoff <fixture>/RUNTIME-HANDOFF.md --run-dir <tmp-run>
jq empty <tmp-run>/RUN.json
jq empty <tmp-run>/STATUS.json
tools/arcanum --resolve refine
tools/arcanum --resolve context-builder
tools/arcanum --resolve invoke
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
arcana/refine/development/run-validation-fixtures.sh
```

Stale active-language check:

```bash
rg -n "GOAL-HANDOFF|Codex Goal|codex-goal|/goal" arcana/refine .codex/commands/refine.md
```

Historical paths may need explicit exceptions.

## First Implementation Slice

1. Add `framework/runtime/` with schema docs and templates.
2. Add `tools/arcanum-runtime-run`.
3. Implement `dry-run` adapter.
4. Add dry-run fixtures and JSON validation.
5. Implement `codex-exec` with isolated per-run `CODEX_HOME`.
6. Route `tools/arcanum --exec` to runtime runner behind `ARCANUM_RUNTIME_RUNNER=1`.
7. Update refine active docs/templates/fixtures to use `RUNTIME-HANDOFF.md`.
8. Update task-session active runtime adapter boundary to generic runtime handoff.
9. Make runtime runner the default `tools/arcanum --exec` path after fixtures pass.

## Open Decisions

No blocking decisions remain.

Recommended names:

- runner: `tools/arcanum-runtime-run`
- refine handoff: `RUNTIME-HANDOFF.md`
- runtime root: `.arcanum/runtime/runs/<runtime-run-id>/`
- first Codex adapter: `codex-exec`
