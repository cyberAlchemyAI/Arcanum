# Spellcraft Lifecycle Receipt: SWU-DEE-005

## Identity

- Spellcraft mode: `validate`
- Spell: `invoke`
- Canonical ID: `invoke`
- Alias used: none
- Source SWU: `SWU-DEE-005`
- Decision: **accept with bounded provenance and agreement composition**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-005` owns exact reviewed-input provenance resolution and cross-artifact agreement over
the completed DEE-002, DEE-003, and DEE-004 evidence. It composes the semantic result into the
accepted `DistillValidationResult` shape and is the first unit allowed to derive
`mutation_handoff_allowed`.

The validator recomputes each reviewed file's SHA-256 digest and byte size, compares request and
receipt provenance sets, and fails closed for changed or unresolved content. It also compares run
identity, semantic status, reported receipt/invoke verdict, event count, and Work Pack binding.
It never trusts an authored handoff flag.

## Binding

Canonical lifecycle owner: `invoke` through Spellcraft.

Execution owner: Task Session, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/development/distill_provenance_validator.py`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/provenance-valid.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/provenance-changed-content.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/provenance-unresolved-handle.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/provenance-verdict-mismatch.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/provenance-workpack-mismatch.json`
- `arcanum/spells/invoke/development/run-distill-provenance-fixtures.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-005-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-03-VALIDATOR.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-005-RESULT.md`

No mode integration, generated mirror, Workbench, or Distill sigil contract path is selected.

## Acceptance Conditions

- exact unchanged content passes digest and size recomputation;
- changed content, unresolved handles, verdict mismatch, and stale Work Pack binding block;
- request and receipt provenance sets agree exactly;
- output conforms to the accepted validation-result schema;
- `mutation_handoff_allowed` is derived `true` only when all semantic and provenance checks
  pass, and is false on every failure;
- authored status or handoff fields cannot make a failed case pass;
- the focused runner is deterministic and uses no model call;
- promotion remains blocked until DEE-006 through DEE-010 produce mode and adversarial evidence.

## Next Route

`task-session` on `SWU-DEE-005` only. `SWU-DEE-006` through `SWU-DEE-013` remain blocked and
unselected.
