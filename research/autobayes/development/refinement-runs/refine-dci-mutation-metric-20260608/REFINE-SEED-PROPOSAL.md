---
profile: refine
run_id: refine-dci-mutation-metric-20260608
name: DCI as a skill-mutation regression metric (differential)
description: Seed to redesign DCI from an absolute coherence gauge (rejected) into a controlled differential — ΔDCI(skill v_old → v_new) on a fixed workload — that detects whether a skill mutation improved or degraded the residue the skill leaves, confronting the observer-co-mutation problem head-on.
type: refine-seed-proposal
status: proposed
preset: full
research_mode: research-if-gap-appears
parent_run: arcanum/research/autobayes/development/refinement-runs/refine-coherence-metric-20260608
last_updated: 2026-06-08
---

# Refine Seed — DCI as a skill-mutation regression metric

## Target

The prior run designed DCI as a per-unit coherence score, and a critique showed it does not
hold up as an **absolute gauge** (circular self-report, ceiling skew, sigil-identity confound,
Goodhart). The operator reframed it: **"I'll make mutations to skills — could DCI detect their
impact?"** This run redesigns DCI as a **controlled differential / regression detector**:

> **ΔDCI(skill v_old → v_new) on a fixed workload** = did editing this skill make it leave more
> or less residue? A CI-style quality gate for skill mutations, not a dashboard.

## Why the differential framing survives the earlier critique

- **Sigil-identity confound removed:** comparing a skill to *itself* before/after holds the
  observer and sigil constant; consistent observer bias cancels in the delta.
- **Ceiling skew tolerable:** we need to detect a *shift* in a rare-event rate, not a smooth dial.
- **Construct moves from "coherence" to "regression," which is testable:** "did residue go up
  or down after this edit, on the same work" is a falsifiable claim.

## The three enabling requirements (the design must establish these)

1. **Version tagging.** Each signal must carry `skill_version` (content hash of the skill file
   at invocation). Not emitted today — the design proposes adding it to the observability
   envelope. Without it, no before/after slice exists.
2. **Fixed workload (replay).** Compare v_old vs v_new on the **same fixtures**, not live drift —
   the `experiment-harness` role. Otherwise ΔDCI just reflects which tasks happened to run.
3. **Observer independence (make-or-break).** Arcanum sigils carry their own observer/quality-bar
   logic. If a mutation changes how the skill *reports*, ΔDCI moves for a measurement reason, not
   a real one. The design must either (a) score with a **frozen external observer**, or (b) use
   **observer-independent ground truth**: real file-rework from git, fixture pass/fail from the
   harness, downstream failures. If neither is cheap, the differential is contaminated and the
   honest verdict is "does not make sense as built."

## Candidate differential designs (the tournament)

- **D-live:** version-slice live telemetry by `skill_version`; cheapest, but workload not held
  fixed and observer not frozen.
- **D-replay:** experiment-harness runs the same fixture corpus through v_old and v_new; holds
  workload fixed; observer still bundled unless frozen.
- **D-ground-truth:** score the replay with **observer-independent** signals (git file-rework,
  fixture pass/fail, downstream failure) — the only design that survives observer co-mutation.

## The toy-game (honest falsification)

On the existing telemetry + a simulated mutation: (a) can we even slice by a version-like key and
detect a shift? (b) **power analysis** — how many runs are needed to detect a change in a ~10%
residue rate? If it needs hundreds of runs per mutation, the metric is impractical and we say so.

## Write scope

- May write only under this run folder. May propose (not execute) an observability envelope field
  (`skill_version`) and an experiment-harness replay config. May not edit canonical packages.

## Done criteria

A non-executed plan with: the selected differential design, the observer-independence solution
(or an explicit block if none is cheap), a power-analysis result on real telemetry, and handoffs
to `experiment-harness` + `observability` + `sigil-development` (the skill-mutation lifecycle owner).

## Validation surface

- `dispatch-spec` validates the route. The toy-game does a real power analysis on
  `sigil-invocations.jsonl`. `experiment-harness` owns replay; `sigil-development` owns the
  skill-mutation lifecycle this metric would gate.

## Preset / research

- **Preset:** full (tournament + power-analysis toy-game).
- **Research:** research-if-gap-appears — local-first; escalate only if a named external method
  gap appears (e.g. a settled before/after rare-event change-detection test).

## Planned stage configuration

Canonical ten-stage loop ([REFINE-DISPATCH.json](REFINE-DISPATCH.json)) with overlays
`baseline_sequence`, `memory_residue`, `tournament_for_alternatives` (three differential designs),
`toy_game_for_low_cost_falsification` (power analysis). Subagents **recommended** (one designer per
differential + a feasibility/power reviewer); requires operator approval.
