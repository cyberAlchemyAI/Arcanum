# Task Session Context: SWU-INV-KS-008

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-005`
- SWU: `SWU-INV-KS-008`
- Goal: update `arcana/inventory/README.md` and `arcana/inventory/SKILL.md`.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-005-docs-contracts.md`
- `arcana/inventory/development/SPEC.md`
- `arcana/inventory/development/ARCHITECTURE.md`
- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/templates/evidence-card-lint.md`

## Controlling Constraints

- Dependency `TASK-002` must be complete.
- README and SKILL must describe evidence-card-aware ingest, lookup, lint, validate, and downstream boundaries.
- Existing Inventory defaults must remain compatible.
- Validation must find evidence-card, `source_refs`, `trace`, `residue`, `promotion_owner`, and non-authority language.

## Gate Verdict

Pass. `TASK-002` is complete, the docs targets exist, and validation is available.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Documentation style | Add evidence-card as an optional layer, not a replacement for wiki inventory. | Preserves existing Inventory behavior while exposing the new POC contract. |
| Skill mode updates | Extend ingest, lookup, lint, and validate mode language. | Makes the behavior discoverable from the command surface. |
| Runtime | Local fallback. | This SWU is documentation and skill contract mutation. |
