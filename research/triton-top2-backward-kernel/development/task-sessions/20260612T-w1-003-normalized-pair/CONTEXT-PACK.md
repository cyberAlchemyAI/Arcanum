# Context Pack - TASK-W1-003 Normalized Pair Weights

Date: 2026-06-12

## Task Scope

Task: `TASK-W1-003`
Objective: Add a normalized selected-pair comparison variant so the project can
compare raw `M * P` routing weights against pair-renormalized weights.

## Controlling Sources

- `WORK-PACK.md`: requires tests comparing `M*P` and normalized pair weights.
- `reference/router_reference.py`: standard-library V0 raw masked probability
  baseline.
- `reference/router_torch.py`: PyTorch tensor mirror.

## Gates

- Dependency gate: pass. `TASK-W1-001` is passed.
- Semantic gate: pass. This variant still uses a saved mask and does not
  differentiate hard Top2 selection.
- GPU gate: not applicable.

## Decisions

- Treat the variant as a comparison baseline, not a replacement for V0.
- Use `a = (M * P) / sum_j(M * P)_j` per token.
- Preserve the same router probabilities and auxiliary term as V0 so the
  comparison isolates the combine-weight difference.
