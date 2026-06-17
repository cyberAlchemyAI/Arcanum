# Rigor Validation Map

Purpose: prevent hallucinated confidence. This file separates what can be proved,
what can be tested, and what must remain undecided until the problem statement is
more precise.

## Validation Layers

| Layer | Question | Best Tool | What It Can Validate | What It Cannot Validate |
| --- | --- | --- | --- | --- |
| L0 - Statement hygiene | Is the mathematical object fully specified? | Definitions/residue review | Symbols, shapes, assumptions, blockers | Correctness of the unstated problem |
| L1 - Reference semantics | Does a concrete differentiable graph run? | PyTorch/JAX reference | Forward values, autograd gradients, gradcheck for smooth cases | GPU kernel correctness |
| L2 - Formal math | Are the gradient equations valid over real numbers? | Lean 4 / Mathlib | Softmax backward, chain rule, `dW = dZ^T X`, fixed-mask derivatives | FP16, Triton, allocation behavior |
| L3 - Numerical parity | Does implementation match reference within tolerance? | PyTest + PyTorch + Triton | FP32/FP16 output and gradient parity | Mathematical proof |
| L4 - Systems contract | Is the kernel zero-allocation and performant? | CUDA memory stats, profiler, benchmarks | Allocation budget, speed, memory traffic | Derivative correctness by itself |

## No-Hallucination Rules

1. Do not claim "exact backward for Top2" without saying which differentiable
   bridge is being used.
2. Do not claim the capacity constraint has gradients unless it is turned into a
   differentiable penalty/barrier or relaxed projection.
3. Do not claim the Triton kernel is correct because a formula looks right;
   compare it against a reference.
4. Do not claim the Lean proof validates FP16 or Triton. Lean validates the
   idealized math unless a separate floating-point proof is built.
5. Do not claim zero allocation if the Python wrapper materializes `Z`, `P`,
   `M`, `dP`, or `dZ` as full tensors.

## Recommended Rigor Path

### Step 1 - Freeze A V0 Contract

Use a deliberately narrow contract:

```text
sigma = softmax
H = FFN(X) is precomputed expert output
M = saved top-2 mask from forward
A = M * P
f_j = fixed hard load, no gradient through f
capacity = checked/flagged, not differentiated
lambda_rec = scalar reconstruction weight replacing ambiguous leading W
```

This is not the only possible interpretation. It is the smallest contract that
can be tested rigorously without inventing an unspecified relaxation.

### Step 2 - Write A PyTorch Reference

The reference should expose every intermediate in debug mode:

```text
Z, P, M, A, Y, L_rec, L_aux, L, dP, dZ, dW, dX_router
```

For TDD, make the first tests fail when any contract choice is missing.

### Step 3 - Prove The Core Identities

Formal proof target over real numbers:

```text
softmax_backward:
  dZ_j = P_j * (dP_j - sum_k P_k * dP_k)

router_weight_gradient:
  if Z_tj = dot X_t W_j,
  then dW_jd = sum_t dZ_tj * X_td

router_input_gradient:
  dX_td = sum_j dZ_tj * W_jd
```

The fixed mask `M` is treated as constant. The proof should not attempt to
differentiate through `argtop2`.

### Step 4 - Test Against The Proof/Reference Boundary

Use PyTorch tests to check:

- finite differences or `gradcheck` for smooth pieces;
- exact hand-computed small examples;
- autograd parity for the reference;
- Triton parity against the reference;
- edge cases: ties, near-ties, non-power-of-two shapes, capacity overflow.

### Step 5 - Only Then Optimize

Once the math/reference layer passes, implement Triton and benchmark.

## Tool Choice

| Tool | Use It For | Fit |
| --- | --- | --- |
| PyTorch autograd + `gradcheck` | Immediate TDD reference and gradient sanity | Best first step |
| Lean 4 + Mathlib | Proving ideal real-number gradient identities | Best formal math step |
| Coq + Flocq | Floating-point proof obligations | Strong but heavy |
| Isabelle/HOL | General theorem proving | Strong, less repo-aligned |
| Dafny/F* | Program contracts and stateful correctness | Not the main fit for calculus here |
| SymPy | Symbolic sanity checks for tiny cases | Useful helper, not proof |

## Rigor Verdict

Lean is appropriate for proving the **math identities** after the graph is fixed.
It is not the first tool for validating the challenge. The first rigorous tool is
a PyTorch reference with contract tests, because it forces the missing choices to
be explicit and gives the Triton kernel an executable oracle.
