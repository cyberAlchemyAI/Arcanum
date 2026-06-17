# Context Pack - TASK-W2-001 Sparsemax Baseline

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-001`
Objective: Add a sparse probability-map baseline from the sparsemax/entmax
prior-art family.

## Controlling Sources

- `WORK-PACK.md`: W2 requires prior-art baselines before CAP2 comparison.
- `PRIOR-ART-MAP.md`: sparsemax/entmax is prior art and should not be claimed
  as novel.
- `RELAXATION-CANDIDATES.md`: C4 frames sparsemax/entmax as a sparse
  differentiable probability-map candidate.

## Gates

- Dependency gate: pass. CPU PyTorch environment exists.
- Semantic gate: pass. Sparsemax is a separate continuous routing baseline, not
  a hard Top2 differentiability claim.
- Formula gate: pass for sparsemax; entmax remains deferred because the local
  tower does not yet pin an implementation-ready formula.

## Decisions

- Implement sparsemax now because its projection formula is compact and
  auditable.
- Record entmax as a named family gap rather than implementing an unverified
  approximation under the entmax name.
