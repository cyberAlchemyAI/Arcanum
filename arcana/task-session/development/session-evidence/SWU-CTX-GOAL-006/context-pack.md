# SWU-CTX-GOAL-006 Context Pack

## Identity

- Task/SWU: `SWU-CTX-GOAL-006`
- Source work-pack: `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Session evidence path: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-006/`
- Runtime handoff: local Task Session execution; Codex Goal delegation not used for this Invoke planning-contract audit.
- Repository revision observed: `b17b888`
- Evidence date: `2026-05-23`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| O1: Generated work-packs include source anchors. | covered | `spells/invoke/plan.md` SWU policy and handoff policy; `spells/invoke/templates/work-pack.md` `Source Anchors` column. |
| O2: Generated work-packs include acceptance evidence and validation surface. | covered | `plan.md` SWU policy and handoff policy; work-pack template `Acceptance Evidence` and `Validation Surface` columns. |
| O3: Generated work-packs include write boundaries. | covered | `plan.md` and work-pack template require write scope. |
| O4: Generated work-packs include related-context hints. | covered | `plan.md` handoff policy and work-pack template `Related Context` column. |
| O5: Context packs are generated at execution time, not during planning. | covered | `plan.md` purpose/mode gates and work-pack template Context Builder readiness rule. |
| O6: Work-pack does not depend on stale generated context packs. | covered | `plan.md` and work-pack template explicitly prohibit pre-generating context packs in Invoke planning. |

## Selected Sources

- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
  - Selectors: `SWU-CTX-GOAL-006`, scope, acceptance, handoff note.
  - Why included: source of the selected SWU contract.
- `spells/invoke/plan.md`
  - Selectors: Purpose, Smallest Working Unit Policy, SWU Subagent Handoff Policy, Mode Gates.
  - Why included: canonical Invoke Plan behavior.
- `spells/invoke/design.md`
  - Selectors: Purpose, Handoff Artifacts.
  - Why included: design-stage handoff context for downstream plan.
- `spells/invoke/templates/work-pack.md`
  - Selectors: Planning Mapping, Split Task File Contract, SWU Execution Handoff, Gate Checks.
  - Why included: generated work-pack output shape.

## Constraints And Non-Goals

- Invoke prepares context-builder-ready SWU contracts; it does not generate task context packs during planning.
- Runtime/session evidence remains owned by Task Session and Context Builder during execution.

## Write Scope

- `spells/invoke/plan.md`
- `spells/invoke/design.md`
- `spells/invoke/templates/work-pack.md`

## Validation Surface

- Search Invoke plan/design/template for source anchors, acceptance evidence, validation surface, write boundaries/write scope, related context, handoff context, context packs generated at execution time, and pre-generation guardrails.
- Parse SWU evidence JSON with `jq empty`.
- Run `git diff --check` on Invoke files and SWU evidence.

## Gaps And Blockers

- No blocker for SWU-006.
- No unresolved gaps require fallback repository exploration.

## Fallback Exploration Rule

No broad exploration is authorized for SWU-006 because selected Invoke sources cover every obligation.

## Strict Coverage Status

`pass`

