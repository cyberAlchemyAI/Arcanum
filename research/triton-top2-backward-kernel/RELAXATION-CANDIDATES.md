# Relaxation Candidates - Continuous Top-2 Routing

Purpose: gather more data about the core challenge choice: what continuous
relaxation should replace or approximate hard `Top2` so the backward pass is
mathematically meaningful and testable.

Checked: 2026-06-12

## Source Records

| Source | Signal For This Challenge |
| --- | --- |
| Xie et al., "Differentiable Top-k Operator with Optimal Transport", NeurIPS 2020, https://arxiv.org/abs/2002.06504 | Top-k is discontinuous as an indicator map; SOFT top-k relaxes it through entropic optimal transport. Strong mathematical fit, heavier kernel fit. |
| Sander et al., "Fast, Differentiable and Sparse Top-k: a Convex Analysis Perspective", ICML 2023, https://arxiv.org/pdf/2302.01425 | Sparse differentiable top-k operators, directly aligned with "top-2 but differentiable." Strong candidate if sparse exactness matters. |
| Martins & Astudillo, "From Softmax to Sparsemax", ICML 2016, https://utstat.utoronto.ca/droy/icml16/publish/martins16.pdf | Sparsemax gives sparse probability mappings with exact zeros. Not top-2-specific, but simple and proof-friendly. |
| Peters et al., "Sparse Sequence-to-Sequence Models", ACL 2019, https://aclanthology.org/P19-1146/ | Entmax family includes softmax/sparsemax and supports sparse probabilities. Useful middle ground for differentiable sparse routing. |
| Petersen et al., "Differentiable Top-k Classification Learning", ICML 2022, https://proceedings.mlr.press/v162/petersen22a/petersen22a.pdf | Differentiable top-k networks and differentiable sorting/ranking context. More classification-loss oriented than router-kernel oriented. |
| Xie/Rolfe et al., "Reparameterizable Subset Sampling via Continuous Relaxations", IJCAI 2019, https://www.ijcai.org/proceedings/2019/0544.pdf | Gumbel/top-k style subset relaxations. Good if stochastic selection is desired; less ideal for deterministic exact backward. |
| Kool et al., "The Gumbel-Top-k Trick for Sampling Sequences Without Replacement", ICML 2019, https://proceedings.mlr.press/v97/kool19a.html | Principled Gumbel top-k sampling without replacement. Sampling focus, not simplest deterministic kernel target. |
| Chi et al., "ReMoE: Fully Differentiable Mixture-of-Experts with ReLU Routing", ICLR 2025, https://arxiv.org/html/2412.14711v1 | MoE-specific alternative: replace `TopK+Softmax` routing with continuous ReLU routing and sparsity regularization. Strong conceptual fit if challenge allows changing router form. |
| "Mixture-of-Experts with Expert Choice Routing", NeurIPS 2022, https://openreview.net/forum?id=jdJo1HIVinI | Capacity/load can be handled by experts choosing tokens instead of tokens choosing experts. Solves a different routing problem; useful boundary case. |
| BASE Layers, https://arxiv.org/pdf/2103.16716 | Balanced assignment approach for sparse experts. Strong load-balancing idea, but assignment is a harder optimization route. |

## Candidate Families

### C1 - Fixed-Mask Top2 Backward

```text
Forward: hard top-2 indices M are selected and saved.
Backward: M is treated as constant.
A = M * softmax(Z)
```

What it solves:

- Gives a clear exact backward for the post-selection graph.
- Easy PyTorch reference.
- Easy Lean proof target.
- Most Triton-friendly first kernel.

What it does not solve:

- Does not differentiate through the selection event.
- May not satisfy the prompt if the hidden challenge expects choosing a continuous relaxation.

Verdict: best baseline, not best final answer if continuous relaxation is required.

### C2 - Soft Routing

```text
A = softmax(Z)
Y = sum_j A_j * H_j
```

What it solves:

- Fully differentiable.
- Easiest to prove and test.
- Good sanity oracle.

What it does not solve:

- Not sparse.
- Does not approximate top-2 strongly unless temperature/sharpening is added.
- Can be expensive if every expert is evaluated.

Verdict: best oracle/reference, weak match to "Top2".

### C3 - Temperature Soft Top-2 Mask

Approximate the top-2 selection with a smooth gate such as a sharpened softmax,
sigmoid threshold, or product of soft comparisons.

Example direction:

```text
A_j = softmax(Z / tau)_j
```

or a top-2-shaped variant:

```text
A_j = P_j * soft_indicator(score_j is in top2; tau)
```

What it solves:

- Simple to implement.
- Kernel-friendly.
- TDD-friendly.

What it risks:

- The exact relaxation must be invented or selected carefully.
- May not be truly 2-sparse.
- As `tau -> 0`, gradients can become unstable.

Verdict: best engineering candidate if the challenge rewards implementability.

### C4 - Sparsemax / Entmax Routing

```text
A = sparsemax(Z)
```

or:

```text
A = entmax_alpha(Z)
```

What it solves:

- Continuous sparse probability mapping.
- Can produce exact zeros.
- Has known Jacobian structure.
- More proof/test friendly than optimal-transport top-k.

What it risks:

- Sparsity level is not guaranteed to be exactly 2.
- Requires projection/threshold logic.

Verdict: best sparse differentiable probability-map candidate, but not exact Top2.

### C5 - SOFT Top-k via Entropic Optimal Transport

SOFT top-k approximates top-k as an entropic optimal transport problem.

What it solves:

- Directly targets differentiable top-k.
- Strong literature fit.
- Produces a smoothed approximation of the top-k indicator.

What it risks:

- Heavier algorithmic machinery.
- Backward may require solving/approximating OT optimality conditions.
- Harder to make a zero-allocation FP16 Triton kernel.

Verdict: best literature-pure top-k relaxation, likely too heavy for first kernel.

### C6 - Fast Sparse Differentiable Top-k / Convex Top-k

Uses convex-analysis/top-k operators that are differentiable and sparse.

What it solves:

- Directly top-k-shaped.
- Sparse by construction.
- More appropriate than soft routing if exact sparsity matters.

What it risks:

- Requires implementing nontrivial threshold/projection logic.
- Need to inspect exact operator and Jacobian before claiming Triton feasibility.

Verdict: best final candidate if the challenge demands "continuous top-2" and still wants sparsity.

### C7 - Gumbel / Reparameterized Subset Top-k

```text
A = RelaxedTopK(Z + Gumbel noise; tau)
```

What it solves:

- Differentiable stochastic subset selection.
- Good for sampling without replacement and stochastic exploration.

What it risks:

- Adds randomness.
- "Exact backward" becomes exact for a stochastic relaxation/estimator, not a deterministic objective.
- Harder to make deterministic test goldens.

Verdict: useful if stochastic routing is intended; not the safest challenge answer.

### C8 - ReLU Routing / Fully Differentiable MoE

Replace top-k router with a continuous sparse-ish activation:

```text
gate_j = relu(z_j)
```

with sparsity/load regularization.

What it solves:

- MoE-specific and fully differentiable.
- Avoids hard `TopK+Softmax` discontinuity.
- Likely easier kernel than OT top-k.

What it risks:

- It changes the router away from Top2.
- May not match the prompt if "Top2" must remain structurally present.

Verdict: best MoE-specific alternative if the challenge allows redefining the router.

## Scored Decision Matrix

Scale: 1 poor, 5 strong.

| Candidate | Matches Top2 | Differentiable | Sparse | Triton Feasible | Easy To Prove/Test | Handles Capacity | Overall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C1 Fixed-mask | 4 | 2 | 5 | 5 | 5 | 2 | 23 |
| C2 Soft routing | 1 | 5 | 1 | 5 | 5 | 2 | 19 |
| C3 Temperature soft top-2 | 3 | 4 | 2 | 5 | 4 | 2 | 20 |
| C4 Sparsemax/Entmax | 2 | 4 | 4 | 4 | 4 | 2 | 20 |
| C5 SOFT Top-k OT | 5 | 5 | 3 | 2 | 3 | 3 | 21 |
| C6 Convex sparse top-k | 5 | 5 | 5 | 3 | 3 | 3 | 24 |
| C7 Gumbel relaxed top-k | 4 | 4 | 3 | 3 | 2 | 2 | 18 |
| C8 ReLU MoE routing | 1 | 5 | 3 | 5 | 4 | 3 | 21 |

## Recommendation

Use a two-track strategy:

### Track A - Rigor Baseline

Implement/test/prove fixed-mask Top2 backward.

Purpose:

- establish the exact backward equations;
- create a reference and TDD scaffold;
- avoid hallucinating gradients through hard selection.

### Track B - Challenge Candidate

Evaluate C6 convex sparse differentiable top-k and C4 entmax/sparsemax as the
main continuous-relaxation candidates.

Why:

- C6 best matches "continuous relaxation of Top2";
- C4 is simpler and may be easier to implement;
- C3 is the fallback if kernel simplicity dominates.

## Next Data To Collect

1. Exact formula and Jacobian for the chosen C6 operator.
2. Whether C6 can be implemented row-wise without full `[T, E]` intermediate tensors.
3. Whether top-2 exact sparsity is required, or sparse-ish routing is acceptable.
4. Whether capacity is part of the differentiable objective or only a gate.
5. Whether the challenge accepts changing `Top2` to a named relaxation.

## Current Best Answer To The Challenge

The strongest rigorous answer is:

```text
We implement exact backward for a named continuous top-2 relaxation.
We keep a fixed-mask Top2 implementation as the baseline oracle.
We reject any claim of exact gradients through hard Top2 itself.
```

The best first named candidates are:

1. convex sparse differentiable top-k;
2. entmax/sparsemax if exact k-sparsity is not required;
3. temperature soft top-2 if Triton simplicity dominates.
