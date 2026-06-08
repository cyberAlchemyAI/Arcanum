---
profile: autobayes-research
name: AutoBayes Research Tower Definition
description: Operating definition for the AutoBayes research-control tower.
type: tower-definition
status: active
last_updated: 2026-06-06
---

# AutoBayes Research Tower

## 0. Operating Definition

Let:

- `L0` be the paper and related-paper corpus.
- `P_n : L_n -> L_{n+1}` be the promotion that turns unresolved understanding into explicit research objects.
- `Carrier(mu_n)` be the set of named obligations produced by auditing level `n`.

This tower is:

```text
L0 corpus
  -> L1 residue map
  -> L2 closure plan
  -> L3 Arcanum interface
  -> Lomega cutoff / scope
```

It follows the `../domainspec-lean-formalization/research-gpt` example: a research folder is healthy only when its residues are named, typed, actionable, and closed or promoted.

## 1. Translation Discipline

The paper's native terms stay visible. Arcanum translations are second-order handles, not replacements.

Example:

```text
open model
  paper role: composable probabilistic model with unobserved, observed, and latent spaces
  Arcanum reading: a composable capability surface whose hidden intermediate state must be carried honestly
```

The research may say "this feels like a sigil/spell boundary," but it must also keep the paper's exact mathematical object visible.

## 2. Claim Kinds

Every claim must be tagged:

- `source-claim`: the paper or related paper says it.
- `derived-reading`: a careful paraphrase from source structure.
- `arcanum-analogy`: useful for the operator, not a formal equivalence.
- `candidate-bridge`: possible future Arcanum design implication.
- `implementation-risk`: something that would matter if we tried to build with it.
- `open-question`: needs more source work.

## 3. Residue Pathologies

| Pathology | Meaning |
| --- | --- |
| `term-drift` | paper term and Arcanum term sound similar but differ |
| `missing-source` | related paper must be read before closure |
| `missing-example` | a definition needs a worked example |
| `bridge-risk` | Arcanum analogy may overstate the mapping |
| `implementation-gap` | paper leaves implementation future work |
| `optimization-semantics-risk` | optimization is being confused with model syntax |
| `promotion-risk` | research output might be mistaken for canonical Arcanum vocabulary |

## 4. Closure Modes

### Source Closure

The item closes by citation-backed reading from the AutoBayes paper or a related paper.

### Definition Closure

The item closes by becoming a stable local definition in [DEFINITIONS.md](DEFINITIONS.md).

### Distill Closure

The item closes by becoming a small reusable operator-facing model in [DISTILLED-KNOWLEDGE.md](DISTILLED-KNOWLEDGE.md).

### Negative Closure

The item closes by showing that an Arcanum mapping is misleading, too broad, or not worth pursuing.

### Promotion Closure

The item does not close, but becomes a sharper next object in [residue/open-residue.md](residue/open-residue.md).

## 5. Safety Rule

Do not convert mathematical elegance into Arcanum authority.

The paper may inspire:

- better route composition language;
- clearer model/inversion/evidence separation;
- local-loss and local-validation analogies;
- runtime semantics thinking.

It does not automatically promote:

- canonical Arcanum glossary;
- ontology edges;
- sigil contracts;
- spell contracts;
- runtime adapters;
- optimizer-like execution semantics.

