# Convex Sparse Top-k Fixtures

Status: active
Date: 2026-06-12

## Function Under Test

```text
convex_sparse_topk_mask_rows(z, k=2, lambda_smooth=1e-2)
```

## Fixture 1 - Official README Shape

Input:

```text
[-5.0, -2.0, 3.0, 1.0]
```

Expected qualitative behavior:

```text
[0.0, 0.0, approximately 0.99999714, approximately 0.99999714]
```

Purpose:

- checks alignment with the official `sparse_soft_topk_mask_pav` README example;
- checks the selected support is the top-2 score indices.

## Fixture 2 - Non-Boundary Support

Inputs:

```text
[4.0, 1.0, -2.0, 3.0]
[0.1, 2.0, 0.7, -1.0]
```

Expected behavior:

- exactly two positive entries;
- positive entries match hard top-2 support;
- all non-selected entries are exactly zero.

## Fixture 3 - Hard Top-k Limit

Input:

```text
[4.0, 1.0, -2.0, 3.0]
```

With:

```text
lambda_smooth = 1e-4
```

Expected behavior:

```text
approximately [1.0, 0.0, 0.0, 1.0]
```

## Boundary/Tie Policy

Avoid ties in pass/fail fixtures until a source-backed tie policy is added.
Boundary behavior is not used as evidence for novelty or correctness claims.

## Router Composition Fixtures

Selected compositions:

```text
A = M_relaxed
A = normalize(M_relaxed * softmax(Z))
```

Checks:

- direct-mask routing uses `A == M_relaxed`;
- direct-mask routing has exactly `k` positive entries on tested non-boundary
  rows;
- normalized masked-softmax routing has exactly `k` active support entries and
  `sum(A_t) == 1` per token;
- normalized masked-softmax routing preserves softmax probabilities for `pbar`
  and the auxiliary term.
