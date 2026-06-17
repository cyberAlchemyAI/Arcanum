# Formal Math Stubs

Status: `proof-note-artifact-linked`

These are proof stubs derived from `FORMAL-MATH-SPEC.md`. They are deliberately
not full Lean proofs yet. Their purpose is to pin the theorem targets before
implementation.

W4 artifact: `W4-PROOF-NOTES.md` converts these proof targets into Lean-shaped
theorem stubs plus manual proof notes. The artifact preserves the fixed-mask
boundary and does not claim hard `Top2` differentiability.

## PO-001 - Softmax Row Derivative

Statement:

```text
P_j = exp(Z_j) / sum_k exp(Z_k)
dP_j / dZ_l = P_j * (delta_jl - P_l)
```

Reverse-mode target:

```text
dL/dZ_l = P_l * (dL/dP_l - sum_j P_j * dL/dP_j)
```

Status: `Lean-shaped theorem stub and proof note in W4-PROOF-NOTES.md`

## PO-002 - Reconstruction Gradient Into A

Statement:

```text
dL_rec/dY_td = 2 * lambda_rec * (Y_td - X_td)
dL_rec/dA_tj = sum_d dL_rec/dY_td * H_tjd
dL_rec/dH_tjd = A_tj * dL_rec/dY_td
```

Status: `Lean-shaped theorem stub and proof note in W4-PROOF-NOTES.md`

## PO-003 - Fixed-Mask Gradient Into P

Statement:

```text
A_tj = M_tj * P_tj
dL/dP_tj = M_tj * dL/dA_tj
```

Status: `Lean-shaped theorem stub and proof note in W4-PROOF-NOTES.md`

## PO-004 - Auxiliary Gradient Into P

Statement:

```text
L_aux = gamma * E * sum_j f_j * ((1/T) * sum_t P_tj)
dL_aux/dP_tj = gamma * E * f_j / T
```

Status: `Lean-shaped theorem stub and proof note in W4-PROOF-NOTES.md; recommended first formal proof target`

## PO-005 - Router Weight Gradient

Statement:

```text
Z_tj = sum_d X_td * W_jd
dL/dW_jd = sum_t dL/dZ_tj * X_td
```

Status: `validated numerically in standard-library reference harness; Lean-shaped theorem stub and proof note in W4-PROOF-NOTES.md; recommended first formal proof target`

## PO-006 - Router Input Gradient

Statement:

```text
dL/dX_td from router = sum_j dL/dZ_tj * W_jd
```

Status: `Lean-shaped theorem stub and proof note in W4-PROOF-NOTES.md`

## Explicit Non-Theorems

Do not encode or claim:

- gradient through hard Top2 mask selection;
- CAP2 correctness before CAP2 exists;
- FP16 correctness;
- Triton allocation or memory behavior;
- full FFN backward.
