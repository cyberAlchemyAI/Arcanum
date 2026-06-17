# Closeout - Triton Top2 Backward Research Dispatch

Run id: `20260612T121416Z-top2-backward-research`

Overall status: `flag`

## What Was Executed

The validated research dispatch was executed as an artifact-backed closeout:

- all route step outputs were checked against existing tower artifacts;
- per-step receipts were written;
- dispatch validation was rerun;
- implementation readiness was assessed.

## What Is Complete

- Research tower exists.
- Dispatch route validates.
- Source/context recovery exists.
- Definitions and glossary exist.
- Claim ledger exists.
- Backward derivation and formal proof targets exist.
- Rigor/no-hallucination guardrails exist.
- Relaxation candidate matrix exists.
- Triton implementation notes exist.
- Learning pack exists.

## What Is Not Complete

Triton implementation should not begin yet. Required decisions:

1. Choose the continuous relaxation:
   - convex sparse differentiable top-k,
   - sparsemax/entmax,
   - temperature soft top-2,
   - SOFT top-k OT,
   - Gumbel top-k,
   - ReLU MoE routing,
   - or fixed-mask baseline only.
2. Decide whether exact 2-sparsity is required during training.
3. Decide top-2 combine semantics.
4. Decide capacity semantics.
5. Decide whether `FFN(X)` is precomputed or part of the kernel.
6. Capture target GPU and Triton version.

## Recommended Next Execution

Run a TDD task session with this scope:

```text
Implement PyTorch reference and tests only.
Do not implement Triton yet.
Use fixed-mask Top2 as baseline.
Add one candidate continuous relaxation, preferably convex sparse top-k or entmax/sparsemax.
Compare gradients and produce a decision report.
```

## Final Verdict

`flag`: research execution is complete; implementation remains gated by a
specific, named relaxation and reference-test decision.
