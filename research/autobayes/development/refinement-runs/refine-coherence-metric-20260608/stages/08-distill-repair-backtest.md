---
stage: 8
name: Distill Repair (backtest on real telemetry)
capability: distill
mode: validate
pattern: toy_game
status: pass
verdict: discriminates-as-anomaly-detector
dispatch_id: refine-coherence-metric-20260608
subagent_receipts:
  - role: telemetry-backtest-reviewer
    agent_id: a8a9e674548e15626
---

# Distill Repair — DCI backtest (real store, n=398)

## Results

- **Coverage:** 398 total → 83 execution-bearing → 315 null (observe-mode, excluded). Confirms the metric is meaningful only on ~21% of records.
- **Discrimination: PASS.** Clean units (status ok & qbar pass & no gaps/drift) mean DCI **100.00** (n=37); residue-bearing mean **71.69** (n=46); **no overlap at the boundary** (clean min 100, residue max 97). DCI cleanly flags residue.
- **Shape: bimodal.** 37/83 pile at exactly 100; the rest spread 39–97 (median 81, stdev 17.8). → **anomaly detector / flag, not a smooth dial.**
- **Reopen term FAILED.** 0 real "later same-target edit in a rework mode" events fired; all 37 reopen flags were re-readings of the record's own `reflection_trigger`/`recommendation` (double-counting `r_status`/`r_qbar`). Discrimination survives without it (gap 20.05 vs 28.31). **v1 must replace reopen with a real signal** (e.g. later record touching the same `files_changed`, or a revert).
- **DCI vs unit-size: U-hypothesis NOT supported here.** Bucket means: 1–3 files **81.0**, 4–10 **88.3**, 11+ **88.6** — coherence slightly **rises** with size. Reason: large units are well-validated `task-session` runs; residue concentrates in small `partial`/`failed`/gap records. **Confound:** size co-varies with which sigil ran, not with intrinsic coherence.
- **Per-sigil:** task-session 84.9, invoke 89.5, experiment-harness 84.5, decision-gate 73.7, refine 40.0 (n=2, noise).

## Repairs / failure interpretations

1. **Reopen is inert → replace in v1.** As implemented it adds no independent signal. Keep DCI on the objective backbone (status + drift + qbar + gaps) until a real reopen signal exists.
2. **DCI is an anomaly detector, not a gauge.** Ship it as a **residue flag + trend**, never as a "0–100 quality dial." The readout must show `N_execution_bearing` and residue-bearing count.
3. **The size→coherence curve is confounded on this store.** Do NOT present DCI-vs-size as evidence of the SCU U-curve. Residue tracks validation-locality and contract fit, not raw size.

## Load-bearing finding for the Craft redefinition

> On real telemetry, **residue does not rise with unit size** — it concentrates where
> validation is weak or the contract drifts, independent of size. This **empirically refutes
> the naive "bigger unit → more entropy" reading** and supports redefining the SCU around
> **residue density / validation locality**, not size. The U-curve remains unconfirmed *and*
> confounded in practice — exactly as the prior-art audit warned.

## Verdict

**pass (as anomaly detector).** DCI discriminates clean from residue-bearing with no overlap;
it is a flag+trend, not a dial; reopen needs replacement; the size-coherence claim is unsupported.
Ready for plan + redefinition.
