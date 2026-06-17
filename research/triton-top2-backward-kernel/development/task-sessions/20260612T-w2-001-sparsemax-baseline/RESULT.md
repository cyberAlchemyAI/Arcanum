# Task Session Result - TASK-W2-001 Sparsemax Baseline

- Task: `TASK-W2-001`
- Result: PASS-Sparsemax
- Date: 2026-06-12

## Summary

Added a sparsemax routing baseline in both standard-library and PyTorch
reference code. The baseline runs on the shared fixture and has tests for
simplex projection, exact zeros, and PyTorch parity.

Entmax is not implemented in this task-session; it remains a named follow-up
until the exact implementation formula/source is pinned.

## Files Updated

- `reference/router_reference.py`
- `reference/router_torch.py`
- `tests/test_router_reference.py`
- `tests/test_router_torch.py`
- `WORK-PACK.md`
- `TOWER.md`

## Validation

```text
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests -q
```

Result:

```text
26 passed, 1 skipped
```

```text
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

Result:

```text
OK (skipped=12)
```

## Synchronization

`TASK-W2-001` is marked `pass-sparsemax` in `WORK-PACK.md`.
`TASK-W2-002` is the next ready W2 baseline task.
