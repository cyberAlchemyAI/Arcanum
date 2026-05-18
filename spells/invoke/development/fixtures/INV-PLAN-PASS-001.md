# Fixture: INV-PLAN-PASS-001

## Scenario

Low-complexity plan from approved design outputs.

## User Request

Plan implementation for a Mars sample catalog import review slice from approved design outputs.

## Inputs

- Approved design artifact: `artifacts/mars-sample-catalog/ARCHITECTURE.md`
- Source design refs: source contracts, six-view design bundle, glossary consistency report, and design transport report.
- Implementation objective: create a bounded import review slice that validates sample records before catalog acceptance.
- Delivery boundary: one module, no cross-repository changes, no runtime migration, no durable-state migration.
- Task estimate: four tasks.
- Output artifacts: implementation plan and work-pack.
- Implementation-layering companion: approved to create global L0-L3 artifact.
- Work-pack companion: approved to create single-file work-pack.
- Validation strategy: fixture replay and markdown contract checks.
- Lifecycle owner approval: L2 planning approved.

## Expected

- Phase status: `pass`
- Complexity: `low`
- Work-pack output mode: `single-file`
- Per-layer planning: compact layer mapping
- Next route: `task-session`

