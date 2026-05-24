# SWU-CTX-GOAL-005 Context Pack

## Identity

- Task/SWU: `SWU-CTX-GOAL-005`
- Source work-pack: `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Session evidence path: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-005/`
- Runtime handoff: local Task Session execution; Codex Goal delegation not used for this adapter-contract audit.
- Repository revision observed: `b17b888`
- Evidence date: `2026-05-23`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| O1: Validate pack quality before `create_goal` or goal delegation. | covered | `arcana/task-session/runtime-adapters/codex-goal.md` availability check, input contract, and transformation block rule. |
| O2: Pass pack Markdown path and JSON/index into the goal objective. | covered | `codex-goal.md` input contract, transformation, and handoff shape. |
| O3: Preserve pack reference in completion evidence. | covered | `codex-goal.md` Result Evidence and runtime-adapters README `result_evidence`. |
| O4: Missing, stale, contradictory, unsafe, missing-validation, missing-write-scope, or non-strict packs block delegation. | covered | `codex-goal.md` transformation and blocked fallback; runtime-adapters README goal-like adapter rule. |
| O5: Successful delegation records pack identity and gap-driven extra exploration. | covered | `codex-goal.md` Result Evidence and handoff shape; runtime-adapters README successful delegation evidence. |

## Selected Sources

- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
  - Selectors: `SWU-CTX-GOAL-005`, scope, acceptance, handoff note.
  - Why included: source of the selected SWU contract.
- `arcana/task-session/runtime-adapters/codex-goal.md`
  - Selectors: Availability Check, Input Contract, Transformation, Handoff Shape, Result Evidence, Blocked Fallback.
  - Why included: canonical Codex Goal adapter contract.
- `arcana/task-session/runtime-adapters/README.md`
  - Selectors: Adapter Contract, Current Adapters, successful delegation evidence.
  - Why included: shared adapter boundary.
- `transmutations/codex-goal-profile/SKILL.md`
  - Selectors: readiness checks and extra-source reporting.
  - Why included: adapter delegates profile shape to this transmutation.

## Constraints And Non-Goals

- Adapter must not override Task Session blockers.
- Adapter must not broaden write scope.
- Adapter must keep Codex native Goal as runtime owner after safe handoff.

## Write Scope

- `arcana/task-session/runtime-adapters/codex-goal.md`
- `arcana/task-session/runtime-adapters/README.md`

## Validation Surface

- Search adapter docs and task-session command mirrors for missing/stale/contradictory/unsafe/write-scope/validation/strict-coverage blockers.
- Search adapter docs for pack identity, JSON/index, gap-driven fallback, and extra-source reporting.
- Parse SWU evidence JSON with `jq empty`.
- Run `git diff --check` on adapter files and SWU evidence.

## Gaps And Blockers

- No blocker for SWU-005.
- No unresolved gaps require fallback repository exploration.

## Fallback Exploration Rule

No broad exploration is authorized for SWU-005 because selected adapter sources cover every obligation.

## Strict Coverage Status

`pass`

