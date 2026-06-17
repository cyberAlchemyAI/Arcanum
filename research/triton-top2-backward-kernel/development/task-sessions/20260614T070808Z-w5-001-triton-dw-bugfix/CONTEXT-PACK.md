# Context Pack - TASK-W5-001 Bug-Fix Continuation

Task: `TASK-W5-001`
SWU: `SWU-W5-001`
Scope: fix the first RunPod failure for the Triton fixed-mask `dW` kernel.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W5-001` is the active W5 task; downstream W5/W6/W7 work depends on it.
- `development/invoke-runs/20260614T070302Z-refresh-w5-triton-dw-bug/REFRESH-REPORT.md`: opens the RunPod bug-fix route.
- `redacted local evidence attachment`: RunPod evidence showing three Triton `dW` failures.
- `reference/router_triton.py`: target Triton kernel.
- `tests/test_router_triton.py`: CUDA/Triton parity tests and local launch-shape guard.
- `<cuda-runner-iteration-command>`: remote iteration harness.

## Failure Summary

RunPod validation failed after the first W5 implementation:

- `tl.dot` compilation failed when logical/requested tile sizes produced physical shapes below `M/N/K >= 16`.
- The tiny fixture exceeded the strict FP32 tolerance, consistent with default dot precision using a less exact path.

## Constraints

- Keep the implementation scoped to the fixed-mask `dW = dZ^T @ X` baseline.
- Do not claim fused backward, zero allocation, final FP16 policy, or performance.
- Do not mark `TASK-W5-001` complete without RunPod CUDA validation.
- Preserve small logical shape coverage; the wrapper may use larger physical tiles internally.

## Implementation Decision

Use masked physical tiles that satisfy Triton's `tl.dot` lower bounds:

- Round requested `block_e`, `block_d`, and `block_t` to powers of two with minimum `16`.
- Keep masks on loads and stores so only logical `[E, D]` output is written.
- Use `input_precision="ieee"` for `tl.dot` to make FP32 parity stricter and avoid TF32 drift on the fixture.

## Validation Surface

Local:

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests/test_router_triton.py -q
.venv/bin/python -m pytest tests -q
```

External:

```sh
<cuda-runner-iteration-command>
```

The pod run must pass:

```sh
/usr/local/bin/python -m pytest tests/test_router_triton.py -q
/usr/local/bin/python -m pytest tests -q
```
