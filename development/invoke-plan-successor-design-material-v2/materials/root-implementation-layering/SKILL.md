---
name: implementation-layering
description: "Use when: creating or evolving a project-agnostic implementation layering model for a feature, capability, product workflow, research workflow, infrastructure change, or system improvement. Builds layers from minimum working unit proof to progressive hardening using value/cost layer-boundary heuristics."
argument-hint: "<target-name> [--path <output-path>] [--update]"
tier: transmutations
domain: implementation-planning
version: 0.1.0
origin: generalized from recurring implementation-planning practice
allowed-tools: Read, Write, Glob, Grep
---

<objective>
Create or evolve a project-agnostic implementation layering model where Layer 0 is the smallest minimum working unit that proves the concept, and each later layer deliberately improves the previous layer without invalidating earlier guarantees.
</objective>

<logic-type>
Transmutation: bounded synthesis from target context into a minimum-proof implementation layering model.
</logic-type>

<applicability>
Use this skill for any project that needs to sequence implementation scope before building, including:

- product features,
- internal tools,
- research workflows,
- infrastructure changes,
- process automation,
- data pipelines,
- agentic or human-in-the-loop systems.
</applicability>

<inputs>
Expected inputs, if available:

- target name, capability name, feature name, or workflow name,
- existing requirements, specs, issues, PRDs, ADRs, README sections, or roadmap notes,
- existing implementation files or tests,
- known constraints such as budget, timeline, team size, safety, compliance, reliability, or pilot needs.
</inputs>

<default-output>
If the user does not provide `--path`, write the artifact to the first suitable location:

1. `docs/{target-name}/implementation-layering.md` when a target-specific docs folder exists,
2. `docs/implementation-layering.md` when project-level docs exist,
3. `implementation-layering.md` at the project root when no docs folder exists.
</default-output>

<template>
Use `templates/implementation-layering.md` as the starting point.
</template>

<process>
1. Identify the target and output path. If the target or output path is ambiguous, infer a conservative default from existing project docs and name it in the result.
2. Gather only relevant context: requirements, specs, user stories, existing architecture notes, README sections, issues, tests, and implementation files that define the target behavior.
3. Define Layer 0 as the minimum working unit POC: the smallest end-to-end slice that proves the target concept can work.
4. For every layer, write the layer decision question using this form: "After this layer, we know whether ...".
5. Apply the layer-boundary heuristic:
   - `Layer value = decision unlocked + user-visible outcome + risk reduced`
   - `Layer cost = implementation time + verification time + coordination burden`
   - Stop a layer when the next unit of work adds less value-per-cost to the current decision than starting the next decision layer.
6. For each layer, document:
   - decision question,
   - minimum working unit,
   - included scope,
   - explicitly deferred scope,
   - user-visible or operator-visible outcome,
   - risk reduced,
   - main cost drivers,
   - exit evidence,
   - promotion decision.
7. Make each later layer build on the previous layer by adding one bounded improvement theme, such as repeatability, reliability, policy depth, observability, degraded-mode behavior, scale, or packaging.
8. Preserve non-regression: state which guarantees from earlier layers must remain true.
9. Prefer 3 to 5 layers. Add more only when each layer unlocks a distinct decision.
10. Summarize the recommended next implementation layer and the most important deferred scope.
</process>

<quality-bar>
A good implementation layering artifact:

- lets the team start with the smallest useful proof,
- avoids mixing pilot, scale, fallback, and polish into the POC,
- makes deferrals explicit rather than accidental,
- makes promotion decisions evidence-based,
- balances working length against value delivered,
- can be understood by both implementation agents and human reviewers.
</quality-bar>

<anti-patterns>
Avoid:

- calling a layer "POC" while including production-scale concerns,
- creating layers that are just task buckets without decision questions,
- advancing to scale before repeatability is proven,
- making layer boundaries by component ownership alone,
- deferring verification until the final layer,
- adding a layer when it does not unlock a new decision.
</anti-patterns>

<output-contract>
Return:

```markdown
## Implementation Layering Result

- Target: <target-name>
- Artifact: <path>
- Mode: created | updated
- Layer count: <n>
- Recommended next layer: <L0/L1/...>
- Boundary heuristic: applied
- Key decision unlocked by L0: <decision>
- Major deferred scope: <summary>
- Validation: <checks performed or not run>
```

</output-contract>
