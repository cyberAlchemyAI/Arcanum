---
stage: 8
name: Distill Repair (low-cost falsification pilot)
capability: distill
mode: validate
pattern: toy_game
status: pass
verdict: pilot-specified-and-falsifiable
dispatch_id: refine-scu-entropy-experiment-20260608
subagent_receipts:
  - role: falsification-pilot-reviewer
    agent_id: a8166a0fc7630867c
---

# Distill Repair — Falsification Pilot (toy game)

The pilot is the cheapest decisive test, run *before* funding the full sweep. It targets
Proxy B's only contentful claim because B's U-shape is otherwise free.

## Pilot spec

- **Cheapest decisive measurement:** Proxy B's MDL minimizer location `r*` under
  **2 reference models × 2 serializations**, with the **blind SCU rubric** overlaid at
  each size point. If `r*` moves > 1 size bin across codings, the "interior minimum" is a
  coding artifact and the whole program stops cheaply.
- **Scope:** 4 size points (re-bundlings of the *same* obligation set, `r ≈ {2,4,8,16}`)
  × 6 difficulty-matched corpus items × N=3 seeds × 4 codings (2 models × 2 serializers);
  Proxy A and Proxy C full curves **deferred** until B's minimizer is shown real.
- **Estimated cost:** ~288 automated evaluations + ~24 blind rubric ratings (≈ half a day
  of human effort). True fixture scale.

## Pre-registered predictions (lodged before running)

- **P1:** B's `r*` is interior (not an edge bin) on the pooled curve.
- **P2:** `r*` invariant — same size bin across all 4 codings (max spread ≤ 1 bin).
- **P3:** blind-rubric peak within ±1 bin of `r*`; Spearman ρ(−MDL, rubric) ≥ 0.5.
- **P4:** sign pre-committed — lower MDL ↔ higher rubric; a reversal is falsification.

## Pass / continue vs fail / stop

- **Continue (fund full sweep):** P1 ∧ P2 ∧ (P3/P4) all hold.
- **Stop (program falsified at this scale):** `r*` at an edge bin (arms don't cross
  in range), or `r*` moves > 1 bin across codings (artifact), or rubric peak > 1 bin from
  `r*` or wrong-sign/null correlation (no co-location).

## Pre-registration locks (repairs from design-review, operationalized)

| Escape hatch | Lock |
|---|---|
| "The U is real" (B by construction) | U is pre-declared **zero-information**; only `r*` invariance + co-location count. |
| Difficulty confound | Corpus difficulty-matched; per-item difficulty must be flat across size bins (pre-set tolerance) or the run is **void**. |
| Rubric circularity | Rubric text hash-frozen; raters blind to `r`/MDL/size; scores lodged before proxy values are read. |
| Forking paths | Models, serializers, MDL coder, seeds, size grid, full corpus list, analysis script all pre-registered; post-hoc changes → exploratory only. |
| Corpus cherry-picking | Full item list fixed up front; all items analyzed; per-item curves reported. |
| Proxy C "absorbed pressure" survivorship | Hard, pre-declared repair budget; un-rising C at budget = falsification of the overload arm, not hidden pressure. |
| Edge-minimum reinterpretation | Size grid must bracket predicted `r*` with ≥1 bin each side; an edge `r*` = H1-fail at this scale; range extension is a *new* study. |

## Distill repair verdict

The composed design is **genuinely falsifiable once the locks are in place** and is now
specified at a cost cheap enough to kill it early. Residual threat: the Proxy C
survivorship save — neutralized only by the hard repair budget lock. Ready for plan.
