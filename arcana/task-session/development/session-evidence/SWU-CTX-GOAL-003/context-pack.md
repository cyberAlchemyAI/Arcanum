# SWU-CTX-GOAL-003 Context Pack

## Identity

- Task/SWU: `SWU-CTX-GOAL-003`
- Source work-pack: `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Session evidence path: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-003/`
- Runtime handoff: local Task Session execution; Codex Goal delegation not used for this command-contract audit.
- Repository revision observed: `b17b888`
- Evidence date: `2026-05-23`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| O1: Task Session builds the handoff pack before gates and delegation. | covered | `arcana/task-session/SKILL.md` Step 2 runs Context Builder before Step 4 gates and Step 5 runtime selection. |
| O2: Context Builder can run as delegated worker when available with inline/local fallback. | covered | `arcana/task-session/SKILL.md` required sigils plus Step 2; `arcana/task-session/README.md` Context Builder baseline and work-pack runtime flow. |
| O3: Block or ask for decision when coverage, contradiction, or staleness gates fail. | covered | `arcana/task-session/SKILL.md` Steps 2, 4, and 5 return `BLOCK` for weak, stale, contradictory, or non-strict context. |
| O4: `--via goal` cannot proceed without Markdown plus JSON/index handoff artifacts and strict coverage. | covered | `arcana/task-session/SKILL.md` Step 5 and README runtime adapter interface. |
| O5: Task Session report includes pack artifacts, strict coverage, gaps, and fallback search policy. | covered | `arcana/task-session/SKILL.md` Step 9 and output contract; README runtime-backed output. |
| O6: Installed command mirrors reflect the same behavior. | covered | `.codex/commands/task-session.md` and `.codex/commands/arcanum-sigil-task-session.md` were refreshed from canonical README/SKILL snapshots. |

## Selected Sources

- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
  - Selectors: `SWU-CTX-GOAL-003`, scope, acceptance, handoff note.
  - Why included: source of the selected SWU contract.
- `arcana/task-session/SKILL.md`
  - Selectors: required sigils, Steps 2, 4, 5, 7, 9, quality bar, output contract.
  - Why included: canonical executable Task Session contract.
- `arcana/task-session/README.md`
  - Selectors: Context Builder baseline, Work-Pack Runtime Flow, Runtime Adapter Interface, Output.
  - Why included: user-facing Task Session contract.
- `.codex/commands/task-session.md`
  - Selectors: repository runtime interface, process, canonical snapshots.
  - Why included: installed command mirror used by slash-style invocation.
- `.codex/commands/arcanum-sigil-task-session.md`
  - Selectors: repository runtime interface, process, canonical snapshots.
  - Why included: alternate installed command mirror.

## Constraints And Non-Goals

- Do not make subagent execution mandatory; the contract is the handoff pack.
- Do not execute a broad multi-SWU session inside one Task Session.
- Do not let command mirrors drift from canonical Task Session behavior.

## Write Scope

- `arcana/task-session/SKILL.md`
- `arcana/task-session/README.md`
- `.codex/commands/task-session.md`
- `.codex/commands/arcanum-sigil-task-session.md`

## Validation Surface

- Search Task Session canonical docs and command mirrors for context-builder, `--via goal`, Markdown plus JSON/index, strict coverage, handoff pack, fallback, gaps, and report fields.
- Search command mirrors for stale embedded snapshot markers.
- Run `git diff --check` on Task Session files, command mirrors, and SWU evidence.

## Gaps And Blockers

- No blocker for SWU-003.
- No unresolved gaps require fallback repository exploration.

## Fallback Exploration Rule

No broad exploration is authorized for SWU-003 because selected Task Session and command mirror sources cover every obligation.

## Strict Coverage Status

`pass`

