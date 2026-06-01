# Implementation Layering: Visual Layered x-ray

Status: pass
Target: `arcana/x-ray`

## L0 - Contract Revision

Question: Does the canonical `x-ray` contract now define modes, lanes, output handles, the renderer ladder, and evidence boundaries?

Evidence:

- `arcana/x-ray/SKILL.md` updated.
- `arcana/x-ray/README.md` updated.
- Grep checks find modes, lanes, dependency terms, and renderer ladder.

## L1 - Static Layered Example

Question: Can the sigil produce or demonstrate a local static HTML/SVG x-ray page?

Evidence:

- Example source exists.
- Example lane model exists.
- Example HTML exists with layer controls.
- HTML parse succeeds.

## L2 - Validation Harness

Question: Can agents verify the x-ray artifact shape before relying on it?

Evidence:

- Validation script or documented validation checklist exists.
- Required lane ids are checked.
- Evidence/inference fields are checked.
- Internal and external dependency sections are checked.

## L3 - Visual Adapter Hardening

Question: Which optional visual adapters are safe and useful after L0-L2 evidence exists?

Evidence:

- Mermaid conservative templates documented.
- CSS3D or Three.js is explicitly optional.
- Remote rendering policy blocks by default for private targets.
- Browser validation covers the generated HTML artifact.

## Promotion Boundary

This layering plan does not promote `x-ray`. Promotion remains gated by Sigil Development plus Experiment Harness evidence across component, process, architecture/plan, and insufficient-context examples.

