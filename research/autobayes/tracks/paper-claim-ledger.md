---
profile: autobayes-research
name: Paper Claim Ledger
description: Source-backed claim ledger for the main AutoBayes paper layers.
type: research-track
status: pass
lane: paper-claim-ledger
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Paper Claim Ledger

This ledger closes the paper-skeleton obligation for the local AutoBayes tower.
It is local research evidence only. It does not promote AutoBayes terms into
canonical Arcanum vocabulary.

## Source Record

| Source kind | Source | Use |
| --- | --- | --- |
| AutoBayes paper | [arXiv:2503.18608v2](https://arxiv.org/abs/2503.18608), submitted 2025-03-24 and revised 2025-03-25 | Primary paper spine |
| related paper | [The Compositional Structure of Bayesian Inference](https://arxiv.org/abs/2305.06112) | Bayesian inversion chain-rule background |
| related paper | [Approximate Inference via Fibrations of Statistical Games](https://arxiv.org/abs/2306.17009) | Statistical-game/lax-section background |
| local receipt | [full-mode-source-receipts.md](../sessions/full-mode-source-receipts.md) | Joined lane receipts |
| local receipt | [open-model-definition-card.md](open-model-definition-card.md), [local-loss-composition-distill.md](local-loss-composition-distill.md), [semantics-functor-reader.md](semantics-functor-reader.md) | Existing local cards |

## Claim Ledger

| Layer | Source kind | Paper claim | Local closure | Arcanum reading | Status |
| --- | --- | --- | --- | --- | --- |
| Model syntax | AutoBayes paper | AutoBayes builds compositional tools for models, beginning with open models: model components expose unobserved, observed, and latent structure so composition can carry hidden intermediates. | [open-model-definition-card.md](open-model-definition-card.md) gives the worked `p : X -> Y`, `q : Y -> Z` carrier account. | A route-capable component must record what enters, what exits, and what hidden state composition carries. | `closed-source` |
| Inversion | AutoBayes paper + related paper | Bayesian inversion can be attached locally and composed by a chain-rule-like discipline; the inverse of a composite is not an arbitrary reverse arrow but a state-indexed reverse pass. | Existing inversion receipt plus this closure creates [bayesian-lens-definition-card.md](bayesian-lens-definition-card.md). | Reverse handoff legality depends on the correct state namespace / pushed-forward prior. | `closed-source` |
| Local loss | AutoBayes paper | Variational free energy and generalized free energies are decomposed locally; energy and entropy/regularizer terms compose differently. | [local-loss-composition-distill.md](local-loss-composition-distill.md) plus [two-step-symbolic-loss-calculation.md](two-step-symbolic-loss-calculation.md). | Parent synthesis should compose typed local evidence/objective receipts rather than inventing a global score. | `closed-source` |
| Parameter exposure | AutoBayes paper | Optimization becomes meaningful after a statistical game exposes parameter space and maps parameters into games. | [parameter-exposure-card.md](parameter-exposure-card.md). | Automation may touch only declared knobs, not arbitrary context. | `closed-definition` |
| Optimization semantics | AutoBayes paper + related paper | Parameterized statistical games receive optimization semantics; gradient assignment is generally lax, and different semantics strategies are future implementation work. | [semantics-functor-reader.md](semantics-functor-reader.md) and [implementation-residue-note.md](implementation-residue-note.md). | Runtime semantics interpret declared structure and must record approximation/residue. | `closed-source` |
| Examples | AutoBayes paper | Appendix examples show familiar learning cases as compositions of open models, lenses, losses, parameters, and semantics. | [appendix-examples-distill.md](appendix-examples-distill.md), [cups-caps-boundary-shift-card.md](cups-caps-boundary-shift-card.md). | Even familiar workflows should not erase boundary discipline. | `closed-source` |

## Operator Summary

AutoBayes is not just "category theory for VI." The local reading that survives
the closure pass is:

```text
model syntax
  -> local inversion
  -> local loss
  -> parameter exposure
  -> optimization semantics
```

Each arrow is a boundary. The Arcanum-useful lesson is to preserve the
boundary, not to import the vocabulary as canon.

## Misuse Warnings

- Do not treat this ledger as canonical Arcanum definition evidence.
- Do not collapse Bayesian inversion, guide programs, handoffs, and runtime adapters into one word.
- Do not call Arcanum evidence scores variational free energies.
- Do not treat optimization semantics as orchestration authority.
- Do not hide source uncertainty inside an Arcanum analogy.

## Extra Source Usage

- Source gap: AutoBayes source record/version check. Source used: arXiv record for `2503.18608`. Changed result: no; it confirmed v2 and the abstract spine.
- Source gap: Bayesian inversion chain rule. Source used: arXiv record for `2305.06112`. Changed result: no; it confirmed the local receipt framing.
- Source gap: statistical-games/fibration terminology. Source used: arXiv record for `2306.17009`. Changed result: no; it confirmed the local receipt framing.
