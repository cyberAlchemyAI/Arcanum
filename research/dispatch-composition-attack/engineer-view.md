---
tags: [dispatch-composition, observability, dispatch-spec, subagent-governance, engineer-view]
node_type: discovery
is_session: false
layer: [architecture, application]
nature: [explanatory, technical]
status: exploratory
governance_status: project-local-overlay
veracidade: high
convicção: high
version: 0.1.0
last_updated: 2026-06-13
created_by: victorboscaro@gmail.com
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Task
---

# Engineer View — verdicts, schemas, and mechanics beneath the dispatch-composition attack

## 1. What this view owns + harvested stance list

### Objective

Resolve every stance the system-view names-but-does-not-decide into exactly one owning row carrying a verdict, a status, and an authority verified on disk. This view OWNS the verdicts; it re-narrates no shape (point up to `system-view.md`) and redefines no term (point to `ontology-view.md`, not yet authored — terms are used, never defined, here).

This view decides; it tells no story and defines no word.

### What this view owns vs. points elsewhere

- **Owns:** the decision inventory (every verdict, keyed `decision:#<id>`), the load-bearing schemas/contracts, and the runtime mechanics naming which gate enforces which verdict and where enforcement is ABSENT.
- **Points up (shape):** the two-halves architecture, the given-vs-optimized layering, the fence — all `system-view.md`. No re-narration.
- **Points down (terms):** "dispatch", "wave/band", "ledger", "envelope/record", "strategy", "grader", "verdict vocabulary" — `ontology-view.md` (not yet authored; cited as forward reference).

### Harvested stance list (Step 1 output — `stance:<slug>`, exactly seven)

| # | `stance:<slug>` | Named at (system-view) |
|---|---|---|
| 1 | `stance:producer-vs-port` | §2 Surface, §3 Layer |
| 2 | `stance:observability-setup-vs-minimal-scaffold` | §3 Layer |
| 3 | `stance:claude-native-existence-vs-codex-hook-reuse` | §4 Layer |
| 4 | `stance:skill-detection-coupled-vs-envelope-driven` | §4 Layer |
| 5 | `stance:wave-band-additive-vs-required` | §5 Layer |
| 6 | `stance:strategy-ref-file-vs-inline` | §5 Layer |
| 7 | `stance:ship-2a-structure-only-vs-wait-for-vlad` | §7 Given-vs-optimized |

Bijection target: 7 stances → 7 rows, one each. Confirmed below (no orphan, no duplicate).

### Central value claim (sets CRITICAL marking)

The thesis: *a subagent dispatch under Claude Code lands a matched `dispatch.started`+`dispatch.closed` pair in the one existing central ledger, and the route spec gains a band and a named strategy — without any cross-repo call.* Any OPEN row whose unresolved state would make that first matched pair unproducible, or would force a cross-repo decision into scope, is CRITICAL.

## 2–3. Dispatch-folder artifacts

**Skip predicate applied:** `single + N=1 + explorer` — the DEFAULT single-author path (engineer-view SKILL §Dispatch). No multi-agent machinery dispatched; no `agents/` folder materialized under `research/dispatch-composition-attack/<view_slug>/`. The skip drops the dispatch, NOT the skeptic FUNCTION: the author ran the skeptic/authority-strike pass inline before Step 7 — every cited authority opened on disk and checked to actually support its verdict; unverifiable authorities would be struck and their rows downgraded to OPEN. Result of that pass: **zero struck authorities, zero downgrades** (every RESOLVED-candidate either held its on-disk gate or was correctly never RESOLVED to begin with).

`exit_reason: success`.

## 4. Decision inventory (the differentiator)

<!-- decision row columns = # | decision-or-stance (back-ref system-view#stance:<slug>) | verdict | status | authority -->

| # | Decision-or-stance | Verdict | Status | Authority |
|---|---|---|---|---|
| D1 | Producer vs. port — system-view#stance:producer-vs-port | Feed the existing writer via a new envelope-producer Formula; do NOT port a second writer. Architecturally settled by the seed, but the producer **does not exist on disk** — designed-not-built. | OPEN | `framework/observability/scripts/observe-invocation.sh:1-90` is the present sole writer (`mkdir -p .../signals` at :58-63, `dedupe_key` at :151) — verified on disk; the §12.3 producer feeding it is ABSENT (no script calls `observe-invocation.sh --envelope` with authored fields; `register-dispatch` writes only `telemetry/agents/subagents-dispatch.yaml` — verified, no `signals/sigil-invocations.jsonl` exists). No running gate enforces "producer not port". |
| D2 | Canonical setup vs. minimal scaffold — system-view#stance:observability-setup-vs-minimal-scaffold | Materialize `signals/` + `reflection-state.json` via the canonical `observability-setup` Formula (manages `reflection-state.json`), not a bare `mkdir+touch`. Correctness-for-counters, not a hard blocker — the writer self-creates its dir. | OPEN | Canonical path `.claude/skills/observability-setup/SKILL.md:59` creates `.arcanum/observability/signals/` — verified; writer self-creates the same dir at `observe-invocation.sh:58-63` — verified. On disk now: `.arcanum/observability/` has `config.json` but **no `signals/` and no `reflection-state.json`** — verified (Glob). No gate enforces canonical-over-minimal — a recommendation, not a verdict. |
| D3 | Claude-native existence vs. Codex-hook reuse — system-view#stance:claude-native-existence-vs-codex-hook-reuse | Author a Claude-native `run_id` (`session_id` + turn counter, NOT `.turn_id`) and a completion signal read from a field present in Claude's `Stop` payload (NOT `last_assistant_message`). Reusing the Codex scripts as-is is necessary-but-not-sufficient. Blocks the first usable record. **Edit target: the canonical hook scripts in `framework/observability/scripts/`, NOT the generated `.codex/hooks/` copies.** | CRITICAL | Coupling verified IN THE CANONICAL SOURCE: `framework/observability/scripts/arcanum-hook-user-prompt-submit.sh:15-16` derives from `.turn_id // "unknown-turn"` and `.session_id // "codex-hook-session"` (absent under Claude → every turn collapses, dedupe key identical at `observe-invocation.sh:151`); `framework/observability/scripts/arcanum-hook-stop.sh:28` reads `.last_assistant_message` (absent → every dispatch `partial`). The `.codex/hooks/arcanum-*.sh` are generated copies (`post-tool-use`/`stop` byte-identical; `user-prompt-submit` an extended 208-line variant). `.claude/settings.json` ABSENT (Glob → none) so nothing fires today — root cause in M6. No running gate — design correction, blocks core thesis; see OQ-B, OQ-C. |
| D4 | Skill-detection coupled vs. envelope-driven — system-view#stance:skill-detection-coupled-vs-envelope-driven | Drive the producer from the dispatch envelope/record, NOT from prompt-side skill detection (which sees only `.agents/skills`, missing `.claude/skills` incl. `dispatch-spec` itself). | OPEN | `.codex/hooks/arcanum-user-prompt-submit.sh:12` reads only `$repo_root/.agents/skills` — verified (26 of 46 skills; `.claude/skills` invisible). The recommendation to decouple (discovery OQ-4) seeds this row; no gate enforces the choice. Recommendation, not verdict → OPEN. |
| D5 | Wave band additive vs. required — system-view#stance:wave-band-additive-vs-required | Attach `waves[]` as an OPTIONAL grouping wrapping `steps[]`; existing routes stay valid; steps keep being validated by Rules 3–7. Not a structural requirement. Designed-not-built. **Edit target: the canonical `formulae/dispatch-spec/` (schema + validator + fixtures), NOT the generated `.claude/skills/dispatch-spec/SKILL.md`.** | OPEN | Canonical route schema `formulae/dispatch-spec/dispatch.schema.json` (+ `.yml`) and `formulae/dispatch-spec/SKILL.md` Rule 1 have **no `waves`/`wave_id`** — verified (Grep: 0); the validator `formulae/dispatch-spec/scripts/validate-dispatch.py` and fixtures `formulae/dispatch-spec/development/fixtures/` carry no band. The `.claude/skills/dispatch-spec/SKILL.md` copy is generated (`canonical_source: formulae/dispatch-spec/SKILL.md`). No gate validates a band — no running gate in repo. |
| D6 | Strategy as referenced file vs. inline — system-view#stance:strategy-ref-file-vs-inline | Add `strategy_ref` on the existing `subagent_strategy` block pointing at a colocated reusable definition (`formulae/dispatch-spec/strategies/<name>.yml`); absent `strategy_ref` nothing breaks. Designed-not-built. **Edit target: canonical `formulae/dispatch-spec/` + the new strategies dir.** | OPEN | Canonical `formulae/dispatch-spec/SKILL.md` (`subagent_strategy` carries `roles`/`parallelism`/`join_policy`/`receipt_requirements`) and `dispatch.schema.json` have **no `strategy_ref`** — verified (Grep: 0). Target dir `formulae/dispatch-spec/strategies/` **does not exist** — verified (Glob → none). The `.claude/skills/` copy is generated. No gate; additive design only. |
| D7 | Ship 2a structure-only vs. wait for Vlad — system-view#stance:ship-2a-structure-only-vs-wait-for-vlad | The additive route-vocabulary half (D5+D6) is decouplable and shippable now AS STRUCTURE-ONLY, named out loud; its review-and-reopen governance teeth (`reviews`/`reopens`) partly need the fenced 2b half, which is a cross-repo (Vlad) decision NOT ours. | CRITICAL | The four Vlad-reserved items (ratify v0.5.2-proposal · single-canonical-spec collapse · P-SS-9 discharge · `loop_cap` default) are cited in `discovery.md:78` and `TO-VLAD/TO-VLAD8.md:265-276`; the v0.5.2 proposal claims were read in the sibling domainspec repo and are **not re-verifiable in this Arcanum tree** (local grep hits only TO-VLAD memos — `findings.md:57`). No running gate in repo — cross-repo decision; blocks the full review-loop value of the route half. See OQ-D. |

**Coverage check (Step 6 self-audit):** 7 stances → D1–D7, exactly one row each. Orphaned stances: 0. Duplicate verdicts: 0. Rows missing authority: 0. Struck authorities: 0 (no RESOLVED row rested on an unverifiable gate). RESOLVED count: 0 — every stance is either a live tension, designed-but-not-built, or cross-repo-gated, and **no on-disk gate enforces any stance verdict** (the producer, the band, the strategy_ref, and the Claude hook surface are all absent), so OPEN-by-default holds across the board. CRITICAL: D3 (blocks the first usable record) and D7 (cross-repo dependency / scope line). Under-marking and over-marking both checked: D1/D2/D4 are OPEN-not-CRITICAL because the thesis can still produce a first matched pair without resolving them (D1 names the architecture already; D2 is self-healed by the writer's `mkdir -p`; D4 is a producer-input choice, not a blocker on emission).

## 5. Schemas and contracts + Runtime mechanics

### Schemas and contracts

**C1 — Invocation-envelope record (realizes D1, D3).** Source: `framework/observability/templates/invocation-envelope.json:1-33` (verified on disk). Load-bearing fields and the closed enum that carries the verdict-bearing state:
- `execution.status` enum (verdict-bearing): `completed | partial | blocked | failed` (`:12`). The producer maps `started → "partial"`, `closed → "completed"` (discovery §3). D3's whole tension lives in *which payload field flips `partial`→`completed`* — today `arcanum-stop.sh:39` flips it only on a non-empty `last_assistant_message`, absent under Claude.
- `observer.reflection_trigger` enum: `none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap` (`:30`) — the false-positive storm of D3 is this firing on a stuck `partial`.
- Authored typed extensions the producer must add (not in the base template, named by discovery §3): `goal`/`angle`/`anti_bias`/`exit_reason`. Points back to D1 (producer owns these).

**C2 — Central ledger + dedupe contract (realizes D1, D2).** Source: `observe-invocation.sh` (verified). The ledger is `<observability_dir>/signals/sigil-invocations.jsonl` (`:64`); `dedupe_key = "$target_run_id:signal-observer:$observer_version"` (`:151`); `target_run_id` is derived from `.run_id // .id // .target_run_id` else a synthesized `invocation-<session>-<capability>-<timestamp>` (`:141-148`). The reflection thresholds live at `.arcanum/observability/config.json:8-13` (`related_workflow_gaps: 3`) — verified; this is the threshold D3's storm trips. Points back to D1 (this writer is fed, never replaced) and D2 (the `signals/` dir this contract needs is the one the scaffold materializes).

**C3 — dispatch-spec route schema (realizes D5, D6).** Source: `.claude/skills/dispatch-spec/SKILL.md` (verified). Current verdict-bearing shape:
- Rule 1 required keys: `dispatch_id`, `intent`, `mode`, `steps`, `gates` (`:72`) — `steps[]` is flat; no band field.
- Rule 3 `pattern` enum (`:74`): `route | sequential | fanout | dialectic | tournament | distill | xray | decision | validation | toy_game | synthesis | handoff` (the mode-conflation the discovery §5 cleanup targets — adjacent to but not one of the seven stances).
- `subagent_strategy` minimum fields (`:108-119`): `status`/`trigger`/`explanation`/`context`/`roles`/`parallelism`/`join_policy`/`authorization`/`permission_prompt`/`receipt_requirements`. D6's `strategy_ref` would be added here.
- Rules 21–25 lifecycle receipts (`:92-96`): `agent_id`/`role_id`/`spawn_status`/`join_status`/`close_status`/`residue`/`reroute`. D5's `wave_id` FK would attach here for L2 logging.
Points back to D5 (band attach point) and D6 (strategy_ref attach point). Confirmed ABSENT: `waves`/`wave_id`/`strategy_ref` (Grep: 0).

### Runtime mechanics — how the pieces join, and where enforcement is ABSENT

**M1 — The host-fire path (realizes D3; enforcement ABSENT).** Under Claude Code the hook surface is `.claude/settings.json`; it is **ABSENT** (Glob → none), so the three Arcanum hooks wired in `.codex/hooks.json:3-37` (verified: `UserPromptSubmit`→`arcanum-user-prompt-submit.sh`, `PostToolUse` matcher `Bash|apply_patch|Edit|Write`→`arcanum-post-tool-use.sh`, `Stop`→`arcanum-stop.sh`) never fire under Claude. **No gate enforces D3** — there is no validator that rejects a Codex-coupled `run_id`/completion derivation; the failure is silent (zero rows, or all-`partial`). This is the mechanic that makes D3 CRITICAL.

**M2 — The emit path (realizes D1; enforcement ABSENT).** Intended join: producer → `observe-invocation.sh --envelope <path>` → append one row to `signals/sigil-invocations.jsonl` → bump reflection counter. On disk the chain is broken at the head: the producer is ABSENT and `register-dispatch` writes only `telemetry/agents/subagents-dispatch.yaml` (verified — that YAML is the only dispatch record; it never calls `observe-invocation.sh`). The model's "mandatory-emit" gate is therefore documentation, not a running gate — **enforcement ABSENT**. This is why D1 is OPEN despite the architecture being settled.

**M3 — The scaffold self-heal (realizes D2).** `observe-invocation.sh:58-63` runs `mkdir -p .../signals .../by-sigil .../by-capability .../hooks`, so the ledger directory auto-creates on first real write — which is exactly why D2 is OPEN-correctness rather than CRITICAL-blocker. The canonical `observability-setup` adds the one thing the writer's `mkdir` does not: a managed `reflection-state.json` (`SKILL.md:59`+). No gate enforces canonical-over-minimal.

**M4 — The route-validation path (realizes D5, D6; enforcement ADDITIVE-ABSENT).** Routes are validated by `formulae/dispatch-spec/scripts/validate-dispatch.py` against Rules 1–25 (`SKILL.md:56-96`). Because `waves[]` and `strategy_ref` are absent from the schema, the validator neither requires nor rejects them — adding them additively (D5/D6 verdicts) leaves every existing route valid, but **no gate yet enforces** a band's shape or a strategy_ref's target resolving to `formulae/dispatch-spec/strategies/<name>.yml` (that dir is ABSENT). D5/D6 stay OPEN until both the schema field and its validator rule land.

**M5 — The cross-repo fence (realizes D7; enforcement is a SCOPE line, not a gate).** No mechanic in this tree can enforce D7's structure-only honesty: the review-wave semantics (`reviews`/`reopens`) that would give the band teeth depend on the typed-DAG fenced into Phase 2b, whose ratification lives in the sibling domainspec repo (`TO-VLAD8.md:265-276`). There is **no running gate in repo** — the fence is a documented scope decision, which is why D7 is CRITICAL/OPEN and can never be RESOLVED here.

**M6 — The generator gap (root cause of M1; realizes D3).** The Claude hook surface is absent not by oversight in a config file but because the generator never emits it. `tools/bootstrap_arcanum.sh:1772-1810` (verified) copies `framework/observability/scripts/arcanum-hook-{user-prompt-submit,post-tool-use,stop}.sh` into `.codex/hooks/` and `write_text_file`s a `.codex/hooks.json` pointing at `.codex/hooks/...` — it emits **only the Codex surface**; the `claude_root` branch (`:1168`) writes `CLAUDE.md` + skills but **no `.claude/settings.json` hooks block**. So D3's fix is two-part and both parts are canonical-source edits: (a) patch the Codex-coupling in `framework/observability/scripts/arcanum-hook-*.sh` (Claude-native `run_id` + completion), and (b) extend `bootstrap_arcanum.sh`'s hook-emission step to also write a Claude `settings.json` hooks block. A hand-written `.claude/settings.json` would be orphaned outside this generator — **enforcement of the Claude surface is GENERATOR-ABSENT**, not config-absent. Points back to D3.

**Generated-vs-canonical note (spans D3, D5, D6).** Every surface this view's mechanics touch has a canonical source and a generated copy carrying `mutation_policy: regenerate-from-canonical-source`: `.claude/skills/dispatch-spec/SKILL.md` ← `formulae/dispatch-spec/SKILL.md`; `.codex/hooks/*` ← `framework/observability/scripts/arcanum-hook-*.sh`; `.claude/settings.json` ← (would be) `bootstrap_arcanum.sh`. The decision-inventory edit targets above name the canonical source; the discovery's §7 carries the full canonical→generated map.

## 7. Open questions + Residue ledger

### Open questions (the OPEN/CRITICAL rows surfaced as the choices a stakeholder must weigh)

- **OQ-A — Producer existence (D1, OPEN).** The producer feeding `observe-invocation.sh` is designed but unbuilt. *Recommendation:* build the ~60-line envelope-producer Formula as the head of M2 before claiming any emit. *Owner:* observability implementer. Not a blocker on the *thesis* (architecture is settled) but a blocker on demonstration.
- **OQ-B — Claude completion signal (D3, CRITICAL → BLOCKER).** Which `Stop`-payload field reliably flips `execution.status` `partial`→`completed`, replacing the absent `last_assistant_message`? *Recommendation:* inspect a live Claude `Stop` payload; prefer a `transcript_path`-derived completion; treat as the gating proof for the existence half being "done" (`discovery.md:79`). *Owner:* observability implementer. **Flagged: blocker** — without it the first matched pair (the core thesis) cannot land as `completed`.
- **OQ-C — Host-native `run_id` stability (D3, CRITICAL → BLOCKER).** Is `session_id`+turn-counter stable and monotonic across a session (so two turns yield two distinct `run_id`s and dedupe holds)? *Recommendation:* confirm empirically over a two-turn session before building the producer on it (`discovery.md:80`). *Owner:* observability implementer. **Flagged: blocker** — shares D3's thesis-blocking status with OQ-B.
- **OQ-D — Cross-repo ratification (D7, CRITICAL → BLOCKER, unowned-in-tree).** The four Vlad-reserved items and the v0.5.2-proposal claims are relayed from the sibling repo, not re-verifiable here. *Recommendation:* confirm against the live domainspec tree before any ratify decision; ship the 2a structure-only half in the meantime, naming it structure-only out loud (`discovery.md:78,82`; `findings.md:80`). *Owner:* cross-repo decision-maker (Vlad). **Flagged: blocker with an unowned-in-tree resolver** — no gate in this repo can close it.
- **OQ-E — Scaffold canonicality (D2, OPEN).** Canonical `observability-setup` vs. bare `mkdir+touch`? *Recommendation:* use canonical to get a managed `reflection-state.json`; low stakes (writer self-heals the dir). *Owner:* observability implementer.
- **OQ-F — Producer skill-coupling (D4, OPEN).** Should the producer depend on skill detection at all, given it sees 26 of 46 skills? *Recommendation:* decouple — drive from the dispatch envelope, not the prompt route (`discovery.md:81`). *Owner:* observability implementer.
- **OQ-G — Band cardinality (D5, OPEN) and OQ-H — strategy_ref location (D6, OPEN).** Optional `waves[]` grouping and colocated `formulae/dispatch-spec/strategies/<name>.yml` are the recommended additive forms; both await the schema field + validator rule. *Owner:* dispatch-spec maintainer.

### Residue ledger

| # | State | Surviving residue | Citation |
|---|---|---|---|
| R-01 | open | "fits now ≠ works now — the §12 wiring is an integration plan, never exercised end to end; treat the existence half as designed-not-demonstrated" | `findings.md:100`; `research.md:89,99` |
| R-02 | open | "Tension A×B resolves *into a hardened spec*, not toward either voice — A is right about the target (producer→writer), B right that a settings.json copy is necessary-but-not-sufficient" (D1+D3) | `findings.md:71`; `research.md:54` |
| R-03 | open | "Tension C×D — both survive: 2a is decouplable and ships (C), AND lands structure-only, under-delivering the review-loop story until 2b (D)" (D7) | `findings.md:80`; `research.md:91` |
| R-04 | open | "cross-repo claims (v0.5.2-proposal, R30-verbatim, P-SS-9 text) relayed from the sibling domainspec tree, not re-verified in this Arcanum tree — local grep hits only TO-VLAD memos" | `findings.md:57`; `research.md:99` |
| R-05 | open | "the `pattern`-enum mode-conflation cleanup (drop 4 function-words, move 2 overlays) rides alongside D5/D6 but is not one of the seven stances — preserved as adjacent additive work, not a verdict here" | `research.md:80`; `discovery.md:70-72` |
| R-06 | closed | "producer-not-port adjudicated: a second writer would fight the existing dedupe/index/counter owner — porting domainspec's appender killed" (D1) | `findings.md:99`; `research.md:38` |
| R-07 | closed | "L2 (wave) and L3 (agent) receipt rows adjudicated out of scope for this increment — they need the Craft Stage Receipt YAML, a later increment" | `discovery.md:36`; `findings.md:30` |

Open residue (R-01…R-05) is preserved, never demoted. Closed residue (R-06, R-07) records adjudicated decisions.

## 8. Cross-reference map + overlay status

**Cross-reference map (nothing decided twice):**
- **Verdicts owned here:** D1–D7 — the sole home of every stance verdict. The system-view's seven `[PROVISIONAL — row not yet authored]` pointers now resolve: `producer-vs-port`→D1, `observability-setup-vs-minimal-scaffold`→D2, `claude-native-existence-vs-codex-hook-reuse`→D3, `skill-detection-coupled-vs-envelope-driven`→D4, `wave-band-additive-vs-required`→D5, `strategy-ref-file-vs-inline`→D6, `ship-2a-structure-only-vs-wait-for-vlad`→D7.
- **Shape pointed up:** all narrative/layering/fence → `system-view.md` (§2–§7). Not re-narrated here.
- **Terms pointed down:** all term meanings → `ontology-view.md` (not yet authored). Used, never defined, here.
- **Schemas/contracts/mechanics** C1–C3, M1–M5 each point back to their owning D-row; each D-row points up to its `stance:<slug>`.

**Connections:**

| Edge | Target | Note |
|---|---|---|
| `derives-from` | `./discovery.md` | seed corpus and sole mutation trigger; reconciled against version 0.2.0 (added canonical edit targets per discovery §7; newer = STALE) |
| `complements` | `./system-view.md` | owns the shape; this view owns the verdicts it named-but-did-not-decide |
| `uses-terms-of` | `./ontology-view.md` | owns every term used here (not yet authored — forward reference) |
| `cites` | `./findings.md` | evidence for the preserved tensions and verdicts |
| `cites` | `./research.md` | raw four-agent evidence bundle |

**Overlay status:** `governance_status: project-local-overlay` — out of promotion until the owning amendment is filed; the artifact rides `node_type: discovery`. Step-8 `domainspec-emit-signals` epilogue SKIPPED — not in the domainspec repo. `exit_reason: success`.
