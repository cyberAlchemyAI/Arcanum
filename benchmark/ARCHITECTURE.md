---
template_id: invoke.architecture
template_type: architecture
status: draft
updated_at: 2026-05-25
source_contracts:
  - starting-point.md
---

# Architecture Plan: Agentic Tech Debt & Optimization Harness

## Architecture Intent

Build a deterministic benchmark harness that evaluates autonomous coding agents on technical-debt repair, architectural smell reduction, and performance optimization while preserving enough telemetry to compare both outcome quality and trajectory cost.

## Optimized Concept Boundary

The first implementation concept was the **Benchmark Run Kernel**: one normalized task fixture plus one patch artifact becomes immutable oracle evidence, a score record, and a telemetry event chain.

This kernel is smaller than the full harness but still carries the system's core behavior. Docker, live dataset ingestion, suite-specific adapters, cloud workers, and dashboards compose around it in later layers.

After the official SWE-bench Lite smoke, the next architecture boundary is the **Benchmark Evidence Bridge**: each upstream benchmark integration must first prove its contract, run one real task through the upstream or documented benchmark runner, import raw result files/logs, and emit a local score artifact derived only from those raw results.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | [starting-point.md](starting-point.md) | yes | Foundational project blueprint and phase outline. |
| SC-002 | [SWE-bench Lite official harness](https://www.swebench.com/SWE-bench/guides/evaluation/) | yes | Official Docker harness is the grading authority for SWE-bench evidence; local mirrors are plumbing evidence only. Dataset and Docker requirements are documented in the [dataset guide](https://www.swebench.com/SWE-bench/guides/datasets/) and [Docker setup guide](https://www.swebench.com/SWE-bench/guides/docker_setup/). |
| SC-003 | [SmellBench / static-analysis oracle](https://arxiv.org/abs/2605.07001) | yes | Structural smell-reduction suite; paper identifies PyExamine, repair effectiveness, false-positive identification, and net codebase impact as core evidence dimensions. The release pointer is `https://doi.org/10.5281/zenodo.19247588`; release artifact and runnable scoring surface must be verified before scoring claims. |
| SC-004 | [PerfCodeBench runtime oracle](https://arxiv.org/abs/2605.15222) | yes | Performance optimization suite; paper identifies executable correctness checks, baseline implementation, reference optimized solution, and runtime efficiency as core evidence dimensions. The release pointer is `https://anonymous.4open.science/r/perfcodebench-7CDE`; hardware determinism constraints are part of acceptance. |

## Benchmark Integration Inventory

All benchmark integrations follow the same bridge sequence:

1. Record a `BenchmarkContractProbe` for source, install path, task schema, runner command, raw result files, score semantics, and runtime constraints.
2. Prepare an agent-only task brief and `CandidateManifest`; do not expose gold patches, reference optimized solutions, or benchmark labels that would leak the expected answer.
3. Run the official or documented upstream runner on one pinned smoke task.
4. Import raw result files, logs, reports, and worker profile metadata into immutable artifacts.
5. Emit a local `score-result.json` derived only from imported upstream result files.
6. Normalize the imported score into `OracleEvidence` after the raw evidence exists.

### SWE-bench Lite / SWE-bench

References:

- Evaluation guide: `https://www.swebench.com/SWE-bench/guides/evaluation/`
- Dataset guide: `https://www.swebench.com/SWE-bench/guides/datasets/`
- Docker setup guide: `https://www.swebench.com/SWE-bench/guides/docker_setup/`
- First dataset: `princeton-nlp/SWE-bench_Lite`, `test`
- Official entrypoint: `python -m swebench.harness.run_evaluation`

Implementation steps:

1. Build and version a `swebench-official-runner` container with Python, Docker CLI, `swebench`, and `datasets`.
2. Mount the project and `/var/run/docker.sock` so the official harness can create evaluation containers.
3. Load `princeton-nlp/SWE-bench_Lite` metadata, select a deterministic `instance_id`, and record `repo`, `base_commit`, and `problem_statement`.
4. Generate the agent task brief from non-gold fields only; redact `patch`, `test_patch`, and other answer-bearing fields from the agent path.
5. Require `fixtures/swebench-lite-agent-patches.json` or a materialized equivalent with `instanceId`, `modelNameOrPath`, and either `modelPatch` or `patchArtifactPath`.
6. Convert the candidate manifest into official prediction JSONL fields: `instance_id`, `model_name_or_path`, and `model_patch`.
7. Run the official harness with `--dataset_name princeton-nlp/SWE-bench_Lite`, `--split test`, `--predictions_path`, `--max_workers 1`, and a pinned `--run_id`.
8. Import official result layout as observed, including `results.json`, `instance_results.jsonl`, report files, and per-instance logs.
9. Map status to `pass` only when official SWE-bench marks the instance resolved; map unresolved official results to `fail`; map missing harness output or preflight failure to `infra-fail`.

Current status:

- The official Lite smoke path is implemented and produced a real unresolved score for `astropy__astropy-14365`.
- The failed score is still valid plumbing evidence because it came from official SWE-bench output.
- Full SWE-bench can scale from this bridge after Lite is reproducible and resource cost is accepted.

### SmellBench

References:

- Paper: `https://arxiv.org/abs/2605.07001`
- Release pointer from the paper: `https://doi.org/10.5281/zenodo.19247588`
- PyExamine reference implementation: `https://github.com/KarthikShivasankar/python_smells_detector`

Implementation steps:

1. Run `SWU-HARNESS-007A` as a contract probe before building an adapter.
2. Verify whether the release contains runnable benchmark data, orchestration code, scoring scripts, task metadata, expected output schemas, and license/access terms.
3. Record the exact task shape: smell ID, smell type, target project/version, file or module scope, PyExamine evidence, expert validation label if present, and available repair/false-positive scoring criteria.
4. Verify the documented runner command. If SmellBench only exposes PyExamine plus data files, record the documented derivation instead of inventing a hidden official score.
5. Select one pinned smell task and create an agent brief without exposing expert judgment, expected repair, or aggregate score labels.
6. Require an agent-produced source-change artifact aligned to the selected smell task.
7. Run the verified upstream or documented SmellBench scoring path and import raw outputs/logs into `artifacts/smellbench-official-smoke/official-or-upstream-results/`.
8. Emit `score-result.json` with separate fields for repair effectiveness, false-positive identification, net codebase impact, and semantic correctness when available.
9. Map aggregate status only from documented SmellBench semantics. If those semantics are absent or incomplete, block with a probe record rather than promoting a local substitute.

Block conditions:

- The release pointer is unavailable, non-runnable, or lacks task/output schema.
- PyExamine can run but no SmellBench scoring semantics can be recovered.
- The selected smoke task has no honest agent-produced candidate artifact.
- Current `OracleEvidence` cannot represent false-positive or net-impact outcomes without a schema decision.

### PerfCodeBench

References:

- Paper: `https://arxiv.org/abs/2605.15222`
- Release pointer from the paper: `https://anonymous.4open.science/r/perfcodebench-7CDE`

Implementation steps:

1. Run `SWU-HARNESS-008A` as a contract probe before building an adapter.
2. Verify release access, task metadata, correctness runner, runtime runner, baseline implementation fields, reference optimized solution fields, expected raw outputs, and license/access terms.
3. Define a deterministic worker profile before any score claim: CPU/GPU availability, memory, compiler/runtime versions, isolation, repetitions, warmups, timeout, and noise threshold.
4. Select one pinned task with executable correctness checks and baseline/runtime metadata.
5. Create the agent task brief without exposing the reference optimized solution or reference timing.
6. Require an agent-produced candidate source artifact aligned to the selected task.
7. Run correctness first. A correctness failure produces `fail` without promoting any speedup claim.
8. Run the documented performance measurement path with recorded repetitions and worker metadata.
9. Import raw timing series, correctness output, runner logs, and worker profile into `artifacts/perfcodebench-official-smoke/official-or-upstream-results/`.
10. Emit `score-result.json` with correctness, runtime delta, speedup, threshold, repetitions, noise status, and worker profile.
11. Normalize only after the raw correctness and timing files exist; do not treat a shared laptop run as official evidence unless the contract probe accepts that profile.

Block conditions:

- The release pointer is inaccessible or does not expose runnable evaluation infrastructure.
- The worker profile cannot satisfy the benchmark's determinism needs.
- Correctness and runtime outputs cannot be tied to the same candidate artifact.
- The current schema cannot preserve runtime series, threshold, and noise metadata without losing auditability.

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
- Benchmark Evidence Bridge: verifies an upstream benchmark contract, prepares candidate manifests, invokes the upstream runner, imports raw results, and maps documented outcomes into local score artifacts without regrading.
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
- `CandidateManifest`: per-benchmark manifest that binds one upstream task ID to one agent-produced patch/source-change artifact and model label; gold/reference outputs are forbidden as candidate artifacts.
- `BenchmarkContractProbe`: artifact that records upstream source, install path, task schema, runner command, raw output files, score semantics, and access/runtime constraints before adapter work begins.
- `RunState`: state machine for queued, preparing, invoking, applying-patch, evaluating, scoring, completed, failed, and quarantined.
- `EvaluatorProfile`: local fixture, Docker, or pinned performance worker profile with CPU, memory, filesystem, network, and timeout limits.
- `UpstreamResultImport`: immutable copy of official or documented benchmark outputs, logs, and reports.
- `OracleResult`: normalized output for semantic correctness, smell repair effectiveness, false-positive identification, net smell impact, performance correctness, runtime delta, reproducibility metadata, and raw logs.
- `TelemetryEvent`: append-only event shape for agent actions, tool calls, command spans, patches, retries, and score calculations.

Local collaboration rules:

- Dataset-specific ingestion may produce enriched metadata, but scoring must consume only normalized task and oracle contracts.
- Upstream benchmark runners or documented result files are the grading authority when available; local scoring may only map their documented outcomes into the shared score shape.
- Sandboxes return evidence, never untraceable final scores; local score artifacts must link to immutable raw result imports.
- Dashboard reads from the telemetry and result store; it must not recompute oracle outcomes.

## View 4: Workflow Process View

Primary flow:

1. Probe the benchmark contract: source artifact, install path, task fields, runner command, raw result files, scoring semantics, and runtime constraints.
2. Load or ingest benchmark cases and normalize them into `TaskDefinition` records only after the contract probe is recorded.
3. Select a pinned smoke task, agent adapter, run profile, and resource budget.
4. Prepare an honest `CandidateManifest` from an agent-produced patch or source-change artifact.
5. Prepare the evaluator substrate: fixture-local for the kernel proof, official SWE-bench Docker harness for SWE-bench, benchmark-specific runner for SmellBench/PerfCodeBench, and pinned workers for performance runs.
6. Invoke the upstream or documented benchmark runner.
7. Import raw benchmark result files, logs, reports, and worker profile metadata.
8. Map documented upstream outcomes into `OracleEvidence` and `ScoreResult` without substituting local inferred grading.
9. Persist telemetry, artifacts, logs, and final run status.
10. Render aggregate and run-level dashboard views.

Failure and compensation paths:

- Dataset ingestion mismatch: quarantine task and record schema gap.
- Upstream runner unavailable or release artifact incomplete: block the benchmark smoke with a precise upstream availability record.
- Candidate artifact missing, empty, or not aligned to the selected task: block before evaluation.
- Sandbox provisioning failure: retry within infrastructure budget, then mark infra-failed.
- Agent timeout or invalid patch: mark agent-failed with full trajectory evidence.
- Oracle flake: rerun only if profile allows deterministic retry; otherwise quarantine.
- Perf noise threshold breach: reject the measurement and rerun on a clean worker profile.

## View 5: Decision Flow View

Key decisions:

- Dataset classification: choose oracle integration from normalized task source and labels.
- Agent contract shape: accept patch output for L0; defer structural diff support until patch flow is stable.
- Evaluator profile: use fixture-local evaluation for the first kernel proof, Docker for repeatable repository tasks, and pinned-resource workers for performance tasks.
- Score authority: prefer official upstream harness/result files; when no official score file exists, derive only from documented upstream output fields and label the derivation.
- Score status: pass only when required semantic/correctness oracle passes and target-specific improvement thresholds are met.
- Telemetry cost model: record raw token/tool/runtime costs first; derive aggregate cost metrics separately.

Selected outcomes:

- Start with one patch-based agent interface.
- Build the benchmark run kernel as the L0 proof before live dataset ingestion.
- Promote Docker-backed SWE-bench tech-debt ingestion to L1 once the kernel evidence model is stable.
- Add structural and performance suites through contract probes and real smoke score artifacts before broad adapters.
- Treat deterministic execution evidence as more important than dashboard breadth in early layers.

## View 6: Dependency Interface View

Internal interfaces:

- `TaskProvider.load(): TaskDefinition[]`
- `AgentAdapter.run(task, repoContext, budget): AgentResult`
- `ContractProbe.probe(source): BenchmarkContractProbe`
- `BenchmarkRunner.run(task, candidateManifest, profile): UpstreamResultImport`
- `Evaluator.evaluate(task, patch, profile): OracleEvidence`
- `OracleScorer.score(task, evidence): ScoreResult`
- `TelemetrySink.append(event): void`

External dependencies:

- Hugging Face or local dataset mirror for local SWE-bench plumbing evidence.
- Official SWE-bench harness for upstream SWE-bench score evidence.
- SmellBench release artifact and PyExamine/static-analysis runtime.
- PerfCodeBench release artifact and executable correctness/runtime evaluation infrastructure.
- Docker daemon or cloud container workers.
- Benchmark-specific setup scripts and oracle commands.
- Static-analysis tooling for smell reduction checks.
- Dashboard runtime and datastore.

Boundary rules:

- Agent adapters cannot access host credentials except through explicit sandbox-mounted secrets.
- Oracle integrations cannot mutate benchmark source definitions.
- Oracle integrations cannot expose gold/reference solutions to the candidate-producing agent path.
- Local mirrors and fixture runs cannot be promoted as upstream benchmark evidence.
- PerfCodeBench runs cannot share CPU-intensive hosts with model inference or unrelated workloads.
- Raw logs remain linked to score components for auditability.

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| Deterministic execution | starting-point.md | Requires pinned environment profiles, repeatable setup, and evidence capture. |
| Multi-oracle support | starting-point.md | Requires normalized task and oracle result contracts. |
| Performance noise sensitivity | starting-point.md | Requires isolated workers and retry/quarantine policy. |
| Upstream benchmark uncertainty | source contracts | Requires integration probes before full ingestion assumptions are promoted. |
| Official evidence authority | SWE-bench implementation evidence | Requires raw upstream result import before score mapping; local mirrors remain plumbing evidence. |
| Gold/reference leakage risk | benchmark ethics | Requires candidate manifests that exclude benchmark gold patches and reference optimized solutions. |
| No execution during invoke plan | invoke contract | This design only prepares implementation handoff. |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | All benchmark inputs are normalized before agent invocation. | Task Registry | Schema validation in ingestion tests. |
| R-002 | Agent output is persisted before patch application. | Agent Adapter Layer | Telemetry event and artifact check. |
| R-003 | Evaluator evidence is immutable after scoring. | Evaluator Substrate, Telemetry Store | Append-only evidence records. |
| R-004 | Perf runs use pinned-resource profiles. | PerfCodeBench oracle | Profile validation before execution. |
| R-005 | Score calculation is centralized. | Oracle Integrations | Scorers consume normalized evidence only. |
| R-006 | Upstream benchmark evidence must come from official or documented raw outputs. | Benchmark Evidence Bridge | Score artifact links to imported result files/logs. |
| R-007 | Candidate artifacts must be agent-produced and instance-aligned. | Agent Adapter Layer, Benchmark Evidence Bridge | Manifest validation blocks empty, missing, gold, or reference artifacts. |

## Decision Log

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-001 | Use Node.js/TypeScript for orchestration. | Node.js, Python, mixed control plane | Matches starting blueprint and keeps agent/dash contracts typeable. |
| D-002 | Use Python/Docker for sandboxes and benchmark scripts. | In-process execution, Docker, VM-only | Docker isolates target repos while preserving common benchmark tooling. |
| D-003 | Normalize all suites through `TaskDefinition`. | Per-suite bespoke runners, shared schema | Enables comparable telemetry and scoring. |
| D-004 | Start with a fixture-local benchmark run kernel. | Docker first, SWE-bench first, all suites at once | Proves the core run model before infrastructure and external dataset risk. |
| D-005 | Treat SmellBench and PerfCodeBench contracts as verification-gated. | Assume direct integration, defer entirely | Avoids baking unverified external APIs into the core architecture. |
| D-006 | Promote Docker-backed evaluation to L1. | L0 Docker requirement, fixture-only forever | Keeps L0 small while preserving the production substrate path. |
| D-007 | Treat upstream benchmark runners/results as grading authority. | Local regrading, official/raw result import | SWE-bench proved that runner output shape can differ from docs; evidence import must adapt to the actual upstream result files without changing grading semantics. |
| D-008 | Split remaining benchmark work into contract probes and real smoke score artifacts. | One generic adapter task, immediate full integration | Prevents SmellBench/PerfCodeBench assumptions from hardening before artifact availability, runner commands, and score semantics are verified. |

## Risks

| Risk ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | Upstream benchmark schemas differ from the blueprint assumptions. | Add integration probes before full adapters. | Harness maintainer |
| RK-002 | Performance metrics are noisy on shared hardware. | Isolate PerfCodeBench workers and enforce retry/quarantine thresholds. | Infrastructure owner |
| RK-003 | Agent trajectory telemetry is inconsistent across adapters. | Define a minimum event envelope and adapter compliance tests. | Orchestrator owner |
| RK-004 | Dashboard work races ahead of reliable scoring. | Gate dashboard slices behind persisted scoring evidence. | Product/UX owner |
| RK-005 | Upstream release artifacts are incomplete, unavailable, or not executable. | Contract probes may complete as precise block records; do not synthesize local substitutes as benchmark evidence. | Harness maintainer |
| RK-006 | Candidate generation accidentally sees gold/reference solutions. | Redact gold fields from agent task briefs and validate candidate manifests before evaluation. | Harness maintainer |
| RK-007 | Upstream result layout drifts from papers or docs. | Import result files by observed output plus documented semantics; tests cover report mapping separately from runner execution. | Harness maintainer |

## Downstream Planning Notes

- Implementation-plan inputs: this architecture, `starting-point.md`, official SWE-bench smoke evidence, and verified benchmark contract probes.
- Work-pack implications: medium complexity, split work-pack, SWU-level tasks.
- Validation implications: schema tests, fixture-local kernel smoke tests, Docker repeatability tests, official/upstream smoke score artifacts, raw result import tests, and deterministic perf-profile checks.

## Design Transport Notes

Carry this design into plan mode as the source design reference. Do not promote unverified SmellBench or PerfCodeBench integration details beyond contract probes until their artifact sources, task schemas, runner commands, raw outputs, score semantics, and runtime constraints are confirmed.

## Gate Result

- Status: flag
- Reason: six design views are covered and planning can proceed, but external benchmark availability and exact suite contracts remain verification-gated target-artifact gaps.
