# TO-VLAD — memo series

External review memos to **Vlad** (Arcanum maintainer, `cyberAlchemyAI/Arcanum`) from **Victor**, each synthesized from a multi-agent audit of the repo (deep slice-audit → skeptics/devil's-advocate → reviser). They are *drafts for discussion*, not change orders.

## Shared method & discipline

- **Audit pipeline:** several agents audit disjoint slices; separate agents challenge the findings; a reviser keeps only what survives the challenge. Most proposals get cut on the way (memo 2 cut 8 of 10 edits and 4 of 10 kinds).
- **Subset rule (claim ≤ proof):** every finding must stand on plain engineering merit. Where categorical / framework vocabulary appears, it is kept only when it predicts something the engineering-only reading would miss; otherwise it is stripped (both memos have a "what I deliberately did not recommend" section recording the cuts).
- **Cite, don't rediscover:** prior art (e.g. `domainspec/TAXONOMY.md`) is credited as parent pattern in the body, not as a footnote.

## The memos

### [`TO-VLAD.md`](TO-VLAD.md) — first pass (2026-05-20)
**Theme: gaps at the *sigil layer*.** Three load-bearing findings:
1. **Residue has no type at any layer** — the framework's central unit (what an artifact cannot carry across its boundary) has no first-class representation; the sigil template ships without a `<source-schema>` / residue field.
2. **Phase joins are the leak site** — when a spell composes A → B, nothing checks B's input requirements are met by A's output contract; `spellcraft validate` checks structural completeness, not contract-join.
3. **The tower is documentary, not measured** — `tier` is recorded but no telemetry answers "does climbing tier reduce `workflow_gaps` per intent?"; reflection fires on activity count, not residue.

Plus a subtler finding (`arcana/` conflates domain- / meta- / registry-orchestrators) and **9 concrete edits ordered by leverage**. Open questions: Quality-Bar iso framing deliberate or oversight; where deprecation authority lives; is `arcana/` one tier or three.

### [`TO-VLAD2.md`](TO-VLAD2.md) — second pass (2026-06-01)
**Theme: the *type substrate* underneath memo 1.** One load-bearing finding with two downstream:
1. **Sigils are untyped and inter-sigil edges have no vocabulary** — `tier` + free-text `domain` is the only typing; the registry has a single implicit edge (`spell composes sigil`). By contrast `domainspec/TAXONOMY.md` (25 meta-types) + `RELATIONSHIPS.md` (29 typed edges) do the same work over a richer surface. **Recommendation:** replicate that pattern — `SIGIL-KINDS.md` (6 kinds) + `SIGIL-EDGES.md` (2 enforced + 8 declared-only edges).
2. **Spell composition is heterogeneous** — only 5 of 11 spells are pipelines; memo 1's contract-join check would false-positive on the rest without a `shape:` tag.
3. **No reverse path from deployed sigil to design intent** — drift between a shipped sigil and its authoring spec is undetectable (gated: build only if drift is confirmed real).

**8 edits**, several gated on open questions Q1–Q4 (drift real? six-kind taxonomy right? spell-shape set right? willing to take a CI gate?). Explicitly notes it is *not independent corroboration* of memo 1 — same audit pipeline, one observation from two angles.

### [`TO-VLAD3.md`](TO-VLAD3.md) — third pass (2026-06-02)
**Theme: the *dynamic axis* — how a sigil improves over time from usage.** One thesis, three findings:
1. **The grading oracle and the sigil-improvement loop are disconnected** — `benchmark/` is a working scalar oracle (`speedupVsBaseline`, numeric thresholds) but grades *external* coding agents and is sigil-blind; the sigil reflection loop emits only categorical signals and human-read proposals. The gap is **the wire between them, not a missing layer.**
2. **The reward surface is the hard part, with a sweet-spot constraint** — the real axis is *external-grader vs. self-defined denominator*. First target must have an external grader: `context-builder` with a held-out fixture, or a patch-sigil routed to the existing `benchmark/` oracle.
3. **The one genuine residue: a sigil must not author the surface it is graded on** — the failure mode SkillOpt can't exhibit (its benchmarks are external by construction); the part that is genuinely Arcanum's, not SkillOpt's.

Prior art cited first-paragraph **for the score-and-edit verb only**: SkillOpt (arXiv:2605.23904). **4 sequenced edits**; open questions Q1–Q3 (automate the loop at all? train on logged usage vs fixtures? which pilot?). Carries a "What the audit killed" section recording two reversed first-pass claims (no-scalar-surface; Codex-Goal-Profile-as-target) — see below.

## How they relate

Layered, not parallel. Memo 1 names what is missing *at* the sigil layer (residue, source-schema, contract-join, measured tower). Memo 2 names the layer *underneath*: the type system that sigils and spells are nodes of. Memo 3 names the layer *on top*: how a typed, scored sigil improves over time. The dependency runs one way — **typing → scoring → optimization** — so read in order: **TO-VLAD.md → TO-VLAD2.md → TO-VLAD3.md**. None is independent corroboration of the others; all three share one audit pipeline, one observation seen from three depths.

**Axes:** memos 1–2 are the *vertical / static* axis (what sigils **are**, **how they relate**); memo 3 is the *horizontal / dynamic* axis (how a sigil **improves**). Memo 3 defends the split on type grounds: typing is a containment predicate ("what the output is"), scoring is a magnitude on an ordered codomain ("how good") — different fibres, so a separate memo rather than a fold-in.

## Provenance note

TO-VLAD3's findings originated from a single-pass conversation about the SkillOpt paper, then were run through the **same multi-agent audit** as the prior memos (explorer + skeptic + auditor, subset rule). That audit **reversed two first-pass claims** before any prose was written — "Arcanum has no scalar reward surface" (false; `benchmark/` exists) and "Codex Goal Profile is the best first target" (reversed; it self-authors its grader). Both are recorded in TO-VLAD3's "What the audit killed" section. The full audit trail (dispatch spec, 4 agents + auditor, verdict table) lives outside this repo at `domainspec-theorem/research-ai/skillopt-arcanum-optimization-axis/`.
