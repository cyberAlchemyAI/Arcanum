# Task Session Result - TASK-W1-002 Gradcheck Parity

- Task: `TASK-W1-002`
- Result: PASS
- Date: 2026-06-12

## Summary

Added PyTorch gradcheck coverage for the fixed-mask graph with respect to `W`
and `H`, and added direct `dW` parity against the standard-library
finite-difference oracle.

## Files Updated

- `tests/test_router_torch.py`
- `WORK-PACK.md`

## Validation

```text
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests -q
```

Result:

```text
19 passed, 1 skipped
```

```text
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

Result:

```text
OK (skipped=9)
```

## Gate Verdict

Pass. The checked graph is the continuous fixed-mask graph; hard Top2 selection
is still outside the differentiable claim surface.

## Synchronization

`TASK-W1-002` and `SWU-W1-002` are marked pass in `WORK-PACK.md`.
`TASK-W1-003` is now the next W1 task.
