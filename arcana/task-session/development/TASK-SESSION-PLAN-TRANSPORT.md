# Task Session Plan Transport

## Stage

- Spell: `invoke`
- Mode: `plan`
- Target: `task-session`
- Date: 2026-05-23

## Produced Or Updated Artifacts

- Updated `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Added `arcana/task-session/development/TASK-SESSION-IMPLEMENTATION-LAYERING.md`

## Reuse Decision

The existing `CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md` already contained the correct implementation SWUs. This plan run reused and normalized that work-pack instead of creating a redundant `TASK-SESSION-WORK-PACK.md`.

## Source Contracts

- `TASK-SESSION-DEFINE.md`
- `TASK-SESSION-GLOSSARY.md`
- `TASK-SESSION-ARCHITECTURE-DESIGN.md`
- `TASK-SESSION-GLOSSARY-CONSISTENCY.md`
- `TASK-SESSION-DESIGN-TRANSPORT.md`
- `CONTEXT-PACK-GOAL-HANDOFF-OPTIMIZATION.md`
- `CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`

## Template And Profile Selection

- Implementation layering companion: `TASK-SESSION-IMPLEMENTATION-LAYERING.md`
- Work-pack companion: reused `CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Execution-pack: deferred; single-file work-pack is sufficient for this medium bounded slice because the six SWUs are ordered and layer-mapped in the canonical work-pack.

## Complexity

Complexity: `medium`

Reason: implementation spans multiple capability contracts and runtime handoff behavior, but it remains a bounded slice with six SWUs and no source-code migration.

## Layer Coverage

| Layer | Status | Evidence |
| --- | --- | --- |
| L0 | planned | SWU-CTX-GOAL-001 defines handoff schema. |
| L1 | planned | SWU-CTX-GOAL-002 adds Context Builder output mode. |
| L2 | planned | SWU-CTX-GOAL-003 through SWU-CTX-GOAL-005 wire Task Session, profile, and adapter consumption. |
| L3 | planned | SWU-CTX-GOAL-006 updates Invoke work-pack readiness guidance. |

## Handoff Readiness

Status: `pass_for_first_swu`

The plan is execution-ready for `SWU-CTX-GOAL-001`. The remaining definition decisions are locked: session-evidence persistence, strict coverage, and Markdown plus JSON/index output. Later SWUs depend on schema implementation and should be run in order unless a Task Session verifies the dependency is already satisfied.

## Next Route

Use Task Session for one SWU at a time.

Recommended first command:

```text
/task-session to arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md --swu SWU-CTX-GOAL-001 --runtime codex --via goal
```
