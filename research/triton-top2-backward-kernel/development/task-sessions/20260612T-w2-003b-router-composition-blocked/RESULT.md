# Task Session Result - TASK-W2-003B Router Composition

- Task: `TASK-W2-003B`
- Result: BLOCK
- Date: 2026-06-12

## Summary

Stopped before implementation because the task requires a blocker-level router
composition decision.

The relaxed convex sparse top-k mask is already extracted as:

```text
M_relaxed = convex_sparse_topk_mask_rows(Z, k=2, lambda_smooth=...)
```

The open decision is how to use it in the router combine weights.

## Decision Options

1. `A = M_relaxed`
2. `A = M_relaxed * softmax(Z)`
3. `A = normalize(M_relaxed * softmax(Z))`

## Recommendation

Use:

```text
A = M_relaxed * softmax(Z)
```

This is the closest analog to the existing fixed-mask baseline, where the hard
mask is multiplied by softmax probabilities.

## Validation

No implementation mutation was made for this task.

Existing extraction validation remains:

```text
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests -q
```

Last known result:

```text
34 passed, 1 skipped
```
