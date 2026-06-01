# Refine Seed Proposal: x-ray schema readiness

## Target

`arcana/x-ray`

## Operator Intent

Decide whether `x-ray` needs schemas now, based on the current lane model, example JSON, local validator, planned component library, and future user-added shapes/charts/patterns.

## Current Evidence

- `arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json` has an implied lane model shape.
- `arcana/x-ray/scripts/validate-xray-example.py` validates required lanes, evidence/inference lists, renderer level, controls, data-lane attributes, dependency layer coverage, and remote refs.
- No explicit JSON Schema exists under `arcana/x-ray/`.
- `SWU-XRAY-VIS-005` is ready for a visual component library and user extension template.

## Preset

`compact`

## Research

`no-research`

The decision is local: this is about when to formalize existing shapes, not about external schema standards.

## Done Criteria

- Decide whether schema work is needed.
- Name which schema surfaces should exist.
- Place schema work in the work-pack at the right dependency point.

