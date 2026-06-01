# Stage 6: Invoke Redefine / Design

## Verdict

`pass`

## Refined Architecture

```text
Arcanum Orchestrator
  writes RUNTIME-HANDOFF.md
  indexes run in orchestrator manifest
  calls tools/arcanum-runtime-run

Runtime Runner
  creates .arcanum/runtime/runs/<run-id>/
  writes RUN.json
  writes STATUS.json
  appends events.jsonl
  delegates to translator + adapter
  writes RESULT.md

Adapter
  receives adapter-specific request
  executes or blocks
  returns result metadata
```

## Two-Folder Model

### Orchestrator Folder

Owned by refine or task-session.

Example:

```text
tools/development/refinement-runs/<run-id>/
  RUN-MANIFEST.md
  evidence-index.json
  REFINE-SEED-PROPOSAL.md
  RUNTIME-HANDOFF.md
  RESULT.md
  stages/
```

Purpose: human-facing workflow evidence and synthesis.

### Runtime Folder

Owned by the runtime executor.

Example:

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

Purpose: machine-readable execution state and adapter evidence.

## Runtime Handoff Contract

Required fields:

- `objective`
- `orchestrator_id`
- `orchestrator_run_id`
- `target_kind`
- `target_id`
- `input_artifacts`
- `allowed_write_scope`
- `expected_outputs`
- `validation`
- `blocked_conditions`
- `adapter_preference`
- `nesting_policy`
- `parent_runtime_run_id`

## Loop Topology

Each runtime run can declare:

- `loop_role`: `root`, `stage`, `candidate`, `nested`, `repair`, `continuation`
- `loop_id`
- `parent_loop_id`
- `stage_number`
- `stage_name`

## Adapter Contract

An adapter must return:

- `adapter_id`
- `status`
- `output_paths`
- `events`
- `blocked_reason`
- `exit_code` when process-backed
- `state_path` when it creates adapter-local state

## Codex Adapter

`codex-exec` should:

- create per-run `CODEX_HOME`,
- symlink stable auth/config only,
- run `codex exec`,
- write last message to runtime `RESULT.md`,
- copy/link result to requested orchestrator output when needed,
- record network/backend/runtime failures in `STATUS.json`.

It must not:

- call native `/goal`,
- rely on shared `.arcanum/codex-home`,
- decide refine stage order,
- mutate orchestrator manifests directly.
