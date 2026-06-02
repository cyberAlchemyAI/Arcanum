---
to: Vlad
from: Victor (multi-agent audit, synthesized)
re: "cyberAlchemyAI/Arcanum — third pass: the dynamics axis (scoring + sigil-improvement loop)"
date: 2026-06-02
audit-against: "arcanum @ 75b2230 (material files unchanged at HEAD c3c6bd0)"
status: draft for discussion
---

# To Vlad — Arcanum, third pass

The first two memos were both on the **static axis**: what a sigil *is* (typed residue, source-schema — TO-VLAD.md) and how sigils *relate* (kinds + edges — TO-VLAD2.md). This one is on the **dynamic axis**: how a sigil *improves over time from usage*. Different fibre, so it is a separate memo, not an edit to the other two — see "Why this is a separate memo" below.

Prior art, named first because the discipline demands it: **SkillOpt** (Yang et al., *Executive Strategy for Self-Evolving Agent Skills*, arXiv:2605.23904, cs.AI, 2026) is, in its own words, "the first systematic controllable text-space optimizer for agent skills." It treats the skill document as the external state of a *frozen* agent: a separate optimizer model turns scored rollouts into bounded add/delete/replace edits on a single skill doc, and **an edit is accepted only when it strictly improves a held-out validation score** (ties rejected). It is **offline** — the optimization happens before deploy, the skill is then frozen, zero inference-time calls added. Optimized skills transfer across model scales and between Codex and Claude Code harnesses. It positions against a contested field: human-authored, one-shot LLM, Trace2Skill, TextGrad, GEPA, EvoSkill. **Where this memo proposes a score-and-edit loop over sigils, that loop owes SkillOpt a first-paragraph citation.** Arcanum's governance/taxonomy/lifecycle contribution does not — to that, SkillOpt is adjacent work, a nice-to-cite.

This memo originated from a single conversation about that paper, *then* went through the same audit discipline as the prior two (explorer + skeptic + auditor, subset rule). I am flagging up front that the audit **reversed two of my own first-pass claims** — surfaced under "What the audit killed" — because the honest version is much smaller than the version I started with.

---

## The one-sentence thesis (everything below is a subset of this)

Arcanum **already owns** a scalar grading oracle (`benchmark/`) and a categorical reflection loop, but they are **disconnected**: the oracle grades *external* agents, the loop over *sigils* is human-gated and emits no score. The honest contribution is **wiring an external grader to a sigil-improvement loop**, whose one genuine residue is that **a sigil must not author the surface it is graded on**.

---

## Finding 1 — The grading oracle and the sigil-improvement loop are disconnected

### Claim

The machinery for scalar grading exists in the repo. The machinery for improving a sigil exists in the repo. They do not touch.

### Evidence

- **A real scalar oracle exists.** `benchmark/src/schemas.ts:77` declares `ScoreResult.components: Record<string, number | boolean>` (and `:69` `metrics?: Record<string, number>`); `benchmark/artifacts/.../score-result.json` carries `speedupVsBaseline: 9.23` with a numeric `threshold` gate. This is a graded scalar with a pass-condition — exactly the shape a SkillOpt-style accept/reject gate consumes.
- **But it is sigil-blind.** `benchmark/` grades *external autonomous coding agents* via an `AgentAdapter` over `patch.diff` (`benchmark/src/agent-adapter.ts:8-11`, `ARCHITECTURE.md:14`). `grep -r "arcanum|sigil|spell|arcana" benchmark/src` returns **zero lines**. The oracle has never been pointed at a sigil.
- **The sigil loop emits no score.** The observability hook (`framework/observability/SIGIL-OBSERVABILITY-HOOK.md:41-59`) emits categorical signals only: `quality_bar_status: pass|partial|fail|not_checked`, `anti_pattern_hits[]`, `workflow_gaps[]`, `output_contract_drift: bool`. The `reflection-state.json` counters are **integer event-counters that gate *when* reflection fires**, not a reward maximized over runs. `arcana/workflow-reflect/` reads those signals and writes *human-read improvement proposals* — it does not accept edits against a score.

### Why this matters

A SkillOpt-style loop needs exactly one thing Arcanum is missing: a **scalar, held-out score feeding an accept/reject gate**. Arcanum has the scalar (pointed at the wrong target) and the improvement loop (carrying no scalar). **The gap is the wire between them — not a missing layer.** This is the smaller, defensible claim; the larger one ("a whole missing dynamics layer") is false and is cut below.

### Recommendation

Do **not** start by building an optimizer. Start by making *one* sigil produce a scalar on a held-out set and routing it through the `benchmark/` oracle shape. The optimizer (SkillOpt, offline) is the cheap downstream piece once the score exists.

---

## Finding 2 — The reward surface is the hard part, and it has a sweet-spot constraint

### Claim

The thing actually missing is the **reward + held-out task distribution**, not the optimizer. And not every sigil can have one: the constraint is **external-grader vs. self-defined denominator**, not "easy vs. worth optimizing."

### Evidence

The sigils that look easiest to score define their own ground truth, which makes the score Goodhart-trivial:

- `transmutations/context-builder/` emits an `Obligation coverage: <percent>` (`SKILL.md:112-113`) — but the obligation *denominator is self-parsed by the sigil* (`SKILL.md:53`). Optimizing against a denominator the sigil itself sets trains the bookkeeping, not the capability.
- `transmutations/codex-goal-profile/` produces a `/goal` whose **verification surface the sigil itself authors** (`SKILL.md:79-80`: "measurable completion condition", "names the verification surface"). A downstream Codex run is then graded against that self-authored target.
- `arcana/definitions-governance/` has integer counts (`Undefined critical terms`, `Conflicting consumers` — `SKILL.md:83-86`) that come closest to an external check, but the sigil is low in model-judgment, so there is little for an optimizer to improve.

### Recommendation

The first target must have an **external** grader. Two honest options:

1. **`context-builder` with a held-out obligation fixture** — supply the obligation set from a curated/external fixture instead of the sigil's self-parsed matrix. This neutralizes the self-denomination and gives a graded coverage scalar on a synthesis sigil.
2. **A patch-emitting sigil routed to the existing `benchmark/` oracle** — reuses the scalar that already exists (`speedupVsBaseline` et al.) rather than inventing a new one.

Pick one as the pilot. (Reminder of the reversal: **not** `codex-goal-profile` — see below.)

---

## Finding 3 — The one genuine residue: a sigil must not author the surface it is graded on

### Claim

This is the single piece SkillOpt does not give you. SkillOpt assumes an external benchmark with ground truth *by construction*. Arcanum sigils that generate their own verification surface or denominator (`codex-goal-profile/SKILL.md:79-80`, `context-builder/SKILL.md:53`) create a closed loop: optimizing trains the *grader*, not the capability. SkillOpt has no vocabulary for this failure mode because its benchmarks can't exhibit it.

### Recommendation

Add a **grader-independence** property — either a field in the sigil output-contract or a `spellcraft validate` check: *the artifact a sigil is scored against must not be authored by that sigil.* This is the residue worth typing, and it is the part of TO-VLAD3 that is genuinely Arcanum's contribution rather than SkillOpt's. It also slots onto TO-VLAD2's edge vocabulary: grader-independence is a `requires-evidence-from` edge to an *external* node, never a self-loop.

---

## Why this is a separate memo, not an edit to TO-VLAD2

The fold-in case is tempting and it loses on type grounds. TO-VLAD2 Finding 1 (and TO-VLAD.md edit 1) want a typed **output-contract** — a *containment predicate*: "what the output **is**", boolean/structural (`TO-VLAD.md:96`: output-contract covers source-schema.required). A reward surface is a **magnitude on an ordered codomain**: "how **good** the output is", which *presupposes* the type is already fixed. Different fibres. Typing is the static axis TO-VLAD2 lives on; scoring is the dynamic axis it explicitly defers (`TO-VLAD2.md:340`). So: separate memo.

But the dependency is real and runs one way: **typing → scoring → optimization.** You cannot define a sigil-scoped scalar without a typed output to score (TO-VLAD2 Finding 1 / TO-VLAD.md edit 1). This memo is **downstream of the other two**, not parallel to them. It is also not independent corroboration — it shares the audit pipeline; treat the three memos as one observation seen from three depths.

---

## What I'm leaving open for you

Three calls only you should make.

### Q1 — Should the sigil-improvement loop be automated at all?

SkillOpt removes the human from accept/reject — the held-out score decides. Arcanum's culture is the opposite (human gate in `robot-talks`, "Artifact Over Vibes"). The honest framing is: SkillOpt powers the **inner reflect→edit** proposal loop, but **promotion stays human and multi-criteria**. If you'd rather keep the whole loop human-gated, this entire memo is deferred — say so and it parks.

### Q2 — Train on logged platform usage, or on curated fixtures?

The plan to train offline on real users' rollouts is sound (and is what SkillOpt does, offline). But usage gives you the *rollouts and the distribution* — it does **not** give you the *label*. The reward still has to come from an observable usage outcome (accepted/rejected, reused/discarded, passed-downstream). Which sigil's usage produces a clean such signal decides whether Q3's pilot is (1) or (2). "Live" optimization (scoring on the same traffic you optimize against) is **not** the SkillOpt setup and reward-hacks — keep it offline.

### Q3 — Which pilot: held-out `context-builder`, or a patch-sigil on the `benchmark/` oracle?

Determines edits 2 and 4. (2) is more representative of Arcanum's synthesis work but needs a fixture built; the patch-sigil reuses an oracle that already exists but is less representative.

---

## Concrete edits, ordered by leverage

Four edits. They are strictly sequenced — each is pointless before the prior lands.

1. **`benchmark/` — add a sigil `AgentAdapter` (or document why not).** Smallest useful proof: make *one* sigil routable through the oracle that already exists, instead of only external `patch.diff` producers. *Effect:* the scalar surface stops being sigil-blind.
2. **A held-out fixture set for the pilot sigil** — external ground truth, **not** the sigil's self-parsed matrix. *Effect:* gives Finding 2 a usable scalar; neutralizes self-denomination.
3. **A grader-independence check** — sigil-contract field or `spellcraft validate` rule: the scored artifact must not be self-authored. *Effect:* lands Finding 3's residue; blocks the `codex-goal-profile`-class reward-hack before any optimizer runs.
4. **Only after 1–3: an offline optimizer** following SkillOpt's accept-on-strict-held-out-improvement (cite SkillOpt here, first paragraph of that doc). *Effect:* closes the loop. **Offline only** — frozen skill at deploy, per SkillOpt; not live.

---

## What the audit killed (honesty about my first-pass claims)

The first-pass version of this memo made three claims the skeptic pass reversed or cut. Recording them so they don't creep back:

- **"Arcanum has no scalar reward surface"** — **false.** `benchmark/src/schemas.ts:77` + `score-result.json` prove a scalar oracle exists. The defensible claim is only "no scalar *wired to the sigil-improvement loop*."
- **"A whole missing dynamics layer"** — **inflated.** The machinery exists; only the *wire* (Finding 1) and the *residue* (Finding 3) are new. Cut the layer framing.
- **`codex-goal-profile` as the strongest first target** — **reversed.** It is the *worst*: it authors its own verification surface (`SKILL.md:79-80`), so optimizing it trains the grader. It is the canonical example of the Finding 3 failure mode, not the pilot.

Also cut: **live/online optimization** (SkillOpt is offline; live reward-hacks without a held-out set); **a blanket SkillOpt citation as framing tax** (the duty bites only on the score-and-edit verb).

---

## One observation beyond the audit

The first two memos gave Arcanum a type system but no thermometer. This memo's finding is that the thermometer already exists — it is just plugged into the wrong socket. That is a much cheaper fix than "build an optimizer," and it is the kind of fix that only becomes visible once you notice the repo is carrying two halves of the same loop in two folders that never reference each other (`benchmark/` and `framework/observability/`). The framework lens said *look for the dynamic axis*; the repo said *you already built most of it*. The residue worth keeping — grader-independence — is the one thing neither the lens nor SkillOpt handed me; it fell out of the skeptic pass.

— V.
