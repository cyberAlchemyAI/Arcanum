# Stage 04: Research Decision

## Status

pass

## Mode

`bounded-research`

The operator explicitly requested web research for visual assets. External research is used as advisory implementation context and does not override local Arcanum evidence.

## Findings

| Source | Relevant Use | Constraint |
| --- | --- | --- |
| Three.js Layers docs, https://threejs.org/docs/pages/Layers.html | Three.js has a built-in layer membership model, useful for toggling groups of 3D objects by camera visibility. | Good for optional 3D enhancement, but not required for the MVP. |
| Three.js CSS3DRenderer docs, https://threejs.org/docs/pages/CSS3DRenderer.html | CSS3DRenderer can apply 3D transforms to DOM elements, which fits HTML layer cards or panels. | It has material/geometry limitations and zoom constraints, so use only as enhancement. |
| Mermaid syntax reference, https://mermaid.js.org/intro/syntax-reference.html | Mermaid supports many diagram types, including flowchart, sequence, class, ER, C4, architecture, sankey, timeline, and more. | Mermaid syntax is strict; generated diagrams need validation or conservative templates. |
| Mermaid architecture diagrams, https://mermaid.ai/open-source/syntax/architecture.html | Mermaid architecture diagrams model groups, services, edges, and junctions, which maps well to architecture/codebase x-rays. | `architecture-beta` should be treated as optional and validated separately. |
| Kroki, https://kroki.io/ | Kroki can render many textual diagram languages, including Mermaid, GraphViz, PlantUML/C4, Structurizr, D2, Excalidraw, Vega, and WireViz, often to SVG. | Remote API use should not be required for local/private targets; self-managed/offline use can be a later adapter. |
| Sketchmark, https://www.sketchmark.dev/ | Sketch-style SVG diagrams could support explanatory, non-photoreal visuals for generated pages. | Consider later; not needed for the first renderer contract. |

## Decision

Use a renderer ladder:

1. MVP: single static HTML file with inline CSS, inline SVG, accessible layer controls, and optionally embedded Mermaid source blocks.
2. Standard: add Mermaid rendering for flow, dependency, and architecture lanes, with conservative syntax templates.
3. Enhanced: add CSS 3D transforms for stacked layer panels.
4. Experimental: add Three.js layer toggles or CSS3DRenderer when a target benefits from spatial inspection.
5. Optional external adapter: Kroki-generated SVG for diagram types that Mermaid cannot handle locally, only when privacy and network policy allow it.

