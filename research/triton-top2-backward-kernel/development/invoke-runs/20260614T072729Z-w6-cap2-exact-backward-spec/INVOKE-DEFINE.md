# Invoke Define - W6 CAP2 Exact Backward

Mode: `define`
Target artifact: `TASK-W6-001` selected-relaxation exact backward specification
Decision input: user selected option `2`, exact CAP2 backward spec first.

## Problem Statement

`TASK-W6-001` cannot safely proceed from "implement selected relaxation kernel"
until the selected relaxation backward contract is explicit. CAP2-v0 is promoted
as a candidate only, but the implementation target must avoid overclaiming.

## Selected Scope

Define an implementation-ready exact-backward target for CAP2-v0 with fixed
load:

```text
Exact backward for the CAP2-v0 differentiable graph, given fixed load_j.
```

Not in scope:

- exact backward through hard Top2;
- novelty claim;
- dynamic-load gradients;
- full FFN internals beyond precomputed expert outputs `H`;
- production performance optimization before parity.

## Tensor Contract

Inputs:

- `X`: `[T, D]`, token activations.
- `W`: `[E, D]`, router weights.
- `H`: `[T, E, D]`, precomputed expert outputs.
- `load`: `[E]`, fixed load vector for CAP2 pressure.
- `f`: `[E]`, fixed auxiliary weights.
- scalars: `lambda_rec`, `gamma`, `tau_rank`, `tau_gate`, `tau_cap`, `mu`, `epsilon`.

Forward intermediates:

- `Z = X W^T`: `[T, E]`.
- `over_j = sigmoid((load_j - 2.1 / E) / tau_cap)`: `[E]`.
- `U = Z - mu * over`: `[T, E]`.
- `P = softmax(U)`: `[T, E]`.
- `Q_tjk = sigmoid((U_tj - U_tk) / tau_rank)` for `j != k`, diagonal ignored.
- `Srank_tj = sum_{k != j} Q_tjk`: `[T, E]`.
- `G_tj = sigmoid((Srank_tj - (E - 2 - 0.5)) / tau_gate)`: `[T, E]`.
- `B = G * P`: `[T, E]`.
- `N_t = epsilon + sum_j B_tj`: `[T]`.
- `A_tj = B_tj / N_t`: `[T, E]`.
- `Y_td = sum_j A_tj H_tjd`: `[T, D]`.
- `R = Y - X`: `[T, D]`.
- `L_rec = lambda_rec * sum_td R_td^2`.
- `L_aux = gamma * E * sum_j f_j * mean_t P_tj`.
- `L = L_rec + L_aux`.

Backward outputs:

- required: `dW = dZ^T @ X`: `[E, D]`.
- required: `dX_router = dZ @ W`: `[T, D]`.
- required: `dH_tjd = A_tj * dY_td`: `[T, E, D]`.
- optional/report-only: `dA`, `dB`, `dG`, `dP`, `dU`.

Fixed no-gradient inputs:

- `load`;
- `f`;
- temperatures and scalar hyperparameters.

## Backward Formula Contract

Let:

```text
dY_td = 2 * lambda_rec * R_td
dA_tj = sum_d dY_td * H_tjd
dH_tjd = A_tj * dY_td
C_t = sum_j dA_tj * B_tj
dB_tj = (dA_tj * N_t - C_t) / N_t^2
dG_tj += dB_tj * P_tj
dP_tj += dB_tj * G_tj
dP_tj += gamma * E * f_j / T
dU_from_softmax_tj = P_tj * (dP_tj - sum_k dP_tk * P_tk)
dSrank_tj = dG_tj * G_tj * (1 - G_tj) / tau_gate
```

Pairwise-rank contribution:

```text
rank_factor_tjk = Q_tjk * (1 - Q_tjk) / tau_rank
dU_from_rank_tj += sum_{k != j} dSrank_tj * rank_factor_tjk
dU_from_rank_tk -= dSrank_tj * rank_factor_tjk
```

Then:

```text
dZ = dU_from_softmax + dU_from_rank
dW = dZ^T @ X
dX_router = dZ @ W
```

This formula is exact for the named CAP2-v0 differentiable graph with fixed
load, subject to normal floating-point tolerance.

## Acceptance Boundary

The W6 implementation cannot pass on a Triton kernel alone. It must first pass
PyTorch/manual VJP parity against autograd and finite differences, then Triton
parity against the validated reference.

## Glossary

- `CAP2-v0`: Capacity-Aware Pairwise Relaxation for Top-2 routing.
- `fixed load`: load vector is treated as input data and receives no gradient.
- `exact backward`: exact VJP of the smooth CAP2-v0 computational graph, not the
  hard Top2 event.
- `row-local`: each token row can be processed independently except for fixed
  batch-level vectors such as `load` and auxiliary `f`.
