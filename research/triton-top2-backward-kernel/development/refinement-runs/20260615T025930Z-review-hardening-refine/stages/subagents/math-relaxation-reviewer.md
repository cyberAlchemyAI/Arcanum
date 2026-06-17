# Subagent Receipt - Math Relaxation Reviewer

agent_id: `math-relaxation-reviewer::<runtime-assigned>`
role_id: `math-relaxation-reviewer`
spawn_status: `spawned`
join_status: `completed`
close_status: `closed`
dispatch_id: `refine-20260615T025930Z-review-hardening`
step_id(s): `s5`, `s8`, `s9`
capability_ref: `refine/subagent-review`
status: `flag`
validation_result: `completed-with-residue`

## Ownership

Owned review surface:

- exact 2-sparsity gap;
- dynamic-load gradient gap;
- fixed-load versus dynamic-load contract;
- formal/numerical validation boundary.

This receipt only refines proof and test targets. It does not mutate the kernel,
paper, proof files, or work-pack.

## Artifacts

- This receipt:
  `research/triton-top2-backward-kernel/development/refinement-runs/20260615T025930Z-review-hardening-refine/stages/subagents/math-relaxation-reviewer.md`

## Evidence Paths

- `research/triton-top2-backward-kernel/derivation.md`
- `research/triton-top2-backward-kernel/open-residue.md`
- `research/triton-top2-backward-kernel/RIGOR-VALIDATION-MAP.md`
- `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md`
- `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md`
- `research/triton-top2-backward-kernel/CAP2-REFERENCE.md`
- `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`
- `research/triton-top2-backward-kernel/paper/CLAIM-GUARDS.md`
- `research/triton-top2-backward-kernel/paper/PAPER-REVIEW.md`
- `research/triton-top2-backward-kernel/paper/formal/FORMAL-VALIDATION-REPORT.md`
- `research/triton-top2-backward-kernel/paper/formal/TritonTop2/SoftmaxCoordinate.lean`
- `research/triton-top2-backward-kernel/paper/formal/TritonTop2/CAP2Definition.lean`
- `research/triton-top2-backward-kernel/paper/formal/TritonTop2/CAP2FixedLoadScalar.lean`
- `research/triton-top2-backward-kernel/paper/formal/TritonTop2/FixedLoadCAP2.lean`

## Findings

### CAP2 Exact 2-Sparsity

Current evidence supports only a sparse-ish or top-2-shaped CAP2-v0 relaxation,
not exact 2-sparsity. `CAP2-CANDIDATE-SPEC.md` defines CAP2-v0 as normalized
gated softmax:

```text
P_tj = softmax(Z'_t)_j
B_tj = G_tj * P_tj
A_tj = B_tj / (epsilon + sum_k B_tk)
```

Because `P_tj`, `G_tj`, and the denominator are smooth positive-style terms
under ordinary finite settings, CAP2-v0 should not be presented as exactly
two-active-expert routing. The current paper/package already guards this through
`NC-003` in `CLAIM-GUARDS.md`, the W6 report, and `PAPER-REVIEW.md`.

Rigorous target:

- Treat exact 2-sparsity as a separate theorem/test goal, not as an implicit
  property of CAP2-v0.
- Define support precisely before proving or testing:
  `support_epsilon(A_t) = {j | A_tj > epsilon_support}` for numerical tests, or
  exact real support `{j | A_tj != 0}` for formal math.
- For CAP2-v0, the expected proof target is negative or boundary-shaped:
  "CAP2-v0 does not guarantee exact 2-sparsity in general."
- If exact 2-sparsity is required, use a different operator family or a hard
  projection step whose backward contract must be separately scoped.

Suggested falsification fixture:

- Use one row with four experts and non-tie logits.
- Evaluate CAP2-v0 at moderate temperatures.
- Assert that more than two entries can be greater than a small tolerance.
- Record this as a non-claim guard test, not a failure of the implementation.

### Dynamic-Load Gradients

The current CAP2-v0 contract treats `load_j` or `f_j` as fixed data. This is
explicit in `CAP2-CANDIDATE-SPEC.md`, `CAP2-REFERENCE.md`,
`CAP2-W6-PARITY-REPORT.md`, `FORMAL-VALIDATION-REPORT.md`, and `CLAIM-GUARDS.md`.
`derivation.md` also names the missing additional term:

```text
gamma * E * sum_j Pbar_j * d(f_j)/dP_tk
```

That term cannot be derived until the project chooses a differentiable load
definition.

Rigorous target:

- Keep the current W6 claim as:
  "exact backward for smooth CAP2-v0 with fixed load."
- Add a new dynamic-load task only after defining:
  `f_j(P)` or `load_j(P)`; its shape; batch/token reduction; temperature or
  smoothing; and whether it participates in the capacity-adjusted logits,
  auxiliary loss, or both.
- Derive the added VJP explicitly:
  `dL/dP += gamma * E * d(sum_j f_j(P) * Pbar_j)/dP`.
- If load pressure also changes `Z'_tj = Z_tj - mu * over_j(load(P))`, include
  the extra path from `A -> Z' -> over -> load -> P/Z`.

Suggested toy dynamic-load definitions:

1. Smooth probability load:

```text
f_j(P) = mean_t P_tj
```

This is easiest to prove and test but may duplicate `Pbar_j`.

2. Smooth gate load:

```text
f_j(G) = mean_t G_tj
```

This better matches CAP2 membership but requires soft-rank and sigmoid-chain
derivatives.

3. Temperature-thresholded load:

```text
f_j(A) = mean_t sigmoid((A_tj - theta) / tau_load)
```

This gives a tunable "active enough" load but adds threshold sensitivity.

### Fixed-Load Versus Dynamic-Load Contract

The current contract is valid and useful because it separates differentiable
router math from batch-level routing-state feedback. The exact wording should
remain:

```text
Exact backward for the CAP2-v0 differentiable graph, given fixed load_j.
```

It should not be widened to:

```text
Exact backward through dynamic load_j.
```

Proof/test target:

- Add a contract test that fails if `load` is accidentally treated as a trainable
  differentiable input in the fixed-load path.
- Add a separate dynamic-load reference function with a different name if the
  project chooses to explore it, for example `cap2_dynamic_load_routing_torch`.
- Require dynamic-load tests to compare against PyTorch autograd and finite
  differences before any Triton implementation.

### Lean Boundary

Lean is already valuable here, but its current boundary is narrow. The formal
report says Lean proves real-valued finite router adjoint identities, fixed-mask
adjoint identities, a finite softmax coordinate derivative, CAP2 definitions,
and a first fixed-load adjusted-logit slice. It explicitly does not prove Triton
kernels, GPU memory behavior, FP16 numerical equivalence, hard Top2
differentiability, a packaged full softmax Jacobian theorem, or full CAP2
calculus.

Lean can prove next:

- A packaged finite softmax Jacobian theorem from the completed coordinate
  derivative:

```text
d softmax_i / d z_k = softmax_i(z) * (delta_ik - softmax_k(z))
```

- The reverse-mode softmax VJP:

```text
dZ_k = P_k * (dP_k - sum_i P_i * dP_i)
```

- Fixed-load CAP2 sub-derivatives after selecting a canonical theorem order:
  adjusted logits, soft-rank sigmoid terms, membership gates, gated weights,
  denominator, and normalized combine weights.

Lean should not be used to claim:

- FP16 numerical correctness;
- Triton/CUDA memory behavior;
- zero allocation;
- hard Top2 differentiability;
- exact 2-sparsity for CAP2-v0 unless a separate exact-support theorem is stated
  and proved.

## Blockers

- Exact 2-sparsity is not a property of the current CAP2-v0 formula.
- Dynamic-load gradients are blocked until a differentiable definition of
  `f_j(P)`, `load_j(P)`, or `load_j(A/G)` is selected.
- Full CAP2 calculus in Lean is blocked on theorem-slicing effort for sigmoid,
  pairwise soft-rank, membership gates, and normalized gated softmax.
- Floating-point/FP16 validation is outside Lean's current real-number proof
  model and must remain numerical unless a separate floating-point proof stack is
  introduced.

## Residue

- Keep CAP2-v0 as `candidate-only`, `fixed-load`, and `not exact 2-sparse`.
- Keep dynamic-load gradients as a future extension, not a hidden part of W6.
- Keep Lean claims theorem-specific; do not use Lean as evidence for GPU memory,
  zero-allocation, or FP16 behavior.
- The next synthesis should decide whether exact 2-sparsity is a challenge
  requirement or only an evaluation metric.

## Reroute

Recommended reroute: `invoke -> task-session`.

Create a math-focused work-pack that first locks the fixed-load/dynamic-load
contract, then adds small reference tests, and only then considers Lean or Triton
extensions.

## Recommended Next Tasks

1. `TASK-MATH-001`: Add an exact-2-sparsity non-claim fixture for CAP2-v0.
   Validation: PyTorch/standard-library fixture shows more than two active
   entries above a named tolerance for at least one row.

2. `TASK-MATH-002`: Define the dynamic-load design menu.
   Validation: one short design artifact chooses among `f_j(P)`, `f_j(G)`, or
   thresholded `f_j(A)` and records the VJP paths that must be added.

3. `TASK-MATH-003`: Implement a PyTorch-only dynamic-load reference after the
   design gate.
   Validation: `gradcheck` and finite-difference parity for `W`, `H`, and the
   selected load path.

4. `TASK-MATH-004`: Package the Lean softmax coordinate theorem into a full
   finite softmax Jacobian/VJP theorem.
   Validation: `lake build` and a report update that explicitly states the
   theorem does not imply hard Top2 differentiability.

5. `TASK-MATH-005`: Create a CAP2 Lean proof ladder.
   Validation: separate theorem targets for adjusted logits, soft-rank,
   membership, gated weights, normalization denominator, and fixed-load combine
   weights before attempting a full derivative.

6. `TASK-MATH-006`: Add a claim-guard check that paper text never widens
   "fixed-load CAP2 exact backward" into "dynamic-load exact backward" or
   "hard Top2 exact backward."
   Validation: grep/scripted text check over the paper package and claim guards.
