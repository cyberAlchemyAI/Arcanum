# TASK-001: Define Canonical Schemas And Repository Skeleton

## Objective

Create the project skeleton and canonical TypeScript schemas for the benchmark run kernel: tasks, agent invocations, evaluator profiles, oracle evidence, score results, and telemetry events.

## Layer And Slice Mapping

- Layer: L0
- Slice: S-001
- Wave: [W0](../waves/W0.md)

## Source Contracts

- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
- [../../starting-point.md](../../starting-point.md)

## Dependencies

None.

## Implementation Detail

Inputs:

- Architecture component list and interface rules.
- One representative local fixture task.

Outputs:

- Buildable project skeleton.
- Runtime-validatable schema definitions.
- Schema fixtures and unit tests.

Implementation notes:

1. Initialize the minimal orchestrator package using the repo's chosen package manager.
2. Define schema modules for `RunAttempt`, `TaskDefinition`, `AgentInvocation`, `AgentResult`, `EvaluatorProfile`, `OracleEvidence`, `ScoreResult`, and `TelemetryEvent`.
3. Add fixture data for one SWE-bench-style tech-debt task and one oracle result.
4. Validate fixtures in tests.
5. Keep all external suite fields behind generic metadata until probes confirm exact shapes.

Edge cases:

- Unknown oracle type must fail schema validation unless explicitly marked `experimental`.
- Missing fixture path or oracle command blocks L0 execution; missing repository ref blocks Docker-backed L1 execution.
- Telemetry events must preserve ordering and run id.

## Smallest Working Units

### SWU-HARNESS-001

- Goal: create the buildable project skeleton and test command.
- Dependencies: none.
- Write scope: package config, source root, test config.
- Done criteria: project installs locally and the empty test suite runs.
- Acceptance evidence: build/test command output.
- Verification: `npm test` or selected equivalent.
- Execution owner: local-fallback.
- Handoff note: return selected stack, package scripts, and any dependency constraints.

### SWU-HARNESS-002

- Goal: implement canonical run-kernel schema definitions and fixture validation tests.
- Dependencies: SWU-HARNESS-001.
- Write scope: schema modules and schema fixture tests.
- Done criteria: representative task and oracle fixtures validate; invalid fixtures fail.
- Acceptance evidence: schema test output.
- Verification: schema/unit test command.
- Execution owner: subagent.
- Handoff note: preserve names from ARCHITECTURE.md and flag any schema ambiguity.

## Synchronization Rules

SWU-HARNESS-002 may start only after the skeleton and test runner exist.

## Completion Evidence

- SWU-HARNESS-001: completed. Project skeleton and TypeScript test command are present; `npm test` passed.
- SWU-HARNESS-002: completed. Runtime-validatable schema definitions are present in `src/schemas.ts`; representative task and oracle fixtures validate; invalid task and oracle fixtures fail with useful issues.
- Verification command: `npm test`
- Latest result: pass, 2 test files, 2 passing subtests, 0 failures.
