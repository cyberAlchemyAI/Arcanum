---
observed_capability: invoke
invoke_mode: plan
artifact: implementation-layering
target_artifact: Skill-Mutation Coherence Canary
complexity: medium
date: 2026-06-08
---

# IMPLEMENTATION-LAYERING — Skill-Mutation Coherence Canary

Layers are bounded by value/cost boundaries; promotion requires evidence from the prior layer.

## L0 — Minimum Working Unit (prove the spine end-to-end)

- **Scope:** emit `skill_version` on signals + a read-only `compute_dci` scorer + print mean DCI per
  `skill_version` from the store.
- **Value:** proves the enabler and the scorer work against real telemetry on one path.
- **Promotion evidence:** scorer runs on `sigil-invocations.jsonl`; at least one real `skill_version`
  appears stamped; mean DCI per version printed with N.
- **Boundary:** no canary logic, no git, no harness.

## L1 — Live-slice gross-regression canary

- **Scope:** `slice_by_version` + `flag_regression` (ΔDCI ≥ threshold, N ≥ min) + a `workflow-reflect`
  readout labeled gross-regression-only.
- **Value:** an always-on cheap safety net that flags big breakages after a skill edit.
- **Promotion evidence (from L0):** scorer + version slicing validated; threshold/min-N chosen from
  the real residue distribution (~0.30–0.38 base).
- **Boundary:** screening only; no causal claim; no git anchor yet.

## L2 — Post-hoc git-rework anchor (observer-independent confirmation)

- **Scope:** `confirm_rework` — given a flagged unit's `files_changed[]` + producing commit, detect a
  later distinct commit re-touching those paths within a window (filtering lint/format noise).
- **Value:** the only observer-independent confirmation of a flagged regression.
- **Promotion evidence (from L1):** a canary flag exists to confirm; rework extractor is deterministic
  and replayable from history.
- **Boundary:** trailing/post-hoc only; not a merge blocker.

## L3 — Calibrated replay gate (Mode B) — DEFERRED behind value/cost boundary

- **Scope:** experiment-harness replay driver + per-skill fixture corpus (~50–100 fixtures) + paired
  McNemar/Wilcoxon gate + frozen reporting component + reporting-line-diff confound guard.
- **Value:** a real merge-gating CI quality gate for skill edits.
- **Promotion evidence required before starting:** L1/L2 in use AND a decision to fund the per-skill
  fixture corpus (power analysis: Δ=0.15 → ~52 paired fixtures).
- **Boundary:** owned by `experiment-harness` + `sigil-development`; not part of the L0–L2 work-pack.

## Layer decision snapshot

| Layer | Build now? | Owner | Gate to next |
| --- | --- | --- | --- |
| L0 | yes | observability | scorer + emit proven on real store |
| L1 | yes | observability + workflow-reflect | threshold calibrated to real base rate |
| L2 | yes | observability | rework extractor deterministic |
| L3 | deferred | experiment-harness + sigil-development | explicit funding of fixture corpus |
