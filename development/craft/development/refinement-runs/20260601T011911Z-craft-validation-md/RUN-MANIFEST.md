# Refine Run Manifest

## Status

- Run id: `20260601T011911Z-craft-validation-md`
- Status: `block`
- Target: `development/craft/CRAFT-VALIDATION.md`
- Preset: `standard`
- Research: `no-research`
- Dispatch route: `development/craft/development/refinement-runs/20260601T011911Z-craft-validation-md/REFINE-DISPATCH.json`
- Dispatch validation: `block`
- Runtime topology: native root orchestration
	- Stage adapter: `local-skill`

## Source Request

development/craft/CRAFT-VALIDATION.md --preset standard --research no

## Stage Evidence

| Stage | Owner | Status | Verdict |
| --- | --- | --- | --- |
| Task Zero Observer Envelope | refine | `pass` | observer envelope prepared |
| Context Builder evidence baseline | context-builder | `block` | Dispatch validation failed before stage execution: block |

## Next Route

If status is `pass`, route the resulting plan to Task Session or the requested downstream owner. If status is `block`, inspect the first blocked stage artifact and its log under `stages/.logs/`.
