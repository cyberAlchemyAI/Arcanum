---
module: agentic-tech-debt-optimization-harness
version: current
status: draft
updatedAt: 2026-05-23
docType: work-pack
---

# WORK-PACK: Agentic Tech Debt & Optimization Harness

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for bounded L0 execution; later layers remain evidence-gated. |
| complexity | medium | Multiple subsystems, external suite adapters, Docker execution, and telemetry. |
| outputMode | split | Required for medium complexity. |
| executionPackRef | [work-pack/EXECUTION-PACK.md](work-pack/EXECUTION-PACK.md) | Wave choreography and parallelization boundaries. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decision boundaries. |
| activeLayerWindow | L0 | Start with the benchmark run kernel proof. |
| lastUpdatedAt | 2026-05-23 | Initial invoke plan. |
| readinessProfile | pilot | Target is a reproducible internal benchmark harness. |

## Objective Summary

- Objective: implement a deterministic benchmark harness that can normalize agentic tech-debt tasks, invoke patch-producing agents, evaluate patches through a stable evaluator contract, score oracle evidence, and expose telemetry for later dashboarding.
- Primary inputs: [starting-point.md](starting-point.md), [ARCHITECTURE.md](ARCHITECTURE.md), [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md), [DISTILL-OPTIMIZATION.md](DISTILL-OPTIMIZATION.md).
- Success condition: L0 is complete when one representative local fixture can run twice from clean state with the same task schema, patch application path, oracle status, score record, and telemetry event chain.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Architecture views | Task contracts | Each major subsystem becomes a task with SWUs. |
| Layer decisions | Waves | Waves W0-W3 map to L0-L3 promotion questions. |
| External benchmark gaps | Blockers and probe tasks | SmellBench and PerfCodeBench stay probe-gated until verified. |
| Validation strategy | Gate checks | Every slice has command or reviewable evidence. |
| Agent interface decision | TASK-002 | Patch-based adapter is the L0 execution contract. |
| Concept optimization | L0 boundary | Docker and live dataset access are deferred until after the run kernel passes. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Canonical run-kernel schemas exist with tests. | L0 | [W0](work-pack/waves/W0.md) | none | Schema/unit tests pass. |
| S-002 | One patch-based agent invocation can be evaluated by the fixture-local run kernel. | L0 | [W0](work-pack/waves/W0.md) | S-001 | Kernel smoke test passes twice from clean state. |
| S-003 | Docker-backed SWE-bench tech-debt ingestion and batch evaluation work for a small sample. | L1 | [W1](work-pack/waves/W1.md) | S-001, S-002 | Docker smoke plus batch report separates pass/fail/infra/quarantine. |
| S-004 | Structural and performance oracle probes fit the shared evidence model. | L2 | [W2](work-pack/waves/W2.md) | S-003 | Probe reports with normalized evidence and deterministic checks. |
| S-005 | Operator campaign reporting and dashboard-ready API are available. | L3 | [W3](work-pack/waves/W3.md) | S-004 | Replayable campaign report and dashboard audit trail. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-001](work-pack/tasks/TASK-001.md) | Define canonical schemas and repository skeleton. | L0 | medium | [W0](work-pack/waves/W0.md) | Architecture views 2, 3, 6 | pass | completed |
| [TASK-002](work-pack/tasks/TASK-002.md) | Implement patch-based agent invocation and fixture-local run kernel. | L0 | medium | [W0](work-pack/waves/W0.md) | Architecture views 3, 4 | ready | not-started |
| [TASK-003](work-pack/tasks/TASK-003.md) | Add Docker-backed SWE-bench tech-debt ingestion and batch runner. | L1 | medium | [W1](work-pack/waves/W1.md) | starting-point.md phase 2 | ready-after-L0 | not-started |
| [TASK-004](work-pack/tasks/TASK-004.md) | Probe SmellBench and PerfCodeBench adapters. | L2 | medium | [W2](work-pack/waves/W2.md) | starting-point.md phase 3 | ready-after-TASK-003 | not-started |
| [TASK-005](work-pack/tasks/TASK-005.md) | Build telemetry reporting and dashboard-ready API. | L3 | medium | [W3](work-pack/waves/W3.md) | starting-point.md phase 4 | ready-after-TASK-004 | not-started |
| TASK-VERIFY | Verify reproducibility, traceability, and plan closure. | L0-L3 | medium | W0-W3 | all artifacts | ready-after-implementation | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source | Dependencies | Write Scope | Done Criteria | Validation | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-HARNESS-001 | [TASK-001](work-pack/tasks/TASK-001.md) | ARCHITECTURE.md | none | package config, source skeleton | Project builds with empty modules. | `npm test` passed | local-fallback | completed |
| SWU-HARNESS-002 | [TASK-001](work-pack/tasks/TASK-001.md) | ARCHITECTURE.md | SWU-HARNESS-001 | schema modules | Schemas validate representative fixtures. | `npm test` passed | subagent | completed |
| SWU-HARNESS-003 | [TASK-002](work-pack/tasks/TASK-002.md) | ARCHITECTURE.md | SWU-HARNESS-002 | agent adapter modules | Patch-based adapter returns typed result. | `npm test` passed | subagent | completed |
| SWU-HARNESS-004 | [TASK-002](work-pack/tasks/TASK-002.md) | ARCHITECTURE.md | SWU-HARNESS-003 | run kernel, fixture evaluator, oracle runner, telemetry sink | Clean fixture patch is applied and scored twice. | kernel smoke test twice | local-fallback | ready |
| SWU-HARNESS-005 | [TASK-003](work-pack/tasks/TASK-003.md) | starting-point.md | SWU-HARNESS-004 | Docker evaluator and SWE-bench provider | Small sample normalizes to `TaskDefinition` and one Docker evaluation path runs. | Docker smoke plus ingestion fixture test | subagent | ready-after-L0 |
| SWU-HARNESS-006 | [TASK-003](work-pack/tasks/TASK-003.md) | starting-point.md | SWU-HARNESS-005 | batch runner, result store | Batch run records agent, oracle, and infra states separately. | sample batch report | local-fallback | ready-after-SWU-HARNESS-005 |
| SWU-HARNESS-007 | [TASK-004](work-pack/tasks/TASK-004.md) | ARCHITECTURE.md | SWU-HARNESS-006 | structural oracle probe | Smell evidence maps to normalized oracle result. | probe report | manual | blocked-until-suite-verified |
| SWU-HARNESS-008 | [TASK-004](work-pack/tasks/TASK-004.md) | ARCHITECTURE.md | SWU-HARNESS-006 | performance oracle probe | Perf evidence includes profile and noise threshold metadata. | probe report | manual | blocked-until-suite-verified |
| SWU-HARNESS-009 | [TASK-005](work-pack/tasks/TASK-005.md) | ARCHITECTURE.md | SWU-HARNESS-006 | telemetry/reporting modules | Run report links scores to immutable evidence. | report snapshot review | subagent | ready-after-L1 |
| SWU-HARNESS-010 | [TASK-005](work-pack/tasks/TASK-005.md) | ARCHITECTURE.md | SWU-HARNESS-009 | dashboard API/UI | Operator can inspect per-run status and aggregate scores. | UI/API smoke check | local-fallback | ready-after-SWU-HARNESS-009 |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | TASK-003 | Exact SWE-bench tech-debt labels, access path, and Docker setup contract must be verified. | Harness maintainer | Run ingestion and Docker evaluator probe against local or remote dataset mirror. | before L1 |
| B-002 | TASK-004 | SmellBench local package/API, fixtures, and static-analysis command are unverified. | Harness maintainer | Create probe spike before adapter implementation. | before L2 |
| B-003 | TASK-004 | PerfCodeBench deterministic baseline and worker requirements are unverified. | Infrastructure owner | Create pinned-resource probe profile and noise policy. | before L2 |

## Gate Checks

1. L0 execution may begin with TASK-001 and TASK-002 only.
2. L1 cannot begin until L0 fixture-local kernel smoke evidence exists.
3. L2 cannot begin until B-002 and B-003 have probe evidence.
4. L3 cannot begin until score records and telemetry are stable enough to display without recomputation.
5. Any SWU with multiple file ownership or external suite uncertainty must run alone or be manually coordinated.

## Handoff To Execution Pack

- Execution pack: [work-pack/EXECUTION-PACK.md](work-pack/EXECUTION-PACK.md)
- Recommended first execution: `SWU-HARNESS-001`
- Next route: `task-session`

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-05-23 | Initial invoke design and plan work-pack created. | Codex |
| 2026-05-23 | Optimized L0 around the benchmark run kernel; moved Docker/live dataset complexity to L1. | Codex |
| 2026-05-23 | Completed TASK-001 skeleton and schema SWUs with passing `npm test`. | Codex |
| 2026-05-23 | Completed SWU-HARNESS-003 adapter contract and mock adapter with passing `npm test`. | Codex |
