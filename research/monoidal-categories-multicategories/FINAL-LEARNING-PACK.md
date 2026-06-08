---
profile: monoidal-categories-multicategories
name: Final Learning Pack
type: final-learning-pack
status: pass-standard
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Final Learning Pack

## One Sentence

Monoidal categories and representable multicategories are equivalent because
coherent tensor products and canonical multi-input factorization encode the same
composition structure from opposite directions.

## Source-First Spine

| Layer | Source meaning | Closure artifact |
| --- | --- | --- |
| Category basics | Objects, morphisms, composition, identities, functors, natural transformations, equivalence. | [GLOSSARY.md](GLOSSARY.md), [DEFINITIONS.md](DEFINITIONS.md) |
| Monoidal structure | Tensor product, unit, associator/unitors, coherence. | [NOTATION.md](NOTATION.md), [DEFINITIONS.md](DEFINITIONS.md) |
| Unbiased monoidal structure | n-fold tensor functors with `gamma` and `iota`. | [DEFINITIONS.md](DEFINITIONS.md) |
| Multicategory structure | Multi-input, one-output multimorphisms with composition. | [GLOSSARY.md](GLOSSARY.md) |
| Representability | Canonical representing objects and universal factorization. | [DEFINITIONS.md](DEFINITIONS.md) |
| Equivalence proof | Construct `V`, restrict to `RMulticat`, prove full, faithful, essentially surjective. | [tracks/equivalence-spine-card.md](tracks/equivalence-spine-card.md) |

## Notation Reading

Start with [NOTATION.md](NOTATION.md). The key conceptual move is reading
`C(A1 ... An; B)` as multi-input arrows and `C((A1 b ... b An), B)` as ordinary
morphisms out of a packed tensor object.

## Arcanum Operator Model

```text
Before claiming two workflow surfaces are equivalent:
  - name the objects/operations in each surface;
  - define how multi-input material is packed;
  - require a universal or canonical factorization receipt;
  - prove structure-preserving maps in both directions;
  - block the claim if the translation only works informally.
```

## What To Borrow Carefully

- Coherence receipts for rearrangement freedom.
- Representability as a test for when multi-input surfaces can be safely packed.
- Full/faithful/essentially-surjective as a lens for comparing encodings.

## What To Keep Analogy-Only

- Monoidal categories.
- Multicategories.
- Universal multimorphisms.
- Coherence isomorphisms.
- Underlying multicategory functors.

## What To Block

- "Multi-input" equals "representable."
- "Equivalent" equals "identical implementation."
- "Tensor" as a generic Arcanum combine verb.
- Canonical vocabulary promotion from this local research run.

## Closed Residue Summary

| Residue | Closure |
| --- | --- |
| MCM.1 theorem | Closed through equivalence spine card. |
| MCM.2 notation | Closed through notation bridge and shared notation additions. |
| MCM.3 monoidal-to-multicategory bridge | Closed through definitions and theorem card. |
| MCM.4 representability boundary | Closed through glossary, definitions, and distill. |
| MCM.5 Arcanum bridge | Closed through bridge decision. |

## Remaining Honest Cutoff

The tower is closed for standard operator understanding and Research Tower sigil
testing. It is not closed for full proof audit, external literature validation,
or formalization.

## Sources

- Primary source: `/mnt/c/Users/vlad_/Downloads/Monoidal Categories and Multicategories.pdf`.
- Related sources are only used as cited by the paper's bibliography; no
  independent external source expansion was performed.

