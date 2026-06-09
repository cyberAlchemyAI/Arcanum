---
stage: 5
name: Distill (select unit of comparison)
capability: distill
mode: standard
status: pass
dispatch_id: refine-dci-mutation-metric-20260608
---

# Distill — unit of comparison and signal set

## Selected unit

> **One (skill_version, fixed-fixture-corpus) cell**, holding `observer_version` constant — the
> residue rate of skill `v` over a replayed fixture set. The differential is the change in that
> rate between two adjacent `skill_version` values on the *same* corpus and observer version.

## Signal set

- **Version key:** `skill_version` (to be added — content hash of the skill file). `observer_version`
  (exists) is a **stratifier held constant**, not the treatment.
- **Residue (self-reported, stratified):** the DCI backbone (status, quality_bar, gaps, drift).
- **Observer-independent ground truth (the trust anchor):** (a) git file-rework — a later commit
  re-touching files the unit "finished"; (b) fixture pass/fail from the harness; (c) downstream
  failure of a sibling/parent. At least one is required for a causal claim.
- **Replay grouping:** `run_id` / `session_id` / `dedupe_key` to align the same fixture across versions.

## Repairs folded in (from review)

- Stratification (`observer_version` fixed) **plus** ≥1 ground-truth signal — neither alone.
- Causal ΔDCI only within a **fixed-corpus replay**; live-slice is observational only.
- Power must be reported as **minimum runs per version** (base rate ~0.30, small N is the risk).

## Rejected alternatives

- Live cross-version slice with no replay — rejected for causal use (workload + difficulty drift).
- Using `observer_version` AS the treatment — rejected: it measures observer change, not skill change.
- Self-reported residue alone — rejected: cannot survive observer co-mutation.

## Recomposition path

unit + signals → 3 differential designs (tournament) → pareto on observer-independence →
power analysis on real store → skill-mutation gate + harness/observability/sigil-development handoff.
