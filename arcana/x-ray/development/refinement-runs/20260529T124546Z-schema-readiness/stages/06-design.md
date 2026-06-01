# Stage 06: Invoke Redefine / Design

Status: pass

## Schema Design Recommendation

Add schemas in two phases:

### Phase A: after current example, before many generated examples

- `arcana/x-ray/schemas/xray-lane-model.schema.json`
- update `validate-xray-example.py` to validate against the schema first, then run HTML-specific checks.
- add one invalid fixture for missing required lane or bad evidence/inference shape.

### Phase B: after component library SWU

- `arcana/x-ray/schemas/xray-visual-component.schema.json`
- `arcana/x-ray/schemas/xray-visual-pattern.schema.json`
- validate `arcana/x-ray/library/` docs or example JSON against those shapes.

### Later

- `xray-result.schema.json` only after multiple real outputs prove the result envelope is stable.

## Schema Boundaries

- JSON Schema validates shape.
- Python validator validates cross-file and HTML conditions.
- Browser proof validates visual rendering.
- Experiment Harness validates reusable behavior.

