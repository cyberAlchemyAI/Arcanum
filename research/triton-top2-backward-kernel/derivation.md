# Derivation Notes

This derivation is a research baseline, not an implementation contract.

## Baseline Graph

Assume:

```text
Z = X W^T
P = softmax(Z, dim=experts)
M = top2_mask(P)                 # hard mask, constant for fixed-mask backward
A = M * P                        # or normalized over selected experts; see residue
H = FFN(X)                       # treated as precomputed expert output here
Y_t = sum_j A_tj H_tj
L_rec = lambda_rec * sum_t ||Y_t - X_t||^2
L_aux = gamma * E * sum_j f_j * Pbar_j
Pbar_j = mean_t P_tj
```

The prompt writes `W ||...||^2`; this tower names it `lambda_rec` until clarified.

## Reconstruction Gradient

Let:

```text
R_t = Y_t - X_t
dY_t = 2 * lambda_rec * R_t
```

If `H` is an input to this backward surface:

```text
dA_tj = dot(dY_t, H_tj)
dH_tj = A_tj * dY_t
```

If `A = M * P` with fixed `M`:

```text
dP_from_rec_tj = M_tj * dA_tj
```

If selected gates are renormalized:

```text
A_tj = M_tj * P_tj / S_t
S_t = sum_k M_tk P_tk
```

then:

```text
dP_tj += M_tj * (dA_tj * S_t - sum_k M_tk dA_tk P_tk) / S_t^2
```

## Auxiliary Loss Gradient

For the Switch-like term:

```text
L_aux = gamma * E * sum_j f_j * Pbar_j
Pbar_j = (1 / T) * sum_t P_tj
```

If `f_j` is hard or fixed:

```text
dP_from_aux_tj = gamma * E * f_j / T
```

If `f_j` is a differentiable relaxed load, there is an additional term:

```text
gamma * E * sum_j Pbar_j * d(f_j)/dP_tk
```

That term cannot be completed without the relaxation definition.

## Softmax Backward

For each token row:

```text
dZ_tj = P_tj * (dP_tj - sum_k dP_tk * P_tk)
```

Then:

```text
dW_jd = sum_t dZ_tj * X_td
dX_router_td = sum_j dZ_tj * W_jd
```

If the loss also differentiates through `H = FFN(X)`, add the expert FFN backward contribution to `dX`.

## Capacity Constraint

The stated constraint:

```text
max_j(f_j) <= 2.1 / E
```

does not by itself define a differentiable loss. Implementation choices:

1. Check and fail/flag outside the kernel.
2. Use forward routing that enforces the capacity.
3. Add a differentiable penalty such as `rho * sum_j relu(f_j - 2.1/E)^2`.
4. Add a barrier term for feasible relaxed `f_j`.

Only choices 3 or 4 contribute gradients.

## Backward Kernel Core

The core router backward kernel computes:

```text
for token block T_b and expert block E_b:
  recompute or load Z/P/top2 state
  compute dP from reconstruction and auxiliary term
  apply row softmax backward to get dZ
  reduce dZ^T @ X into dW
  optionally compute dX_router = dZ @ W
```

For zero allocation, logits/probabilities should be recomputed inside tiles or loaded from a saved forward state buffer that the wrapper explicitly owns.
