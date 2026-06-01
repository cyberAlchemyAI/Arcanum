# Durable Arcanum Runtime Interface: Refined Implementation Handoff

## Summary

Arcanum should add a generic durable runtime layer shared by refine, task-session, and future orchestrators. Refine and task-session should no longer depend on Codex Goal or native `/goal`; Codex should be one adapter behind a generic executor.

The canonical model is:

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor
```

The refinement run also proved the current problem: `tools/arcanum --exec` reached Codex CLI but failed before producing a stage artifact, while observer evidence was recorded. The missing piece is a durable runtime run folder that can represent adapter failure, preserve status, and support retry/resume without conflating Arcanum orchestration with Codex state.

## Proposed Runtime Architecture

- **Orchestrator**: owns intent, loop/stage topology, budgets, and final synthesis.
- **Async task handoff**: immutable request artifact with objective, inputs, scope, expected outputs, validation, adapter preference, and blocked conditions.
- **Runtime translator**: turns the generic handoff into adapter-specific execution input.
- **Runtime executor**: creates durable run state, invokes adapter, writes status/events/result, and records failure/block evidence.

New shared command:

```bash
tools/arcanum-runtime-run --handoff <handoff-path> --run-dir <run-dir> --adapter <adapter-id>
```

`tools/arcanum --exec` should become a compatibility wrapper that resolves the Arcanum command, generates a runtime handoff, and delegates to `tools/arcanum-runtime-run`.

## Durable Run Folder Contract

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

`RUN.json` identifies the run:

- run id,
- parent run id,
- orchestrator id,
- adapter id,
- target command or skill,
- handoff path,
- result path,
- artifacts directory,
- children directory.

`STATUS.json` records:

- `queued`, `running`, `passed`, `flagged`, `blocked`, or `failed`,
- adapter status,
- output paths,
- blocked reason,
- started/completed timestamps.

`events.jsonl` records lifecycle events and adapter events.

`HANDOFF.md` is immutable intent. Runtime status must not be written back into the handoff.

## Refine Integration

Refine keeps its target-local run folder but replaces `GOAL-HANDOFF.md` with `RUNTIME-HANDOFF.md`:

```text
<target>/development/refinement-runs/<run-id>/
  RUN-MANIFEST.md
  evidence-index.json
  REFINE-SEED-PROPOSAL.md
  RUNTIME-HANDOFF.md
  RESULT.md
  stages/
```

Refine owns:

- seed proposal,
- canonical loop topology,
- research decision,
- stage manifest,
- evidence index,
- final synthesis.

Runtime owns:

- execution status,
- adapter invocation,
- logs/events,
- adapter result capture,
- adapter blocked/failure reason.

Every command-backed refine stage should reference a runtime child run id and its output artifact.

## Task-Session Integration

Task-session should use the same runtime contract:

```text
task-session -> RUNTIME-HANDOFF.md -> tools/arcanum-runtime-run -> adapter
```

Task-session still owns:

- selected task/SWU,
- dependency state,
- context pack,
- write scope,
- done criteria,
- validation surface,
- work-pack synchronization.

The runtime owns execution and adapter evidence. The current `codex-goal` adapter should be replaced by a generic runtime adapter contract. Native `/goal` material can remain as historical/deprecated until cleaned up.

## Multiple-Loop Model

A single refinement loop is a parent run with stage child runs:

```text
refine-run/
  children/
    01-context-builder/
    02-invoke-define/
    03-interrogation-refine-review/
    04-research-decision/
    05-distill/
    06-invoke-design/
    07-interrogation-design-review/
    08-distill-repair/
    09-invoke-plan/
    10-final-interrogation/
```

Multiple loops use explicit topology:

- `candidate`: sibling loops for different structure/template candidates,
- `nested`: child loop for a sub-object discovered during a parent loop,
- `repair`: bounded loop for a named failed verdict,
- `continuation`: resumed loop using existing durable status.

Do not merge multiple loops into one prose artifact. Compare loops through manifests and evidence indexes.

## Adapter Model

First adapters:

- `dry-run`: validates handoff, creates run state, writes synthetic result.
- `codex-exec`: runs Codex CLI through `codex exec`.

Codex adapter boundaries:

- must not use native `/goal`,
- must not own Arcanum orchestration,
- must not share `.arcanum/codex-home` across runtime runs,
- must create isolated per-run adapter state,
- must record backend/network/runtime failures as adapter evidence,
- must write or link output to `RESULT.md`.

## Validation Plan

Validation should require:

- `RUNTIME-HANDOFF.md`, not `GOAL-HANDOFF.md`, in active refine artifacts.
- No required refine runtime path depends on `/goal` or Codex Goal state.
- Every non-blocked runtime-backed stage has:
  - runtime run id,
  - adapter id,
  - command or skill target,
  - resolved command file when command-backed,
  - output artifact path,
  - status/verdict.
- Blocked stages have exact missing field or adapter reason.
- Codex adapter uses isolated per-run state.
- Nested runs include parent/child ids.
- Multiple candidate loops are represented as separate runtime run folders.

Validation commands after implementation:

```bash
tools/arcanum --resolve refine
tools/arcanum --resolve context-builder
tools/arcanum --resolve invoke
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
tools/arcanum-runtime-run --handoff <fixture>/HANDOFF.md --run-dir <fixture-run> --adapter dry-run
tools/arcanum-runtime-run --handoff <fixture>/HANDOFF.md --run-dir <fixture-run> --adapter codex-exec
arcana/refine/development/run-validation-fixtures.sh
```

## First Implementation Slice

1. Add `tools/arcanum-runtime-run`.
2. Add `framework/runtime/` docs, templates, and fixtures.
3. Implement `dry-run` adapter first.
4. Implement `codex-exec` adapter with isolated per-run `CODEX_HOME`.
5. Route `tools/arcanum --exec` through the runtime runner.
6. Update refine active docs/templates/fixtures/validation from `GOAL-HANDOFF.md` to `RUNTIME-HANDOFF.md`.
7. Update task-session active adapter boundary from `codex-goal` to generic runtime handoff.
8. Keep old Codex Goal/Profile development history as deprecated/historical unless active validation consumes it.

## Open Decisions

No blocking design decisions remain.

Recommended names:

- command: `tools/arcanum-runtime-run`
- refine artifact: `RUNTIME-HANDOFF.md`
- first Codex adapter: `codex-exec`
- durable run root: `.arcanum/runtime/runs/<run-id>/`
