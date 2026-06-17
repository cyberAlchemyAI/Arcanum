# Context Pack - TASK-W6-001B CAP2 Row Backward

Task: `TASK-W6-001B`
Mode: lean

## Objective

Implement CAP2 Triton row-local backward for `dZ`, `dX_router`, and `dH`, using
the passed W6A manual reference as oracle.

## Controlling Sources

- `development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/WORK-PACK-W6-CAP2.md`
  marks `TASK-W6-001B` ready after `TASK-W6-001A`.
- `development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/INVOKE-DEFINE.md`
  defines the smooth CAP2-v0 backward formulas with fixed load.
- `reference/router_torch.py` exposes `cap2_manual_backward`.
- `reference/router_triton.py` contains the existing fixed-mask Triton kernels
  and reusable `dX_router = dZ @ W` path.
- `tests/test_router_triton.py` is the RunPod-gated CUDA/Triton parity surface.

## Obligations

- Compute row-local CAP2 `dZ` in Triton.
- Compute CAP2 `dH` in Triton.
- Produce `dX_router` using validated Triton matrix multiplication.
- Compare all three outputs against W6A manual reference.
- Do not implement or mark CAP2 `dW` in this task.

## Gate Verdict

Pass. Dependencies are met and RunPod validation is available.
