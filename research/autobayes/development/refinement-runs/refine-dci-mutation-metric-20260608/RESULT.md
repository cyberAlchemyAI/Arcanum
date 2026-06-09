---
profile: refine
run_id: refine-dci-mutation-metric-20260608
type: refine-result
status: flag
preset: full
research_mode: no-research
dispatch: REFINE-DISPATCH.json
dispatch_validation: pass
verdict: makes-sense-conceptually-underpowered-on-incidental-data
last_updated: 2026-06-08
---

# Refine Result — Does DCI make sense as a skill-mutation metric?

## Direct answer

**Yes, conceptually — your reframing is right — but with one binding constraint: data volume.**

- The **differential framing fixes the confounds** that killed the absolute gauge: comparing a skill
  to *itself* before/after removes the sigil-identity confound, and an **observer-independent anchor
  exists** (git file-rework — authored by future external commits over `files_changed[]`, a field the
  skill cannot retroactively edit, so self-report changes can't move it).
- **But the power analysis on your real telemetry is decisive:** residue base rate is ~0.30–0.38 and
  per-sigil samples are tiny (15–32 total, ~7–16 per arm). Detecting a realistic 5–20pp mutation
  effect needs **36–254 paired runs** per skill; you have ~10. So on incidental telemetry it is a
  **gross-regression-only canary** — it catches a skill edit that roughly *doubles* residue, and is
  blind to the subtle effects a normal edit produces.

So: it makes sense, and it's not circular anymore — it's just **underpowered unless you feed it more
data.** That's a buyable problem, not a conceptual dead end.

## The make-or-break, resolved

Observer co-mutation **is** solvable — but **only** by the git-rework signal. Self-reported-DCI
differentials (live, replay) stay contaminated by execution-prose priming the skill's own observer
("self-report measuring self-edit"), which no version-pin / component-freeze / line-diff fully catches.
Causal claims must anchor on rework. Caveat: rework is a **trailing** signal → it's a post-hoc CI canary,
not a same-second pre-merge blocker.

## Two honest deployment modes

- **Free now:** add a `skill_version` hash to telemetry → a gross-regression canary (live-slice +
  post-hoc rework on accumulated history). Flags big breakages; never a calibrated gate.
- **Investment:** a **dedicated replay corpus of ~50–100 fixtures per skill** + harness replay + the
  git-rework anchor → a real calibrated CI gate (Δ=0.15 → ~52 paired fixtures). Real compute cost,
  bounded and concrete.

## Stage evidence

| Stage | Capability | Status |
|---|---|---|
| 1–5 (baseline → define → review → research → distill) | context-builder/invoke/interrogation/refine/distill | pass / flag |
| 6 Invoke Design (tournament) | invoke + 3 subagents | pass (3-layer ladder) |
| 7 Interrogation design-review | interrogation | flag |
| 8 Distill Repair (power analysis) | distill + 1 subagent | **flag — gross-regression-only-canary** |
| 9 Invoke Plan | invoke | pass (two modes) |
| 10 Final synthesis | interrogation + refine | flag |

## Recommendation

If you want a **cheap safety net** for skill edits: ship Mode A (the `skill_version` hash is one small
field, and a gross-regression canary is genuinely useful for catching breakages). If you want a **real
quality gate**: commit to Mode B's per-skill fixture corpus — that, and only that, makes ΔDCI a
trustworthy answer to "did my edit help." Anything in between is an underpowered number that will mostly
read noise.

## Open residue / next routes

- `observability-setup`: add `skill_version` (enables every mode).
- `experiment-harness`: replay driver + per-skill fixture corpus (the power fix).
- `sigil-development`: where the gate lives in the skill-mutation lifecycle.
- Standing finding: on incidental telemetry, **N is the wall** — no metric design escapes it.
