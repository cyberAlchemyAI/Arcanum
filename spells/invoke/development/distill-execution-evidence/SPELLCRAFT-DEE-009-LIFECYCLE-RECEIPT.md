# Task Session Lifecycle Receipt: SWU-DEE-009

## Identity

- Lifecycle owner: `task-session`
- Spell: `invoke`
- Canonical ID: `invoke`
- Source SWU: `SWU-DEE-009`
- Decision: **accept one missing-required-evidence fail-closed fixture**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-009` owns the focused negative case where an active Invoke mode omits an applicable
required evidence field. The resolver must return `block`, identify the missing field with a
stable diagnostic, and deny mutation handoff.

This unit does not add a new detector or modify the active evidence contract. It consumes the
DEE-007 resolver and leaves fabricated/schema-complete corruption to DEE-010.

## Binding

Execution owner: Task Session, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/development/fixtures/distill-evidence/missing-evidence-case.json`
- `arcanum/spells/invoke/development/run-distill-missing-evidence-fixture.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-009-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-05-FIXTURES.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-009-RESULT.md`

Dependency consumed as read-only evidence: DEE-007 active-mode evidence resolver and its
`mode-evidence-missing-required.json` fixture.

## Acceptance Conditions

- the missing required field is `work_pack` in active `plan` mode;
- the resolver returns `block`;
- the diagnostic names the missing field;
- `mutation_handoff_allowed` is false;
- the runner is deterministic, local, and model-free.

## Next Route

`task-session` must bind `SWU-DEE-010` schema-complete fabricated-evidence coverage. It remains
blocked and unselected until its own receipt exists.
