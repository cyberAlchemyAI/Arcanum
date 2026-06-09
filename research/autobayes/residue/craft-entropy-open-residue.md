---
profile: autobayes-research
name: Craft Entropy Search — Open Residue
description: Open residue and next objects after the Craft translation-entropy search pass.
type: open-residue
status: open
dispatch: arcanum/research/autobayes/craft-entropy-search.dispatch.json
dispatch_id: craft-entropy-search-20260608
last_updated: 2026-06-08
---

# Craft Entropy Search — Open Residue

Residue from `craft-entropy-search-20260608`. Each entry names the next object and an
owner lane. None of these promote canonical Arcanum or Craft authority on their own.

## R1 — The term-split decision (highest priority)

- **Residue:** `E` conflates a spread term, an energy/divergence term, a composition
  defect, and an attention term. The energy term double-counts what Craft already calls
  residue.
- **Next object:** a decision-gate for the Craft definition owner — *adopt the four-way
  split (`H_spread`, `E_energy`, `R_rel`, `A_att`), or keep one scalar `E` and document
  the conflation as accepted imprecision?*
- **Owner:** craft-definition-owner (outside this dispatch).
- **Mark:** promote-residue.

## R2 — Attentional decay has no source home

- **Residue:** no searched object (information theory, free energy, GVI, statistical
  games, PPL) expresses attentional decay as *target-drift of `p(data|schema)` under
  unit/salience load*. It is the strongest candidate for a genuinely new Craft primitive.
- **Next object:** a focused search lane outside the AutoBayes corpus — context-length /
  long-context degradation, lost-in-the-middle effects, transformer attention dilution,
  position-dependent fidelity. Promote to a sibling tower if it grows.
- **Owner:** new research lane (not yet scoped).
- **Mark:** promote-residue.

## R3 — The U-curve has no measured axis

- **Residue:** the SCU fidelity curve is a real bias-variance / MDL *shape* with an
  asserted-but-unmeasured vertical axis. "SCU = local minimum of entropy" and "SCU is the
  pre-translation control on `E`" are currently unfalsifiable (Craft Open Question #4).
- **Next object:** instrument one entropy proxy and test for an interior minimum —
  candidates: (a) semantic-entropy / self-consistency variance over N stochastic
  generations per unit; (b) two-part description length (schema/context bits + residue/
  repair bits); (c) post-hoc validation-failure rate vs unit size. A `toy_game` /
  experiment-harness target.
- **Owner:** experiment-harness lane.
- **Mark:** promote-residue.

## R4 — Relational defect measurability

- **Residue:** the games/lens view *measures* its relational defect (lax mutual-information
  gap) because every local object is an exact distribution; the PCRA translator has no
  posterior, so Craft's relational load stays unmeasured.
- **Next object:** ask whether a cross-unit coupling residue can be measured operationally
  (e.g. cross-file edit-conflict rate, recomposition-failure rate) *without* inventing a
  posterior — the operational analogue of the lax mutual-information gap.
- **Owner:** statistical-games lane / distill.
- **Mark:** promote-residue.

## R5 — Rate-distortion alternative to "entropy"

- **Residue:** the L-info lane notes the U-shape cannot come from `H(D|S)` alone and may
  be a rate-distortion / information-bottleneck quantity (description length traded
  against fidelity), which would explain an interior minimum natively.
- **Next object:** a small lane testing whether rate-distortion / information bottleneck
  is a better single home for the whole curve than the four-way split — a competing
  hypothesis to R1.
- **Owner:** info-theoretic lane.
- **Mark:** promote-residue.

## Missing-source residue

- None. Every lane reached a cited source object. No lane was closed as missing-source.

## Next route

- `decision-gate` on R1 (term split) for the Craft definition owner, then `invoke` to
  author a Craft-definition refresh if the split is adopted. R2/R3/R5 are candidate new
  research lanes; R4 routes to distill. See
  [the candidate definition card](../tracks/craft-entropy-definition-card.md).
