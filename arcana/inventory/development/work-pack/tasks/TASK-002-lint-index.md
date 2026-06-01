# TASK-002: Promote Lint And Index Contracts

## Objective

Create production lint contract and patch Inventory index template with evidence-card index/retrieval expectations.

## Source Contracts

- `../../templates/evidence-card-lint.md`
- `../../templates/evidence-card-index.md`
- `../../OPERATIONS.md`
- `../../FLOWS-POLICIES.md`

## Smallest Working Units

### SWU-INV-KS-003

- Goal: Add `arcana/inventory/templates/evidence-card-lint.md`.
- Dependencies: SWU-INV-KS-001.
- Write scope: `arcana/inventory/templates/evidence-card-lint.md`.
- Done criteria: lint contract includes required checks and invalid examples.
- Validation: `rg -n "Expected finding|owner/status|selector|unknown enum|minimal" arcana/inventory/templates/evidence-card-lint.md`
- Execution owner: local-fallback.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-003-CONTEXT.md`, `../../task-session/SWU-INV-KS-003-RESULT.md`.

### SWU-INV-KS-004

- Goal: Patch `arcana/inventory/templates/index.md` with evidence-card index and retrieval sections.
- Dependencies: SWU-INV-KS-001.
- Write scope: `arcana/inventory/templates/index.md`.
- Done criteria: index families and retrieval output shape are documented.
- Validation: `rg -n "cards-by-id|selected_cards|excluded_matches|trace_notes" arcana/inventory/templates/index.md`
- Execution owner: local-fallback.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-004-CONTEXT.md`, `../../task-session/SWU-INV-KS-004-RESULT.md`.

## Synchronization

After completion, unblock pilot fixture and docs work.

## Completion Evidence

| SWU | Status | Evidence | Validation |
| --- | --- | --- | --- |
| SWU-INV-KS-003 | completed | `arcana/inventory/templates/evidence-card-lint.md` | `rg -n "Expected finding|owner/status|selector|unknown enum|minimal" arcana/inventory/templates/evidence-card-lint.md` |
| SWU-INV-KS-004 | completed | `arcana/inventory/templates/index.md` | `rg -n "cards-by-id|selected_cards|excluded_matches|trace_notes" arcana/inventory/templates/index.md` |
