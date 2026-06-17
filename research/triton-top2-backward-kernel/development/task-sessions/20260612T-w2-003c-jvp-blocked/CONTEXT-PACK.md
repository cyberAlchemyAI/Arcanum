# Context Pack - TASK-W2-003C JVP/Backward Gate

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003C`
Objective: Add differentiable/JVP-backed convex sparse top-k parity or blocked
report.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W2-003C` as the next ready task and accepts either
  source-backed backward/JVP parity or an explicit blocked report.
- `CONVEX-SPARSE-TOPK-RESEARCH-PACK.md`: selects the official sparse soft top-k
  PAV mask path as the source-backed prior-art target.
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`: records that the local extraction covers
  the forward mask only and does not claim source-backed PyTorch/custom-JVP
  backward behavior.
- `development/task-sessions/20260612T-w2-003b-router-composition/RESULT.md`:
  records the selected router compositions and defers differentiable parity to
  this task.

## Gate Checks

- Dependency gate: pass. `TASK-W2-003B` passed.
- Semantic gate: pass. No hard Top2 differentiability claim may be introduced.
- Source-backed backward gate: block. The tower lacks an extracted VJP/JVP
  contract for the PAV partition operation.
- Validation path: pass for existing forward/reference tests; blocked for
  differentiable parity tests.

## Decision Pack

No user decision is needed in this task-session. The blocker is missing
source-backed derivative evidence, not an unresolved preference between safe
implementation options.

## Write Scope

- `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md`
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- task-session evidence folder
