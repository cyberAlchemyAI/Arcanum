# CAP2 Candidate Spec

Status: `promoted-candidate-no-novelty-claim`

Purpose: define a concrete candidate so the project can stop treating CAP2 as a
name-only idea. This is not a novelty claim.

## Name

```text
CAP2: Capacity-Aware Pairwise Relaxation for Top-2 Routing
```

## Design Intent

CAP2-v0 should be:

- deterministic;
- differentiable;
- top-2-shaped;
- capacity-aware;
- row-local except for optional batch-level load pressure;
- simple enough for PyTorch reference tests;
- plausible enough to later evaluate for Triton.

## Inputs

For token `t` and expert `j`:

- `Z_tj`: router logit.
- `load_j`: current smooth/fixed load estimate for expert `j`.
- `capacity = 2.1 / E`.
- `tau_rank > 0`: soft-rank temperature.
- `tau_gate > 0`: soft membership temperature.
- `mu >= 0`: capacity pressure strength.

## Capacity-Adjusted Logits

Define smooth overload:

```text
over_j = sigmoid((load_j - capacity) / tau_cap)
```

Then:

```text
Z'_tj = Z_tj - mu * over_j
```

For V0, `load_j` is treated as fixed with respect to `Z`. A later version may
differentiate through a relaxed load estimate.

## Pairwise Soft Rank

For each token:

```text
s_tj = sum_{k != j} sigmoid((Z'_tj - Z'_tk) / tau_rank)
```

`s_tj` approximates how many experts expert `j` outranks. For `E` experts,
membership in hard top-2 corresponds roughly to:

```text
s_tj >= E - 2
```

## Soft Top-2 Membership

Use:

```text
G_tj = sigmoid((s_tj - (E - 2 - 0.5)) / tau_gate)
```

The `0.5` margin creates a soft boundary between rank 2 and rank 3.

## Combine Weights

V0 uses normalized gated softmax:

```text
P_tj = softmax(Z'_t)_j
B_tj = G_tj * P_tj
A_tj = B_tj / (epsilon + sum_k B_tk)
```

This gives a differentiable sparse-ish mixture. It does not guarantee exact
2-sparsity.

## Loss Integration

Use the same reconstruction skeleton:

```text
Y_t = sum_j A_tj H_tj
L_rec = lambda_rec * sum_t ||Y_t - X_t||^2
```

Capacity/load regularization is initially:

```text
L_aux = gamma * E * sum_j f_j * Pbar_j
```

with `f_j` fixed for V0 comparisons. CAP2 capacity pressure enters through
`Z'` using `load_j`.

## Exact Backward Claim

Allowed:

```text
Exact backward for the CAP2-v0 differentiable graph, given fixed load_j.
```

Not allowed:

```text
Exact backward through hard Top2.
```

Not yet allowed:

```text
Exact backward through dynamic load_j.
```

## Prior-Art Risk

CAP2-v0 may be equivalent to or a minor variant of soft-rank / NeuralSort-style
relaxations plus capacity-adjusted logits. It must be compared before any novelty
claim.

## Acceptance For Candidate Survival

CAP2-v0 survives initial design only if:

1. the forward operator is implementable in a reference function;
2. gradients pass finite-difference or PyTorch gradcheck;
3. active support trends toward two experts as temperatures decrease;
4. capacity pressure changes routing in the expected direction;
5. it is not trivially identical to entmax/sparsemax or convex sparse top-k;
6. it has a credible row-wise Triton path.

## Reference Status

`TASK-W3-001` implemented the CAP2-v0 reference in standard-library and PyTorch
form. Forward parity and fixed-load PyTorch gradcheck pass. Survival still
requires `TASK-W3-002` comparison against prior-art baselines and `TASK-W3-003`
kill/promote/defer decision.

## Decision Status

`TASK-W3-003` promoted CAP2-v0 as a candidate only. This means CAP2-v0 remains
eligible for later Triton feasibility and broader comparison, but it is not a
novelty claim, not exact 2-sparse, and not a final selected solution.
