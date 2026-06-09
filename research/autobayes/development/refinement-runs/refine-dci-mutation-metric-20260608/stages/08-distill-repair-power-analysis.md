---
stage: 8
name: Distill Repair (power analysis)
capability: distill
mode: validate
pattern: toy_game
status: flag
verdict: gross-regression-only-canary
dispatch_id: refine-dci-mutation-metric-20260608
subagent_receipts:
  - role: power-analysis-reviewer
    agent_id: a0121922320a9c34e
---

# Distill Repair — Power analysis (real telemetry, n=398)

## Base rates (computed)

- Overall residue rate (execution-bearing, n=83): **0.385**. Per-sigil: task-session 0.375 (N=32),
  invoke 0.286 (N=21), experiment-harness 0.333 (N=15). Smaller sigils noisier on tiny N.
- **Realistic per-version sample = ~7–16 per arm** (per-sigil N halved across before/after).

## Required N per arm — 80% power, α=0.05 (computed)

| Δ (p1 = p0−Δ) | Unpaired two-proportion | Paired McNemar |
|---|---|---|
| 0.05 | 1354 | 254 |
| 0.10 | 323 | 91 |
| 0.15 | 135 | 52 |
| 0.20 | 71 | 36 |

Pairing buys ~4–5× — but even the cheapest cell (Δ=0.20 paired = **36 pairs**) exceeds every
per-sigil ceiling. Pooling all 83 (~41/arm) still only reaches useful power around Δ≳0.30, and
introduces sigil-mix heterogeneity (Simpson-reversal risk).

## Verdict

> **gross-regression-only-canary.** At current data volume the residue differential can flag only a
> **large regression (Δ≳0.30–0.40, residue roughly doubling)** as a noisy alarm. It **cannot** serve
> as a calibrated pass/fail gate for the plausible **5–20pp** effects a normal skill edit produces.

## What would make it a real gate (the honest cost)

Detection power is purely a **sample-size** problem, and it is buyable:
- Δ=0.15 needs ~**52 paired fixtures** per skill (McNemar); Δ=0.10 needs ~**91**.
- So a real gate requires a **dedicated replay corpus of ~50–100 fixtures per skill**, run before/after
  through the harness — not the incidental live telemetry. That is real compute cost, but it is
  concrete and bounded.

## Assessment-failure note (honest)

The metric is **underpowered as built on incidental telemetry** — recorded as a flag, not dressed as
success. The conceptual design (observer-independent rework anchor + paired test) is sound; the binding
constraint is data volume, which only a sized replay corpus fixes.

## Most important caveat

The N's assume independent replays of a *fixed* corpus. Observational history has a drifting sigil/mode
mix and evolving `observer_version`, so any live shift is confounded with corpus composition unless you
freeze and replay an identical fixture set.
