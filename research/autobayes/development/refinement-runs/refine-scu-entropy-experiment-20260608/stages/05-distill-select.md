---
stage: 5
name: Distill (select coherent unit)
capability: distill
mode: standard
status: pass
dispatch_id: refine-scu-entropy-experiment-20260608
---

# Distill — Smallest coherent measurable unit

## Selected unit

> **One granularity sweep of a single fixed objective over a difficulty-matched corpus,
> measured by all three proxy curves separately, with unit size operationalized as the
> number of cross-unit relations/obligations the unit must preserve.**

This is the smallest unit that still carries the whole hypothesis: it has one x-axis,
separable y-axes, a blind SCU rubric, and a recomposition path into a full experiment.

## Why this unit (SCU reasoning, applied reflexively)

- Smaller (e.g. "just measure one proxy on one unit") loses H1 — you cannot see a curve from one point.
- Larger (e.g. "sweep across many objectives and corpora at once") injects the difficulty confound the curve is supposed to isolate.
- This unit holds exactly: one objective, one size axis, three separable proxies, one blind rubric.

## Rejected alternatives (residue ledger)

- **Cross-corpus sweep** — rejected: confounds difficulty with size (refine-review Q5).
- **Single blended entropy score** (average of A/B/C) — rejected: proxies measure different sub-mechanisms; blending hides shape (refine-review Q2).
- **Human-only SCU judgment as the entropy axis** — rejected: that is the *dependent quality* in H2, not the entropy proxy; using it as both is circular (refine-review Q3).

## Repairs folded in

All four refine-review repairs are now constraints on the design: separate proxy
curves, blind SCU rubric, single primary size axis (relations/obligations),
difficulty-confound control.

## Recomposition path

Unit → design tournament (proxy A/B/C metric+estimator+predicted curve) → pareto rank →
pilot falsification → non-executed plan → experiment-harness handoff.
