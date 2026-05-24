# Glossary Consistency Report: Agentic Tech Debt & Optimization Harness

## Source Terms

| Term | Meaning In Source | Consistency Status | Notes |
| --- | --- | --- | --- |
| Harness | Unified benchmark orchestration and scoring system. | pass | Used as the top-level product/system boundary. |
| Orchestrator | Node.js/TypeScript control plane for tasks, state, and telemetry. | pass | Kept distinct from sandbox execution. |
| Agent Interface | Contract an autonomous coding agent fulfills. | pass | Expressed as `AgentAdapter` / `BaseAgent`. |
| Execution Sandbox | Isolated Python/Docker environment for patch application and oracle execution. | pass | Kept out of orchestrator process. |
| Oracle | Benchmark-specific correctness, smell, or performance evaluator. | pass | Normalized as `OracleResult` / evidence. |
| Trajectory Cost | Efficiency cost of the agent's repository navigation and actions. | pass | Represented by telemetry events and derived scoring. |
| Tech Debt Subset | SWE-bench cases filtered for refactor, cleanup, and performance work. | flag | Exact upstream labels must be verified. |
| SmellBench | Structural debt repair benchmark. | flag | Local integration contract must be verified before implementation. |
| PerfCodeBench | Performance optimization benchmark. | flag | Local integration contract and deterministic baseline rules must be verified. |

## Conflicts

No direct terminology conflicts were found inside [starting-point.md](starting-point.md). The flagged terms are external-contract gaps, not naming conflicts.

## Planning Impact

- Use `TaskDefinition`, `AgentAdapter`, `SandboxProfile`, `OracleEvidence`, `ScoreResult`, and `TelemetryEvent` as implementation vocabulary.
- Keep benchmark-suite names as source labels until adapters verify exact package/API names.
- Do not rename `trajectory cost` to generic runtime cost; it includes navigation/action efficiency, not only wall-clock duration.

## Gate Result

- Status: flag
- Reason: internal terminology is consistent; external benchmark terms need verification probes.
