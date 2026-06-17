# Task Session Result - TASK-W2-003A Convex Sparse Top-k Extraction

- Task: `TASK-W2-003A`
- Result: PASS
- Date: 2026-06-12

## Summary

Extracted a standard-library CPU reference for the official sparse soft top-k
PAV mask path with `p=4/3` and `k=2`.

The implementation is intentionally only the relaxed mask operator:

```text
convex_sparse_topk_mask_rows
```

The router composition rule is still blocked behind `TASK-W2-003B`.

## Files Updated

- `reference/router_reference.py`
- `tests/test_router_reference.py`
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`
- `CONVEX-SPARSE-TOPK-FIXTURES.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- `development/task-sessions/20260612T-w2-003a-convex-topk-extraction/`

## Validation

```text
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests/test_router_reference.py -q
```

Result:

```text
19 passed
```

## Gate Verdict

Pass for extraction. Blocked for router composition.

## Next Blocker

`TASK-W2-003B` must choose one composition rule:

- `A = M_relaxed`
- `A = M_relaxed * softmax(Z)`
- `A = normalize(M_relaxed * softmax(Z))`

Recommended first route: `A = M_relaxed * softmax(Z)`.
