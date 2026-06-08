---
profile: autobayes-research
name: AutoBayes Local Glossary
description: Closed local glossary for AutoBayes research, source terms first and Arcanum readings second.
type: glossary
status: closed-local
last_updated: 2026-06-07
---

# AutoBayes Local Glossary

This glossary is local to `research/autobayes/`. It is not canonical Arcanum vocabulary. Every entry preserves source meaning before Arcanum reading.

| Term | Source kind | Local meaning | Arcanum reading | Misuse warning | Status |
| --- | --- | --- | --- | --- | --- |
| AutoBayes | AutoBayes paper | A compositional framework for generalized variational inference with tools for models, inversions, local losses, parameter exposure, and optimization semantics. | A lens for compositional capability-contract hygiene. | Do not treat it as an Arcanum runtime spec. | `closed-definition` |
| Open model | AutoBayes paper | A composition-ready probabilistic model with unobserved, observed, and latent carrier structure. | A route-capable local declaration whose hidden intermediate state remains accountable. | Do not flatten latent space into generic context or residue. | `closed-definition` |
| Latent space | AutoBayes paper | The carried structure that may become hidden when open models compose. | A state-carrier analogy. | It is not Arcanum residue by definition. | `closed-definition` |
| Bayesian lens | AutoBayes paper + related paper | Open model plus prior-indexed inversion/posterior family. | Forward behavior plus reverse handoff legality. | Do not call every adapter a lens. | `closed-definition` |
| Bayesian inversion | AutoBayes paper + related paper | Reverse-direction inversion associated with a model and belief state. | Disciplined reverse handoff. | Do not confuse with arbitrary guide generation. | `closed-source` |
| Pushed-forward prior | AutoBayes paper + related paper | Belief state after a prior passes through a kernel/model factor. | State namespace needed to make a reverse handoff legal. | Do not ignore the state index. | `closed-source` |
| Bayesian chain rule | related paper | Inversions of composite models can be computed piecewise with correct state indexing. | Route-local reverse handoff discipline. | Not every reverse explanation is Bayesian inversion. | `closed-source` |
| Statistical game | AutoBayes paper | Bayesian lens plus local energy and entropy/regularizer data. | Component plus local objective/evidence pressure. | Do not turn Arcanum validation into VI loss language. | `closed-definition` |
| Energy | AutoBayes paper | Likelihood-like local loss contribution that adds under composition. | Local evidence pressure. | Not every evidence score is energy. | `closed-definition` |
| Entropy / regularizer | AutoBayes paper | Local regularizer term that composes through posterior-indexed expectation. | Constraint/spread pressure separate from fit. | Do not collapse entropy into a guardrail. | `closed-definition` |
| Variational free energy | AutoBayes paper | Objective also framed as EUBO/negative ELBO; decomposes through energy and entropy terms. | Global objective assembled from structured local receipts. | Keep sign and source context explicit. | `closed-definition` |
| Open free energy | AutoBayes paper | Free energy for an open game before composing in a prior contribution. | Local objective before upstream belief closes the route. | Do not mistake it for full VFE. | `closed-definition` |
| Parameter exposure | AutoBayes paper | Declaring a parameter space and map into statistical games so optimization has legal handles. | Declaring which knobs a runtime or task may touch. | Not every variable is a parameter. | `closed-definition` |
| Parameterized statistical game | AutoBayes paper | A parameter space paired with a parameter-indexed statistical game. | A route object with explicit authorized knobs. | Do not let optimizer own model structure. | `closed-definition` |
| Optimization semantics | AutoBayes paper | Interpretation layer that optimizes parameterized games, often with lax gradient composition. | Runtime semantics interpreting a declared route. | Runtime is not orchestration authority by default. | `closed-source` |
| Semantics functor | AutoBayes paper, derived reading | Candidate optimization interpretation for parameterized games. | Runtime adapter analogy only. | Arcanum runtime is not automatically a functor. | `analogy-only` |
| Lax composition | AutoBayes paper + related paper | Accountable composition where strict equality/information preservation may fail. | Declared approximation with receipt. | Do not use laxness for vague evidence. | `analogy-only` |
| Guide program | related PPL contrast | Inference/proposal program coupled to a model program. | Weakly coupled inverse/handoff contrast. | Do not equate guides with Bayesian lenses. | `closed-source` |
| Support coverage | related PPL contrast | Guide/proposal ability to cover model-program support. | Handoff coverage analogy. | Not Bayesian inversion correctness. | `analogy-only` |
| Cup / cap / reveal / copier | AutoBayes paper | Open-model operations that shift/copy/reveal boundaries in the compositional calculus. | Receipt-boundary-shift analogy. | Do not import names as Arcanum patterns. | `closed-distill` |
| Dependent output shape | AutoBayes appendix | Output space can depend on input value. | Route branch can determine legal receipt shape. | Stronger than optional late validation. | `closed-distill` |
