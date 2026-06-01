# Stage 6: Invoke Redefine / Design

## Verdict

`pass`

## Proposed Runtime Architecture

```text
refine/task-session/other orchestrator
  -> RUNTIME-HANDOFF.md
  -> tools/arcanum-runtime-run
  -> runtime translator
  -> adapter executor
  -> durable result/status/artifacts
```

## Durable Run Folder

```text
.arcanum/runtime/runs/<run-id>/
  RUN.json
  HANDOFF.md
  STATUS.json
  RESULT.md
  events.jsonl
  artifacts/
  children/
```

## Target-Local Refine Folder

```text
<target>/development/refinement-runs/<run-id>/
  RUN-MANIFEST.md
  evidence-index.json
  REFINE-SEED-PROPOSAL.md
  RUNTIME-HANDOFF.md
  RESULT.md
  stages/
```

Refine's target-local folder indexes the workflow. The runtime folder owns execution state. The two are linked by runtime run ids and artifact paths.

## Generic Handoff Fields

Minimum fields:

- `objective`
- `orchestrator`
- `target`
- `inputs`
- `allowed_write_scope`
- `expected_outputs`
- `validation`
- `blocked_conditions`
- `adapter_preference`
- `nesting_policy`
- `parent_run_id`

## Runtime Executor Responsibilities

- create run folder,
- write initial `RUN.json`,
- acquire run-local lock,
- call translator,
- invoke adapter,
- append `events.jsonl`,
- write `STATUS.json`,
- write or link `RESULT.md`,
- preserve adapter blocked/failure evidence.

## Codex Adapter Boundary

The first adapter is `codex-exec`.

It may:

- run `codex exec`,
- build an adapter prompt from handoff content,
- use an isolated per-run `CODEX_HOME`,
- write final output to `RESULT.md`.

It must not:

- use native `/goal`,
- own Arcanum orchestration,
- share `.arcanum/codex-home` across nested runs,
- hide backend/network/runtime failures.

## Compatibility

`tools/arcanum --exec --output <path> <command> <request>` should translate into a runtime handoff and call:

```bash
tools/arcanum-runtime-run --adapter codex-exec --handoff <generated-handoff> --run-dir <generated-run-dir>
```
