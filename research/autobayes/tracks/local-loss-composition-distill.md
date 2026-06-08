---
profile: autobayes-research
name: Local Loss Composition Distill
description: Source-backed loss-chain-rule reader for AutoBayes section 4.
type: track-receipt
status: pass
lane: loss-chain-rule-reader
last_updated: 2026-06-07
---

# Local Loss Composition Distill

## Lane Receipt

- Lane: `loss-chain-rule-reader`
- Result: `PASS`
- Scope: AutoBayes section 4, plus current local receipts.
- Primary source: [AutoBayes: A Compositional Framework for Generalized Variational Inference](https://arxiv.org/pdf/2503.18608), section 4, "Composing Complex Loss Functions".
- Local context: [GLOSSARY.md](../GLOSSARY.md), [DISTILLED-KNOWLEDGE.md](../DISTILLED-KNOWLEDGE.md), [sessions/full-mode-source-receipts.md](../sessions/full-mode-source-receipts.md), [tracks/open-model-definition-card.md](open-model-definition-card.md).
- Promotion guardrail: this is a local research distill. It does not promote AutoBayes vocabulary into canonical Arcanum glossary, ontology, sigil, spell, runtime, or inventory terms.

## Source Claim

AutoBayes section 4 asks how to evaluate approximate local inversions. It begins with divergence from the exact Bayesian inverse, then moves to variational free energy because exact posterior evaluation is usually intractable.

The paper's compositional move is:

```text
Bayesian lens
  + local energy / likelihood
  + local entropy / regularizer
  = statistical game

statistical games compose
  -> generalized free energies compose by a chain rule
```

This is not just "add losses together." The paper stresses that energy and entropy behave differently. Energies add locally. Entropy follows the same kind of pushed-forward-prior and reverse-posterior shape that already appeared in Bayesian inversion.

## Terms To Keep Separate

| Term | Source-First Meaning | Arcanum Reading | Misuse Warning |
| --- | --- | --- | --- |
| Divergence | A measure of how far an approximate inversion is from the exact inversion; section 4 begins with KL or relative entropy between `c'_pi(y)` and `c^dagger_pi(y)`. | A comparison between an attempted reverse handoff and the ideal one. | Do not call any disagreement or review gap a divergence. |
| VFE / EUBO / negative ELBO | Variational free energy; the paper notes it is also called evidence upper bound or negative evidence lower bound. It is KL plus negative marginal log likelihood. | A named objective that avoids direct exact-posterior evaluation. | Keep signs explicit: ELBO is maximized, negative ELBO/EUBO/VFE is minimized. |
| Energy / likelihood | The local fit term `l^c`; in VFE form, it is the part inside the posterior expectation, such as negative log model density and prior density contributions. | Local evidence pressure: how costly this local explanation is. | Do not treat every evidence score as AutoBayes energy. It is part of a statistical game. |
| Entropy / regularizer | The local term `H^c`; subtracted from expected energy in generalized free energy. | Local spread or constraint pressure on the inversion/posterior candidate. | Do not collapse entropy into Arcanum guardrails. It is a mathematical regularizer. |
| Generalized free energy | The loss `F^c(pi, y) = E[l^c] - H^c` attached to a statistical game. | A local objective receipt that can compose into a larger objective. | Do not make it a generic validation verdict. |
| Open free energy | The free energy of an open statistical game before composing in the prior term. It is missing the prior energy contribution. | Local objective pressure before the route is closed by upstream belief. | Do not mistake an open local objective for the final closed VFE. |
| Local loss composition | Sequential statistical games compose by adding energies and composing entropies through a posterior-indexed chain rule. | The parent route should not hand-derive a global objective if each local step carries the right receipt. | Do not equate this with ordinary sum-of-metrics dashboards. |

## VFE In Plain Language

AutoBayes defines variational free energy for a Bayesian lens `(c, c')` as:

```text
VFE(c, c')(pi, y)
  = KL(c, c')(pi, y) - log p_(c_Y bullet pi)(y)
```

The important alternative form is:

```text
VFE(c, c')(pi, y)
  = E_{(x,a) ~ c'_pi(y)}
      [ -log p_c(a, y | x) - log p_pi(x) ]
    - H(c'_pi(y))
```

Source reading:

- `c'` is the approximate inversion/posterior family.
- `-log p_c(a, y | x)` is the model-side energy.
- `-log p_pi(x)` is the prior-side energy.
- `H(c'_pi(y))` is the entropy of the approximate posterior.
- The exact inverse `c^dagger_pi` disappears from this form, which is why the bound is computationally useful.

Arcanum reading:

```text
Do not ask the final synthesis to compare against an unreachable ideal.
Attach local objective terms that can be evaluated through the declared handoff.
```

## Statistical Game Definition

Section 4 defines a statistical game `c : X -> Y` as:

```text
(c, c', l^c, H^c)
```

where:

- `(c, c')` is a Bayesian lens;
- `l^c : X x latent(c) x Y -> [0, infinity]` is energy or likelihood;
- `H^c : P X x Y -> [0, infinity]` is entropy or regularizer;
- the combined loss is:

```text
F^c(pi, y)
  = E_{(x,a) ~ c'_pi(y)} [ l^c(x,a,y) ]
    - H^c(pi,y)
```

The novelty, according to the paper, is the decomposition of free energy into energy and entropy with their different compositional behavior.

## How Sequential Losses Compose

Take two statistical games:

```text
c : X -> Y
d : Y -> Z
```

Their composite is:

```text
d after c : X -> Z
```

### Energy Composition

Energy is simple:

```text
l^(dc)(x,a,y,b,z)
  = l^c(x,a,y) + l^d(y,b,z)
```

Local reading:

```text
cost of composite explanation
  = cost of upstream local explanation
  + cost of downstream local explanation
```

This part behaves like an additive ledger.

### Entropy Composition

Entropy is not merely:

```text
H^c + H^d
```

It is:

```text
H^(dc)(pi,z)
  = E_{(y,b) ~ d'_(c_* pi)(z)} [ H^c(pi,y) ]
    + H^d(c_* pi,z)
```

Local reading:

```text
regularization of the composite
  = expected upstream regularization under the downstream reverse pass
  + downstream regularization using the pushed-forward prior
```

The downstream game must be indexed by `c_* pi`, the belief produced after pushing the prior through `c`. The upstream entropy is averaged over the downstream inversion's reconstruction of the intermediate `Y` and downstream latent `b`.

This is the same state-discipline lesson as the inversion chain rule: the reverse pass is only legal when the correct forward belief state is available.

## Free-Energy Chain Rule

The paper's theorem says:

```text
F^(dc)(pi,z)
  = E_{(y,b) ~ d'_(c_* pi)(z)} [ F^c(pi,y) ]
    + F^d(c_* pi,z)
```

So the global loss is:

```text
expected upstream local loss
  + downstream local loss
```

But "expected upstream local loss" is doing real work. It says the upstream loss is evaluated under the downstream inversion's reconstruction of the hidden intermediate state. The parent does not just add two scalar losses after the fact.

## Open Free Energy

Section 4 warns that a pure statistical game `c : X -> Y` with negative log likelihood and Shannon entropy gives:

```text
F^c(pi,y)
  = E_{x ~ c'_pi(y)} [ -log p_c(y | x) ]
    - H(c'_pi(y))
```

This is not yet the full VFE because it is missing:

```text
-log p_pi(x)
```

The reason is that `c` is open. Its prior has not been composed in as a prior game.

To get ordinary VFE:

```text
prior game pi : 1 -> X
c : X -> Y

c after pi : 1 -> Y
```

The prior game contributes:

```text
l^pi(x) = -log p_pi(x)
H^pi = 0
```

Then:

```text
F^(c pi)(*, y) = VFE(c, c')(pi,y)
```

This is the cleanest "open model" lesson for local losses: an open component can have a valid local objective without being the whole closed Bayesian objective.

## Arcanum Mental Model

```text
forward route:

  X -- c --> Y -- d --> Z

reverse/objective route:

  evidence at Z
      |
      v
  d' uses pushed-forward prior c_* pi
      |
      |-- reconstructs intermediate (Y plus downstream latent)
      |
      v
  c' uses original prior pi

local objective composition:

  energy:
    l^c + l^d

  entropy:
    expected H^c under downstream reverse reconstruction
    + H^d under pushed-forward prior

  free energy:
    expected F^c + F^d
```

Arcanum translation:

```text
Do not make a parent route infer the global objective from prose.
Each step should expose:
  - local forward declaration;
  - local reverse/handoff behavior;
  - local evidence pressure;
  - local regularization/constraint pressure;
  - state namespace needed to make the reverse pass legal.

The parent composes receipts; it does not rediscover the whole loss.
```

This is analogy-only, but it is a strong design lens for Arcanum:

```text
local validation/evidence signals should remain typed by their boundary,
not collapsed into a global "quality" number too early.
```

## Misuse Warnings

- Do not say "losses just add." Energies add; entropy/regularizer terms compose with a posterior-indexed expectation.
- Do not call every Arcanum validation result a local loss. AutoBayes local loss is a mathematical object attached to a Bayesian lens/statistical game.
- Do not treat open free energy as full VFE. Full VFE appears after the prior is composed in.
- Do not ignore the prior. In VFE, the energy has a model contribution and a prior contribution.
- Do not hide the state index. `c_* pi` is the forward belief state that makes the downstream reverse pass meaningful.
- Do not treat GVI decomposable losses as identical to AutoBayes categorical local composition. GVI supplies objective ingredients; AutoBayes adds model/lens/game composition laws.
- Do not promote this card into canonical Arcanum vocabulary. It is a local research bridge.

## Operator Distill

Smallest useful sentence:

```text
AutoBayes makes loss compositional by splitting local objective pressure into
energy, which adds, and entropy, which composes through the same belief-state
discipline as Bayesian inversion.
```

Arcanum-facing version:

```text
If a route step contributes evidence pressure and regularization pressure,
keep those receipts local and typed, pass the state that makes them legal,
then let the parent compose them mechanically instead of writing a global
objective by hand.
```

## Open Residue

- Work one numerical or symbolic two-step example where `Y` becomes latent in the composite and the local free-energy terms are evaluated.
- Build the `related-framework-crosswalk` so GVI, VFE/EUBO, BLR, PPL guides, and AutoBayes are compared without term drift.
- Build the `semantics-functor-reader` to separate the section 4 composition law from section 5 gradient and optimization semantics.

