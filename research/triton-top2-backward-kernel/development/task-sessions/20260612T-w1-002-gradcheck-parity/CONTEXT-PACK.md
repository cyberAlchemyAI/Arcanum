# Context Pack - TASK-W1-002 Gradcheck Parity

Date: 2026-06-12

## Task Scope

Task: `TASK-W1-002`
Objective: Add gradcheck and finite-difference parity for the V0 fixed-mask
PyTorch reference.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W1-002` depends on passed `TASK-W1-001`.
- `reference/router_reference.py`: manual backward and finite-difference `dW`
  oracle.
- `reference/router_torch.py`: PyTorch fixed-mask objective.
- `tests/test_router_torch.py`: PyTorch parity surface.

## Gates

- Dependency gate: pass. `TASK-W1-001` is passed.
- Semantic gate: pass. Gradcheck is applied only to the fixed-mask smooth graph,
  not to hard Top2 selection.
- GPU gate: not applicable.

## Decisions

- Gradcheck `W` and `H`, because those are the parameters already covered by the
  V0 fixed-mask backward surface.
- Compare autograd `dW` directly with the standard-library finite-difference
  oracle.
- Keep system Python tolerant of missing torch by skipping PyTorch tests there.
