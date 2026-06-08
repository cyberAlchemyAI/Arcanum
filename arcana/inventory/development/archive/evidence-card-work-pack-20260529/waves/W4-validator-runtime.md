# W4: Validator Runtime

## Layer

- Layer: L4
- Tasks: TASK-007

## Objective

Implement the fast shell plus `jq` validator surface for agents while keeping the human UI surface deferred.

## Included SWUs

| SWU | Task | Exit Evidence | Batch |
| --- | --- | --- | --- |
| SWU-INV-KS-010 | TASK-007 | validator script runs against pilot fixtures | A |
| SWU-INV-KS-011 | TASK-007 | invalid examples fixture parses | A |
| SWU-INV-KS-012 | TASK-007 | runtime contract notes exist | A |
| SWU-INV-KS-013 | TASK-007 | validator result synchronized | after A |

## Batch Gate

Batch A may run together only if the task-session runner confirms the write scopes remain disjoint:

- `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`
- `arcana/inventory/development/pilot/evidence-card/invalid-examples.json`
- `arcana/inventory/development/VALIDATOR-RUNTIME.md`

If any SWU needs to edit a shared planning or readiness file, stop the batch and resume sequentially.

## Exit Gate

The validator runs through shell plus `jq`, reports schema/authority failures clearly, and records readiness without starting the deferred human UI.
