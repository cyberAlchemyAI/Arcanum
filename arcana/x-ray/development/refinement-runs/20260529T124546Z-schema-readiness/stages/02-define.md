# Stage 02: Invoke Define

Status: pass

`x-ray` should add candidate schemas when it wants agent-generated outputs to be repeatably valid.

The first schema should describe the lane model JSON. It should not try to validate the full HTML page. HTML remains better checked by parser, browser proof, and targeted artifact checks.

Candidate schema surfaces:

1. `xray-lane-model.schema.json`
2. `xray-visual-component.schema.json`
3. `xray-visual-pattern.schema.json`
4. optional later `xray-result.schema.json`

