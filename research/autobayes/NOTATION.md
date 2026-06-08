---
profile: autobayes-research
name: AutoBayes Notation Bridge
description: Local notation bridge from AutoBayes paper notation to shared research notation and Arcanum-safe readings.
type: notation-bridge
status: pass
last_updated: 2026-06-07
promotion_scope: local-research-only
shared_glossary: ../shared-notation-glossary.md
---

# AutoBayes Notation Bridge

This bridge makes the paper's early notation explicit for the AutoBayes tower.
It points to the reusable [shared notation glossary](../shared-notation-glossary.md)
and records the AutoBayes-specific meanings.

This is local research evidence only. It does not promote notation into
canonical Arcanum vocabulary.

## AutoBayes-Specific Notation

| Notation | Source meaning in AutoBayes | Plain reading | Arcanum-safe analogy | Primary local artifact |
| --- | --- | --- | --- | --- |
| `p : X -> Y` | An open model from unobserved space `X` to observed space `Y`. | Model `p` carries input-side uncertainty into observations. | Route-capable component with declared boundary. | [open-model-definition-card.md](tracks/open-model-definition-card.md) |
| `latent(p)` | Latent carrier of open model `p`. | Hidden structure carried by `p`. | State carrier, analogy only. | [open-model-definition-card.md](tracks/open-model-definition-card.md) |
| `p : X -> latent(p) x Y` | Kernel form of an open model. | Given `X`, the model produces hidden carrier plus observed output. | A step returns visible output plus hidden receipt state. | [open-model-definition-card.md](tracks/open-model-definition-card.md) |
| `q after p : X -> Z` | Sequential composition of open models. | `p` feeds `q`; the external output is `Z`. | Parent route joins local steps. | [open-model-definition-card.md](tracks/open-model-definition-card.md) |
| `latent(q after p) = latent(p) x Y x latent(q)` | Composite latent carrier includes the intermediate observed value `Y`. | What was locally visible can become globally hidden. | Intermediate handoff remains accountable after composition. | [open-model-definition-card.md](tracks/open-model-definition-card.md) |
| `c'` | Approximate/local inversion paired with model `c`. | Reverse or posterior candidate for `c`. | Reverse handoff candidate. | [bayesian-lens-definition-card.md](tracks/bayesian-lens-definition-card.md) |
| `c^dagger` | Exact Bayesian inverse of `c`, where used. | Ideal posterior/reverse object. | Ideal reverse handoff, analogy only. | [local-loss-composition-distill.md](tracks/local-loss-composition-distill.md) |
| `c'_pi(y)` | Inversion for `c` indexed by prior `pi` and observation `y`. | Reverse pass depends on both state and evidence. | Reverse handoff must name source state. | [bayesian-lens-definition-card.md](tracks/bayesian-lens-definition-card.md) |
| `c_* pi` | Prior `pi` pushed forward through `c`. | Belief state after running `c`. | State namespace after a route step. | [bayesian-lens-definition-card.md](tracks/bayesian-lens-definition-card.md) |
| `l^c` | Energy / likelihood-like local loss attached to `c`. | Local fit pressure. | Local evidence pressure. | [local-loss-composition-distill.md](tracks/local-loss-composition-distill.md) |
| `H^c` | Entropy / regularizer-like local term attached to `c`. | Local spread/regularization pressure. | Constraint pressure, analogy only. | [local-loss-composition-distill.md](tracks/local-loss-composition-distill.md) |
| `F^c(pi,y)` | Generalized free energy for game `c` at prior `pi` and observation `y`. | Local objective value with state and observation. | Typed local objective receipt. | [two-step-symbolic-loss-calculation.md](tracks/two-step-symbolic-loss-calculation.md) |
| `Theta` | Parameter space for a parameterized statistical game. | The set/space of legal optimization handles. | Declared knob space. | [parameter-exposure-card.md](tracks/parameter-exposure-card.md) |
| `cup`, `cap`, `reveal`, `copier` | Open-model operations controlling how boundaries are bent, revealed, or copied. | Boundary-shift / structural operators. | Receipt boundary-shift analogy only. | [cups-caps-boundary-shift-card.md](tracks/cups-caps-boundary-shift-card.md) |

## Operator Reading

When the paper introduces notation, read it in this order:

```text
symbol
  -> object type
  -> source state or boundary
  -> what composes
  -> what becomes hidden or exposed
  -> only then, Arcanum analogy
```

## Misuse Warnings

- Do not read every arrow as a deterministic function.
- Do not erase whether a symbol is source state, observed output, latent carrier, or parameter.
- Do not translate notation into sigil/spell language before its paper role is clear.
- Do not promote AutoBayes notation into canonical Arcanum vocabulary.
