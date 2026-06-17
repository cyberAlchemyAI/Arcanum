# Decision Gate - W2-003D Implement PAV JVP Parity Now

Date: 2026-06-12

## Target Scope

`TASK-W2-003D-DG`: Decide whether to implement PAV JVP parity now or defer to
CAP2-v0.

## Blocked Work

`TASK-W2-003D` was blocked by an implementation-ordering decision after the
feasibility gate found a source-backed route for a narrow PyTorch
custom-autograd parity oracle.

## Decision Question

Should the tower implement narrow convex sparse top-k PAV JVP/backward parity
before proceeding to CAP2-v0?

## Considered Options

### Option 1 - Implement Narrow `TASK-W2-003D` Now

Benefit: strongest rigor before CAP2. It gives the tower a source-backed
backward comparison for the strongest direct prior-art relaxation.

Cost or risk: slower than moving directly to CAP2, and still limited to a
CPU/PyTorch oracle rather than a Triton-ready kernel.

Choose when: avoiding hallucinated or weak backward claims matters more than
speed.

Downstream impact: `TASK-W2-003D` becomes the next ready task. CAP2-v0 waits
until this parity oracle is attempted.

### Option 2 - Defer `TASK-W2-003D` And Proceed To `TASK-W3-001`

Benefit: faster novelty exploration and less immediate implementation burden.

Cost or risk: CAP2 comparison remains weaker because convex sparse top-k
backward parity is not available.

Choose when: forward behavior is enough for the next learning pass.

Downstream impact: W3 starts now; `TASK-W2-003D` remains deferred.

### Option 3 - Keep Both Ready And Run CAP2 First

Benefit: preserves the JVP route while still exploring CAP2.

Cost or risk: creates more bookkeeping and can blur whether W3 conclusions are
forward-only or backward-backed.

Choose when: schedule pressure exists but the team does not want to lose the
JVP path.

Downstream impact: CAP2 starts first, with explicit caveats.

### Standing Option - Explain / More Context

Non-committal. Does not resolve the gate.

## Selected Option

Option 1 - Implement narrow `TASK-W2-003D` now.

## Rationale

User selected `1`.

This chooses maximum rigor before CAP2. It makes the next implementation task a
source-backed PyTorch custom-autograd parity oracle for the PAV p=4/3 sparse
top-k mask, limited to non-boundary fixtures and score-gradient validation.

## Source Of Decision

User message on 2026-06-12:

```text
[$decision-gate] ... 1
```

## Remaining Blockers

None for ordering. `TASK-W2-003D` is ready.

Implementation risks remain:

- PAV support-boundary and tie gradients must be skipped or documented.
- The result is CPU/PyTorch parity only, not Triton-ready.
- No gradient should be claimed for `k`, `lambda_smooth`, `p`, or sort indices.

## Deferred Decisions

- Whether to later port this parity path into a Triton-compatible relaxation.
- Whether CAP2 survives comparison after the prior-art backward oracle exists.

## Assumptions

- `TASK-W2-003D` should implement only the narrow route described in
  `CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md`.
- Tests should prioritize source-backed score-gradient parity over broad API
  surface area.
