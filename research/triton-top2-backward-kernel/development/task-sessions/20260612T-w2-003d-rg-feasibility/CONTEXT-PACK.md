# Context Pack - TASK-W2-003D-RG Feasibility Research Gate

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003D-RG`
Objective: Run a bounded feasibility research gate for convex sparse top-k PAV
JVP/backward extraction.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W2-003D-RG` ready after the user selected the
  research-first decision.
- `development/decision-gates/20260612T-w2-003d-research-gate/DECISION.md`:
  records selected option 3, a bounded research gate before full implementation.
- `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md`: lists missing derivative inputs that
  blocked `TASK-W2-003C`.
- Official Google Research sparse soft top-k sources:
  - `sparse_soft_topk/_src/topk.py`
  - `sparse_soft_topk/_src/isotonic_pav.py`
  - `sparse_soft_topk/tests/topk_test.py`
  - `sparse_soft_topk/README.md`
- Sander et al., ICML 2023 paper page.

## Gates

- Dependency gate: pass. `TASK-W2-003C` produced the blocked report and the user
  selected this research gate.
- Semantic gate: pass. No hard Top2 differentiability claim is introduced.
- Source gate: pass. Official implementation exposes a custom VJP path for the
  PAV isotonic operator.
- Implementation gate: not entered. This task is research-only.

## Write Scope

- `CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md`
- `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- task-session evidence folder

## Decision State

This task resolves feasibility, not the next implementation choice. A downstream
decision remains: implement narrow PyTorch PAV JVP parity now, or defer it and
resume CAP2-v0 forward work.
