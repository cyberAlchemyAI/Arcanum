# TASK-003: Add Docker-Backed SWE-bench Tech-Debt Ingestion And Batch Runner

## Objective

Wrap the L0 run kernel with Docker-backed repository evaluation, integrate a small SWE-bench tech-debt sample into the normalized task registry, and run it in batch mode.

## Layer And Slice Mapping

- Layer: L1
- Slice: S-003
- Wave: [W1](../waves/W1.md)

## Source Contracts

- [../../starting-point.md](../../starting-point.md)
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)

## Dependencies

- TASK-001
- TASK-002
- B-001 resolved or explicitly scoped to a local fixture mirror.

## Implementation Detail

Inputs:

- Docker evaluator setup contract.
- SWE-bench dataset access path or local mirror.
- Filter labels or equivalent metadata for refactor, cleanup, and performance tasks.
- L0 task schema and sandbox runner.

Outputs:

- SWE-bench task provider.
- Docker evaluator profile.
- Small curated sample manifest.
- Batch runner and report.

Implementation notes:

1. Probe available dataset fields before coding final filters.
2. Implement a Docker evaluator that preserves the L0 `OracleEvidence` and `ScoreResult` contract.
3. Map repository ref, setup commands, patch target, oracle commands, and labels into `TaskDefinition`.
4. Preserve upstream identifiers in metadata.
5. Add a sample manifest small enough for local repeatability.
6. Run batch jobs with infra failure and agent failure as separate statuses.

Edge cases:

- Missing labels require an explicit alternate filter and gap entry.
- Docker/repository setup failures must not count as agent failures.
- Flaky oracle behavior should quarantine the task.

## Smallest Working Units

### SWU-HARNESS-005

- Goal: implement Docker evaluator probe plus SWE-bench provider probe and sample normalization.
- Dependencies: SWU-HARNESS-004.
- Write scope: Docker evaluator, SWE-bench provider, sample manifest, ingestion tests.
- Done criteria: a small sample normalizes to valid `TaskDefinition` records and one Docker-backed fixture path runs.
- Acceptance evidence: Docker smoke output and ingestion fixture test.
- Verification: provider and Docker evaluator test command.
- Execution owner: subagent.
- Handoff note: record exact dataset path and labels discovered.

### SWU-HARNESS-006

- Goal: implement sample batch runner and result summary.
- Dependencies: SWU-HARNESS-005.
- Write scope: batch runner, result store, report generation.
- Done criteria: batch report separates pass, fail, infra-fail, timeout, and quarantine statuses.
- Acceptance evidence: sample batch report.
- Verification: batch smoke command.
- Execution owner: local-fallback.
- Handoff note: include raw artifact paths in the report for audit.

## Synchronization Rules

Do not begin full SWE-bench ingestion until the small sample batch has stable statuses.

## Completion Evidence

- Sample manifest checked in or generated deterministically.
- Batch report links every task to score and telemetry evidence.
