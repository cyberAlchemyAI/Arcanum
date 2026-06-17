# Context Pack - TASK-W2-002 ReLU Routing

Date: 2026-06-12

## Task Scope

Task: `TASK-W2-002`
Objective: Add a ReLU routing prior-art baseline.

## Controlling Sources

- `WORK-PACK.md`: requires a ReLU routing baseline.
- `PRIOR-ART-MAP.md`: ReLU routing / ReMoE is prior art and must be compared
  before novelty claims.
- `RELAXATION-CANDIDATES.md`: C8 frames ReLU routing as a fully
  differentiable MoE alternative.

## Gates

- Dependency gate: pass. CPU PyTorch environment exists.
- Semantic gate: pass. This is a separate continuous-router baseline, not a
  hard Top2 differentiability claim.
- Scope gate: pass. Implemented normalized ReLU routing only, not the full ReMoE
  recipe.

## Decisions

- Use `A = relu(Z) / sum_j relu(Z_j)` per token as the local comparison
  baseline.
- Reject all-nonpositive rows explicitly rather than silently inventing a
  fallback distribution.
