# PerfCodeBench Contract Probe Command Notes

## Source Probe

Command:

```bash
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/README.md
```

Result: passed. The direct README path returned Markdown that documents:

- tasks under `executable_tasks/`,
- evaluation scripts under `scripts/`,
- model config in `configs.json`,
- single-task command `python3 scripts/run_openai_codegen_eval.py fast_float_parse --model gpt-5.4 --runs 3`,
- subset command `python3 scripts/run_model_suite.py --model gpt-5.4 --limit 10 --runs 3`,
- outputs under `results/`, candidates under each task's `candidate/<model>/`, and build artifacts under `build/`.

Command:

```bash
git ls-remote https://anonymous.4open.science/r/perfcodebench-7CDE.git
```

Result:

```text
fatal: repository 'https://anonymous.4open.science/r/perfcodebench-7CDE.git/' not found
```

Command:

```bash
curl -L -I https://anonymous.4open.science/r/perfcodebench-7CDE
```

Result:

```text
HTTP/2 302
location: /api/repo/perfcodebench-7CDE/file/

HTTP/2 401
content-type: application/json; charset=utf-8
```

Command:

```bash
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE
```

Result:

```json
{"error":"not_connected"}
```

Direct file API samples:

```bash
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/configs.json
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/scripts/run_openai_codegen_eval.py
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/scripts/run_model_suite.py
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/executable_tasks/fast_float_parse/instance.json
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/executable_tasks/fast_float_parse/baseline/solution.cpp
curl -L https://anonymous.4open.science/r/perfcodebench-7CDE/executable_tasks/fast_float_parse/harness/benchmark_main.cpp
```

Result: passed. These direct paths returned the expected files.

Sample task schema from `fast_float_parse/instance.json`:

```json
{
  "task_id": "fast_float_parse",
  "title": "Optimize decimal parsing throughput",
  "goal": "Parse a large newline-delimited decimal buffer and return the sum of all values.",
  "metric": "median elapsed_ns over repeated runs; lower is better",
  "correctness_rule": "Returned sum must be within relative tolerance 1e-12 of the expected sum.",
  "allowed_external_includes": ["fast_float/fast_float.h"],
  "build": {
    "compiler": "g++",
    "cxxflags": ["-O3", "-std=c++17", "-I{task_dir}/harness", "-I{root}/external/fast_float/include"],
    "sources": ["{task_dir}/harness/benchmark_main.cpp", "{variant_dir}/solution.cpp"]
  }
}
```

## Paper Source Probe

Command:

```bash
curl -L -o /tmp/perfcodebench-src.tar.gz https://arxiv.org/e-print/2605.15222
tar -xzf /tmp/perfcodebench-src.tar.gz -C /tmp/perfcodebench-src
```

Useful source files:

- `/tmp/perfcodebench-src/neurips_2026.tex`
- `/tmp/perfcodebench-src/texs/main_table.tex`
- `/tmp/perfcodebench-src/texs/data_source.tex`

## Probe Conclusion

The arXiv source plus direct README/file paths are sufficient to record expected task shape, runner commands, output locations, candidate contract, scoring semantics, and worker constraints. `SWU-HARNESS-008B` is still blocked until we materialize a complete runnable checkout or archive, verify all dependencies for the selected task, and accept a deterministic worker profile.
