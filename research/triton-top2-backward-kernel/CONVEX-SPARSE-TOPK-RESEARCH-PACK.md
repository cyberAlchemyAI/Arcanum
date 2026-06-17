# Convex Sparse Top-k Research Pack

Status: dispatch-ready
Date: 2026-06-12

## Purpose

Unblock `TASK-W2-003A` by pinning the source-backed extraction path for a convex
sparse differentiable top-k baseline.

## Primary Sources

1. Sander, Puigcerver, Djolonga, Peyre, Blondel, "Fast, Differentiable and
   Sparse Top-k: a Convex Analysis Perspective", ICML 2023.
   - PMLR: `https://proceedings.mlr.press/v202/sander23a.html`
   - arXiv PDF: `https://arxiv.org/pdf/2302.01425`
2. Official Google Research implementation:
   - Repository folder:
     `https://github.com/google-research/google-research/tree/master/sparse_soft_topk`
   - Core implementation:
     `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/_src/topk.py`
   - PAV implementation:
     `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/_src/isotonic_pav.py`
   - Tests:
     `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/tests/topk_test.py`

## Source-Backed Claims

- The paper frames top-k as discontinuous and hard to train through directly.
- The proposed family builds differentiable sparse top-k operators using
  p-norm regularization over a convex-analysis/isotonic-optimization reduction.
- The paper names two implementation paths:
  - PAV: exact solution path, implemented with Numba in the official code.
  - Dykstra: GPU/TPU-friendly approximate path, especially attractive for `p=2`.
- The official package exposes:
  - `sparse_soft_topk_mask_pav(x, k, l=..., p=...)`
  - `sparse_soft_topk_mag_pav(x, k, l=..., p=...)`
  - `sparse_soft_topk_mask_dykstra(x, k, l=..., num_iter=...)`
  - `sparse_soft_topk_mag_dykstra(x, k, l=..., num_iter=...)`
- For our router baseline, the relevant first extraction target is the mask
  operator, not magnitude top-k:

```text
sparse_soft_topk_mask_pav(scores, k=2, l=<regularization>, p=<regularizer>)
```

## Extraction Decision

Use the official PAV mask operator as the CPU reference extraction target:

```text
convex_sparse_topk_mask_reference(scores, k=2, lambda_smooth=1e-2, p=4/3)
```

Why:

- It is the exact path in the official implementation.
- It is source-backed and already tested upstream for sparsity and batched input.
- `p=4/3` is the official default for the PAV top-k function and is described as
  smooth/continuously differentiable in the README.
- It avoids conflating the approximate Dykstra path with the exact CPU baseline.

## What To Extract

The extraction task should produce:

1. a small standard-library or NumPy-free CPU reference if feasible;
2. otherwise, a documented PyTorch/JAX-backed adapter with the exact dependency
   boundary;
3. tests that check:
   - support size is `k` when inputs have no ties near the boundary;
   - non-selected entries are exactly zero;
   - selected entries are positive;
   - behavior approaches hard top-k as `lambda_smooth` becomes small;
   - boundary/tie behavior is documented rather than overclaimed.

## Do Not Claim Yet

- Do not call CAP2 novel until it is compared against this family.
- Do not claim we have a Triton-ready backward just because the CPU reference is
  extracted.
- Do not use Dykstra as an "exact" baseline; it is an approximation route.

## Open Technical Questions

1. Can we reasonably port PAV `p=4/3` to a tiny pure-Python reference for the
   tower, or should we vendor only behavior into tests and use PyTorch/JAX for
   comparison?
2. Should the router combine use the mask directly, `A = mask * softmax(Z)`, or
   use the relaxed mask as the routing weight itself? The prior-art operator is
   a mask/top-k relaxation; the router objective must choose the composition.
3. For zero-allocation Triton, should the final candidate use PAV-style exactness
   or Dykstra-style GPU friendliness?

## Next Route

Use `convex-sparse-topk-extraction-20260612.dispatch.json` to run a governed
extraction task-session for `TASK-W2-003A`.
