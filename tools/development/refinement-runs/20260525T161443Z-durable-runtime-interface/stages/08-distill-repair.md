# Stage 8: Distill Repair

## Verdict

`pass`

## Repair Applied

The design is repaired by separating immutable handoff, runtime status, and orchestrator manifest.

## Repaired Contract

### Async Task Handoff

File: `RUNTIME-HANDOFF.md`

Purpose: intent, scope, adapter preference, input context, expected outputs, validation, blocked conditions.

Mutation rule: create once per run request; do not mutate for status.

### Runtime Run State

Files:

- `RUN.json`
- `STATUS.json`
- `events.jsonl`
- `RESULT.md`
- `artifacts/`

Purpose: execution state and evidence.

Mutation rule: executor-owned.

### Orchestrator Manifest

Files:

- refine `RUN-MANIFEST.md`
- refine `evidence-index.json`

Purpose: stage topology, child run references, verdicts, and synthesis inputs.

Mutation rule: orchestrator-owned.

## Minimal First Slice

The first slice should introduce the runtime runner and update refine to depend on runtime evidence. Task-session can be updated to consume the same contract in the same slice only at documentation/adapter boundary level, with deeper task-session execution migration as a follow-up.
