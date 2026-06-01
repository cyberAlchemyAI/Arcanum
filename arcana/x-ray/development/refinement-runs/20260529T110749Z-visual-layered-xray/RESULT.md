# Refine Result

- Target: `arcana/x-ray`
- Status: flag
- Preset: `standard`
- Research: `bounded-research`
- Run manifest: `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RUN-MANIFEST.md`
- Evidence index: `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/evidence-index.json`
- Seed proposal: `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/REFINE-SEED-PROPOSAL.md`
- Dispatch route: `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/REFINE-DISPATCH.json`
- Runtime handoff: `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RUNTIME-HANDOFF.md`

## Stage Evidence

- Context Builder evidence baseline: pass
- Invoke Define: pass
- Interrogation refine-review: pass
- Research decision: pass
- Distill: pass
- Invoke Redefine / Design: pass
- Interrogation refine-design-review: flag
- Distill Repair: pass
- Invoke Plan: pass
- Final Interrogation and Synthesis: flag

## Final Synthesis

`x-ray` should be revised from a general HTML explainer seed into a dispatch-spec governed visual inspection sigil.

The refined core is:

> A target is inspected through lanes. Each lane gives one vision of the target and emits a handle. The handles compose into one local HTML page where visual layers can be stacked, isolated, compared, or traced.

The canonical modes should be:

- `object`
- `artifact`
- `architecture`
- `codebase`
- `process`
- `mixed`

The canonical lanes should be:

- `surface`
- `properties`
- `components`
- `internal_dependencies`
- `external_dependencies`
- `flow`
- `lifecycle`
- `risk_questions`
- `visual_composition`

The output should be a static local HTML artifact first, using semantic HTML, CSS, inline SVG, and a selectable layer stack. Mermaid, CSS3D, Three.js, and Kroki should be optional adapters layered in after the L0 HTML/SVG model is proven.

## Research Summary

External visual research supports the following choices:

- Three.js Layers can support later 3D layer visibility controls.
- Three.js CSS3DRenderer can apply 3D transforms to DOM elements, but has constraints and should be optional.
- Mermaid provides broad diagram syntax and architecture diagrams that can map well to architecture and codebase x-rays.
- Kroki can generate SVG from many diagram languages, but remote rendering should not be required for private local targets.
- Sketch-style SVG tooling may be useful later for more expressive explanatory visuals.

## Recommended Next Routes

1. `/sigil-development arcana/x-ray --mode revise --from arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RESULT.md`
2. `/task-session arcana/x-ray/development/WORK-PACK.md --task <new visual x-ray revision task>` after Sigil Development approves the revision.

## Implementation Boundary

This run does not update the canonical `x-ray` skill. It provides a validated refinement package for the next route.

