# Dispatch Run - Convex Sparse Top-k Extraction Research

Dispatch ID: `convex-sparse-topk-extraction-20260612`
Date: 2026-06-12
Status: pass

## Purpose

Design and validate a source-backed route for `TASK-W2-003A`, extracting the
convex sparse differentiable top-k baseline without hallucinating the operator,
backward rule, or novelty boundary.

## Artifacts

- `../../../convex-sparse-topk-extraction-20260612.dispatch.json`
- `../../../CONVEX-SPARSE-TOPK-RESEARCH-PACK.md`
- `execution-index.json`
- `CLOSEOUT.md`

## Validation

```text
python3 .agents/skills/dispatch-spec/scripts/validate-dispatch.py \
  research/triton-top2-backward-kernel/convex-sparse-topk-extraction-20260612.dispatch.json
```

Result:

```text
VALIDATION=pass
```

## Selected Extraction Direction

Use the official Google Research `sparse_soft_topk_mask_pav` path as the first
CPU reference extraction target for `k=2`.

Dykstra remains a later GPU-friendly approximation candidate, not the exact CPU
baseline.
