---
profile: refine
run_id: refine-coherence-metric-20260608
name: CRAFT-INITIAL-DEFINITION.md — Candidate Revision (redline)
description: Candidate redline correcting SCU, entropy, and the formal model, and placing DCI — synthesized from the operational-author / philosophical-guardian dialectic. Candidate only; routed to a decision-gate; not applied.
type: craft-definition-revision
status: candidate
target_file: arcanum/development/craft/CRAFT-INITIAL-DEFINITION.md
evidence:
  - arcanum/research/autobayes/tracks/craft-entropy-definition-card.md
  - arcanum/research/autobayes/tracks/craft-entropy-novelty-verdict.md
  - arcanum/research/autobayes/development/refinement-runs/refine-coherence-metric-20260608/stages/08-distill-repair-backtest.md
last_updated: 2026-06-08
---

# Candidate Revision — CRAFT-INITIAL-DEFINITION.md

> **Candidate redline. Not applied.** Routed to a decision-gate for the Craft definition
> owner. Claims **only operationalization**, no novelty (prior art: bias-variance, MDL,
> rate-distortion, semantic entropy, Spivak/St Clere Smithe functorial inversion).

## The three questions, answered

### 1. What does SCU *really* represent?

Not "the smallest unit" and not "the local minimum of entropy" (entropy `E` is not
measurable — that claim is unfalsifiable). Operationally:

> **The SCU is the unit at which residue density is locally minimized, *subject to*
> singular responsibility and an explicit recomposition path into the upper schema.** It is
> defined by **validation locality and contract closure — not by size.** "Smallest coherent"
> means "smallest unit that still closes its own validation and reattaches upward," never
> "smallest in tokens or files."

Two guardrails make this honest, not circular:
- **Recomposition is a co-constraint, not an afterthought.** A pure residue minimizer would
  shatter work into trivially-clean fragments that no longer recompose. Recomposition stops that.
- **SCU selection stays predictive (pre-translation).** You choose an SCU on coherence
  criteria *before* any residue exists (singular responsibility, bounded relation load, local
  validation, explicit recomposition). Residue density only *validates* that choice afterward.

### 2. What is DCI's relation to SCU and the Craft model?

> **DCI is the post-translation estimator of `R` (residue), per unit, from observability
> telemetry.** In the formal model `C = (I, S, F, E, D, R, G, V)`: `E` is an **unmeasured
> latent** uncertainty bundle; `R` is the **measured** quantity; **DCI estimates `R`.**

SCU-selection (pre) and DCI (post) are the **same coherence optimum from two sides of the
translation**: one *chooses* to minimize expected residue; the other *measures* the residue
that resulted. DCI **closes the Craft `Reflect` stage with a number** and feeds
`workflow-reflect` to repair schemas. But DCI **validates; it does not replace** SCU selection
— it is post-hoc.

**Empirical caveat (real telemetry, n=398):** DCI is a **bimodal anomaly flag, not a smooth
gauge** — it separates clean (100) from residue-bearing (71.7) with no overlap, but does not
grade between. And it does **not** corroborate the SCU U-curve: residue concentrates where
validation is weak / the contract drifts, **independent of unit size** (size co-varies with
which sigil ran — a confound).

### 3. The entropy correction

The scalar "entropy `E`" conflates four mechanisms the literature keeps distinct; split it:

| Term | What it is | Status |
|---|---|---|
| `H_spread` | sample spread of `p(data\|schema)` — **the only true entropy** (semantic entropy; Kuhn/Farquhar) | keep the word "entropy" here only |
| `E_energy` → **residue-pressure / divergence** | schema↔data fit gap — the *forward dual of residue*; "entropy before translation" double-counts residue | rename |
| `R_rel` | relational / lax-composition defect across coupled units | name separately |
| `A_att` | attentional decay (target-drift as `\|schema\|` grows) — candidate-distinct primitive, **size-form unconfirmed** | name, do not over-claim |

## Section-by-section redline (candidate)

- **§Smallest Coherent Unit (line 185).** Replace "The SCU is the current best point of low
  entropy…" → "The SCU is the unit at which residue density is locally minimized, subject to
  singular responsibility and explicit recomposition; it is defined by validation locality and
  contract closure, not size. The single-sweet-spot-size intuition is a bias-variance-shaped
  hypothesis ([novelty verdict](../../tracks/craft-entropy-novelty-verdict.md)), and on real
  telemetry it is unconfirmed and confounded ([backtest](stages/08-distill-repair-backtest.md))."
  Keep bullets 175–183 unchanged (already size-agnostic).

- **§Entropy, SCU, And PCRA Translation (189, 193–196).** Replace the opening scalar definition
  with the four-term typed bundle above; relabel the four bullets to `H_spread`,
  residue-pressure, `R_rel`, `A_att`; reserve "entropy" for `H_spread`.

- **§ (200–211).** Add an inline caveat to the U-curve diagram: "Hypothesis — bias-variance /
  MDL / rate-distortion restated; vertical axis unmeasured; size axis empirically confounded
  (residue does not rise with size in telemetry). Craft claims no novelty here." Resolve toward
  the existing line 213 ("smallest *coherent*, not smallest possible").

- **§ (237).** "observable trace of entropy after translation" → "realized trace of
  residue-pressure (`E_energy`) after validation."

- **§Initial Formal Model (544, 554, 570, 581).** `E` → unmeasured latent bundle
  `{H_spread, E_energy, R_rel, A_att}`; `R` is measured; **DCI is the estimator of `R`**; SCU
  selection = pre-translation control on *expected residue*; residue analysis (DCI) =
  post-translation measurement and the only direct evidence about latent `E`.

- **§Open Questions (704–705).** #3: residue is "acceptable" when DCI shows no anomaly flag on
  the execution-bearing subset, read as a per-sigil trend + residue-bearing count (a flag, not a
  continuous threshold). #4: measure SCU by residue density + validation locality, not by
  information load, context size, or unit size — the backtest rejects "failure rises with size."

## What must NOT change (honesty boundary — preserved)

- The schema→translator→data→residue→reflection→recomposition **loop** (the real spine; untouched by the audit).
- The **recomposition criterion** and the **residue taxonomy** (the typed decision surface).
- The **reflection-tower trigger**: residue floor-bounded under further reduction ⇒ a missing
  higher schema ⇒ **climb, do not shrink.**
- The **pre/post distinction** (selection vs validation).
- The **honesty boundary** (660–672) and the **staged universal-physics horizon** (624–631),
  kept explicitly as *labeled-unproven horizon*, not result.
- **No novelty claims** anywhere — positioning is "operationalization + protocol."

## Next route

`decision-gate` for the Craft definition owner: apply this redline to
CRAFT-INITIAL-DEFINITION.md (a separate owner task), amend, or reject.
