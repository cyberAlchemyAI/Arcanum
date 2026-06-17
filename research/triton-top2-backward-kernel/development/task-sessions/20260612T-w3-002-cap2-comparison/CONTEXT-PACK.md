# Context Pack - TASK-W3-002 CAP2 Comparison

Date: 2026-06-12

## Task Scope

Task: `TASK-W3-002`
Objective: Compare CAP2-v0 against prior-art baselines.

## Controlling Sources

- `WORK-PACK.md`: marks `TASK-W3-002` ready after sparsemax, ReLU, convex sparse
  top-k parity, and CAP2 reference tasks passed.
- `CAP2-REFERENCE.md`: defines the implemented CAP2-v0 reference and non-claims.
- `PRIOR-ART-MAP.md`: requires comparison against fixed-mask Top2,
  entmax/sparsemax, convex sparse top-k, and ReLU routing before novelty claims.
- `FINAL-QUESTION-RESOLUTION.md`: requires CAP2 to be killed or promoted with
  evidence.

## Gates

- Dependency gate: pass.
- Novelty gate: not entered. This task produces comparison evidence only.
- Semantic gate: pass. No hard Top2 differentiability claim is introduced.

## Write Scope

- `CAP2-PRIOR-ART-COMPARISON.md`
- `WORK-PACK.md`
- `README.md`
- `TOWER.md`
- task-session evidence folder

## Completion Boundary

Success means a comparison table exists and W3 can proceed to the kill/promote/
defer decision.

Success does not mean CAP2 is novel or selected for Triton.
