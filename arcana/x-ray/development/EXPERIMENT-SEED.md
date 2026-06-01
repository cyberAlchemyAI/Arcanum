# x-ray Experiment Seed

## Purpose

Define the first live example branches needed before `x-ray` can move beyond seed status.

## Branches

| Branch ID | Focus | Prompt Shape | Expected Evidence |
| --- | --- | --- | --- |
| XRAY-COMPONENT-001 | component | Explain a bounded component from a supplied README or code excerpt. | HTML output shape includes purpose, inputs, outputs, collaborators, and relationships. |
| XRAY-PROCESS-001 | process | Explain a workflow or operational process from notes. | HTML output shape includes actors, steps, decision points, data flow, and transformations. |
| XRAY-ARCH-001 | architecture or plan | Explain an architecture/design plan from supplied planning context. | HTML output shape includes system overview, entities, dependencies, flows, assumptions, and open questions. |
| XRAY-BLOCK-001 | insufficient context | Ask x-ray to explain too little or contradictory context. | Result blocks or flags with missing-context questions rather than inventing structure. |

## Harness Expectations

When Experiment Harness is initialized for `x-ray`, it should:

- use the `sigil-development` profile,
- preserve real user-facing output bodies,
- reject save-summary outputs,
- require at least one HTML-shaped result,
- keep promotion blocked until all required branches have live evidence.

## Initial Output Shape

The first HTML-shaped result should include:

- title,
- context summary,
- intent/focus,
- overview section,
- actors/entities section,
- flow or transformation section,
- relationships section,
- assumptions,
- open questions,
- evidence boundary.
