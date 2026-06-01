# Task Session Context Pack: SWU-XRAY-VIS-006A

## Scope

Execute `SWU-XRAY-VIS-006A` from `WORK-PACK.md`.

## Selected Task

- Task: `TASK-XRAY-VIS-006`
- SWU: `SWU-XRAY-VIS-006A`
- Objective: add a candidate lane-model schema and integrate it into the x-ray example validator before HTML-specific checks.

## Controlling Sources

- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/refinement-runs/20260529T124546Z-schema-readiness/RESULT.md`
- `framework/SCHEMA-CONSTITUTION.md`
- `arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json`
- `arcana/x-ray/scripts/validate-xray-example.py`

## Write Scope

- `arcana/x-ray/schemas/xray-lane-model.schema.yml`
- `arcana/x-ray/scripts/validate-xray-example.py`
- `arcana/x-ray/development/fixtures/invalid-missing-lane.lanes.json`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/task-session/TASK-XRAY-VIS-006A-RESULT.md`

## Hard Constraints

- Use `.schema.yml`, not `.schema.json`, to comply with the repo schema constitution.
- Keep schema status candidate/local.
- Validate structure only; do not claim explanatory correctness.
- Run a negative fixture probe.
- Do not add component or pattern schemas in this SWU.

## Decision Pack

- Schema format: candidate YAML schema with an `artifact` metadata block and a structural `schema` payload. Selected to align with framework schema and artifact metadata governance.
- Validator integration: Python validator loads the YAML schema and derives required lanes, allowed modes, renderer levels, and required lane fields before HTML parsing.

## Gate Verdict

pass

Dependencies are satisfied by completed `SWU-XRAY-VIS-005B`; the selected write scope is bounded and validation is available.
