# PerfCodeBench Official Smoke Command Notes

## Candidate Materialization

The prepared candidate was copied into the materialized PerfCodeBench runner slot:

```text
artifacts/perfcodebench-materialization-probe/materialized/executable_tasks/fast_float_parse/candidate/codex-local-smoke/solution.cpp
```

The previous candidate binary was removed so the runner rebuilt it.

## Runner Command

```bash
env PYTHONPATH=/tmp/perfcodebench-pydeps python3 scripts/run_openai_codegen_eval.py fast_float_parse --model codex-local-smoke --runs 3 --reuse-candidate --output results/codex-local-smoke-fast-float-runs3.json
```

Working directory:

```text
artifacts/perfcodebench-materialization-probe/materialized
```

## Raw Result

`artifacts/perfcodebench-official-smoke/raw/codex-local-smoke-fast-float-runs3.json`

## Interpretation

The smoke score is derived only from the raw PerfCodeBench runner JSON. The candidate passed correctness and had a lower median runtime than the baseline under the accepted three-run smoke profile.

