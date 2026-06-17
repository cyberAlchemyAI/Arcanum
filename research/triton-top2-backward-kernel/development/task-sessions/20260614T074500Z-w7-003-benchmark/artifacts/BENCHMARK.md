# Triton Path Benchmark

Timestamp: `2026-06-14T07:44:35Z`
Device: `NVIDIA RTX PRO 4000 Blackwell`
PyTorch: `2.8.0+cu128`
CUDA: `12.8`
Warmup/iters: `10` / `50`

| Size | Path | T | E | D | Median ms | Mean ms | Min ms | Max ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| small | fixed_mask | 128 | 8 | 64 | 0.1350 | 0.1394 | 0.1306 | 0.2688 |
| small | cap2_fixed_load | 128 | 8 | 64 | 0.1739 | 0.1805 | 0.1656 | 0.2990 |
| medium | fixed_mask | 512 | 16 | 128 | 0.1378 | 0.1412 | 0.1309 | 0.1724 |
| medium | cap2_fixed_load | 512 | 16 | 128 | 0.1673 | 0.1707 | 0.1646 | 0.2110 |

Notes:

- Fixed-mask timing includes Triton `dW`, `dX_router`, and `dH` kernels.
- CAP2 timing includes row-local CAP2 `dZ`/`dH`, plus Triton `dX_router` and `dW` kernels.
- These are implementation-path timings on the recorded RunPod GPU, not a production tuning claim.
