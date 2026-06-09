---
profile: autobayes-research
name: Craft Entropy / SCU — Prior-Art Open Residue
description: Open residue after the prior-art / novelty audit.
type: open-residue
status: open
dispatch: arcanum/research/autobayes/craft-entropy-priorart.dispatch.json
dispatch_id: craft-entropy-priorart-20260608
last_updated: 2026-06-08
---

# Prior-Art Audit — Open Residue

## R-PA1 — Reframe the experiment as protocol validation, not discovery

- **Residue:** the audit shows the U-curve, the entropy metric, MDL, and the functorial
  framing are all prior art. The refine experiment must therefore stop positioning itself
  as testing a novel law.
- **Next object:** rewrite the experiment's contribution statement to "a falsification
  protocol (`r*` codebook-invariance + blind-rubric co-location) applied to translation-unit
  sizing," explicitly citing Geman, Rissanen, Tishby, Kuhn/Farquhar, Spivak/Smithe as the
  inherited machinery.
- **Owner:** experiment-harness lane / Craft definition owner.
- **Mark:** promote-residue.

## R-PA2 — Verify the strongest novelty claim is real (kill or keep #1) — RESOLVED: killed

- **Residue:** the surviving "protocol" novelty (`r*` codebook-invariance + blind co-location)
  is affirmatively-uncovered but not exhaustively searched.
- **Second-pass result:** **collapsed to restatement.** NML/universal codes (Rissanen 1996)
  give codebook-invariance by construction; stability selection (Meinshausen & Bühlmann 2010)
  is "select by invariance across perturbations"; multiverse/spec-curve (Steegen 2016;
  Simonsohn 2020) is "real only if invariant across analytic choices"; convergent validity
  (Campbell & Fiske 1959) is blind-criterion co-location. The protocol is triangulation of
  named methods; only the packaging is unnamed.
- **Status:** closed. **Mark:** restatement.

## R-PA3 — Resolve the contested module-size pillar — RESOLVED: drop

- **Residue:** C8's unit-agnostic law leans on module-size, which El Emam/Koru argue is a
  measurement artifact (reciprocal-correlation). The cross-domain claim is fragile.
- **Second-pass result:** **drop module-size.** Hatton 1997 (read in full) + El Emam/Koru
  2008/2009: the density U is likely a spurious-ratio artifact; raw-count modeling gives a
  monotonic power law, no interior minimum. Restrict C8 to diff-size + LLM-subtask (a
  narrower 2-domain claim); the ~200–400 LOC coincidence is no longer corroboration.
- **Status:** closed. **Mark:** restatement (module-size); diff-size/LLM-subtask remain partial.

## R-PA4 — Close the Wu et al. 2025 gap — RESOLVED: killed

- **Residue:** the closest LLM-axis prior art (Wu et al. 2025) was not read in full; its
  theory may already generalize to a unit-size axis.
- **Second-pass result:** **axis novelty collapsed.** Wu's accuracy model is axis-agnostic by
  its own statement (per-step error depends only on model and subtask difficulty `T/N`, no
  CoT/token term); "translation-unit size" relabels their `N`. Corroborated by arXiv:2506.16411
  (divide-and-conquer noise decomposition) and multi-agent subtask-count optima.
- **Status:** closed. **Mark:** restatement.

## Final state

All surviving novelty resolved to **restatement**. The audit's bottom line: the Craft
entropy / SCU bundle is prior art; the experiment is not novel theory. Remaining residue is
a single decision, not a search.

## Next route

- `decision-gate` for the Craft definition owner: **given that this is full restatement, is
  the experiment still worth running at all?** Defensible options: (a) **drop** the experiment
  as a novelty bid; (b) **reframe** it as an *internal validation / operationalization* that
  applies known machinery (NML, semantic entropy, Wu's decomposition law) to Arcanum craft
  units, with **no novelty claim**; (c) **repurpose** the apparatus as a practical SWU-sizing
  tool, not a research contribution. No edit to `CRAFT-INITIAL-DEFINITION.md` from this audit.
