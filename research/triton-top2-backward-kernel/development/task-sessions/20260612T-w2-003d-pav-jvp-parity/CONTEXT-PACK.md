# Context Pack - TASK-W2-003D PAV JVP Parity

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003D`
Objective: Extract source-backed PyTorch/custom-JVP parity for convex sparse
top-k PAV.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W2-003D` ready after the user selected option 1
  to implement the narrow parity oracle before CAP2.
- `CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md`: defines the implementation route and
  candidate backward contract.
- `development/decision-gates/20260612T-w2-003d-implement-now/DECISION.md`:
  records the user decision to implement now.
- Official Google Research `sparse_soft_topk/_src/isotonic_pav.py`: source of
  the blockwise custom VJP behavior.
- Existing local forward extraction:
  `reference/router_reference.py::convex_sparse_topk_mask_rows`.

## Gates

- Dependency gate: pass. CPU PyTorch environment is available in `.venv`.
- Decision gate: pass. User selected implement-now.
- Semantic gate: pass. No hard Top2 differentiability claim is introduced.
- Scope gate: pass. Implementation is limited to CPU/PyTorch parity oracle.

## Write Scope

- `reference/router_torch.py`
- `tests/test_router_torch.py`
- `CONVEX-SPARSE-TOPK-JVP-PARITY.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- task-session evidence folder

## Completion Boundary

Success means mask-level source-backed score-gradient parity on non-boundary
fixtures plus direct-mask router forward parity.

Success does not mean Triton readiness, zero-allocation readiness, or full
normalized masked-softmax router backward parity.
