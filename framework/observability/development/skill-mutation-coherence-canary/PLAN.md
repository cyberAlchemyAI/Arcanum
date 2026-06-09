---
observed_capability: invoke
invoke_mode: plan
artifact: implementation-plan
target_artifact: Skill-Mutation Coherence Canary
complexity: medium
date: 2026-06-08
---

# PLAN — Skill-Mutation Coherence Canary

Plan → Waves → Tasks → SWUs. L0–L2 are in scope; L3 is a deferred handoff.

## Wave 1 — L0 spine

### T1.1 Emit `skill_version`
- **Owner:** observability hook (`observe-invocation.sh` / `signal-observer`).
- **Detail spec:**
  - Input: the resolved skill file path(s) the runtime loaded for the invocation.
  - Compute: `skill_version = sha256(concat(sorted(file_contents)))[:12]`.
  - Output: add `"skill_version": "<hash>"` to the signal envelope, sibling to `observer_version`.
  - Edge cases: skill file unreadable → emit `skill_version: "unknown"` (do not fail the run);
    multi-file skills → hash all loaded files in sorted path order.
  - Failure mode: never block the invocation on hashing.
  - Validation: a new signal line contains `skill_version`.
- **Validation strategy:** inspect a freshly appended record for the field.

### T1.2 `compute_dci` scorer (read-only)
- **Owner:** observability (new script under `scripts/`).
- **Detail spec (algorithmic):**
  - Input: path to `sigil-invocations.jsonl`.
  - Normalize `execution.status` → {ok, partial, fail} (handle enum drift: pass/flag/block/
    completed_with_block/None).
  - Execution-bearing filter: mode ∈ {new,update,execute} OR `files_changed` non-empty OR
    `workflow_gaps` non-empty.
  - Per record: `residue = min(0.30·r_status + 0.25·r_drift + 0.10·r_qbar + 0.35·r_gaps, 1)`
    (reopen term dropped per backtest); `DCI = 100·(1−residue)`; hard floor 40 on fail.
  - Output: per-record DCI + `skill_version` + `sigil`.
  - Validation: clean records → 100; gap/fail records < 100 (matches prior backtest separation).
- **Validation strategy:** re-run the prior backtest numbers (clean mean 100, residue-bearing < 100).

### T1.3 Print mean DCI per `skill_version`
- **Owner:** observability.
- **Detail spec:** group by `skill_version`, print mean DCI, N, residue-bearing count; exclude null.
- **Validation strategy:** output has one row per observed version with N.

## Wave 2 — L1 canary

### T2.1 `slice_by_version` + `flag_regression`
- **Owner:** observability + workflow-reflect.
- **Detail spec (algorithmic):**
  - Pair adjacent `skill_version` slices (by first-seen timestamp order).
  - `ΔDCI = mean_DCI(v_new) − mean_DCI(v_old)`.
  - Flag if `ΔDCI ≤ −THRESHOLD` AND both `N ≥ MIN_N`. Defaults: `THRESHOLD = 30` (gross only),
    `MIN_N = 10` (honest floor; below this, emit "insufficient-N" not a flag).
  - Edge cases: < 2 versions → no comparison; N below MIN_N → `insufficient-N`.
  - Failure mode: never flag on `insufficient-N`.
  - Output: `CanaryFlag{v_old, v_new, ΔDCI, N_old, N_new}` or `insufficient-N`.
- **Validation strategy:** synthetic two-version slice with a planted Δ≥30 fires; Δ<30 does not;
  N<10 yields `insufficient-N`.

### T2.2 workflow-reflect readout
- **Owner:** workflow-reflect (proposal/config only; no canonical edit).
- **Detail spec:** render per-version mean DCI + N + flags; **every readout labeled
  "gross-regression-only, screening; not causal"**.
- **Validation strategy:** readout shows label + N on every row.

## Wave 3 — L2 rework anchor

### T3.1 `confirm_rework` extractor (post-hoc)
- **Owner:** observability.
- **Detail spec (algorithmic):**
  - Input: a flagged unit's `files_changed[]` + producing commit/timestamp + window (K=5 commits or
    T=72h).
  - For each path: `git log --follow --format=%H -- <path>` after the producing commit, within window.
  - Exclude the producing commit and noise commits (lint/format/whitespace via path-allowlist or
    `git diff --check`).
  - Output: `rework ∈ {0,1}` per unit; aggregate confirm/deny for the flag.
  - Edge cases: path renamed → `--follow`; null `files_changed` → not analyzable (report).
  - Failure mode: missing git history → `rework: unknown`, never a false confirm.
  - Validation: a unit with a known later same-file edit → `rework=1`; an untouched file → `0`.
- **Validation strategy:** seed two fixtures (one reworked, one not) and assert the extractor.

## Deferred — L3 handoff (Mode B)

Hand off to `experiment-harness` (replay driver + per-skill fixture corpus, sized Δ=0.15→~52 paired)
and `sigil-development` (gate in the skill-mutation lifecycle). **Not in this work-pack.**

## Validation strategy summary (per slice)

| Slice | Validation |
| --- | --- |
| L0 emit | field present on a fresh signal |
| L0 scorer | reproduces prior backtest separation (clean 100 vs residue <100) |
| L1 canary | planted Δ≥30 fires; Δ<30 and N<10 do not |
| L1 readout | label + N on every row |
| L2 rework | seeded reworked/clean fixtures resolve correctly |
