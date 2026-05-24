# SWU-CTX-GOAL-002 Context Pack

## Identity

- Task/SWU: `SWU-CTX-GOAL-002`
- Source work-pack: `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Session evidence path: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-002/`
- Runtime handoff: local Task Session execution; Codex Goal delegation not used for this template/mode audit.
- Repository revision observed: `b17b888`
- Evidence date: `2026-05-23`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| O1: Add a handoff mode such as `--handoff codex-goal`. | covered | `transmutations/context-builder/SKILL.md` frontmatter and flags document `--handoff codex-goal`. |
| O2: Add persistence option such as `--persist <session-evidence-path>`. | covered | `transmutations/context-builder/SKILL.md` flags and process document `--persist`; `README.md` describes run/session evidence. |
| O3: Emit both human-readable Markdown and structured JSON/index forms. | covered | `transmutations/context-builder/SKILL.md` process and output contract; templates added under `transmutations/context-builder/templates/`. |
| O4: A task/SWU can produce a session-evidence handoff pack. | covered | This SWU evidence pack plus the templates prove the output path and shape. |
| O5: Pack includes source selectors and coverage summary. | covered | `templates/codex-goal-handoff-pack.md` includes `Obligation Coverage` and `Selected Sources`; JSON template includes `obligations` and `selected_sources`. |
| O6: Pack records unresolved gaps rather than hiding them. | covered | Markdown template includes `Gaps And Blockers`; JSON template includes `gaps_and_blockers`. |

## Selected Sources

- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
  - Selectors: `SWU-CTX-GOAL-002`, scope, acceptance, handoff note.
  - Why included: source of the selected SWU contract.
- `transmutations/context-builder/SKILL.md`
  - Selectors: frontmatter `argument-hint`, flags, process steps 10-14, output contract.
  - Why included: canonical Context Builder behavior contract.
- `transmutations/context-builder/README.md`
  - Selectors: `Output`, template references, `Handoff Pack Schema`.
  - Why included: user-facing mode and persistence description.
- `transmutations/context-builder/templates/codex-goal-handoff-pack.md`
  - Selectors: full template headings.
  - Why included: Markdown handoff pack output shape.
- `transmutations/context-builder/templates/codex-goal-handoff-index.json`
  - Selectors: top-level keys.
  - Why included: structured JSON/index output shape.

## Constraints And Non-Goals

- Generated packs are execution evidence, not canonical planning docs.
- This SWU does not implement a separate executable CLI; Context Builder is a Codex skill contract.

## Write Scope

- `transmutations/context-builder/SKILL.md`
- `transmutations/context-builder/README.md`
- `transmutations/context-builder/templates/codex-goal-handoff-pack.md`
- `transmutations/context-builder/templates/codex-goal-handoff-index.json`

## Validation Surface

- Confirm flags and process mention `--handoff codex-goal`, `--persist`, Markdown, and JSON/index.
- Validate template JSON with `jq empty`.
- Run `git diff --check` on Context Builder files and SWU-002 evidence.

## Gaps And Blockers

- No blocker for SWU-002.
- No unresolved gaps require fallback repository exploration.

## Fallback Exploration Rule

No broad exploration is authorized for SWU-002 because the output-mode obligations are covered by selected sources.

## Strict Coverage Status

`pass`

