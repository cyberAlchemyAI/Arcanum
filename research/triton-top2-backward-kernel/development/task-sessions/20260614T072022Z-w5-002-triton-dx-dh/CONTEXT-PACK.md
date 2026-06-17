# Context Pack - TASK-W5-002

Task: `TASK-W5-002`
Scope: add Triton fixed-mask `dX_router` and optional `dH` parity kernels.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W5-002` depends on `TASK-W5-001`, which now has RunPod pass evidence.
- `reference/router_reference.py`: `fixed_mask_manual_backward` defines:
  - `d_x_router[t, d] = sum_j d_z[t, j] * w[j, d]`
  - `d_h[t, j, d] = a[t, j] * d_y[t, d]`
- `reference/router_triton.py`: W5 Triton implementation surface.
- `tests/test_router_triton.py`: CUDA parity tests for fixed-mask kernels.

## Implementation Decision

Implement the task as two narrow fixed-mask kernels:

- `fixed_mask_dx_router_triton(d_z, w)` for the router-logit contribution `dZ @ W`.
- `fixed_mask_dh_triton(a, d_y)` for the optional expert-output gradient `A * dY`.

This does not claim full `dX` through the reconstruction residual and does not
claim fused full backward.

## Validation Surface

Local:

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests/test_router_triton.py -q
.venv/bin/python -m pytest tests -q
```

RunPod:

```sh
<cuda-runner-iteration-command>
```
