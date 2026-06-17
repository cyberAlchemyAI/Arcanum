# Task Session Result - TASK-W7-002

Status: `pass-runpod`

## Summary

Completed FP16 tolerance coverage for the fixed-mask Triton kernels:

- `dW`: FP16 inputs, FP32 output, compared to FP32 PyTorch matmul.
- `dX_router`: FP16 inputs, FP32 output, compared to FP32 PyTorch matmul.
- `dH`: FP16 inputs, FP32 output, compared to FP32 PyTorch elementwise reference.

Tolerance: `rtol=2e-3`, `atol=2e-3`.

## Files Updated

- `tests/test_router_triton.py`

## Local Validation

```text
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py: pass
.venv/bin/python -m pytest tests/test_router_triton.py -q: 2 passed, 10 skipped in 2.50s
.venv/bin/python -m pytest tests -q: 51 passed, 11 skipped in 3.26s
```

## RunPod Validation

```text
CUDA/Triton probe: 62 passed in 3.95s
tests/test_router_triton.py: 12 passed in 3.07s
full suite: 62 passed in 3.76s
PASS: remote CUDA/Triton iteration completed.
```

Validated bundle:

```text
development/runner-bundles/triton-top2-iteration-20260614T072330Z.tar.gz
sha256: 0874060b4cb038a42357fcaeb0a1954a9bf4da8bd12dba66354fde2cb8b91a52
```

## Follow-Up

- `TASK-W7-003` is now unblocked for benchmark reporting.
- Selected-relaxation Triton work remains separate under `TASK-W6-001`.
