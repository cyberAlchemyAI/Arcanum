# x-ray Visual Adapter Backlog

Status: seed backlog
Updated: 2026-05-29

## Baseline Rule

`x-ray` must remain useful with L0 static HTML, CSS, and inline SVG. Optional adapters can improve expressiveness, but they must not become required for a valid result.

## Adapter Ladder

| Level | Adapter | Use When | Entry Gate | Validation Required |
| --- | --- | --- | --- | --- |
| L0 | Static HTML/SVG | Any x-ray target needs a local, inspectable page. | Always available. | HTML parse, lane model validation, browser snapshot or screenshot for generated artifacts. |
| L1 | Mermaid source blocks | Flow, dependency, sequence, class, or architecture diagrams are clearer as text diagrams. | L0 example and validator pass. | Conservative syntax templates plus rendered or parse-equivalent review. |
| L2 | In-browser Mermaid rendering | The artifact policy allows local browser-side Mermaid rendering. | Mermaid source blocks validate. | Browser snapshot, console check, fallback source visible when render fails. |
| L3 | CSS 3D layer stack | Layer depth helps inspect overlap without requiring a graphics engine. | Static layer controls are already usable. | Browser checks across desktop and mobile widths. |
| L4 | Three.js or CSS3DRenderer | Spatial exploration genuinely improves understanding of a complex target. | L0-L3 evidence exists and a target-specific reason is recorded. | Canvas or DOM render proof, nonblank screenshot, interaction check, fallback path. |
| External | Kroki SVG export | A diagram type is better rendered by a text-diagram service or self-hosted adapter. | Privacy and network policy explicitly allow it. | Local/self-hosted preference, saved SVG artifact, no private context leak. |

## Browser Validation Requirements

Any generated HTML artifact that is claimed as a visual output must have browser proof:

- serve over localhost when browser tooling cannot handle `file://`,
- capture a snapshot showing main controls and rendered visual content,
- capture a screenshot,
- check console output and explain any remaining warnings,
- verify text and controls do not overlap at the tested viewport,
- record the proof path in the task-session result or experiment evidence.

## Mermaid Backlog

Candidate templates:

- flowchart for process and data movement,
- sequence diagram for actor handoffs,
- class or ER diagram for object/entity structure,
- architecture diagram only with conservative syntax and fallback because architecture syntax may be stricter than ordinary flowcharts.

Deferred work:

- add Mermaid source examples,
- add syntax validation or snapshot-render validation,
- keep Mermaid source visible when rendering fails.

## CSS 3D Backlog

Candidate behaviors:

- depth-separated layer stack,
- isolate layer,
- compare two lanes,
- trace one component across dependency and flow layers.

Deferred work:

- mobile fallback for stacked panels,
- reduced-motion support,
- overlap and readability checks.

## Three.js Backlog

Candidate behaviors:

- component graph in 3D when architecture depth matters,
- layer visibility toggles using Three.js layer concepts,
- CSS3DRenderer panels for HTML-native layer cards.

Entry rule:

Three.js is justified only when the target needs spatial exploration. It is not justified merely to make the page look more advanced.

Deferred work:

- nonblank canvas validation,
- camera framing checks,
- interaction checks,
- static SVG fallback.

## Kroki Backlog

Candidate use:

- generate SVG from diagram languages not handled by the local renderer,
- compare Mermaid, GraphViz, PlantUML/C4, Structurizr, D2, or Excalidraw output when a specific target needs that format.

Entry rule:

Kroki must be local or explicitly approved for remote use. Private target content cannot be sent to a public remote renderer by default.

## Stop Conditions

Stop or block adapter work when:

- the adapter becomes required for baseline success,
- the target includes private context and the adapter needs remote rendering,
- the visual output is decorative but does not improve explanation,
- browser proof cannot show nonblank, readable, interactive output,
- the adapter hides source evidence or inference markers.

