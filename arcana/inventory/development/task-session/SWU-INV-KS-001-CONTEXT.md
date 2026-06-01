# Task Session Context: SWU-INV-KS-001

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-001`
- SWU: `SWU-INV-KS-001`
- Goal: promote the evidence-card schema contract into `arcana/inventory/templates/evidence-card-schema.md`.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-001-templates.md`
- `arcana/inventory/development/templates/evidence-card-schema.md`
- `arcana/inventory/development/POC-VALIDATION.md`
- `arcana/inventory/development/POC-CANDIDATES.md`
- `arcana/inventory/development/work-pack/shared/SOURCE-CONTRACTS.md`

## Controlling Constraints

- Execute exactly one SWU.
- Keep the mutation to the production evidence-card schema and synchronization evidence.
- Preserve Inventory authority boundaries: evidence-cards can record candidates, but cannot promote ontology or definition authority.
- Keep the POC source slice bounded: start with the recommended five-section candidate slice, then add selected Craft sections only if EvidenceSet remains unresolved.
- Validator implementation remains deferred.

## Gate Verdict

Pass. `SWU-INV-KS-001` has no dependency, a declared write scope, a concrete source template, and a validation command.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Production schema shape | Promote the development template and add explicit vocabularies/rules. | The development source already contains the core contract; production needs enough detail for authoring and lint SWUs. |
| POC candidate update | Keep recommended five-section slice first; retain Craft as a second-pass EvidenceSet stressor. | This tests the evidence-card unit before adding recursive-ledger complexity. |
| Runtime | Local fallback. | The SWU is a static artifact promotion with direct validation. |
