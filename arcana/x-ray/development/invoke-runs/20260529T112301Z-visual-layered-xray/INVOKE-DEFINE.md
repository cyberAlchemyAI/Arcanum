# Invoke Define: Visual Layered x-ray

Status: pass
Mode: define
Date: 2026-05-29
Target: `arcana/x-ray`

## Request

Author the define baseline for revising `x-ray` from a general HTML explainer seed into a dispatch-spec governed visual inspection sigil with modes, lanes, internal/external dependency views, and a layered HTML output.

## Canonical Sources Used

- `spells/invoke/README.md`
- `spells/invoke/define.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RESULT.md`

## Specification Baseline

`x-ray` explains a target by decomposing it into inspectable lanes. Each lane is one vision of the target and emits a named handle. The handles are composed into a local HTML artifact where layers can be stacked, isolated, compared, or traced.

## Target Types

| Mode | Definition |
| --- | --- |
| `object` | A bounded conceptual, data, or domain object. |
| `artifact` | A document, spec, plan, deck, generated output, or other durable artifact. |
| `architecture` | A system, subsystem, component graph, or deployment/design architecture. |
| `codebase` | A repository, package, module, or source subtree. |
| `process` | A workflow, operational routine, business process, or human/system sequence. |
| `mixed` | A target that legitimately combines multiple shapes. |

## Canonical Lanes

| Lane | Purpose |
| --- | --- |
| `surface` | Name what the target appears to be and why it is being inspected. |
| `properties` | Capture important attributes, invariants, metadata, state, and constraints. |
| `components` | Identify internal parts and their local responsibilities. |
| `internal_dependencies` | Show dependencies among target-internal parts. |
| `external_dependencies` | Show libraries, services, people, policies, APIs, or artifacts outside the target. |
| `flow` | Show data, control, work, or meaning movement. |
| `lifecycle` | Show creation, operation, mutation, validation, failure, and retirement states. |
| `risk_questions` | Preserve ambiguity, missing context, risks, contradictions, and open questions. |
| `visual_composition` | Define how lane handles map into SVG, Mermaid, and optional 3D layers. |

## Glossary

| Term | Definition |
| --- | --- |
| x-ray target | The object, artifact, architecture, codebase, process, or mixed context being inspected. |
| lane | A focused interpretation pass over the target. |
| layer | The visual representation of one or more lane handles in the HTML page. |
| handle | A structured output reference emitted by a lane for later composition. |
| evidence boundary | The distinction between source-backed facts and inferred explanatory structure. |
| renderer ladder | The staged renderer plan from static HTML/SVG to optional Mermaid/CSS3D/Three.js. |

## Decisions

- Keep L0 output local and static: HTML, CSS, and inline SVG.
- Treat Mermaid, CSS3D, Three.js, and Kroki as later adapters.
- Preserve seed status until experiment evidence exists.
- Route lifecycle quality through Sigil Development and execution through Task Session.

## Unresolved Gaps

- Live example evidence remains missing.
- The first implementation still needs a validation harness for lane presence and HTML parse checks.
- Browser validation is required once a generated HTML artifact exists.

## Next Route

`invoke design`

