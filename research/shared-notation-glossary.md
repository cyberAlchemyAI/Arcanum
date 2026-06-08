---
name: Shared Research Notation Glossary
description: Reusable local notation glossary for research towers that read mathematical or formal papers.
type: shared-notation-glossary
status: draft
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Shared Research Notation Glossary

This glossary is for local research towers. It teaches notation patterns used in
papers without promoting them into canonical Arcanum vocabulary.

Use it when a paper introduces symbols before the reader has built the local
mental model. Each research tower can point here and add a local bridge card for
paper-specific meanings.

## Reading Rules

- Preserve the paper's symbol first.
- Explain the object type before the analogy.
- Keep Arcanum readings explicitly marked as analogy.
- Do not convert mathematical notation into Arcanum canon.
- If the same symbol is overloaded by a paper, define the local meaning in that tower.

## Core Notation Patterns

| Notation | Generic reading | How to read it aloud | Arcanum-safe analogy | Misuse warning |
| --- | --- | --- | --- | --- |
| `X -> Y` | A map, morphism, function, kernel, model, or process from domain `X` to codomain `Y`, depending on context. | "`X` to `Y`." | A declared input/output boundary. | Do not assume it is an ordinary deterministic function. |
| `p : X -> Y` | Object `p` has type or direction from `X` to `Y`. | "`p` is a map/model from `X` to `Y`." | A named route step with declared boundary. | The colon states typing; the arrow states direction/shape. |
| `1` | Often a terminal/unit object or singleton-like space. | "unit" or "one." | A closed/no-input or no-extra-boundary surface. | Do not read it as the number one unless the paper does. |
| `X x Y` | Product/pairing of `X` and `Y`. | "`X` times `Y`." | A receipt carrying both parts. | It is structural pairing, not multiplication in every context. |
| `pi` | Often a prior, belief state, distribution, or parameter-like variable depending on paper. | "pi." | Current state namespace or belief handle. | Always check local paper meaning. |
| `c_* pi` | Pushforward of `pi` through `c`; the belief/state after applying `c`. | "`c` pushforward of pi." | State namespace after a route step. | Do not drop the state index in reverse reasoning. |
| `c'` | A related or inverse/approximate object, depending on paper. | "`c` prime." | Companion handoff/inversion candidate. | Prime notation is paper-specific. |
| `c^dagger` | Often an exact inverse/adjoint/dagger object. | "`c` dagger." | Ideal reverse handoff, analogy only. | Dagger has domain-specific meanings. |
| `Theta` | Parameter space. | "theta." | Declared knob space. | Not every variable is a parameter. |
| `F^c` | A quantity `F` attached to object `c`, often a loss/free energy in AutoBayes. | "`F` of/for `c`." | Local objective/evidence receipt. | Do not turn all scores into losses. |
| `l^c` | A local likelihood/energy-like term attached to `c` in AutoBayes. | "`ell` of `c`." | Local fit pressure. | Paper-specific; do not generalize blindly. |
| `H^c` | A local entropy/regularizer-like term attached to `c` in AutoBayes. | "`H` of `c`." | Local constraint/spread pressure. | Not a governance guardrail by itself. |
| `E[...]` | Expectation under a distribution/process. | "expected value of ..." | Averaging a local receipt under a stated state. | Ask "under which distribution?" |
| `~` | "Distributed as" or sampled from. | "is sampled from." | Produced under a source state. | It is probabilistic, not mere similarity. |
| `:=` | Definition by assignment. | "is defined as." | Local definition. | Do not treat it as an observed result. |
| `≅` / `~=` | Isomorphism/equivalence-like relation. | "is isomorphic/equivalent to." | Same structure for the current purpose. | Not necessarily literal equality. |
| `C(A, B)` | Homset of morphisms from `A` to `B` in category `C`. | "`C` from `A` to `B`." | Typed handoff space for one input and one output. | Do not read it as function application. |
| `C(A1 ... An; B)` | Multicategory homset of multimorphisms from a list of inputs to output `B`. | "`C` from `A1` through `An` to `B`." | Multi-input handoff surface. | The semicolon separates input list from output. |
| `ob(C)` | Objects of category or multicategory `C`. | "objects of `C`." | Declared nodes in a context. | It is not the morphism/edge set. |
| `1_A` | Identity morphism on object `A`. | "identity on `A`." | No-op receipt for a boundary. | Not a scalar one unless the source says so. |
| `o` / `circ` | Composition of morphisms or multimorphisms. | "after" or "composed with." | Sequential receipt composition. | Check the paper's order convention. |
| `b` | Tensor product or monoidal product in a monoidal category. | "tensor." | Composition that combines independent surfaces. | Not always vector-space tensor product. |
| `b_n` | n-fold tensor product functor in an unbiased monoidal category. | "`n`-fold tensor." | Variadic composition surface. | Do not collapse it to binary bracketing without coherence data. |
| `gamma` | Coherence isomorphism for reassociating or flattening tensor groupings. | "gamma coherence." | Boundary-normalization receipt. | It is structural evidence, not an arbitrary rewrite. |
| `iota` | Coherence isomorphism between identity functor and one-fold tensor. | "iota unit/one-fold coherence." | No-op-to-structured-boundary bridge. | Do not confuse with identity morphism. |
| `V(C)` | Underlying multicategory of an unbiased monoidal category `C` in this paper. | "`V` of `C`." | Re-encoding functor that exposes multi-input operations. | Paper-specific construction. |

## Research-Tower Pattern

For a paper-specific notation card, use:

```text
symbol
source meaning
paper section / source kind
plain-language reading
local worked example
Arcanum analogy
misuse warning
promotion scope
```

## Reuse Policy

Other research towers may reference this file directly. They should not copy the
whole table unless they need local modifications. If a new paper uses the same
symbol differently, the local tower's notation bridge owns that difference.
