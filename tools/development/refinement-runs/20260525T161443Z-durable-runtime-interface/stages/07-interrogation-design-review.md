# Stage 7: Interrogation Design Review

## Verdict

`flag`

## Review Findings

The design is implementable, but three details must be tightened before planning:

1. `RUNTIME-HANDOFF.md` must not become an execution log.
2. Runtime folders and refine folders must not duplicate each other's authority.
3. The first slice must avoid updating every historical Codex Goal document at once.

## Required Corrections

### Handoff Boundary

`RUNTIME-HANDOFF.md` is immutable intent for a run. It should not be edited with live status. Status belongs in `STATUS.json` and `events.jsonl`.

### Folder Authority

Runtime folder owns execution truth:

- process status,
- adapter status,
- events,
- adapter logs,
- result capture.

Refine folder owns loop truth:

- stage order,
- seed proposal,
- research decision,
- stage verdict index,
- final synthesis.

### Rollout Boundary

The first implementation slice should update active refine/task-session runtime paths and validation, while leaving old development history as historical unless active validation consumes it.

## Pass Condition

Plan may proceed if the implementation explicitly preserves this authority split.
