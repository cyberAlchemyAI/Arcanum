# Context Pack - TASK-W6-001C CAP2 dW Reduction

Task: `TASK-W6-001C`
Mode: lean

## Objective

Wire CAP2 `dZ` into the validated Triton `dW = dZ^T @ X` reduction and compare
CAP2 `dW` against the W6A manual reference.

## Controlling Sources

- `WORK-PACK-W6-CAP2.md` marks `TASK-W6-001C` ready after W6B.
- `TASK-W6-001A` provides `cap2_manual_backward` as the reference oracle.
- `TASK-W6-001B` provides Triton CAP2 `d_z`.
- `fixed_mask_dw_triton` is already validated as the generic `dZ^T @ X`
  reduction kernel.

## Obligations

- Add CAP2 `d_w` output through the Triton wrapper.
- Reuse the validated W5 reduction rather than adding a duplicate `dW` kernel.
- Compare `d_w` against the manual W6A reference on RunPod.
- Preserve existing `d_z`, `d_x_router`, and `d_h` parity.

## Gate Verdict

Pass. W6B is complete and the validated dW reduction path is available.
