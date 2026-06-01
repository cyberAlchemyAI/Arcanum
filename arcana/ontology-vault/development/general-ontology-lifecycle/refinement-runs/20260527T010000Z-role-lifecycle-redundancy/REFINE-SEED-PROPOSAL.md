# Refine Seed Proposal: Role And Lifecycle Redundancy

Status: exploratory, non-canonical
Run id: `20260527T010000Z-role-lifecycle-redundancy`
Preset: compact
Research: no-research

## Target

`arcana/ontology-vault/development/general-ontology-lifecycle/GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md`

Focus selectors:

- `## Lifecycle States`
- `## Candidate Role Semantics`
- `## Confidence Rules`
- `## Operational Use Rules`

## Concern

Evaluate whether the candidate role semantics section duplicates the ontology lifecycle model instead of complementing it.

The suspected redundancy is strongest where the same words appear as both lifecycle states or outcomes and role semantics:

- `candidate`
- `premise`
- `policy`
- `constitution`
- `axiom`
- `contradiction` / `contradicted`
- `retirement` / `retired`

## Write Scope

This run may write only refinement evidence under this run folder.

It does not mutate:

- canonical Ontology Vault contracts,
- Inventory,
- structured-action-schema,
- lifecycle templates,
- the source lifecycle model.

## Done Criteria

- Identify true redundancy versus useful mirrored vocabulary.
- Define a clean boundary between lifecycle/status and role/claim semantics.
- Recommend whether to edit the source model now or defer to schema design.
- Preserve candidate-only posture.

## Validation Surface

- Local file selectors are sufficient.
- Arcanum command resolution is recorded.
- Stage dispatch is represented using dry-run evidence for command-backed stages.
- Final synthesis is a non-executed refinement result.
