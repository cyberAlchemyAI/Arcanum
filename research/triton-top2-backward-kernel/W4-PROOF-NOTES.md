# W4 Proof Notes - Formal Math Stubs

Task: `TASK-W4-001`

Status: `proof-note-artifact`

This artifact converts the proof targets in `FORMAL-MATH-STUBS.md` into
Lean-shaped theorem stubs and manual proof notes. It is not a completed Lean
development. Its job is to make the formal boundary executable for later proof
work without overclaiming hard `Top2` differentiability, Triton correctness, or
FP16 behavior.

## Scope

The V0 graph is the fixed-mask graph from `FORMAL-MATH-SPEC.md`:

```text
Z_tj = sum_d X_td * W_jd
P_t = softmax(Z_t)
A_tj = M_tj * P_tj
Y_td = sum_j A_tj * H_tjd
R_td = Y_td - X_td
L_rec = lambda_rec * sum_t sum_d R_td^2
Pbar_j = (1 / T) * sum_t P_tj
L_aux = gamma * E * sum_j f_j * Pbar_j
```

Hard top-2 selection is already complete. `M` and `f` are fixed parameters for
these proof targets.

## Lean Module Shape

The first Lean pass should avoid a monolithic MoE formalization. A small module
can start with finite index types and real-valued functions:

```lean
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Data.Finset.Basic

noncomputable section

open scoped BigOperators

variable {T E D : Type}
variable [Fintype T] [Fintype E] [Fintype D]
variable [DecidableEq T] [DecidableEq E] [DecidableEq D]
```

For early proof progress, PO-004 and PO-005 can be encoded as finite-sum
linearity lemmas before the softmax derivative is formalized.

## PO-001 - Softmax Row Derivative

Lean-shaped theorem target:

```lean
def softmax (z : E -> Real) (j : E) : Real :=
  Real.exp (z j) / (Finset.univ.sum fun k : E => Real.exp (z k))

theorem softmax_row_derivative
    (z : E -> Real) (j l : E)
    (hden : (Finset.univ.sum fun k : E => Real.exp (z k)) != 0) :
    deriv (fun a : Real =>
      softmax (fun k => if k = l then a else z k) j) (z l)
      =
      softmax z j * (if j = l then 1 - softmax z l else 0 - softmax z l) := by
  sorry

theorem softmax_reverse_mode
    (z dP : E -> Real) (l : E)
    (hden : (Finset.univ.sum fun k : E => Real.exp (z k)) != 0) :
    (Finset.univ.sum fun j : E =>
      dP j * (softmax z j * (if j = l then 1 - softmax z l else 0 - softmax z l)))
      =
      softmax z l * (dP l - Finset.univ.sum fun j : E => softmax z j * dP j) := by
  sorry
```

Proof note:

1. Differentiate `exp(z_j) / S` with respect to coordinate `z_l`.
2. If `j = l`, numerator and denominator both depend on `z_l`.
3. If `j != l`, only the denominator depends on `z_l`.
4. Factor the result into `P_j * (delta_jl - P_l)`.
5. The reverse-mode identity follows by summing `dP_j * dP_j/dZ_l` over `j`
   and factoring out `P_l`.

## PO-002 - Reconstruction Gradient Into A

Lean-shaped theorem targets:

```lean
def y_of_a (A : E -> Real) (H : E -> D -> Real) (d : D) : Real :=
  Finset.univ.sum fun j : E => A j * H j d

def rec_loss_row (lambda_rec : Real) (X Y : D -> Real) : Real :=
  lambda_rec * (Finset.univ.sum fun d : D => (Y d - X d) ^ 2)

theorem rec_loss_dY
    (lambda_rec : Real) (X Y : D -> Real) (d : D) :
    deriv (fun y : Real =>
      rec_loss_row lambda_rec X (fun d' => if d' = d then y else Y d')) (Y d)
      =
      2 * lambda_rec * (Y d - X d) := by
  sorry

theorem rec_loss_dA
    (lambda_rec : Real) (X A : D -> Real) (Gate : E -> Real)
    (H : E -> D -> Real) (j : E) :
    -- Placeholder: after defining Y(A), prove dL/dA_j = sum_d dL/dY_d * H_jd.
    True := by
  trivial

theorem rec_loss_dH
    (lambda_rec : Real) (A : E -> Real) (H : E -> D -> Real) (j : E) (d : D) :
    -- Placeholder: after defining Y(H), prove dL/dH_jd = A_j * dL/dY_d.
    True := by
  trivial
```

Proof note:

`dL_rec/dY_td` is the derivative of a squared residual. The `A` and `H`
identities are direct finite-sum linearity results because `Y_td` is linear in
each `A_tj` and each `H_tjd` when the other terms are fixed.

## PO-003 - Fixed-Mask Gradient Into P

Lean-shaped theorem target:

```lean
theorem fixed_mask_dP
    (M dA : E -> Real) (j : E) :
    deriv (fun p : Real => dA j * (M j * p)) 0
      =
      M j * dA j := by
  sorry
```

Proof note:

With `A_j = M_j * P_j` and `M_j` fixed, the coordinate Jacobian is diagonal:
`dA_j/dP_j = M_j` and `dA_k/dP_j = 0` for `k != j`. The reverse accumulation is
therefore `dL/dP_j = M_j * dL/dA_j`.

## PO-004 - Auxiliary Gradient Into P

Lean-shaped theorem target:

```lean
def aux_loss
    (gamma e_count inv_t : Real) (f : E -> Real) (P : T -> E -> Real) : Real :=
  gamma * e_count *
    (Finset.univ.sum fun j : E =>
      f j * (inv_t * (Finset.univ.sum fun t : T => P t j)))

theorem aux_loss_dP
    (gamma e_count inv_t : Real) (f : E -> Real) (P : T -> E -> Real)
    (t0 : T) (j0 : E) :
    deriv (fun p : Real =>
      aux_loss gamma e_count inv_t f
        (fun t j => if t = t0 then if j = j0 then p else P t j else P t j))
      (P t0 j0)
      =
      gamma * e_count * f j0 * inv_t := by
  sorry
```

Proof note:

Only the `j0` expert summand depends on `P_t0j0`. Inside that summand, only one
term in `sum_t P_tj0` depends on the varied coordinate. Since `f` is fixed,
the derivative is the constant coefficient `gamma * E * f_j / T`. In Lean,
represent `1 / T` as a real scalar such as `inv_t` to avoid natural-number
coercion noise in the first pass.

## PO-005 - Router Weight Gradient

Lean-shaped theorem target:

```lean
def logits (X : T -> D -> Real) (W : E -> D -> Real) (t : T) (j : E) : Real :=
  Finset.univ.sum fun d : D => X t d * W j d

def linear_pullback_W
    (dZ : T -> E -> Real) (X : T -> D -> Real) (j : E) (d : D) : Real :=
  Finset.univ.sum fun t : T => dZ t j * X t d

theorem router_weight_gradient
    (dZ : T -> E -> Real) (X : T -> D -> Real) (j : E) (d : D) :
    deriv (fun wjd : Real =>
      Finset.univ.sum fun t : T =>
        dZ t j *
          (Finset.univ.sum fun d' : D =>
            X t d' * (if d' = d then wjd else 0)))
      0
      =
      linear_pullback_W dZ X j d := by
  sorry
```

Proof note:

The formal theorem should eventually vary `W j d` inside a full `W` function.
The algebra is simple: `Z_tj = sum_d X_td * W_jd` is linear in each `W_jd`, so
`dZ_tj/dW_jd = X_td`. Reverse accumulation over tokens gives
`dL/dW_jd = sum_t dL/dZ_tj * X_td`.

## PO-006 - Router Input Gradient

Lean-shaped theorem target:

```lean
def linear_pullback_X
    (dZ : T -> E -> Real) (W : E -> D -> Real) (t : T) (d : D) : Real :=
  Finset.univ.sum fun j : E => dZ t j * W j d

theorem router_input_gradient
    (dZ : T -> E -> Real) (W : E -> D -> Real) (t : T) (d : D) :
    -- Placeholder: vary X_t_d in sum_j dZ_tj * Z_tj and prove pullback.
    True := by
  trivial
```

Proof note:

The router-logit contribution to `dX_td` is the transpose companion to PO-005:
`dZ_tj/dX_td = W_jd`, so `dL/dX_td` from router logits is
`sum_j dL/dZ_tj * W_jd`. This is not the full `dX` for the model because the
residual term and expert network may also depend on `X`.

## Non-Claims Preserved

These stubs do not prove or imply:

- gradients through hard `Top2` index selection;
- CAP2 correctness or novelty;
- convex sparse top-k backward correctness;
- Triton kernel parity, memory safety, or zero-allocation behavior;
- FP16 numerical correctness;
- full expert FFN backward;
- differentiable capacity gradients when capacity is represented only as fixed
  hard load or a feasibility check.

## Next Proof Order

1. Turn PO-004 into a compiling Lean lemma using finite sums and scalar
   linearity.
2. Turn PO-005 into a compiling Lean lemma for one coordinate of `W`.
3. Add PO-006 as the transpose input-gradient lemma.
4. Formalize PO-002 finite-sum linearity for `A` and `H`.
5. Formalize PO-001 after notation and denominator assumptions are stable.
