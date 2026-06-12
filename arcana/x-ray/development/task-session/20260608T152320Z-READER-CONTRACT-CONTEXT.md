# Task Session Context: x-ray Reader Contract Proof

## Selected Task

Task reference: `arcana/x-ray/development/READER-ONRAMP-WORK-PACK.md`

Selected unit: prove the reader-on-ramp shape in the candidate lane model, example, and validator.

## Objective

Update the x-ray seed package so the existing order-ingestion example carries machine-checkable reader explanation fields:

- `reader_contract`
- `reader_terms`
- `layer_reader_outcomes`
- `readability_dynamics`

The work must keep `x-ray` at seed status and must not promote any local x-ray term into canonical project definitions.

## Controlling Sources

- `arcana/x-ray/development/READER-ONRAMP-WORK-PACK.md`
- `arcana/x-ray/development/READER-ONRAMP-RESEARCH.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/schemas/xray-lane-model.schema.yml`
- `arcana/x-ray/scripts/validate-xray-example.py`
- `arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json`
- `arcana/x-ray/examples/visual-layered-order-ingestion.html`

## Write Scope

- `arcana/x-ray/schemas/xray-lane-model.schema.yml`
- `arcana/x-ray/scripts/validate-xray-example.py`
- `arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json`
- `arcana/x-ray/examples/visual-layered-order-ingestion.html`
- `arcana/x-ray/development/task-session/20260608T152320Z-READER-CONTRACT-RESULT.md`

## Gates

| Gate | Status | Notes |
| --- | --- | --- |
| Exactly one task scope | pass | Reader contract proof for x-ray example and validator. |
| Context pack exists before mutation | pass | This file. |
| Human approval required | n/a | User invoked Task Session for the current x-ray work-pack context. |
| Runtime handoff | n/a | Local execution only. |
| Subagents | n/a | No delegated agents requested or needed. |
| Promotion boundary | pass | Seed status preserved; no registry or canonical definition mutation. |

## Implementation Path

1. Extend the lane-model candidate schema metadata with optional top-level reader fields and validation expectations.
2. Extend the JSON example with reader contract, local reader terms, layer outcomes, and readability dynamics.
3. Extend `validate-xray-example.py` to validate those fields when the schema names them.
4. Add HTML text markers so the visual example has nearby reader-facing explanations for compact labels.
5. Run validation commands.

## Validation Surface

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json --html arcana/x-ray/examples/visual-layered-order-ingestion.html
python3 arcana/x-ray/scripts/validate-xray-library.py
git diff --check -- arcana/x-ray
rg -n "reader_contract|reader_terms|layer_reader_outcomes|readability_dynamics|Reader terms|Reader outcomes" arcana/x-ray
```
