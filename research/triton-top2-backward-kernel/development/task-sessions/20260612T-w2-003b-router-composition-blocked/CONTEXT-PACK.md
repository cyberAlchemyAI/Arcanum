# Context Pack - TASK-W2-003B Router Composition

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003B`
Objective: Decide and implement convex sparse top-k router composition.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W2-003B` as `blocked-by-decision`.
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`: extracts only the relaxed mask operator
  and explicitly leaves composition undecided.
- `CONVEX-SPARSE-TOPK-FIXTURES.md`: validates the mask, not the router combine.
- `development/task-sessions/20260612T-w2-003a-convex-topk-extraction/DECISION-GATE.md`:
  records the three viable composition options.

## Gate Verdict

BLOCK. Implementing this task requires choosing how the relaxed mask becomes the
router combine weights.

## Options

1. `A = M_relaxed`
2. `A = M_relaxed * softmax(Z)`
3. `A = normalize(M_relaxed * softmax(Z))`

Recommended first implementation:

```text
A = M_relaxed * softmax(Z)
```

Reason: it is the closest analog to the current fixed-mask baseline.
