# Context Pack - TASK-W2-003A Convex Sparse Top-k Extraction

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003A`
Objective: Extract an implementation-ready convex sparse top-k operator from
the source-backed dispatch route.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W2-003A` dispatch-ready.
- `convex-sparse-topk-extraction-20260612.dispatch.json`: validates the route.
- `CONVEX-SPARSE-TOPK-RESEARCH-PACK.md`: selects official PAV mask path.
- Official Google Research `sparse_soft_topk` implementation.

## Gate Verdict

- Source gate: pass.
- Operator identity gate: pass. Extracted mask operator, not magnitude top-k.
- Exactness gate: pass. PAV path extracted; Dykstra remains deferred.
- Novelty guardrail: pass. This is prior art.
- Triton guardrail: pass. No Triton readiness claim.

## Write Scope

- `reference/router_reference.py`
- `tests/test_router_reference.py`
- `CONVEX-SPARSE-TOPK-EXTRACTION.md`
- `CONVEX-SPARSE-TOPK-FIXTURES.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`

## Decision Boundary

This task extracts the relaxed mask. It does not decide the final router
composition rule for the convex sparse top-k baseline.
