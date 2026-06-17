# Invoke Design - W6 CAP2 Exact Backward

Mode: `design`
Source define: `INVOKE-DEFINE.md`

## Context View

W5 fixed-mask Triton kernels now pass RunPod parity, allocation, and FP16 tests.
W6 should extend the research tower from fixed-mask backward to the selected
CAP2-v0 relaxation, but only after the exact backward contract is pinned.

## High-Level Structure View

The W6 implementation should have three layers:

1. Reference VJP layer:
   - manual CAP2 backward in PyTorch or standard tensor ops;
   - parity against `torch.autograd.grad`;
   - finite-difference checks on `W` and optionally `H`.

2. Triton parity layer:
   - CAP2 row-local backward kernel(s);
   - outputs `dW`, `dX_router`, and `dH`;
   - parity against the reference VJP.

3. Systems validation layer:
   - preallocated outputs;
   - FP16 input tolerance;
   - benchmark only after parity passes.

## Low-Level Components View

### Reference Components

- `cap2_backward_reference` or equivalent helper:
  - input: `X`, `W`, `H`, `load`, `f`, scalar hyperparameters;
  - output: dict with `loss`, forward intermediates, `dZ`, `dW`, `dX_router`, `dH`.

- Autograd oracle:
  - call `cap2_routing_torch`;
  - compare gradients for `W` and `H`;
  - compare `dX_router` separately if `X` is made differentiable and residual
    direct term is isolated.

### Triton Components

Two implementation options are allowed:

- fused per-row CAP2 backward plus reductions into `dW`;
- split kernels:
  - row kernel computes `dZ`, `dX_router`, `dH`, optional `A`;
  - reduction kernel reuses W5-style `dW = dZ^T @ X`.

Recommended first implementation: split kernels. It reduces risk by reusing the
validated W5 `dW` reduction path.

### Buffer Contract

Caller-owned outputs:

- `d_w_out`: `[E, D]`, `float32`.
- `d_x_router_out`: `[T, D]`, `float32`.
- `d_h_out`: `[T, E, D]`, `float32`.

Optional scratch:

- `d_z_scratch`: `[T, E]`, `float32`, allowed for W6-v0.

Zero-allocation finalization can later remove or predeclare scratch. W6-v0 may
use explicit caller-provided scratch as part of the contract.

## Workflow Process View

1. Add reference/manual CAP2 VJP.
2. Prove reference VJP against PyTorch autograd and finite differences.
3. Add Triton kernel for row-local `dZ`, `dX_router`, and `dH`.
4. Reuse fixed-mask `dW` Triton reduction on `dZ`.
5. Validate CUDA parity on RunPod.
6. Only then evaluate allocation, FP16, and benchmark claims.

## Decision Flow View

If manual reference VJP fails autograd parity:

- stop and fix math; do not write Triton.

If Triton parity fails:

- compare `dZ` first, then `dW`, `dX_router`, `dH`.

If memory pressure from `d_z_scratch` is unacceptable:

- record as W7/W6-v1 optimization, not W6-v0 blocker.

If `E` grows too large for row-local pairwise work:

- set W6-v0 max supported `E` and record scale limitation.

## Dependency Interface View

Inputs from existing code:

- `cap2_routing_torch` for autograd oracle;
- fixed-mask Triton output-buffer validation style;
- `<cuda-runner-iteration-command>` for external validation.

Outputs to downstream work:

- W6 exact backward parity report;
- benchmark target for W7-003;
- limitation text for W8 final report.

## Glossary Consistency

Pass:

- "exact backward" remains scoped to the chosen differentiable bridge.
- "zero allocation" remains separate from mathematical parity.
- CAP2 remains candidate-only, no novelty claim.

## Risks

- CAP2 pairwise rank is `O(E^2)` per token.
- Triton implementation may need an explicit maximum `E` for W6-v0.
- `d_z_scratch` may violate a strict no-scratch interpretation unless declared
  as caller-provided scratch.
