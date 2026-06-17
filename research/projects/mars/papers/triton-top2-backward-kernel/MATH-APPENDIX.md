# Math Appendix: Relaxed Top2 Backward Contract

Status: `complete`

This appendix explains the math contract behind the paper's "exact backward"
language. The short version is:

- hard `Top2` selection is not differentiated;
- a fixed mask or continuous relaxation is selected as the differentiable
  surrogate graph;
- the backward pass is exact inside that selected graph;
- the current Lean slice proves router-linear-map adjoint identities, fixed-mask
  adjoint identities, a finite softmax coordinate derivative, and first
  fixed-load CAP2 boundary lemmas, not the full Triton implementation or the
  full relaxation calculus.

## Scope Box

This appendix proves or supports:

- the notation bridge from `Z = X W^T` to router-logit backward contractions;
- the fixed-mask versus continuous-relaxation reading of "exact backward";
- the Lean-backed theorem map for router adjoints, fixed-mask adjoints, finite
  softmax coordinate derivative, and first fixed-load CAP2 boundary lemmas.

This appendix does not prove:

- differentiability of hard `Top2` selection;
- a packaged full softmax Jacobian or full softmax VJP theorem;
- full CAP2 calculus or dynamic-load gradients;
- Triton/CUDA memory behavior;
- FP16 numerical equivalence.

## Symbols

Let:

- `X` be the input matrix with token rows and feature columns;
- `W` be the router weight matrix with expert rows and feature columns;
- `Z = X W^T` be the router-logit matrix;
- `P = sigma(Z)` be continuous routing probabilities, where `sigma` is the
  chosen smooth probability map such as softmax;
- `A` be the selected routing weights used by the surrogate graph.

For hard `Top2`, `A` would be produced by a discrete selection step. That step
can jump when the ordering of expert scores changes, so it is not a smooth
function of `Z`. This package therefore does not claim a gradient through hard
`Top2` selection.

The implemented and paper-facing contract is narrower. Once a fixed mask or
continuous relaxation is chosen, `A` is either treated as fixed data or as part
of a smooth surrogate graph. The backward pass is exact for that graph.

## Router Logits

For token `t`, expert `e`, and feature `d`, the router logits are:

```text
Z[t, e] = sum_d X[t, d] * W[e, d]
```

In matrix form:

```text
Z = X W^T
```

The Lean definition `logitsReal` in
`formal/TritonTop2/RealBackwardIdentities.lean` encodes this finite sum over
real-valued matrices.

## Upstream Gradient Through Logits

Let `dZ` be the upstream gradient arriving at the router logits. This appendix
does not need to decide where `dZ` came from. In the full model, it can include
terms from the routing mixture, the FFN branch, and load-balancing terms inside
the chosen surrogate graph.

Once `dZ` is known, the router-linear-map backward identities are:

```text
dW[e, d] = sum_t dZ[t, e] * X[t, d]
```

and:

```text
dX_router[t, d] = sum_e dZ[t, e] * W[e, d]
```

In matrix form:

```text
dW = dZ^T X
dX_router = dZ W
```

The Lean definitions `dWReal` and `dXRouterReal` encode these contractions.

## What Lean Proves Here

The theorem `dWReal_adjoint` proves that the `dW` contraction has the expected
inner-product action for the `W` argument of the linear map `Z = X W^T`.

The theorem `dXRouterReal_adjoint` proves the matching identity for the
router-side contribution to `X`.

These are algebraic adjoint identities over finite real matrices. They support
the paper's router-backward explanation, but they do not prove:

- differentiability of hard `Top2`;
- a packaged full softmax Jacobian or full softmax VJP theorem;
- the full derivative of CAP2, including normalized gate and soft-rank calculus;
- Triton/CUDA memory behavior;
- FP16 numerical equivalence.

## Theorem-To-Claim Map

This table is the paper-facing bridge from Lean theorem names to claims. Each
row also states what the theorem must not be used to claim.

| Lean theorem or definition group | Supports | Evidence ID | Does not support |
| --- | --- | --- | --- |
| `dWReal_adjoint`, `dXRouterReal_adjoint` in `RealBackwardIdentities.lean` | The real-valued router-linear-map adjoint identities for `dW = dZ^T X` and `dX_router = dZ W`. | `EV-FORMAL-002` | Softmax/CAP2 calculus, Triton memory behavior, or FP16 numerical equivalence. |
| `fixedMaskDW_adjoint`, `fixedMaskDXRouter_adjoint`, `fixedMask_is_data_not_selection_gradient` in `FixedMaskBackward.lean` | Exact fixed-mask backward identities once the mask and upstream routing weights are fixed data. | `EV-FORMAL-003` | Any gradient through hard `Top2` selection or a claim that fixed-mask evidence covers dynamic mask changes. |
| `softmaxDen_pos`, `softmaxDen_ne_zero`, `softmaxCoord_coordLine_hasDerivAt` in `SoftmaxCoordinate.lean` | Finite softmax denominator safety and the coordinate derivative `softmax_i * (basis_k_i - softmax_k)` along one coordinate perturbation line. | `EV-FORMAL-006`, `EV-FORMAL-010` | Hard `Top2` differentiability or a packaged full softmax Jacobian/VJP theorem. |
| CAP2-v0 definitions and boundary lemmas in `CAP2Definition.lean` | Canonical row-level CAP2-v0 objects and fixed-load boundary status. | `EV-FORMAL-008` | CAP2 novelty, exact 2-sparsity, a full CAP2 derivative, or dynamic-load gradients. |
| `cap2AdjustedLogit_coordLine_self`, `cap2AdjustedLogit_coordLine_of_ne` in `CAP2FixedLoadScalar.lean` | First fixed-load adjusted-logit coordinate perturbation slice for CAP2. | `EV-FORMAL-009` | Normalized gate calculus, soft-rank calculus, full CAP2 calculus, or dynamic-load behavior. |
| `hardTop2Selection_is_not_a_formal_claim`, `cap2FixedLoad_no_dynamic_load_claim`, `fixedLoad_is_fixed_data`, `triton_memory_status_is_not_proved_in_lean`, `fp16_numerics_are_deferred` | Formal boundaries that keep hard selection, dynamic load, GPU memory behavior, and FP16 numeric proof outside the Lean claim. | `EV-FORMAL-001`, `EV-FORMAL-008`, `EV-FORMAL-009` | Any implementation, performance, allocation, or numeric accuracy claim by itself. |

## Fixed Mask Versus Continuous Relaxation

There are two safe ways to read the backward contract in this package.

The fixed-mask path says: the selected experts are already known, so the mask is
data. The backward pass differentiates the smooth operations downstream of that
mask, not the act of selecting the mask.

The continuous-relaxation path says: hard selection is replaced by a smooth
surrogate. The backward pass differentiates that surrogate. In this package,
CAP2-v0 is used only inside its fixed-load validation boundary.

Both readings avoid the same mistake: they do not pretend that hard `Top2`
became differentiable.

## Relation To The Challenge Objective

The challenge expression contains:

```text
||X - Top2(sigma(X W^T)) * FFN(X)||^2
```

plus a load-balancing term. The exact backward implementation must therefore be
understood relative to the selected routing contract:

- if the mask is fixed, the backward pass is exact for that fixed-mask graph;
- if a smooth relaxation is selected, the backward pass is exact for that
  relaxation graph;
- if hard `Top2` itself is used as a discrete selection function, this package
  does not claim a derivative through that selection.

This is the central boundary that keeps the paper's claim rigorous.
