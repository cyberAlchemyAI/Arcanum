# Invoke Design - Baselines, TDD, Math Validation

Run id: `20260612T123402Z-baselines-tdd-math-validation`

Status: `pass`

## Design Summary

Use a layered validation architecture:

```text
Layer 0: contract and glossary
Layer 1: PyTorch reference baselines
Layer 2: gradient/math validation
Layer 3: CAP2 design/equivalence check
Layer 4: Triton parity
Layer 5: FP16/zero-allocation/performance
```

Implementation starts only after layers 0-3 are green or explicitly scoped.

## Architecture

### Layer 0 - Contract Gate

Purpose: prevent hidden math choices.

The test harness must fail fast if these are unset:

- `sigma`;
- reconstruction weight meaning;
- `FFN(X)` scope;
- top-2 combine semantics;
- capacity semantics;
- relaxation identity;
- saved mask/gate contract;
- output gradient contract.

V0 defaults:

```text
sigma = softmax
lambda_rec = scalar
H = precomputed
A = M * P
capacity = check/flag
M = saved from forward
```

### Layer 1 - Reference Baselines

Implement as ordinary PyTorch functions:

1. `fixed_mask_top2_reference`
2. `soft_routing_reference`
3. `entmax_or_sparsemax_reference`
4. `convex_sparse_topk_reference` if feasible from prior-art implementation
5. `cap2_reference` only after CAP2 is defined

Each reference returns:

```text
loss
Y
Z
P or A
aux_loss
debug intermediates
```

### Layer 2 - Gradient Validation

Use:

- PyTorch autograd;
- finite differences for small examples;
- `gradcheck` where smooth;
- hand-computed tiny cases;
- Lean proof targets for V0 equations.

Gradient outputs:

- `dW`;
- `dX_router`;
- `dH` if `H` is an input;
- optionally `dX_total` only after direct residual and FFN path are specified.

### Layer 3 - CAP2 Design And Kill Gate

CAP2 must define:

```text
A = CAP2(Z, load_state, parameters)
```

Required properties:

- top-2-specific or near-top-2 behavior;
- capacity-aware term or mechanism;
- exact backward/Jacobian;
- row-local if possible;
- stable under FP16-like ranges;
- comparable against prior art.

Kill CAP2 if:

- it is equivalent to entmax/sparsemax;
- it is equivalent to convex sparse top-k for `k=2`;
- it cannot define exact backward;
- it requires global iterative solve but claims kernel simplicity;
- it cannot be tested against baselines.

### Layer 4 - Triton Parity

Only after reference layers pass:

- implement one kernel for V0 `dW` parity first;
- compare FP32 parity against reference;
- add `dX_router`;
- add FP16 input/FP32 accumulation;
- add candidate relaxation kernel only after CAP2 or selected relaxation passes reference tests.

### Layer 5 - Systems Validation

Validate:

- no full tensor allocations for `Z`, `P`, `M`, `dP`, `dZ`;
- output buffers preallocated;
- scratch buffers explicit;
- no hidden PyTorch allocations in measured region;
- benchmark separately from correctness.

## Test Matrix

| Test Class | Purpose |
| --- | --- |
| Contract tests | Ensure semantic choices are explicit. |
| Forward reference tests | Ensure formulas produce expected small outputs. |
| Backward autograd tests | Ensure gradients exist and shapes match. |
| Gradcheck tests | Validate smooth reference gradients. |
| Golden tiny cases | Catch same-shape wrong-math errors. |
| Prior-art parity tests | Compare candidate behavior against known baselines. |
| Triton parity tests | Compare kernel outputs to reference. |
| Allocation tests | Enforce zero-allocation contract. |
| FP16 tolerance tests | Separate precision error from semantic error. |

## Evidence Model

Every stage should emit:

- source artifact;
- assumptions;
- test command;
- pass/flag/block;
- known residue;
- comparison baselines.

## Design Verdict

Proceed with V0 reference/TDD immediately. CAP2 requires a design pass before any
implementation claim. Triton waits for reference parity.
