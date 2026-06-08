---
profile: autobayes-research
name: L0 - Corpus
description: Closed corpus map for AutoBayes and related works.
type: tower-level
level: 0
status: closed-local
last_updated: 2026-06-07
---

# L0 - Corpus

## Primary Paper

**AutoBayes: A Compositional Framework for Generalized Variational Inference** introduces a compositional framework for generalized variational inference.

Seed source facts from the paper front matter:

- It separates model specification from inversion.
- It treats Bayesian inference and variational-inference loss functions as satisfying chain-rule-like composition laws.
- It constructs tools for building models, constructing inversions, attaching local loss functions, exposing parameters, and optimizing parameterized statistical games.
- It explicitly separates syntax of model specification from semantics of optimization.
- It leaves implementation of the framework for future work, while giving examples in the appendix.

## Paper Structure

| Section | Research Meaning |
| --- | --- |
| 1. Introduction | Why inference chain rules matter, and why existing PPL/GVI/BLR views are incomplete. |
| 2. Beyond Bayesian Networks | Open models, observed/unobserved/latent spaces, and model composition. |
| 3. Local Inversions for Compositional Models | How inversions compose rather than being derived globally each time. |
| 4. Composing Complex Loss Functions | How local losses compose and how likelihood differs from regularization. |
| 5. Optimization via Functorial Semantics | How parameter exposure and optimization semantics sit after model/loss construction. |
| Appendix A | Examples: Gaussian mixture model, EM, VBEM, and related classic cases. |

## Full-Mode Claim Ledger

Status: `joined-with-thread-cap-residue` from [sessions/full-mode-source-receipts.md](../sessions/full-mode-source-receipts.md).

| Section | Claim Ledger |
| --- | --- |
| Abstract | `source-claim`: AutoBayes is a compositional framework for generalized variational inference, with tools for models, inversions, local losses, parameter exposure, and optimization of parameterized statistical games. |
| 1. Introduction | `source-claim`: Bayesian inference has a chain rule analogous to reverse-mode autodiff. `source-claim`: PPL guides, GVI, and BLR are close but insufficiently compositional. `derived-reading`: the target is Bayesian autodiff as a contract discipline. |
| 2. Beyond Bayesian Networks | `source-claim`: open models generalize Bayesian networks by making unobserved, observed, and latent spaces explicit. `source-claim`: composition stores hidden intermediate structure. |
| 3. Local Inversions | `source-claim`: Bayesian lenses pair open models with local inversions. `source-claim`: exact inversions are functorial under composition; tensor composition is lossy/lax because marginals discard joint-prior information. |
| 4. Complex Loss Functions | `source-claim`: VFE can be rewritten without direct exact-posterior evaluation. `source-claim`: energy/likelihood and entropy/regularizer behave differently under composition. `source-claim`: statistical games package Bayesian lenses plus local energy and entropy. |
| 5. Optimization Semantics | `source-claim`: parameterized statistical games expose parameters after model/loss construction. `source-claim`: local gradients compose into structured vectors, but strict equality with global composite gradients generally fails. |
| Appendix A | `source-claim`: examples include Gaussian mixture MLE, EM, VBEM, supervised learning, and Bayesian deep learning. |
| Appendix B | `source-claim`: dependent typed models allow output spaces to depend on input values. |

## Related-Paper Lanes

| Lane | Related Work | Why It Matters |
| --- | --- | --- |
| Bayesian chain rule | Braithwaite, Hedges, St Clere Smithe, The Compositional Structure of Bayesian Inference | Source of the inference chain rule the paper builds on. |
| Generalized VI | Knoblauch, Jewson, Damoulas, Generalized Variational Inference | Baseline for generalized loss functions beyond exact Bayes. |
| Bayesian learning rule | Khan and Rue, The Bayesian Learning Rule | Key adjacent optimization/loss framework. |
| Statistical games | St Clere Smithe, Approximate Inference via Fibrations of Statistical Games | Likely mathematical substrate for parameterized statistical games. |
| Bayesian brain / compositional foundations | St Clere Smithe, Mathematical Foundations for a Compositional Account of the Bayesian Brain | Background for open models and Bayesian lenses. |
| Copy composition | St Clere Smithe, Copy-composition for probabilistic graphical models | Background for composing graphical/probabilistic model structure. |
| PPL semantics | Staton, Commutative Semantics for Probabilistic Programming | Supports the claim that probabilistic programs denote kernels. |
| Categorical Bayesian networks | Fong, Causal Theories | Prior categorical account of Bayesian networks. |
| PPL guide programs | Ritchie et al.; Bingham et al.; Pham et al. | Contrast class: guides/inversions exist, but coupling is weaker than AutoBayes wants. |
| Compositional game theory | Ghani, Hedges, Winschel, Zahn | Background for game-theoretic composition. |

## Joined Related-Work Readings

| Lane | Status | Joined Finding |
| --- | --- | --- |
| Bayesian inversion chain rule | `closed-source` | Inversions compose in reverse order, but each local inversion is indexed by the correct pushed-forward prior. |
| Statistical games | `closed-source` | Statistical games add local energy and entropy terms to Bayesian lenses; parameterized games expose the optimizer's legal handles. |
| PPL contrast | `closed-source` | PPL guides provide model/inference separation, but AutoBayes wants structural coupling by construction. |
| GVI and BLR | `closed-source` | GVI supplies objective ingredients; BLR supplies update semantics; AutoBayes wraps both in compositional model/inversion/loss syntax. |
| Glossary steward | `closed-definition` | Source-first glossary terms joined; key expansion: open model, latent space, Bayesian lens, local loss, energy, entropy, parameter exposure, and functorial semantics. |

## What Is Closed For Learning

| Area | Solid Content |
| --- | --- |
| Compositionality | The paper is explicitly about composing models, inversions, losses, and parameterized games. |
| Separation of layers | Syntax, inversion, loss, parameter exposure, and optimization are distinct. |
| Arcanum relevance | The structure resembles Arcanum's boundary discipline: contract, handoff, evidence, semantics, execution. |
| Implementation status | Implementation is future work, so any executable claim must be treated as a design implication, not source fact. |

## Remaining Cutoff

| Area | Weak Point |
| --- | --- |
| Proof-level category theory | The tower is not a formal proof artifact. |
| Deep related-paper reconstruction | Related papers were used to close named gaps, not exhaustively formalized. |
| Arcanum implementation | Analogies are closed for understanding but not validated as canonical contract changes. |
| Numeric experiments | No optimizer/runtime experiment was run. |
| Canonical glossary promotion | Explicitly out of scope without later owner review. |

## L0 Verdict

The useful research object is not "AutoBayes as another ML paper." It is AutoBayes as a compositional contract discipline for inference:

```text
local model parts + local inversion + local loss + exposed parameters
  -> globally composable inference game
```

That gives Arcanum a strong lens for thinking about local capability contracts and global runtime semantics, but the mapping must stay typed as analogy or candidate bridge until source-backed.
