# Fixture: INV-PLAN-SPLIT-001

## Scenario

Medium-complexity plan from approved design outputs.

## User Request

Plan implementation for a Mars habitat supply approval workflow that needs staged rollout and governance checks.

## Inputs

- Approved design artifact: `artifacts/mars-habitat-supply/ARCHITECTURE.md`
- Source design refs: source contracts, six-view design bundle, dependency/interface map, glossary consistency report, and design transport report.
- Implementation objective: deliver supply request intake, approval state management, audit notes, and operator review handoff.
- Delivery boundary: one repository, no irreversible migration, staged release required.
- Task estimate: eight tasks.
- Output artifacts: implementation plan, implementation-layering artifact, split work-pack, and execution-pack handoff.
- Implementation-layering companion: approved to create global L0-L3 artifact.
- Work-pack companion: approved to create split work-pack.
- Validation strategy: unit checks, fixture replay, governance checks, and release-readiness evidence.
- Lifecycle owner approval: L2 planning approved.

## Expected

- Phase status: `pass`
- Complexity: `medium`
- Work-pack output mode: `split`
- Per-layer planning: L0, L1, L2, L3
- Execution-pack handoff: required
- Next route: `task-session`
