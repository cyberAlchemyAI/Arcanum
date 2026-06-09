---
stage: 7
name: Interrogation (refine-design-review)
capability: interrogation
mode: refine-design-review
status: flag
verdict: proceed-to-power-analysis
dispatch_id: refine-dci-mutation-metric-20260608
---

# Interrogation refine-design-review — ladder critique

## Q1. Does the ladder actually escape the earlier critique?

Yes for the anchor (git rework is observer-independent by construction), partial for the gate. The
honest position: **causal claims rest only on D-ground-truth.** The replay gate is a fast pre-filter,
not proof. That is a real improvement over the absolute-gauge DCI, which had no observer-independent
anchor at all.

## Q2. The trailing-signal problem — is it fatal?

Not fatal, but it relocates the metric. Rework needs accumulated history → the anchor is a **post-hoc
CI canary**, not a pre-merge blocker. The pre-merge layer is the (weaker) replay gate. **Repair:** the
plan must state this honestly — "block-on-merge" is the replay gate's job (with the confound flag);
"confirm-after-the-fact" is the rework anchor's job.

## Q3. Is per-sigil N large enough for ANY of it to work?

The open question the power analysis must answer. task-session has 32 execution-bearing records
*total*, fewer per version. If detecting a 0.30→0.15 shift needs >50 paired runs, the gate only catches
gross regressions and the per-mutation cost is high. **Repair (decisive):** the power analysis must
report minimum paired runs at base 0.30 for Δ∈{0.05,0.10,0.15,0.20}; if subtle effects need impractical
N, say so plainly — that is a finding, not a failure of the run.

## Q4. Goodhart on rework?

Could a skill suppress rework by writing files nobody re-touches (e.g. trivially correct stubs)? Less
gameable than self-report, but not immune. **Repair:** pair rework with fixture pass/fail so "no rework"
plus "fixture failed" is caught.

## Verdict

**flag — proceed to power analysis** with the repairs (causal claims anchored on rework; pre/post-merge
split; report minimum N per effect size; pair rework with fixture oracle). The power analysis decides
whether this is a usable gate or a gross-regression-only canary.
