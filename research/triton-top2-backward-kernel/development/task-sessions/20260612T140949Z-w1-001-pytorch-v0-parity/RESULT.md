# Task Session Result - TASK-W1-001 PyTorch V0 Parity

- Task: `TASK-W1-001`
- SWU: `SWU-W1-001`
- Result: PASS
- Date: 2026-06-12

## Summary

Added a PyTorch V0 fixed-mask reference that mirrors the standard-library
oracle. The implementation uses differentiable PyTorch operations for logits,
softmax, masked probabilities, expert combination, reconstruction loss, and the
auxiliary load-balancing term. The saved Top2 mask remains fixed input data.

## Files Updated

- `reference/router_torch.py`
- `tests/test_router_torch.py`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`

## Validation

```text
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests -q
```

Result:

```text
17 passed, 1 skipped
```

```text
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

Result:

```text
OK (skipped=7)
```

The tower-local venv exercises the PyTorch checks. The system Python unittest
path skips PyTorch tests when torch is unavailable, preserving the lightweight
standard-library validation path.

## Gate Verdict

- Dependency gate: pass.
- Semantic gate: pass; no hard Top2 differentiability claim was introduced.
- Triton gate: not applicable for W1.

## Synchronization

`TASK-W1-001` and `SWU-W1-001` are marked pass in `WORK-PACK.md`.
`TASK-W1-002` is now the next W1 task.
