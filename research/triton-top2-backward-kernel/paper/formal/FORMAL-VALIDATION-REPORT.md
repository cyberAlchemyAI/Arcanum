# Formal Validation Report

Status: `complete`
Toolchain: Lean 4.30.0 / Lake 5.0.0
Mathlib: `v4.30.0`

## Scope

The formal package validates a narrow paper-facing boundary. It also proves a
Mathlib-backed real-valued theorem slice for the linear router map
`(X, W) -> X W^T` and a finite softmax coordinate derivative along one
coordinate perturbation line. It does not prove the Triton kernels, GPU memory
behavior, FP16 numerical equivalence, hard Top2 differentiability, a packaged
full softmax Jacobian theorem, or the full calculus of CAP2.

## Mechanized Files

| File | Purpose | Status |
| --- | --- | --- |
| `TritonTop2/RouterAlgebra.lean` | Encodes finite-index matrix/router algebra forms for logits, dW, and dX-router reductions using explicit reducer parameters. | proved by definitional equality |
| `TritonTop2/RealBackwardIdentities.lean` | Encodes real-valued finite-sum logits and proves dW/dX-router adjoint identities with Mathlib. | proved |
| `TritonTop2/FixedMaskBackward.lean` | Composes the real-valued router adjoint identities with a fixed mask/upstream logit gradient, proving exact fixed-mask dW and dX-router adjoint identities. | proved |
| `TritonTop2/SoftmaxCoordinate.lean` | Defines finite softmax coordinates and coordinate perturbation lines, then proves denominator positivity plus the full finite softmax coordinate derivative along a coordinate line. | proved |
| `TritonTop2/CAP2Definition.lean` | Freezes CAP2-v0 row-level definitions from the candidate/reference contract, including adjusted logits, pairwise soft rank, membership, gated weights, and fixed-load boundary lemmas. | proved by definition/boundary lemmas |
| `TritonTop2/CAP2FixedLoadScalar.lean` | Proves first fixed-load scalar slice for CAP2 adjusted logits under coordinate perturbation, while preserving fixed-load boundary status. | proved |
| `TritonTop2/FormalBoundary.lean` | Encodes claim-boundary statuses, including hard Top2 as a non-theorem. | proved by definitional equality |
| `TritonTop2/FixedLoadCAP2.lean` | Encodes fixed-load CAP2 boundary classification. | proved by definitional equality |
| `SOFTMAX-PROOF-FEASIBILITY.md` | Records why a finite softmax Jacobian proof is deferred until a finite-vector derivative model is selected. | scoped deferred |
| `SOFTMAX-COORDINATE-BLOCKER.md` | Historical blocker report for the coordinate derivative theorem; superseded by `softmaxCoord_coordLine_hasDerivAt`. | resolved |
| `CAP2-PROOF-FEASIBILITY.md` | Records why CAP2 derivative formalization is deferred until a canonical CAP2 mathematical definition is frozen. | scoped deferred |

## Proved Inside This Lean Slice

| Proof | Meaning |
| --- | --- |
| `logits_apply` | The encoded logits contraction expands to the expected finite-index reducer form. |
| `dWFromDZ_apply` | The encoded dW contraction expands to the expected finite-index reducer form. |
| `dXRouterFromDZ_apply` | The encoded router contribution to dX expands to the expected finite-index reducer form. |
| `dWReal_adjoint` | For real-valued finite matrices, the dW contraction is adjoint to the logits map in the W argument. |
| `dXRouterReal_adjoint` | For real-valued finite matrices, the router-side dX contraction is adjoint to the logits map in the X argument. |
| `fixedMaskDW_adjoint` | For fixed mask/upstream routing weights, the fixed-mask dW contraction is adjoint to the logits map in the W argument. |
| `fixedMaskDXRouter_adjoint` | For fixed mask/upstream routing weights, the fixed-mask dX-router contraction is adjoint to the logits map in the X argument. |
| `fixedMask_is_data_not_selection_gradient` | The fixed mask is represented as data multiplying upstream logit gradients, not as a differentiated hard-selection operation. |
| `softmaxDen_pos` | The finite softmax denominator is positive for nonempty expert index sets. |
| `softmaxDen_ne_zero` | The finite softmax denominator is nonzero under the same nonempty expert condition. |
| `coordLine_zero` | The coordinate perturbation line returns the original vector at perturbation zero. |
| `coordLine_hasDerivAt` | The coordinate perturbation line has derivative `basis k j` in coordinate `j`. |
| `exp_coordLine_hasDerivAt` | The numerator `Real.exp (coordLine z k h i)` has derivative `Real.exp (z i) * basis k i`. |
| `softmaxDen_coordLine_hasDerivAt` | The finite softmax denominator has derivative `Real.exp (z k)` along the coordinate perturbation line. |
| `softmaxCoord_coordLine_hasDerivAt_raw` | The quotient-rule derivative for a finite softmax coordinate is proved in raw quotient form. |
| `softmaxCoord_coordLine_hasDerivAt` | The finite softmax coordinate derivative is normalized to `softmaxCoord z i * (basis k i - softmaxCoord z k)`. |
| `cap2AdjustedLogit_fixed_load_data` | CAP2 adjusted logits are defined from raw logits and fixed load pressure. |
| `cap2Weight_uses_fixed_load_argument` | CAP2 weights are defined from gated weights and a fixed-load weight denominator. |
| `cap2AdjustedLogit_coordLine_self` | Under fixed load, perturbing the selected coordinate changes the adjusted logit by the perturbation amount. |
| `cap2AdjustedLogit_coordLine_of_ne` | Under fixed load, perturbing a different coordinate leaves this adjusted logit unchanged. |
| `cap2FixedLoad_no_dynamic_load_claim` | CAP2 fixed-load theorem slice preserves fixed-load boundary status. |
| `hardTop2Selection_is_not_a_formal_claim` | Hard Top2 differentiability is explicitly outside this formal claim. |
| `fixedLoad_is_fixed_data` | Fixed load is an assumption, not a differentiated dynamic decision. |
| `triton_memory_status_is_not_proved_in_lean` | GPU implementation behavior is not claimed as Lean-proved. |
| `fp16_numerics_are_deferred` | FP16 numeric error analysis remains deferred. |

## Deferred Obligations

| Obligation | Reason |
| --- | --- |
| Full softmax Jacobian proof | The coordinate derivative theorem now builds; a packaged full Jacobian theorem remains future work. |
| Full CAP2 derivative proof | CAP2 definitions and first fixed-load adjusted-logit slice now build; normalized gate/soft-rank calculus remains future work. |
| Dynamic load-gradient proof | Out of W6 scope. |
| Triton/CUDA memory proof | Requires a GPU/kernel semantics model, not present here. |
| FP16 error bound | Requires numerical analysis beyond this boundary slice. |

## Dependency Lock

`lake-manifest.json` records Mathlib at commit
`c5ea00351c28e24afc9f0f84379aa41082b1188f`, corresponding to input revision
`v4.30.0`, plus inherited transitive dependencies.

## Validation Command

```bash
cd <repo>/research/triton-top2-backward-kernel/paper/formal
lake build
```
