# Task Session Lifecycle Receipt: SWU-DEE-010

## Identity

- Lifecycle owner: `task-session`
- Spell: `invoke`
- Canonical ID: `invoke`
- Source SWU: `SWU-DEE-010`
- Decision: **accept schema-complete fabricated-evidence corruption matrix**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-010` owns four isolated fabricated-evidence cases and one combined case. Each case
must remain schema-complete, reach the provenance/authority checks, emit its expected diagnostic,
and deny mutation handoff. The combined case proves fail-closed behavior when several plausible
authored claims disagree at once.

This unit does not change validator behavior. It proves the existing DEE-003 and DEE-005
detectors discriminate fabricated evidence rather than only checking labels or shape.

## Binding

Execution owner: Task Session, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/development/fixtures/distill-evidence/fabricated-evidence-matrix.json`
- `arcanum/spells/invoke/development/run-distill-fabricated-evidence-fixture.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-010-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-05-FIXTURES.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-010-RESULT.md`

Dependencies consumed as read-only evidence: DEE-003 runtime events, DEE-004 semantic
validation, DEE-005 provenance validation, and DEE-008 positive composition.

## Acceptance Conditions

- four isolated corruptions remain schema-complete and block for their expected reason;
- the combined corruption case blocks closed;
- every case derives `mutation_handoff_allowed=false`;
- authored handoff fields cannot override a failed validator result;
- the runner is deterministic, local, and model-free.

## Next Route

`spellcraft` must bind `SWU-DEE-011` generated parity and exact mirror paths. DEE-011 through
DEE-013 remain blocked and unselected until their own lifecycle receipts exist.
