# Plan Transport Report: Agentic Tech Debt & Optimization Harness

## Invocation Summary

- Spell: invoke
- Modes: design and plan
- Source artifact: [starting-point.md](starting-point.md)
- Design artifact: [ARCHITECTURE.md](ARCHITECTURE.md)
- Plan artifacts: [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md), [WORK-PACK.md](WORK-PACK.md), [work-pack/EXECUTION-PACK.md](work-pack/EXECUTION-PACK.md)
- Optimization artifact: [DISTILL-OPTIMIZATION.md](DISTILL-OPTIMIZATION.md)

## Transport Decisions

| Decision | Result | Reason |
| --- | --- | --- |
| Treat starting point as approved source contract | accepted | User explicitly requested invoke design and plan with the file open as context. |
| Use discovery-to-plan synthesis instead of blocking for missing define artifacts | flag | The blueprint is sufficiently concrete for architecture and L0 planning, but not a full governed define bundle. |
| Use medium complexity split work-pack | accepted | The system spans schemas, agents, sandboxes, multiple benchmark oracles, and telemetry. |
| Start execution at L0 | accepted | Multi-suite scope depends on first proving one deterministic path. |
| Optimize L0 around the benchmark run kernel | accepted | Fixture-local evaluation proves the core concept before Docker and live dataset risk. |

## Gap Ledger

| Gap ID | Owner | Gap | Impact | Follow-Up |
| --- | --- | --- | --- | --- |
| G-001 | target artifact | Approved define spec and glossary were not provided. | Design/plan are usable but flagged. | Optionally run `invoke define` before implementation hardening. |
| G-002 | target artifact | External benchmark contracts are unverified. | L1/L2 tasks need probes before broad implementation. | Run dataset and oracle probe SWUs. |
| G-003 | invoke telemetry | Benchmark folder has no local `.arcanum/observability`; parent observability was not mutated. | Closeout is report-only. | Run from repository root with hook telemetry if durable observation is required. |

## Handoff Recommendation

Begin with `task-session` for [SWU-HARNESS-001](WORK-PACK.md), then proceed through W0 only. Do not start Docker-backed SWE-bench work until the fixture-local run kernel passes twice, and do not start SmellBench or PerfCodeBench adapter implementation until their probe blockers are resolved.
