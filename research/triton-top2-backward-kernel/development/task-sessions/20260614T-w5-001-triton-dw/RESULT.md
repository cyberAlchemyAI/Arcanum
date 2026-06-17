# Task Session Result - TASK-W5-001

Status: `pending-runpod-validation`

## Summary

Implemented a first Triton fixed-mask `dW` kernel for the narrow W5 baseline:

```text
dW = dZ^T @ X
```

The kernel takes already-computed `dZ` from the validated fixed-mask backward
graph and computes the router weight gradient on CUDA.

## Files Updated

- `reference/router_triton.py`
- `tests/test_router_triton.py`

## Local Validation

Local CPU-only validation passed with CUDA/Triton tests skipped:

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests -q
```

Result:

```text
49 passed, 4 skipped in 3.10s
```

Runner bundle:

```text
research/triton-top2-backward-kernel/development/runner-bundles/triton-top2-w5-kernel-20260614T-w5-001.tar.gz
```

## Required External Validation

Run on the RunPod pod:

```sh
python -m pytest tests/test_router_triton.py -q
python -m pytest tests -q
```

`TASK-W5-001` can only be synchronized to `pass` after those CUDA/Triton tests
pass on the pod.
