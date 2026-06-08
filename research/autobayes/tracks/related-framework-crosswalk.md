---
profile: autobayes-research
name: Related Framework Crosswalk
description: Source-backed crosswalk across exact Bayes, VI, GVI, BLR, AutoBayes, PPL guides, amortized guides, programmable MCMC guide composition, and Arcanum analogies.
type: research-track
status: source-backed-receipt
lane: related-framework-crosswalk
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Related Framework Crosswalk

This track is local to `research/autobayes/`. It does not promote AutoBayes terms into canonical Arcanum vocabulary.

## Receipt

### Core Reading

AutoBayes is easiest to understand when the nearby frameworks are not collapsed into one bucket.

The useful axis is:

```text
exact Bayes
  -> defines the posterior target
standard VI / VFE / negative ELBO / EUBO
  -> approximates that target by optimizing a bound/objective
GVI
  -> generalizes the target by choosing loss, divergence, and feasible family
BLR
  -> gives posterior-learning update semantics, especially natural-gradient style updates
PPL guides / amortized guides
  -> provide user- or learned inference programs coupled to model programs
Programmable MCMC guide composition
  -> verifies protocol/support soundness for sequential guide programs
AutoBayes
  -> makes model syntax, inversion, local loss, parameter exposure, and optimization semantics compositional
```

For Arcanum, the key lesson is not "AutoBayes maps directly to sigils." The key lesson is:

```text
Do not let a global synthesis rediscover hidden structure.
Make the local contract declare what it models, how reverse evidence is legal,
what local objective/evidence pressure it owns, what knobs are exposed,
and which runtime semantics are interpreting it.
```

## Source Anchors

| Source | What It Contributes To This Crosswalk | Link |
| --- | --- | --- |
| AutoBayes | Compositional framework for generalized variational inference; tools for models, inversions, local losses, parameter exposure, and local optimization. | [arXiv:2503.18608](https://arxiv.org/abs/2503.18608) |
| Variational Inference: A Review for Statisticians | Standard VI as approximating probability densities through optimization; ELBO-based variational framing. | [arXiv:1601.00670](https://arxiv.org/abs/1601.00670), [JASA](https://www.tandfonline.com/doi/full/10.1080/01621459.2017.1285773) |
| Generalized VI | Generalized posterior construction from loss, divergence, and feasible distribution family. | [arXiv:1904.02063](https://arxiv.org/abs/1904.02063) |
| Bayesian Learning Rule | Many learning algorithms as instances of one Bayesian learning rule over candidate distributions. | [arXiv:2107.04562](https://arxiv.org/abs/2107.04562), [JMLR](https://jmlr.org/beta/papers/v24/22-0291.html) |
| Pyro SVI docs | Operational model/guide/optimizer/loss separation in a PPL. | [Pyro SVI](https://docs.pyro.ai/en/dev/inference_algos.html) |
| Deep Amortized Inference for Probabilistic Programs | Guide programs with similar model structure but richer data flow, including neural networks. | [arXiv:1610.05735](https://arxiv.org/abs/1610.05735), [PDF](https://cocolab.stanford.edu/papers/daipptr.pdf) |
| Programmable MCMC with Soundly Composed Guide Programs | Sequential guide composition with protocol and support-coverage checks for MCMC soundness. | [Project page](https://www.cs.cmu.edu/~longp/publication/sequential-compositions-guide-programs/), [PDF](https://www.cs.cmu.edu/~fsaad/assets/papers/2024-PhamEtAl-OOPSLA.pdf) |

## Comparison Table

| Frame | Core Object | Coupling Mechanism | What It Secures | What It Leaves As Residue For AutoBayes |
| --- | --- | --- | --- | --- |
| Exact Bayes | Posterior distribution | Bayes rule: prior, likelihood, normalization | A principled posterior target when prior and likelihood are accepted | Does not by itself provide scalable approximate computation or compositional loss/inversion machinery |
| Standard VI / VFE / negative ELBO / EUBO | Variational posterior and evidence-bound objective | Optimize within a variational family, often through ELBO/free-energy forms | Tractable approximate inference by turning posterior approximation into optimization | Global objective may be hand-derived; local composition of model, inversion, and loss is not the central contract |
| GVI | Generalized posterior | Chosen loss, divergence, and feasible family | Permission to construct posterior-like beliefs from explicit objective ingredients beyond likelihood-only Bayes | Objective ingredients are explicit, but model/loss composition is not the whole framework |
| BLR | Candidate distribution update | Natural-gradient posterior learning rule | A reusable update semantics over candidate distributions that recovers many algorithms | Optimizer semantics can swallow model structure unless syntax and local composition stay separately typed |
| Pyro / PPL guides | Model program plus guide program | Operational trace/name/loss coupling through inference algorithm | Practical inference workflows: SVI, autoguides, MCMC, importance sampling | Guide coupling is weaker than an inversion contract composed by model structure |
| Deep amortized inference | Learned guide program `q(x|y)` against program model `p(x,y)` | Guide resembles the model but has richer data flow and neural components | Fast amortized posterior proposals; guide learning attached to model execution | Still guide-design and training focused, not local inversion/loss composition by construction |
| Programmable MCMC guide composition | Sequentially composed guide programs | Coroutine/type protocol checks and support coverage | Soundness condition: guides can cover model-program support under MCMC composition | Secures proposal soundness, not generalized VI loss composition or AutoBayes statistical-game syntax |
| AutoBayes | Open model, Bayesian lens, statistical game, parameterized statistical game | Chain rules for model inversion and generalized free energy; layered optimization semantics | Local model syntax, local inversion, local energy/entropy, parameter exposure, and semantics can be composed | Implementation is future-facing; analogies to workflow systems must remain guarded |

## Exact Bayes

Exact Bayes gives the clean posterior identity: posterior belief is obtained from prior belief and likelihood, with normalization. It is the reference point for why "inversion" matters: observations update belief about latent or unobserved quantities.

In this crosswalk:

- **Borrow:** Use exact Bayes as the clean target story: a posterior is not a generic score, it is a belief state after evidence.
- **Block:** Do not imply every AutoBayes or Arcanum reverse handoff is exact Bayes. AutoBayes supports exact and approximate inversions; Arcanum handoffs are governance/evidence objects, not probability kernels.
- **Confidence:** High.

## Standard VI, VFE, Negative ELBO, EUBO

Standard variational inference turns inference into optimization by choosing an approximating family and optimizing an evidence-bound/free-energy objective. The joined receipts emphasize that AutoBayes treats VFE, also discussed as EUBO or negative ELBO in its framing, as structurally decomposable rather than merely a single scalar glued onto a model.

AutoBayes residue:

- VI is already optimization-shaped.
- AutoBayes asks where the terms came from locally and how their composition remains lawful.
- The important distinction is energy/likelihood versus entropy/regularizer, because those terms compose differently.

In this crosswalk:

- **Borrow:** Treat "global objective assembled from local terms" as the core intuition.
- **Block:** Do not call every validation metric a variational loss, free energy, EUBO, or negative ELBO.
- **Confidence:** High for VI-as-optimization and ELBO/free-energy framing; medium-high for sign naming because conventions vary by community.

## GVI

GVI generalizes posterior construction by making loss, divergence, and feasible distribution family explicit. The joined `gvi-blr-comparator` receipt read this as: GVI gives the objective ingredients; AutoBayes gives a compositional contract discipline around those ingredients.

The useful distinction:

```text
GVI:
  What objective should define the posterior-like belief?

AutoBayes:
  How do local models, inversions, losses, and parameters compose so that
  posterior-like beliefs and objectives can be assembled structurally?
```

In this crosswalk:

- **Borrow:** Use GVI to understand why likelihood is not sacred when defining posterior-like beliefs.
- **Block:** Do not equate GVI decomposable loss with AutoBayes categorical/local composition.
- **Confidence:** High for GVI ingredients; medium for direct Arcanum translation.

## BLR

The Bayesian Learning Rule is best treated as an optimization semantics lane. It frames many algorithms as instances of posterior learning over candidate distributions, often through natural-gradient updates. AutoBayes can point to BLR-like behavior as a semantics for optimizing parameterized statistical games, but it does not let that semantics erase the model/lens/game syntax.

The useful distinction:

```text
BLR:
  How should a candidate belief distribution update?

AutoBayes:
  What compositional object is being optimized, and where were its model,
  inversion, loss, and parameter handles declared?
```

In this crosswalk:

- **Borrow:** Treat BLR as a candidate semantics family, not as the composition layer itself.
- **Block:** Do not treat an optimizer as an orchestrator or as the owner of model structure.
- **Confidence:** High for BLR-as-update-semantics; medium for any Arcanum runtime analogy.

## Pyro And PPL Guides

Pyro's SVI surface makes the operational split visible: `SVI(model, guide, optim, loss)` combines a model callable, guide callable, optimizer, and loss. This is powerful and practical, but it is not the same as AutoBayes' structural inversion-by-composition story.

The useful distinction:

```text
PPL guide:
  A program that helps inference approximate or sample posterior behavior.

AutoBayes local inversion:
  A prior-indexed reverse kernel/contract attached to a compositional model piece.
```

In this crosswalk:

- **Borrow:** PPL guides are the right contrast class for "inference artifact separate from model."
- **Block:** Do not collapse guide programs, Bayesian inversions, and Arcanum handoffs into one concept.
- **Confidence:** High for the operational contrast; medium for Pyro internals beyond SVI/autoguide-level behavior.

## Deep Amortized Inference

Deep amortized inference strengthens the model/guide relation by learning guide programs that resemble the original probabilistic program while adding richer data flow, including neural-network components. This makes it more structured than a completely ad hoc guide, but it is still primarily a learned guide/proposal story.

AutoBayes' remaining difference:

- The guide may resemble the model.
- AutoBayes wants the inversion/loss/parameter layers to be part of the compositional contract.
- A learned guide can be an implementation strategy, not the whole syntax.

In this crosswalk:

- **Borrow:** Use DAI as the "stronger guide coupling" comparison.
- **Block:** Do not treat learned structural resemblance as the same thing as a Bayesian lens chain rule.
- **Confidence:** Medium-high.

## Programmable MCMC Guide Composition

Programmable MCMC with soundly composed guide programs addresses a real weakness in guide composition: sequential guides can be unsound if their communication protocol or support coverage is wrong. Its coverage-checking algorithm verifies that composed guides agree with model-program support, which is a key MCMC soundness condition.

This is closer to Arcanum's evidence-boundary instincts than ordinary guides, because it says operational composition must be checked. But it is still a different theorem from AutoBayes:

```text
Programmable MCMC:
  Can the sequential guide composition reach the model support correctly?

AutoBayes:
  Given compositional model structure, how should inversion and generalized
  free-energy terms compose?
```

In this crosswalk:

- **Borrow:** Support coverage is a strong analogy for handoff coverage checks.
- **Block:** Do not say support coverage is the same as Bayesian inversion correctness.
- **Confidence:** High for the contrast; medium for Arcanum analogy.

## AutoBayes

AutoBayes' distinctive contribution is layer discipline:

| AutoBayes Layer | Role |
| --- | --- |
| Open model | Composable probabilistic syntax with carried latent state. |
| Bayesian lens | Open model plus prior-indexed inversion family. |
| Statistical game | Bayesian lens plus local energy and entropy/regularizer data. |
| Parameterized statistical game | Exposes parameter handles for optimization. |
| Optimization semantics | Interprets parameterized games with gradients/updates, generally with laxness. |

The joined receipts converge on one sentence:

```text
AutoBayes is a compiler-shaped contract discipline for inference.
```

That sentence is useful because it preserves both sides:

- It is not merely "a better optimizer."
- It is not merely "a different PPL."
- It is a discipline for keeping syntax, inversion, local loss, exposed parameters, and semantics separately typed while still composable.

In this crosswalk:

- **Borrow:** Layer discipline, explicit local ownership, and composition-first thinking.
- **Block:** Do not promote AutoBayes terms into canonical Arcanum vocabulary from this research tower alone.
- **Confidence:** High for paper-level interpretation; medium for future implementation implications because AutoBayes itself frames implementation as future-facing.

## Arcanum Analogy

The safest Arcanum reading is:

| AutoBayes Concept | Arcanum Analogy | Guardrail |
| --- | --- | --- |
| Open model | Route-capable local declaration with carried hidden state | Do not rename Arcanum residue as latent space. |
| Bayesian lens | Forward behavior plus reverse handoff behavior | Do not call every runtime adapter a lens. |
| Pushed-forward prior | State namespace making reverse inference legal | Do not ignore the state index in reverse explanations. |
| Local loss | Local evidence/objective pressure | Do not call every validation score a loss. |
| Parameter exposure | Declared knobs an optimizer may touch | Do not treat every variable as a parameter. |
| Optimization semantics | Runtime interpretation of declared structure | Do not let runtime semantics rewrite the contract. |
| Laxness | Accounted-for approximation or information loss | Do not use laxness as permission for vague evidence. |

Borrow category:

- local ownership of evidence/objective terms,
- explicit reverse handoff state,
- syntax versus semantics separation,
- parameter/knob exposure before automation,
- coverage-style checks for handoffs.

Block category:

- Arcanum is not "AutoBayes for workflows."
- Latent space is not Arcanum residue.
- Support coverage is not Bayesian inversion correctness.
- GVI decomposable loss is not AutoBayes local categorical composition.
- Optimizers are not orchestrators.
- PPL guides are not Bayesian lenses by default.

Analogy-only category:

- `semantics functor` as runtime adapter metaphor,
- `statistical game` as capability-plus-objective metaphor,
- `pushed-forward prior` as state namespace metaphor,
- `local loss` as evidence-pressure metaphor.

## Decision Notes

### What To Borrow Now

1. Use the crosswalk as a local research map for later AutoBayes cards.
2. Let "syntax versus semantics" inform Arcanum explanations, especially where dispatch/task-session/runtime boundaries are being discussed.
3. Add "reverse handoff state must be named" as a candidate design question for future Arcanum research, not as a new rule.
4. Use guide-program support coverage as a comparison for handoff coverage, with a warning that the mathematical objects differ.

### What To Block Now

1. No canonical vocabulary promotion.
2. No rewrite of sigil, spell, task-session, dispatch-spec, or ontology contracts.
3. No claim that Arcanum evidence equals likelihood, entropy, divergence, or free energy.
4. No claim that AutoBayes has solved implementation semantics; it supplies the composition framework and points to semantics lanes.

### What Needs Another Track

1. `open-model-definition-card`: precise definition and worked composition example.
2. `loss-composition-note`: energy, entropy, divergence, VFE/EUBO, negative ELBO, and open free energy.
3. `semantics-functor-reader`: what AutoBayes proves versus what it leaves as implementation strategy.
4. `autobayes-arcanum-bridge-decision`: borrow/block/analogy-only decisions with owner boundaries.

## Confidence

| Claim | Confidence | Reason |
| --- | --- | --- |
| AutoBayes' novelty is compositional layer discipline over models, inversions, losses, parameters, and semantics. | High | Stated in AutoBayes abstract/structure and supported by joined receipts. |
| GVI supplies objective ingredients rather than AutoBayes' full local composition law. | High | Supported by GVI framing and `gvi-blr-comparator`. |
| BLR is best read here as optimization/update semantics. | High | Supported by BLR source framing and AutoBayes receipt synthesis. |
| Pyro/PPL guides are operationally coupled to models, not equivalent to Bayesian lenses. | High | Supported by Pyro SVI docs and PPL contrast receipt. |
| Deep amortized inference is a stronger guide-structure comparison but not AutoBayes-style composition. | Medium-high | Source supports guide-program structural resemblance; exact mapping is interpretive. |
| Programmable MCMC guide composition is a support/protocol soundness lane, not generalized free-energy composition. | High | Supported by project page/PDF and PPL contrast receipt. |
| Arcanum analogies are useful design lenses. | Medium | Strong conceptual fit, but intentionally local and non-promoted. |

## Task Session Result

- Task: `related-framework-crosswalk`
- Result: `PASS`
- Runtime: local/read-write within requested scope
- Files updated: `research/autobayes/tracks/related-framework-crosswalk.md`
- Validation: scoped file created; source anchors included; joined receipts incorporated; no canonical Arcanum artifact edited
- Follow-up: use this crosswalk as input to `autobayes-arcanum-bridge-decision`, not as promotion evidence by itself
