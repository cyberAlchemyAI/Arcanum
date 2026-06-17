# Refine Result - TDD/Testability for Triton Top-2 Backward Kernel

## Status

`flag`

The problem is testable, but not directly as a Triton-first task. It must be
tested as a staged mathematical contract first, then as a kernel implementation.
The Refine run is flagged because the original execution used stale legacy
command-route checks and did not collect full native stage receipts for every
stage. This has been corrected in `CORRECTION.md` and `REFINE-DISPATCH.json`.

The corrected dispatch route validates:

```text
VALIDATION=pass
DISPATCH=research/triton-top2-backward-kernel/development/refinement-runs/20260612T114953Z-tdd-testability-full-refine/REFINE-DISPATCH.json
```

## Core Answer

Yes, we can do TDD for this problem.

The first test is not a GPU benchmark. The first test is: "what exact
differentiable graph are we claiming to implement?"

The hard `Top2` route is not differentiable through the choice itself, so TDD
must separate:

1. the reference differentiable bridge,
2. the expected gradients for that bridge,
3. the Triton implementation of those gradients,
4. the zero-allocation/performance contract.

## Smallest Coherent Testable Unit

The smallest coherent unit is:

```text
Given X, W, and precomputed expert outputs H:
  Z = X W^T
  P = softmax(Z)
  A = selected differentiable bridge over P
  Y = sum_j A_tj H_tj
  L = lambda_rec * ||Y - X||^2 + gamma * E * sum_j f_j * Pbar_j

Test dW, dX_router, and optionally dH against a PyTorch reference.
```

Do not include full expert FFN parameter backward in the first unit. That would
hide the router problem inside a much larger model.

## TDD Ladder

### Red 0 - Semantic Contract Test

Write tests that fail until the implementation names:

- `sigma = softmax`;
- top-2 combine rule: `A = M * P` or `A = M * P / sum(M * P)`;
- load rule: hard fixed `f_j`, relaxed `f_j`, penalty, or no gradient;
- capacity behavior: check, enforce, penalty, or barrier;
- `FFN(X)` scope: precomputed `H` vs full FFN backward.

Expected result: tests fail with a clear "contract unresolved" error until those
choices are explicit.

### Red 1 - PyTorch Forward Reference

Create a tiny PyTorch reference with deterministic tensors:

- `T = 2 or 3` tokens;
- `E = 3 or 4` experts;
- `D = 2` features;
- fixed `X`, `W`, and `H`;
- no ties in router logits for baseline cases.

Assertions:

- `P` rows sum to one;
- `A` has the expected sparsity/weights;
- `Y` matches hand-computed values;
- `L_aux` matches the chosen load rule.

### Red 2 - PyTorch Backward Reference

Use PyTorch autograd on the reference graph.

Assertions:

- `dW` exists and has shape `[E, D]`;
- `dX_router` exists if the reference differentiates through `Z = X W^T`;
- `dH` exists if `H` is an input to the tested surface;
- hard `f_j` contributes no gradient unless replaced by a relaxed load;
- fixed-mask top-2 does not pretend to differentiate through index selection.

For a smooth relaxation, add `gradcheck` in double precision.

### Red 3 - Formula-Level Golden Cases

Add hand-checkable golden cases:

- uniform-ish logits;
- one dominant expert;
- top-2 selected but not renormalized;
- top-2 selected and renormalized;
- equal logits/tie case marked as unstable or resolved by deterministic tie rule;
- capacity overflow case.

The goal is to catch "same shape, wrong math" before Triton exists.

### Red 4 - Triton Forward/Backward Parity

After the reference passes, test the Triton backward against the PyTorch
reference:

- FP32 inputs first;
- small sizes first;
- non-power-of-two `E` and `D`;
- compare `dW`, `dX_router`, and `dH` if produced;
- use tolerances that distinguish FP16 error from semantic mismatch.

### Red 5 - FP16 Precision Contract

Run FP16 input tests with FP32 accumulation.

Assertions:

- gradient max error within chosen tolerance;
- relative error reported separately from absolute error;
- ties and near-ties are either excluded from exact parity or covered by a
  deterministic saved-mask contract.

### Red 6 - Zero-Allocation Contract

Measure allocations around the Python wrapper.

Assertions:

- no allocation of `Z`, `P`, `M`, `dP`, or `dZ` as full tensors;
- output tensors are preallocated by the caller;
- allowed scratch is explicitly passed and counted;
- PyTorch CUDA memory counters do not increase except for declared outputs or
  setup outside the measured region.

### Red 7 - Performance Guard

Only after correctness:

- benchmark against the PyTorch reference;
- benchmark against a partially fused baseline;
- record throughput and memory bandwidth;
- keep performance thresholds loose until hardware/Triton version is pinned.

## Recommended Test Files For A Future Implementation

```text
tests/test_reference_contract.py
tests/test_reference_forward.py
tests/test_reference_backward.py
tests/test_reference_gradcheck.py
tests/test_triton_backward_parity.py
tests/test_triton_fp16_tolerance.py
tests/test_zero_allocation.py
tests/test_capacity_semantics.py
```

## First TDD Task Session

Implement only the reference and tests:

1. Create `reference_top2_router_loss` in a test helper.
2. Choose fixed-mask exact backward as the default initial contract.
3. Add contract tests that fail if semantic choices are missing.
4. Add tiny forward and backward parity expectations using PyTorch autograd.
5. Do not write Triton until these tests pass.

## Gates Before Triton

Triton implementation should not begin until:

- contract tests pass;
- PyTorch reference forward/backward tests pass;
- ambiguity residue R001-R006 is either resolved or explicitly fixed for v0;
- capacity semantics are fixed as check/enforce/penalty/barrier;
- output gradient contract is explicit.

## Recommended Next Routes

1. Operator decision: choose the differentiable bridge and combine semantics.
2. `task-session`: implement PyTorch reference plus tests only.
3. `task-session`: implement Triton `dW` parity kernel after reference tests pass.
4. Later: add zero-allocation measurement and FP16 performance gates.
