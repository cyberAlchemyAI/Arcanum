# Governed Definitions

## DEF-001 - Tensor Shapes

Unless a later implementation spec overrides this, the tower uses:

- `X`: `[T, D]`, FP16 input tokens/features.
- `W`: `[E, D]`, FP16/FP32 router weights.
- `Z = X W^T`: `[T, E]`, router logits.
- `P = softmax(Z)`: `[T, E]`, router probabilities.
- `H = FFN(X)`: either `[T, E, D]` for per-expert outputs or `[T, E, O]` for output dimension `O`.
- `A = Top2(P)`: `[T, E]` sparse combine weights.
- `Y_t = sum_j A_tj H_tj`: reconstructed output.
- `R = Y - X`: residual, if output dimension equals `D`.

## DEF-002 - Load Terms

- `P_j = (1 / T) * sum_t P_tj`, the mean router probability for expert `j`.
- `f_j = (1 / T) * sum_t S_tj`, where `S_tj` is the top-2 selection/load indicator or a relaxed substitute.
- `L_aux = gamma * E * sum_j f_j * P_j`.

## DEF-003 - Top-2 Backward Contract

The hard top-2 indices are nondifferentiable. A valid "exact backward" must name one of:

1. **Fixed-mask exact backward:** top-2 mask is computed in forward and treated as constant in backward; gradients flow through softmax values for selected experts only.
2. **Relaxed top-2 exact backward:** a continuous top-2 relaxation is specified and gradients are exact for that relaxation.
3. **Straight-through estimator:** hard top-2 forward with a surrogate backward. This is useful but not exact in the mathematical sense.

This tower recommends option 1 as the narrowest implementation interpretation unless the user supplies a specific relaxation.

## DEF-004 - Zero Allocation

Zero allocation means no new persistent PyTorch tensors or device buffers are allocated by the backward path. Temporary values in registers/SRAM inside a Triton program are allowed. Output tensors such as `dX`, `dW`, and optionally `dH` must be preallocated by the wrapper.

## DEF-005 - Capacity Constraint

`max_j(f_j) <= 2.1 / E` is a feasibility or penalty gate. A pure backward kernel cannot enforce it unless the forward path has already chosen a feasible routing or the objective includes a differentiable barrier/penalty for violations.
