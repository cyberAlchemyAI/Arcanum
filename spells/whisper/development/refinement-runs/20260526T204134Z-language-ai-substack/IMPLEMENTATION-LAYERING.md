# Implementation Layering: Language AI Substack

## Purpose

Define the non-executed layer boundary for moving the repaired refinement substrate into a first drafting handoff without treating the article draft, citation research, or publication as complete.

## Source Contract

- Invoke plan contract: `spells/invoke/plan.md`
- Layering seed: `IMPLEMENTATION-LAYERING-SEED.md`
- Approved design surface: `DESIGN-REDEFINITION.md`
- Repaired substrate: `stages/08-distill-repair.md`
- Reference-first bridge: `REFERENCE-CHECK-HARARI.md`
- Target seed: `REFINE-SEED-PROPOSAL.md`

## Target And Scope

- Target: `language-ai-substack`
- Scope: Whisper-guided Substack research-post refinement
- Current state: L0 intent proof passed; L1 composition proof accepted by design and repair stages; lightweight reference-first repair accepted; L2 draft proof is ready for Task Session handoff.
- Non-execution boundary: this artifact plans the route only. It does not draft the article, verify external citations, publish, or mutate upstream seed state.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (Intent Proof) | After this layer, we know whether the article thesis, reader, non-goals, and citation policy are coherent enough to refine. | Define baseline and local glossary. | `INVOKE-DEFINE.md`, `GLOSSARY.md`, text-intent substrate, citation policy. | Composition proof, first draft, publication readiness. | Define output, seed proposal, context-builder evidence. | Passed; continue to L1. |
| L1 (Composition Proof) | After this layer, we know whether the body-part composition plan can carry the thesis into a draftable public article shape. | Draft-Readiness Composition Plan. | Six-view design, body-part composition plan, accepted design review, repair flag carry-forward. | First article draft, bounded citation research, publication review. | `DESIGN-REDEFINITION.md`, `stages/06-invoke-design.md`, `stages/07-interrogation-refine-design-review.md`, `stages/08-distill-repair.md`. | Passed with flags; continue to L2 under the constraints below. |
| L2 (Draft Proof) | After this layer, we know whether the repaired substrate can produce a reviewable first Substack draft without inventing source claims or relying on private jargon. | `SWU-WHISPER-ARTICLE-001`: first Substack draft from the repaired substrate and reference-first composition plan. | Checked Harari bridge, draft hook, research context, core insight, translated Arcanum example, implications, invitation, and quote/page gate if exact `Sapiens` wording is needed. | Publication, fundraising-copy transport, canonical glossary promotion, exact Harari wording unless verified. | Draft artifact plus objective, audience, resonance, structure, and citation-integrity checks. | Next route: `task-session` for one SWU. |
| L3 (Publication Readiness) | After this layer, we know whether the draft is fit for publication or later fundraising-copy transport. | Review and citation/readiness pass. | Bounded citation verification if Harari framing remains, public-language polish, final operator review. | Distribution, metrics, product positioning, durable campaign copy. | Review notes, citation evidence or omission decision, final publication-readiness verdict. | Deferred until L2 draft proof exists. |

## Carry-Forward Constraints

- `G1-harari-citation`: use `REFERENCE-CHECK-HARARI.md` for the shared-fiction / cooperation bridge; verify owned-copy edition/page only before direct quotation or precise page citation.
- `G2-public-translation`: translate `whisper`, `invoke`, aliases, schemas, and Arcanum-style naming into public reader language before using them as examples.
- `G3-meta-schema-example`: include one concrete public-facing sentence/example for `meta-schema` or omit the term from the first draft.
- Stage ownership: do not retroactively mutate `REFINE-SEED-PROPOSAL.md` from this plan. Final synthesis may later incorporate approved deltas.

## Recommended Next Layer

- Next layer: L2
- Key decision unlocked: whether the repaired substrate can become a reviewable first Substack draft under the citation, translation, and meta-schema constraints.
- Major deferred scope: citation research beyond bracket preservation, publication readiness, and fundraising-copy adaptation.
