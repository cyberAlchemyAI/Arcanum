---
module: agentic-tech-debt-optimization-harness
version: current
status: draft
updatedAt: 2026-05-23
docType: implementation-layering
---

# Implementation Layering: Agentic Tech Debt & Optimization Harness

## Purpose

Define the smallest evidence-building path from a fixture-local benchmark run kernel to a multi-oracle benchmark system with reliable telemetry and operator visualization.

## Source Contract

- Invoke source: [starting-point.md](starting-point.md)
- Design source: [ARCHITECTURE.md](ARCHITECTURE.md)
- Glossary consistency: [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md)
- Concept optimization: [DISTILL-OPTIMIZATION.md](DISTILL-OPTIMIZATION.md)

## Target And Scope

- Target: Agentic Tech Debt & Optimization Harness
- Scope: benchmark infrastructure and evaluation workflow
- Current state: greenfield planning baseline

## Layer Boundary Rule

Each layer answers one promotion question:

```text
After this layer, we know whether the next broader benchmark claim is justified by evidence.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether the benchmark run kernel can turn one local task fixture and one patch artifact into oracle evidence, score, and telemetry deterministically. | One fixture-local task run through task schema, mock or local agent adapter, evaluator, oracle result, score, and telemetry record. | Canonical schemas, patch-based agent contract, fixture-local evaluator, semantic oracle fixture, raw telemetry. | Docker, live SWE-bench ingestion, SmellBench, PerfCodeBench, cloud workers, dashboard polish, multi-agent comparison. | Passing schema tests, two fixture-local kernel smoke runs, persisted score and telemetry artifact. | Continue only if the kernel path is reproducible twice from clean state. |
| L1 | After this layer, we know whether the kernel survives Docker-backed repository evaluation and SWE-bench tech-debt ingestion across multiple tasks. | Docker evaluator plus dataset ingestion and batch runner for a small curated SWE-bench tech-debt sample. | Docker profile, ingestion filters, task queue, retry/quarantine policy, result store, CLI report. | Structural smell and perf suites, full UI, large-scale scheduling. | Docker smoke report, batch fixture report with pass/fail, infra failures separated from agent failures, telemetry completeness check. | Harden if ingestion labels, Docker setup, and oracle commands are stable. |
| L2 | After this layer, we know whether structural and performance oracles fit the shared task/evidence model without corrupting determinism. | SmellBench probe adapter and PerfCodeBench probe adapter behind normalized `OracleEvidence`. | Static-analysis oracle wrapper, perf profile constraints, score composition, deterministic worker checks. | Broad benchmark coverage, long-run cloud scaling, public reporting. | Probe reports for each suite, perf noise threshold evidence, static-analysis delta evidence. | Scale only if suite-specific evidence remains comparable through the shared model. |
| L3 | After this layer, we know whether the harness can support repeatable operator-facing benchmark campaigns. | Packaged runner plus dashboard for configured agents and benchmark suites. | Dashboard, campaign config, cloud/local worker profiles, artifact retention, release docs. | Marketplace-style benchmark sharing, advanced analytics, hosted multi-tenant operation. | End-to-end campaign report, dashboard audit trail, reproducible setup documentation. | Pilot if campaign replay produces consistent scores and telemetry. |

## Non Regression Guardrails

- Later layers must preserve L0 kernel reproducibility and schema stability.
- Docker integration must wrap the kernel instead of replacing its evidence contract.
- External benchmark assumptions remain probe-gated until local integration evidence exists.
- Performance claims must cite isolated worker evidence.
- Dashboard metrics must link back to immutable run evidence.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the unified task, patch, evaluator, oracle, score, and telemetry path works at all.
- Major deferred scope: Docker-backed live repositories, SmellBench, PerfCodeBench, cloud scaling, and dashboard beyond minimal report output.
