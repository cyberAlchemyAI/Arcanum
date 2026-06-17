# Context Pack - TASK-W2-003 Convex Sparse Top-k

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-003`
Objective: Add convex sparse top-k baseline or explicit blocked report.

## Controlling Sources

- `WORK-PACK.md`: explicitly permits a blocked report if implementation details
  are missing.
- `RELAXATION-CANDIDATES.md`: C6 says convex sparse top-k is the strongest
  final candidate if continuous top-2 plus sparsity is required, but also says
  exact operator and Jacobian inspection are needed.
- `PRIOR-ART-MAP.md`: warns that convex differentiable sparse top-k is prior art
  and must be compared before novelty claims.

## Gate Verdict

BLOCK for implementation, PASS for producing the allowed blocked report.

## Missing Inputs

- exact forward operator;
- k=2 specialization;
- threshold/projection algorithm;
- backward/Jacobian;
- tie/support-boundary policy;
- fixture expected outputs.
