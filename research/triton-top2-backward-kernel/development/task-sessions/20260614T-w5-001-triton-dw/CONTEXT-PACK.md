# Context Pack - TASK-W5-001

Task: `TASK-W5-001`

Objective: implement Triton fixed-mask `dW` kernel.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W5-001` is ready after `TASK-W0-008` passed on RunPod.
- `RUNPOD-W5-READY-BUNDLE-PASS.md`: proves a CUDA/Triton pod is available.
- `reference/router_reference.py`: `fixed_mask_manual_backward` and
  `finite_difference_d_w` define the fixed-mask `dW` oracle.
- `reference/router_torch.py`: PyTorch fixed-mask reference.
- `tests/test_router_reference.py` and `tests/test_router_torch.py`: existing
  CPU/PyTorch parity ladder.

## Implementation Boundary

W5 baseline implements only:

```text
dW = dZ^T @ X
```

where `dZ` comes from the fixed-mask backward graph. This does not claim a fused
full backward, hard Top2 differentiability, zero allocation, or final FP16
tolerance/performance.

## Validation Surface

- Local CPU-only suite should still pass with Triton tests skipped.
- RunPod CUDA suite must run `tests/test_router_triton.py` and pass.
