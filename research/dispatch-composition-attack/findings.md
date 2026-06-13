# findings.md — synthesis: attacking DISPATCH-COMPOSITION-MODEL

- **dispatch_id:** `2026-06-13-dispatch-composition-attack` · **role:** synthesize
- **discipline:** claim <= proof. Every load-bearing finding cites the return/file it rests on. The two recorded tensions are preserved, not collapsed.
- **upstream:** four investigate returns assembled in `research/dispatch-composition-attack/research.md`; confirmed against `TO-VLAD/DISPATCH-COMPOSITION-MODEL.md` and `TO-VLAD/TO-VLAD8.md`.

---

## 1. The shape of the work

Two **independent** work-streams, no ordering between them (research.md:97):

- **Phase 1 — observability wiring (§12).** Touches `.claude/` + `framework/observability/` + `formulae/`. Make a Claude-Code dispatch emit L1 ledger rows.
- **Phase 2 — dispatch-spec schema.** Touches `dispatch-spec/SKILL.md` + a strategies file. Add the Wave band and strategy-as-typed-object. Splits into **2a** (additive, no cross-repo decision) and **2b** (typed-DAG, gated on a Vlad decision).

Neither blocks the other. What follows separates **READY** from **BLOCKED**, and preserves the two tensions.

---

## 2. READY to ship (and what it actually requires)

### 2.1 Phase 1 — observability wiring

The writer already exists and is reusable as-is: `framework/observability/scripts/observe-invocation.sh:1-356` is a complete schema-validated, dedupe-guarded ledger writer (research.md:29; model §12.1 at `DISPATCH-COMPOSITION-MODEL.md:413-416`). The correct move is a **producer feeding the existing writer**, NOT porting domainspec's appender (which would fight the existing dedupe/index/counter owner — model §12.1 at `:427-428`). Three deliverables, in order (research.md:33-38; model §12.5 at `:489-497`):

1. **`.claude/settings.json` hooks block** (~25 lines) mirroring the 3 Codex events (`UserPromptSubmit`/`PostToolUse`/`Stop`). **Locally confirmed: `.claude/settings.json` does not exist** (Glob -> none; research.md:31,44). This is the single highest-priority gap (model §12.1 at `:418-420`).
2. **`signals/` scaffold** — `observe-invocation.sh:58-63` does `mkdir -p`, so the ledger auto-creates; `observability-setup` is the clean path, `mkdir+touch` the minimal one (research.md:35).
3. **Dispatch-envelope-producer Formula** (~60 lines): writes a conformant `invocation-envelope.json` (template at `framework/observability/templates/invocation-envelope.json:1-33`) carrying authored `goal`/`angle`/`anti_bias`/`exit_reason` as a typed extension, then calls `observe-invocation.sh --envelope <path>`. `started` -> `status:"partial"`; `closed` -> `"completed"` with dedupe key `dispatch-<id>:close` (research.md:36).

Shipping L1 alone closes the "32 ungoverned folders" gate (research.md:38; model §7 mandatory-emit gate at `:278-281`). L2/L3 rows are a **second increment** — they need the Craft Stage Receipt YAML (model §7 L3 at `:261-266`) — and are out of scope for the minimal increment.

### 2.2 Phase 2a — dispatch-spec schema (additive, no cross-repo decision)

These extend the current spec without reopening anything (research.md:64-65, table 68-75; auditor concurs research.md:88):

- **Wave band** as a `waves[]` grouping wrapping `steps[]`, each wave carrying `wave_id`/`lane`/`intent` + typed edges; steps stay validated by Rules 3–7; `wave_id` FK added to Rules 23–25 for L2 logging (research.md:64). `dispatch-spec/SKILL.md` confirmed on disk at `.claude/skills/dispatch-spec/SKILL.md` and `formulae/dispatch-spec/SKILL.md`.
- **`strategy_ref`** on the existing `subagent_strategy` block (already has `roles[]`/`parallelism`/`join_policy`/`receipt_requirements`, Rules 21–25); absent `strategy_ref` -> nothing breaks (research.md:65). The `research` grader is real on disk under the current linear regime (research.md:88).
- Also 2a, R30-free: `loop_cap` + verdict on waves, L1/L2/L3 row schema, `verdict` vocab `pass|flag|block`, `pattern` enum cleanup (research.md table 70-75).
- **Mode-conflation cleanup (minimum safe slice):** drop the 4 function-words (`distill/synthesis/validation/decision`) from Rule 3 `pattern`, require them in `roles[]` (tightening Rule 21), move the 2 overlays (`xray/toy_game`) to Rule 12. `route/sequential/handoff` are deferred to 2b (entangled with the Connection/edge layer) (research.md:80).

---

## 3. BLOCKED on a Vlad-reserved cross-repo decision

Phase **2b** is fenced off. It is everything that needs the typed-DAG or reopens R30 (research.md table 76-78; auditor research.md:86-89):

- typed `consumes`/`reviews`/`reopens` edges between steps;
- non-linear fan-in synthesis;
- `dispatch_kind=meta` nesting.

The Vlad-reserved decisions (NOT ours — research.md:89; `TO-VLAD8.md:265-276`):
1. ratify/reopen **R30 · OQ-mixed-dag-schema** (linear-composition closure);
2. the **single-canonical-spec** collapse (domainspec onto Arcanum's dispatch-spec) (`TO-VLAD8.md:267-271`);
3. the **P-SS-9 discharge** (premise-layer revision separating lifecycle-order from topology);
4. the **`loop_cap` default** value.

**Cross-repo verification caveat (claim <= proof, honest):** R30's verbatim text and the `subagents-strategy-constitution-proposal.md` (v0.5.2) cited by Agent D live in the **sibling domainspec repo**, not in this Arcanum tree — a local grep for `zig-zag`/`dependency-scheduled`/`v0.5.2-proposal` hits only TO-VLAD memos and this dispatch's own files. Those claims are therefore **relayed from the investigate agents' reading of an external repo**, not re-verified on disk here. This is exactly why they are Vlad-reserved: they are a genuine cross-repo ownership call (`TO-VLAD8.md:239-241`).

---

## 4. The two preserved tensions

### Tension A×B — is Phase 1 "ready"? (explorer optimism × harness-fragility skepticism)

- **A (explorer):** the minimal 3-deliverable path is correct about *what to build*, and the codex `.sh` hooks are reusable as-is once a Claude hook surface exists (research.md:33-38).
- **B (skeptic) DISSENTS:** three of those hooks are **Codex-payload-coupled** and will misbehave under Claude even once registered (research.md:44-50). **Locally confirmed:**
  - `turn_id` is absent in Claude payloads; `arcanum-user-prompt-submit.sh:16` derives `run_id` from `.turn_id // "unknown-turn"` -> every Claude turn collapses to the same `run_dir`, overwriting `pending-envelope.json` and tripping identical dedupe keys (research.md:45). **Verified at `arcanum-user-prompt-submit.sh:16`.**
  - `last_assistant_message` is absent in Claude's `Stop` payload; `arcanum-stop.sh:28,39` sets `completed` only if `-n "$last_message"` -> **every dispatch logs `partial`**, firing a false-positive reflection storm (threshold 3) (research.md:46). **Verified at `arcanum-stop.sh:28,37-41`.**
  - the §12.3 producer **does not exist on disk**; `register-dispatch` writes only `subagents-dispatch.yaml`, never calling `observe-invocation.sh` (research.md:47).

**Resolution (does NOT collapse to one voice):** A is right about the *target architecture* (producer -> existing writer); B is right that a `settings.json` copy is **necessary but not sufficient**. The minimal increment MUST additionally include a **Claude-native `run_id` derivation** (from `session_id` + a turn counter, not `turn_id`) and a **completion derivation from a payload field that is actually present under Claude** (not `last_assistant_message`). With those two patches added, A's path ships; without them, "fits now" is not "works now" — **Phase 1 produces zero usable rows today** (research.md:52,54). Tension resolves *into a hardened spec*, not in favour of either side.

### Tension C×D — does Phase 2a need the R30 decision? (fits-the-spec-now × structural-cost)

- **C (explorer):** Wave band + strategy-typing are purely additive (2a) and need **no R30 decision** (research.md:64-66).
- **D (auditor) DISSENTS — sharpening, not refuting:** two corrections (research.md:86-91):
  1. The R30 decision is **already half-made**: per Agent D's reading, domainspec's own `subagents-strategy-constitution-proposal.md` is v0.5.2 and *already adopted* a dependency-scheduled typed DAG (`sequential|zig-zag|feedback`), structurally equal to the model's `consumes`/`reviews`/`reopens` — but it is `status: draft`, **not ratified**. So "reopen R30" reframes to "**ratify the existing draft**."
  2. 2a **without** 2b is **structure-only**: Wave's governance teeth — the `reviews`/`reopens` review-wave semantics (model §5) — partly need 2b. 2a lands as bands + strategy typing and **under-delivers the review-loop story** until 2b (research.md:88).

**Resolution (both survive, neither killed):** C is correct — 2a is decouplable and ships without a cross-repo decision; the v0.5.2 draft proves the converse independence (it adopted the DAG *without* naming Wave or strategy-typing, so the two halves move separately — research.md:88). D's caveat **stays open as scope-honesty**: 2a is worth shipping, but the team must name out loud that it is structure-only until 2b clears the Vlad gate.

---

## 5. Open questions

1. **Vlad gate (4 items):** ratify v0.5.2-proposal / single-canonical-spec collapse / P-SS-9 discharge / `loop_cap` default. All four block Phase 2b (research.md:89; `TO-VLAD8.md:265-276`).
2. **Claude `Stop` payload:** which field (if any) reliably signals completion under Claude Code, to replace `last_assistant_message`? Until answered, completion derivation is unspecified (research.md:46).
3. **Claude-native `run_id`:** confirm `session_id` + turn-counter is stable and monotonic across a session (research.md:45,52).
4. **Skill-detection coverage:** `arcanum-user-prompt-submit.sh:12` reads only `.agents/skills` (26 of 46 skills); `.claude/skills` is invisible, so `dispatch-spec` itself is undetected (research.md:48). Decide whether the L1 producer depends on skill detection at all.
5. **Cross-repo verification:** the v0.5.2 and R30-verbatim claims were not re-verifiable in this repo — confirm against the live domainspec tree before any ratify decision (§3 caveat above).

---

## 6. What this dispatch killed / corrected

- **Killed: "the Vlad decision is invent-the-DAG."** Corrected to **ratify-the-draft** — per Agent D, the typed-DAG already exists, unratified, in domainspec's own v0.5.2 proposal (research.md:86,98). The cross-repo call is promotion, not invention.
- **Killed: "settings.json copy = Phase 1 done."** Corrected — the codex `.sh` hooks are **payload-coupled to Codex** (`turn_id`, `last_assistant_message` absent under Claude). A copy is necessary but not sufficient (research.md:99; verified at `arcanum-user-prompt-submit.sh:16`, `arcanum-stop.sh:28,39`).
- **Corrected: R30 over-attributing to P-SS-9.** Per Agent D, R30 cites P-SS-9 ("lifecycle is linear"), but P-SS-9's actual text is *"No Dispatch Without a Confirmed Strategy"* — an **authoring** lifecycle, silent on execution topology. "Lifecycle is linear" is an **interpretive bridge, not premise text**; the role-ordering invariant (c) does not depend on total-order (a) (research.md:84-85). (Cross-repo; see §3 caveat.)
- **Killed: "port domainspec's appender as Arcanum's writer."** It would duplicate and fight an owner that already exists (model §12.1 at `:427-428`).
- **Named: "fits now" != "works now."** §12 wiring is an *integration plan, not built — never exercised* (model §12.6 at `:501-502`; research.md:89).
