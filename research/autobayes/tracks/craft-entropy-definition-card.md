---
profile: autobayes-research
name: Craft Translation-Entropy Definition Card
description: Converged, candidate-only definition card for Craft "translation entropy" after the AutoBayes-tower search. Candidate reading; not an approved Craft edit.
type: definition-card
status: candidate
dispatch: arcanum/research/autobayes/craft-entropy-search.dispatch.json
dispatch_id: craft-entropy-search-20260608
source_definition: arcanum/development/craft/CRAFT-INITIAL-DEFINITION.md
last_updated: 2026-06-08
---

# Craft Translation-Entropy Definition Card (candidate)

> **Status: candidate reading.** This card is a research output of the AutoBayes
> tower. It does **not** edit `CRAFT-INITIAL-DEFINITION.md` and does not promote any
> canonical Arcanum or Craft vocabulary. Adoption is a separate owner-approved task.

## Dialectic verdict

Two roles were held to synthesis: a **source-loyal formal reading** (what the cited
objects actually are) and a **Craft-operator translation** (what the operator needs
the word to do). They converge on a single honest verdict:

> **Craft "translation entropy" is not one quantity. As written it is an operational
> proxy that *conflates* three separable things the literature keeps distinct — a
> spread term, an energy/divergence term, and a composition-defect term — plus one
> genuinely distinct construct (attentional decay) that no searched source object can
> express.**

This places the verdict across two of the three allowed outcomes, honestly:

- **Operational proxy** (for the spread + energy parts): these are proxies for named
  formal objects and should be *split and renamed*, not borrowed wholesale.
- **Distinct construct** (for the attention part): attentional decay is irreducible to
  any source object and is the strongest candidate for a genuinely new Craft primitive.

It is **not** pure metaphor: every arm has a citable structural analogue. But it is
**not** a proven formal isomorphism with any single object either.

## The conflation, made explicit

`CRAFT-INITIAL-DEFINITION.md` writes one scalar:

```text
E = entropy(F_PCRA, S, context, relation_load, unit_size)
```

The search shows this `E` bundles four mechanisms that the literature separates:

| Craft sub-mechanism | Nearest source object | What it really is | Lane(s) |
| --- | --- | --- | --- |
| Spread term `H_spread` | conditional entropy `H(D\|S)` / model entropy `H(p(data\|schema))` | irreducible distributional spread of the translator — a real entropy | L-info (analogy), L-ppl (definitional) |
| Energy term `E_energy` | variational free-energy *energy* term; GVI loss `ℓ` | the schema↔data **fit/divergence** pressure — this is what **residue** measures, mislabeled as "entropy" | L-free, L-gvi |
| Relational term `R_rel` | Bayesian-lens **lax composition** defect (mutual-information gap) | a **composition cost**, not an entropy — relations live in wiring + belief-state index | L-games |
| Attention term `A_att` | *(none found)* | degradation of the translator as a function of unit size/salience; **changes the target distribution**, not the approximation | unmapped by all lanes |

## What can be borrowed, by analogy, or rejected

- **Borrow (with rename):** the spread term `H_spread` can be defined as the entropy
  of the conditional `p(data | schema)` (Staton-style model semantics). This is the
  *only* part for which "entropy" is the correct word.
- **Reject (rename, do not call it entropy):** the energy/fit term. It is a
  divergence/loss, structurally identical to what Craft already calls **residue** when
  realized after validation. Calling it "entropy before translation" double-counts
  residue. Candidate split: `E_energy` = *expected* free energy (forward, pre-run);
  residue = *realized* free energy (after validation).
- **Reject as entropy / promote as structure:** relational load is **lax composition
  cost** (mutual-information defect between local and global correctness), best owned by
  the statistical-games / lens view, not by an entropy scalar.
- **Promote-residue (genuinely distinct):** attentional decay. No searched object
  expresses "the conditional `p(data|schema)` itself drifts/flattens as `|schema|`
  grows." This is the most defensible candidate for a *new* Craft primitive and should
  not be folded into spread, energy, or composition.

## Candidate sharpened definition (proposal only)

> **Translation entropy is not a single scalar.** Craft should model translation
> uncertainty as a small **typed bundle**, mirroring the modularity the GVI / free-energy
> literature already uses:
>
> - `H_spread` — entropy of the translator's conditional `p(data | schema)` *(real entropy; borrow)*.
> - `E_energy` — expected schema↔data divergence; the forward dual of residue *(rename away from "entropy")*.
> - `R_rel` — lax composition defect across coupled units *(composition cost; owned by the games/lens view)*.
> - `A_att` — target-drift of the translator under unit size / salience load *(candidate new primitive; no source analogue)*.
>
> The **SCU** is then the unit size that minimizes the bundle: `H_spread`/`E_energy`
> dominate when units are too small (under-determination), `R_rel`/`A_att` dominate when
> units are too large (overload). The U-shaped fidelity curve is a **bias-variance-shaped
> hypothesis** whose vertical axis is currently unmeasured.

## Honesty boundary

1. No claim of formal isomorphism is made. Each bridge is structural analogy or an
   explicit term-split proposal, with the source object cited in
   [the lane receipts](../sessions/craft-entropy-search-receipts.md).
2. The four-way split is itself a *candidate*; it is the search's best reduction of the
   conflation, not a proven decomposition.
3. The U-curve has a real, citable *shape* (bias-variance / MDL) but **no measured
   axis**. "SCU is the local minimum of entropy" remains a hypothesis, and "SCU
   selection is the pre-translation control on `E`" is unfalsifiable until an entropy
   proxy is instrumented.
4. Nothing here is approved for `CRAFT-INITIAL-DEFINITION.md`. See
   [open residue](../residue/craft-entropy-open-residue.md) for the next objects.
