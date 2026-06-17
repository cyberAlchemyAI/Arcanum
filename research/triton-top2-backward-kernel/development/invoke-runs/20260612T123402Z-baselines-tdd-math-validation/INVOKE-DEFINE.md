# Invoke Define - Baselines, TDD, Math Validation

Run id: `20260612T123402Z-baselines-tdd-math-validation`

Status: `pass`

## Objective

Define the governed work needed to move from research tower to rigorous
implementation readiness for the Top2/Triton challenge.

The work must cover:

- baselines;
- TDD;
- math validation;
- prior-art comparison;
- CAP2 novelty hypothesis;
- implementation gates;
- non-overclaiming boundaries.

## Problem Statement

We need to solve or responsibly approach:

```text
Implement a zero-allocation Triton kernel executing the exact backward pass for:
W ||X - Top2(sigma(X W^T)) * FFN(X)||^2
  + gamma * E * sum_j(f_j * P_j)
subject to max_j(f_j) <= 2.1 / E

Optimized for FP16 precision, bypassing non-differentiable selection via continuous relaxation.
```

The challenge mixes:

- hard `Top2`, which is nondifferentiable;
- a request for exact backward;
- a continuous-relaxation requirement;
- MoE-style load balancing;
- capacity constraints;
- FP16/Triton systems constraints.

## Ground Truth From Current Research

### Safe V0 Baseline

```text
sigma = softmax
lambda_rec = scalar reconstruction weight
H = precomputed expert outputs
M = saved top-2 mask from forward
A = M * P
f_j = fixed hard load, no gradient through f
capacity = checked/flagged, not differentiated
```

Allowed claim:

```text
Exact backward for the fixed-mask post-selection graph.
```

Forbidden claim:

```text
Exact backward through hard Top2 selection.
```

### Novelty Hypothesis

Working name:

```text
CAP2: Capacity-Aware Pairwise Relaxation for Top-2 Routing
```

CAP2 is not a solution yet. It is a design hypothesis that may either become a
precise operator or be killed as prior-art-equivalent.

## Baseline Set

Minimum baselines:

| Baseline | Role |
| --- | --- |
| Fixed-mask Top2 | Rigorous V0 oracle. |
| Soft routing | Fully differentiable sanity baseline. |
| Sparsemax/entmax | Sparse differentiable probability baseline. |
| Convex sparse top-k | Strongest direct prior-art competitor. |
| ReLU routing / ReMoE | MoE-specific continuous-router competitor. |

Optional/heavier baselines:

- SOFT top-k via optimal transport;
- Gumbel relaxed top-k;
- balanced assignment / expert choice when capacity dominates.

## Math Validation Scope

Formal proof targets for V0:

- softmax row derivative;
- reconstruction gradient into `A`;
- fixed-mask gradient into `P`;
- auxiliary gradient into `P` when `f_j` is fixed;
- router weight gradient `dW = dZ^T X`;
- router input gradient `dX_router = dZ W`.

Non-theorems:

- hard Top2 selection gradient;
- CAP2 correctness before CAP2 exists;
- FP16 numerical correctness;
- Triton zero-allocation behavior;
- capacity gradients without a differentiable penalty/barrier.

## Done Criteria

This phase is done when:

1. V0 baseline has a PyTorch reference and tests.
2. V0 gradient identities have either formal proof targets or Lean stubs.
3. CAP2 has a precise design spec or is killed.
4. At least three baselines are runnable in reference form.
5. Triton implementation is gated behind reference parity.
6. Every novelty claim has a prior-art comparison.

## Non-Goals

- Do not write Triton before reference tests.
- Do not claim novelty for fixed-mask Top2.
- Do not claim exact gradients through hard Top2.
- Do not fold full FFN backward into V0.
- Do not optimize FP16 before semantic parity.
