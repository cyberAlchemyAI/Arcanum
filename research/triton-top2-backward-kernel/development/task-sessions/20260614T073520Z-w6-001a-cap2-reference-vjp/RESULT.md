# Task Session Result - TASK-W6-001A

Result: `pass-local`

## Summary

Implemented `cap2_manual_backward` as the exact manual VJP for the CAP2-v0
differentiable graph with fixed load. The helper exposes forward intermediates
and backward outputs needed by later Triton parity work, including `d_z`,
`d_w`, `d_x_router`, and `d_h`.

## Files Updated

- `reference/router_torch.py`
- `tests/test_router_torch.py`
- `development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/WORK-PACK-W6-CAP2.md`
- `development/task-sessions/20260614T073520Z-w6-001a-cap2-reference-vjp/`

## Validation

```sh
.venv/bin/python -m py_compile reference/router_torch.py tests/test_router_torch.py
```

Pass.

```sh
.venv/bin/python -m pytest tests/test_router_torch.py -q
```

Pass: `24 passed in 5.10s`.

```sh
.venv/bin/python -m pytest tests -q
```

Pass: `54 passed, 11 skipped in 3.34s`.

## Acceptance

- Manual CAP2 `dW` and `dH` match PyTorch autograd.
- Manual CAP2 `dZ` matches PyTorch autograd on a logits leaf.
- Manual CAP2 `dW` matches central finite differences.
- Later Triton CAP2 work remains gated behind this reference.

## Follow-Up

Next ready task: `TASK-W6-001B`, CAP2 Triton row-local backward for `dZ`,
`dX_router`, and `dH`, validated on RunPod.
