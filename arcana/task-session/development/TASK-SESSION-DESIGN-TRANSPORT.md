# Task Session Design Transport

## Stage

- Spell: `invoke`
- Mode: `design`
- Target: `task-session`
- Date: 2026-05-23

## Produced Or Updated Artifacts

- Updated `arcana/task-session/development/TASK-SESSION-ARCHITECTURE-DESIGN.md`
- Added `arcana/task-session/development/TASK-SESSION-GLOSSARY-CONSISTENCY.md`

## Source Contracts

- `arcana/task-session/development/TASK-SESSION-DEFINE.md`
- `arcana/task-session/development/TASK-SESSION-GLOSSARY.md`
- `arcana/task-session/SKILL.md`
- `arcana/task-session/README.md`
- `arcana/task-session/runtime-adapters/README.md`
- `arcana/task-session/runtime-adapters/codex-goal.md`
- `transmutations/context-builder/SKILL.md`
- `transmutations/codex-goal-profile/SKILL.md`
- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`

## Template And Profile Selection

- Selected profile: architecture design bundle with six required invoke design views.
- Companion evidence: existing context-pack goal handoff design.
- Glossary check: `TASK-SESSION-GLOSSARY-CONSISTENCY.md`.

## Six-View Coverage

| View | Artifact | Status |
| --- | --- | --- |
| Context view | `TASK-SESSION-ARCHITECTURE-DESIGN.md` | pass |
| High-level structure view | `TASK-SESSION-ARCHITECTURE-DESIGN.md` | pass |
| Low-level components view | `TASK-SESSION-ARCHITECTURE-DESIGN.md` | pass |
| Workflow process view | `TASK-SESSION-ARCHITECTURE-DESIGN.md` | pass |
| Decision flow view | `TASK-SESSION-ARCHITECTURE-DESIGN.md` | pass |
| Dependency interface view | `TASK-SESSION-ARCHITECTURE-DESIGN.md` | pass |

## Design Decisions

- Preserve Task Session as the coordinator for one bounded execution unit.
- Use Context Builder output as the architectural boundary before gates and execution.
- Persist runtime handoff packs as session evidence with Markdown plus JSON/index.
- Require strict coverage before Codex Goal handoff.
- Treat runtime delegation as adapter-bound and optional.
- Require evidence-backed synchronization after validation.
- Preserve `context pack` vs `handoff pack` as distinct terms.

## Risks

- Context Builder, Codex Goal Profile, and Codex Goal adapter contracts must change together or the pack-first architecture will only be documented, not enforced.
- Saved handoff packs need provenance/staleness controls and strict coverage before they can be trusted during longer-running sessions.
- Plan tasks should avoid turning the design into one broad implementation task; the affected capabilities cross three ownership boundaries.

## Unresolved Gaps

- No Necronomicon transport target was updated.

## Recommended Next Route

Run `invoke plan` for `arcana/task-session` and produce a refreshed work-pack that maps:

- define requirements,
- glossary constraints,
- six-view architecture decisions,
- context-pack goal handoff design,
- validation and observability requirements.
