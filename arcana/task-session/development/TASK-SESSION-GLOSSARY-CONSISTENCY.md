# Task Session Glossary Consistency

## Invocation

- Spell: `invoke`
- Mode: `design`
- Target artifact: `task-session`
- Source glossary: `TASK-SESSION-GLOSSARY.md`
- Checked design artifacts:
  - `TASK-SESSION-ARCHITECTURE-DESIGN.md`
  - `CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`
  - `CONTEXT-PACK-GOAL-HANDOFF-OPTIMIZATION.md`

## Result

Status: `pass`

The design artifacts use the canonical glossary terms consistently enough for plan handoff.

## Term Checks

| Term | Expected Use | Design Status |
| --- | --- | --- |
| Task Session | Sigil and governed execution loop. | pass |
| Selected Unit | Single task or SWU under execution. | pass |
| Work-Pack | Planning source of truth for task/SWU status and evidence. | pass |
| SWU | Smallest Working Unit. | pass |
| Context Pack | General selected evidence bundle. | pass |
| Handoff Pack | Runtime-facing persisted or inline context pack. | pass |
| Strict Coverage | Runtime handoff gate requiring every obligation to be covered or explicitly resolved. | pass |
| Obligation | Requirement, constraint, validation expectation, or source contract. | pass |
| Decision Pack | Option cards for unresolved implementation choices. | pass |
| Gate Verdict | Result of checking scope, dependencies, context, write scope, runtime, and validation readiness. | pass |
| Runtime Adapter | Boundary that translates gated state into runtime-specific handoff. | pass |
| Codex Goal Profile | Arcanum-generated profile for native Codex Goal. | pass |
| Evidence Sync | Evidence-backed update of task/work-pack records. | pass |
| Fallback Exploration | Runtime exploration beyond the pack for named gaps only. | pass |
| Authority Precedence | Conflict resolution order between instruction, task, work-pack, architecture, code, and inference. | pass |

## Consistency Notes

- `Task Session` remains runtime-neutral.
- `Codex Goal` is treated as an optional runtime, not as Task Session's identity.
- `context pack` and `handoff pack` are related but not identical:
  - use `context pack` for the selected evidence bundle,
  - use `handoff pack` when that bundle is persisted as session evidence for runtime delegation.
- `strict coverage` applies to Codex Goal handoff and should block incomplete packs.
- Generated context packs are described as execution evidence, not canonical project documentation.

## Plan Warnings

- Implementation tasks should not rename `handoff pack` to `context cache`; that would imply a reusable source of truth.
- Runtime adapter tasks should not collapse `Runtime Adapter` and `Codex Goal Profile`; the adapter owns runtime boundary checks, while the profile owns native goal text.
- Evidence sync tasks should preserve the rule that validation evidence precedes status updates.
