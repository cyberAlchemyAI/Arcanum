# Research Decision: Refine Development Package

> Historical note: this research decision predates the dispatch-route Refine contract. Codex Goal adapter wording is historical; current Refine runtime readiness is expressed through `REFINE-DISPATCH.json` and `RUNTIME-HANDOFF.md`.

## Research Offer

Research was offered as part of the one-loop refinement seed.

Options:

| Option | Meaning | Decision |
| --- | --- | --- |
| No research | Use only local repository and supplied context. | not selected |
| Bounded research | Run one external comparison pass now. | not selected |
| Research only if gap appears | Start local-first, ask again only if Interrogation or Distill identifies a named external-context gap. | selected |

## Selected Mode

`research-if-gap-appears`

## Rationale

The local Arcanum contracts already define the relevant ownership boundaries:

- Task Session execution boundary,
- iterative refinement profile phase ownership,
- Codex Goal adapter strict handoff boundary,
- Sigil Development lifecycle ownership,
- Invoke work-pack creation responsibility.

No named external-context gap remains after Interrogation. External research would add cost without changing the first development package.

## Bounds If Research Is Later Triggered

Use the `REFINEMENT-LOOP.md` research bounds:

- max 1 research pass,
- max 8 external sources,
- max depth 2,
- prefer standards, official docs, mature OSS architecture docs, research papers, and well-cited essays,
- record each source as evidence, analogy, or rejected alternative,
- never override local repository evidence with external research.

## Status

Research offered and deferred until a named gap appears.
