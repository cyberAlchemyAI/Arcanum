# PerfCodeBench Contract Probe Report

## Status

- Result: `partial-contract-verified`
- Blocker: `B-003`
- SWU: `SWU-HARNESS-008A`
- Decision: README, scripts, and one sample task are accessible by direct file path; do not start `SWU-HARNESS-008B` until a complete runnable checkout and worker profile are verified.

## What Was Verified

The arXiv source confirms the expected benchmark shape:

- 1,854 executable tasks.
- Languages include C, C++, Go, Java, Python, and CUDA.
- Each task contains metadata, a benchmark harness, `baseline`, `reference`, and candidate slot.
- Candidate implementations must preserve the same function contract as the baseline/reference.
- Correctness is checked by deterministic task-specific oracles.
- Runtime is measured through repeated runs and median latency.
- Metrics include CRR, FBR, RBR, CGRE, and thresholded CGRE.

The direct README path confirms the repository surface:

- executable tasks in `executable_tasks/`,
- evaluation scripts in `scripts/`,
- model config in `configs.json`,
- single-task command `python3 scripts/run_openai_codegen_eval.py fast_float_parse --model gpt-5.4 --runs 3`,
- subset command `python3 scripts/run_model_suite.py --model gpt-5.4 --limit 10 --runs 3`,
- outputs in `results/`,
- candidate code in each task's `candidate/<model>/`,
- build artifacts in `build/`.

Direct file paths also returned `configs.json`, runner scripts, `executable_tasks/fast_float_parse/instance.json`, baseline source, and harness source.

## What Still Blocks Score Smoke

The release pointer is not currently available as a cloneable/listable full checkout from the tested endpoints.

Evidence:

- `git ls-remote https://anonymous.4open.science/r/perfcodebench-7CDE.git` returned repository not found.
- `curl -L -I https://anonymous.4open.science/r/perfcodebench-7CDE` redirected to `/api/repo/perfcodebench-7CDE/file/` and returned HTTP 401.
- `curl -L https://anonymous.4open.science/r/perfcodebench-7CDE` returned `{"error":"not_connected"}`.

Because of that, this probe still cannot verify:

- complete repository layout,
- license/access terms,
- full task inventory,
- all selected-task dependencies,
- local execution of the runner,
- raw output from a real local run.

## Worker Constraint From Paper

The paper reports a substantial evaluation environment: two Intel Xeon Platinum 8480C CPUs, 224 logical CPU cores, 2.0 TiB RAM, and three NVIDIA H800 GPUs. It also reports Python 3.13.3, GCC/G++ 11.4.0, Go 1.18.1, Java 11.0.30, CUDA 12.1, PyTorch 2.8.0, NumPy 2.2.6, Pandas 3.0.2, and Numba 0.61.2.

This means a future score smoke must record worker profile, repetitions, warmups, timeout policy, CPU/GPU pool, and noise status before claiming benchmark evidence.

## Unblock Actions

1. Materialize a complete runnable checkout from clone, archive, or scripted direct-file fetch.
2. Record the complete release layout and license/access terms.
3. Verify selected-task dependencies, especially `external/` dependencies referenced by `instance.json`.
4. Run a dry or reuse-candidate single-task command locally and capture raw result JSON.
5. Decide whether local hardware is acceptable for a smoke or whether a dedicated worker is required.
6. Only then start `SWU-HARNESS-008B`.
