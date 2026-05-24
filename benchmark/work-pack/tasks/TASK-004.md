# TASK-004: Probe SmellBench And PerfCodeBench Adapters

## Objective

Verify that structural smell and performance benchmark suites can be represented through the same task and oracle evidence model before implementing broad integrations.

## Layer And Slice Mapping

- Layer: L2
- Slice: S-004
- Wave: [W2](../waves/W2.md)

## Source Contracts

- [../../starting-point.md](../../starting-point.md)
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)

## Dependencies

- TASK-003
- B-002 resolved for SmellBench.
- B-003 resolved for PerfCodeBench.

## Implementation Detail

Inputs:

- Verified SmellBench package/API or local fixture.
- Verified PerfCodeBench package/API or local fixture.
- Existing `TaskDefinition` and `OracleEvidence` schemas.

Outputs:

- Structural oracle probe report.
- Performance oracle probe report.
- Schema extension proposal only if the current evidence model is insufficient.

Implementation notes:

1. Build probes before full adapters.
2. For structural probes, capture baseline smell score, post-patch smell score, static-analysis command, and delta.
3. For performance probes, capture baseline runtime, candidate runtime, repetitions, worker profile, threshold, and noise status.
4. Normalize both into `OracleEvidence` without suite-specific score logic leaking into the orchestrator.
5. Block full adapter work if evidence cannot be represented without a schema decision.

Edge cases:

- Structural smell reduction without semantic correctness should not be scored as full pass.
- Performance speedup with failing tests should not be scored as full pass.
- Noisy performance measurements must be rerun or quarantined.

## Smallest Working Units

### SWU-HARNESS-007

- Goal: produce a SmellBench probe adapter report.
- Dependencies: SWU-HARNESS-006 and B-002.
- Write scope: structural oracle probe files and report.
- Done criteria: smell delta maps to normalized oracle evidence.
- Acceptance evidence: probe report with command, raw output, and normalized evidence.
- Verification: reviewable probe report.
- Execution owner: manual.
- Handoff note: include exact package/API and static-analysis command discovered.

### SWU-HARNESS-008

- Goal: produce a PerfCodeBench probe adapter report.
- Dependencies: SWU-HARNESS-006 and B-003.
- Write scope: performance oracle probe files and report.
- Done criteria: perf delta maps to normalized oracle evidence with deterministic profile metadata.
- Acceptance evidence: probe report with repetitions, baseline, candidate, threshold, and noise status.
- Verification: reviewable probe report.
- Execution owner: manual.
- Handoff note: run only on an isolated worker profile.

## Synchronization Rules

SWU-HARNESS-007 and SWU-HARNESS-008 may run in parallel after L1 because their write scopes are disjoint.

## Completion Evidence

- Both probe reports either pass or record a schema/blocker decision.
