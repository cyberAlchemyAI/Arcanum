---
profile: autobayes-research
name: AutoBayes Definitions
description: Stabilized local definitions for the AutoBayes research tower.
type: definitions
status: closed-local
last_updated: 2026-06-07
---

# AutoBayes Definitions

These are local research definitions. They are stable enough for the AutoBayes tower and final learning pack, not canonical Arcanum definitions.

## D1 - AutoBayes

**Source meaning:** A compositional framework for generalized variational inference that separates model building, inversion construction, local loss attachment, parameter exposure, and optimization semantics.

**Arcanum reading:** AutoBayes is useful as a model of disciplined composition: each local part carries enough contract structure that a global behavior can be assembled without hand-derived global glue.

**Status:** `closed-definition`

## D2 - Open Model

**Source meaning:** A composable probabilistic model with explicit unobserved, observed, and latent spaces; composition carries hidden intermediate structure in the composite latent space.

**Arcanum reading:** Open model is the best first bridge into Arcanum because it makes hidden intermediate state explicit rather than pretending composition is lossless.

**Misuse warning:** Do not translate latent space into Arcanum residue. Use `state carrier` or `state namespace` only as analogy.

**Status:** `closed-definition`

## D3 - Layer Separation

**Source meaning:** The paper separates model specification syntax from optimization semantics, with inversion, loss construction, and parameter exposure as intermediate structured layers.

**Arcanum reading:** This mirrors the separation between declaration surfaces, handoffs, evidence contracts, runtime adapters, and promotion governance.

**Status:** `closed-definition`

## D4 - Local-To-Global Composition

**Source meaning:** Complex inference/loss/optimization structures can be built by composing local parts according to chain-rule-like discipline.

**Arcanum reading:** A route should be able to preserve local evidence, local contracts, and local residues while producing a global synthesis.

**Misuse warning:** Do not claim ordinary modularity is the same as AutoBayes local-to-global composition.

**Status:** `closed-definition`

## D6 - Bayesian Lens

**Source meaning:** An open model paired with a prior-indexed inversion family. The inversion is meaningful relative to a belief state, not as an unscoped reverse arrow.

**Arcanum reading:** A reverse handoff is legitimate only when the route names the state/context namespace that authorizes it.

**Misuse warning:** Do not call every adapter, guide, or handoff a Bayesian lens.

**Status:** `closed-definition`

## D7 - Parameter Exposure

**Source meaning:** The layer where a statistical game exposes a parameter space and a parameter-indexed map into games, making optimization handles explicit.

**Arcanum reading:** Automation may mutate only knobs declared by the route and authorized by the owner.

**Misuse warning:** Do not treat every context field as an optimizable parameter.

**Status:** `closed-definition`

## D8 - Local Loss Composition

**Source meaning:** Local energy and entropy terms compose by a generalized free-energy chain rule; energy adds, while entropy composes through posterior-indexed expectation.

**Arcanum reading:** Local evidence/objective receipts should remain typed by their boundary and state, then be joined mechanically by the parent.

**Misuse warning:** Do not call Arcanum validation metrics free energy.

**Status:** `closed-definition`

## D9 - Optimization Semantics

**Source meaning:** A semantic interpretation layer for optimizing parameterized statistical games; the paper treats gradient assignment as generally lax and implementation-facing.

**Arcanum reading:** Runtime semantics should interpret declared structure and report approximation/residue instead of rewriting the contract.

**Misuse warning:** Do not make runtime semantics the orchestrator.

**Status:** `closed-definition`

## D5 - Arcanum Bridge

**Source meaning:** Not a paper term.

**Local definition:** A controlled analogy or candidate design relation from AutoBayes concepts to Arcanum concepts, always labelled as analogy, candidate, rejected, or promoted-residue.

**Status:** `closed-definition`
