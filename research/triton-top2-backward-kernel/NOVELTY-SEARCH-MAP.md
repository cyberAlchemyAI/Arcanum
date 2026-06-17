# Novelty Search Map

Purpose: give the operator a fair shot at inventing something without drifting
into renamed prior art.

## Starting Point

The challenge probably wants us to choose a continuous relaxation. Prior art
already has many relaxations. So our possible novelty is not:

```text
"make top-k differentiable"
```

Our possible novelty is more like:

```text
"choose/design a relaxation that is especially good for exact backward,
capacity-aware routing, and zero-allocation FP16 Triton."
```

## Design Axes

A new candidate should pick positions on these axes:

| Axis | Options |
| --- | --- |
| Sparsity | dense, sparse-ish, exactly k-sparse |
| Determinism | deterministic, stochastic |
| Capacity handling | none, auxiliary loss, penalty, barrier, assignment, built-in balancing |
| Kernel shape | row-local, needs global expert state, needs iterative solve |
| Proof shape | simple closed-form Jacobian, piecewise proof, implicit differentiation |
| Training behavior | smooth early/sharp late, always sparse, adaptive sparsity |
| Inference match | same as training, hard top-2 at inference, annealed to top-2 |

## Candidate Novel Directions

### N1 - Top2-Calibrated Entmax

Idea:

Use an entmax/sparsemax-style map, but adapt its sparsity parameter or threshold
so the expected active expert count is near 2.

Why it might be novel:

- Not generic entmax; targeted to top-2 routing.
- Could be simpler than convex top-k and more sparse than softmax.

Risk:

- Adaptive entmax/sparsemax variants may already exist.
- Exact 2-sparsity may not be guaranteed.

Test:

Compare active expert count, gradient stability, and Triton simplicity against
entmax and convex sparse top-k.

### N2 - Capacity-Aware Top2 Barrier Gate

Idea:

Add a smooth load pressure directly into the gate:

```text
score'_tj = score_tj - beta * smooth_overload_j
A = relaxed_top2(score')
```

where `smooth_overload_j` approximates whether expert `j` is above capacity.

Why it might be novel:

- The relaxation is not just local top-2; it couples routing to capacity.

Risk:

- Requires global or batch-level state, harder for zero-allocation kernels.
- Could resemble existing load-balancing losses or assignment methods.

Test:

Measure whether it reduces capacity violations better than Switch-style
auxiliary loss without harming parity/testability.

### N3 - Two-Stage Smooth Candidate Then Exact Sparse Mixture

Idea:

Use a smooth gate to choose a soft candidate region, then compute a cheap
two-expert mixture inside that region.

Why it might be novel:

- It tries to balance gradient flow and top-2 efficiency.
- Could be more kernel-friendly than OT.

Risk:

- Might collapse into straight-through top-2 if not carefully defined.

Test:

Check whether gradients flow to near-miss experts and whether the final forward
remains sparse.

### N4 - Proof-First Top2 Relaxation

Idea:

Design the relaxation by starting from what can be proved simply:

- closed-form forward;
- closed-form Jacobian;
- row-local operations;
- no iterative solve;
- simple FP16 stabilization.

Why it might be novel:

- Most prior art optimizes modeling behavior first; this optimizes proof plus
kernel implementability.

Risk:

- May be too simple and underperform.

Test:

Lean proof complexity, PyTorch gradcheck, Triton parity, and baseline quality.

### N5 - K=2-Specific Convex Relaxation

Idea:

Use the fact that `k=2` is fixed. Avoid generic top-k machinery and derive a
simpler pair-selection relaxation.

Why it might be novel:

- Most top-k prior art handles general `k`.
- A top-2-only operator might have simpler backward and faster Triton code.

Risk:

- Need to ensure it is not just a special case of existing convex sparse top-k.

Test:

Prove or empirically show lower complexity than generic convex top-k while
matching its behavior for `k=2`.

## Best First Novelty Attempt

The most promising first idea is:

```text
K=2-specific, proof-first, capacity-aware sparse relaxation.
```

Working name:

```text
CAP2: Capacity-Aware Pairwise Relaxation for Top-2 Routing
```

Do not claim this as novel yet. Treat it as a hypothesis.

Minimum definition needed:

1. forward operator;
2. exact backward/Jacobian;
3. capacity/load term;
4. proof target;
5. PyTorch reference;
6. comparison against fixed-mask, entmax/sparsemax, convex top-k, and ReLU routing.

## Novelty Claim Template

Use this only after evidence exists:

```text
We propose <operator>, a <deterministic/stochastic> continuous relaxation for
top-2 MoE routing. Unlike <prior art A/B>, it is designed for <specific axis:
zero-allocation Triton backward / capacity-aware routing / proof simplicity>.
We validate it against <baselines> using <tests/proofs/benchmarks>.
```

## Stop Conditions

Stop calling an idea novel if:

- it is equivalent to entmax/sparsemax after reparameterization;
- it is equivalent to convex sparse top-k for `k=2`;
- it needs an iterative global solve but claims to be simple/zero-allocation;
- it cannot define exact backward;
- it only changes names, not math or implementation properties.
