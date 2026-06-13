# research.md — attack plan for implementing DISPATCH-COMPOSITION-MODEL

- **dispatch_id:** `2026-06-13-dispatch-composition-attack`
- **type:** research (LIVE) · **final_approver:** parent
- **anti_bias_global:** ship-the-ready-path optimism vs structural-cost skepticism
- **groups:** `phase1-probe` (explorer × skeptic), `phase2-probe` (explorer × auditor) → `synthesize`
- **discipline:** claim ≤ proof; every load-bearing claim cites a file the agent read. Tension is preserved, not collapsed.

This file is the **raw evidence** assembled verbatim-in-substance from the four investigate returns. `findings.md` synthesizes it; `discovery.md` decides how we attack.

---

## Group `phase1-probe` — observability wiring (§12)

### Agent A — explorer (angle: shippable-now optimism)

**Verified file map**

| Claim | File:Line |
|---|---|
| §7 three-level flat JSONL (L1 dispatch / L2 wave / L3 agent) joined by FK | `TO-VLAD/DISPATCH-COMPOSITION-MODEL.md:247-266` |
| Mandatory emit gate (`dispatch.started`+`dispatch.closed`) | `…:278-280` |
| §12.1 names the 3 missing pieces (hook surface, scaffold, envelope producer) | `…:417-426` |
| §12.5 exact wiring steps | `…:489-497` |
| `.codex/hooks.json` wires the 3 events to 3 scripts | `.codex/hooks.json:3-37` |
| user-prompt-submit opens `pending-envelope.json` under `runs/arcanum-hooks/<run_id>/` | `.codex/hooks/arcanum-user-prompt-submit.sh:125-199` |
| post-tool-use appends to `tool-events.jsonl` | `.codex/hooks/arcanum-post-tool-use.sh:25-32` |
| stop closes envelope, calls `observe-invocation.sh`, appends ledger | `.codex/hooks/arcanum-stop.sh:49-83` |
| `observe-invocation.sh` is a complete schema-validated, dedupe-guarded writer | `framework/observability/scripts/observe-invocation.sh:1-356` |
| `.arcanum/observability/` has `config.json` (v0.2.0) but **no `signals/` and no `reflection-state.json`** | disk |
| `.claude/settings.json` **does not exist** | Glob → none |

**The minimal shippable increment (3 deliverables, in order):**
1. **`.claude/settings.json` hooks block** (~25 lines) mirroring the 3 codex events. *The single highest-priority gap (`…:418-420`): without it, under Claude Code nothing fires.*
2. **`signals/` scaffold** — `observe-invocation.sh:58-63` does `mkdir -p`, so the ledger file auto-creates; `observability-setup` is the clean path, `mkdir+touch` the minimal one.
3. **Dispatch-envelope-producer script** (~60 lines): writes a conformant `invocation-envelope.json` (template at `framework/observability/templates/invocation-envelope.json:1-33`) carrying authored `goal`/`angle`/`anti_bias`/`exit_reason` as extensions, then calls `observe-invocation.sh --envelope <path>`. `started` → `execution.status:"partial"`; `closed` → `"completed"` with dedupe key `dispatch-<id>:close`.

**Reusability:** `observe-invocation.sh` reusable **as-is** (sole writer authority); `arcanum-stop.sh` / `arcanum-post-tool-use.sh` reusable **as-is** once Claude hooks exist; `arcanum-user-prompt-submit.sh` needs **extension** (exits `{}` for any non-`/command`/non-`$skill` prompt — `…:112-115`). L2/L3 rows are a *second* increment (need Craft Stage Receipt YAML); L1 alone closes the "32 ungoverned folders" gate. **No existing owner displaced** — producer feeds the existing writer.

### Agent B — skeptic (angle: harness-fragility) — DISSENTS from A on "ready"

Ranked failure modes, all cited:

1. **CRITICAL — hooks in the wrong config, NEVER fire under Claude.** `.codex/hooks.json:3-38` is Codex config; Claude reads `.claude/settings.json` (absent). Global `~/.claude/settings.json` has only domainspec's 3 PreToolUse hooks, no Arcanum hooks. → **Phase 1 produces zero rows today** — a *current total failure*, not just a gap.
2. **CRITICAL — `turn_id` absent in Claude payloads.** `arcanum-user-prompt-submit.sh:16-17,122-124` derive `run_id` from `.turn_id // "unknown-turn"`. Claude's `UserPromptSubmit` has `session_id`/`transcript_path`/`cwd`/`prompt` but **no `turn_id`**. → every turn → `run_id="arcanum-hook-unknown-turn"` → same `run_dir`; turns overwrite each other's `pending-envelope.json`; dedupe_key identical every turn (`observe-invocation.sh:151,221`) → turn 2+ skipped as duplicates.
3. **HIGH — `last_assistant_message` absent in Claude `Stop` payload.** `arcanum-stop.sh:28,37-41,43-47`: completion is set only if `last_message` non-empty → with it empty, **every dispatch logs `partial`** → reflection counter (`observe-invocation.sh:314`, threshold 3 at `config.json:12`) fires a false-positive storm.
4. **HIGH — natural-language prompts never produce an envelope** (`arcanum-user-prompt-submit.sh:70-115`); the §12.3 producer **does not exist on disk** (no template at the named path, no script calling `observe-invocation.sh` with authored fields). `register-dispatch` writes only to `subagents-dispatch.yaml`, never calls `observe-invocation.sh` → zero cross-ledger wiring exists.
5. **MEDIUM — skill detection covers 26 of 46 skills** (`arcanum-user-prompt-submit.sh:12` reads only `.agents/skills`, not `.claude/skills`); `dispatch-spec` itself is invisible.
6. **MEDIUM — counter increments not idempotent** against a producer that re-submits without a stable `run_id` (`observe-invocation.sh:138-151,311-322`).
7. **LOW — `date +%s%3N` on Git Bash/Windows** (`observe-invocation.sh:70` + arithmetic at 152,206,222,327,331,335) may emit literal `%3N` → arithmetic error under `set -euo pipefail` → no row.

**Minimum proof before "done" (single green Claude-Code session):** (1) hook fires → `pending-envelope.json` appears; (2) two turns → two distinct `run_id`s (needs a Claude-native run_id, not `turn_id`); (3) `execution.status:"completed"` lands (needs completion derived from a present payload field); (4) a natural-language dispatch yields a row traceable to `subagents-dispatch.yaml` (needs the producer); (5) dedupe holds across a session; (6) `reflection-state.json` created + counter incremented. **None met today.**

> **Tension A×B (recorded):** A's "minimal path" is correct about *what to build* but assumes the codex `.sh` hooks port cleanly. B shows three of them are **Codex-payload-coupled** (`turn_id`, `last_assistant_message`) and will misbehave under Claude even once registered. Resolution belongs in findings: the "minimal increment" must include a **Claude-native run_id + completion derivation**, not just a settings.json copy.

---

## Group `phase2-probe` — dispatch-spec schema (Wave band + strategy typing)

### Agent C — explorer (angle: fits-the-spec-now)

**Current spec (dispatch-spec/SKILL.md):** Rule 1 requires `dispatch_id`/`intent`/`mode`/`steps`/`gates`; `steps[]` is flat (no band between dispatch and step); Rule 3 = per-step `pattern`; Rule 4 = non-first steps name a typed input source (`frame`/`handle`/`decision`/`ledger`/`human_answer`/`external_context`). No `waves[]`, no `wave_id`.

1. **Wave band** attaches as a `waves[]` grouping wrapping `steps[]`, each wave carrying `wave_id`, `lane`, `intent`, and the typed edges. Steps stay validated by Rules 3–7; the band groups them. Extends Rule 1 (add `waves`, optional until DAG decision); Rules 23–25 already carry `role_id` per agent — add `wave_id` FK for L2 logging without touching lifecycle logic. (`…SKILL.md:73-78`; model §1,§7,§8.)
2. **Strategy-as-(role-set,grader)**: add `strategy_ref` to the existing `subagent_strategy` block (which already has `roles[]`/`parallelism`/`join_policy`/`receipt_requirements`, Rules 21–25, lines 108–120). `strategy_ref: research|review|plan|experiment` points to a reusable definition (e.g. `formulae/dispatch-spec/strategies/research.yml`) anchored to domainspec `research-constitution.md` R4–R8. Additive; absent `strategy_ref` → nothing breaks.
3. **2a vs 2b split** (partition criterion = does it need typed-DAG / reopen R30):

| Sub-change | Phase | R30 dep |
|---|---|---|
| `waves[]` grouping (label + L2 obs) | 2a | none |
| `strategy_ref` on subagent_strategy | 2a | none |
| `loop_cap` + verdict on waves (cycle is wave-level) | 2a | none |
| L1/L2/L3 observability rows | 2a | none |
| `verdict` vocab `pass\|flag\|block` | 2a | none |
| `pattern` enum cleanup | 2a | none |
| typed `consumes/reviews/reopens` between steps | 2b | **R30 blocks** |
| non-linear fan-in synthesis | 2b | **R30 blocks** |
| `dispatch_kind=meta` nesting | 2b | **R30 blocks** |

4. **mode-conflation cleanup** (Rule 3 enum `route|sequential|fanout|dialectic|tournament|distill|xray|decision|validation|toy_game|synthesis|handoff`): move `distill/synthesis/validation/decision` → `subagent_strategy.roles[]`; move `xray/toy_game` → technique-overlay (Rule 12/14); `route/sequential/handoff` → Connection layer (2b, entangled with edges); keep `fanout/dialectic/tournament` migrating to the Layer/Wave. **Minimum safe 2a cleanup:** drop the 4 function-words from `pattern`, require them in `roles[]` (tightening Rule 21), move the 2 overlays to Rule 12.

### Agent D — auditor (angle: structural-cost) — DISSENTS from C on "no R30 decision needed"

1. **R30 verbatim** (`domainspec/vault/constitution/domainspec-subagents-strategy-constitution.md:501`): *"Composition is linear: layer N runs after layer N−1. There is no DAG and no `depends_on:` field on agents. The role-ordering invariant … inherited from R25 …"* It protects **(a)** total order, **(b)** no `depends_on` (positional dependency), **(c)** role-ordering invariant. **(c) does NOT depend on (a).**
2. **claim≤proof correction:** R30 cites `P-SS-9 (lifecycle is linear)`, but P-SS-9 text (`premises.md:203-225`) is titled *"No Dispatch Without a Confirmed Strategy"* — a propose→confirm→dispatch→research→findings→discovery **authoring** lifecycle, **silent on execution topology**. "Lifecycle is linear" is an **interpretive bridge, not premise text.** P-SS-9 needs *authoring*-order linear, not *execution*-order.
3. **CRITICAL — the blast has already detonated.** Repo-root `subagents-strategy-constitution-proposal.md` is **v0.5.2-proposal** (`:8`), `replaces …@v0.3.0` (`:10`), and **already adopted dependency-scheduled DAG**: *"groups … scheduled by dependency: a group is READY when every group with a `sequential` or `zig-zag` edge into it has produced what it must respond to; all READY groups launch concurrently"* (`:61-63`), typed `{from,to,type,loop_cap?}` with `sequential|zig-zag|feedback` (`:293-320`), `feedback` = bounded back-edge (`:316-320`) — structurally the model's `consumes`/`reviews`/`reopens`. **OQ-mixed-dag-schema is de facto reopened in domainspec's own newer draft**; v0.3.0 R30 closure is **stale, not live law.** But the proposal is `status: draft` (`:7`) — **not ratified.**
4. **Blast radius if ratified:** voids/rewrites R30; dissolves `pipeline`-as-mode (R19, `:298-309`); adds `connections[]` to R25 schema; requires P-SS-9 discharge (draft affirms P-SS-9 but **carries it open** `:557-561`: *"Groups + connections describe data-flow topology; the lifecycle stays linear … Discharge requires a P-SS-9 revision separating lifecycle-order from topology"* — *"an honest dependency, not a discharge"* `:615`); re-grounds role-ordering invariant (c) as edge-direction.
5. **2a decouplable from 2b? YES, with one caveat.** Wave band is a grouping layer (model §1, marked *draft / not yet a field*) — no non-linear edges required. Strategy-typing is orthogonal to topology (`research` grader real on disk under the *current linear* regime). The v0.5.2 draft proves the converse independence: it adopted the DAG **without** naming Wave or strategy-typing (the two things model §8 says are missing) → two halves moved separately → the seam is real. **Caveat:** Wave's *governance teeth* — `reviews`/`reopens` review-wave semantics (model §5) — partly need 2b; 2a lands as **structure-only** (bands + strategy typing), under-delivering the review-loop story until 2b.
6. **Vlad-reserved cross-repo decisions (NOT ours):** (i) ratifying/reopening R30·OQ-mixed-dag-schema (TO-VLAD8 `:81`, `:239`; model §11 "Killed: R30-linearity as settled"); (ii) the single-canonical-spec collapse (TO-VLAD8 `:266-276`); (iii) the P-SS-9 discharge (premise-layer revision); (iv) `loop_cap` default value. **What IS ours (safe):** Wave band as additive field, strategy-typing, the §12 logging wiring. **Caution flag for the optimist:** §12 wiring is *"integration plan, not built … never exercised"* (model §12.6) — "fits now" ≠ "works now".

> **Tension C×D (recorded):** C is right that Wave + strategy-typing are additive (2a) and need no R30 decision. D sharpens it two ways: (1) the R30 decision is **already half-made** in domainspec's unratified v0.5.2 draft — so "reopen R30" reframes to "**ratify the v0.5.2 draft**"; (2) 2a without 2b is **structure-only** — the review-loop governance that motivates Wave waits on the DAG. Both survive; neither is killed.

---

## Cross-cutting evidence (both groups)

- The §12 wiring and the Phase-2 schema are **independent work-streams** — Phase 1 touches `.claude/`+`framework/observability/`+`formulae/`; Phase 2a touches `dispatch-spec/SKILL.md`+a strategies file. Neither blocks the other.
- The single biggest reframing from this dispatch: **domainspec v0.5.2-proposal already contains the typed-DAG** (Agent D §3). The "Vlad decision" is now *promote-the-draft-to-canonical*, not *invent-the-DAG*.
- The single biggest correction to the optimist path: **the codex `.sh` hooks are payload-coupled to Codex** (Agent B §2–3). A settings.json copy is necessary but not sufficient.
