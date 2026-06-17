# Decision Gate - W2-003D Feasibility Research Gate

Date: 2026-06-12

## Target Scope

`triton-top2-backward-kernel` route after `TASK-W2-003C`.

## Blocked Work

The tower cannot honestly proceed with differentiable/JVP-backed convex sparse
top-k parity until it decides whether to:

- continue to CAP2-v0 forward comparison now;
- stop and fully extract source-backed PAV JVP/backward parity first;
- run a small feasibility research gate before choosing either larger route.

## Decision Question

After the `TASK-W2-003C` blocked report, what should happen next?

## Considered Options

### Option 1 - Proceed to `TASK-W3-001` CAP2-v0 Reference

Benefit: keeps momentum and tests the candidate novel idea against forward
baselines.

Cost or risk: convex sparse top-k backward remains unresolved, so downstream
claims must avoid differentiable parity or novelty over backward behavior.

Choose when: forward comparison is enough for the next learning step.

Downstream impact: W3 starts immediately; `TASK-W2-003D` remains blocked.

### Option 2 - Stop and Unblock `TASK-W2-003D` First

Benefit: strongest rigor before CAP2 comparison.

Cost or risk: likely slower and harder; may require extracting official JAX
custom VJP behavior, partition derivative behavior, and PyTorch parity tests.

Choose when: exact backward comparison is mandatory before any CAP2 work.

Downstream impact: W3 waits; implementation energy moves into PAV backward
extraction.

### Option 3 - Run a Small Research Gate for `TASK-W2-003D`, Then Decide

Benefit: gathers enough source evidence to estimate difficulty before committing
to either a full JVP extraction or CAP2-first path.

Cost or risk: adds a bounded research step before implementation progress.

Choose when: the team wants rigor without blindly expanding scope.

Downstream impact: add a ready feasibility task before full `TASK-W2-003D`
implementation; W3 waits until that gate reports feasibility.

### Standing Option - Explain / More Context

Non-committal. Does not resolve the gate.

## Selected Option

Option 3 - Run a small research gate for `TASK-W2-003D`, then decide.

## Rationale

User selected `3`.

This is the lowest-regret rigorous path. It protects against hallucinating a
PAV backward formula, but it also avoids prematurely spending a large
implementation pass before we know whether the source-backed derivative
contract can be extracted cleanly.

## Source Of Decision

User message on 2026-06-12:

```text
[$decision-gate] ... 3
```

## Remaining Blockers

- Full differentiable/JVP-backed convex sparse top-k parity remains blocked
  until the feasibility research gate reports an implementable source-backed
  derivative route.
- CAP2 novelty claims still cannot rely on convex sparse top-k backward parity.

## Deferred Decisions

- Whether to fully implement `TASK-W2-003D`.
- Whether CAP2 comparison should proceed before convex sparse top-k backward
  parity.

## Assumptions

- The feasibility gate is research-only and should not mutate reference
  implementation code.
- The feasibility gate should prefer primary sources and official
  implementation evidence.
