---
stage: 6
name: Invoke Redefine / Design (differential tournament)
capability: invoke
mode: design
pattern: tournament
join: ranked
status: pass
dispatch_id: refine-dci-mutation-metric-20260608
subagent_receipts:
  - role: ground-truth-differential-designer
    agent_id: a54a80b356cb7e580
  - role: harness-replay-designer
    agent_id: ac9826efa8fa68769
  - role: live-version-slice-designer
    agent_id: a867a73e0b434f714
---

# Invoke Design — skill-mutation differential (ranked ladder)

## Pareto comparison

| Design | Observer-independence | Workload control | Power (base ~0.30, small N) | Cost | Verdict |
|---|---|---|---|---|---|
| D-ground-truth (git rework, paired McNemar) | **structural** — rework authored by future external commits over `files_changed[]`; self-report cannot move it | replay | gross regressions Δ≥0.15–0.20 | medium (2 replays + git scan) | **trust anchor** |
| D-harness-replay (paired Wilcoxon on self-reported DCI) | **partial** — pinned `observer_version` + frozen reporting component + reporting-line-diff flag; **cannot** catch execution-prose priming the observer (confound #2) | replay | ~4–6 DCI pts if coherent | cheap (2 replays) | **practical gate** |
| D-live-slice | **none** | none | only huge regressions | lowest (groupby) | **screening canary** |

## Ranked decision — a 3-layer ladder, not one winner

> **Compose, don't pick.** (1) **D-live-slice** = always-on cheap canary that *flags* candidate
> version transitions, never decides. (2) **D-harness-replay** = the practical fixed-workload gate,
> trustworthy for *coherent execution-side edits that do not touch reporting*, and self-flagging
> `reporting-confounded` when they do. (3) **D-ground-truth (git rework)** = the only
> observer-independent anchor — used to adjudicate the cases replay flags as confounded, and as a
> post-hoc CI canary over accumulated rework history.

## Does the make-or-break resolve?

**Observer-independence is solvable — but only by the git-rework signal.** Self-reported-residue
differentials (replay, live) are contaminated by execution-prose priming that no version-pin,
component-freeze, or line-diff fully catches ("self-report measuring self-edit"). So a causal "this
mutation improved the skill" claim **must** be anchored on rework, not DCI. The catch:

> **The git-rework signal is *trailing*** — in a pre-merge sandbox the future commits that
> constitute residue do not exist yet. It is strongest as a **post-hoc CI canary on accumulated
> history**, weakest as a same-second pre-merge gate. Partial fix: seed the replay corpus with units
> of *known historical rework* and test whether v_new reproduces the bad output.

## Enablers required (none exist today)

1. **`skill_version`** field = content hash of the skill file at invocation (the missing join key).
2. **Harness replay driver** — check out v_old/v_new, run the same corpus into isolated branches,
   stamp `run_id`s with `skill_version`; assert `observer_version` equal across arms.
3. **Git-rework extractor** — per `files_changed[]` path, detect a later distinct commit re-touching
   it within a window, filtering lint/format noise.
4. **Frozen reporting component + reporting-line-diff** for the replay gate's confound guard.

## Statistics

Paired designs throughout (same fixtures both arms): **McNemar exact** (rework, binary) /
**Wilcoxon signed-rank** (DCI, continuous). Power rides on discordant-pair count, not N — pairing is
what makes small N usable. Per-sigil gates with a Bonferroni guard if pooling.

Carried to the power analysis: is even the anchor detectable at real N?
