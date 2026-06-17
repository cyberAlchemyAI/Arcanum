# Context Pack - TASK-W3-001 CAP2-v0 Reference

Date: 2026-06-12

## Task Scope

Task: `TASK-W3-001`
Objective: Implement CAP2-v0 reference.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W3-001` ready after W1 and W2 reference/parity
  tasks passed.
- `CAP2-CANDIDATE-SPEC.md`: defines CAP2-v0 formula, fixed-load boundary,
  allowed backward claim, and survival criteria.
- `FINAL-QUESTION-RESOLUTION.md`: selects CAP2-v0 as the continuous relaxation
  hypothesis and fixes dynamic load gradients as later scope.
- `OPEN-QUESTIONS-DECISION-LEDGER.md`: requires CAP2 to define forward,
  backward/Jacobian, capacity/load term, support behavior, PyTorch reference,
  and comparisons.

## Gates

- Dependency gate: pass. PyTorch CPU environment is available in `.venv`.
- Semantic gate: pass. No hard Top2 differentiability claim is introduced.
- Scope gate: pass. Fixed load is treated as data, not a dynamic differentiable
  load estimate.
- Novelty gate: not entered. No novelty claim is made.

## Write Scope

- `reference/router_reference.py`
- `reference/router_torch.py`
- `tests/test_router_reference.py`
- `tests/test_router_torch.py`
- `CAP2-REFERENCE.md`
- `CAP2-CANDIDATE-SPEC.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- task-session evidence folder

## Completion Boundary

Success means CAP2-v0 forward values and gradients run in reference tests.

Success does not mean CAP2 is novel, exact 2-sparse, Triton-ready, or preferable
to prior-art baselines.
