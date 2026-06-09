---
profile: refine
run_id: refine-coherence-metric-20260608
name: Decomposition Coherence Index + Craft definition redefinition
description: Seed to refine (1) a readable agentic-system performance metric (DCI) computed from observability telemetry and surfaced by workflow-reflect, and (2) a candidate redefinition of SCU, entropy, and the Craft formal model that DCI operationally grounds.
type: refine-seed-proposal
status: proposed
preset: full
research_mode: no-research
parent_run: arcanum/research/autobayes/development/refinement-runs/refine-scu-entropy-experiment-20260608
parent_audit: arcanum/research/autobayes/tracks/craft-entropy-novelty-verdict.md
last_updated: 2026-06-08
---

# Refine Seed — Decomposition Coherence Index (DCI)

## Target

Turn the SCU / translation-entropy apparatus — which the prior-art audit confirmed is
**restatement, not novel science** — into its honest, useful form: an **internal
agentic-system performance metric** that measures *how well the system breaks concepts and
work into coherent units*, computed from observability telemetry and surfaced by
[`workflow-reflect`](../../../../.claude/skills/workflow-reflect).

This is option (b)/(c) from the [novelty verdict](../../tracks/craft-entropy-novelty-verdict.md):
operationalization with **no novelty claim**.

**Second objective (added):** use this whole chain — the entropy split, the prior-art
verdict, and DCI — to **redefine, improve, and correct the definitions** in
[CRAFT-INITIAL-DEFINITION.md](../../../../development/craft/CRAFT-INITIAL-DEFINITION.md):
what **SCU really represents**, how **entropy** should be stated honestly, and what
**relation DCI bears to SCU and the Craft formal model**. The run produces a *candidate
revision* (redline) and a decision-gate — it does **not** edit the canonical file.

## Why this is now cheap and grounded

The observability package already emits, per sigil invocation, exactly the signals a
coherence metric needs (see `arcanum/framework/observability/templates/invocation-envelope.json`):

| Telemetry field | Coherence meaning | Entropy-bundle mapping (descriptive only) |
| --- | --- | --- |
| `execution.status` (completed/partial/blocked/failed) | did the unit close? | `E_energy` (realized residue) |
| `observer.quality_bar_status` (pass/partial/fail) | did it meet its own bar? | `E_energy` |
| `observer.workflow_gaps[]` (category, severity) | typed residue per unit | `E_energy` / `R_rel` |
| `observer.output_contract_drift` (bool) | did it fail to recompose to its contract? | `R_rel` (composition defect) |
| `execution.files_changed[]` count | unit-size proxy (relations touched) | `A_att` (overload axis) |
| `observer.reflection_trigger` / `recommendation` | system already flags trouble | label for validation |

So **Proxy C** (residue / validation-failure rate — the cheapest proxy from the experiment)
is already in the signal store (`.arcanum/observability/signals/sigil-invocations.jsonl`,
~850 KB of real records). No new instrumentation is needed; `workflow-reflect` already reads
this store.

## Honesty boundary (carried from prior runs)

- DCI measures **realized residue** (the trace), **not** pre-translation entropy `H_spread`.
  We do not claim to measure "the pressure." This is consistent with the definition card and
  the prior-art verdict.
- The U-curve (coherence vs unit size) is used only as a **descriptive diagnostic**, never as
  a novel law (Wu 2025 / bias-variance / MDL already own it).
- The metric must be computable from signals the package actually emits, and must name how it
  resists trivial gaming (e.g. a sigil that emits no gaps to look coherent).

## What "good" looks like

A readable performance signal of the agentic system's decomposition skill:

- **DCI(unit)** in [0,100]: 100 = clean, single-responsibility, recomposed unit; low = residue-heavy.
- **DCI(sigil)** and **DCI(window)**: which capabilities decompose well; trend over time.
- **DCI vs unit-size curve**: diagnostic — does coherence degrade as the system takes bigger units?
- Surfaced by `workflow-reflect` as: a dashboard-able score + low-DCI flags → improvement proposals.

## Second objective — what SCU really is, and where DCI sits (working redefinition, to be hardened)

The run will harden a candidate redefinition along these lines (this is the *starting
position*, not the final text):

**1. What SCU really represents.** The current doc says "SCU is the local minimum of
entropy" and "SCU selection is the pre-translation control on `E`." The prior-art audit
showed `E` (pre-translation entropy) is **not directly measurable** and that claim is
unfalsifiable as written. Honest restatement:

> The **SCU** is the unit size that, in practice, **minimizes realized residue per
> obligation** while keeping responsibility singular and recomposition explicit. It is the
> bias-variance / MDL coherence optimum, located *post-hoc by measurement*, not asserted.
> "Smallest coherent unit" is correct; "minimum of entropy" should become "minimum of
> measured residue density (DCI-optimal), used as a proxy for the unreachable entropy."

**2. Entropy correction.** Reserve "entropy" for `H_spread` (the one true entropy — sample
spread of the conditional, à la semantic entropy). Rename the schema↔data gap to
**residue-pressure / divergence** (`E_energy`), keep `R_rel` (composition defect) and
`A_att` (overload) as named, separate terms — the four-way split from the
[definition card](../../tracks/craft-entropy-definition-card.md). Cite the prior art
(bias-variance, MDL, rate-distortion, semantic entropy, functorial inversion); claim none
as novel.

**3. DCI's relation to SCU and Craft.** The Craft model is `C = (I, S, F, E, D, R, G, V)`.
DCI is an **estimator of `R` (residue), normalized per unit** — the *post-translation,
observable* operationalization of the SCU criterion:

> Craft says: *choose SCU to minimize `E` before translation; analyze residue to learn
> where `E` actually appeared after.* **DCI is that post-translation measurement.** SCU
> selection (pre) and DCI (post) are the **same coherence optimum viewed from two sides of
> the translation.** `workflow-reflect` feeds DCI back into schema repair — closing the
> Craft `Reflect` stage with a number.

This directly **answers Open Questions #3 and #4** (stability metric for "residue
acceptable enough"; how to measure SCU beyond prose) and **resolves residue R1/R3** from
the prior runs.

## Write scope

- May write only under this run folder. May propose (not execute) a `workflow-reflect`
  configuration, an `observability` metric spec, and a **candidate redline revision** of
  CRAFT-INITIAL-DEFINITION.md. May **not** edit the canonical Craft definition or sigil
  packages — the redline is a proposal routed through a decision-gate.

## Done criteria

1. A non-executed plan with the selected DCI definition (formula over named telemetry
   fields), its gaming-resistance, and a backtest result on the real signal store.
2. A **candidate Craft-definition revision** (redline) covering: the SCU redefinition, the
   entropy correction (four-way split + prior-art citations), and the DCI↔SCU↔formal-model
   relation — resolving Open Questions #3/#4 and residue R1/R3.
3. Handoffs: to `workflow-reflect` + `observability` owners for the candidate metric, and a
   **decision-gate** to the Craft definition owner for the candidate redline.

## Validation surface

- `dispatch-spec` validates the route. `workflow-reflect` / `observability-setup` own the
  metric integration. The toy-game stage backtests on the real `sigil-invocations.jsonl`.

## Preset / research

- **Preset:** full (tournament across metric definitions + toy-game backtest).
- **Research:** no-research — prior-art audit is complete; local telemetry is sufficient.

## Planned stage configuration

Canonical ten-stage loop ([REFINE-DISPATCH.json](REFINE-DISPATCH.json)) with overlays
`baseline_sequence`, `memory_residue_for_context_recovery`, `tournament_for_alternatives`
(three candidate DCI definitions), `toy_game_for_low_cost_falsification` (backtest on real
telemetry). Subagents **recommended** (one designer per candidate metric + a backtest
reviewer); requires operator approval.
