# Softmax Proof Feasibility Report

Status: `scoped-deferred`

## Target

The planned theorem was the finite softmax Jacobian identity:

```text
d p_i / d z_k = p_i * (indicator(i = k) - p_k)
```

for:

```text
p_i = exp(z_i) / sum_j exp(z_j)
```

## Feasibility Result

This proof should not be added as a small theorem in the current task session.
The local Mathlib package provides calculus infrastructure, but this paper
package does not yet define the finite-vector derivative model needed to state
the theorem cleanly.

The missing formal choices are:

- whether logits are represented as `Fin E -> ℝ`, `EuclideanSpace ℝ (Fin E)`,
  or another finite-dimensional normed-space representation;
- whether the theorem should be stated as scalar `HasDerivAt` along a coordinate
  perturbation, Fréchet derivative `HasFDerivAt`, or a Jacobian matrix theorem;
- how the positive denominator proof for `sum_j exp(z_j)` is packaged;
- how this theorem should connect back to the router objective without claiming
  the whole relaxed router is formally proved.

## Exact Blocker

The blocker is not missing Lean or Mathlib installation. The blocker is that a
rigorous softmax derivative theorem requires a larger calculus substrate than
the current bounded paper package has selected.

## Next Smallest Theorem

The next safe theorem should be a coordinate-direction theorem:

```text
softmaxCoord (z + h * basis_k) i
```

has derivative at `h = 0` equal to:

```text
softmaxCoord z i * (indicator(i = k) - softmaxCoord z k)
```

This avoids committing immediately to a full Jacobian matrix API while still
formalizing the useful derivative fact.

## Claim Boundary

This report is feasibility evidence only. It does not prove softmax calculus,
CAP2 calculus, or end-to-end relaxed-router differentiability.
