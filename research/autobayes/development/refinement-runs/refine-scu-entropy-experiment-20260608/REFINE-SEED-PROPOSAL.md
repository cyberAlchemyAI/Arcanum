---
profile: refine
run_id: refine-scu-entropy-experiment-20260608
name: SCU Entropy U-Curve Measurement Experiment — Refine Seed
description: Seed proposal to refine, through the canonical ten-stage loop, a falsifiable experiment that instruments a translation-entropy proxy against work-unit size and tests whether the SCU is an interior minimum.
type: refine-seed-proposal
status: proposed
preset: full
research_mode: research-if-gap-appears
parent_residue: arcanum/research/autobayes/residue/craft-entropy-open-residue.md#R3
last_updated: 2026-06-08
---

# Refine Seed Proposal — SCU Entropy U-Curve Measurement Experiment

## Target

Residue **R3** from the Craft entropy search
([craft-entropy-open-residue.md](../../residue/craft-entropy-open-residue.md)):

> The SCU fidelity curve is a real bias-variance / MDL *shape* with an
> asserted-but-unmeasured vertical axis. "SCU = local minimum of entropy" and "SCU is
> the pre-translation control on `E`" are currently unfalsifiable.

The refinement target is an **experiment design** — not the experiment run — that
makes those two claims falsifiable by instrumenting at least one translation-entropy
proxy as a function of work-unit size.

## Why this is a refinement target, not a direct task

The measurement axis is undefined and contested: the prior search surfaced three
candidate proxies and a competing single-home hypothesis (rate-distortion). Choosing
and de-risking a measurable axis needs discovery, critique, a controlled falsification
pilot, and a non-executed plan before any harness run. That is exactly the refine loop.

## Source context

- [CRAFT-INITIAL-DEFINITION.md](../../../../development/craft/CRAFT-INITIAL-DEFINITION.md) — §"Entropy, SCU, And PCRA Translation" (lines 187–244, 570–579), Open Question #4.
- [craft-entropy-definition-card.md](../../tracks/craft-entropy-definition-card.md) — the four-way conflation (`H_spread`, `E_energy`, `R_rel`, `A_att`) and the unmeasured-axis honesty boundary.
- [craft-entropy-search-receipts.md](../../sessions/craft-entropy-search-receipts.md) — L-scu (bias-variance/MDL), L-info (rate-distortion alternative), L-ppl (definitional vs runtime spread).

## Candidate entropy proxies to compare (the measurable axis)

These become the tournament alternatives in the design stage:

1. **Proxy A — semantic-entropy / self-consistency dispersion.** For each unit, sample
   N stochastic generations; measure dispersion (semantic-cluster entropy, or
   pairwise disagreement). Most literal "entropy"; captures `H_spread`.
2. **Proxy B — two-part description length (MDL).** Schema/context bits + residue/repair
   bits. Yields an interior minimizer by construction; captures the SCU-as-min claim.
3. **Proxy C — post-hoc residue / validation-failure rate.** Measured residue per unit
   after validation, regressed on unit size. Cheapest; measures `E_energy` trace, not spread.

## Independent variable and prediction

- **Independent variable:** work-unit size (e.g. SWU scope: lines/files/relations/obligations per unit), swept from too-small to too-large on a fixed corpus.
- **Pre-registered prediction (the falsifiable claim):** at least one proxy is **U-shaped** with an **interior minimum**, and that minimum aligns with independently-judged SCU quality. **Falsified if** every proxy is monotone (no interior minimum) or the minimum does not track SCU quality.

## Write scope

- May write only under `arcanum/research/autobayes/development/refinement-runs/refine-scu-entropy-experiment-20260608/`.
- May propose a handoff to `experiment-harness` / `research-evidence-harness`; may not run a live experiment or edit `CRAFT-INITIAL-DEFINITION.md`.

## Done criteria

A non-executed experiment plan that defines: the chosen entropy proxy (or proxy set),
the unit-size variable and sweep, a controlled corpus, the pre-registered U-curve
prediction, the falsification condition, a low-cost pilot (toy game) result, and a
validator-safe handoff to `experiment-harness`.

## Validation surface

- `dispatch-spec` validates the route shape.
- `research-evidence-harness` / `experiment-harness` validate the run schema, metric
  definitions, and fixture plan (without claiming live results).

## Preset and research mode

- **Preset:** `full` — the design stage runs a tournament across proxies and the repair
  stage runs a toy-game falsification, so deeper interrogation/distill are warranted.
- **Research mode:** `research-if-gap-appears` — local-first (the tower already cites
  bias-variance, MDL, semantic entropy); escalate only if a named external gap appears
  (e.g. a settled semantic-entropy estimator the tower has not captured).

## Planned stage configuration

Canonical ten-stage loop, materialized in [REFINE-DISPATCH.json](REFINE-DISPATCH.json),
with overlays `baseline_sequence`, `tournament_for_alternatives` (proxy comparison),
`toy_game_for_low_cost_falsification` (pilot), and `memory_residue_for_context_recovery`
(prior search residue). Subagent strategy: **recommended** (one designer per proxy) —
requires operator approval before execution.
