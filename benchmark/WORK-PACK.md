---
module: agentic-tech-debt-optimization-harness
version: current
status: draft
updatedAt: 2026-05-26
docType: work-pack
---

# WORK-PACK: Agentic Tech Debt & Optimization Harness

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | complete | Reproducibility and traceability audit passed; work-pack is ready for closeout or scale-up planning. |
| complexity | medium | Multiple subsystems, external suite adapters, Docker execution, and telemetry. |
| outputMode | split | Required for medium complexity. |
| executionPackRef | [work-pack/EXECUTION-PACK.md](work-pack/EXECUTION-PACK.md) | Wave choreography and parallelization boundaries. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decision boundaries. |
| activeLayerWindow | closed | `TASK-VERIFY` completed the W0-W3 reproducibility and traceability audit. |
| lastUpdatedAt | 2026-05-26 | Completed `TASK-VERIFY` closure audit with tests, report/dashboard regeneration, JSON validation, and zero evidence gaps. |
| readinessProfile | pilot | Target is a reproducible internal benchmark harness. |

## Objective Summary

- Objective: implement a deterministic benchmark harness that can normalize agentic tech-debt tasks, invoke patch-producing agents, evaluate patches through a stable evaluator contract, score oracle evidence, and expose telemetry for later dashboarding.
- Primary inputs: [starting-point.md](starting-point.md), [ARCHITECTURE.md](ARCHITECTURE.md), [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md), [DISTILL-OPTIMIZATION.md](DISTILL-OPTIMIZATION.md).
- Current success condition: TASK-VERIFY is complete when tests, report/dashboard regeneration, JSON validation, and traceability assertions pass with zero evidence gaps.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Architecture views | Task contracts | Each major subsystem becomes a task with SWUs. |
| Layer decisions | Waves | Waves W0-W3 map to L0-L3 promotion questions. |
| External benchmark gaps | Blockers and probe tasks | SmellBench and PerfCodeBench stay probe-gated until verified. |
| Validation strategy | Gate checks | Every slice has command or reviewable evidence. |
| Agent interface decision | TASK-002 | Patch-based adapter is the L0 execution contract. |
| Concept optimization | Benchmark Evidence Bridge | Contract probes convert upstream uncertainty into executable knowledge or precise blocks before any score smoke claims benchmark support. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Canonical run-kernel schemas exist with tests. | L0 | [W0](work-pack/waves/W0.md) | none | Schema/unit tests pass. |
| S-002 | One patch-based agent invocation can be evaluated by the fixture-local run kernel. | L0 | [W0](work-pack/waves/W0.md) | S-001 | `npm run smoke:kernel` passed twice from clean state. |
| S-003 | Docker-backed SWE-bench tech-debt ingestion and batch evaluation work for a small sample. | L1 | [W1](work-pack/waves/W1.md) | S-001, S-002 | `npm run smoke:docker`; `npm run smoke:batch` passed against local fixture mirror. |
| S-003.5 | Official SWE-bench Lite evaluation path can hand predictions to the upstream harness. | L1.5 | [W1](work-pack/waves/W1.md) | S-003 | Official prediction JSONL, official report/logs, and `score-result.json` captured. |
| S-004 | Structural and performance benchmarks produce upstream-derived evidence or precise block records. | L2 | [W2](work-pack/waves/W2.md) | S-003.5 | Contract probe reports plus real smoke score artifacts or precise upstream/runtime blocks. |
| S-005 | Operator campaign reporting and dashboard-ready API are available. | L3 | [W3](work-pack/waves/W3.md) | S-004 | Replayable campaign report and dashboard audit trail. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-001](work-pack/tasks/TASK-001.md) | Define canonical schemas and repository skeleton. | L0 | medium | [W0](work-pack/waves/W0.md) | Architecture views 2, 3, 6 | pass | completed |
| [TASK-002](work-pack/tasks/TASK-002.md) | Implement patch-based agent invocation and fixture-local run kernel. | L0 | medium | [W0](work-pack/waves/W0.md) | Architecture views 3, 4 | pass | completed |
| [TASK-003](work-pack/tasks/TASK-003.md) | Add Docker-backed SWE-bench tech-debt ingestion and batch runner. | L1 | medium | [W1](work-pack/waves/W1.md) | starting-point.md phase 2 | pass-local-mirror | completed |
| [TASK-003.5](work-pack/tasks/TASK-003.5.md) | Add official SWE-bench Lite evaluation path. | L1.5 | medium | [W1](work-pack/waves/W1.md) | SWE-bench docs | pass-official-smoke | completed |
| [TASK-004](work-pack/tasks/TASK-004.md) | Probe SmellBench and PerfCodeBench official paths. | L2 | medium | [W2](work-pack/waves/W2.md) | starting-point.md phase 3, SmellBench/PerfCodeBench papers | pass-real-smokes | completed |
| [TASK-005](work-pack/tasks/TASK-005.md) | Build telemetry reporting and dashboard-ready API. | L3 | medium | [W3](work-pack/waves/W3.md) | starting-point.md phase 4 | pass-dashboard-ready | completed |
| [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Verify reproducibility, traceability, and plan closure. | L0-L3 | medium | W0-W3 | all artifacts | pass-closure-audit | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source | Dependencies | Write Scope | Done Criteria | Validation | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-HARNESS-001 | [TASK-001](work-pack/tasks/TASK-001.md) | ARCHITECTURE.md | none | package config, source skeleton | Project builds with empty modules. | `npm test` passed | local-fallback | completed |
| SWU-HARNESS-002 | [TASK-001](work-pack/tasks/TASK-001.md) | ARCHITECTURE.md | SWU-HARNESS-001 | schema modules | Schemas validate representative fixtures. | `npm test` passed | subagent | completed |
| SWU-HARNESS-003 | [TASK-002](work-pack/tasks/TASK-002.md) | ARCHITECTURE.md | SWU-HARNESS-002 | agent adapter modules | Patch-based adapter returns typed result. | `npm test` passed | subagent | completed |
| SWU-HARNESS-004 | [TASK-002](work-pack/tasks/TASK-002.md) | ARCHITECTURE.md | SWU-HARNESS-003 | run kernel, fixture evaluator, oracle runner, telemetry sink | Clean fixture patch is applied and scored twice. | `npm test`; `npm run smoke:kernel` passed with `kernel-smoke-001` and `kernel-smoke-002` | local-fallback | completed |
| SWU-HARNESS-005 | [TASK-003](work-pack/tasks/TASK-003.md) | starting-point.md | SWU-HARNESS-004 | Docker evaluator and SWE-bench provider | Small sample normalizes to `TaskDefinition` and one Docker evaluation path runs. | `npm test`; `npm run smoke:docker` passed with `docker-smoke-001` | subagent | completed-local-mirror |
| SWU-HARNESS-006 | [TASK-003](work-pack/tasks/TASK-003.md) | starting-point.md | SWU-HARNESS-005 | batch runner, result store | Batch run records agent, oracle, and infra states separately. | `npm test`; `npm run smoke:batch` passed with `sample-batch-001` | local-fallback | completed-local-mirror |
| SWU-HARNESS-006A | [TASK-003.5](work-pack/tasks/TASK-003.5.md) | SWE-bench docs | SWU-HARNESS-006 | official prediction adapter | Official prediction JSONL writer and harness command wrapper exist. | `npm test` passed | local-fallback | completed |
| SWU-HARNESS-006B | [TASK-003.5](work-pack/tasks/TASK-003.5.md) | SWE-bench docs | SWU-HARNESS-006A | official SWE-bench Lite run artifacts | Official harness completes on a real instance-aligned agent patch and writes `score-result.json`. | `npm run smoke:swebench:official:build`; `npm run smoke:swebench:official` passed with unresolved official score for `astropy__astropy-14365` | local-fallback | completed-official-smoke |
| SWU-HARNESS-007A | [TASK-004](work-pack/tasks/TASK-004.md) | SmellBench paper/release, PyExamine | SWU-HARNESS-006B | SmellBench contract probe | Upstream artifact, install path, task schema, runner command, raw outputs, and score semantics are recorded. | `artifacts/smellbench-contract-probe/report.json`; `artifacts/smellbench-contract-probe/command-notes.md` | manual | completed-contract-probe |
| SWU-HARNESS-007B.1 | [TASK-004](work-pack/tasks/TASK-004.md) | SmellBench contract probe | SWU-HARNESS-007A, B-002 resolved | SmellBench candidate acquisition | One pinned hard task has non-gold metadata, an agent-only brief, a harness-local patch attempt, and a manifest. | `artifacts/smellbench-agent-smoke/smellbench-hard-0001/patch.diff`; `fixtures/smellbench-agent-patches.json`; validator passed with 4,352-byte patch | manual | completed-candidate |
| SWU-HARNESS-007B.2 | [TASK-004](work-pack/tasks/TASK-004.md) | SmellBench evaluator contract | SWU-HARNESS-007B.1 | SmellBench smoke adapter/importer | Candidate manifest is evaluated through verified SmellBench path and writes upstream-derived `score-result.json`. | `npm test`; `npm run smoke:smellbench:official` completed with post-patch PyExamine/Dataset Builder analysis and `status: pass`, `resolved: true` | manual | completed-smoke-adapter |
| SWU-HARNESS-007B | [TASK-004](work-pack/tasks/TASK-004.md) | SWU-HARNESS-007B.1, SWU-HARNESS-007B.2 | B-002A.1 resolved, B-002A.2 resolved | SmellBench real smoke closure | One pinned SmellBench task runs through verified evaluator path and writes upstream-derived `score-result.json`. | `artifacts/smellbench-official-smoke/score-result.json` with `status: pass`; raw evaluator Excel/logs and post-patch analysis under `official-or-upstream-results/` | manual | completed-smellbench-smoke |
| SWU-HARNESS-008A | [TASK-004](work-pack/tasks/TASK-004.md) | PerfCodeBench paper/release | SWU-HARNESS-006B | PerfCodeBench contract probe | Upstream artifact, install path, task schema, runner command, correctness/runtime outputs, and worker constraints are recorded. | `artifacts/perfcodebench-contract-probe/report.json`; README/scripts/sample task verified by direct file paths; full checkout/local run still blocked | manual | completed-partial-contract-probe |
| SWU-HARNESS-008A.1 | [TASK-004](work-pack/tasks/TASK-004.md) | PerfCodeBench direct-file probe | SWU-HARNESS-008A | PerfCodeBench runnable checkout/materialization probe | A complete selected-task checkout is materialized or a precise missing-file/dependency block is recorded before score smoke. | `artifacts/perfcodebench-materialization-probe/report.json`; raw dry-run setup proof at `artifacts/perfcodebench-materialization-probe/materialized/results/dry-run-fast-float.json`; selected task `fast_float_parse` compiled baseline/reference/candidate | manual | completed-materialization-probe |
| SWU-HARNESS-008B.1 | [TASK-004](work-pack/tasks/TASK-004.md) | PerfCodeBench materialization probe | SWU-HARNESS-008A.1 | PerfCodeBench candidate/profile prep | A non-dry-run agent candidate artifact and deterministic worker/noise profile are produced for `fast_float_parse`. | `artifacts/perfcodebench-agent-smoke/report.json`; candidate source/diff; worker profile; compile-only check passed; no score claim | manual | completed-candidate-profile |
| SWU-HARNESS-008B | [TASK-004](work-pack/tasks/TASK-004.md) | SWU-HARNESS-008B.1 | B-003 resolved, deterministic worker/profile decision, agent candidate artifact | PerfCodeBench real smoke | One pinned PerfCodeBench task runs through verified runner and writes upstream-derived `score-result.json`. | `artifacts/perfcodebench-official-smoke/score-result.json` with `status: pass`, `resolved: true`; raw runner output and oracle evidence captured | manual | completed-perfcodebench-score-smoke |
| SWU-HARNESS-009 | [TASK-005](work-pack/tasks/TASK-005.md) | ARCHITECTURE.md | SWU-HARNESS-006 | telemetry/reporting modules | Run report links scores to immutable evidence. | `npm test`; `npm run report:campaign`; campaign report snapshot with 6 runs and 0 evidence gaps | subagent | completed-reporting |
| SWU-HARNESS-010 | [TASK-005](work-pack/tasks/TASK-005.md) | ARCHITECTURE.md | SWU-HARNESS-009 | dashboard API/UI | Operator can inspect per-run status and aggregate scores. | `npm test`; `npm run smoke:dashboard-api`; dashboard data artifact with 6 runs, score components, telemetry counts, and 0 evidence gaps | local-fallback | completed-dashboard-api |
| TASK-VERIFY | [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | WORK-PACK.md, IMPLEMENTATION-LAYERING.md, W0-W3 | TASK-001..TASK-005 | closure audit artifacts and status records | Tests and report/dashboard regeneration pass; score artifacts parse; campaign/dashboard evidence gaps are zero. | `npm test`; `npm run report:campaign`; `npm run smoke:dashboard-api`; `jq empty`; traceability assertions; `artifacts/verification-traceability-audit/report.json` | local-fallback | completed-closure-audit |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | TASK-003 | Exact SWE-bench tech-debt labels, access path, and Docker setup contract must be verified. | Harness maintainer | Resolved for local fixture mirror: `fixtures/swe-bench-local-sample.json`, labels `refactor`, `cleanup`, `tech-debt`, Docker image `test-nestjs-app:latest`; live upstream Hugging Face labels remain unpromoted. | completed-local-mirror |
| B-001A | TASK-003.5 | Official SWE-bench Lite evaluation requires Docker socket access and a real instance-aligned agent patch. | Harness maintainer | Resolved: `fixtures/swebench-lite-agent-patches.json` was generated for `astropy__astropy-14365`; official smoke completed and wrote `artifacts/swebench-lite-official-smoke/score-result.json` with `status: fail`, `resolved: false`. | completed-official-smoke |
| B-002 | TASK-004 | SmellBench release artifact, task schema, PyExamine/static-analysis command, runner/scoring surface, and access/license constraints are unverified. | Harness maintainer | Resolved: `artifacts/smellbench-contract-probe/report.json` verifies Zenodo artifact, package structure, PyExamine/Dataset Builder/MCP/Scheduler/Evaluator flow, hard-task schema, evaluator command, raw outputs, and score semantics. | completed-contract-probe |
| B-002A | SWU-HARNESS-007B | SmellBench real smoke needs a harness-local candidate manifest, one pinned task, an agent-produced candidate artifact, and a smoke adapter/importer before any local SmellBench score can be claimed. | Harness maintainer | Resolved: `npm run smoke:smellbench:official` generated a post-patch PyExamine report, classified it with Dataset Builder, produced upstream evaluator outputs, and wrote `score-result.json` with `status: pass`, not `infra-fail`. | completed-smellbench-smoke |
| B-002A.1 | SWU-HARNESS-007B.1 | A harness-local SmellBench candidate does not exist yet. Bundled benchmark agent outputs must not be used as our candidate. | Harness maintainer | Resolved: `smellbench-hard-0001` selected from the hard scikit-learn CSV, `TASK.md` generated from non-answer fields, local patch attempt exported, and `fixtures/smellbench-agent-patches.json` materialized. | completed-candidate |
| B-002A.2 | SWU-HARNESS-007B.2 | A SmellBench smoke adapter/importer does not exist yet for turning the harness-local candidate into raw evaluator outputs and `score-result.json`. | Harness maintainer | Resolved: adapter validates the manifest, runs post-patch PyExamine and Dataset Builder classification for the pinned candidate, imports raw evaluator output, and maps score only from evaluator metrics. | completed-smoke-adapter |
| B-003 | TASK-004 / SWU-HARNESS-008B | PerfCodeBench score smoke required a non-dry-run agent candidate artifact, accepted deterministic worker/noise profile, and raw runner-derived score artifact. | Infrastructure owner | Resolved: `SWU-HARNESS-008B.1` produced candidate/profile inputs, and `SWU-HARNESS-008B` emitted `artifacts/perfcodebench-official-smoke/score-result.json` from raw runner output. | completed-perfcodebench-score-smoke |

## Gate Checks

1. L0 execution may begin with TASK-001 and TASK-002 only.
2. L1 cannot begin until L0 fixture-local kernel smoke evidence exists.
3. L2 is complete: SmellBench and PerfCodeBench both have upstream-derived score artifacts.
4. L3 and `TASK-VERIFY` are complete; score, report, and dashboard artifacts have closure evidence with zero evidence gaps.
5. Any SWU with multiple file ownership or external suite uncertainty must run alone or be manually coordinated.

## Handoff To Execution Pack

- Execution pack: [work-pack/EXECUTION-PACK.md](work-pack/EXECUTION-PACK.md)
- Recommended next execution: none within this work-pack; create a new work-pack or scale-up task for broader benchmark coverage.
- Next route: closeout or new planning session.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-05-23 | Initial invoke design and plan work-pack created. | Codex |
| 2026-05-23 | Optimized L0 around the benchmark run kernel; moved Docker/live dataset complexity to L1. | Codex |
| 2026-05-23 | Completed TASK-001 skeleton and schema SWUs with passing `npm test`. | Codex |
| 2026-05-23 | Completed SWU-HARNESS-003 adapter contract and mock adapter with passing `npm test`. | Codex |
| 2026-05-25 | Completed SWU-HARNESS-004 fixture-local run kernel, scoring, telemetry, and two-run smoke evidence. | Codex |
| 2026-05-25 | Completed TASK-003 against a local SWE-bench fixture mirror with Docker smoke and batch report evidence. | Codex |
| 2026-05-25 | Added TASK-003.5 official SWE-bench Lite adapter and recorded current runtime/patch blockers. | Codex |
| 2026-05-25 | Completed TASK-003.5 official SWE-bench Lite smoke with a real instance-aligned Codex patch and official unresolved score artifact. | Codex |
| 2026-05-25 | Refined TASK-004 from broad suite probes into benchmark-specific contract probes and real smoke score artifacts using the SWE-bench implementation lessons. | Codex |
| 2026-05-25 | Refreshed readiness after interrogation/distill: start `SWU-HARNESS-007A`; keep `007B/008B` blocked until contract probes resolve. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-007A` SmellBench contract probe and recorded next blocker `B-002A` for local candidate/smoke evidence. | Codex |
| 2026-05-25 | Decomposed `B-002A` into `SWU-HARNESS-007B.1` candidate acquisition and `SWU-HARNESS-007B.2` smoke adapter/importer. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-007B.1` with `smellbench-hard-0001`, an agent-only task brief, harness-local patch artifact, and candidate manifest. | Codex |
| 2026-05-25 | Completed initial `SWU-HARNESS-007B.2` and `SWU-HARNESS-007B` with upstream SmellBench evaluator artifacts; later superseded by real post-patch score evidence. | Codex |
| 2026-05-25 | Upgraded SmellBench smoke to real post-patch PyExamine/Dataset Builder analysis and reran until `score-result.json` reported `status: pass`, `resolved: true`. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-008A` as a PerfCodeBench contract probe block record: paper source verified, anonymous release endpoint returned HTTP 401 `not_connected`, and `SWU-HARNESS-008B` remains blocked. | Codex |
| 2026-05-25 | Refreshed `SWU-HARNESS-008A` after direct PerfCodeBench README/file paths worked; runner surface and sample task are verified, while full checkout/local score smoke remains blocked. | Codex |
| 2026-05-25 | Added `SWU-HARNESS-008A.1` as the missing bridge between PerfCodeBench partial contract verification and real score smoke. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-008A.1`: `fast_float_parse` materialized with `fast_float`, runner imports passed via `/tmp/perfcodebench-pydeps`, and dry-run setup proof wrote raw result JSON. | Codex |
| 2026-05-25 | Ran invoke-style refresh over benchmark artifacts and inserted `SWU-HARNESS-008B.1` as the executable candidate/profile prep before PerfCodeBench score smoke. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-008B.1` with a non-dry-run `fast_float_parse` candidate, diff artifact, candidate manifest, accepted smoke worker profile, and compile-only validation. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-008B` PerfCodeBench score smoke with `status: pass`, `resolved: true`, raw runner output, and oracle evidence artifact. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-009` campaign reporting with dashboard-ready read models, JSON/Markdown report snapshots, and passing tests. | Codex |
| 2026-05-25 | Completed `SWU-HARNESS-010` dashboard-ready static API data contract with smoke validation and generated dashboard data. | Codex |
| 2026-05-26 | Completed `TASK-VERIFY` closure audit with tests, report/dashboard regeneration, JSON validation, traceability assertions, and zero evidence gaps. | Codex |
