---
stage: 9
name: Invoke Plan (skill-mutation gate, non-executed)
capability: invoke
mode: plan
status: pass
dispatch_id: refine-dci-mutation-metric-20260608
---

# Invoke Plan — skill-mutation gate (non-executed)

Two honest deployment modes, sized by what you're willing to invest. Running either is owned by
`experiment-harness` / `observability` / `sigil-development`.

## Mode A — free now: gross-regression canary

Uses only incidental telemetry; no new corpus.
- A0.1 Add `skill_version` (content hash) to the observability envelope — the one cheap enabler.
- A0.2 D-live-slice: mean DCI per `skill_version`, always-on; flags only Δ≳0.30–0.40 swings.
- A0.3 Post-hoc D-ground-truth: git-rework extractor over accumulated history, keyed by `skill_version`.
- **Use:** catch big breakages after a skill edit. **Never:** a calibrated pass/fail or causal claim.

## Mode B — investment: calibrated CI gate

Buys the statistical power the analysis showed is missing.
- B1.1 Build a **dedicated replay corpus of ~50–100 fixtures per skill** (sized: Δ=0.15 → ~52 paired;
  Δ=0.10 → ~91).
- B1.2 Harness replay driver: run the corpus through v_old and v_new into isolated branches; stamp
  `skill_version`; assert `observer_version` equal across arms.
- B1.3 Score with **D-ground-truth (git rework, paired McNemar)** as the causal anchor; use
  D-harness-replay (paired Wilcoxon on self-reported DCI) as a fast pre-filter **with** the
  frozen-reporting-component + reporting-line-diff confound guard (advisory when reporting lines change).
- B1.4 Pair rework with fixture pass/fail (anti-Goodhart: "no rework" + "fixture failed" is caught).
- **Use:** block-on-merge for the replay pre-filter; confirm-after-the-fact for the rework anchor
  (it is a trailing signal).

## Owner boundary

Proposal only. No edit to canonical observability / experiment-harness / sigil-development / sigil
packages. Next routes: `observability-setup` (skill_version field), `experiment-harness` (replay +
corpus), `sigil-development` (gate in the skill-mutation lifecycle).
