# Task Session Result - TASK-W5-002

Status: `pass-runpod`

## Summary

Added Triton kernels for the remaining fixed-mask W5 baseline gradients:

- `fixed_mask_dx_router_triton`: computes `dX_router = dZ @ W`.
- `fixed_mask_dh_triton`: computes `dH[t, e, d] = A[t, e] * dY[t, d]`.

The implementation preserves the same non-claims as W5-001: this is not fused
full backward, not zero-allocation, and not a selected-relaxation kernel.

## Files Updated

- `reference/router_triton.py`
- `tests/test_router_triton.py`

## Local Validation

```text
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py: pass
.venv/bin/python -m pytest tests/test_router_triton.py -q: 2 passed, 7 skipped in 2.33s
.venv/bin/python -m pytest tests -q: 51 passed, 8 skipped in 3.14s
```

## RunPod Validation

Command:

```sh
<cuda-runner-iteration-command>
```

Result:

```text
CUDA/Triton probe: 59 passed in 4.25s
tests/test_router_triton.py: 9 passed in 3.05s
full suite: 59 passed in 3.74s
PASS: remote CUDA/Triton iteration completed.
```

Validated bundle:

```text
development/runner-bundles/triton-top2-iteration-20260614T071942Z.tar.gz
sha256: 7bd5f3320bf88c2ba810ec2b1f8f4fdfd95843001a69d2a733e6b1fb5a81fb4a
```

## Follow-Up

- `TASK-W6-001`, `TASK-W7-001`, and `TASK-W7-002` remain unblocked by W5.
- `TASK-W7-003` still depends on W7 allocation and FP16 checks.
