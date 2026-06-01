# Stage 09: Invoke Plan

Status: pass

## Non-Executed Plan

Add `TASK-XRAY-VIS-006`: Add candidate x-ray schemas and validator integration.

SWUs:

- `SWU-XRAY-VIS-006A`: add `xray-lane-model.schema.json`, invalid fixtures, and validator integration.
- `SWU-XRAY-VIS-006B`: add component and pattern schemas after the component library exists.

Validation:

```bash
test -f arcana/x-ray/schemas/xray-lane-model.schema.json
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json --html arcana/x-ray/examples/visual-layered-order-ingestion.html
python3 -m json.tool arcana/x-ray/schemas/xray-lane-model.schema.json >/dev/null
git diff --check -- arcana/x-ray/schemas arcana/x-ray/scripts arcana/x-ray/development
```

