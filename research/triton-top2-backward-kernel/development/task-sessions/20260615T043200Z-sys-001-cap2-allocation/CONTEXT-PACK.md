# Context Pack - SWU-SYS-001 CAP2 CUDA Memory-Stat Allocation Test

Task: Add a CAP2 CUDA memory-stat zero-allocation test and validate it on the CUDA/Triton runner.

Primary work-pack: `research/triton-top2-backward-kernel/development/invoke-runs/20260615T032100Z-systems-hardening-workpack/WORK-PACK.md`

Evidence read:

- `research/triton-top2-backward-kernel/tests/test_router_triton.py`
- `research/triton-top2-backward-kernel/reference/router_triton.py`
- `research/triton-top2-backward-kernel/development/invoke-runs/20260615T032100Z-systems-hardening-workpack/WORK-PACK.md`

Decision:

Add the strict memory-stat test beside the existing CAP2 pointer-reuse test, using warm-up, preallocated outputs, `torch.cuda.reset_peak_memory_stats()`, and equality checks for `memory_allocated` and `max_memory_allocated`.

Blocker:

CUDA validation requires a live NVIDIA/Triton runner. The previously used RunPod endpoint `<redacted-runner-host>:<redacted-runner-port>` refused SSH connection during the iteration script.
