# Refine Seed: x-ray

## Source

This seed was materialized from the `refine` live experiment output:

- Prompt: `arcana/refine/development/example-prompts/sigil-new-low.md`
- Output: `arcana/refine/development/example-outputs/sigil-new-low.output.md`
- Review: `arcana/refine/development/LIVE-XRAY-RUN-REVIEW.md`

## Refined Intent

`x-ray` should become an Arcana sigil that accepts user-supplied context and creates a visual-first HTML explanation surface that helps the user navigate the knowledge being x-rayed.

The sigil should support components, plans, architectures, processes, repositories, and systems. It should clarify what is being analyzed, identify the important knowledge surfaces, and produce candidate visual structures that can be selected or adapted for the object being x-rayed.

## North Star

The primary result should feel like a visual way to move through the known context, not a text report with occasional diagrams.

The user should be able to inspect the x-rayed knowledge by moving through visual entry points such as system maps, relationship graphs, flow diagrams, actor/entity views, timelines, or layered architecture views. Text should explain what the user is looking at, reveal assumptions and open questions, and connect the visual pieces into a coherent understanding. The explanation surface should also allow text to expand into more detailed descriptions when the user wants to inspect a concept, relationship, step, assumption, or unresolved question more deeply.

Refinement outcomes should include different template structure candidates for different x-ray targets. A component, process, plan, architecture, subsystem, repository, or large system may need a different visual explanation model rather than one universal layout.

Large objects should support layers of explanation. If the object is big enough, such as a whole repository, the result should not try to explain everything through one visualization. It should provide a navigable layered model where the user can move from high-level orientation into focused views.

The visual interface should highlight the concepts that matter most inside the object being x-rayed. Important concepts, central relationships, risky assumptions, core flows, and decision points should become visible landmarks in the interface.

## Expected Explanation Surface

The initial `x-ray` design should account for:

- overview,
- actors,
- entities,
- data flow,
- transformations,
- process steps,
- relationships,
- layers of explanation,
- assumptions,
- open questions,
- important concepts and landmarks,
- a primary visual navigation model,
- multiple template structure candidates for different x-ray targets,
- constructed visual or diagram-like explanations,
- concise explanatory text that supports the visual model,
- expandable detailed descriptions for deeper inspection.

## Seed Boundary

This seed is not the finished `x-ray` sigil.

It exists so Task Session can execute `TASK-XRAY-SIGIL-001` from a real work-pack instead of blocking on a missing input path.

## Refinement Defaults

- Research mode: `research-if-gap-appears`
- Preset: `standard`
- Loop count: `2`
- Execution owner: `task-session`
- Lifecycle owner after package creation: `sigil-development`
- Runtime default: `codex`
- Goal route: `--via goal` when strict handoff coverage is available

## Promotion Constraint

Promotion is not in scope for the first task.

Promotion readiness should require live examples for at least:

- one component,
- one process,
- one architecture or plan.
