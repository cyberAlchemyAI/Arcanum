# findings.md — synthesis for `2026-06-16-arcanum-manual-question-types`

> Writer (synthesizer) return. Merges Explorer A (prompt-archaeology, witnessed), Explorer B
> (affordance-map, contracts), and Explorer C (latent-demand) from
> [`research.md`](research.md) into a question-type matrix, ready-to-insert manual edits, and a
> "questions now answered" list. Every load-bearing claim cites the explorer return it rests on
> (claim<=proof). Nothing is invented beyond A's witnessed types and C's latent types.

---

## 1 — Question-type matrix

Owner/witness column: a user prompt # (from A, P1–P6), a capability affordance with path (from B),
or `latent` (from C, with the persona that would ask). `sound?` = backed by a witness or a real
contract (not invented). Verdict GO = ship as a manual answer now; latent = real but unwitnessed,
ship only if flagged. Use-mode: `build-from-owned` = answerable from the user's own witnessed usage;
`novel` = answerable only from capability surface the user has not yet exercised.

| type | owner / witness | sound? | verdict | use-mode |
| --- | --- | --- | --- | --- |
| T1 Compose a multi-capability pipeline (craft→dispatch-spec→whisper) | P2 (A) | yes | GO | build-from-owned |
| T2 Distill a large body of knowledge into an explainer | P2 (A); whisper+distill, x-ray intake (B) | yes | GO | build-from-owned |
| T3 Inspect/expose the framework surface as base | P2 (A); x-ray | yes | GO | build-from-owned |
| T4 Execute by spawning subagents | P3+P4 (A); subagents-strategy P1 trigger + human gate (B/C#4) | yes | GO | build-from-owned |
| T5 Validate/design the dispatch route before running | P1+P2 (A); `dispatch.schema.yml` + dispatch-spec SKILL (B) | yes | GO | build-from-owned |
| T6 Build a research strategy that mines the user's own prompts | P4 (A) | yes | GO | build-from-owned |
| T7 Explain how to USE the tools, grounded in own use (refine + dispatch-spec + whisper) | P4 (A); refine ten-stage loop (B) | yes | GO | build-from-owned |
| T8 Explain governance concepts + rationale (constitution-governance) | P4 (A); constitution-governance SKILL (B) | yes | GO | build-from-owned |
| T9 Generate more questions of this kind (meta/self-amplifying) | P4 (A); subagents-strategy (B) | yes | GO | build-from-owned |
| T10 Retry / re-run a stalled attempt | P5 (A); orchestration control | yes | GO | build-from-owned |
| L1 "How do I see what just happened in a run I dispatched?" (Reviewer) | latent (C#1); signal-observer + `.arcanum/observability/` + workflow-reflect | yes (contract) | latent | novel |
| L2 "refine vs invoke vs task-session — when each?" (Consumer) | latent (C#2); lifecycle boundary (B: refine SKILL) | yes (contract) | latent | novel |
| L3 "How do I validate a dispatch-spec before running it?" (Researcher) | latent (C#3); dispatch-spec validate-mode + check-tension | yes (contract) | latent | novel |
| L4 "Tension between subagents-strategy and running inline?" (Author) | latent (C#4); subagents-strategy P1 trigger + human gate | yes (contract) | latent | novel |
| L5 "When does my pipeline graduate into a reusable spell?" (Author) | latent (C#5); 12-stage lifecycle + evidence-gated promotion | yes (contract) | latent | novel |
| L6 "How do I install this for another repo?" (Maintainer) | latent (C#6); arcanum-bootstrap, sigil-runtime-installer, FRIEND-INSTALL | yes (contract) | latent | novel |
| L7 "Which constitution applies to THIS artifact, and how do I compose one?" (Reviewer) | latent (C#7); constitution-governance select/compose/validate | yes (contract) | latent | novel |
| L8 "How do I make a run reflect on itself and improve next time?" (Author/Reviewer) | latent (C#8); observe→reflect→iterate, reflection thresholds | yes (contract) | latent | novel |
| L9 "How do I explain a pipeline to a non-Arcanum collaborator?" (Cross-functional) | latent (C#9); guide-architecture + User/Translate/Guide + whisper | yes (contract) | latent | novel |

**Cross-cutting fact (A, claim<=A's three-highest summary):** the user always couples *do* + *explain*;
every pipeline ends in an explainer; execution is delegated; no standalone "just run one tool"
intent was observed. The four named tutorial topics all sit on `build-from-owned` GO types (T1, T4,
T5, T7, T8) — none rests on a latent guess.

### FLAGS for the skeptics

- **L2 and L7 risk collapsing into existing manual content.** L2 (refine vs invoke vs task-session)
  is already partially answered by Part 2 Process B and the Consumer persona; L7 overlaps the new
  constitution-governance edit (d). Skeptic check: distinct questions or restatements? Proof they
  are distinct: L2 is a *boundary* question (which tool, when) — the manual states each tool's job
  but not the switch-rule (claim<=C#2 + B refine SKILL). Recommend folding L2's switch-rule into
  edit (b) rather than shipping a standalone section.
- **All L* items are unwitnessed (latent, C only).** They rest on persona inference + capability
  contract, not on a user prompt. Verdict held at `latent`, not GO. Do not present them as
  "questions the user asked" — present at most as "questions the manual can now answer."
  (claim<=C preamble: "no current witness".)
- **Edit (b) and edit (c) share the dispatch-spec surface and could blur.** (b) is about *refine*
  (the discovery loop that may emit a route); (c) is about the *dispatch-spec artifact shape*
  itself. Skeptic risk: a reader conflates "refine produced a Run Strategy Proposal" with "I
  authored a dispatch-spec." Proof they are distinct: refine does NOT auto-execute and shows a
  proposal first (claim<=B: refine SKILL); dispatch-spec validates *shape* and does not execute
  (claim<=B: dispatch-spec misread note). The edits below keep this seam explicit.
- **T9/T4 both route to subagents-strategy.** Not a contradiction: T4 is "execute by delegating,"
  T9 is "delegate to *amplify the question set*." Both GO (claim<=A: T4, T9). Skeptic should confirm
  no third subagent intent is missing — none observed.

---

## 2 — Tutorial improvement edits (ready-to-insert, manual voice)

Each is written to drop into ARCANUM-MANUAL.md, grounded in a witnessed type, with a source line in
the manual's `*(Source: …)*` style.

### (a) "Using the tools the way you work" — tie to T1 / T4

> ### Use the tools the way you already work
>
> If your instinct is "set up a space, route a plan, then turn it into something readable," Arcanum
> already matches that shape — you don't adopt a new workflow, you name the one you have. A common
> real pipeline is **`craft` → `dispatch-spec` → `whisper`**: open a Craft ledger to hold context
> and decisions, author a validated route, then synthesize the result into an explainer. Two habits
> make this work: **couple *do* with *explain*** — every pipeline ends in an artifact a human can
> read — and **delegate execution** by spawning subagents for bounded stages rather than running
> everything inline. *(Source: witnessed user pipeline P2 + delegation P3/P4 in
> [research.md](research.md))*

### (b) "How refine helps" — tie to T7 + B's affordance

> ### How `refine` helps (and how it differs from `invoke` and `task-session`)
>
> `refine` is for when the idea is still broad. It runs a fixed **ten-stage** discovery/design loop
> — context baseline → invoke-define → interrogation review → research decision → distill →
> invoke-design → design review → distill-repair → invoke-plan → final synthesis — and presets tune
> the *depth*, not the stages. It makes discovery **mandatory before design**, and it does **not
> auto-execute**: it shows you a Run Strategy Proposal and waits for permission, which mirrors a
> propose → permission → execute → synthesize habit. The switch-rule: reach for **`refine`** when
> the target is still vague; **`invoke`** when you already have approval and want durable
> define/design/plan artifacts; **`task-session`** only once a bounded unit of work exists. *(Source:
> [arcanum/arcana/refine/SKILL.md](../../../../arcana/refine/SKILL.md), via Explorer B affordance-map in
> [research.md](research.md))*

### (c) "Constructing a dispatch-spec to execute actions" — tie to T5 / T7 + B

> ### Constructing a `dispatch-spec`
>
> A dispatch-spec is the *shape* of a route, not the run itself — **it validates structure and does
> not execute**. The required fields are `dispatch_id, intent, mode, steps, gates, observability`.
> Each step carries `step_id, name, capability_ref, pattern, inputs[], outputs[]`, where `pattern`
> is one of the catalogued kinds (`route | sequential | fanout | dialectic | tournament | distill |
> xray | decision | validation | toy_game | synthesis | handoff`). Parallel steps need a
> `join_policy`; a `validation` step needs an `evidence_artifact`; techniques are cited from the
> catalog only when actually used; and **gates** (`policy | quality | promotion_guardrail |
> validation | human_approval`) prevent unsafe continuation. Use **design-mode** to author a new
> route and **validate-mode** to check an existing one before running. *(Source:
> [.claude/skills/dispatch-spec/SKILL.md](../../../../.claude/skills/dispatch-spec/SKILL.md) +
> [arcanum/formulae/dispatch-spec/dispatch.schema.yml](../../../../formulae/dispatch-spec/dispatch.schema.yml),
> via Explorer B in [research.md](research.md))*

### (d) "What constitution-governance is and why it matters" — tie to T8 + B

> ### What `constitution-governance` is, and why it matters
>
> A constitution is a **modular, scoped ruleset** that governs the *structure and form* of
> artifacts. Constitutions compose **narrowest-scope-first** (task → artifact-type → domain →
> framework → repo), and each rule declares a **validation mode** — `deterministic`, `review`,
> `hybrid`, or `none-yet`. The point is that it is a **selector**, not a 200-rule catch-all: you
> load only the rules that apply to the artifact in front of you. Why it matters, stated without
> circularity: it lets you **validate an artifact without context bloat**, and it lets you **promote
> work only once its rules are met** — so authority and quality stay legible instead of living in
> someone's head. *(Source:
> [arcanum/arcana/constitution-governance/SKILL.md](../../../../arcana/constitution-governance/SKILL.md),
> via Explorer B in [research.md](research.md))*

---

## 3 — "Questions this manual now answers"

Seeded from the GO rows of the matrix (witnessed types). Latent rows are offered as a separate,
clearly-labeled "and can also answer" set so the manual never claims a user asked them.

**Answered (witnessed):**
- How do I compose a multi-capability pipeline like `craft → dispatch-spec → whisper`? *(T1)*
- How do I distill a large body of knowledge into an explainer? *(T2)*
- How do I inspect/expose the framework surface to work from it? *(T3, x-ray)*
- How do I execute work by spawning subagents instead of running inline? *(T4)*
- How do I validate or design a dispatch route before running it? *(T5)*
- How do I build a research strategy that mines my own prompts? *(T6)*
- How do I use the tools the way I already work? *(T7)*
- What is constitution-governance and why does it matter? *(T8)*
- How do I generate more questions of this kind by delegating? *(T9)*
- How do I retry/re-run a stalled attempt? *(T10)*

**Can also answer (latent, contract-backed, unwitnessed — FLAGGED):**
- refine vs invoke vs task-session — when each? *(L2)* — fold into edit (b).
- How do I see what just happened in a run I dispatched? *(L1, densest gap per C)*
- How do I make a run reflect on itself and improve next time? *(L8)*
- Which constitution applies to THIS artifact, and how do I compose one? *(L7)* — overlaps edit (d).
- How do I install this for another repo? *(L6)* / explain a pipeline to a non-Arcanum collaborator? *(L9)*

---

## Close

- **Dispatch:** `2026-06-16-arcanum-manual-question-types` · **exit_reason:** `resolved`
- **final_approver:** Vlachopulos, Ioannis (auditor) — **ACCEPT**, conditional on 6 revision obligations (seam rewrite mandatory); all satisfied in the manual edit.
- **agents_spawned:** total 8 — explorer ×3 (Ariely, Simon, Alexander), skeptic ×3 (Popper, Kuhn, Quine), writer ×1 (Ahrens), auditor ×1 (Vlachopulos); loops_used 1. Plus check-tension gate infrastructure (Brandenburg checker, Gödel reviewer; one reprove → revise → both PASS) — not counted as dispatch agents.
- **Skeptic verdicts:** non-vacuity PASS (0 demotions); precedent — all 4 edits novel/build-from-owned, no kills; definitional-soundness PASS + 1 mandatory rewrite (refine↔dispatch-spec seam) — applied.
- **Applied to:** [ARCANUM-MANUAL.md](../../ARCANUM-MANUAL.md) Part 4 (four tool sections) + "Questions this manual now answers". Latent (L*) types shipped only as a labelled "can also answer" set.
- **One-line answer to the goal:** ship 10 witnessed question-types via four manual edits (use-the-tools / refine / dispatch-spec / constitution-governance); the 9 latent types are offered separately and clearly labelled unwitnessed.
