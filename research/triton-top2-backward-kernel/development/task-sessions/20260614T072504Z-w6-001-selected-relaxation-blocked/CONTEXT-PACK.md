# Context Pack - TASK-W6-001

Task: `TASK-W6-001`
Scope: implement selected relaxation kernel if CAP2/promoted relaxation survives.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W6-001` depends on `TASK-W3-003` and `TASK-W5-001`.
- `CAP2-CANDIDATE-SPEC.md`: CAP2-v0 was promoted as candidate only, with no novelty claim.
- `CAP2-REFERENCE.md`: CAP2-v0 reference and fixed-load gradcheck pass in PyTorch.
- `reference/router_torch.py`: PyTorch CAP2 reference uses autograd for the smooth graph.
- `CAP2-PRIOR-ART-COMPARISON.md`: CAP2 is plausible but not Triton-ready or novelty-proven.

## Gate Finding

The selected relaxation is conceptually chosen, but the Triton task is not yet
execution-ready as written.

Known:

- CAP2 forward routing weights are specified:
  - capacity-adjusted logits;
  - pairwise soft rank;
  - soft top-2 membership;
  - normalized gated softmax.
- PyTorch CAP2 fixed-load graph passes gradcheck.

Missing for a safe Triton implementation:

- whether W6 should implement only CAP2 forward weights or exact backward for
  the CAP2-v0 differentiable graph;
- expected kernel outputs: `A`, `P`, `dW`, `dX_router`, `dH`, auxiliaries, or all;
- saved-state versus recompute policy for zero-allocation;
- output/scratch buffer contract;
- FP16/FP32 accumulation policy and tolerances;
- small-shape and capacity-pressure fixtures for Triton parity;
- whether to block W7 benchmark on W6 or benchmark fixed-mask only.

## Blocker

Implementing a forward-only CAP2 Triton kernel would not satisfy the original
backward challenge, while implementing full exact backward requires a more
specific implementation-detail spec than the current work-pack row provides.

## Recommended Decision Gate

Pick one:

1. Implement CAP2 forward-routing weights only as a Triton feasibility slice.
2. Author a W6 implementation-detail spec for exact CAP2 backward before code.
3. Defer CAP2 Triton and proceed with fixed-mask-only W7 benchmark/final report.
