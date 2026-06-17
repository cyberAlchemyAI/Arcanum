# Learning Pack - Triton Top-2 Backward Kernel

## One-Sentence Model

This is a sparse MoE router backward problem: compute exact gradients for a specified differentiable top-2 routing surrogate, fuse softmax/top-2/load-balance math into Triton, and avoid materializing router intermediates.

## What the Task Is Really About

The hard part is not only writing Triton. The hard part is pinning down the mathematical graph:

- `Top2` is nondifferentiable.
- MoE load `f_j` is often a hard count and therefore nondifferentiable.
- The prompt asks for "exact backward" while also saying to bypass nondifferentiable selection with continuous relaxation.
- Therefore, exactness must be relative to the selected relaxation.

## Plain-Language Reading

The core issue is that we do not yet have a differentiable bridge between the
request/input, multiple latent spaces or expert routes, and the final mixed
routing decision.

The natural operation sounds like:

```text
scores -> pick the best 2 routes -> send the input only there
```

But `pick the best 2` is a hard choice. A tiny score change can suddenly swap
which latent space is selected, so normal backpropagation has no smooth gradient
through the choice itself.

To train the router, we need a smooth or surrogate bridge:

```text
request representation
-> route scores over latent spaces
-> mixture weights
-> combined output
```

The differentiable version is closer to:

```text
weights = softmax(scores)
mixed_output = sum_j weights_j * expert_j_output
```

or, if we still want top-2-like sparsity:

```text
weights = relaxed_top2(scores)
mixed_output = sum_j weights_j * expert_j_output
```

Then gradients can flow into the router because the weights move smoothly instead
of jumping as a discrete selection.

So the real design choice is:

- **Hard Top2:** efficient and sparse, but not differentiable through the choice.
- **Soft routing:** differentiable, but routes through every expert/latent space.
- **Relaxed top-2:** differentiable-ish and sparse-ish, if the relaxation is defined.
- **Straight-through top-2:** hard routing forward, surrogate gradient backward.
- **Fixed-mask backward:** exact after the top-2 choice is made, but not exact through the choice itself.

For this tower, "exact backward" means exact backward for the chosen differentiable
bridge, not exact backward through an impossible hard selection. A clearer target
objective would say:

```text
A = RelaxedTop2(softmax(X W^T))
Y = sum_j A_j * FFN_j(X)
```

Then the Triton kernel can implement the exact backward for that relaxed `A`.

## Recommended Interpretation

Start with fixed-mask exact backward:

1. Forward computes softmax probabilities and top-2 indices.
2. Backward treats the top-2 mask as constant.
3. Gradients flow through the selected softmax probabilities and the load-balancing `P_j` term.
4. Hard `f_j` has no gradient unless replaced by a relaxed load.

This matches the Switch/GShard idea of pairing hard load with differentiable probability mass while keeping the implementation narrow enough to validate.

## Implementation Spine

1. Build PyTorch reference for the chosen relaxation.
2. Write a Triton router backward kernel for `dW` and optionally `dX_router`.
3. Treat `FFN(X)` as a precomputed input unless expert FFN backward is explicitly in scope.
4. Recompute logits/softmax in the kernel to avoid allocating `Z` and `P`.
5. Accumulate reductions in FP32.
6. Validate before optimizing.

## Rigor Spine

To avoid hallucinating the math, validate in this order:

1. **Contract tests:** fail until `sigma`, top-2 combine semantics, `f_j`,
   capacity behavior, and `FFN(X)` scope are explicit.
2. **PyTorch reference:** create the executable oracle for the chosen graph.
3. **Gradient tests:** use autograd, finite differences, and `gradcheck` where
   the graph is smooth.
4. **Formal proof:** use Lean for the real-number gradient identities in
   `FORMAL-MATH-SPEC.md`.
5. **Triton parity:** compare kernel gradients against the PyTorch oracle.
6. **Systems checks:** verify zero allocation, FP16 tolerance, and benchmark
   behavior separately.

The key discipline: Lean can prove the clean derivative equations, but it does
not prove FP16 Triton correctness or zero allocation. Those need tests.

## Relaxation Choice

More data is in `RELAXATION-CANDIDATES.md`. The current reading is:

- fixed-mask Top2 is the best rigorous baseline;
- soft routing is the easiest sanity oracle;
- convex sparse differentiable top-k is the strongest match to "continuous Top2";
- sparsemax/entmax is the simpler sparse differentiable fallback;
- SOFT top-k via optimal transport is literature-strong but probably too heavy
  for a first zero-allocation Triton kernel;
- Gumbel top-k is useful for stochastic subset selection, but less suitable for
  deterministic exact-backward tests;
- ReLU MoE routing is a strong MoE-specific alternative, but changes the router
  away from Top2.

The recommended challenge strategy is two-track:

1. prove/test fixed-mask Top2 backward as the baseline oracle;
2. evaluate a named continuous top-2 relaxation, preferably convex sparse
   differentiable top-k or entmax/sparsemax, before implementing Triton.

Task-session update:

- A standard-library V0 reference harness now exists at `reference/router_reference.py`.
- Local tests exist at `tests/test_router_reference.py`.
- Manual `dW` backward matches finite differences on the tiny fixture.
- PyTorch autograd/gradcheck remains pending because PyTorch is not installed in
  the current environment.
- The final work-pack assumptions are now recorded in
  `FINAL-QUESTION-RESOLUTION.md`.
- The active end-to-end task matrix is `WORK-PACK.md`; its local implementation
  path is currently blocked by missing PyTorch, pytest, Triton, and visible GPU
  runtime.

## Prior Art And Novelty

Use `PRIOR-ART-MAP.md` before making any novelty claim. The main prior-art lesson
is that many people have already attacked "differentiable top-k" and "continuous
MoE routing." So a novel contribution must be narrower.

The most promising novelty hypothesis is in `NOVELTY-SEARCH-MAP.md`:

```text
K=2-specific, proof-first, capacity-aware sparse relaxation.
```

Working name:

```text
CAP2: Capacity-Aware Pairwise Relaxation for Top-2 Routing
```

This is still only a hypothesis, but it now has a concrete V0 forward operator
in `CAP2-CANDIDATE-SPEC.md`. It becomes a real contribution only after exact
backward equations, proof notes, a PyTorch reference, and comparison against
prior-art baselines.

## Dispatch Recommendation

Use the dispatch in `top2-backward-research.dispatch.json` as a full context-research route:

- lane 1: math semantics,
- lane 2: Triton implementation shape,
- lane 3: PyTorch integration,
- lane 4: MoE/load-balance references,
- lane 5: validation/performance plan.

## Current Execution Assumptions

The open questions are resolved for execution in `FINAL-QUESTION-RESOLUTION.md`:

- `sigma` is softmax.
- the leading `W` is treated as scalar `lambda_rec`.
- the V0 Top2 baseline uses `A = M * P` with a saved fixed mask.
- `FFN(X)` is precomputed expert output for router-backward work.
- `f_j` is fixed for V0 and capacity is checked or penalized, not differentiated.
- CAP2-v0 is the novelty hypothesis to test, compare, and either kill or promote.
