# Prior Art Map - Continuous Top-2 / Sparse Routing

Purpose: explain the known solution families before trying to invent a novel
one. This is not a complete literature review; it is the practical map needed to
avoid embarrassing overclaims.

Checked: 2026-06-12

## Plain Meaning Of Prior Art

Prior art means: "What have other people already done that is close to this?"

For this challenge, prior art tells us:

- hard `Top2` being nondifferentiable is already known;
- differentiable top-k relaxations already exist;
- sparse differentiable probability maps already exist;
- MoE routers with different load-balancing strategies already exist;
- our novelty, if any, must be more specific than "make Top2 differentiable."

## Prior-Art Families

### P1 - Fixed-Mask / Stop-Gradient Top-k

Basic idea:

```text
Forward chooses top-k.
Backward treats the chosen mask as constant.
```

Why it matters:

- It is practical and easy to test.
- It gives exact gradients after the selection.
- It does not solve differentiating through selection.

Novelty warning:

Do not claim this as new. It is a common engineering pattern.

### P2 - Dense Soft Routing

Basic idea:

```text
A = softmax(scores)
Y = sum_j A_j expert_j(X)
```

Why it matters:

- Fully differentiable.
- Easy reference oracle.
- Not sparse, so it may violate the efficiency spirit of Top2.

Novelty warning:

Soft mixtures are very old. Novelty would need to be in a special constraint,
kernel, or training procedure, not in soft routing itself.

### P3 - Sparse Probability Maps: Sparsemax / Entmax

Basic idea:

Replace softmax with a sparse transformation that can assign exact zero
probability to some routes.

Prior art:

- Sparsemax: Martins & Astudillo, 2016.
- Entmax: Peters et al., 2019.

Why it matters:

- Differentiable almost everywhere.
- Sparse but not necessarily exactly top-2.
- Easier to reason about than heavy top-k relaxations.

Novelty opening:

A kernel-friendly, capacity-aware entmax-like router specialized for top-2-ish
MoE could be interesting, but the sparse probability family itself is prior art.

### P4 - Differentiable Top-k Via Optimal Transport

Basic idea:

Relax top-k into an entropic optimal transport problem.

Prior art:

- SOFT top-k: Xie et al., 2020.

Why it matters:

- Directly targets top-k.
- Mathematically serious.
- Heavier to implement as a zero-allocation Triton backward kernel.

Novelty opening:

A simplified or approximate OT-top2 backward that is row-local and FP16-friendly
could be interesting, but would need careful comparison.

### P5 - Convex Sparse Differentiable Top-k

Basic idea:

View top-k through convex geometry and regularization to produce sparse,
differentiable top-k-like outputs.

Prior art:

- Sander et al., 2023, "Fast, Differentiable and Sparse Top-k."

Why it matters:

- Strongest match to "continuous relaxation of Top2."
- Sparse and differentiable.
- Used in contexts including sparse MoE routing.

Novelty opening:

The most promising novelty zone is adapting this family to a zero-allocation
Triton backward pass with capacity/load terms and a clean test/proof story.

### P6 - Gumbel / Stochastic Relaxed Top-k

Basic idea:

Use noise and a reparameterized relaxation to sample or approximate top-k subsets.

Prior art:

- Gumbel-Top-k and relaxed subset sampling papers.

Why it matters:

- Good for stochastic exploration.
- Harder to use for deterministic exact-backward challenge tests.

Novelty opening:

Less promising unless the challenge wants stochastic routing.

### P7 - MoE-Specific Continuous Routers

Basic idea:

Stop trying to smooth Top2 directly; replace the router with a continuous
activation or different routing rule.

Prior art:

- ReMoE uses ReLU routing as a differentiable alternative to TopK+Softmax.
- Expert Choice Routing changes who selects whom: experts choose tokens.
- BASE Layers use balanced assignment.

Why it matters:

- These approaches attack MoE routing and load balancing directly.
- Some are more capacity-aware than generic top-k relaxations.

Novelty opening:

A new continuous router that preserves the spirit of Top2 while being
capacity-aware, row-local, and Triton-friendly could be a real idea. It must be
compared against ReMoE, Expert Choice, BASE, and differentiable top-k relaxations.

## What Is Already Taken

Do not claim novelty for:

- noticing hard top-k is nondifferentiable;
- using softmax as a differentiable mixture;
- using sparsemax/entmax to get sparse probabilities;
- using optimal transport to relax top-k;
- using convex differentiable sparse top-k;
- using Gumbel noise for relaxed subset selection;
- replacing MoE TopK+Softmax with a continuous router in general.

## What Might Still Be Novel

These are plausible openings:

1. **Kernel-native relaxation**
   A relaxation designed from the start for zero-allocation Triton backward:
   row-local, low-branching, FP16-stable, and no full intermediate tensors.

2. **Capacity-aware continuous top-2**
   A relaxation that includes the `max(f_j) <= 2.1/E` pressure directly, without
   a separate hard routing/projection step.

3. **Two-level relaxation**
   A smooth "candidate set" gate plus a sparse exact-in-candidate mixture, giving
   better gradients than fixed-mask but cheaper math than OT top-k.

4. **Proof-first relaxation**
   A relaxation whose backward equations are simple enough for Lean proof and
   direct Triton implementation.

5. **Load-balanced sparse router for small k**
   A top-2-specific operator, not generic top-k, that exploits `k=2` for simpler
   math and kernels.

## Novelty Test

Before calling an idea novel, ask:

1. Is it just softmax, sparsemax, entmax, SOFT top-k, convex top-k, Gumbel top-k,
   ReLU routing, expert choice, or balanced assignment with new words?
2. Does it define a precise forward operator?
3. Does it define exact backward for that operator?
4. Does it improve one axis: proof simplicity, kernel simplicity, capacity
   handling, FP16 stability, or testability?
5. Can it be compared against at least three baselines?

If the answer to #1 is yes and #4 is no, it is not novel yet.

## Best Prior-Art Baselines For Our Challenge

Use these as the minimum comparison set:

| Baseline | Why |
| --- | --- |
| Fixed-mask Top2 | Practical baseline and easy oracle. |
| Soft routing | Fully differentiable lower-complexity sanity check. |
| Entmax/sparsemax | Sparse differentiable probability baseline. |
| Convex sparse top-k | Strongest direct prior-art competitor. |
| ReLU routing / ReMoE | Strong MoE-specific continuous-router competitor. |
