# Decision Gate - W3-003 CAP2 Kill/Promote/Defer

Date: 2026-06-12

## Target Scope

`TASK-W3-003`: Kill/promote/defer CAP2.

## Blocked Work

The work-pack cannot choose a selected relaxation for later Triton work until
CAP2-v0 is explicitly killed, promoted as a candidate, or deferred.

## Evidence

Primary comparison artifact:

```text
CAP2-PRIOR-ART-COMPARISON.md
```

Summary:

- CAP2-v0 is differentiable under fixed load.
- CAP2-v0 responds to capacity pressure in the intended direction.
- CAP2-v0 has lower fixture loss than sparsemax, normalized ReLU, and
  normalized selected-pair comparisons on the shared fixture.
- CAP2-v0 does not provide exact 2-sparsity on the shared fixture.
- CAP2-v0 may be close to known soft-rank / NeuralSort-style relaxations.
- CAP2-v0 has no Triton or zero-allocation implementation yet.

## Decision Question

What should happen to CAP2-v0?

## Options

### Option 1 - Promote As Candidate Only

Benefit: keeps CAP2-v0 alive for Triton feasibility and broader comparison while
preserving honest non-claims.

Cost or risk: future work must keep saying "candidate," not "novel solution,"
until stronger prior-art and systems evidence exists.

When to choose: choose this if capacity awareness and differentiability are
valuable enough to keep testing.

Downstream impact: W3 can mark CAP2 promoted as candidate; W6 may later evaluate
selected relaxation implementation after W5 GPU/Triton baseline exists.

### Option 2 - Defer CAP2

Benefit: preserves the reference without spending immediate effort on it.

Cost or risk: later Triton relaxation choice remains less resolved.

When to choose: choose this if formal math or fixed-mask Triton work matters
more now than CAP2 exploration.

Downstream impact: CAP2 remains a documented candidate, but later waves should
not depend on it until reopened.

### Option 3 - Kill CAP2-v0

Benefit: avoids spending more time on a candidate that is not exact 2-sparse and
may be too close to known soft-rank relaxations.

Cost or risk: loses the capacity-aware relaxation hypothesis and narrows future
work to fixed-mask or prior-art relaxations.

When to choose: choose this if exact top-2 sparsity or clear novelty is required
before promotion.

Downstream impact: W6 should not implement CAP2-v0; final report records it as
tested and rejected.

### Standing Option - Explain / More Context

Non-committal. Does not resolve the gate.

## Recommended Option

Option 1 - Promote as candidate only.

Rationale: CAP2-v0 has enough evidence to remain useful, but not enough evidence
to claim novelty or final selection.

## Selected Option

Option 1 - Promote as candidate only.

## Rationale

User selected `1`.

This keeps CAP2-v0 alive because it is differentiable under fixed load, responds
to capacity pressure, and is distinct enough from the local sparsemax/ReLU/
convex-top-k fixture behavior to merit later testing. It does not promote CAP2
to a novelty claim or final solution.

## Remaining Blockers

None for `TASK-W3-003`.

## Deferred Decisions

- Whether CAP2-v0 is novel.
- Whether CAP2-v0 should be implemented in Triton.
- Whether dynamic load gradients are worth adding.
