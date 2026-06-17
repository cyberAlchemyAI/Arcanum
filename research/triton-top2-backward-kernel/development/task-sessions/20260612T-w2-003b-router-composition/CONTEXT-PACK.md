# Context Pack - TASK-W2-003B Router Composition

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003B`
Objective: Decide and implement convex sparse top-k router composition.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W2-003B` as blocked by router composition.
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`: extracts `M_relaxed`.
- `CONVEX-SPARSE-TOPK-FIXTURES.md`: defines mask and composition checks.
- User decision: `1 AND 3`.

## Decision

Selected:

```text
A = M_relaxed
A = normalize(M_relaxed * softmax(Z))
```

Not selected:

```text
A = M_relaxed * softmax(Z)
```

## Gates

- Dependency gate: pass. `TASK-W2-003A` passed.
- Decision gate: pass. User selected options 1 and 3.
- Semantic gate: pass. No hard Top2 differentiability claim is introduced.
- Backward gate: deferred. PAV mask custom backward/JVP parity is not claimed.

## Write Scope

- `reference/router_reference.py`
- `tests/test_router_reference.py`
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`
- `CONVEX-SPARSE-TOPK-FIXTURES.md`
- `WORK-PACK.md`
- task-session evidence folder
