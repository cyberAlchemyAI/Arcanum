# Plan Transport

## Route

`invoke define` -> `invoke design` -> `invoke plan` -> `task-session`

## Task Session Target

- Work pack: `WORK-PACK.md`
- Task: `TASK-IDD-001`
- SWU: `SWU-IDD-001`

## Context Builder Selection

Use lean context from:

- `arcanum/spells/invoke/README.md`
- `arcanum/spells/invoke/define.md`
- `arcanum/spells/invoke/design.md`
- `arcanum/spells/invoke/plan.md`
- `arcanum/formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- `arcanum/spells/invoke/development/run-validation-fixtures.sh`
- `arcanum/spells/invoke/development/fixtures/*DEFINE*.expected.md`
- `arcanum/spells/invoke/development/fixtures/*DESIGN*.expected.md`
- `.agents/skills/invoke/define.md`
- `.agents/skills/invoke/design.md`

## Gate Checks

- Scope is bounded to one SWU.
- Acceptance criteria are verifiable with local commands.
- Mutation authority is limited to source contract and fixture edits.
- No unresolved blocker requires user input.

## Dispatch Technique Trace

- `frame_handoff`: this transport passes a bounded work-pack frame to Task Session.
- `concrete_path_evidence`: source refs are concrete local paths.
- `execution_receipt_handoff`: Task Session must write result evidence back to this package.

## Distill Validation

- Status: pass
- Unit: one bounded task-session execution.
- Next route: task-session
