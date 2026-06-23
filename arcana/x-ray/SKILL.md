---
name: x-ray
description: "Use when: turning user-supplied context about an object, artifact, architecture, codebase, process, or system into a visual layered HTML explanation page with properties, components, flows, dependencies, and evidence boundaries."
argument-hint: "<context-or-path> [--mode object|artifact|architecture|codebase|process|mixed] [--depth quick|standard|deep] [--output <html-path>]"
tier: arcana
domain: context-explanation
version: 0.2.0-seed
origin: revised from visual layered x-ray refine and invoke define/design/plan artifacts
allowed-tools: Read, Write, Glob, Grep, AskQuestions, Bash
---

# Sigil: x-ray

<objective>
Dissect a target object, artifact, architecture, codebase, process, or mixed context into explanation lanes, then compose those lanes into a local visual HTML x-ray page where layers can be stacked, isolated, compared, or traced.
</objective>

<logic-type>
Arcana: dispatch-spec governed explanation and visual-structure orchestration for hidden target structure.
</logic-type>

<status>
Seed. This contract defines the revised lane model, renderer ladder, and validation surface. It is not promoted and does not yet prove live reusable behavior.
</status>

<modes>
Supported inspection modes:

| Mode | Use When | Required Emphasis |
| --- | --- | --- |
| `object` | The target is a bounded conceptual, data, or domain object. | properties, relationships, lifecycle, dependencies |
| `artifact` | The target is a document, spec, plan, deck, or generated artifact. | intent, structure, claims, evidence, gaps |
| `architecture` | The target is a system, subsystem, component graph, or design architecture. | components, boundaries, flows, internal dependencies, external dependencies |
| `codebase` | The target is a repository, package, module, or source subtree. | entrypoints, modules, internal dependencies, external dependencies, tests, flows |
| `process` | The target is an operational, human, or system workflow. | actors, steps, decisions, transformations, handoffs |
| `mixed` | The target combines more than one shape. | explicit lane selection and omitted-lane reasons |
</modes>

<canonical-lanes>
Every run selects a bounded lane set. A lane is one vision of the target and must emit a handle that later composition can consume.

| Lane | Vision | Output Handle |
| --- | --- | --- |
| `surface` | What the target appears to be and why the user is inspecting it. | `surface.summary` |
| `properties` | Important attributes, invariants, metadata, constraints, and state. | `properties.catalog` |
| `components` | Internal parts and their purposes. | `components.map` |
| `internal_dependencies` | Dependencies among internal parts, modules, sections, stages, or concepts. | `dependencies.internal` |
| `external_dependencies` | Services, libraries, APIs, people, policies, documents, or systems outside the target. | `dependencies.external` |
| `flow` | Data, control, work, or meaning movement through the target. | `flow.graph` |
| `lifecycle` | Creation, operation, mutation, validation, failure, and retirement states. | `lifecycle.timeline` |
| `risk_questions` | Ambiguity, missing evidence, contradiction, risk, and open questions. | `risk.questions` |
| `visual_composition` | Instructions for mapping lane handles to HTML, SVG, Mermaid, and optional 3D layers. | `visual.model` |
</canonical-lanes>

<renderer-ladder>
Use the smallest renderer that can explain the target clearly.

1. L0: single local static HTML page with semantic HTML, CSS, and inline SVG.
2. L1: conservative Mermaid source blocks for flow, dependency, and architecture diagrams.
3. L2: in-browser Mermaid rendering only when artifact policy allows it.
4. L3: CSS 3D transforms for depth-separated layer panels.
5. L4: optional Three.js or CSS3DRenderer for spatial exploration when a target genuinely benefits from 3D.
6. Optional external adapter: Kroki-generated SVG only when privacy, network, and local policy allow it.

L0 is the default proof path. Remote or 3D rendering must never be required for a valid `x-ray` result.
</renderer-ladder>

<applicability>
Use this sigil when:

- the user provides context and wants to understand what it is about,
- the target is an object, artifact, architecture, codebase, process, plan, workflow, or mixed system,
- important structure is hidden inside prose, code, diagrams, plans, or repository layout,
- the explanation should expose properties, components, flows, dependencies, transformations, assumptions, and open questions,
- a local HTML explanation page is the desired output surface,
- visual layers or diagram-like structure would make the target easier to inspect.
</applicability>

<non-applicability>
Do not use this sigil when:

- a short plain-language summary is enough,
- the user wants direct implementation instead of explanation,
- the source context is too sensitive to transform into a generated artifact,
- the target is too large and the user has not provided a bounded scope,
- a production renderer or polished design system is required immediately,
- there is not enough context to identify the object under inspection.
</non-applicability>

<inputs>
Expected inputs:

- supplied context text or a path to local context,
- optional inspection mode: `object`, `artifact`, `architecture`, `codebase`, `process`, or `mixed`,
- optional user question or intent,
- optional output path for the HTML page,
- optional depth, audience, privacy, or visual style constraints.
</inputs>

<reader-onramp>
An `x-ray` page must teach the target to a reader who may not already know the domain.

Before composing the visual page, identify the likely reader baseline from the user request or source context:

- `newcomer`: needs plain definitions, why-it-matters framing, and step-by-step causality.
- `working-reader`: understands the domain category but not this target's local structure.
- `expert`: can handle compact terms, but still needs local evidence and boundary clarity.
- `unknown`: default to `newcomer` for explanation text and `working-reader` for labels.

For every important lane, provide an on-ramp before the detail:

1. Name the thing in ordinary language.
2. Say why it matters in this target.
3. Explain what changes, moves, depends on it, or can fail because of it.
4. Only then introduce local terms, handles, or technical labels.

When the target has dense vocabulary, use a local reader glossary pattern: plain term, plain meaning, why it matters here, source or lane, and misuse warning. Keep this glossary explanatory; do not promote local x-ray terms into canonical project definitions.

When the page has multiple visual layers, give each layer a reader outcome: what the reader should understand after inspecting that layer and why the layer matters to the target.

Avoid explanations that require prior knowledge of the target's domain vocabulary. If a technical term is unavoidable, define it where the reader first needs it. Visual labels may be compact, but adjacent text must make the label understandable.
</reader-onramp>

<process>
1. Resolve the input context and identify the target boundary.
2. Select an inspection mode or ask one clarification question when mode ambiguity changes the lane set.
3. Identify the reader baseline and explanation depth from the request; when unknown, default to newcomer-friendly prose.
4. Build an evidence boundary that separates source-backed facts from inference.
5. Select the required lanes for the mode and record omitted-lane reasons.
6. Produce lane handles for surface, properties, components, internal dependencies, external dependencies, flow, lifecycle, risk questions, and visual composition as relevant.
7. Add reader on-ramps for important lane content: plain name, why it matters, causal role, then local or technical term.
8. Select YAML-backed visual library components and patterns from `arcana/x-ray/library/` that fit the lane handles.
9. Nudge the user to add a custom shape, chart, or pattern when the target has a domain-specific form that the starter library cannot represent honestly.
10. Compose the lane handles into an HTML page model with selectable visual layers, local reader glossary entries, layer reader outcomes, and scan-friendly explanatory blocks.
11. Use L0 static HTML/SVG by default; add Mermaid or 3D adapters only when they clarify the target and validation remains available.
12. Validate that every visual element maps back to source evidence or an explicit inference, and that every important technical label has a nearby plain-language explanation.
13. Report missing context, unsupported visual adapters, or target-size blockers honestly.
</process>

<output-contract>
Return:

```markdown
## x-ray Result

- Status: pass | flag | block
- Mode: object | artifact | architecture | codebase | process | mixed | unknown
- Target boundary: <resolved scope or blocked reason>
- User intent: <resolved intent or open question>
- Reader baseline: newcomer | working-reader | expert | unknown
- Output: <html path or planned output>
- Lane handles:
  - surface: <handle or omitted reason>
  - properties: <handle or omitted reason>
  - components: <handle or omitted reason>
  - internal_dependencies: <handle or omitted reason>
  - external_dependencies: <handle or omitted reason>
  - flow: <handle or omitted reason>
  - lifecycle: <handle or omitted reason>
  - risk_questions: <handle or omitted reason>
  - visual_composition: <handle or omitted reason>
- Layer interaction: stacked | isolate | compare | trace | planned
- Renderer level: L0 | L1 | L2 | L3 | L4 | blocked
- Visual library: <YAML components/patterns used and custom shape/chart/pattern nudge if relevant>
- Evidence boundary: <source-backed facts vs inference>
- Reader on-ramp: <plain-language definitions, why-it-matters framing, or omitted reason>
- Validation: <checks performed or blocked reason>
```
</output-contract>

<quality-bar>
A successful `x-ray` run must:

- identify the mode and target boundary,
- preserve the user's inspection intent,
- produce a structured explanation rather than a loose summary,
- teach prerequisite concepts before relying on target-specific jargon,
- make each important technical label understandable to a reader without assumed prior domain knowledge,
- include properties, components, flows, internal dependencies, external dependencies, assumptions, and open questions when relevant,
- emit lane handles that can be consumed by the visual composition step,
- use reusable YAML-backed visual components and patterns only when they preserve the evidence/inference boundary,
- make the HTML visual layer model inspectable without requiring remote services,
- keep generated visual structure tied to the source context,
- distinguish evidence from inference,
- report blockers when context is insufficient or the target is too broad,
- preserve seed status until Sigil Development and Experiment Harness evidence support promotion.
</quality-bar>

<anti-patterns>
Avoid:

- inventing system structure not grounded in supplied context,
- producing decorative visuals that do not explain the target,
- skipping the user's intent and defaulting to generic documentation,
- using expert shorthand where the reader needs a plain-language bridge,
- drawing labels, arrows, or layers whose meaning is only clear to someone who already understands the target,
- treating every target as software architecture,
- claiming production renderer readiness from seed artifacts,
- requiring Mermaid, Three.js, Kroki, or remote rendering for baseline success,
- using 3D to make the page impressive when simple SVG would explain better,
- analyzing an entire codebase when the user provided no bounded scope,
- promoting the sigil before live examples exist.
</anti-patterns>

<observability>
For meaningful executions, record:

- mode,
- target boundary,
- input size and source shape,
- clarification needed or not,
- selected lanes and omitted-lane reasons,
- renderer level,
- output path or blocked reason,
- evidence/inference boundary quality,
- internal and external dependency coverage,
- missing-context gaps,
- user correction signals.

Additionally record these UX-and-rework signals (added 2026-06-23 from the componentize/workflow-reflect run, which found the default reflection trigger fires on invocation count, not on any quality signal — so iteration cost was invisible):

- `renderer_level_attempted` and `renderer_level_shipped` (L0–L4) — a downgrade delta is the single most informative UX signal, e.g. an attempted 3D layer shipped as L0,
- `renderer_downgrade_reason` (readability | validation | perf | mobile),
- `ux_revision_count` — post-first-render layout reworks in the run,
- `interaction_defects_found` (overlap | hover-trap | hardcoded-spacer | mobile-illegible | z-index-collision),
- `ux_validation_evidence` (none | screenshot | playwright | manual),
- `validator_status` (pass | block | n-a-bespoke) so the share of unvalidatable artifacts is visible,
- `lane_genre` (orthogonal-toggle | ordered-ladder | graph).

Reflection thresholds should be evidence-based, not clock-based: trigger reflect-now when `ux_revision_count >= 2` in a run, OR `interaction_defects_found` is non-empty, OR `renderer_level_attempted > renderer_level_shipped` recurs across >= 2 runs, OR `validator_status: n-a-bespoke` exceeds a share of recent x-ray runs.
</observability>

<promotion-gate>
Promotion requires Sigil Development review plus Experiment Harness evidence for:

- one object or component example,
- one process example,
- one architecture or codebase example,
- one generated L0 HTML/SVG output body,
- one blocked or flagged example showing insufficient context handling,
- one validation pass that checks lane presence, evidence boundaries, and HTML structure.
</promotion-gate>
