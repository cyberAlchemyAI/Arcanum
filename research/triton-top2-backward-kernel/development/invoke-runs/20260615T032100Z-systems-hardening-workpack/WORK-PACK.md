# Work Pack - CAP2 Systems Hardening

Status: `ready-for-task-session`
Owner: `research/triton-top2-backward-kernel`

## Objective

Strengthen CAP2 systems evidence from parity/smoke benchmark to guarded W7-style
acceptance for allocation, FP16, and benchmark reproducibility.

## Source Evidence

- `stages/subagents/systems-validation-reviewer.md` from the review refine run.
- `CAP2-W6-PARITY-REPORT.md`
- `TRITON-BENCHMARK-REPORT.md`
- `tests/test_router_triton.py`
- `scripts/benchmark_triton_paths.py`

## Task Board

| Task ID | Layer | Task | Status |
| --- | --- | --- | --- |
| TASK-SYS-001 | L0 | Add CAP2 CUDA memory-stat zero-allocation test. | ready |
| TASK-SYS-002 | L1 | Add CAP2 FP16/mixed-precision parity test. | ready-after-001 |
| TASK-SYS-003 | L2 | Extend benchmark sweep and environment capture. | ready-after-002 |
| TASK-SYS-004 | L3 | Sync benchmark and evidence reports. | ready-after-003 |

## SWU Manifest

| SWU ID | Parent | Goal | Write Scope | Validation |
| --- | --- | --- | --- | --- |
| SWU-SYS-001 | TASK-SYS-001 | Warm up CAP2 kernels, reset CUDA stats, rerun with preallocated outputs, assert no allocation increase. | `tests/test_router_triton.py` | RunPod focused Triton tests |
| SWU-SYS-002 | TASK-SYS-002 | Test CAP2 FP16 inputs with explicit FP32 output/tolerance contract. | `tests/test_router_triton.py`, maybe `reference/router_triton.py` | RunPod focused Triton tests |
| SWU-SYS-003 | TASK-SYS-003 | Add CLI sweep sizes/dtypes/env capture. | `scripts/benchmark_triton_paths.py` | benchmark JSON includes env fields |
| SWU-SYS-004 | TASK-SYS-004 | Update reports from new GPU evidence. | `TRITON-BENCHMARK-REPORT.md`, `DATA-APPENDIX.md`, `EVIDENCE-MANIFEST.md` | report cites new receipts |

## Gates

- Requires NVIDIA CUDA/Triton runner.
- Do not claim CAP2 W7 acceptance until `SWU-SYS-001` and `SWU-SYS-002` pass on GPU.
- Benchmark reports must keep smoke-vs-scaling scope explicit.

## Next Route

`task-session` beginning with `SWU-SYS-001` on RunPod/CUDA runner.
