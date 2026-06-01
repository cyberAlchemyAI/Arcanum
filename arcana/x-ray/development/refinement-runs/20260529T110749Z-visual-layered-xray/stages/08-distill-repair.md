# Stage 08: Distill Repair

## Status

pass

## minimum-viable-xray

`handle:xray-mvp-static-layered-html`

## Repair Decision

The minimum viable next implementation should be:

1. Update `arcana/x-ray/SKILL.md` with modes, lane catalog, renderer ladder, and output contract.
2. Add one example source and one generated static HTML example under `arcana/x-ray/examples/`.
3. Build an L0 HTML/SVG renderer shape as a static template or generated artifact.
4. Add validation that checks artifact existence, HTML parse, lane ids, and evidence/inference fields.
5. Defer Mermaid rendering, CSS3D, and Three.js until the static layer model is proven.

## Why This Repair Holds

This keeps the coolest part of the idea, the stacked visual x-ray, while avoiding a first-step dependency on 3D runtime quality. It also creates a clean path for later visual upgrades.

