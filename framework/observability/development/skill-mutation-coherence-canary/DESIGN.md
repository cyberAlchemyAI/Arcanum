---
observed_capability: invoke
invoke_mode: design
target_artifact: Skill-Mutation Coherence Canary
target_type: observability feature (cross-capability)
target_owner: observability (enabler + scorer); experiment-harness (replay); sigil-development (gate)
status: design (candidate, non-executed)
source_define: arcanum/research/autobayes/development/refinement-runs/refine-dci-mutation-metric-20260608/RESULT.md
date: 2026-06-08
---

# DESIGN — Skill-Mutation Coherence Canary

## 1. Define baseline (inherited)

Approved define input is the refine RESULT
([refine-dci-mutation-metric-20260608](../../../../research/autobayes/development/refinement-runs/refine-dci-mutation-metric-20260608/RESULT.md)):

- **Goal:** detect whether editing a skill made it leave more/less residue — a regression signal,
  not an absolute gauge.
- **Hard findings carried in as constraints:**
  - The enabler `skill_version` does **not** exist in telemetry today; it must be emitted.
  - Self-reported residue is **observer-co-mutation-contaminated**; only **git file-rework** is a
    structurally observer-independent anchor (but it is a **trailing** signal).
  - On incidental telemetry the differential is **gross-regression-only** (power analysis: Δ=0.20
    needs 36 paired runs, ~10 available). A calibrated gate needs a per-skill replay corpus.

## 2. Scope decision

Build **Mode A (gross-regression canary)** as the deliverable; carry **Mode B (calibrated replay
gate)** as an explicit deferred layer (L3), behind a value/cost boundary. This matches the evidence:
Mode A is cheap and genuinely useful; Mode B is real work justified only if merge-gating is wanted.

## 3. Domain model

| Entity | Meaning | Source |
| --- | --- | --- |
| `SkillVersion` | content hash of the resolved skill file(s) at invocation | new, emitted by the observability hook |
| `InvocationSignal` | one telemetry record | existing `sigil-invocations.jsonl` |
| `ResidueScore` | per-record DCI = 100·(1−weighted_residue) | derived (deterministic scorer) |
| `VersionSlice` | aggregate residue rate / mean DCI for one `SkillVersion` | derived |
| `CanaryFlag` | a gross cross-version swing (Δ ≥ threshold) | derived |
| `ReworkEvent` | a later distinct commit re-touching a unit's `files_changed[]` | derived from git history |

## 4. Capabilities / operations

| Operation | Owner | Input → Output |
| --- | --- | --- |
| `emit_skill_version` | observability hook | resolved skill file(s) → `skill_version` stamped on each signal |
| `compute_dci` | scorer (read-only) | execution-bearing signals → `ResidueScore` per record |
| `slice_by_version` | scorer | scores + `skill_version` → `VersionSlice` (mean DCI, N, residue-bearing count) |
| `flag_regression` | canary | adjacent `VersionSlice` pair → `CanaryFlag` if ΔDCI ≥ threshold and N ≥ min |
| `confirm_rework` | rework anchor (post-hoc) | flagged unit `files_changed[]` + git log → `ReworkEvent` confirm/deny |
| `surface` | workflow-reflect | flags + slices → operator readout |

## 5. Events

`skill-version-stamped` → `dci-scored` → `version-slice-updated` → `canary-flagged` →
`rework-confirmed` (post-hoc).

## 6. Architecture / infrastructure

- **Emission** hooks the existing observability append path
  (`arcanum/framework/observability/scripts/observe-invocation.sh` / `signal-observer` /
  `arcanum-hook-post-tool-use.sh`). It computes a content hash of the skill file the runtime loaded
  and adds `skill_version` to the envelope next to the existing `observer_version`.
- **Scorer** is a read-only function over `.arcanum/observability/signals/sigil-invocations.jsonl`
  (no writes to the store). Pure, deterministic, replayable.
- **Canary** is a `workflow-reflect` lens, always-on, screening only.
- **Rework anchor** is a deterministic git-history extractor, run post-hoc.

## 7. Interaction model

`workflow-reflect` shows per-`skill_version` mean DCI + N + any `CanaryFlag`; a flag escalates to the
post-hoc rework anchor for confirmation; `sigil-development` consumes confirmed regressions in the
skill-mutation lifecycle.

## 8. Validation shape

- The scorer is validated on the existing store (it already discriminates clean vs residue-bearing
  with no overlap — prior backtest).
- Every readout is **labeled gross-regression-only** and shows `N` + residue-bearing count.
- Canary flags are **screening, never causal**; causal confirmation requires the rework anchor.

## 9. Glossary consistency

`DCI`, `residue`, `skill_version`, `observer_version`, `execution-bearing`, `gross-regression-only`,
`rework anchor` are used consistently with the refine run's definitions. No conflicts with the
canonical observability envelope (`observer_version` is the existing sibling field).

## 10. Honesty boundaries (design-level gates)

1. No readout may present DCI as an absolute quality score; it is a residue flag + trend.
2. No causal "this edit helped/hurt" claim without the rework anchor (observer-independent).
3. The rework anchor is trailing → post-hoc confirmation, not a same-second merge blocker.
4. Mode B (calibrated gate) stays deferred until a per-skill fixture corpus exists.

## Next route

`invoke plan` (this packet's PLAN.md + WORK-PACK.md), then `task-session` for L0–L2 execution;
`experiment-harness` + `sigil-development` for the deferred L3.
