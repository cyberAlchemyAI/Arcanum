# Invoke Plan Transport: Branch-Aware Ontology Schema Tests

Status: pass
Mode: plan
Date: 2026-05-27

## Request

Create a plan for first creating tests that validate the branch-aware ontology schemas.

## Mode Contract

Used `spells/invoke/plan.md`.

## Template/Profile Selection

Selected:

- standalone implementation-layering companion,
- standalone work-pack companion,
- medium-complexity split planning style.

Reason:

- the work is validation-first,
- it includes fixtures, validator logic, cross-system pressure examples, and readiness reporting,
- SWUs make the first execution step small enough to run without reopening schema design.

## Outputs

- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `PLAN-TRANSPORT.md`

## Decisions

- Start with fixtures before validator code.
- Keep all validation artifacts under development-only paths.
- Treat validation failures as schema gaps or fixture gaps, not as forced data edits.
- Defer JSON Schema generation until after fixture validation.

## Gaps

- Fixture format still needs implementation-time selection.
- Validator dependency policy depends on fixture format.
- Cross-system fixtures may reveal schema gaps that require another design/refine pass.

## Next Route

`task-session OVS-SWU-001`
