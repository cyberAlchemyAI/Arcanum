# Context Pack: SWU-DFE-002

- Mode: `lean`
- Handoff: `runtime`
- Strict coverage: `pass`
- Task: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-REDUCER.md`
- Material writes: `9`
- Execution outputs: `2`
- Authority effect: `none`

## Obligations

- `scope`: `covered` — spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-REDUCER.md
- `dependencies`: `covered` — SWU-DFE-001 owner receipt
- `write-partition`: `covered` — spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/shared/COMMAND-MATRIX.json
- `validation`: `covered` — ['python3 goal/development/decision-frontier-experiment/scripts/run_frontier_fixtures.py --replay 2']
- `closeout`: `covered` — spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/shared/CLOSEOUT-CONTRACT.md
- `authority`: `covered` — public fixture-only; authority effect none

## Runtime Boundary

Apply only the digest-bound material package, run the exact validation argv, reconcile outputs against the allowed union, write one terminal receipt, and join the Invoke Refresh closeout receipt.
