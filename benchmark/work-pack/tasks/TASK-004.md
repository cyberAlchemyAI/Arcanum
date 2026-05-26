# TASK-004: Probe SmellBench And PerfCodeBench Official Paths

## Objective

Refine the remaining benchmark integrations using the official SWE-bench lesson: do not claim benchmark evidence from local mirrors or inferred scoring. First verify each upstream contract, then run the smallest real benchmark smoke that produces a score artifact derived from raw upstream benchmark output.

## Layer And Slice Mapping

- Layer: L2
- Slice: S-004
- Wave: [W2](../waves/W2.md)

## Source Contracts

- [../../starting-point.md](../../starting-point.md)
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
- SmellBench paper: `https://arxiv.org/abs/2605.07001`
- SmellBench release pointer from paper: `https://doi.org/10.5281/zenodo.19247588`
- PyExamine reference implementation: `https://github.com/KarthikShivasankar/python_smells_detector`
- PerfCodeBench paper: `https://arxiv.org/abs/2605.15222`
- PerfCodeBench release pointer from paper: `https://anonymous.4open.science/r/perfcodebench-7CDE`

## Dependencies

- TASK-003.5 completed with official SWE-bench Lite smoke evidence.
- B-002 resolved by SmellBench contract probe before SmellBench scoring smoke.
- B-003 resolved by PerfCodeBench contract probe before PerfCodeBench scoring smoke.

## Implementation Detail

Inputs:

- Verified SmellBench artifact source, task data shape, runner/scoring command, and license/access constraints.
- Verified PerfCodeBench artifact source, task data shape, runner/scoring command, hardware/runtime constraints, and license/access constraints.
- Existing `TaskDefinition` and `OracleEvidence` schemas.
- Candidate patch/source-change artifact produced by the agent for the selected smoke task; do not substitute benchmark gold/reference solutions.

Outputs:

- SmellBench contract probe report.
- SmellBench real smoke score artifact, or a precise block if no runnable upstream artifact is available.
- PerfCodeBench contract probe report.
- PerfCodeBench real smoke score artifact, or a precise block if no runnable upstream artifact is available.
- Schema extension proposal only if the current evidence model is insufficient.

Implementation notes:

1. Start with contract probes, not adapter implementation.
2. For each benchmark, record the exact upstream artifact, install command, dataset/task fields, runner command, raw result files, and score semantics.
3. Use one pinned smoke task per benchmark before broad ingestion.
4. Require an agent-produced candidate artifact aligned to the selected task; do not use gold patches, reference optimized code, or local fixture substitutes as benchmark evidence.
5. Import raw upstream result files/logs into `artifacts/<run-id>/official-or-upstream-results/`.
6. Emit a local `score-result.json` derived only from raw upstream result files. If the upstream benchmark lacks a canonical score file, derive only from documented upstream output fields and label the derivation in the report.
7. Normalize into `OracleEvidence` only after the raw result import exists; do not custom-run the benchmark's underlying commands as a replacement for the benchmark harness.
8. Block full adapter work if the benchmark cannot produce a real score artifact or if evidence cannot be represented without a schema decision.

## Benchmark-Specific Implementation Inventory

### SWE-bench Bridge Reference

This task inherits the completed SWE-bench Lite bridge as the reference pattern:

1. Use official docs as the runner contract: `https://www.swebench.com/SWE-bench/guides/evaluation/`, `https://www.swebench.com/SWE-bench/guides/datasets/`, and `https://www.swebench.com/SWE-bench/guides/docker_setup/`.
2. Keep the upstream harness as the grading authority: `python -m swebench.harness.run_evaluation`.
3. Convert agent patches into official prediction JSONL with `instance_id`, `model_name_or_path`, and `model_patch`.
4. Import upstream `results.json`, `instance_results.jsonl`, reports, and logs before mapping local status.
5. Treat official unresolved output as `fail`, not `infra-fail`.
6. Treat missing Docker, dataset, prediction, or result files as `infra-fail`.

### SmellBench

References:

- Paper: `https://arxiv.org/abs/2605.07001`
- Release pointer: `https://doi.org/10.5281/zenodo.19247588`
- PyExamine reference implementation: `https://github.com/KarthikShivasankar/python_smells_detector`

Required integration steps:

1. Probe the release artifact and record whether it contains runnable data/code, task metadata, scoring scripts, and raw output examples.
2. Record task fields needed by the harness: smell ID, smell type, target project/version, scope, PyExamine finding, expert validation label availability, and expected scoring dimensions.
3. Verify the exact runner command or documented scoring derivation. PyExamine alone is not enough unless SmellBench explicitly defines it as the scoring surface.
4. Select one pinned smell task and generate an agent brief that does not expose expert labels or expected repair outcomes.
5. Materialize a candidate manifest with the selected smell task ID, model label, and an agent-produced source-change artifact.
6. Run the verified SmellBench path, import raw outputs/logs, and emit `score-result.json`.
7. Preserve repair effectiveness, false-positive identification, and net codebase impact as separate result fields before any aggregate pass/fail mapping.
8. Block if release access, runner semantics, or score derivation cannot be verified.

### PerfCodeBench

References:

- Paper: `https://arxiv.org/abs/2605.15222`
- Release pointer: `https://anonymous.4open.science/r/perfcodebench-7CDE`

Required integration steps:

1. Probe the release artifact and record task metadata, correctness runner, runtime runner, baseline implementation, reference optimized solution fields, raw outputs, and access/license terms.
2. Define the worker profile before scoring: CPU/GPU, memory, compiler/runtime versions, isolation, repetitions, warmups, timeouts, and noise threshold.
3. Select one pinned task and generate an agent brief that does not expose the reference optimized solution or reference timing.
4. Materialize a candidate manifest with task ID, model label, candidate source artifact, and worker profile reference.
5. Run correctness first; failing correctness maps to `fail` and must not claim performance improvement.
6. Run the documented performance measurement path only after correctness passes or when the benchmark explicitly records failing-candidate timing.
7. Import correctness output, timing series, logs, and worker profile, then emit `score-result.json`.
8. Preserve correctness, speedup/runtime delta, threshold, repetitions, noise status, and worker metadata in normalized evidence.
9. Block if the release is inaccessible, the worker is not deterministic enough, or timing output cannot be tied to the candidate artifact.

Edge cases:

- Structural smell reduction without semantic correctness should not be scored as full pass.
- Performance speedup with failing tests should not be scored as full pass.
- SmellBench false-positive classification is a first-class outcome, not a failed repair by default.
- SmellBench net impact matters: removing one smell while introducing more smells must not be collapsed into pass.
- PerfCodeBench speedup must be paired with correctness success and worker profile metadata.
- Noisy performance measurements must be rerun or quarantined with the raw measurement series preserved.

## Smallest Working Units

### SWU-HARNESS-007A

- Goal: verify the SmellBench upstream contract before implementation.
- Dependencies: SWU-HARNESS-006B completed.
- Write scope: SmellBench probe report and blocker updates only.
- Done criteria: exact artifact source, install path, task schema, runner command, raw output files, and scoring semantics are recorded.
- Acceptance evidence: `artifacts/smellbench-contract-probe/report.json` plus linked raw command/output notes, or a block record naming the missing upstream artifact.
- Completion evidence: `artifacts/smellbench-contract-probe/report.json` and `artifacts/smellbench-contract-probe/command-notes.md`.
- Verification: reviewable probe report; evaluator command `python generate_cross_comparison.py` completed and wrote `evaluation_reports/cross_agent_comparison_20260525_152420.xlsx`.
- Execution owner: manual.
- Handoff note: confirm whether the Zenodo release contains runnable data/code or only paper artifacts; verify PyExamine command separately from SmellBench scoring.
- Status: completed-contract-probe.

### SWU-HARNESS-007B

- Goal: run one real SmellBench structural smoke and emit an upstream-derived score artifact.
- Dependencies: SWU-HARNESS-007A, B-002 resolved, B-002A.1 and B-002A.2 resolved, agent candidate artifact for the selected smell task.
- Write scope: SmellBench smoke runner, candidate manifest, artifact import, score artifact, and focused tests.
- Done criteria: one pinned SmellBench task runs through the verified evaluator path and writes `score-result.json`.
- Acceptance evidence: `artifacts/smellbench-official-smoke/score-result.json`, raw upstream results/logs, candidate manifest, and normalized `OracleEvidence` sample.
- Verification: `npm run smoke:smellbench:official` or documented block if no runnable official harness exists.
- Execution owner: manual.
- Handoff note: score fields must preserve repair effectiveness, false-positive outcome, and net impact separately before any aggregate status.
- Completion evidence: `artifacts/smellbench-official-smoke/score-result.json`, `artifacts/smellbench-official-smoke/official-smellbench-report.json`, `artifacts/smellbench-official-smoke/oracle-evidence.json`, and raw evaluator outputs under `artifacts/smellbench-official-smoke/official-or-upstream-results/`.
- Verification result: `npm run smoke:smellbench:official` completed after generating a post-patch PyExamine report and Dataset Builder classification, then wrote `status: pass`, `resolved: true` from upstream evaluator metrics.
- Status: completed-smellbench-smoke.

### SWU-HARNESS-007B.1

- Goal: prepare a harness-local SmellBench candidate source without using bundled benchmark agent outputs.
- Dependencies: SWU-HARNESS-007A, B-002 resolved.
- Write scope: pinned task metadata, local scikit-learn checkout/preparation notes, agent task brief, candidate manifest contract, and generated patch artifact.
- Done criteria: one deterministic SmellBench hard task is selected, an agent-only task brief is generated from non-answer fields, a local patch attempt is made against scikit-learn 1.7.2, and a non-empty patch artifact is exported.
- Acceptance evidence: `artifacts/smellbench-agent-smoke/<task-id>/task-metadata.json`, `TASK.md`, `patch.diff`, and `fixtures/smellbench-agent-patches.json`.
- Completion evidence: `artifacts/smellbench-agent-smoke/smellbench-hard-0001/task-metadata.json`, `artifacts/smellbench-agent-smoke/smellbench-hard-0001/TASK.md`, `artifacts/smellbench-agent-smoke/smellbench-hard-0001/patch.diff`, and `fixtures/smellbench-agent-patches.json`.
- Verification: manifest validator confirms selected task exists in `CodeSmells_Scikit_architectural_hard_classification.csv`, `patch.diff` is non-empty, and manifest points only to harness-local artifacts.
- Verification result: passed; selected task exists in a 65-row hard CSV, manifest has one entry, and `patch.diff` is 4,352 bytes.
- Execution owner: manual.
- Handoff note: bundled `tasks_state_*.db`, bundled post-fix CSVs, and anonymous experiment repositories are allowed as contract/reference evidence only; they must not be used as our candidate patch.
- Status: completed-candidate.

### SWU-HARNESS-007B.2

- Goal: build the SmellBench real-smoke adapter/importer around the verified evaluator.
- Dependencies: SWU-HARNESS-007B.1.
- Write scope: smoke command, manifest validator, evaluator import path, score artifact mapper, report importer, and focused tests.
- Done criteria: the smoke command consumes the harness-local candidate manifest, runs or invokes the verified SmellBench evaluation path for the pinned task/candidate scope, imports raw evaluator outputs, and writes `score-result.json`.
- Acceptance evidence: `artifacts/smellbench-official-smoke/candidate-manifest.json`, raw evaluator outputs under `official-or-upstream-results/`, `score-result.json`, and normalized `OracleEvidence` sample.
- Verification: `npm run smoke:smellbench:official` produces `status: pass` or `status: fail`; `infra-fail` is not accepted as plumbing proof.
- Execution owner: manual.
- Handoff note: if the upstream evaluator only supports full-agent batch reports, the adapter must generate the minimal required post-fix CSV/task_state pair for the pinned candidate by running post-patch analysis and classification, or block with the exact missing evaluator granularity; do not infer score from PyExamine alone.
- Completion evidence: `src/smellbench.ts`, `src/run-smellbench-official-smoke.ts`, `test/smellbench.test.ts`, `artifacts/smellbench-official-smoke/candidate-manifest.json`, `artifacts/smellbench-official-smoke/official-or-upstream-results/`, `artifacts/smellbench-official-smoke/score-result.json`, and `artifacts/smellbench-official-smoke/oracle-evidence.json`.
- Verification result: `npm test` passed; `npm run smoke:smellbench:official` passed with upstream evaluator metrics `Tasks Attempted: 1`, `Failed Repairs: 1`, `Weighted Repair Score: 0.1000`, `Overall Effectiveness: 0.1000`.
- Status: completed-smoke-adapter.

### SWU-HARNESS-008A

- Goal: verify the PerfCodeBench upstream contract before implementation.
- Dependencies: SWU-HARNESS-006B completed.
- Write scope: PerfCodeBench probe report and blocker updates only.
- Done criteria: exact artifact source, install path, task schema, runner command, correctness output, runtime output, reference/baseline fields, and hardware constraints are recorded.
- Acceptance evidence: `artifacts/perfcodebench-contract-probe/report.json` plus linked raw command/output notes, or a block record naming the missing upstream artifact.
- Verification: reviewable probe report.
- Execution owner: manual.
- Handoff note: separate benchmark availability from hardware determinism; a public repo may be available while real scoring is still blocked by worker constraints.
- Completion evidence: `artifacts/perfcodebench-contract-probe/report.json`, `artifacts/perfcodebench-contract-probe/report.md`, and `artifacts/perfcodebench-contract-probe/command-notes.md`.
- Verification result: arXiv source verified task shape, score semantics, and worker constraints; direct README/file paths verified runner commands, `configs.json`, scripts, and one sample `fast_float_parse` task; root listing/clone still blocked with repository not found and HTTP 401 `{"error":"not_connected"}`.
- Status: completed-partial-contract-probe.

### SWU-HARNESS-008A.1

- Goal: finish the PerfCodeBench probe bridge by materializing a runnable selected-task checkout before any score-smoke claim.
- Dependencies: SWU-HARNESS-008A completed partial contract probe.
- Write scope: materialization script or notes, selected-task file inventory, local runner preflight/output artifact, worker profile record, and blocker/work-pack updates.
- Done criteria: `fast_float_parse` or another pinned low-cost CPU task has a complete local tree with `instance.json`, `baseline`, `reference`, `candidate`, `harness`, required `external/` dependencies, runner imports, and either one raw local result JSON or a precise missing-file/dependency block.
- Acceptance evidence: `artifacts/perfcodebench-materialization-probe/report.json`, direct-file inventory, local command notes, and raw result JSON if runnable.
- Verification: reviewable probe report; `jq empty` for JSON artifacts; local runner command when materialization succeeds.
- Completion evidence: `artifacts/perfcodebench-materialization-probe/report.json`, `artifacts/perfcodebench-materialization-probe/file-inventory.json`, `artifacts/perfcodebench-materialization-probe/worker-profile.json`, and `artifacts/perfcodebench-materialization-probe/materialized/results/dry-run-fast-float.json`.
- Verification result: `fast_float_parse` materialized with `instance.json`, baseline, reference, dry-run candidate, harness, `fast_float` external headers, runner scripts, and compiled binaries. Dry-run runner output is setup proof only and not a score.
- Execution owner: manual.
- Handoff note: this SWU may use scripted direct-file fetch if clone/archive remains unavailable. Do not use reference optimized code as an agent candidate. If using `--dry-run`, label it setup proof rather than benchmark score.
- Status: completed-materialization-probe.

### SWU-HARNESS-008B

- Goal: run one real PerfCodeBench performance smoke and emit an upstream-derived score artifact.
- Dependencies: SWU-HARNESS-008B.1, B-003 resolved, isolated worker/profile decision, agent candidate artifact for the selected task.
- Write scope: PerfCodeBench smoke runner, prediction/candidate manifest, artifact import, score artifact, and focused tests.
- Done criteria: one pinned PerfCodeBench task runs through the verified runner and writes `score-result.json` with correctness, runtime, threshold, repetitions, and noise metadata.
- Acceptance evidence: `artifacts/perfcodebench-official-smoke/score-result.json`, raw upstream results/logs, candidate manifest, worker profile record, and normalized `OracleEvidence` sample.
- Verification: `npm run smoke:perfcodebench:official` or documented block if no deterministic runnable profile exists.
- Completion evidence: `artifacts/perfcodebench-official-smoke/score-result.json`, `artifacts/perfcodebench-official-smoke/raw/codex-local-smoke-fast-float-runs3.json`, `artifacts/perfcodebench-official-smoke/official-perfcodebench-report.json`, and `artifacts/perfcodebench-official-smoke/oracle-evidence.json`.
- Verification result: PerfCodeBench runner exited `0`; candidate correctness passed; candidate median runtime was `7495451 ns` versus baseline `69189972 ns`; `score-result.json` reports `status: pass`, `resolved: true`.
- Execution owner: manual.
- Handoff note: a faster candidate with failed correctness is `fail`; unavailable or noisy worker is `infra-fail` or `quarantined`, not `pass`.
- Current block: none; candidate/profile inputs are available under `artifacts/perfcodebench-agent-smoke/`.
- Status: completed-perfcodebench-score-smoke.

### SWU-HARNESS-008B.1

- Goal: prepare the missing PerfCodeBench score-smoke inputs without claiming a score.
- Dependencies: SWU-HARNESS-008A.1 completed materialization probe.
- Write scope: `artifacts/perfcodebench-agent-smoke/`, candidate manifest or notes, worker profile record, blocker/work-pack updates.
- Done criteria: a non-dry-run agent candidate source/diff exists for `fast_float_parse`, the candidate is not copied from the reference optimized solution, an accepted deterministic worker/noise profile is recorded, and `SWU-HARNESS-008B` has concrete input paths.
- Acceptance evidence: `artifacts/perfcodebench-agent-smoke/fast_float_parse/candidate/solution.cpp`, `artifacts/perfcodebench-agent-smoke/fast_float_parse/patch.diff`, `artifacts/perfcodebench-agent-smoke/worker-profile.json`, and `artifacts/perfcodebench-agent-smoke/report.json`.
- Verification: candidate artifact is non-empty; diff is non-empty; worker profile JSON passes `jq empty`; report links to materialized task and candidate artifact.
- Completion evidence: `artifacts/perfcodebench-agent-smoke/report.json`, `artifacts/perfcodebench-agent-smoke/fast_float_parse/candidate-manifest.json`, `artifacts/perfcodebench-agent-smoke/worker-profile.json`, and compile-only validation against the materialized harness.
- Verification result: JSON artifacts passed `jq empty`; candidate source and diff are non-empty; candidate compiles with `g++ -O3 -std=c++17` against the materialized harness and `fast_float` include tree.
- Execution owner: manual.
- Handoff note: use the `fast_float_parse` problem statement, allowed include list, baseline implementation, and harness interface from the materialized checkout. Do not inspect or copy the reference optimized implementation. This SWU prepares inputs only; score execution remains `SWU-HARNESS-008B`.
- Status: completed-candidate-profile.

## Synchronization Rules

SWU-HARNESS-007A and SWU-HARNESS-008A may run in parallel because they are read/probe-only and have disjoint artifact paths. Do not start SWU-HARNESS-007B or SWU-HARNESS-008B until the corresponding contract/materialization probe resolves the benchmark-specific blocker. SWU-HARNESS-008B additionally requires `SWU-HARNESS-008B.1` to produce a real agent candidate artifact and accepted worker/noise policy; `SWU-HARNESS-008A.1` dry-run output is not score evidence.

## Completion Evidence

- Both contract probes either pass or record a precise upstream availability block.
- Any completed smoke produces a score artifact derived only from raw upstream benchmark output.
- TASK-004 is complete: SmellBench and PerfCodeBench both emitted real score artifacts derived from upstream or verified runner outputs.
