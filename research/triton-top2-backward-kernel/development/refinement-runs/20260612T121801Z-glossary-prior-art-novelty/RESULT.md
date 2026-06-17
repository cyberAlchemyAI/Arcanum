# Refine Result - Glossary, Prior Art, Novelty Search

Status: `pass`

## Final Synthesis

The glossary is now beginner-friendlier and prior-art-aware. The main conceptual
move is:

```text
prior art tells us what not to claim as new;
novelty search tells us where a new contribution might still live.
```

The safest novelty hypothesis is:

```text
K=2-specific, proof-first, capacity-aware sparse relaxation for Top2 routing.
```

This is not claimed as novel yet. It is a research hypothesis that must be
checked against prior art and tested against baselines.

## Prior Art In Plain English

Known work already covers:

- fixed-mask / stop-gradient top-k patterns;
- soft routing;
- sparsemax and entmax;
- SOFT top-k via optimal transport;
- convex sparse differentiable top-k;
- Gumbel relaxed top-k;
- ReLU routing / fully differentiable MoE;
- expert-choice and balanced-assignment routing.

So the possible novel space is not "make Top2 differentiable." It is more
specific:

- make it top-2-specific;
- make it capacity-aware;
- make it proof-friendly;
- make it zero-allocation Triton-friendly;
- make the exact backward simple enough to test and prove.

## Recommended Next Route

Run a design session for `CAP2: Capacity-Aware Pairwise Relaxation for Top-2
Routing`, with the explicit goal of either killing it as prior art-equivalent or
turning it into a precise forward/backward spec.
