# EXECUTION-PACK: Agentic Tech Debt & Optimization Harness

## Purpose

Coordinate the medium-complexity work-pack by waves while preserving SWU-level execution boundaries.

## Source Links

- Work-pack: [../WORK-PACK.md](../WORK-PACK.md)
- Layering: [../IMPLEMENTATION-LAYERING.md](../IMPLEMENTATION-LAYERING.md)
- Architecture: [../ARCHITECTURE.md](../ARCHITECTURE.md)

## Wave Schedule

| Wave | Layer | Question Answered | Tasks | SWUs | Gate |
| --- | --- | --- | --- | --- | --- |
| [W0](waves/W0.md) | L0 | Can the fixture-local benchmark run kernel work end to end? | TASK-001, TASK-002 | SWU-HARNESS-001..004 | Two clean kernel smoke runs match. |
| [W1](waves/W1.md) | L1 | Can Docker-backed SWE-bench tech-debt ingestion and batch evaluation repeat? | TASK-003 | SWU-HARNESS-005..006 | Docker smoke plus batch report separates agent, oracle, and infra outcomes. |
| [W2](waves/W2.md) | L2 | Can structural and performance probes fit the shared evidence model? | TASK-004 | SWU-HARNESS-007..008 | Probe reports prove normalized evidence. |
| [W3](waves/W3.md) | L3 | Can operators replay and inspect benchmark campaigns? | TASK-005, TASK-VERIFY | SWU-HARNESS-009..010 plus verification exemption | Campaign report and dashboard-ready views. |

## Parallelization Boundary

- W0 is mostly serial because schemas precede adapters and fixture-local kernel execution.
- W1 can split Docker evaluation, ingestion, and reporting only after the kernel evidence shape is stable.
- W2 probes can run in parallel after L1, because structural and performance adapters have disjoint write scopes.
- W3 reporting and UI/API work can run after telemetry records stabilize.

## Execution Rule

Mutation-capable execution should select exactly one SWU unless the coordinator confirms disjoint write scopes and merge order.
