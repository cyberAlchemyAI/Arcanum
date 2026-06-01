# Stage 2: Invoke Define

## Verdict

`pass`

## Defined Problem

Arcanum currently has orchestration skills that want to delegate work, but the delegation model is split between:

- refine's canonical loop and target-local evidence model,
- task-session's bounded SWU/task execution model,
- Codex Goal/Profile terminology,
- `tools/arcanum --exec` as a direct Codex CLI launcher.

This creates an architectural leak: Codex is treated as the runtime identity instead of an adapter. When Codex execution fails, there is no generic durable run folder that can represent queued/running/blocked/failed state independently from Codex.

## Desired Runtime Identity

Arcanum needs a generic durable runtime interface:

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor
```

Definitions:

- **orchestrator**: decides what should happen and in what loop/stage order.
- **async task handoff**: durable request contract that can be executed now, later, or by another adapter.
- **runtime translator**: converts generic handoff into adapter-specific input.
- **runtime executor**: creates the run, invokes the adapter, records status, writes events, and captures artifacts.

## Core Requirement

The runtime must be able to execute one stage, one full refine loop, multiple candidate loops, nested loops, and repair loops without depending on native `/goal`.

## Non-Goals

- Do not recreate native Codex Goal.
- Do not make Task Session or Sigil Development stages inside refine.
- Do not make Codex the canonical runtime model.
- Do not require a scheduler in the first slice.

## Success Criteria

- Refine can create `RUNTIME-HANDOFF.md` instead of `GOAL-HANDOFF.md`.
- Task-session can hand off a selected task/SWU to the same runtime.
- Every non-blocked runtime-backed stage records run id, adapter id, command, resolved file, output artifact, status, and verdict.
- Adapter failure is represented as `blocked` or `failed` with exact reason and retained evidence.
