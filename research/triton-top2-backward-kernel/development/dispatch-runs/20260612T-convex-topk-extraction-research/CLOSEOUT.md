# Closeout - Convex Sparse Top-k Extraction Dispatch

Status: pass
Date: 2026-06-12

## Result

The dispatch route is schema-valid and governance-valid.

The research pass identified enough source evidence to make `TASK-W2-003A`
actionable:

- paper: Sander et al., ICML 2023;
- official implementation: Google Research `sparse_soft_topk`;
- first extraction target: `sparse_soft_topk_mask_pav(scores, k=2, l, p)`;
- recommended default: PAV mask path with `p=4/3` for CPU reference extraction;
- later candidate: Dykstra mask path for GPU-friendly approximation research.

## Guardrails

- Convex sparse top-k is prior art, not a CAP2 novelty claim.
- PAV and Dykstra must not be conflated: PAV is the exact extraction path,
  Dykstra is approximate and GPU-friendly.
- A CPU/JAX/PyTorch extraction does not satisfy the zero-allocation Triton gate.
- Boundary/tie behavior must be documented before marking implementation pass.

## Next Route

Run `task-session` for:

```text
TASK-W2-003A: Extract implementation-ready convex sparse top-k operator.
```

Controlling artifacts:

- `CONVEX-SPARSE-TOPK-RESEARCH-PACK.md`
- `convex-sparse-topk-extraction-20260612.dispatch.json`
- `CONVEX-SPARSE-TOPK-BLOCKED.md`
