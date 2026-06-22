# Runtime Source Selection: Goal W1

## Selection

- Runtime source: `arcanum/spells/goal/runtime/goal_loop.py`
- Validation runner: `arcanum/spells/goal/validation/run-fixtures.py`
- Fixtures: `arcanum/spells/goal/validation/fixtures/*.json`
- Results: `arcanum/spells/goal/validation/results/`
- Profile mode: `neutral-default`

## Boundary

This runtime source is generic public spell code. It reads public-safe JSON
fixtures or caller payloads, emits frontier snapshots and goal-loop results, and
does not load filled profile data or mutate Craft state.

## Write Scope

Allowed for W1:

- `arcanum/spells/goal/runtime/goal_loop.py`
- `arcanum/spells/goal/validation/fixtures/*.json`
- `arcanum/spells/goal/validation/run-fixtures.py`
- `arcanum/spells/goal/validation/results/*`
- `arcanum/spells/goal/development/task-session-runs/20260621T031241Z-workpack-one-shot-w1/*`

Not allowed:

- Filled profile content.
- Active Craft ledger mutation.
- Generated host runtime surfaces.
- Commit, push, PR, publication, or parent gitlink movement.

## Decision

Proceed with generic runtime source and public-safe fixtures. This satisfies
`G-GOAL-RUNTIME-SOURCE` for W1 only; W2/W3 may refine the same runtime source
under their own SWU gates.
