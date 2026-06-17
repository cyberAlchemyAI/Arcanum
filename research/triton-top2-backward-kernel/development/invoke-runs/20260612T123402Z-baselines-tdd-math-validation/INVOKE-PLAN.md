# Invoke Plan - Baselines, TDD, Math Validation

Run id: `20260612T123402Z-baselines-tdd-math-validation`

Status: `pass`

This is a non-executed plan. It should be consumed by a future Task Session.

## Wave 0 - Contract And Reference Harness

Goal: create tests that force semantic clarity.

Tasks:

1. Create a reference module for router loss experiments.
2. Encode V0 contract defaults.
3. Add tests that fail when required semantic fields are unset.
4. Add fixtures for tiny deterministic tensors.
5. Add debug outputs for all intermediates.

Acceptance:

- contract tests pass;
- fixed-mask forward reference runs;
- missing relaxation/capacity choices produce explicit errors, not silent defaults.

## Wave 1 - V0 Fixed-Mask Baseline

Goal: prove/test the safe baseline.

Tasks:

1. Implement `fixed_mask_top2_reference`.
2. Test `A = M * P`.
3. Test reconstruction loss.
4. Test auxiliary loss with fixed `f_j`.
5. Test autograd gradients for `dW`, `dX_router`, and `dH`.
6. Add finite-difference checks for tiny cases.

Acceptance:

- PyTorch autograd gradients match finite differences where applicable;
- no test claims gradient through `M`;
- V0 can serve as baseline oracle.

## Wave 2 - Math Validation

Goal: create formal math proof scaffolding.

Tasks:

1. Translate `FORMAL-MATH-SPEC.md` into Lean theorem stubs or equivalent proof notes.
2. Start with `PO-005 dW = dZ^T X`.
3. Add `PO-004 auxiliary gradient`.
4. Add `PO-001 softmax backward` after notation stabilizes.
5. Mark non-theorems explicitly in proof notes.

Acceptance:

- at least theorem statements exist for PO-001 through PO-006;
- one simple theorem/proof is completed or clearly blocked;
- proof scope does not include hard Top2.

## Wave 3 - Prior-Art Baselines

Goal: compare against known alternatives.

Tasks:

1. Add soft-routing reference.
2. Add sparsemax/entmax reference, using a known implementation or minimal local formula.
3. Add convex sparse top-k reference if feasible.
4. Add ReLU routing reference.
5. Record behavior: active experts, gradients, capacity violations, loss values.

Acceptance:

- at least three baselines run on the same fixtures;
- CAP2 cannot be claimed novel unless compared to them.

## Wave 4 - CAP2 Design Gate

Goal: either define CAP2 precisely or kill it.

Tasks:

1. Propose CAP2 forward operator.
2. Derive its exact backward/Jacobian.
3. Decide whether capacity uses local penalty, global load state, or deferred auxiliary term.
4. Decide exact vs expected vs sparse-ish two-expert support.
5. Compare formula against entmax/sparsemax and convex sparse top-k.
6. Run small numerical experiments if formula exists.

Acceptance:

One of:

- `CAP2=defined`: forward/backward/reference ready.
- `CAP2=killed`: equivalent to prior art or fails exact backward.
- `CAP2=deferred`: missing benchmark/acceptance info blocks design.

## Wave 5 - Triton Readiness Gate

Goal: decide whether kernel implementation can start.

Requirements:

- V0 tests pass.
- At least one candidate relaxation reference passes.
- `dW` and `dX_router` outputs are defined.
- output dtype/accumulation policy is defined.
- target GPU/Triton version captured.
- zero-allocation measurement method defined.

Acceptance:

- if all pass, open Triton implementation task;
- otherwise, keep implementation blocked and report exact missing fields.

## Suggested Test Files

```text
tests/test_contract.py
tests/test_reference_fixed_mask.py
tests/test_reference_gradients.py
tests/test_math_identities.py
tests/test_prior_art_baselines.py
tests/test_cap2_candidate.py
tests/test_triton_parity_v0.py
tests/test_zero_allocation.py
tests/test_fp16_tolerance.py
```

## Stop Conditions

Stop before Triton if:

- CAP2 has no forward formula;
- V0 gradients do not match finite differences;
- relaxation baseline cannot define exact backward;
- capacity semantics are still ambiguous for the selected candidate;
- target GPU/Triton version is unknown for performance claims.
