---
module: agentic-tech-debt-optimization-harness
version: current
status: draft
updatedAt: 2026-05-26
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
- Current state: closed after fixture-local kernel, Docker/local mirror, batch, official SWE-bench Lite smoke evidence, completed SmellBench real score evidence, completed PerfCodeBench real score evidence, campaign report read-model evidence, dashboard-ready data contract evidence, and W0-W3 closure audit evidence.

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
| L2 | After this layer, we know whether structural and performance benchmarks can produce real upstream-derived score artifacts without corrupting determinism. | SmellBench and PerfCodeBench contract probes, followed by one pinned real smoke per benchmark when runnable upstream artifacts exist. | Upstream artifact verification, runner/scoring surface discovery, candidate manifest contract, candidate-to-benchmark-input transforms, raw result/log import, local score artifacts derived from upstream output, static-analysis evidence, perf profile constraints, deterministic worker checks. | Broad benchmark coverage, long-run cloud scaling, public reporting, any local-mirror-only substitutes. | Contract probe reports for each suite; real smoke score artifacts or precise block records; perf noise threshold evidence; structural smell effectiveness/false-positive/net-impact evidence. | Scale only if each suite can produce auditable upstream-derived evidence through the shared model; otherwise keep the suite blocked with exact missing upstream/runtime conditions. |
| L3 | After this layer, we know whether the harness can support repeatable operator-facing benchmark campaigns. | Packaged runner plus dashboard for configured agents and benchmark suites. | Dashboard, campaign config, cloud/local worker profiles, artifact retention, release docs. | Marketplace-style benchmark sharing, advanced analytics, hosted multi-tenant operation. | End-to-end campaign report, dashboard audit trail, reproducible setup documentation. | Pilot if campaign replay produces consistent scores and telemetry. |

## Non Regression Guardrails

- Later layers must preserve L0 kernel reproducibility and schema stability.
- Docker integration must wrap the kernel instead of replacing its evidence contract.
- External benchmark assumptions remain probe-gated until local integration evidence exists.
- Performance claims must cite isolated worker evidence.
- Dashboard metrics must link back to immutable run evidence.

## Recommended Next Layer

- Next layer: new work-pack or scale-up planning.
- Key decision unlocked: the pilot harness has enough reproducibility and traceability evidence to plan broader benchmark coverage or operator hardening from a closed baseline.
- Default next unit: none in this work-pack.
- Readiness boundary: SmellBench and PerfCodeBench both have real smoke score artifacts derived from upstream or verified runner outputs, the campaign report links six persisted runs to score/evidence artifacts with zero evidence gaps, dashboard-ready data exposes summary, run details, score components, and telemetry counts, and `TASK-VERIFY` confirms reproducibility/traceability closure.
- Major deferred scope: broad benchmark coverage, campaign scheduling, cloud-scale workers, and dashboard beyond report-linked evidence.
