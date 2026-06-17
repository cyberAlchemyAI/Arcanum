# Task Session Result - TASK-W6-001B

Result: `pass-runpod`

## Summary

Implemented a CAP2 row-local Triton backward wrapper,
`cap2_row_backward_triton`, that returns `d_z`, `d_x_router`, and `d_h`.
The row kernel computes CAP2 forward intermediates, reconstruction VJP,
softmax VJP, pairwise-rank VJP, and `dH`; the wrapper reuses the existing
validated Triton `dZ @ W` kernel for `dX_router`.

## Validation

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
```

Pass.

```sh
.venv/bin/python -m pytest tests/test_router_triton.py -q
```

Local pass with CUDA skipped: `2 passed, 12 skipped`.

```sh
.venv/bin/python -m pytest tests -q
```

Local pass with CUDA skipped: `54 passed, 13 skipped`.

```sh
<cuda-runner-iteration-command>
```

RunPod pass:

- focused Triton tests: `14 passed in 3.29s`;
- full test suite: `67 passed in 3.88s`.

## Follow-Up

Next ready task: `TASK-W6-001C`, wire CAP2 `d_z` into the Triton `dW`
reduction and validate `d_w`.
