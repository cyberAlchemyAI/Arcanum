---
stage: 2
name: Invoke Define
capability: invoke
mode: define
status: pass
dispatch_id: refine-dci-mutation-metric-20260608
---

# Invoke Define — DCI as skill-mutation differential

## Objective

Define DCI not as an absolute gauge but as **ΔDCI(skill v_old → v_new) on a fixed workload** —
a regression signal answering "did this skill edit make the skill leave more or less residue?"

## What the telemetry actually gives us (grounding)

- **No `skill_version` key exists.** It must be added (content hash of the skill file at
  invocation). This is the enabling change.
- **`observer_version` DOES exist** (393/398). The co-mutating component is already version-tracked
  — so we can **stratify/hold `observer_version` fixed** across before/after to separate a skill
  effect from an observer-reporting change. This is the lever that makes observer-independence
  *partially achievable from existing data*.
- `run_id`, `session_id`, `dedupe_key`, `command`, `capability`, `target_artifact` exist →
  usable for replay grouping and attribution.
- **Residue rate on execution-bearing units is ~0.30–0.38** (task-session 0.38, invoke 0.29,
  experiment-harness 0.33) — not the ~0.10 feared. A larger base rate makes a shift easier to
  detect. But **per-sigil N is small** (15–32), so power is the open question.

## The make-or-break: observer co-mutation

You cannot evaluate a change to a skill using that skill's own self-report. Mitigations the
design must choose among:
1. **Hold `observer_version` fixed** across v_old/v_new (cheap, partial — only controls observer
   *version* drift, not whether the skill's content changes what it chooses to report).
2. **Observer-independent ground truth** — git file-rework, fixture pass/fail from the harness,
   downstream failure. The only fully clean option.

## Closure

The metric is a differential; the enabler is `skill_version`; the threat is observer co-mutation;
the levers are `observer_version` stratification + observer-independent ground truth; feasibility
hinges on a power analysis given small N. Ready for refine-review.
