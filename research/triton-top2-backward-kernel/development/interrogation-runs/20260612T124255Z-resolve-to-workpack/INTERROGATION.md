# Interrogation - Resolve Open Questions To Work-Pack

Status: `pass`

## Target

`research/triton-top2-backward-kernel/`

## Question

Can we solve the open questions enough to invoke a full work pack that can carry
the effort to completion?

## Verdict

Yes, with one important discipline:

```text
We resolve questions as execution assumptions, not as final truth claims.
```

## Key Resolution

CAP2 now has a v0 candidate formula in `CAP2-CANDIDATE-SPEC.md`.

CAP2-v0:

- uses capacity-adjusted logits;
- computes pairwise soft rank;
- gates softmax weights with a soft top-2 membership;
- normalizes selected soft weights;
- treats load as fixed for the first candidate;
- does not claim exact 2-sparsity;
- does not claim novelty yet.

## Main Risk

CAP2-v0 may be prior-art-equivalent to soft-rank differentiable sorting with a
capacity logit bias. Therefore the work pack must include a kill gate before any
novelty claim.

## Decision

Invoke a full work pack with waves:

1. Reference harness and contract completion.
2. PyTorch autograd/gradcheck.
3. Prior-art baselines.
4. CAP2-v0 design-or-kill.
5. Math validation.
6. Triton V0 fixed-mask kernel.
7. Triton selected-relaxation kernel.
8. Zero-allocation and FP16 validation.
9. Final comparison and novelty report.
