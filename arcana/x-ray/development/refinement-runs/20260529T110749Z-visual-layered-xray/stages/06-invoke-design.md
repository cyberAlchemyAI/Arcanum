# Stage 06: Invoke Redefine / Design

## Status

pass

## lane-model

`handle:xray-canonical-lane-model`

## Design

`x-ray` should become a two-part sigil:

1. **Analysis dispatch**: produce lane artifacts from the target.
2. **Visual synthesis**: compose lane artifacts into one HTML x-ray page.

## Canonical Lanes

| Lane | Vision | Required Output Handle |
| --- | --- | --- |
| `surface` | What the target appears to be and why the user is inspecting it. | `surface.summary` |
| `properties` | Important attributes, invariants, metadata, constraints, and state. | `properties.catalog` |
| `components` | Internal parts and their purposes. | `components.map` |
| `internal_dependencies` | Dependencies among internal components, modules, sections, or stages. | `dependencies.internal` |
| `external_dependencies` | Services, libraries, APIs, people, policies, or artifacts outside the target. | `dependencies.external` |
| `flow` | Data, control, work, or meaning movement through the target. | `flow.graph` |
| `lifecycle` | Creation, operation, mutation, validation, and failure states. | `lifecycle.timeline` |
| `risk_questions` | Ambiguity, missing evidence, risk, contradiction, and open questions. | `risk.questions` |
| `visual_composition` | Renderer instructions for layer stack, SVG, Mermaid, and optional 3D. | `visual.model` |

## Mode-Specific Lane Selection

- `object`: surface, properties, components, internal_dependencies, external_dependencies, lifecycle, risk_questions, visual_composition.
- `artifact`: surface, properties, components, flow, risk_questions, visual_composition.
- `architecture`: surface, components, internal_dependencies, external_dependencies, flow, lifecycle, risk_questions, visual_composition.
- `codebase`: surface, components, internal_dependencies, external_dependencies, flow, lifecycle, risk_questions, visual_composition.
- `process`: surface, components, flow, lifecycle, external_dependencies, risk_questions, visual_composition.
- `mixed`: dispatch-selected lane set plus an explicit reason for each lane included or omitted.

## HTML Page Model

The page should contain:

- target header with mode, confidence, and evidence boundary,
- layer stack viewport,
- layer selector controls,
- dependency toggle for internal/external,
- properties inspector,
- diagram panel,
- source evidence panel,
- open questions panel,
- exportable static artifact.

## Visual Stack Interaction

Layer states:

- `stacked`: all selected lanes are visible as depth-separated translucent layers.
- `isolate`: one lane is full focus; related lanes remain dimmed.
- `compare`: two lanes are shown side by side or overlapped.
- `trace`: select one component and highlight its path across property, dependency, and flow layers.

## Renderer Ladder

- L0: semantic HTML plus CSS and inline SVG.
- L1: generated Mermaid source blocks for flow/dependency/architecture diagrams.
- L2: Mermaid rendered in-browser when allowed by artifact policy.
- L3: CSS 3D transforms for stacked panels.
- L4: Three.js or CSS3DRenderer for optional spatial exploration.

## Validation Expectations

- HTML parses.
- No remote dependency is required for L0.
- Mermaid source is syntactically conservative.
- Each lane has an evidence/inference boundary.
- Every visual element maps back to a lane handle.

