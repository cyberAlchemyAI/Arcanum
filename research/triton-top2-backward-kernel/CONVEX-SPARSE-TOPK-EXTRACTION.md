# Convex Sparse Top-k Extraction

Status: extracted-mask-operator
Date: 2026-06-12

## Scope

This artifact extracts the convex sparse differentiable top-k **mask** operator
needed for `TASK-W2-003A`.

It does not yet define the router composition rule. In other words, it extracts:

```text
M_relaxed = sparse_soft_topk_mask_pav(scores, k=2, l, p)
```

It does not decide whether the router should later use:

```text
A = M_relaxed
A = M_relaxed * softmax(scores)
A = normalize(M_relaxed * softmax(scores))
```

That choice remains a separate design gate.

## Source Contract

Primary source:

- Sander et al., "Fast, Differentiable and Sparse Top-k: a Convex Analysis
  Perspective", ICML 2023.
- Official implementation:
  `google-research/google-research/sparse_soft_topk`.

Selected function family:

```text
sparse_soft_topk_mask_pav(x, k, l=1e-1, p=4/3)
```

Selected local extraction:

```text
convex_sparse_topk_mask_rows(z, k=2, lambda_smooth=1e-2)
```

## Algorithm Reading

For each score row:

1. sort scores descending;
2. set `w = [1, 1, 0, ..., 0]` for `k=2`;
3. solve the p=4/3 isotonic PAV mask problem in sorted order;
4. map the isotonic solution back into a relaxed mask with:

```text
mask_sorted_i = ((score_sorted_i - isotonic_i) / lambda_smooth)^3
```

5. invert the sort permutation to return the mask in original score order.

## Boundary Policy

- Non-boundary rows should have exactly `k` positive entries.
- Non-selected entries are exactly zero in the extracted reference.
- As `lambda_smooth` becomes small, the mask approaches hard top-k on tested
  non-boundary rows.
- Tie/support-boundary behavior is not overclaimed. Tests should either avoid
  ties or document expected ambiguity.

## Implementation

Implemented in:

```text
reference/router_reference.py
```

Function:

```text
convex_sparse_topk_mask_rows
```

The implementation is standard-library only and is intended as an auditable CPU
reference for small fixtures, not as a performance implementation.

## Validation

Covered by:

```text
tests/test_router_reference.py
```

Current checks:

- matches the official README example shape for `[-5, -2, 3, 1]`, `k=2`,
  `lambda_smooth=1e-2`;
- exactly `k` positive entries for non-boundary rows;
- zero outside selected support;
- approaches hard top-k for small smoothing.

## Remaining Design Gate

The router composition decision for `TASK-W2-003B` selected options 1 and 3:

```text
A = M_relaxed
A = normalize(M_relaxed * softmax(scores))
```

Implemented functions:

```text
convex_topk_mask_direct_reference
convex_topk_normalized_masked_softmax_reference
```

The direct-mask variant is a pure sparse-top-k-mask router comparison. The
normalized masked-softmax variant keeps softmax probabilities for the auxiliary
term and normalizes selected combine weights.

## Remaining Backward Gate

This extraction still does not claim a source-backed PyTorch/custom-JVP backward
for the PAV mask. That must be handled before using this baseline as evidence
for a differentiable end-to-end backward implementation.

Current status:

```text
blocked-before-differentiable-parity
```

See `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md` for the explicit `TASK-W2-003C`
blocked report and the `TASK-W2-003D` unblock criteria.
