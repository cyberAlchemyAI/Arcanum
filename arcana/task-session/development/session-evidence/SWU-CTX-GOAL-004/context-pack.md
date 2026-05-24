# SWU-CTX-GOAL-004 Context Pack

## Identity

- Task/SWU: `SWU-CTX-GOAL-004`
- Source work-pack: `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Session evidence path: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-004/`
- Runtime handoff: local Task Session execution; Codex Goal delegation not used for this profile-contract audit.
- Repository revision observed: `b17b888`
- Evidence date: `2026-05-23`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| O1: Add handoff pack Markdown path and JSON/index path as required inputs. | covered | `transmutations/codex-goal-profile/SKILL.md` argument hint, inputs, readiness checks, and template source table. |
| O2: Add fallback exploration rule. | covered | `SKILL.md`, `README.md`, template, and examples restrict exploration to named gaps. |
| O3: Add expected final reporting for context gaps and extra sources used. | covered | `SKILL.md`, `README.md`, template, passing example, and command mirrors require extra-source reporting tied to named gaps. |
| O4: Generated goal prompt instructs Codex to use pack first. | covered | `templates/codex-goal-profile.md` Native Codex Goal text and passing example. |
| O5: Broad exploration is allowed only for named uncovered obligations or gaps. | covered | `SKILL.md` readiness, quality bar, README output, and template text. |
| O6: Missing strict coverage blocks profile generation. | covered | `SKILL.md` readiness and anti-patterns, README block rule, blocked example. |

## Selected Sources

- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
  - Selectors: `SWU-CTX-GOAL-004`, scope, acceptance, handoff note.
  - Why included: source of the selected SWU contract.
- `transmutations/codex-goal-profile/SKILL.md`
  - Selectors: argument hint, inputs, readiness, quality bar, output contract.
  - Why included: canonical profile generation contract.
- `transmutations/codex-goal-profile/README.md`
  - Selectors: Inputs, Output, block rule.
  - Why included: user-facing profile behavior.
- `transmutations/codex-goal-profile/templates/codex-goal-profile.md`
  - Selectors: Readiness, Native Codex Goal, Audit Notes.
  - Why included: generated goal shape.
- `transmutations/codex-goal-profile/examples/passing.md`
  - Selectors: output profile and verdict.
  - Why included: runnable positive example.
- `transmutations/codex-goal-profile/examples/blocked.md`
  - Selectors: blocked result and unblock action.
  - Why included: negative strict-coverage example.
- `.codex/commands/codex-goal-profile.md`
- `.codex/commands/arcanum-sigil-codex-goal-profile.md`
  - Selectors: process and guardrails.
  - Why included: installed command mirrors.

## Constraints And Non-Goals

- Codex Goal Profile owns prompt shape, not Task Session orchestration or Context Builder selection.
- Do not generate runnable goals when strict handoff coverage fails.

## Write Scope

- `transmutations/codex-goal-profile/SKILL.md`
- `transmutations/codex-goal-profile/README.md`
- `transmutations/codex-goal-profile/templates/codex-goal-profile.md`
- `transmutations/codex-goal-profile/examples/passing.md`
- `transmutations/codex-goal-profile/examples/blocked.md`
- `.codex/commands/codex-goal-profile.md`
- `.codex/commands/arcanum-sigil-codex-goal-profile.md`

## Validation Surface

- Search profile files and command mirrors for context pack/index inputs, pack-first language, strict coverage, fallback, extra-source reporting, and block behavior.
- Run `git diff --check` on profile files, command mirrors, and SWU evidence.
- Parse SWU evidence JSON with `jq empty`.

## Gaps And Blockers

- No blocker for SWU-004.
- No unresolved gaps require fallback repository exploration.

## Fallback Exploration Rule

No broad exploration is authorized for SWU-004 because selected profile sources cover every obligation.

## Strict Coverage Status

`pass`

