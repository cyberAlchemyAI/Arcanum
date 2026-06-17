# Context Pack - TASK-W6-001A CAP2 Reference VJP

Task: `TASK-W6-001A`
Mode: lean

## Objective

Implement a manual/reference VJP for the exact backward of the smooth CAP2-v0
graph with fixed load, before any Triton CAP2 kernel work.

## Controlling Sources

- `development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/WORK-PACK-W6-CAP2.md`
  selects `TASK-W6-001A` as ready and keeps later Triton tasks pending on it.
- `development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/INVOKE-DEFINE.md`
  defines the fixed-load CAP2 tensor contract and backward formula.
- `development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/INVOKE-PLAN.md`
  requires a manual VJP, autograd parity for `dW`, `dH`, and `dZ`, and finite
  difference parity for `dW`.
- `reference/router_torch.py` contains the existing CAP2 PyTorch forward and
  routing-weight graph.
- `tests/test_router_torch.py` contains CAP2 forward parity and fixed-load
  gradcheck tests.

## Obligations

- Add a bounded `cap2_manual_backward` helper for the named CAP2-v0 smooth graph.
- Treat `load`, `f`, temperatures, and scalar hyperparameters as fixed inputs.
- Return the required backward outputs: `dW`, `dX_router`, and `dH`; expose
  `dZ` for downstream Triton parity.
- Validate against PyTorch autograd for `dW`, `dH`, and `dZ`.
- Validate `dW` against finite differences.
- Do not start Triton CAP2 work in this task.
- Do not claim novelty or exact backward through hard Top2.

## Gate Verdict

Pass. The task has a precise formula, write scope, and local validation surface.
No blocker decision is open.
