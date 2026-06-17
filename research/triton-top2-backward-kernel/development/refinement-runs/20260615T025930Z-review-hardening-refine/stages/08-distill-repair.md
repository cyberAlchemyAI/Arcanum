# Stage 08 - Distill Repair

Status: `pass`

## Repair Decisions

- Keep CAP2 candidate-only.
- Add exact 2-sparsity as a negative/non-claim fixture before any new operator work.
- Require a differentiable load definition before dynamic-load gradients.
- Treat CAP2 zero-allocation and FP16 as separate systems acceptance tasks.
- Treat entmax as either implemented baseline or explicit limitation.
- Patch paper guard wording only after the updated task plan exists.
- Inventory artifacts before any commit/share/export step.

## Toy-Game Requirements

Tiny fixtures should be used first for:

- CAP2 support count above tolerance;
- dynamic-load VJP sanity;
- CAP2 FP16 tolerance;
- CAP2 allocation reuse after warmup.
