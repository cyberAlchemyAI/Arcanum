# Interrogation - Open Questions And Gaps

Target: `research/triton-top2-backward-kernel/`

Mode: `open-question decision interrogation`

Status: `pass`

## Question

Can we decide the open questions enough to move from research tower to a safe
next design/TDD step?

## Verdict

Yes, but split the work:

1. **V0 baseline:** fixed-mask Top2 backward can proceed to PyTorch reference and
   tests now.
2. **Novel candidate:** CAP2 needs a design session before implementation.
3. **Performance/kernel:** Triton implementation remains blocked until semantic
   contract and target environment are chosen.

## Findings

### F1 - The baseline can be made rigorous now

The fixed-mask baseline has enough information if we make conservative choices:

- `W ||...||^2` becomes `lambda_rec * ||...||^2`;
- `FFN(X)` becomes precomputed `H`;
- `A = M * P`;
- `M` is saved from forward;
- `f_j` is fixed for auxiliary gradient;
- capacity is checked, not differentiated.

This is not a novel solution. It is the anti-hallucination baseline.

### F2 - The challenge likely expects a relaxation choice

The prompt explicitly mentions bypassing nondifferentiable selection via
continuous relaxation. So a final answer should not stop at fixed-mask Top2.

### F3 - CAP2 is a reasonable novelty hypothesis

CAP2 is worth exploring because it combines constraints not usually optimized
together in the prior-art framing:

- `k=2` specifically;
- proof-first backward;
- capacity awareness;
- zero-allocation FP16 Triton friendliness.

But CAP2 is not yet a solution. It has no operator formula.

### F4 - Capacity is the most dangerous ambiguity

If capacity is a hard constraint, it has no ordinary gradient. If it is a
penalty/barrier, it changes the objective. If it is built into routing, it may
require batch/global state. CAP2 must choose this explicitly.

### F5 - Exact 2-sparsity may conflict with smoothness

A smooth relaxation can be differentiable and sparse-ish, but exact 2-sparsity
with clean gradients is harder. This is where convex sparse top-k prior art is
the strongest competitor.

## Decisions

See `../../OPEN-QUESTIONS-DECISION-LEDGER.md`.

## Blockers

- No CAP2 forward operator yet.
- No CAP2 backward/Jacobian yet.
- No target GPU/Triton version yet.
- No benchmark acceptance rule for exact vs sparse-ish top-2 training.

## Recommendation

Proceed with:

1. V0 PyTorch reference tests for fixed-mask baseline.
2. CAP2 design session.
3. Prior-art equivalence check before implementation.
