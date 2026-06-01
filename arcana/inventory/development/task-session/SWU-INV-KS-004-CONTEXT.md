# Task Session Context: SWU-INV-KS-004

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-002`
- SWU: `SWU-INV-KS-004`
- Goal: patch `arcana/inventory/templates/index.md` with evidence-card index and retrieval sections.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-002-lint-index.md`
- `arcana/inventory/development/templates/evidence-card-index.md`
- `arcana/inventory/templates/index.md`
- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/development/POC-VALIDATION.md`

## Controlling Constraints

- Dependency `SWU-INV-KS-001` must be complete.
- Patch the existing Inventory index template rather than replacing its page catalog role.
- Include index families and retrieval output shape.
- Retrieval must preserve selected cards, excluded matches, and trace notes for the POC retrieval-value gate.

## Gate Verdict

Pass. The existing index template is present, the source retrieval contract exists, and validation is available.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Patch style | Append evidence-card sections after the existing page/type index. | Preserves the older index role while adding card-specific retrieval contract. |
| Retrieval output | YAML shape with selected cards, excluded matches, and trace notes. | Matches the POC need to compare compact retrieval against broad source rereading. |
| Runtime | Local fallback. | This SWU is static template mutation. |
