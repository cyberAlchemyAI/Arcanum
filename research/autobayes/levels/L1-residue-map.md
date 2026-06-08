---
profile: autobayes-research
name: L1 - Residue Map
description: Named obligations and closure status for the AutoBayes corpus.
type: tower-level
level: 1
status: closed-for-learning
last_updated: 2026-06-07
---

# L1 - Residue Map

## Carrier(mu_0)

| ID | Residue | Pathology | Track | Closure Target |
| --- | --- | --- | --- | --- |
| AB.1 | What is an open model exactly, and how does its latent space behave under composition? | missing-example | model-composition | closed-definition + worked diagram |
| AB.2 | How does Bayesian inversion compose, and how is it distinct from guide-program coupling? | missing-source | inversion-chain-rule | closed-source from Braithwaite et al. |
| AB.3 | How do local loss functions compose without smuggling global derivations back in? | optimization-semantics-risk | loss-composition | closed-distill + example |
| AB.4 | What is a parameterized statistical game in this paper's sense? | term-drift | statistical-games | closed-definition from paper + St Clere Smithe 2023a |
| AB.5 | Where does generalized VI fit relative to exact Bayes, VFE, EUBO, and BLR? | missing-source | related-frameworks | crosswalk table |
| AB.6 | What can Arcanum safely borrow from AutoBayes language? | bridge-risk | arcanum-interface | candidate bridge list with guardrails |
| AB.7 | What should not be mapped into Arcanum? | promotion-risk | arcanum-interface | closed-negative list |
| AB.8 | Which examples are the best operator-facing path into the paper? | missing-example | examples | worked distills for GMM, EM, VBEM |
| AB.9 | What would implementation require, given the paper leaves it for future work? | implementation-gap | implementation | implementation-residue note |
| AB.10 | Which related papers are prerequisites vs optional depth? | missing-source | literature-map | reading order and gates |

## Dependency Graph

```text
AB.1 -> AB.2 -> AB.3 -> AB.4
AB.5 -> AB.3 and AB.4
AB.8 -> AB.1, AB.2, AB.3
AB.6 depends on AB.1-AB.5
AB.7 depends on AB.6
AB.9 depends on AB.1-AB.4
AB.10 supports all source closures
```

## Highest Leverage Residues

### 1. AB.1 Open Model

The open model is the paper's first major object. If this term drifts, every later Arcanum analogy becomes noisy.

### 2. AB.3 Local Loss Composition

This is the sharpest Arcanum bridge: local loss/evidence terms compose into global behavior, but likelihood and regularization play different roles.

### 3. AB.6 Arcanum Interface

This is where the user's personal language matters. The interface should translate into sigil/spell/dispatch/evidence terms without pretending AutoBayes is an Arcanum spec.

## L1 Verdict

The original live residue was:

```text
how does a local compositional contract become a global inference/optimization behavior
without collapsing syntax, inversion, loss, parameters, and semantics?
```

That question is closed for operator learning by [FINAL-LEARNING-PACK.md](../FINAL-LEARNING-PACK.md). Remaining residue is implementation-candidate work only, listed in [implementation-residue-note.md](../tracks/implementation-residue-note.md).
