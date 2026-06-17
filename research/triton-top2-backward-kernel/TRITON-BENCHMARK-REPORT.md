# Triton Benchmark Report

Status: `pass-runpod`
Date: 2026-06-14

## Scope

`TASK-W7-003`: benchmark fixed-mask kernels against the selected CAP2
fixed-load exact-backward Triton path.

This is an implementation-path timing report on the recorded RunPod GPU. It is
not a production tuning claim.

## Environment

- Device: NVIDIA RTX PRO 4000 Blackwell
- PyTorch: 2.8.0+cu128
- CUDA: 12.8
- Warmup/iters: 10 / 50

## Results

| Size | Path | T | E | D | Median ms | Mean ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| small | fixed_mask | 128 | 8 | 64 | 0.1350 | 0.1394 |
| small | cap2_fixed_load | 128 | 8 | 64 | 0.1739 | 0.1805 |
| medium | fixed_mask | 512 | 16 | 128 | 0.1378 | 0.1412 |
| medium | cap2_fixed_load | 512 | 16 | 128 | 0.1673 | 0.1707 |

Raw artifacts:

- `development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json`
- `development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/BENCHMARK.md`

## Interpretation

- Fixed-mask timing includes Triton `dW`, `dX_router`, and `dH`.
- CAP2 timing includes row-local CAP2 `dZ`/`dH`, plus Triton `dX_router` and
  `dW`.
- CAP2 is slower than the fixed-mask path in these smoke sizes because it
  computes the smooth pairwise rank relaxation in addition to the shared matrix
  reductions.
- Both measured paths complete in sub-millisecond median time for the selected
  smoke sizes on the recorded RunPod GPU.

## Remaining Limits

- These are two smoke sizes, not an exhaustive scaling study.
- No claim is made about production-optimal block sizes or fusion.
- CAP2 zero-allocation memory behavior is partially supported through
  preallocated outputs, but not yet promoted as a separate W7 acceptance claim.
- CAP2 remains candidate-only and non-novelty-claimed.
