---
template_id: invoke.architecture
template_type: architecture
status: draft
updated_at: 2026-05-23
source_contracts:
  - starting-point.md
---

# Architecture Plan: Agentic Tech Debt & Optimization Harness

## Architecture Intent

Build a deterministic benchmark harness that evaluates autonomous coding agents on technical-debt repair, architectural smell reduction, and performance optimization while preserving enough telemetry to compare both outcome quality and trajectory cost.

## Optimized Concept Boundary

The first implementation concept is the **Benchmark Run Kernel**: one normalized task fixture plus one patch artifact becomes immutable oracle evidence, a score record, and a telemetry event chain.

This kernel is smaller than the full harness but still carries the system's core behavior. Docker, live dataset ingestion, suite-specific adapters, cloud workers, and dashboards compose around it in later layers.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | [starting-point.md](starting-point.md) | yes | Foundational project blueprint and phase outline. |
| SC-002 | SWE-bench tech-debt subset | yes | Dataset ingestion and dockerized unit-test oracle; exact filter labels must be verified during implementation. |
| SC-003 | SmellBench / static-analysis oracle | yes | Structural smell-reduction suite; availability and PyExamine contract must be verified before hard integration. |
| SC-004 | PerfCodeBench runtime oracle | yes | Performance optimization suite; hardware determinism constraints are part of acceptance. |

## View 1: Context View

The harness sits between benchmark datasets, autonomous agents, and isolated execution environments.

External actors and systems:

- Benchmark operator: configures datasets, agents, run budgets, and comparison reports.
- Agent runtime: receives task definitions and repository state, then returns patches or structured diffs.
- Benchmark datasets: SWE-bench, SmellBench, and PerfCodeBench supply tasks and oracles.
- Execution substrate: Docker locally or on provisioned cloud workers runs repository setup, patch application, tests, static analysis, and performance measurements.
- Dashboard consumer: reviews outcome scores, smell/performance deltas, and trajectory telemetry.

Ownership boundary:

- The harness owns task normalization, execution orchestration, scoring, telemetry, and dashboard data.
- The harness does not own upstream benchmark definitions, agent internals, or long-term model evaluation policy.

## View 2: High-Level Structure View

Major subsystems:

- Benchmark Run Kernel: executes one normalized task attempt from patch artifact to evidence, score, and telemetry.
- Task Registry: normalizes upstream benchmark cases into one `TaskDefinition` contract.
- Agent Adapter Layer: exposes a stable `BaseAgent` interface and adapter-specific invocation rules.
- Run Orchestrator: queues tasks, allocates sandboxes, enforces budgets, and records run state.
- Evaluator Substrate: applies patches and runs oracle commands through a fixture-local evaluator in L0, then Docker-backed sandboxes in L1+.
- Oracle Integrations: wrap SWE-bench tests, SmellBench smell checks, and PerfCodeBench performance comparisons.
- Telemetry Store: records events, costs, artifacts, command results, and score components.
- Dashboard API/UI: serves aggregate and per-run views for operators.

## View 3: Low-Level Components View

Core components:

- `RunAttempt`: aggregate root for one task, agent result, evaluator profile, oracle evidence, score, and telemetry chain.
- `TaskDefinition`: canonical task schema with dataset source, repository ref, setup commands, oracle type, acceptance checks, resource limits, and scoring weights.
- `AgentInvocation`: request/response envelope containing task, repository context budget, allowed tools, timeout, returned patch, and error state.
- `RunState`: state machine for queued, preparing, invoking, applying-patch, evaluating, scoring, completed, failed, and quarantined.
- `EvaluatorProfile`: local fixture, Docker, or pinned performance worker profile with CPU, memory, filesystem, network, and timeout limits.
- `OracleResult`: normalized output for semantic correctness, smell delta, performance delta, reproducibility metadata, and raw logs.
- `TelemetryEvent`: append-only event shape for agent actions, tool calls, command spans, patches, retries, and score calculations.

Local collaboration rules:

- Dataset-specific ingestion may produce enriched metadata, but scoring must consume only normalized task and oracle contracts.
- Sandboxes return evidence, never final scores; scoring is centralized in the orchestrator.
- Dashboard reads from the telemetry and result store; it must not recompute oracle outcomes.

## View 4: Workflow Process View

Primary flow:

1. Load or ingest benchmark cases and normalize them into `TaskDefinition` records.
2. Select an agent adapter, run profile, and resource budget.
3. Prepare the evaluator substrate: fixture-local for the kernel proof, Docker or pinned workers for later layers.
4. Invoke the agent with bounded context and task instructions.
5. Receive a patch or structured diff.
6. Apply the patch through the selected evaluator substrate.
7. Execute the relevant oracle commands.
8. Normalize oracle evidence into score components.
9. Persist telemetry, artifacts, logs, and final run status.
10. Render aggregate and run-level dashboard views.

Failure and compensation paths:

- Dataset ingestion mismatch: quarantine task and record schema gap.
- Sandbox provisioning failure: retry within infrastructure budget, then mark infra-failed.
- Agent timeout or invalid patch: mark agent-failed with full trajectory evidence.
- Oracle flake: rerun only if profile allows deterministic retry; otherwise quarantine.
- Perf noise threshold breach: reject the measurement and rerun on a clean worker profile.

## View 5: Decision Flow View

Key decisions:

- Dataset classification: choose oracle integration from normalized task source and labels.
- Agent contract shape: accept patch output for L0; defer structural diff support until patch flow is stable.
- Evaluator profile: use fixture-local evaluation for the first kernel proof, Docker for repeatable repository tasks, and pinned-resource workers for performance tasks.
- Score status: pass only when required semantic oracle passes and target-specific improvement thresholds are met.
- Telemetry cost model: record raw token/tool/runtime costs first; derive aggregate cost metrics separately.

Selected outcomes:

- Start with one patch-based agent interface.
- Build the benchmark run kernel as the L0 proof before live dataset ingestion.
- Promote Docker-backed SWE-bench tech-debt ingestion to L1 once the kernel evidence model is stable.
- Add structural and performance suites behind the same `TaskDefinition` and `OracleResult` abstractions.
- Treat deterministic execution evidence as more important than dashboard breadth in early layers.

## View 6: Dependency Interface View

Internal interfaces:

- `TaskProvider.load(): TaskDefinition[]`
- `AgentAdapter.run(task, repoContext, budget): AgentResult`
- `Evaluator.evaluate(task, patch, profile): OracleEvidence`
- `OracleScorer.score(task, evidence): ScoreResult`
- `TelemetrySink.append(event): void`

External dependencies:

- Hugging Face or local dataset mirror for SWE-bench cases.
- Docker daemon or cloud container workers.
- Benchmark-specific setup scripts and oracle commands.
- Static-analysis tooling for smell reduction checks.
- Dashboard runtime and datastore.

Boundary rules:

- Agent adapters cannot access host credentials except through explicit sandbox-mounted secrets.
- Oracle integrations cannot mutate benchmark source definitions.
- PerfCodeBench runs cannot share CPU-intensive hosts with model inference or unrelated workloads.
- Raw logs remain linked to score components for auditability.

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| Deterministic execution | starting-point.md | Requires pinned environment profiles, repeatable setup, and evidence capture. |
| Multi-oracle support | starting-point.md | Requires normalized task and oracle result contracts. |
| Performance noise sensitivity | starting-point.md | Requires isolated workers and retry/quarantine policy. |
| Upstream benchmark uncertainty | source contracts | Requires integration probes before full ingestion assumptions are promoted. |
| No execution during invoke plan | invoke contract | This design only prepares implementation handoff. |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | All benchmark inputs are normalized before agent invocation. | Task Registry | Schema validation in ingestion tests. |
| R-002 | Agent output is persisted before patch application. | Agent Adapter Layer | Telemetry event and artifact check. |
| R-003 | Evaluator evidence is immutable after scoring. | Evaluator Substrate, Telemetry Store | Append-only evidence records. |
| R-004 | Perf runs use pinned-resource profiles. | PerfCodeBench oracle | Profile validation before execution. |
| R-005 | Score calculation is centralized. | Oracle Integrations | Scorers consume normalized evidence only. |

## Decision Log

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-001 | Use Node.js/TypeScript for orchestration. | Node.js, Python, mixed control plane | Matches starting blueprint and keeps agent/dash contracts typeable. |
| D-002 | Use Python/Docker for sandboxes and benchmark scripts. | In-process execution, Docker, VM-only | Docker isolates target repos while preserving common benchmark tooling. |
| D-003 | Normalize all suites through `TaskDefinition`. | Per-suite bespoke runners, shared schema | Enables comparable telemetry and scoring. |
| D-004 | Start with a fixture-local benchmark run kernel. | Docker first, SWE-bench first, all suites at once | Proves the core run model before infrastructure and external dataset risk. |
| D-005 | Treat SmellBench and PerfCodeBench contracts as verification-gated. | Assume direct integration, defer entirely | Avoids baking unverified external APIs into the core architecture. |
| D-006 | Promote Docker-backed evaluation to L1. | L0 Docker requirement, fixture-only forever | Keeps L0 small while preserving the production substrate path. |

## Risks

| Risk ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | Upstream benchmark schemas differ from the blueprint assumptions. | Add integration probes before full adapters. | Harness maintainer |
| RK-002 | Performance metrics are noisy on shared hardware. | Isolate PerfCodeBench workers and enforce retry/quarantine thresholds. | Infrastructure owner |
| RK-003 | Agent trajectory telemetry is inconsistent across adapters. | Define a minimum event envelope and adapter compliance tests. | Orchestrator owner |
| RK-004 | Dashboard work races ahead of reliable scoring. | Gate dashboard slices behind persisted scoring evidence. | Product/UX owner |

## Downstream Planning Notes

- Implementation-plan inputs: this architecture, `starting-point.md`, and verified benchmark integration probes.
- Work-pack implications: medium complexity, split work-pack, SWU-level tasks.
- Validation implications: schema tests, fixture-local kernel smoke tests, Docker repeatability tests, oracle fixture tests, and deterministic perf-profile checks.

## Design Transport Notes

Carry this design into plan mode as the source design reference. Do not promote unverified SmellBench or PerfCodeBench integration details beyond probe tasks until their local APIs, fixtures, and oracle commands are confirmed.

## Gate Result

- Status: flag
- Reason: six design views are covered and planning can proceed, but external benchmark availability and exact suite contracts remain verification-gated target-artifact gaps.
