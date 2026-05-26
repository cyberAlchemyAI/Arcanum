# TASK-002: Implement Patch-Based Agent Invocation And Fixture-Local Run Kernel

## Objective

Implement the L0 execution path: invoke a patch-producing agent adapter, persist its result, apply the patch through a fixture-local evaluator, run the semantic oracle, score the result, and record normalized evidence.

## Layer And Slice Mapping

- Layer: L0
- Slice: S-002
- Wave: [W0](../waves/W0.md)

## Source Contracts

- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)

## Dependencies

- TASK-001

## Implementation Detail

Inputs:

- Validated `TaskDefinition`.
- Agent adapter config.
- Local fixture repository or evaluator fixture.

Outputs:

- Typed `AgentResult` with patch artifact path.
- Fixture-local evaluator result.
- Normalized `OracleEvidence`.
- `ScoreResult`.
- Telemetry event chain.

Implementation notes:

1. Define `AgentAdapter.run(task, context, budget)`.
2. Implement a deterministic mock/local adapter first so L0 does not depend on a live model.
3. Persist the returned patch before applying it.
4. Implement evaluator execution behind an interface that uses a fixture-local evaluator in L0 and can later wrap Docker.
5. Apply patch, run configured oracle command, capture exit code, stdout/stderr paths, and duration.
6. Convert raw command evidence into `OracleEvidence`, produce `ScoreResult`, and append telemetry events for each state transition.

Edge cases:

- Invalid patch marks agent failure, not infra failure.
- Fixture setup failure marks infra failure.
- Oracle command timeout marks oracle failure with timeout evidence.
- Missing telemetry event for a completed stage blocks promotion.

## Smallest Working Units

### SWU-HARNESS-003

- Goal: implement the patch-based `AgentAdapter` contract and deterministic mock adapter.
- Dependencies: SWU-HARNESS-002.
- Write scope: agent adapter modules and tests.
- Done criteria: mock adapter returns a typed patch result and error states are tested.
- Acceptance evidence: adapter unit tests.
- Verification: adapter unit test command.
- Execution owner: subagent.
- Handoff note: do not add model-specific API assumptions in L0.

### SWU-HARNESS-004

- Goal: implement fixture-local patch application, oracle execution, scoring, and telemetry persistence for a fixture task.
- Dependencies: SWU-HARNESS-003.
- Write scope: run kernel, fixture evaluator, oracle runner, scorer, telemetry sink, fixture tests.
- Done criteria: same fixture run succeeds twice from clean state with matching score status.
- Acceptance evidence: two clean smoke-run outputs and telemetry files.
- Verification: kernel smoke test twice.
- Execution owner: local-fallback.
- Handoff note: Docker is intentionally out of L0; report fixture-local evaluator constraints and any future Docker assumptions.

## Synchronization Rules

No Docker-backed or live external benchmark ingestion until SWU-HARNESS-004 proves the fixture-local kernel path.

## Completion Evidence

- SWU-HARNESS-003: completed. Patch-based `AgentAdapter` contract and deterministic `MockAgentAdapter` are present in `src/agent-adapter.ts`.
- SWU-HARNESS-003 validation: `npm test` passed with adapter tests covering patch, no-patch, error, and timeout states.
- SWU-HARNESS-004: completed. Fixture-local `runBenchmarkKernel` copies a clean fixture workspace, persists the agent patch artifact, applies it with `patch`, runs the semantic oracle, writes normalized oracle evidence, scores centrally, and appends telemetry.
- SWU-HARNESS-004 validation: `npm test` passed, and `npm run smoke:kernel` produced two passing clean runs: `kernel-smoke-001` and `kernel-smoke-002`.
- SWU-HARNESS-004 evidence paths: `artifacts/kernel-smoke-001/telemetry.jsonl`, `artifacts/kernel-smoke-001/score-result.json`, `artifacts/kernel-smoke-002/telemetry.jsonl`, and `artifacts/kernel-smoke-002/score-result.json`.
- Fixture-local evaluator constraints: L0 uses local filesystem fixture copies plus POSIX `patch`; Docker-backed repository setup and live benchmark ingestion remain gated to TASK-003.
