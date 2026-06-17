# Context Pack - TASK-W7-002

Task: `TASK-W7-002`
Scope: add FP16 tolerance checks for fixed-mask Triton W5 kernels.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W7-002` depends on `TASK-W5-001`.
- `claim-ledger.md`: recommends FP32 accumulation for FP16 optimization.
- `reference/router_triton.py`: fixed-mask kernels emit FP32 outputs.
- `tests/test_router_triton.py`: CUDA parity and tolerance checks.

## Scope Boundary

This task validates FP16 inputs for:

- `fixed_mask_dw_triton`
- `fixed_mask_dx_router_triton`
- `fixed_mask_dh_triton`

The tolerance target is approximate FP16 input parity against FP32 PyTorch
reference calculations, with FP32 Triton outputs.

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
