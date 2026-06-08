# TASK-005: Update Docs And Mode Contracts

## Objective

Update reusable Inventory docs and skill contract so evidence-card behavior is discoverable and compatible with existing modes.

## Source Contracts

- `../../SPEC.md`
- `../../ARCHITECTURE.md`
- `../../TEMPLATE-MANIFEST.md`

## Smallest Working Units

### SWU-INV-KS-008

- Goal: Update `arcana/inventory/README.md` and `arcana/inventory/SKILL.md`.
- Dependencies: TASK-002.
- Write scope: `arcana/inventory/README.md`, `arcana/inventory/SKILL.md`.
- Done criteria: README and SKILL describe evidence-card-aware ingest, lookup, lint, validate, and downstream boundaries.
- Validation: `rg -n "evidence-card|source_refs|trace|residue|promotion_owner|non-authority" arcana/inventory/README.md arcana/inventory/SKILL.md`
- Execution owner: local-fallback.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-008-CONTEXT.md`, `../../task-session/SWU-INV-KS-008-RESULT.md`.

## Synchronization

After completion, readiness can close docs alignment.

## Completion Evidence

| SWU | Status | Evidence | Validation |
| --- | --- | --- | --- |
| SWU-INV-KS-008 | completed | `arcana/inventory/README.md`, `arcana/inventory/SKILL.md` | `rg -n "evidence-card|source_refs|trace|residue|promotion_owner|non-authority" arcana/inventory/README.md arcana/inventory/SKILL.md` |
