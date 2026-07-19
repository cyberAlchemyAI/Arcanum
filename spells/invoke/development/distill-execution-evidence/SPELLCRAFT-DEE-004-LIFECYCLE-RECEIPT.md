# Spellcraft Lifecycle Receipt: SWU-DEE-004

## Identity

- Spellcraft mode: `validate`
- Spell: `invoke`
- Canonical ID: `invoke`
- Alias used: none
- Scope: library
- Source lifecycle receipts: `SPELLCRAFT-LIFECYCLE-RECEIPT.md` and
  `SPELLCRAFT-DEE-003-LIFECYCLE-RECEIPT.md`
- Source SWU: `SWU-DEE-004`
- Decision: **accept with bounded semantic extension**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-004` owns deterministic semantic checks over the already accepted request, receipt, and
runtime-event contracts. It checks process completion and produces semantic diagnostics only;
`SWU-DEE-005` remains the owner of provenance/cross-artifact agreement and final validator-result
composition.

The structural receipt schema may gain optional `objection_id`, `category`, `disposition`, and
`objection_ref` fields so semantic fixtures can carry the categories and reconciliation
dispositions required by the design. No existing required field is removed or weakened, and
existing DEE-002 fixtures must remain valid.

## Semantic Contract

The semantic validator must:

1. validate the request, receipt, and every referenced runtime event with the accepted schemas;
2. require request/receipt/event run identity agreement and complete event-reference coverage;
3. resolve ordered role/process events using the DEE-003 adapter;
4. require `termination.round_count <= request.round_budget.max_rounds` and an allowed
   termination reason;
5. require every objection to have a stable ID and category, and exactly one reconciliation with
   a disposition in `accept`, `revise`, `reject`, `defer`, or `route`;
6. require every requested technique to be traced as `applied` or `not_applicable`; a failed or
   missing technique blocks semantic readiness;
7. return stable diagnostics and `semantic_status` (`pass` or `block`) without setting
   `mutation_handoff_allowed` or synthesizing a final `DistillValidationResult`.

## SWU-DEE-004 Binding

Canonical lifecycle owner: `invoke` through Spellcraft.

Execution owner: Task Session, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/schemas/distill-execution-receipt.schema.json`
- `arcanum/spells/invoke/development/distill_semantic_validator.py`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/semantic-valid.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/semantic-missing-objection-category.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/semantic-unreconciled-objection.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/semantic-missing-technique-trace.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/semantic-round-budget-exceeded.json`
- `arcanum/spells/invoke/development/run-distill-semantic-fixtures.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-004-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-03-VALIDATOR.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-004-RESULT.md`

The schema extension is optional structural metadata only. It does not move semantic authority
into JSON Schema and does not authorize changes to DEE-002 result history.

## Acceptance Conditions

- the five semantic fixtures distinguish valid process completion from each named failure;
- diagnostics are deterministic, stable, and fail closed;
- the semantic result contains no `mutation_handoff_allowed` field;
- no provenance, mode, generated-mirror, Workbench, or Distill sigil contract paths are changed;
- the focused semantic runner uses no model call and reuses the DEE-003 resolver;
- later promotion remains blocked until DEE-005 through DEE-010 produce the remaining evidence.

## Next Route

`spellcraft` must bind the canonical provenance/cross-artifact validator owner and exact write
paths for `SWU-DEE-005`. `SWU-DEE-005` through `SWU-DEE-013` remain blocked and unselected.
