# x-ray

`x-ray` is an Arcana sigil seed for turning a target object, artifact, architecture, codebase, process, or mixed context into a visual layered HTML explanation page.

It is meant for moments when the important structure is present but hard to see: dependencies hidden in prose, concepts spread across a plan, modules buried in a codebase, or process steps implied by an operational description.

## Status

Status: seed.

This package defines the revised lane model, renderer ladder, and validation direction for `x-ray`. It is not promoted and does not yet include reusable behavior evidence from live examples.

## Problem It Solves

Raw context can be hard to inspect because structure is often implicit. A system description may hide actors, transformations, data flow, dependencies, decisions, and open questions inside prose, code, diagrams, or planning notes.

`x-ray` makes that structure visible by splitting a target into explanation lanes. Each lane gives one vision of the target, such as properties, components, internal dependencies, external dependencies, flow, lifecycle, or risk questions. The lane handles compose into a local HTML page where layers can be stacked, isolated, compared, or traced.

## Modes

| Mode | Use When |
| --- | --- |
| `object` | Explain a bounded conceptual, data, or domain object. |
| `artifact` | Explain a document, spec, plan, deck, or generated artifact. |
| `architecture` | Explain a system, subsystem, component graph, or design architecture. |
| `codebase` | Explain a repository, package, module, or source subtree. |
| `process` | Explain an operational, human, or system workflow. |
| `mixed` | Explain a target that legitimately combines multiple shapes. |

## Canonical Lanes

| Lane | What It Shows |
| --- | --- |
| `surface` | What the target appears to be and why it is being inspected. |
| `properties` | Important attributes, invariants, metadata, constraints, and state. |
| `components` | Internal parts and their purposes. |
| `internal_dependencies` | Dependencies among parts inside the target. |
| `external_dependencies` | Services, libraries, APIs, people, policies, or artifacts outside the target. |
| `flow` | Data, control, work, or meaning movement. |
| `lifecycle` | Creation, operation, mutation, validation, failure, and retirement states. |
| `risk_questions` | Ambiguity, missing evidence, contradictions, risks, and open questions. |
| `visual_composition` | How lane handles map into the HTML/SVG layer stack and optional adapters. |

## Output Model

The target output is a single local HTML explanation page.

The first renderer level is intentionally simple:

- semantic HTML,
- inline CSS,
- inline SVG,
- layer controls,
- source evidence and inference markers,
- internal and external dependency sections.

Later renderer levels may add Mermaid diagrams, CSS 3D transforms, Three.js, or Kroki-generated SVG, but those are optional adapters. A valid baseline `x-ray` result must not depend on remote rendering or 3D.

## Visual Library

The starter visual library lives in [library/](library/). It is a YAML-backed catalog for HTML/SVG x-rays, not a renderer engine.

- [components.yml](library/components.yml) is the canonical source for starter shapes, connectors, and tiny charts: node, boundary, layer panel, risk marker, arrow, branch, feedback loop, timeline strip, and risk matrix.
- [patterns.yml](library/patterns.yml) is the canonical source for starter compositions: process branch, dependency boundary, lifecycle stack, and evidence/inference split.
- [user-shapes-template.yml](library/user-shapes-template.yml) is the canonical template for custom shapes, charts, and patterns when the target has a domain-specific form.
- Markdown files in [library/](library/) are companion docs for reading and navigation.

Add your own shape, chart, or pattern when the starter set cannot represent the target honestly. Custom visuals should name the lane served and the source evidence or inference they represent.

## Use When

- a user supplies context and wants to understand it step by step,
- the target is an object, artifact, architecture, codebase, process, workflow, plan, or mixed system,
- an HTML explanation page is a useful output format,
- properties, components, internal dependencies, external dependencies, flow, lifecycle, and open questions matter,
- visual or diagram-like structure would clarify the target.

## Do Not Use When

- the user only wants a short text summary,
- the task is direct implementation rather than explanation,
- the source context is too sensitive to transform into a generated artifact,
- the target is too broad and no bounded scope is provided,
- the output needs a production-grade visual renderer,
- live experiment evidence is required but has not been collected.

## Ownership Model

| Capability | Owner |
| --- | --- |
| Seed execution | Task Session |
| Sigil lifecycle | Sigil Development |
| Experiment mechanics | Experiment Harness |
| Runtime handoff | Codex Goal adapter when strict coverage passes |
| Promotion readiness | Sigil Development after live examples |

## Development

The original seed work-pack lives at [development/WORK-PACK.md](development/WORK-PACK.md).

The visual layered revision artifacts live under [development/invoke-runs/20260529T112301Z-visual-layered-xray](development/invoke-runs/20260529T112301Z-visual-layered-xray).

Promotion requires live examples for at least one object or component, one process, one architecture or codebase, one generated L0 HTML/SVG output, and one insufficient-context block or flag.
