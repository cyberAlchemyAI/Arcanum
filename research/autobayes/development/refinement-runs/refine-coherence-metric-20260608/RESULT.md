---
profile: refine
run_id: refine-coherence-metric-20260608
type: refine-result
status: pass
preset: full
research_mode: no-research
dispatch: REFINE-DISPATCH.json
dispatch_validation: pass
last_updated: 2026-06-08
---

# Refine Result — DCI metric + Craft definition redefinition

## Answer in one paragraph

The agentic system **already emits** what a coherence metric needs, so DCI is cheap and real:
**DCI = a per-unit estimator of realized residue** from observability telemetry. Backtested on
398 real records it **separates clean (100) from residue-bearing (71.7) with no overlap** — but
it is a **bimodal anomaly flag, not a smooth dial**, the reopen term was inert (re-encoded the
observer's own reflection trigger), and — decisively — **residue does not rise with unit size**;
it concentrates where validation is weak, not where units are large. That backtest finding
reshapes the Craft definitions: **SCU is not "smallest" and not "minimum entropy" — it is the
unit of minimum residue density *subject to* singular responsibility and explicit recomposition,
defined by validation locality, not size.** DCI is the post-translation measurement of the same
coherence optimum that SCU-selection chooses pre-translation; it closes the Reflect stage with a
number but validates rather than replaces the (still predictive) selection.

## DCI (objective A)

- **Definition (v0):** objective-weighted residue backbone (status + output_contract_drift +
  quality_bar + gaps), enum-normalized, execution-bearing subset only, surfaced as the typed
  {E_energy, R_rel, A_att} quad. Anti-gaming: objective signals ≥0.75, hard floor on fail,
  `clean-unverified` flag for zero-variance sigils.
- **Backtest verdict:** discriminates (no overlap) but **anomaly-detector, not gauge.** Reopen
  term **failed** → replace in v1 with a real same-files reopen signal. Data-quality residue:
  the `execution.status` enum is inconsistent in the store (flag to observability owners).
- **Honesty:** DCI measures realized residue (the trace), not pre-translation entropy.

## Craft redefinition (objective B) — candidate redline

[CRAFT-DEFINITION-REVISION.md](CRAFT-DEFINITION-REVISION.md) — answers the three questions:

1. **What SCU really represents:** minimum residue density **subject to** singular
   responsibility + explicit recomposition; validation locality, not size.
2. **DCI ↔ SCU ↔ Craft:** DCI estimates `R` post-translation; SCU-selection chooses to minimize
   expected residue pre-translation — same optimum, two sides; DCI validates, not replaces.
3. **Entropy correction:** split the scalar into {H_spread (the only true entropy), residue-
   pressure, R_rel, A_att}; cite prior art; claim no novelty.

Resolves **Open Questions #3/#4** and **residue R1/R3**. Guardian guardrails kept: recomposition
co-constraint, pre/post loop, size-as-symptom, reflection-tower trigger, honesty boundary, and
the universal-physics horizon as labeled-unproven.

## Stage evidence

| Stage | Capability | Status |
|---|---|---|
| 1 Context baseline | context-builder | pass |
| 2 Invoke Define | invoke | pass |
| 3 Interrogation refine-review | interrogation | flag |
| 4 Research decision | refine | pass (no-research) |
| 5 Distill select | distill | pass |
| 6 Invoke Design (tournament) | invoke + 3 subagents | pass |
| 7 Interrogation design-review | interrogation | flag |
| 8 Distill Repair (backtest) | distill + 1 subagent | pass (anomaly-detector) |
| 9 Invoke Plan (DCI + redefinition) | invoke | pass |
| 10 Final Interrogation + redefinition dialectic | interrogation + 2 subagents | pass |

## Open residue / next routes

- **DCI v1:** replace the inert reopen term; propose the status-enum normalization + obligation
  count to `observability` owners → route to `workflow-reflect` + `observability-setup`.
- **Craft redline:** `decision-gate` for the Craft definition owner to apply / amend / reject
  [CRAFT-DEFINITION-REVISION.md](CRAFT-DEFINITION-REVISION.md). No canonical edit was made here.
- **Standing finding:** the SCU U-curve is unconfirmed *and* confounded in practice — coherence,
  not size, is the control variable.
