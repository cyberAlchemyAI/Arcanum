# Task Session Context Pack: SWU-XRAY-VIS-006B

## Scope

Execute `SWU-XRAY-VIS-006B` from `WORK-PACK.md`.

## Selected Task

- Task: `TASK-XRAY-VIS-006`
- SWU: `SWU-XRAY-VIS-006B`
- Objective: add candidate component and pattern schemas after the visual library has real YAML records.

## Controlling Sources

- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/refinement-runs/20260529T124546Z-schema-readiness/RESULT.md`
- `arcana/x-ray/library/components.yml`
- `arcana/x-ray/library/patterns.yml`
- `framework/SCHEMA-CONSTITUTION.md`
- `arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md`

## Write Scope

- `arcana/x-ray/schemas/xray-component-library.schema.yml`
- `arcana/x-ray/schemas/xray-pattern-library.schema.yml`
- `arcana/x-ray/scripts/validate-xray-library.py`
- `arcana/x-ray/development/fixtures/invalid-component-library.yml`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/task-session/TASK-XRAY-VIS-006B-RESULT.md`

## Hard Constraints

- Use `.schema.yml` for schema files.
- Validate structure only; do not claim renderer correctness or promotion readiness.
- Component and pattern schemas must validate the YAML library records created by `SWU-XRAY-VIS-005B`.
- Include a negative fixture/probe.

## Decision Pack

- Validator shape: add `validate-xray-library.py` rather than overloading the HTML example validator. Selected because library schemas validate reusable YAML catalogs, while `validate-xray-example.py` validates lane model plus HTML artifacts.
- Cross-reference check: validate pattern `recommended_components` against component IDs. Selected because it catches drift between schemas and the actual library.

## Gate Verdict

pass

Dependencies are satisfied by completed `SWU-XRAY-VIS-006A`; component and pattern YAML files exist and validation is available.
