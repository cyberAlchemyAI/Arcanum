# Decision Gate - TASK-W6-001 Selected Relaxation

## Blocker Question

What should count as the W6 "selected relaxation kernel" for CAP2-v0?

## Option 1 - Forward-Only CAP2 Triton Feasibility

Implement a Triton kernel that computes CAP2-v0 routing weights `A` from logits
and fixed load.

- Benefit: fastest proof that CAP2 has a plausible row-wise Triton path.
- Cost/Risk: does not satisfy exact backward; must be labeled feasibility only.
- Downstream impact: W7 benchmark can compare fixed-mask kernels and CAP2
  forward routing cost, but final report must say CAP2 backward is deferred.

## Option 2 - Exact CAP2 Backward Spec First

Pause W6 implementation and author an implementation-detail spec for exact
CAP2-v0 backward outputs, intermediates, buffers, tolerances, and tests.

- Benefit: most rigorous; avoids embarrassing overclaim.
- Cost/Risk: slower; requires deriving and validating a larger backward graph.
- Downstream impact: W6 remains blocked until the spec exists, but later Triton
  implementation has a precise target.

## Option 3 - Defer CAP2 Triton, Finish Fixed-Mask Track

Defer selected-relaxation Triton work and proceed with fixed-mask-only benchmark
and final report.

- Benefit: fastest path to a complete, honest fixed-mask Triton deliverable.
- Cost/Risk: challenge novelty is weaker; CAP2 remains candidate-only.
- Downstream impact: W7-003 and W8 can finish with explicit limitation notes.

## Recommendation

Option 2 is the rigorous path. It best matches the user's stated goal of not
hallucinating or overclaiming math/kernel correctness.
