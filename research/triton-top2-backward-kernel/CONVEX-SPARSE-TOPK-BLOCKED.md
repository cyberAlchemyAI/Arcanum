# Convex Sparse Top-k Baseline Blocker

Status: blocked-before-implementation
Date: 2026-06-12

## Task

`TASK-W2-003`: Add convex sparse top-k baseline or explicit blocked report.

## Blocker

The tower identifies convex sparse differentiable top-k as the strongest
literature match for a continuous Top2 relaxation, but the local artifacts do
not yet contain an implementation-ready operator definition or backward rule.

Implementing it now would risk naming a hand-rolled approximation as prior art.

## Missing Inputs

Before implementation, pin:

1. the exact convex sparse top-k forward operator to implement;
2. the k=2 specialization, if one is allowed;
3. the threshold/projection algorithm;
4. the Jacobian or backward rule needed for parity tests;
5. numerical behavior at support-boundary ties;
6. fixture-level expected outputs for at least one nontrivial row.

## Accepted Substitute For This Wave

The baseline matrix currently has:

- fixed-mask Top2;
- soft routing;
- normalized selected-pair comparison;
- sparsemax;
- normalized ReLU routing.

That is enough to continue local reference work, but not enough to claim CAP2
novelty against convex sparse top-k.

## Unblock Action

Run a focused research/task-session pass on the convex sparse top-k source:

```text
TASK-W2-003A: Extract implementation-ready convex sparse top-k operator.
```

Done criteria:

- source-backed formula;
- CPU reference function;
- tests for simplex/sparsity/top-k-like behavior;
- documented nonsmooth boundary policy.
