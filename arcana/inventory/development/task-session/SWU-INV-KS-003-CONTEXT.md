# Task Session Context: SWU-INV-KS-003

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-002`
- SWU: `SWU-INV-KS-003`
- Goal: promote the evidence-card lint contract into `arcana/inventory/templates/evidence-card-lint.md`.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-002-lint-index.md`
- `arcana/inventory/development/templates/evidence-card-lint.md`
- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/templates/evidence-card.md`
- `arcana/inventory/development/POC-VALIDATION.md`

## Controlling Constraints

- Dependency `SWU-INV-KS-001` must be complete.
- Keep write scope to the lint contract plus synchronization.
- The contract must include required checks and invalid examples.
- Validation strictness is one of the six POC gates.

## Gate Verdict

Pass. The schema and authoring template exist, the source lint contract exists, and validation is available.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Lint scope | Static authoring contract, not executable validator. | Runtime validator language is explicitly deferred. |
| Finding language | Use expected findings as fixture seeds. | This supports the POC validation-strictness gate. |
| Runtime | Local fallback. | This SWU is static contract promotion. |
