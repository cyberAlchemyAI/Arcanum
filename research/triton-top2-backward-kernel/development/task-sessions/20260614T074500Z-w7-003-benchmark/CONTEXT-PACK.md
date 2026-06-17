# Context Pack - TASK-W7-003 Benchmark

Task: `TASK-W7-003`
Mode: lean

## Objective

Benchmark fixed-mask Triton kernels against the selected CAP2 fixed-load
exact-backward Triton path after W5, W6, W7-001, and W7-002 have passed.

## Controlling Sources

- `WORK-PACK.md` marks `TASK-W7-003` ready after W6 closure.
- `CAP2-W6-PARITY-REPORT.md` defines the CAP2 selected-relaxation path.
- `reference/router_triton.py` exposes fixed-mask and CAP2 Triton wrappers.
- RunPod is the active CUDA/Triton validation environment.

## Obligations

- Add a repeatable benchmark command.
- Run the benchmark on the CUDA/Triton pod.
- Save raw JSON and Markdown artifacts.
- Update the work-pack without claiming production tuning.

## Gate Verdict

Pass. Dependencies are complete and the RunPod runner is available.
