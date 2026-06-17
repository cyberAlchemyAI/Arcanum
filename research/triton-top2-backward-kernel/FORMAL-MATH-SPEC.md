# Formal Math Spec - Proof Targets

This file defines a proof-shaped subset of the problem. It is intentionally
narrow. Anything outside this spec is residue, not something to hand-wave.

## V0 Assumptions

Let:

- `T` be the number of tokens.
- `E` be the number of experts.
- `D` be the feature dimension.
- `X : T x D` over real numbers.
- `W : E x D` over real numbers.
- `H : T x E x D` over real numbers, precomputed expert outputs.
- `Z_tj = sum_d X_td * W_jd`.
- `P_t = softmax(Z_t)` over experts.
- `M_tj in {0, 1}` is a fixed saved top-2 mask from forward.
- `A_tj = M_tj * P_tj`.
- `Y_td = sum_j A_tj * H_tjd`.
- `R_td = Y_td - X_td`.
- `L_rec = lambda_rec * sum_t sum_d R_td^2`.
- `Pbar_j = (1 / T) * sum_t P_tj`.
- `f_j` is fixed with respect to `P`.
- `L_aux = gamma * E * sum_j f_j * Pbar_j`.
- `L = L_rec + L_aux`.

This spec treats top-2 selection as already done. It does **not** prove gradients
through top-2 indices.

## Proof Obligations

### PO-001 - Softmax Row Derivative

For one row:

```text
P_j = exp(Z_j) / sum_k exp(Z_k)
```

Prove:

```text
dP_j / dZ_l = P_j * (delta_jl - P_l)
```

Then prove the reverse-mode form:

```text
dL/dZ_l = P_l * (dL/dP_l - sum_j P_j * dL/dP_j)
```

### PO-002 - Reconstruction Gradient Into A

Given:

```text
Y_td = sum_j A_tj * H_tjd
L_rec = lambda_rec * sum_t sum_d (Y_td - X_td)^2
```

Prove:

```text
dL_rec/dY_td = 2 * lambda_rec * (Y_td - X_td)
dL_rec/dA_tj = sum_d dL_rec/dY_td * H_tjd
dL_rec/dH_tjd = A_tj * dL_rec/dY_td
```

### PO-003 - Fixed-Mask Gradient Into P

Given:

```text
A_tj = M_tj * P_tj
```

and `M` fixed, prove:

```text
dL/dP_tj from reconstruction = M_tj * dL/dA_tj
```

### PO-004 - Auxiliary Gradient Into P

Given:

```text
L_aux = gamma * E * sum_j f_j * ((1/T) * sum_t P_tj)
```

and `f_j` fixed, prove:

```text
dL_aux/dP_tj = gamma * E * f_j / T
```

### PO-005 - Router Weight Gradient

Given:

```text
Z_tj = sum_d X_td * W_jd
```

prove:

```text
dL/dW_jd = sum_t dL/dZ_tj * X_td
```

### PO-006 - Router Input Gradient

For the part of `X` that flows through router logits:

```text
dL/dX_td from router = sum_j dL/dZ_tj * W_jd
```

This is not necessarily the full `dL/dX`, because `X` also appears directly in
`R = Y - X` and may flow through `H = FFN(X)` if FFN is inside scope.

## Explicit Non-Theorems

These must not be claimed from the V0 proof:

- gradient through hard top-2 index selection;
- correctness of a relaxed top-2 operator that has not been defined;
- FP16 numerical correctness;
- Triton memory safety or zero allocation;
- capacity constraint gradients unless a differentiable penalty/barrier is added;
- full expert FFN backward.

## Lean Suitability

Lean 4 is appropriate for PO-001 through PO-006 as real-number calculus or
finite-dimensional algebra, but the proof will be easier if staged:

1. prove finite-sum algebra identities;
2. prove softmax derivative separately;
3. compose reverse-mode equations;
4. keep top-2 as a fixed mask parameter.

Do not start by formalizing the whole challenge. Start with PO-005 or PO-004,
then PO-001 once the notation is stable.
