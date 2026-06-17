# Context Pack - TASK-W7-001

Task: `TASK-W7-001`
Scope: add zero-allocation checks for fixed-mask Triton W5 kernels.

## Controlling Sources

- `WORK-PACK.md`: W7 allocation checks depend on `TASK-W5-001`.
- `definitions.md`: zero allocation means no new persistent PyTorch tensors or device buffers in the backward hot path; outputs must be preallocated by the wrapper/caller.
- `implementation-notes.md`: allocation checks should use PyTorch CUDA memory stats around the backward wrapper.
- `reference/router_triton.py`: fixed-mask Triton kernels.
- `tests/test_router_triton.py`: CUDA-focused parity and allocation checks.

## Scope Boundary

This task validates the fixed-mask W5 kernel wrappers only:

- `fixed_mask_dw_triton`
- `fixed_mask_dx_router_triton`
- `fixed_mask_dh_triton`

It does not validate CAP2, selected relaxation kernels, fused full backward, or
performance.

## Implementation Decision

Add optional preallocated `out` buffers to each wrapper and test the hot path
after warm-up:

- output pointer is reused;
- `torch.cuda.memory_allocated()` is unchanged;
- `torch.cuda.max_memory_allocated()` does not exceed the pre-call value.

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
