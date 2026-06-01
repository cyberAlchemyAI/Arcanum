# Refine Seed Proposal: visual layered x-ray

## Target

`arcana/x-ray`

## Operator Intent

Refine `x-ray` into a sigil that dissects a target object, artifact, architecture, or codebase. It should use dispatch-spec to create lanes, where each lane gives one vision of the target, then produce a comprehensive HTML explanation page with visual layers, SVG/diagram support, Mermaid architecture drawings, properties, internal dependencies, external dependencies, and an interactive stacked-layer view. Explore web assets and libraries that can support the visual model.

## Source Context

- Existing seed sigil: `arcana/x-ray/SKILL.md`
- Existing package README: `arcana/x-ray/README.md`
- Prior blocked refine result: `arcana/x-ray/development/refinement-runs/20260524T225844Z-sigil-new-low/RESULT.md`
- Dispatch-spec schema: `formulae/dispatch-spec/dispatch.schema.json`
- Dispatch technique catalog: `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- Research sources captured in `stages/04-research-decision.md`

## Write Scope

This refinement run may write only this run folder. It should not mutate the canonical sigil contract directly. Updating `arcana/x-ray/SKILL.md`, examples, or renderer scaffolding belongs to the recommended next route.

## Preset

`standard`

## Research Mode

`bounded-research`

External research is confirmed by the operator request: "research in web for assets that could help us in the visual part."

## Done Criteria

- A valid dispatch route exists for a ten-stage refine loop.
- The route uses `x_ray`, `component_descriptor`, and `entity_component_reference` in a way that produces consumable artifacts or handles.
- The refined design defines modes for object, artifact, architecture, and codebase inspection.
- The design defines dispatch-spec lane outputs, including at least properties, structure, dependency, flow, risk, and visual composition lanes.
- The HTML output model supports stacked visual layers and per-layer selection.
- The research decision records candidate visual assets or libraries and their constraints.
- The final synthesis recommends the next execution route without treating this refine run as implementation.

## Planned Stage Configuration

1. Context Builder evidence baseline: local package and dispatch-spec evidence.
2. Invoke Define: define the refined `x-ray` capability.
3. Interrogation refine-review: check ownership, scope, and evidence boundary.
4. Research decision: bounded web research for visual assets.
5. Distill: select the coherent unit.
6. Invoke Redefine / Design: design modes, lanes, output model, and renderer shape.
7. Interrogation refine-design-review: test the design against dispatch-spec and visual feasibility.
8. Distill Repair: tighten the minimum viable implementation layer.
9. Invoke Plan: produce a non-executed plan for implementation.
10. Final Interrogation and Synthesis: decide status and next route.

