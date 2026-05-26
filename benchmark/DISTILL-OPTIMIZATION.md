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

---

# Distill Result: Benchmark Evidence Bridge Refinement

## Target Context

Refine the benchmark architecture after one real official benchmark path, SWE-bench Lite, was implemented and scored. The remaining SmellBench and PerfCodeBench work must avoid local-mirror evidence claims and must not hardcode unverified upstream assumptions.

## Objective And Output Artifact

- Objective: reduce the remaining benchmark integration design to the smallest coherent unit that can safely generalize from SWE-bench to SmellBench and PerfCodeBench.
- Output artifact: design refinement plus work-pack/task refinement for L2 benchmark implementations.
- Mode and budget: Standard; one proposal track, Proposer/Balancer role simulation, two recursive rounds.

## Discovery Baseline

SWE-bench proved the harness can run a real upstream benchmark and emit a local score artifact. It also exposed three design lessons:

1. Documentation and actual result layout can diverge; the importer must adapt to observed official output while preserving upstream grading authority.
2. A real score artifact needs an instance-aligned agent candidate, not a gold/reference patch or local fixture substitute.
3. `fail` is a valid benchmark result when the upstream harness completed; `infra-fail` means the benchmark plumbing did not prove itself.

SmellBench and PerfCodeBench are less operationally verified in this repo than SWE-bench. Their first implementation unit must therefore discover and record upstream contracts before any adapter claims readiness.

## Role Conversation Trace

| Round | Proposer Claim | Evidence Or Assumption | Balancer Objection | Reconciliation |
| --- | --- | --- | --- | --- |
| 1 | The next coherent unit is one shared benchmark adapter interface for SmellBench and PerfCodeBench. | Both need task ingestion, candidate artifacts, raw outputs, and score mapping. | Too abstract: SmellBench and PerfCodeBench have different authority surfaces and runtime risks. | Revise to a shared evidence bridge pattern with benchmark-specific contract probes. |
| 2 | The smallest coherent unit is a Benchmark Evidence Bridge: contract probe, candidate manifest, upstream runner/import, and score mapper. | SWE-bench implementation used exactly these parts once the missing patch blocker was resolved. | Still too much if the upstream artifact is unavailable. | Split execution into contract probe first, real smoke second; block precisely when the runner or artifact is unavailable. |

## Current Smallest Coherent Unit

**Benchmark Evidence Bridge**

Responsibility: turn one verified upstream benchmark task and one agent-produced candidate artifact into imported raw benchmark results, a local upstream-derived score artifact, and normalized oracle evidence.

Inputs:

- benchmark contract probe report,
- selected upstream task ID,
- agent-produced candidate artifact,
- evaluator/worker profile,
- documented score semantics.

Outputs:

- candidate manifest,
- raw upstream result/log import,
- `score-result.json`,
- normalized `OracleEvidence` sample,
- block record when the upstream runner or deterministic worker is unavailable.

## Optimization Point

The evidence bridge is the best size because it is larger than a generic schema mapper but smaller than a full benchmark adapter. It preserves the evidence authority lesson from SWE-bench while allowing SmellBench and PerfCodeBench to differ in runner setup, result shape, and score dimensions.

## Distill Layer Map

| Layer | Concept | Status |
| --- | --- | --- |
| Broad system | Multi-suite agent benchmark harness | Target product. |
| Architecture unit | Benchmark Evidence Bridge | Current L2 optimization point. |
| Benchmark-specific units | SmellBench contract/smoke; PerfCodeBench contract/smoke | Planned in TASK-004. |
| Smaller fragments | schema-only result mapper, static-analysis-only probe, runtime-only benchmark script | Too small; cannot prove benchmark evidence authority alone. |

## Technique Pack Trace

| Technique | Activation Reason | Output | Decision |
| --- | --- | --- | --- |
| Abstraction-level guard | TASK-004 risked becoming two broad adapter builds. | Separate contract probes from scoring smokes. | accepted |
| Recomposition proof | Need to show this unit scales back to all benchmarks. | Evidence bridge pattern composes into SWE-bench, SmellBench, and PerfCodeBench with suite-specific runners. | accepted |
| Evolution profile | New benchmarks or result layouts are likely. | Preserve candidate manifest, raw import, score mapper, and normalized evidence as separate responsibilities. | accepted |
| Boundary-object check | Raw upstream result files must be auditable by humans and code. | `official-or-upstream-results/` import becomes the shared boundary object. | accepted |
| Premortem | Likely failure is claiming benchmark support from a local substitute or incomplete release artifact. | Require contract probe and precise block records before scoring smoke. | accepted |

## Closure And Recomposition Proof

The Benchmark Evidence Bridge closes because it has a clear input/output contract and a precise authority boundary: local code may prepare candidates, invoke runners, import artifacts, and map documented outcomes, but it does not replace benchmark grading.

It recomposes upward by becoming the shared pattern for:

- SWE-bench official harness results,
- SmellBench structural repair outcomes,
- PerfCodeBench correctness and runtime outcomes,
- later dashboard score presentation.

## Evolution Profile

Expected evolution:

- upstream result layouts change,
- benchmark release artifacts move from anonymous/preprint locations to stable repositories,
- worker profiles become more precise,
- more benchmark suites are added.

Smallest extension boundary:

- add benchmark-specific contract probes and import mappers,
- keep the candidate manifest and score artifact shape stable,
- promote schema extensions only when raw evidence cannot be represented honestly.

## Deferred Complexity

- Full SmellBench adapter: deferred until release artifact, runner, and scoring semantics are verified.
- Full PerfCodeBench adapter: deferred until executable runner and deterministic worker/profile constraints are verified.
- Cross-suite aggregate scoring: deferred until each suite has one real upstream-derived smoke score.
- Dashboard UX: deferred until score artifacts have stable links to raw imported evidence.

## Tension Ledger

| Tension | Resolution |
| --- | --- |
| Need one shared model, but benchmarks have different result semantics. | Share evidence bridge responsibilities, not one universal runner. |
| Need real benchmark proof, but upstream artifacts may be incomplete. | Contract probes may complete as precise block records; no local substitute promotion. |
| Need performance scores, but hardware noise can dominate. | PerfCodeBench smoke requires worker profile and noise metadata before pass/fail scoring. |
| Need structural smell scores, but smell detections can be false positives. | SmellBench evidence preserves repair effectiveness, false-positive identification, and net impact separately. |

## Frame-Expiry Note

This optimization point expires if SmellBench or PerfCodeBench publish a stable official harness with a canonical prediction/results interface equivalent to SWE-bench. In that case, the bridge should shrink to an official-runner adapter for that benchmark rather than a contract-probe-first path.

## Navigation Guide

Start with `SWU-HARNESS-007A` or `SWU-HARNESS-008A`. Do not start scoring smokes until the matching contract probe records the upstream artifact, runner, result files, and score semantics. Treat any unavailable artifact or non-deterministic worker as a block/infra outcome, not as permission to invent a local benchmark.

## Next Route

interrogation, then task-session on `SWU-HARNESS-007A` or `SWU-HARNESS-008A`.

---

# Distill Result: Post-Interrogation Readiness

## Target Context

The benchmark work-pack after adding reference-backed integration inventories for SWE-bench, SmellBench, and PerfCodeBench.

## Objective And Output Artifact

- Objective: answer whether everything is ready and reduce the next action to the smallest coherent execution unit.
- Output artifact: readiness distillation plus next-route guidance.
- Mode and budget: Validate; one Balancer-led critique with Proposer repair not needed.

## Discovery Baseline

The interrogation found that the pack is ready for contract probes but not ready for benchmark scoring smokes. This is the intended state after the SWE-bench lesson: real benchmark evidence must come from upstream/documented runners and raw result imports, not local substitutes.

Evidence:

- `WORK-PACK.md` marks `TASK-004` as `ready-contract-probes`.
- `SWU-HARNESS-007A` and `SWU-HARNESS-008A` are ready.
- `SWU-HARNESS-007B` and `SWU-HARNESS-008B` remain blocked until the corresponding contract probes resolve benchmark-specific blockers.
- `TASK-004.md` now names references, implementation steps, block conditions, and score artifact requirements per benchmark.

## Role Conversation Trace

| Round | Proposer Claim | Evidence Or Assumption | Balancer Objection | Reconciliation |
| --- | --- | --- | --- | --- |
| 1 | Everything is ready. | Design, work-pack, and TASK-004 now contain references and per-benchmark inventory. | Too broad: scoring smokes are not ready because upstream contracts are unverified. | Narrow readiness to contract-probe execution only. |
| 2 | Start either SmellBench or PerfCodeBench probe. | Both `007A` and `008A` are read/probe-oriented and disjoint. | PerfCodeBench may require worker decisions sooner; SmellBench may be simpler to probe first. | Default next unit is `SWU-HARNESS-007A`; run `008A` in parallel or next if capacity allows. |

## Current Smallest Coherent Unit

**Benchmark Contract Probe**

Responsibility: verify one benchmark's upstream artifact, install path, task schema, runner/scoring command, raw outputs, score semantics, and constraints before any adapter or smoke score is built.

Inputs:

- benchmark reference links,
- current `TASK-004` implementation inventory,
- network/release access when executing the probe,
- existing `TaskDefinition` and `OracleEvidence` expectations.

Outputs:

- `artifacts/smellbench-contract-probe/report.json` or `artifacts/perfcodebench-contract-probe/report.json`,
- precise block record if artifact or scoring surface is unavailable,
- recommendation for whether the matching score smoke may start.

## Optimization Point

The best next unit is not another architecture pass and not a score smoke. It is one contract probe, because that is the smallest action that can convert the remaining uncertainty into executable knowledge or a precise block.

## Concept Layer Map

| Layer | Concept | Readiness |
| --- | --- | --- |
| Full benchmark harness | Multi-suite official/upstream benchmark evidence | Not complete. |
| L2 benchmark bridge | Contract probe -> candidate manifest -> upstream runner -> raw import -> score artifact | Designed. |
| Next executable unit | One benchmark contract probe | Ready. |
| Score smoke | One upstream-derived score artifact | Blocked until probe resolves. |

## Technique Pack Trace

| Technique | Activation Reason | Output | Decision |
| --- | --- | --- | --- |
| Navigable result check | User asked "everything is ready?" | Ready only for `007A`/`008A`; not ready for `007B`/`008B`. | accepted |
| Abstraction-level guard | Avoid turning readiness into a vague yes/no. | Split readiness by contract probe vs score smoke. | accepted |
| Premortem | Likely failure is running a smoke against an unverified benchmark surface. | Keep score smokes blocked until raw outputs and semantics are proven. | accepted |
| Recomposition proof | Need the probe to feed later smoke work. | Probe outputs become inputs to candidate manifest, runner, importer, and score mapper. | accepted |

## Closure And Recomposition Proof

The contract probe closes because it has a concrete source, command/output discovery target, and binary outcome: runnable score path or precise block. It recomposes upward by unlocking or blocking the matching benchmark smoke without changing the architecture.

## Evolution Profile

The probe report may later evolve into benchmark-specific adapters, but only after it records real artifact paths, runner commands, result files, and scoring semantics. If SmellBench or PerfCodeBench publish a stable official harness, future probes should shrink to official-runner verification.

## Deferred Complexity

- SmellBench score smoke deferred until `SWU-HARNESS-007A` resolves B-002.
- PerfCodeBench score smoke deferred until `SWU-HARNESS-008A` resolves B-003 and worker/profile constraints.
- Dashboard/reporting remains deferred until L2 evidence is stable enough to display.

## Tension Ledger

| Tension | Resolution |
| --- | --- |
| User wants benchmark implementation to move forward, but upstream surfaces are unverified. | Move forward through contract probes, not smoke claims. |
| Both probes are ready, but one first task is needed for focus. | Default to SmellBench `007A`; PerfCodeBench `008A` may run next or in parallel. |
| A block record feels less satisfying than a score. | A precise block is valid L2 evidence when upstream artifacts are incomplete or unavailable. |

## Premortem

Likely failure: a future run treats PyExamine output or local timing as benchmark evidence without proving the benchmark's documented scoring surface.

Guardrail: completion of `007A` or `008A` requires exact artifact source, runner command, raw output files, score semantics, and access/runtime constraints, or an explicit block record.

## Frame-Expiry Note

This readiness distillation expires when either contract probe completes. At that point the next smallest coherent unit becomes the matching real smoke or a blocker-resolution task.

## Navigation Guide

Start with `SWU-HARNESS-007A` unless performance infrastructure is the priority. Do not start `SWU-HARNESS-007B` or `SWU-HARNESS-008B` until their matching probe says the runner, output shape, and score semantics are known.

## Next Route

`task-session` on `SWU-HARNESS-007A`, with `SWU-HARNESS-008A` as the parallel-safe sibling.
