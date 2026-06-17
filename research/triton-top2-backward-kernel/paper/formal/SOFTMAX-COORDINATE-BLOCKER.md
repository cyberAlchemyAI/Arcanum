# Softmax Coordinate Derivative Blocker

Status: `resolved`

Resolution: `softmaxCoord_coordLine_hasDerivAt` now builds in
`TritonTop2/SoftmaxCoordinate.lean`.

## Built In This Pass

`TritonTop2/SoftmaxCoordinate.lean` now builds with:

- `softmaxDen`
- `softmaxCoord`
- `basis`
- `coordLine`
- `basis_self`
- `basis_of_ne`
- `coordLine_zero`
- `coordLine_self`
- `coordLine_of_ne`
- `softmaxDen_pos`
- `softmaxDen_ne_zero`
- `softmaxCoord_def`

## Theorem Attempted

The intended next theorem remains:

```text
d/dh softmaxCoord (coordLine z k h) i at h = 0
  = softmaxCoord z i * (indicator(i = k) - softmaxCoord z k)
```

## Original Blocker

The package now has the finite softmax definitions and positivity theorem, but
the coordinate derivative theorem needs a dedicated Mathlib calculus slice:

- a statement form using `HasDerivAt` or `deriv`;
- derivative lemmas for `fun h => Real.exp (coordLine z k h i)`;
- derivative of the finite sum denominator along `coordLine`;
- quotient derivative with a nonzero denominator proof;
- simplification back to the standard softmax expression.

This was split into theorem tasks and resolved in the softmax coordinate
derivative proof plan.

## Resolved Theorem Chain

- `coordLine_hasDerivAt`
- `exp_coordLine_hasDerivAt`
- `softmaxDen_coordLine_hasDerivAt`
- `softmaxCoord_coordLine_hasDerivAt_raw`
- `softmaxCoord_coordLine_hasDerivAt`

The originally requested denominator theorem now builds:

```text
HasDerivAt
  (fun h => softmaxDen (coordLine z k h))
  (Real.exp (z k))
  0
```

## Claim Boundary

The resolved theorem proves a finite smooth-softmax coordinate derivative along
a coordinate perturbation line. It does not prove hard `Top2` differentiability,
Triton/CUDA correctness, FP16 numeric behavior, or a packaged full softmax
Jacobian theorem.
