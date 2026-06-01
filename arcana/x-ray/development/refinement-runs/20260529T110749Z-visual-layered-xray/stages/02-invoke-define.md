# Stage 02: Invoke Define

## Status

pass

## xray-definition-handle

`handle:xray-lane-based-visual-explainer`

## Definition

`x-ray` is a lane-based visual explanation sigil. Given a target object, artifact, architecture, codebase, process, workflow, or plan, it creates a governed inspection model and renders that model as a local HTML artifact.

The sigil does not simply summarize the target. It separates the target into explanation lanes. Each lane gives one vision of the target and emits a structured handle that the renderer can consume.

## Modes

| Mode | Use | Primary Lanes |
| --- | --- | --- |
| `object` | Explain a bounded conceptual or data object. | properties, relationships, lifecycle, dependency |
| `artifact` | Explain a document, spec, plan, deck, or generated artifact. | intent, structure, claims, evidence, gaps |
| `architecture` | Explain a system or component architecture. | components, boundaries, flow, internal dependencies, external dependencies |
| `codebase` | Explain repository or module structure. | packages, entrypoints, call/data flow, tests, external services |
| `process` | Explain an operational or human workflow. | actors, steps, decisions, transformations, handoffs |
| `mixed` | Explain targets that combine more than one shape. | adaptive lane set selected by dispatch |

## Output Promise

The output is a single browsable HTML page with:

- a target summary and evidence boundary,
- selectable lanes,
- a stacked layer view where layers can be isolated or overlaid,
- SVG-native constructed visuals,
- Mermaid or equivalent diagram blocks when useful,
- internal dependency and external dependency views,
- properties and open questions,
- optional 3D or pseudo-3D layer controls when they improve understanding.

## Boundary

`x-ray` explains and visualizes. It does not execute code changes, promote ontology, certify architecture correctness, or replace domain-specific validators.

