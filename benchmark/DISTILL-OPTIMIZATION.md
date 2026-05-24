# Distill Result: Agentic Tech Debt & Optimization Harness

## Target Context

Optimize the existing architecture and plan for a greenfield benchmark harness so the first implementation step is small enough to execute, but still proves the central system behavior.

## Objective And Output Artifact

- Objective: reduce the plan to the smallest coherent concept unit that can prove the harness architecture.
- Output artifact: Distill optimization note plus updates to architecture, layering, work-pack, execution-pack, and L0 task contracts.
- Mode and budget: Standard; one proposal track, Proposer/Balancer role simulation, two recursive rounds.

## Discovery Baseline

Existing artifacts already establish a strong architecture: normalized task contracts, patch-based agent interface, evaluator/oracle evidence, telemetry, and later dashboarding.

The main optimization pressure is that the first layer was still too broad. It required Docker, sandbox behavior, scoring, schemas, agent patching, and telemetry in one initial proof. That makes L0 implementation brittle because infrastructure failure can hide whether the core run model is sound.

## Role Conversation Trace

| Round | Proposer Claim | Evidence Or Assumption | Balancer Objection | Reconciliation |
| --- | --- | --- | --- | --- |
| 1 | The smallest useful unit is one complete benchmark run from task to score. | The architecture's value depends on comparing agent outcome and trajectory cost. | Too broad if it requires Docker and external dataset access immediately. | Revise to a fixture-local benchmark run kernel. |
| 2 | The smallest coherent unit is a benchmark run kernel: task fixture, patch artifact, fixture evaluator, oracle evidence, score, telemetry. | This preserves the full semantic loop without external infrastructure. | It may underrepresent production sandbox constraints. | Accept, with Docker moved to L1 as the repeatability/infrastructure promotion proof. |

## Current Smallest Coherent Unit

**Benchmark Run Kernel**

Responsibility: turn one normalized local task fixture and one patch artifact into immutable oracle evidence, a score record, and telemetry events.

Inputs:

- `TaskDefinition` fixture
- patch artifact from deterministic mock/local adapter
- evaluator profile
- scoring policy

Outputs:

- `OracleEvidence`
- `ScoreResult`
- `TelemetryEvent` chain
- artifact links for patch and raw command output

## Optimization Point

The kernel is the best first unit because it keeps the system's meaning intact: it still proves the benchmark loop. It removes premature Docker/cloud/dataset concerns from the first proof, so failures become easier to classify.

## Distill Layer Map

| Layer | Concept | Status |
| --- | --- | --- |
| Broad system | Multi-suite agent benchmark harness | Target product. |
| Architecture unit | Normalized run orchestration over task, agent, evaluator, oracle, score, telemetry | Stable design boundary. |
| Selected unit | Benchmark Run Kernel | First coherent implementation unit. |
| Smaller fragments | schema-only, adapter-only, telemetry-only | Too small; do not prove benchmark behavior alone. |

## Technique Pack Trace

| Technique | Activation Reason | Output | Decision |
| --- | --- | --- | --- |
| Abstraction-level guard | L0 mixed business proof and infrastructure proof. | Separate run kernel from sandbox substrate. | accepted |
| Recomposition proof | Need to show the kernel scales back to full harness. | Kernel is wrapped by Docker/SWE adapters in L1 and suite probes in L2. | accepted |
| Evolution profile | Future suite adapters are expected. | Preserve generic task/evidence interfaces, defer suite-specific plugins. | accepted |
| Cognitive load check | Work-pack had many first-step concepts. | Start at `SWU-HARNESS-001` with skeleton, then kernel fixture path. | accepted |
| Premortem | Likely failure is infrastructure blocking core model learning. | Keep fixture-local evaluator in L0; promote Docker only after kernel passes. | accepted |

## Closure And Recomposition Proof

The kernel closes because it has named inputs, outputs, state transitions, and evidence. It recomposes upward by replacing the fixture evaluator with Docker-backed evaluators, then adding dataset providers and suite-specific oracle adapters without changing the run evidence contract.

## Evolution Profile

Expected evolution:

- more dataset providers,
- more evaluator profiles,
- suite-specific oracle adapters,
- campaign reporting,
- later dashboard UI.

Smallest extension boundary:

- keep `TaskProvider`, `EvaluatorProfile`, `OracleEvidence`, and `TelemetryEvent` as interfaces;
- keep suite-specific fields in metadata or typed extension blocks until probe evidence justifies promotion.

## Deferred Complexity

- Docker sandboxing in L0: deferred to L1 because infrastructure determinism is real work but not required to prove the kernel.
- Live SWE-bench ingestion in L0: deferred to L1 because external dataset shape can obscure the core run model.
- SmellBench and PerfCodeBench adapters: deferred to L2 probe tasks.
- Dashboard UI: deferred to L3; static report/read model comes first.

## Tension Ledger

| Tension | Resolution |
| --- | --- |
| Need determinism, but Docker adds early setup risk. | L0 uses fixture-local evaluator; L1 proves Docker repeatability. |
| Need a complete run, but schemas alone are simpler. | Keep the complete kernel because schema-only does not prove benchmark behavior. |
| Need future multi-suite support, but not plugin architecture too early. | Preserve interface boundaries; defer plugin mechanics until probes. |

## Frame-Expiry Note

This optimization point expires if the first implementation must run real upstream benchmark repositories immediately. In that case, Docker becomes part of L0 again and the first SWU should be re-planned around environment provisioning.

## Navigation Guide

Start with the revised `SWU-HARNESS-001` and `SWU-HARNESS-002`, then implement the fixture-local run kernel before Docker. Use the kernel's evidence shape as the source of truth for later SWE-bench, SmellBench, PerfCodeBench, and dashboard work.

## Next Route

task-session
