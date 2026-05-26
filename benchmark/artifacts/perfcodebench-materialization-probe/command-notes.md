# PerfCodeBench Materialization Command Notes

## Commands Run

```bash
git clone --depth 1 https://github.com/fastfloat/fast_float.git artifacts/perfcodebench-materialization-probe/materialized/external/fast_float
```

Purpose: replace a bad direct-header fetch payload with the real dependency tree required by `fast_float_parse`.

```bash
python3 -m pip install --target /tmp/perfcodebench-pydeps openai
```

Purpose: satisfy the runner's import-time `openai` dependency without changing the project environment.

```bash
env PYTHONPATH=/tmp/perfcodebench-pydeps python3 scripts/run_openai_codegen_eval.py fast_float_parse --model gpt-5.4 --runs 1 --dry-run --output results/dry-run-fast-float.json
```

Purpose: compile and run baseline, reference, and dry-run candidate variants through the verified PerfCodeBench runner.

## Result

- Raw output: `artifacts/perfcodebench-materialization-probe/materialized/results/dry-run-fast-float.json`
- Baseline status: `ok`
- Reference status: `ok`
- Candidate status: `ok`
- Candidate source: dry-run placeholder copied from baseline.

## Interpretation

This is materialization evidence only. It proves the selected task tree, dependency tree, runner imports, compile path, and raw result JSON emission. It is not the real PerfCodeBench agent-candidate score smoke.

