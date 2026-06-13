# findings.md — observability adaptation: what to reuse from each system

- **dispatch_id:** `2026-06-13-observability-adaptation-eval`
- **type:** research (LIVE) · **writer:** synthesize · **final_approver:** parent
- **inputs:** `research/observability-adaptation/research.md` (Agent A return, Agent B return, recorded A×B tension); confirmed against `TO-VLAD/DISPATCH-COMPOSITION-MODEL.md` §7, §12.
- **discipline:** claim ≤ proof. Every load-bearing claim cites a return line or a file. The A×B tension is preserved as a partition, not collapsed to one voice.

This synthesizes the two tensioned explorer returns into (1) a verified capability-by-capability reuse matrix across **both planes**, (2) the central two-planes finding, (3) an adaptation design sketch consistent with §12, and (4) open questions with recommendations.

---

## 0. The one-sentence result

A and B are not in conflict; they are right about **two different planes** of the same composite log — A about the **capability-telemetry plane** (`signals/sigil-invocations.jsonl`, written by `observe-invocation.sh`), B about the **dispatch-governance plane** (`subagents-dispatch.yaml`, written by `append-dispatch.cjs`). These are distinct data models for distinct purposes; the resolution (§12 fusion) is to keep both writers, let each plane be written by whoever *can* write it, and **join them by `dispatch_id` / `run_id`** — not to build one ledger that does both.

---

## 1. Verified reuse matrix

### 1a. Capability-telemetry plane (A's plane — `signals/sigil-invocations.jsonl`)

| Capability | Arcanum has (file:line) | domainspec has (file:line) | Verdict |
|---|---|---|---|
| Sole ledger writer (single append path) | `observe-invocation.sh:262` | — (its appender writes the *other* plane) | **reuse-Arcanum** |
| Envelope validation (14-field) | `observe-invocation.sh:105-136` | `append-dispatch.cjs` validateDispatch `:131-225` (governance schema, different) | **reuse-Arcanum** (telemetry); domainspec validator belongs to the governance plane |
| Legacy sigil/capability normalization | `observe-invocation.sh:157-201` | — | **reuse-Arcanum** |
| Two-tier dedupe (`hooks/dedupe.jsonl` + ledger `dedupe_key`) | `observe-invocation.sh:205-232` | idempotent-on-`dispatch_id`/`close_of` `append-dispatch.cjs:337-339,357-360` (governance-plane idempotency, not row dedupe) | **reuse-Arcanum** |
| Reference indexes (`by-capability/`, `by-sigil/`) | `observe-invocation.sh:269-294` | — | **reuse-Arcanum** |
| Atomic reflection counters | `observe-invocation.sh:296-333` (`reflection-state.json`) | — | **reuse-Arcanum** |
| Threshold-triggered reflection | `observe-invocation.sh:235-259` | — | **reuse-Arcanum** |
| Machine-parseable output contract | `observe-invocation.sh:344-356` | — | **reuse-Arcanum** |
| Observed-run open (L1 start) | `start-observed-run.sh:36-125`, `parent_run_id` FK `:44,:88` | — | **reuse-Arcanum** |
| Observed-run close (typed status) | `finish-observed-run.sh:37-91` (`completed\|partial\|blocked\|failed\|interrupted`) | close row `append-dispatch.cjs` `isClose` branch `:258-259,:385` (governance close, different status set) | **reuse-Arcanum** (telemetry close); governance close is a separate event on the other plane |
| Per-stage checkpoint (≈L3 skeleton) | `checkpoint-observed-run.sh:60-97` (phase/tools/files/decisions/validation/blockers) | — | **adapt-Arcanum** — ~60% of a Craft Stage Receipt; missing `result`/`artifact_path`/`handoff_note`/`briefing`/`angle`/`sources[]` (~30 lines jq) |
| Crash recovery (started-without-closed) | `recover-arcanum-observations.sh:45-70` | — | **reuse-Arcanum** |
| Index rebuild | `rebuild-observability-indexes.sh:49-106` | — | **reuse-Arcanum** |
| Store compaction | `compact-observability-store.sh:41-88` | — | **reuse-Arcanum** |
| Infra-row separation (keep hook ops out of capability telemetry) | `record-hook-operation.sh:118-133`; `observe:false` sentinel `hook-operation.json:16` | — | **reuse-Arcanum** |
| Hook-health reflection | `reflect-hook-health.sh:31-57` | — | **reuse-Arcanum** |
| Invocation-signal reflection (kind filter) | `reflect-invocation-signals.sh:1-199` (filters `--kind skill`) | — | **reuse-Arcanum** |
| Scaffold Formula | `observability-setup` Formula `:44-110` | — | **reuse-Arcanum** (must be *run* at root — see §3) |
| Envelope templates (L1 structure verbatim) | `observed-run-envelope.json:1-41` (`session_id`/`run_id`/`parent_run_id`/`opened`/`closed`); `invocation-envelope.json:1-33`; `hook-operation.json` | — | **reuse-Arcanum** |
| L2 wave-governance schema (lane/verdict/edges/n_reviewers/dissent) | NOT in template (A's read, research.md:22) | carried by the *governance* plane below | **build-new** (additive schema extension; validator at `observe-invocation.sh:105-128` accepts unknown fields, so non-breaking) |

### 1b. Dispatch-governance plane (B's plane — `subagents-dispatch.yaml`)

| Capability | Arcanum has (file:line) | domainspec has (file:line) | Verdict |
|---|---|---|---|
| Per-dispatch governance ledger (distinct data model) | — (`signals/sigil-invocations.jsonl` is per-*capability*, not per-*dispatch*; research.md:31-32) | `subagents-dispatch.yaml`; "the three coexist; do not conflate them" README `:21-24` | **adopt-domainspec** |
| Two-append discipline (spec row + close row) | — | `SKILL.md:1-12`; `isClose = rec.close_of != null` `:258-259`; both branches `fs.appendFileSync` `:352,:385`; never overwrite; `created`/`closed` stamped by appender `:39` (unforgeable at authoring) | **adopt-domainspec** |
| Append-only enforcement (PreToolUse) | `.arcanum/observability/hooks/` has only `.gitkeep` — nothing denies a ledger Edit/Write (research.md:46) | `enforce-append-only-dispatch.cjs` (101 lines): path-canonicalize+match `:44-46`, deny mutation `:80-87`, Bash read-only allowlist defaults-to-deny `:52-72`, no escape hatch `:12-16`, fail-open `:98` | **adopt-domainspec** |
| Agent-reminder nudge | — | `remind-register-dispatch.cjs` (27 lines), fires on `Agent`, emits `additionalContext` `:21-23`, writes nothing | **adopt-domainspec** |
| Workflow-deny (force governed path) | — | `block-workflow.cjs` (32 lines), `permissionDecision:"deny"` `:23` | **adopt-domainspec** |
| Schema-validate-or-reject (governance intent) | — | `append-dispatch.cjs` validateDispatch `:131-225` / validateClose `:227-253`; unknown/removed/legacy keys `:133-138`; anti_bias/angle conditionals `:185-199`; `anti_bias_global` `:201-204`; connection/loop_cap `:207-223` (exit 2) | **adopt-domainspec** |
| Corrupt-ledger refusal at next write | no analog for `subagents-dispatch.yaml` (research.md:48) | structure-only self-check exit 1 refusing corrupt ledger `append-dispatch.cjs:299-333` (grandfathers old rows) | **adopt-domainspec** |
| Model-authored intent (`goal`/`context`/`angle`/`anti_bias`/`initial_prompt`) | not hook-derivable; observed-run records *capability invocations*, not authored intent (research.md:45; §12.2) | `register-dispatch` skill authors the row; README `:83-84` (`anti_bias_global` example) | **adopt-domainspec** (model-invoked authoring — keep, do not auto-derive) |
| Per-user Claude installer | — (bootstrap installs no `~/.claude` hook surface; research.md:42) | `install.cjs` (143 lines): writes `~/.claude/hooks/` + `~/.claude/skills/register-dispatch/` + three `PreToolUse` entries `:100-133`; REPLACE-semantics, BOM-tolerant, non-destructive; "appender is harness-neutral; only the hook wiring is Claude-specific" `:28` | **investigate** — the install *mechanism* is Claude-specific and the real native gap (see §3, §4) |

**Confirmed install state (B):** all three hooks live in `~/.claude/hooks/` + wired in `~/.claude/settings.json:3-30`; `register-dispatch` in `~/.claude/skills/`. So Arcanum **already uses** this discipline today — but only by having run the domainspec `install.cjs` per-user; it is **not native to `bootstrap_arcanum.sh`** (research.md:42, 50).

---

## 2. Central synthesis — two planes, not one ledger

The single most important correction in this dispatch, owed to B and confirmed by §12.2, is that **A's plane and B's plane are different data models** and a max-reuse-of-Arcanum reading that treats the observed-run lifecycle as a substitute for the governance ledger is wrong on the merits:

- **Arcanum's `observe-invocation.sh` → `signals/sigil-invocations.jsonl`** is **per-capability telemetry**: `capability.id`/`kind`, execution status, derived behavioral signals (research.md:31). It answers *what ran and how it behaved*.
- **domainspec's `append-dispatch.cjs` → `subagents-dispatch.yaml`** is **per-dispatch governance**: who was dispatched, each agent's angle, the `anti_bias` tension, `goal`/`context`, `exit_reason`, `agents_spawned` (research.md:32). It answers *what we intended and whether the governance held* (did ≥2 reviewers run; was there dissent — §7 L2).

The README is explicit that **"the three coexist; do not conflate them"** (research.md:32), and §12.2 names exactly three planes cross-referenced by `dispatch_id`/`run_id`: authored dispatch-spec (model-invoked, *meaning*), derived behavioral signals (hook-first, *existence*), and per-stage receipts (§7 L3).

**Where A and B genuinely disagree — and how it resolves.** The live disagreement (research.md:56-60) is whether the observed-run lifecycle's `parent_run_id` + checkpoint structure *already covers* L1/L2/L3 (A) or is *a different contract entirely* (B):

- **A is right on the capability-telemetry plane.** The writer + observed-run lifecycle + dedupe/index/reflection/recovery is mature and reused **as-is**; building a second writer is precisely the move §12.1 forbids ("port the domainspec appender as Arcanum's writer is the wrong move — it would duplicate and fight an owner that already exists").
- **B is right on the dispatch-governance plane.** Two-append / append-only / model-authored discipline is a distinct data model Arcanum's scripts do **not** provide, and it is what makes a governance ledger *trustworthy* (stated policy ≠ mechanically enforced; research.md:46). It is globally installed but **not native to bootstrap**.
- **Resolution (a partition, not a winner):** the observed-run lifecycle covers the *telemetry* L1/L3 skeleton (`start`/`finish` ≈ L1 started/closed; `checkpoint` ≈ ~60% of an L3 Stage Receipt), but the *governance* fields — `lane`, typed `verdict pass|flag|block`, typed edges `consumes`/`reviews`/`reopens`, `n_reviewers`, `dissent_count`, and authored `intent`/`anti_bias` — are **exactly the half it does not carry** (research.md:22, 60). Both halves are needed, joined by `dispatch_id`/`run_id`. Neither "reuse" nor "adopt" alone is the answer.

B's four contests stand and refine, not overturn, A:
1. **Intent cannot be hook-derived** — `goal`/`angle`/`anti_bias` are authored design decisions, not observable tool-call properties (research.md:45; §12.2). → keeps model-invoked authoring on the governance plane.
2. **A ledger without enforcement is not trustworthy** — Arcanum's `hooks/` is `.gitkeep`-only (research.md:46). → adopt the enforcer.
3. **Arcanum's capability ledger doesn't exist yet** — `signals/` absent, `runs/` empty, `.codex/hooks` unproven under Claude (research.md:47; §12.1 calls the scaffold unrun and the pipeline never-exercised, §12.6). → the plane is *baseline-ready, not proven*.
4. **Corruption-at-next-write is domainspec-only** (research.md:48). → adopt the self-check.

None of these say "rebuild Arcanum's writer." They say "Arcanum's writer owns plane A; adopt domainspec's discipline for plane B; wire both under Claude."

---

## 3. Adaptation design sketch (consistent with §12)

The design is **producer-into-existing-writer on plane A, adopt-as-is on plane B, and one real native gap in bootstrap**.

**Plane A — feed the existing writer; do not port an appender.**
- Add an **envelope-producer Formula** (textbook Formula: stateless, deterministic, schema-validate-or-reject, idempotent — §12.3) that emits an `invocation-envelope.json` (per `framework/observability/templates/`) carrying authored `goal`/`angle`/`anti_bias` as a **typed extension**, then either writes `tmp/latest-invocation.json` and calls `observe-invocation.sh`, or drops a `pending-envelope.json` for the `Stop` hook to close (§12.3).
- `observe-invocation.sh` stays the **sole ledger-writing authority** — keeps append, dedupe, indexes, counters (§12.3). domainspec becomes "one more envelope producer alongside the Codex hooks" — the role `observed-invocation-loop` already assigns to "Codex hook or wrapper."
- **Run `observability-setup` at the repo root** to materialize `signals/` + `reflection-state.json` (currently `.gitkeep` placeholders) (§12.1 item 2, §12.5 item 2).

**Plane B — adopt the governance discipline as-is.** It is ~400 lines, zero-dep, and **already globally installed** (research.md:42, 50). The load-bearing choice — **two appends (spec at dispatch, close at termination), model-authored, append-only-enforced** (§12.4) — ports unchanged: the appender, the three hooks (reminder-nudge / workflow-deny / append-only enforcer), the `register-dispatch` skill, and the schema-validate-or-reject + corrupt-ledger self-check. Nothing here is rebuilt.

**The one real native gap — `bootstrap_arcanum.sh` grows a Claude hook-wiring step.** This is the crux both planes converge on. Today bootstrap installs **no `~/.claude` hook surface** (research.md:42), so a clean Arcanum install on a new machine gets neither the governance hooks nor a Claude observability surface; both depend on a manual `node install.cjs` or on Codex-only `.codex/hooks.json` that never fires under Claude (§12.1 item 1 — "a concrete reason the ledger is empty"). Bootstrap must wire **both hook families**:
- **Governance PreToolUse hooks** — the three domainspec `PreToolUse` entries (reminder on `Agent`, deny on `Workflow`, append-only enforcer on `Edit|Write|Bash|…`) into `.claude/settings.json` / `~/.claude` (§12.4, research.md:36-38, 40).
- **Observability surface** — a `.claude/settings.json` hooks block mirroring the three Codex events `UserPromptSubmit` (open envelope) / `PostToolUse` (append evidence) / `Stop` (close + call writer); all three exist in both harnesses, so this is "the one real harness gap" (§12.1 item 1, §12.5 item 1).

**Plus the schema extensions (build-new):**
- The **envelope-producer Formula** carrying authored `goal`/`angle`/`anti_bias` (§12.5 item 3).
- The **L2 wave-governance schema extension** — `lane`, typed `verdict`, typed edges, `n_reviewers`, `dissent_count` — additive because the L1 validator accepts unknown fields (research.md:24).
- The **L3 Stage-Receipt adaptation** to `checkpoint-observed-run.sh` — add `result`/`artifact_path`/`handoff_note`/`briefing`/`angle`/`sources[]` (~30 lines jq; research.md:22).

**Reconciliation principle (§12.5 item 4):** split by plane — **hook-first for *existence*** (envelope skeleton, tool events, run boundaries the hook can capture automatically) and **model-authored for *meaning*** (the intent a hook cannot derive). Preserve model-invoked authoring for the semantic fields; do not auto-derive intent.

---

## 4. Open questions and recommendations

1. **One installer or two?** Bootstrap currently installs nothing for Claude; domainspec's `install.cjs` installs the governance hooks per-user.
   - *Recommendation:* **one installer — fold the Claude hook-wiring into `bootstrap_arcanum.sh`** so a clean install gets both governance and observability surfaces with no manual `node install.cjs`. Two installers leaves the documented failure mode (empty ledger, manual step) (research.md:50, §12.1).

2. **Should bootstrap call domainspec's `install.cjs` or reimplement it?**
   - *Recommendation:* **call/vendor `install.cjs` for the governance hooks** (it is REPLACE-semantics, BOM-tolerant, non-destructive, harness-neutral at the appender, Claude-specific only at the wiring — `install.cjs:28`, research.md:40) and **add a sibling step that writes the observability `UserPromptSubmit`/`PostToolUse`/`Stop` block**. Reimplementing the governance installer risks drift from the live, proven `~/.claude` install state. Investigate whether one `settings.json` writer can own both hook families to avoid REPLACE-semantics fighting between two writers.

3. **L2/L3 schema ownership.** The L2 governance fields (lane/verdict/edges/n_reviewers/dissent) and the L3 Stage-Receipt fields cross both planes — telemetry envelope vs governance ledger.
   - *Recommendation:* **Arcanum owns the ledger contract + writer; the authored-semantics layer is a typed envelope extension; domainspec (governance) consumes** (§12.3 end-state, Arcanum-as-source-of-truth). L2 governance fields live on the dispatch-governance plane (`subagents-dispatch.yaml` via `register-dispatch`); the L3 receipt extends `checkpoint-observed-run.sh` on the telemetry plane. Join by `dispatch_id`/`run_id`. Do not let one schema try to own both planes.

4. **The Codex-coupling patch in framework hooks.** The writer is driven by `.codex/hooks.json`; under Claude nothing fires (§12.1 item 1). Reconciliation with `observed-invocation-loop` and the deprecated `.arcanum/runtimes/` adapter model is flagged as required (§12.6).
   - *Recommendation:* keep `observe-invocation.sh` harness-neutral (it already is — called by a hook, agnostic to which); add the Claude hook surface as a **peer** to the Codex hooks (both are "envelope producers"), and **cite-don't-rediscover** the `observed-invocation-loop` spec and the deprecated runtime-adapter model before this is promoted to its own TO-VLAD memo (§12.6).

5. **L2 additivity assumption.** A asserts the L1 validator accepts unknown fields (`observe-invocation.sh:105-128`), making the L2 extension non-breaking (research.md:24).
   - *Recommendation:* **investigate** — verify directly that unknown top-level fields survive validation and round-trip through dedupe/index before relying on additivity; it is load-bearing for "schema extension, not rewrite."

---

## 5. Summary

- **The single most important reuse decision:** keep **two planes, not one ledger** — reuse Arcanum's `observe-invocation.sh` as the *sole writer* of the capability-telemetry plane (do **not** port domainspec's appender — §12.1), and adopt domainspec's governance discipline **as-is** for the dispatch-governance plane (it is already globally installed). A is right on plane A, B is right on plane B; they join by `dispatch_id`/`run_id`.
- **The real native gap is not code, it is wiring:** `bootstrap_arcanum.sh` must grow a Claude hook-wiring step for **both** hook families — the governance `PreToolUse` hooks and the observability `UserPromptSubmit`/`PostToolUse`/`Stop` surface — plus the envelope-producer Formula and the additive L2/L3 schema extensions. Everything else carries.
- **What the next artifact should be:** an **implementation plan** that sequences (1) run `observability-setup` at root, (2) the bootstrap hook-wiring step (one installer, calling/vendoring `install.cjs` for governance + adding the observability block), (3) the envelope-producer Formula, (4) the L2 schema extension and L3 Stage-Receipt adaptation, with the §4 open questions resolved as gates before build.
