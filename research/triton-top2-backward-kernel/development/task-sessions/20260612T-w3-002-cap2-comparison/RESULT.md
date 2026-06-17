# Task Session Result - TASK-W3-002 CAP2 Comparison

- Task: `TASK-W3-002`
- Result: PASS
- Date: 2026-06-12

## Summary

Compared CAP2-v0 against fixed-mask Top2, normalized selected-pair, sparsemax,
normalized ReLU, convex top-k direct mask, and convex top-k normalized
masked-softmax on the shared fixture.

CAP2-v0 survives as a candidate for decision: it is differentiable under fixed
load and capacity-aware, but not exact 2-sparse and not novelty-proven.

## Files Updated

- `CAP2-PRIOR-ART-COMPARISON.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- `development/task-sessions/20260612T-w3-002-cap2-comparison/`

## Validation

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

Pass for comparison evidence.

Next task `TASK-W3-003` is a decision blocker: kill, promote, or defer CAP2-v0.
