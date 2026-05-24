# Refinement Loop

## Identity

- Owner: `refine`
- Status: pilot
- Use for: concept, architecture, ontology, lifecycle, governance, research-informed synthesis, article-quality design, and unclear refinement targets.
- Avoid for: already-approved implementation tasks, simple direct edits, or tasks that already have a selected execution-ready SWU.

## Objective

Run bounded pre-task refinement before Task Session execution. The loop turns a vague target or design concern into an approved seed work-pack/task that Task Session can execute through Codex Goal.

## Ownership Boundary

- Refine owns target understanding, research offer, loop budget, seed proposal, confirmation, and lifecycle handoff.
- Invoke owns the phase artifacts it is asked to produce: define, design, and plan.
- Interrogation owns critique, blocker questions, and pass/flag/block verdicts.
- Distill owns tournament, compact repair, and validate passes.
- Research is bounded evidence gathering. It cannot override local repo evidence.
- Sigil Development owns reusable sigil lifecycle after the handoff.
- Task Session owns execution of the approved refinement-loop work-pack task or SWU after Refine preflight.

## Execution Rule

Refine prepares the loop. Task Session executes the approved loop through Codex Goal by dispatching the installed skill/sigil contracts when they are available. The loop is not valid if the execution merely labels hand-written prose as Context Builder, Invoke, Interrogation, Distill, or Sigil Development output.

Each dispatched stage must preserve one of:

- the stage artifact path,
- the stage observation envelope or invocation summary,
- a pass/flag/block verdict when the stage provides one,
- or an explicit blocked reason when the required skill is unavailable.

## Required Local Baseline

1. Build or consume a bounded context pack first.
2. Treat the context pack as the local evidence baseline.
3. Use context gaps and uncovered obligations to guide any extra local search.
4. Do not redo broad repository discovery unless the pack is missing required evidence.
5. If context coverage cannot support a coherent seed, return `BLOCK`.

## One Refinement Loop Unit

One refinement loop is the smallest complete executable unit that can produce a useful seed:

1. Task Session dispatches `context-builder`.
2. Task Session dispatches `invoke` in Define mode.
3. Task Session dispatches `interrogation`.
4. Research offer and decision record.
5. Task Session dispatches `distill`.
6. Task Session dispatches `invoke` in Redefine plus Design/Plan mode.
7. Task Session dispatches `sigil-development` handoff or produces final synthesis when sigil lifecycle work is not applicable.

The research offer is mandatory even when research is skipped. Record one of:

- `no-research`: use only local repository and supplied context.
- `bounded-research`: run one external comparison pass within the Research Bounds below.
- `research-if-gap-appears`: start local-first and ask again only if Interrogation or Distill identifies a named external-context gap.

`research-if-gap-appears` is the default when the user has not already chosen a research mode.

## Full Loop

The full loop expands the one-loop unit into additional critique, repair, and planning passes:

1. Task Session dispatches `context-builder`.
2. Task Session dispatches `invoke` Pass 1: Define.
3. Task Session dispatches `interrogation` Pass 1.
4. Research offer and bounded online research pass when selected or when a named external-context gap appears.
5. Task Session dispatches `distill` tournament.
6. Task Session dispatches `invoke` Pass 2: Redefine plus Design.
7. Task Session dispatches `interrogation` Pass 2.
8. Task Session dispatches `distill` repair pass.
9. Task Session dispatches `invoke` Pass 3: Plan.
10. Task Session dispatches final `interrogation`.
11. Final synthesis and Task Session handoff.

## Presets

| Preset | Loop Budget | Use When |
| --- | --- | --- |
| compact | One refinement loop without research unless selected. | The target is narrow and mostly local. |
| standard | One loop plus one repair/synthesis pass. | The target needs critique and repair but not a full tournament. |
| full | Full loop with research offer, tournament or repair as needed, plan, and final interrogation. | Architecture, lifecycle, governance, or multi-artifact development needs a strong seed. |
| deep | Full loop plus checkpoint before mutation-heavy delegation. | The target is high-risk, broad, or likely to span several follow-up tasks. |

## Loop Limits

- Context Builder: at most 1 pass.
- Invoke: at most 3 passes.
- Interrogation: at most 3 passes.
- Distill: at most 2 passes.
- Bounded online research: at most 1 pass.

If the same disagreement appears twice without new evidence, stop and record it as an open decision.

## Research Bounds

When research is selected:

- use at most 8 external sources,
- use max depth 2,
- prefer standards, research papers, official docs, mature OSS architecture docs, and well-cited essays,
- record what each useful source contributes,
- record what does not fit the local domain,
- label influence as evidence, analogy, or rejected alternative,
- never let online research override local repo evidence.

## Handoff Output

A completed refinement loop should produce either:

- a seed work-pack/task ready for Task Session and Codex Goal handoff,
- a Sigil Development handoff,
- or a `BLOCK` report with the smallest missing context, decision, write scope, validation surface, or handoff field.

The output must also include required-stage evidence for every stage selected by the preset.
