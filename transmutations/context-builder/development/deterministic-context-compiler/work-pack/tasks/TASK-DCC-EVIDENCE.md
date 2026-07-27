# TASK-DCC-EVIDENCE: Paired Reusable-Behavior Evidence

## Task Objective

Run a paired baseline/candidate experiment over the same task, obligations, and
source snapshot before making any cost or reusable-behavior claim.

## Mapping

- Layer: L3
- Slice: S-007
- Wave: W5
- Dependencies: SWU-DCC-006
- Blockers: `G-003` and `G-005`
- Selection: `none`

## SWU-DCC-007

### Primary Behavior

Create and run one Experiment Harness profile comparing current Context Builder
assembly with compiler-assisted assembly under coverage parity.

### Independent Acceptance Boundary

The paired receipt records identical task scope and source snapshot, obligation
coverage parity, selected-source differences, compile duration, cache state,
and actual usage when available. It makes no percentage claim when actual usage
is missing.

### Split Analysis

Profile authoring and live execution were considered separately. They remain
one evidence SWU because a profile without a run cannot support reusable
behavior and an unbound run cannot be reproduced. Canonical integration remains
separate.

### Source Anchors

- `SPEC.md`: Acceptance Criteria and Evidence Ceiling
- `ARCHITECTURE.md`: Experiment Harness interface and Significant Behavior Scenario
- `WITNESS-CONTRACTS.md`: Live Evidence Contract

### Related Context

- [Validation strategy](../../VALIDATION-STRATEGY.md)
- [Cross-task gaps](../shared/GAPS.md)
- All passing SWU-DCC-001 through SWU-DCC-006 owner receipts

### Exact Write Scope

1. `transmutations/context-builder/development/deterministic-context-compiler/experiment/experiment-profile.json`
2. `transmutations/context-builder/development/deterministic-context-compiler/experiment/baseline-run.json`
3. `transmutations/context-builder/development/deterministic-context-compiler/experiment/candidate-run.json`
4. `transmutations/context-builder/development/deterministic-context-compiler/experiment/comparison-receipt.json`
5. `transmutations/context-builder/development/deterministic-context-compiler/experiment/REVIEW.md`
6. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-007/baseline.json`
7. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-007/task-session-receipt.json`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-007/owner-receipt.json`

### Done Criteria

- Profile binds one task/SWU, source snapshot, obligations, and both routes.
- Both runs complete or the comparison receipt names exact residue.
- Coverage and authority-context parity are reviewed.
- Actual prompt usage is recorded only if returned by the runtime.
- Review separates implementation, reproducibility, savings, approval, and
  lifecycle readiness.
- Public scan passes.

### Acceptance Evidence And Validation

Use the Experiment Harness validator for the profile and both runs. Recompute
source and obligation digests, compare coverage, validate usage provenance, and
record the human sufficiency/noise review.

### Execution Owner And Expected Result

- Lifecycle owner: Sigil Development
- Execution owner after selection: one bounded Task Session operating the
  Experiment Harness
- Expected result: evidence either supports a bounded reuse/cost claim or keeps
  the claim explicitly unproven

## Closeout Synchronization

- Shared protocol: [CLOSEOUT-CONTRACT.md](../shared/CLOSEOUT-CONTRACT.md)
- Baseline: exact eight-target inventory above
- Allowed deltas: `artifact_added`, `evidence_added`, `status_changed`
- Owner validation: validate profile/run schemas, coverage parity, source
  digest equality, usage provenance, and review
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-007/owner-receipt.json`
- Successor: `SWU-DCC-008`; selected false

## Completion Evidence

The task closes with the owner receipt even when savings remain unproven,
provided residue is explicit. A blocked reusable-behavior result prevents
SWU-DCC-008 eligibility.
