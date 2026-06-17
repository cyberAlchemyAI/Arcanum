# Convex Sparse Top-k JVP/Backward Feasibility Gate

Status: feasibility-pass-implementation-decision-needed
Date: 2026-06-12

## Task

`TASK-W2-003D-RG`: Run a bounded feasibility research gate for convex sparse
top-k PAV JVP/backward extraction.

## Verdict

Feasible for a narrow CPU/PyTorch custom-autograd parity oracle.

Not yet feasible to call Triton-ready or zero-allocation-ready.

The official sparse soft top-k implementation contains enough derivative
structure to extract a source-backed backward for the PAV mask path. The next
implementation task should be scoped to non-boundary fixtures and score-gradient
parity, not full kernel optimization.

## Primary Sources Checked

- Sander et al., "Fast, Differentiable and Sparse Top-k: a Convex Analysis
  Perspective", ICML 2023:
  `https://proceedings.mlr.press/v202/sander23a.html`
- Official Google Research `sparse_soft_topk` README:
  `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/README.md`
- Official Google Research top-k wrapper:
  `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/_src/topk.py`
- Official Google Research PAV implementation:
  `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/_src/isotonic_pav.py`
- Official Google Research tests:
  `https://raw.githubusercontent.com/google-research/google-research/master/sparse_soft_topk/tests/topk_test.py`

## Source Findings

The official PAV mask wrapper:

- sorts scores with a stopped-gradient permutation;
- builds a top-k weight vector;
- calls `isotonic_mask_pav`;
- maps the isotonic solution into a relaxed mask;
- unsorts the mask back to original order.

The official isotonic PAV path:

- uses `jax.custom_vjp`;
- stores `(s, p, sol)` as residuals;
- computes backward through a Numba callback;
- returns a gradient only for `s`, treating `w`, `l`, `p`, and
  `bisect_max_iter` as non-differentiated parameters.

For p=4/3, the conjugate exponent is:

```text
q = p / (p - 1) = 4
```

The relaxed mask in sorted order is:

```text
m = ((s - v) / l) ** 3
```

where `v` is the isotonic PAV solution.

The official VJP for the isotonic solution groups equal-solution PAV blocks and,
inside each block, weights the upstream vector by:

```text
diff_i = abs(v_i - s_i) ** (q - 2)
```

For p=4/3, that becomes:

```text
diff_i = abs(v_i - s_i) ** 2
```

## Implementation Route

The feasible narrow route is:

1. Implement a PyTorch `torch.autograd.Function` for the sorted PAV mask
   operator.
2. Reuse the existing forward extraction for p=4/3.
3. During forward, save:
   - sorted scores `s`;
   - isotonic solution `v`;
   - block partition inferred from equal contiguous values of `v`;
   - smoothing value `l`;
   - permutation needed to map gradients back to original score order.
4. During backward, compose:
   - direct derivative of `m = ((s - v) / l) ** 3`;
   - source-backed isotonic VJP for `v(s)`;
   - stopped-gradient sort/unsort mapping.
5. Validate only on non-boundary rows with no ties and stable support.

## Candidate Backward Contract

Let upstream gradient wrt sorted mask be `u`, and:

```text
alpha = 3 * (s - v) ** 2 / l ** 3
```

The mask derivative contributes:

```text
dL/ds = alpha * u - VJP_isotonic(alpha * u)
```

where `VJP_isotonic` is the official blockwise VJP for the isotonic PAV solution.
Then map `dL/ds` back through the stopped-gradient permutation.

This is an implementation contract to test, not yet an accepted theorem.

## Required Test Fixtures

Minimum tests for `TASK-W2-003D`:

- forward parity against `convex_sparse_topk_mask_rows`;
- score-gradient parity against finite differences for non-boundary rows;
- one official README fixture retained for forward behavior;
- a tie/support-boundary fixture marked skipped or explicitly documented;
- gradcheck for the selected router composition if numerical tolerances allow;
- no claim of gradient wrt `k`, `l`, `p`, or sort indices.

## Risks

- PAV block partition changes at boundaries; gradients there should not be
  overclaimed.
- Official implementation uses float32-oriented Numba/JAX callbacks; local
  PyTorch double gradcheck may need tolerance and fixture care.
- The stopped-gradient permutation is acceptable only away from ties.
- This does not establish a zero-allocation Triton strategy.

## Recommendation

Proceed with a narrow `TASK-W2-003D` implementation only if the next decision
accepts the added scope. The recommended implementation target is PyTorch
score-gradient parity for:

```text
convex_sparse_topk_mask_rows(scores, k=2, lambda_smooth=1e-2)
```

on non-boundary fixtures.

If schedule or novelty exploration matters more, defer the implementation and
resume `TASK-W3-001` CAP2-v0 forward reference with this feasibility result
recorded.
