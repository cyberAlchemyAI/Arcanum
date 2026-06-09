---
stage: 7
name: Interrogation (refine-design-review)
capability: interrogation
mode: refine-design-review
status: flag
verdict: proceed-to-backtest
dispatch_id: refine-coherence-metric-20260608
---

# Interrogation refine-design-review — DCI v0 critique

## Q1. Does the composition still discriminate on a ceiling-skewed store?

Unknown until measured — that is the backtest's job. Prediction: A+drift alone ≈ flat 100;
**reopen is the only term expected to move the needle.** If reopen also fails to discriminate,
the honest conclusion is "the current telemetry cannot support a smooth coherence gauge; DCI is
an anomaly flag only." **Repair:** the backtest must report discrimination *with and without* the
reopen term, to isolate its contribution.

## Q2. Reopen false positives (healthy iteration vs failed recomposition)?

Real risk (designer C flagged it). A legitimate later edit to the same artifact looks like a
rework reopen. **Repair:** require the reopen event to carry a rework `mode` OR a
`reflection_trigger`/`recommendation` indicating rework — not mere co-occurrence on the target;
report the false-positive-prone count separately.

## Q3. Is the typed quad honest given sparse data?

Designer B conceded R_rel/A_att are data-starved. **Repair:** ship the quad but label R_rel/A_att
`low-confidence (n<30)` until enough gap-bearing records accumulate; DCI scalar rides on A+C.

## Q4. Does v0 over-promise as a "performance metric"?

Risk of dashboard theatre: a flat-100 gauge looks like "system is perfect" when it just means
"nothing measurable happened." **Repair:** the readout must always show `N_execution_bearing` and
the residue-bearing count beside DCI, and split observe-mode out.

## Verdict

**flag — proceed to backtest** with four repairs (isolate reopen contribution; rework-mode
gate on reopen; low-confidence label on sparse lanes; always show N). The backtest decides whether
DCI is a gauge or an anomaly detector.
