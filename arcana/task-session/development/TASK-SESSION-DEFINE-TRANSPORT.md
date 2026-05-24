# Task Session Define Transport

## Stage

- Spell: `invoke`
- Mode: `define`
- Target: `task-session`
- Date: 2026-05-23

## Produced Artifacts

- `arcana/task-session/development/TASK-SESSION-DEFINE.md`
- `arcana/task-session/development/TASK-SESSION-GLOSSARY.md`

## Source Evidence

- `arcana/task-session/README.md`
- `arcana/task-session/SKILL.md`
- `arcana/task-session/runtime-adapters/README.md`
- `arcana/task-session/runtime-adapters/codex-goal.md`
- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-OPTIMIZATION.md`
- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`
- `arcana/task-session/development/TASK-SESSION-ARCHITECTURE-DESIGN.md`

## Template Selection

No dedicated Task Session define template exists. This run used the generic invoke define contract and produced a compact sigil definition baseline plus glossary.

## Decisions

- Treat Task Session as a sigil-level execution coordinator, not a runtime implementation.
- Treat Context Builder output as the execution boundary before gates, mutation, or runtime handoff.
- Treat generated context packs as session evidence rather than canonical planning documents.
- Treat Codex Goal handoff packs as Markdown plus JSON/index session evidence with strict coverage.
- Treat native Codex Goal as an optional runtime adapter target, not the identity of Task Session.

## Gaps

- No Necronomicon transport target was updated.
- Implementation-layering and work-pack companions now exist in the Task Session development folder.
- Execution implementation still needs to apply the locked handoff-pack policy across the canonical contracts.

## Recommended Next Route

Run `invoke plan` for `arcana/task-session` to normalize implementation SWUs against:

- `TASK-SESSION-DEFINE.md`,
- `TASK-SESSION-GLOSSARY.md`,
- `TASK-SESSION-ARCHITECTURE-DESIGN.md`,
- `CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`.
