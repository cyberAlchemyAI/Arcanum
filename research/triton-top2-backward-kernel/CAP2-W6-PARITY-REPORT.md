# CAP2 W6 Parity Report

Status: `pass-runpod`
Date: 2026-06-14

## Scope

This report closes W6 for the selected relaxation path:

```text
exact backward for the smooth CAP2-v0 graph with fixed load
```

It does not claim exact backward through hard Top2, dynamic-load gradients,
novelty, exact 2-sparsity, production performance, or CAP2 zero-allocation
behavior.

## Implemented Outputs

Reference/manual VJP:

- `d_z`
- `d_x_router = d_z @ W`
- `d_h`
- `d_w = d_z^T @ X`

Triton path:

- row-local CAP2 Triton kernel for `d_z` and `d_h`;
- existing validated Triton matrix kernel for `d_x_router`;
- existing validated Triton reduction kernel for `d_w`.

## Evidence

`TASK-W6-001A`: reference VJP passed local PyTorch/autograd/finite-difference
validation.

- Evidence:
  `development/task-sessions/20260614T073520Z-w6-001a-cap2-reference-vjp/`
- Full local suite: `54 passed, 11 skipped`.

`TASK-W6-001B`: Triton row-local `d_z`, `d_x_router`, and `d_h` passed RunPod
validation.

- Evidence:
  `development/task-sessions/20260614T073920Z-w6-001b-cap2-row-backward/`
- RunPod focused Triton suite: `14 passed`.
- RunPod full suite: `67 passed`.

`TASK-W6-001C`: Triton `d_w` reduction from CAP2 `d_z` passed RunPod
validation.

- Evidence:
  `development/task-sessions/20260614T074112Z-w6-001c-cap2-dw-reduction/`
- RunPod focused Triton suite: `15 passed`.
- RunPod full suite: `68 passed`.

## Acceptance

W6 passes for parity of the selected relaxation backward contract:

- CAP2 manual backward agrees with PyTorch autograd for `d_w`, `d_h`, and `d_z`.
- CAP2 manual `d_w` agrees with finite differences.
- CAP2 Triton backward agrees with the manual reference for `d_z`,
  `d_x_router`, `d_h`, and `d_w` on RunPod.

## Remaining Limits

- CAP2 remains a candidate relaxation only.
- CAP2 is not proven novel.
- CAP2 does not guarantee exact 2-sparsity.
- CAP2 fixed-load backward does not include gradients through dynamic load.
- CAP2 performance has not been benchmarked against the fixed-mask kernels.
- CAP2 zero-allocation behavior has not been measured as a W7 acceptance check.

## Next Task

Proceed to `TASK-W7-003`: benchmark fixed-mask and selected-relaxation paths.
