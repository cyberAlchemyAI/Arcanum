---
profile: autobayes-research
name: Parameter Exposure Card
description: Source-backed local definition card for parameter exposure and parameterized statistical games.
type: definition-card
status: pass
lane: parameter-exposure-card
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Parameter Exposure Card

## Source Kind

- AutoBayes paper: section 5, "Optimization via Functorial Semantics."
- Local receipt: [semantics-functor-reader.md](semantics-functor-reader.md).
- Related source context: [Bayesian Learning Rule](https://arxiv.org/abs/2107.04562) as optimization-semantics background through the existing crosswalk.

## Source Meaning

A statistical game has a loss, but a loss alone does not say what an optimizer
is allowed to change. AutoBayes therefore introduces parameterized statistical
games:

```text
(Theta, c)
```

where:

- `Theta` is a parameter space;
- `c` maps each parameter value to a statistical game;
- the parameter may affect the model, inversion, energy, entropy, or distribution-family annotation.

Parameter exposure is the layer that turns "this object has a loss" into "this
object has declared handles an optimizer may act on."

## Arcanum Reading

For Arcanum, this is the cleanest bridge into automation discipline:

```text
Before a runtime or task automates anything, name the knobs it may touch.
```

Examples:

- A Task Session write scope is not just a file list; it is a set of mutation handles.
- A runtime adapter choice is not merely execution metadata; it can determine which semantics interprets the declared route.
- A parameter is not any variable in context. It is an exposed handle with authority.

## Misuse Warnings

- Do not call every context field a parameter.
- Do not treat "optimizer" as the owner of model structure.
- Do not hide parameter exposure inside a final synthesis.
- Do not import `Theta` notation into Arcanum contracts unless a later decision gate approves it.

## Operator Sentence

```text
The optimizer can only act on handles the model has exposed.
```

Arcanum version:

```text
Automation can only mutate knobs the route declared and the owner authorized.
```

## Status

`closed-definition`

## Residue

Future Arcanum work may test whether task-session reports should distinguish
ordinary context, write scope, runtime choice, and optimizable knobs more
sharply. That is a proposed work-pack candidate, not a mutation in this tower.
