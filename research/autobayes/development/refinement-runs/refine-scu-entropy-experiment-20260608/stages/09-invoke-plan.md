---
stage: 9
name: Invoke Plan (non-executed)
capability: invoke
mode: plan
status: pass
dispatch_id: refine-scu-entropy-experiment-20260608
---

# Invoke Plan — SCU Entropy Experiment (non-executed)

A non-executed plan. Running it is owned by `experiment-harness`, not this refine loop.

## Plan → Waves → Tasks

### Wave 0 — Pre-registration (gate before any measurement)

- T0.1 Build the difficulty-matched corpus: one objective, a fixed obligation set, re-bundlable into `r ≈ {2,4,8,16}`; per-item difficulty proxy computed and shown flat across size bins.
- T0.2 Freeze the blind SCU rubric (one-responsibility, recomposition success); hash-commit text; define rater blinding protocol.
- T0.3 Pre-register: reference models (≥2), serializers (≥2), MDL coder, N/seeds, size grid bracketing predicted `r*`, full corpus list, hard repair budget for Proxy C, and the analysis script. Lodge predictions P1–P4.
- **Gate:** no measurement until Wave 0 artifacts are frozen.

### Wave 1 — Pilot (toy game, cheapest decisive falsification)

- T1.1 Compute Proxy B `r*` over 2 models × 2 serializers on 4 sizes × 6 items × N=3.
- T1.2 Score the blind rubric at the 4 size points.
- T1.3 Evaluate P1–P4 against the pre-registered pass/stop criteria.
- **Gate (stop rule):** edge `r*`, or `r*` spread > 1 bin, or rubric peak > 1 bin / wrong sign → **stop, program falsified at this scale**; record and route to residue.

### Wave 2 — Full sweep (only if Wave 1 passes)

- T2.1 Extend size grid and corpus; full Proxy A curve (left arm, Miller–Madow-corrected, judge κ-audited).
- T2.2 Full Proxy C curve (right arm, per-obligation normalized, hard repair budget enforced; raw + normalized reported).
- T2.3 Full Proxy B curves across all codings; confirm `r*` invariance at scale.
- T2.4 Composition test: does A (descending) + C (ascending) cross at an interior `r*`, and does B's `r*` agree?

### Wave 3 — Adjudication and handoff

- T3.1 H1 verdict: interior minimum present and codebook-invariant?
- T3.2 H2 verdict: minima co-locate with blind-rubric quality peak within tolerance?
- T3.3 Write claim-adjudication record (source-backed, marks borrow/analogy/reject/promote-residue).
- T3.4 Route outcome to the Craft definition owner as a **candidate** input to the R1 term-split decision-gate.

## Pre-registered prediction (the falsifiable spine)

> At least one spread proxy descends, at least one residue proxy ascends, their crossing
> `r*` is reference-model-invariant, and `r*` co-locates with blind SCU quality. **Any of:
> all-monotone, codebook-variant `r*`, or no co-location ⇒ "SCU is the local minimum of
> entropy" is refuted as written.**

## Experiment-harness handoff fields

- Run schema: proxies A/B/C metric defs + estimators (from stage 6 receipts).
- Fixtures: corpus item list, size bins, codings, seeds.
- Metrics/objectives: `r*` location + invariance; Spearman ρ; curvature CIs.
- Stop rules: Wave 1 gate.
- Non-claim boundary: harness validates schema/fixtures/metrics; it does not assert live results, and nothing edits the Craft definition.

## Owner boundary

Plan only. No execution, no Craft-definition edit. Next route = `experiment-harness` for the run, then a `decision-gate` (R1) for the owner.
