# Convex Sparse Top-k PAV JVP/Backward Parity

Status: narrow-pytorch-parity-pass
Date: 2026-06-12

## Task

`TASK-W2-003D`: Extract source-backed PyTorch/custom-JVP parity for convex sparse
top-k PAV.

## Result

Implemented a narrow CPU/PyTorch custom-autograd oracle for the p=4/3 PAV sparse
soft top-k mask.

Covered:

- forward parity against `convex_sparse_topk_mask_rows`;
- source-backed score-gradient parity against finite differences on
  non-boundary rows;
- direct-mask router forward parity against the standard-library oracle.

Not covered:

- normalized masked-softmax router backward parity;
- support-boundary or tie-gradient claims;
- gradients with respect to `k`, `lambda_smooth`, `p`, or sort indices;
- Triton, GPU, zero-allocation, or FP16 kernel claims.

## Implemented API

```text
reference/router_torch.py
```

Functions:

```text
convex_sparse_topk_mask_torch(z, k=2, lambda_smooth=1e-2)
convex_topk_mask_direct_torch(x, w, h, f, ...)
```

The mask function uses a `torch.autograd.Function` whose forward path reuses the
local standard-library p=4/3 PAV extraction and whose backward path implements
the official blockwise isotonic VJP specialization for p=4/3.

## Backward Contract

For sorted scores `s`, PAV isotonic solution `v`, upstream sorted mask gradient
`u`, and smoothing `l`:

```text
mask = ((s - v) / l) ** 3
alpha = 3 * (s - v) ** 2 / l ** 3
dL/ds = alpha * u - VJP_isotonic(alpha * u)
```

`VJP_isotonic` groups contiguous equal-solution PAV blocks and uses the official
general-p VJP weighting:

```text
diff_i = abs(v_i - s_i) ** 2
```

The sort permutation is treated as stopped-gradient, matching the official
source path away from ties.

## Validation

Tests:

```text
tests/test_router_torch.py
```

Key checks:

- `test_convex_sparse_topk_mask_torch_matches_standard_library_oracle`
- `test_convex_sparse_topk_mask_score_gradient_matches_finite_difference`
- `test_convex_sparse_topk_mask_tie_gradient_boundary_is_documented`
- `test_convex_topk_mask_direct_torch_matches_standard_library_forward`

Validation commands:

```text
.venv/bin/python -m pytest tests/test_router_torch.py -q
.venv/bin/python -m pytest tests -q
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

## Boundary Policy

Use this oracle only on non-boundary rows for backward claims. If scores tie or
the support/partition changes under perturbation, tests should skip or document
the boundary instead of asserting a smooth derivative.

## Next Work

The next implementation route may proceed to `TASK-W3-001` CAP2-v0 reference.

If the normalized masked-softmax convex top-k composition becomes important for
backward comparison, add a separate task that composes the mask-level VJP with
softmax and normalization and validates whole-router gradients.
