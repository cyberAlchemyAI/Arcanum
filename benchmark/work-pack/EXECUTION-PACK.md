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
| [W1](waves/W1.md) | L1/L1.5 | Can Docker-backed SWE-bench plumbing and official SWE-bench Lite evaluation repeat? | TASK-003, TASK-003.5 | SWU-HARNESS-005..006B | Local mirror smoke/batch plus official SWE-bench Lite score artifact separate benchmark fail from infra fail. |
| [W2](waves/W2.md) | L2 | Can structural and performance benchmarks expose upstream-derived evidence paths? | TASK-004 | SWU-HARNESS-007A..008B | Contract probes first; score smokes only after upstream runner/result semantics and runtime constraints are proven. |
| [W3](waves/W3.md) | L3 | Can operators replay and inspect benchmark campaigns? | TASK-005, TASK-VERIFY | SWU-HARNESS-009..010 plus verification exemption | Campaign report, dashboard-ready views, and closure audit passed. |

## Parallelization Boundary

- W0 is mostly serial because schemas precede adapters and fixture-local kernel execution.
- W1 can split Docker evaluation, ingestion, and reporting only after the kernel evidence shape is stable.
- W2 contract probes `SWU-HARNESS-007A` and `SWU-HARNESS-008A` can run in parallel after L1.5 because they are read/probe-oriented and have disjoint artifact paths.
- W2 score smokes `SWU-HARNESS-007B` and `SWU-HARNESS-008B` must not start until the matching contract/materialization probe resolves the benchmark-specific blocker. `SWU-HARNESS-008B` additionally requires `SWU-HARNESS-008B.1` to produce a real PerfCodeBench agent candidate and deterministic worker/noise profile; the `SWU-HARNESS-008A.1` dry-run output is setup proof only.
- W3 reporting and UI/API work can run after telemetry records stabilize.

## Execution Rule

Mutation-capable execution should select exactly one SWU unless the coordinator confirms disjoint write scopes and merge order.
