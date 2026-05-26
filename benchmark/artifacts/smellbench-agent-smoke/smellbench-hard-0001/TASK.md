# SmellBench Agent Task: smellbench-hard-0001

## Target

- Benchmark: SmellBench
- Project: scikit-learn 1.7.2
- Repository: `https://github.com/scikit-learn/scikit-learn.git`
- Base commit: `25dee604bae18205b01548348388baf7a1cdfe0e`

## Finding

- Type: Architectural
- Name: Scattered Functionality
- Severity: medium
- Difficulty: hard
- Description: Function `make_estimator` appears in 10 modules: `benchmarks.common`, `benchmarks.cluster`, `benchmarks.decomposition`, `benchmarks.ensemble`, `benchmarks.linear_model`, `benchmarks.manifold`, `benchmarks.model_selection`, `benchmarks.neighbors`, `benchmarks.svm`, and `miscellaneous.plot_outlier_detection_bench`.

## Affected Files From The Benchmark Row

- `asv_benchmarks/benchmarks/common.py`
- `asv_benchmarks/benchmarks/cluster.py`
- `asv_benchmarks/benchmarks/decomposition.py`
- `asv_benchmarks/benchmarks/ensemble.py`
- `asv_benchmarks/benchmarks/linear_model.py`
- `asv_benchmarks/benchmarks/manifold.py`
- `asv_benchmarks/benchmarks/model_selection.py`
- `asv_benchmarks/benchmarks/neighbors.py`
- `asv_benchmarks/benchmarks/svm.py`

## Patch Attempt

Make a bounded source change that attempts to reduce repeated estimator-construction logic behind `make_estimator` without changing benchmark semantics. Keep the change small, reviewable, and limited to the benchmark source tree.

Do not use bundled SmellBench model outputs, bundled `tasks_state_*.db` records, bundled post-fix CSV rows, or any gold/reference solution as the candidate patch.

## Produced Candidate

- Patch artifact: `artifacts/smellbench-agent-smoke/smellbench-hard-0001/patch.diff`
- Model label: `codex-local-smoke`
- Candidate type: local bounded patch attempt
