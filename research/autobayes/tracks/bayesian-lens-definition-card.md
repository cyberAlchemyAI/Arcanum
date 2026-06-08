---
profile: autobayes-research
name: Bayesian Lens Definition Card
description: Source-backed local definition card for Bayesian lenses and inversion chain discipline.
type: definition-card
status: pass
lane: bayesian-lens-definition-card
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Bayesian Lens Definition Card

## Source Kind

- AutoBayes paper: section 3 as represented by the joined receipts.
- Related paper: [The Compositional Structure of Bayesian Inference](https://arxiv.org/abs/2305.06112).
- Local receipts: [full-mode-source-receipts.md](../sessions/full-mode-source-receipts.md), [open-model-definition-card.md](open-model-definition-card.md).

## Source Meaning

A Bayesian lens is the local research tower's name for the AutoBayes object that
pairs a forward open model with an inversion family indexed by a prior or belief
state. The forward part says how observations are generated. The reverse part
says how evidence at the observed boundary updates or reconstructs hidden and
unobserved structure.

The important closure point is indexing:

```text
forward model c : X -> Y
prior pi on X
observation y in Y
inverse c'_pi(y)
```

The inverse is not free-floating. It is meaningful relative to `pi`.

## Worked Open-Model Continuation

Start from two open models:

```text
c : X -> Y
d : Y -> Z
```

The forward composite is:

```text
d after c : X -> Z
```

For inversion, evidence arrives at `Z`. The downstream inverse for `d` must use
the prior that results from pushing `pi` through `c`:

```text
d'_(c_* pi)(z)
```

That downstream reverse pass reconstructs an intermediate `Y` value and
downstream latent data. Then the upstream inverse for `c` is evaluated with the
original `pi` and the reconstructed `Y`:

```text
c'_pi(y)
```

So the reverse pass is:

```text
z evidence
  -> d' using pushed-forward prior c_* pi
  -> reconstructed y
  -> c' using original prior pi
```

This is why the intermediate `Y` that became latent in the open-model composite
still matters. It is the handoff value that makes the upstream inverse legal.

## Arcanum Reading

```text
forward route step
  -> observed handoff boundary
  -> downstream result
  -> reverse reading only legal with the right upstream state namespace
```

The useful Arcanum shape is not "a Bayesian lens is a task-session handoff." The
safer shape is:

```text
A reverse handoff must name the state that makes the reverse move legal.
```

If a downstream artifact is used to reinterpret upstream context, the route
should record the prior/context namespace that authorizes that reinterpretation.

## Misuse Warnings

- Do not call every adapter or prompt a Bayesian lens.
- Do not ignore the prior/state index.
- Do not treat guide-program support coverage as the same thing as Bayesian inversion correctness.
- Do not promote `Bayesian lens` as canonical Arcanum vocabulary from this card.

## Status

`closed-definition`

The remaining Arcanum work is not mathematical definition work; it is a possible
future toy game for reverse-handoff legality.
