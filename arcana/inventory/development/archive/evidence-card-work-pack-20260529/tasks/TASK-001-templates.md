# TASK-001: Promote Schema And Authoring Templates

## Objective

Create production evidence-card schema and authoring templates from the refreshed development templates.

## Source Contracts

- `../../templates/evidence-card-schema.md`
- `../../templates/evidence-card.md`
- `../../CONCEPT-MODEL.md`

## Smallest Working Units

### SWU-INV-KS-001

- Goal: Add `arcana/inventory/templates/evidence-card-schema.md`.
- Dependencies: none.
- Write scope: `arcana/inventory/templates/evidence-card-schema.md`.
- Done criteria: schema contract includes required fields, controlled vocabularies, profile rules, trace, residue, selectors, and authority rules.
- Validation: `rg -n "schema_version|profile|captured|trace|residue|promotion_owner|non_authority_notice" arcana/inventory/templates/evidence-card-schema.md`
- Execution owner: local-fallback.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-001-CONTEXT.md`, `../../task-session/SWU-INV-KS-001-RESULT.md`.

### SWU-INV-KS-002

- Goal: Add `arcana/inventory/templates/evidence-card.md`.
- Dependencies: SWU-INV-KS-001.
- Write scope: `arcana/inventory/templates/evidence-card.md`.
- Done criteria: template can author full and minimal cards.
- Validation: `rg -n "source_refs|captured|trace|residue|updated_at" arcana/inventory/templates/evidence-card.md`
- Execution owner: local-fallback.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-002-CONTEXT.md`, `../../task-session/SWU-INV-KS-002-RESULT.md`.

## Synchronization

After completion, update `WORK-PACK.md` task status and unblock TASK-002.

## Completion Evidence

| SWU | Status | Evidence | Validation |
| --- | --- | --- | --- |
| SWU-INV-KS-001 | completed | `arcana/inventory/templates/evidence-card-schema.md` | `rg -n "schema_version|profile|captured|trace|residue|promotion_owner|non_authority_notice" arcana/inventory/templates/evidence-card-schema.md` |
| SWU-INV-KS-002 | completed | `arcana/inventory/templates/evidence-card.md` | `rg -n "source_refs|captured|trace|residue|updated_at" arcana/inventory/templates/evidence-card.md` |
