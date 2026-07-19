# Task Session Lifecycle Receipt: SWU-DEE-008

## Identity

- Lifecycle owner: `task-session`
- Spell: `invoke`
- Canonical ID: `invoke`
- Source SWU: `SWU-DEE-008`
- Decision: **accept one positive integrated evidence fixture**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-008` owns one deterministic positive case proving that accepted request, runtime
events, execution receipt, reviewed-input provenance, and cross-artifact Invoke state resolve to
`pass` with derived mutation handoff allowed.

It composes the existing DEE-002 through DEE-005 validators and does not add a second authority
path, alter the accepted schemas, or cover adversarial corruption. Missing and fabricated cases
remain DEE-009 and DEE-010.

## Binding

Execution owner: Task Session, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/development/fixtures/distill-evidence/positive-evidence-case.json`
- `arcanum/spells/invoke/development/run-distill-positive-evidence-fixture.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-008-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-05-FIXTURES.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-008-RESULT.md`

Dependencies consumed as read-only evidence: DEE-002 request/receipt/result schemas, DEE-003
runtime event resolver, DEE-004 semantic validator, and DEE-005 provenance validator.

## Acceptance Conditions

- the positive fixture resolves through all accepted validator layers;
- reviewed-input bytes are materialized and their digest/size agree;
- runtime event order, role identity, semantic reconciliation, and provenance agree;
- the result is `pass` and `mutation_handoff_allowed` is derived `true`;
- no authored handoff field is used as authority;
- the runner is deterministic, local, and model-free.

## Next Route

`task-session` must bind `SWU-DEE-009` missing-evidence coverage and then `SWU-DEE-010`
fabricated-evidence coverage. Both remain blocked and unselected until their own receipts exist.
