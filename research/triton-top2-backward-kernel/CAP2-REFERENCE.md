# CAP2-v0 Reference

Status: reference-and-gradcheck-pass
Date: 2026-06-12

## Task

`TASK-W3-001`: Implement CAP2-v0 reference.

## Result

Implemented CAP2-v0 in the standard-library oracle and PyTorch reference.

Covered:

- capacity-adjusted logits with fixed load;
- pairwise soft rank;
- soft top-2 membership;
- normalized gated softmax combine weights;
- reconstruction and auxiliary loss integration;
- PyTorch autograd/gradcheck for the fixed-load smooth graph.

## Implemented API

Standard-library functions in `reference/router_reference.py`:

```text
cap2_adjusted_logits_rows
cap2_pairwise_soft_rank_rows
cap2_membership_rows
cap2_routing_weights_rows
cap2_routing_reference
```

PyTorch functions in `reference/router_torch.py`:

```text
cap2_routing_weights_torch
cap2_routing_torch
cap2_manual_backward
```

Triton functions in `reference/router_triton.py`:

```text
cap2_row_backward_triton
```

## Contract

For fixed load vector `load_j`, CAP2-v0 computes:

```text
capacity = 2.1 / E
over_j = sigmoid((load_j - capacity) / tau_cap)
Z'_tj = Z_tj - mu * over_j
s_tj = sum_{k != j} sigmoid((Z'_tj - Z'_tk) / tau_rank)
G_tj = sigmoid((s_tj - (E - 2 - 0.5)) / tau_gate)
P_tj = softmax(Z'_t)_j
B_tj = G_tj * P_tj
A_tj = B_tj / (epsilon + sum_k B_tk)
```

The loss uses the existing reconstruction skeleton and auxiliary term:

```text
Y_t = sum_j A_tj H_tj
L_rec = lambda_rec * sum_t ||Y_t - X_t||^2
L_aux = gamma * E * sum_j f_j * Pbar_j
```

## Validation

Key checks:

- CAP2 weights are normalized and top-2-shaped on a simple row.
- Capacity pressure reduces weight assigned to an overloaded expert.
- PyTorch CAP2 weights match the standard-library oracle.
- PyTorch CAP2 full forward matches the standard-library oracle.
- PyTorch gradcheck passes for `W` and `H` with fixed load.
- Manual CAP2 backward matches PyTorch autograd for `dW`, `dH`, and `dZ`.
- Manual CAP2 `dW` matches finite differences.
- Triton CAP2 backward matches the manual reference for `dZ`, `dX_router`,
  `dH`, and `dW` on RunPod.

Validation commands:

```text
.venv/bin/python -m pytest tests/test_router_reference.py tests/test_router_torch.py -q
.venv/bin/python -m pytest tests -q
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
<cuda-runner-iteration-command>
```

## Non-Claims

- CAP2-v0 does not guarantee exact 2-sparsity.
- CAP2-v0 does not differentiate through dynamic load.
- CAP2-v0 is not claimed novel.
- CAP2-v0 performance has not been benchmarked.
- CAP2-v0 zero-allocation behavior has not been measured as a W7 acceptance
  check.

## Next Work

Proceed to `TASK-W3-002`: compare CAP2-v0 against prior-art baselines.

The comparison should include fixed-mask Top2, sparsemax, normalized ReLU,
convex sparse top-k direct mask, and convex sparse top-k normalized masked
softmax. It should separate forward behavior, support shape, capacity response,
and backward availability instead of collapsing them into one score.
