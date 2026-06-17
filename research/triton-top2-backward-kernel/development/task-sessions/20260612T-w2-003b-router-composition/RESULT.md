# Task Session Result - TASK-W2-003B Router Composition

- Task: `TASK-W2-003B`
- Result: PASS
- Date: 2026-06-12

## Summary

Resolved the router-composition decision with the user's selection:

```text
1 AND 3
```

Implemented two standard-library convex sparse top-k router baselines:

- `convex_topk_mask_direct_reference`
- `convex_topk_normalized_masked_softmax_reference`

Option 2, `A = M_relaxed * softmax(Z)`, was not implemented in this task.

## Files Updated

- `reference/router_reference.py`
- `tests/test_router_reference.py`
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`
- `CONVEX-SPARSE-TOPK-FIXTURES.md`
- `WORK-PACK.md`

## Validation

```text
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests/test_router_reference.py -q
```

Result:

```text
22 passed
```

```text
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

Result:

```text
OK (skipped=14)
```

## Gate Verdict

Pass for standard-library forward baselines.

The differentiable/JVP-backed PAV mask parity remains a follow-up and is tracked
as `TASK-W2-003C`.
