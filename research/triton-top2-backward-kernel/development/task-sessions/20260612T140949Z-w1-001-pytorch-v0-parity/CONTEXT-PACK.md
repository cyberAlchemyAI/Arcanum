# Context Pack - TASK-W1-001 PyTorch V0 Parity

Date: 2026-06-12

## Task Scope

Task: `TASK-W1-001`
SWU: `SWU-W1-001`
Objective: Port the V0 fixed-mask reference to PyTorch tensors and autograd.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W1-001` ready after `TASK-W0-005`.
- `reference/router_reference.py`: standard-library oracle for fixed-mask forward
  and manual backward.
- `tests/test_router_reference.py`: existing finite-difference and contract tests.
- `TOOLING-PLAN.md`: CPU PyTorch is enough for W1; Triton/GPU is only required
  for W5-W7.

## Gates

- Dependency gate: pass. Tower-local `.venv` has `torch 2.12.0+cpu`.
- Semantic gate: pass. The saved Top2 mask remains fixed input data and is not
  treated as differentiable.
- Triton gate: not applicable. No Triton kernel is introduced in this task.

## Write Scope

- Add a PyTorch reference module under `reference/`.
- Add PyTorch parity tests under `tests/`.
- Synchronize `WORK-PACK.md`, `README.md`, `TOWER.md`, and this task-session
  evidence folder.

## Decisions

- Use the standard-library implementation as the oracle instead of replacing it.
- Validate `dW` and `dH` against the manual backward oracle through PyTorch
  autograd.
- Keep the mask tensor as fixed data with `requires_grad=False`.
- Skip PyTorch tests under non-torch runners instead of making system Python
  require torch.

## Done Criteria

- PyTorch forward values match the standard-library oracle.
- PyTorch autograd `dW` matches manual `dW`.
- PyTorch autograd `dH` matches manual `dH`.
- Mask non-differentiability is preserved.
- Tests pass in the tower-local venv, and standard-library discovery remains
  usable when torch is unavailable.
