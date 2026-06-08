# Example Source: Visual Layered Order Ingestion

## Target

Order ingestion process.

## Source Context

```text
We have an order ingestion process. A merchant uploads a CSV. The validator checks required fields, normalizes currency, and sends accepted rows to the pricing queue. Rejected rows are written to an error report. Support reviews recurring rejection causes weekly.
```

## Intended x-ray Mode

`process`

## Evidence Boundary

Source-backed facts:

- merchant uploads a CSV,
- validator checks required fields,
- validator normalizes currency,
- accepted rows go to the pricing queue,
- rejected rows go to an error report,
- support reviews recurring rejection causes weekly.

Inferred structure:

- the validator is the process boundary where rows branch,
- currency normalization happens before accepted rows enter pricing,
- support feedback may influence future validator rules.

## Expected Renderer Level

L0 static HTML/SVG. No remote rendering, Mermaid, CSS3D, Three.js, or Kroki is required.

