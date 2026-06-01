# Stage 02: Invoke Define

Status: pass

## Definition

The missing slice is an `x-ray visual library`: a small local catalog of reusable explanatory visual primitives and pattern recipes.

The library should help agents compose L0 static HTML/SVG outputs and should gently invite the user to add domain-specific shapes, charts, and patterns when the built-ins do not fit.

## Candidate Library Families

- shapes: node, boundary, layer, actor, queue, document, decision, risk marker,
- connectors: arrow, branch, dependency edge, feedback loop, handoff,
- charts: count bar, timeline, risk matrix, dependency table, small sankey-like flow,
- patterns: process branch, component map, architecture boundary, lifecycle stack, evidence/inference split, comparison view.

## User Nudge

Each generated x-ray result should include a small "Extend this x-ray" note when helpful:

> Add your own shape, chart, or pattern when this target has a domain-specific form the default library cannot express.

