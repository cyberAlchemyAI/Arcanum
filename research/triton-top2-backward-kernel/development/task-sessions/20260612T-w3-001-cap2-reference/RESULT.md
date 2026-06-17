# Task Session Result - TASK-W3-001 CAP2-v0 Reference

- Task: `TASK-W3-001`
- Result: PASS
- Date: 2026-06-12

## Summary

Implemented CAP2-v0 in the standard-library and PyTorch references.

The reference covers capacity-adjusted logits, pairwise soft rank, soft top-2
membership, normalized gated softmax weights, and fixed-load PyTorch gradcheck.

## Files Updated

- `reference/router_reference.py`
- `reference/router_torch.py`
- `tests/test_router_reference.py`
- `tests/test_router_torch.py`
- `CAP2-REFERENCE.md`
- `CAP2-CANDIDATE-SPEC.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- `development/task-sessions/20260612T-w3-001-cap2-reference/`

## Validation

```text
.venv/bin/python -m pytest tests/test_router_reference.py tests/test_router_torch.py -q
```

Result:

```text
46 passed
```

```text
.venv/bin/python -m pytest tests -q
```

Result:

```text
48 passed, 1 skipped
```

```text
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

Result:

```text
OK (skipped=22)
```

## Gate Verdict

Pass for CAP2-v0 reference implementation.

The next ready task is `TASK-W3-002`: compare CAP2-v0 against prior-art
baselines.
