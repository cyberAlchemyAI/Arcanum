# Task Session Result - TASK-W6-001C

Result: `pass-runpod`

## Summary

Extended `cap2_row_backward_triton` to return `d_w` by feeding the CAP2 Triton
`d_z` into the existing validated `fixed_mask_dw_triton` reduction. Added CAP2
`d_w` assertions and output-buffer reuse coverage to the RunPod-gated Triton
tests.

## Validation

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
```

Pass.

```sh
.venv/bin/python -m pytest tests/test_router_triton.py -q
```

Local pass with CUDA skipped: `2 passed, 13 skipped`.

```sh
.venv/bin/python -m pytest tests -q
```

Local pass with CUDA skipped: `54 passed, 14 skipped`.

```sh
<cuda-runner-iteration-command>
```

RunPod pass:

- focused Triton tests: `15 passed in 3.04s`;
- full test suite: `68 passed in 3.81s`.

## Follow-Up

Next ready task: `TASK-W6-001D`, close the CAP2 W6 parity contract and unblock
or reroute benchmark scope.
