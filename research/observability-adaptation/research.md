# research.md — observability adaptation: what to reuse from each system

- **dispatch_id:** `2026-06-13-observability-adaptation-eval`
- **type:** research (LIVE) · **final_approver:** parent
- **anti_bias:** where the adaptation work mainly lands — max-reuse of Arcanum's existing observed-run surface (in-place) vs adopt domainspec's governance discipline (the missing half)
- **discipline:** claim ≤ proof; every load-bearing claim cites a file the agent read. Tension preserved, not collapsed.

This is the raw evidence from the two tensioned explorers. `findings.md` synthesizes it into the reuse matrix + adaptation design.

---

## Agent A — explorer (angle: Arcanum already has most of it; reuse in place)

**Reusable AS-IS (carry, do not rebuild):**
- **`observe-invocation.sh`** — sole ledger writer: 14-field envelope validation (`:105-136`), legacy sigil/capability normalization (`:157-201`), **two-tier dedupe** (`hooks/dedupe.jsonl` + central-ledger `dedupe_key`, `:205-232`), single append path (`:262`), dual reference indexes `by-capability/` + `by-sigil/` (`:269-294`), atomic reflection counters in `reflection-state.json` (`:296-333`), threshold-triggered reflection (`:235-259`), machine-parseable output contract (`:344-356`). §12.1 explicitly says do not replace.
- **Observed-run lifecycle:** `start-observed-run.sh` (`:36-125`, carries **`parent_run_id` FK** `:44,:88` → hierarchical nesting), `finish-observed-run.sh` (`:37-91`, `--status completed|partial|blocked|failed|interrupted`), `checkpoint-observed-run.sh` (`:60-97`, phase/tools/files/decisions/validation/blockers), `recover-arcanum-observations.sh` (`:45-70`, **crash recovery of started-without-closed**).
- **Index/store:** `rebuild-observability-indexes.sh` (`:49-106`), `compact-observability-store.sh` (`:41-88`).
- **Infra plane:** `record-hook-operation.sh` (`:118-133`, dual-mode dedupe; `observe:false` sentinel in `hook-operation.json:16` keeps infra rows out of capability telemetry), `reflect-hook-health.sh` (`:31-57`), `reflect-invocation-signals.sh` (`:1-199`, already filters `--kind skill`).
- **Scaffold:** `observability-setup` Formula (`:44-110`).
- **Templates:** `observed-run-envelope.json` (`:1-41`, has `session_id`/`run_id`/`parent_run_id` + `opened`/`closed` = the L1 started/closed structure verbatim); `invocation-envelope.json` (`:1-33`); `hook-operation.json`.

**A's L1/L2/L3 read:** L1 = `start`+`finish` with `--kind spell` (present, reusable; `exit_reason` maps to `--status`+`--notes` with a thin adapter). L2 = call with `parent_run_id`=dispatch, but the governance fields (`lane`, `n_reviewers`, `dissent_count`, typed `verdict pass|flag|block`, typed edges) are **NOT in the template** → schema extension. L3 = `checkpoint` is ~60% of a Craft Stage Receipt (missing `result`, `artifact_path`, `handoff_note`, `briefing`/`angle`/`sources[]`) → needs adaptation (~30 lines of jq fields).

**A's "genuinely missing" (only 3):** (1) Claude hook registration (`.claude/settings.json` block — config, not code); (2) the **envelope-producer Formula** (~80 lines, carries authored `goal`/`angle`/`anti_bias`, feeds the existing writer — the §12.3 plug point); (3) the **L2 wave-governance schema extension** (validator at `observe-invocation.sh:105-128` accepts unknown fields, so additive). A's bottom line: 5 items, 3 of them <30 lines; everything else carries as-is.

---

## Agent B — skeptic (angle: the missing half is domainspec's governance discipline) — DISSENTS

**B's core correction: A conflates two distinct ledgers / data models.**
- Arcanum's `observe-invocation.sh` writes **`signals/sigil-invocations.jsonl`** = per-**capability** telemetry (capability.id/kind, execution status).
- domainspec's `append-dispatch.cjs` writes **`telemetry/agents/subagents-dispatch.yaml`** = per-**dispatch** governance (who was dispatched, angle, anti_bias tension, goal/context, exit_reason, agents_spawned). README (`:21-24`): "the three coexist; do not conflate them." These are **distinct data models for distinct purposes** — the observed-run lifecycle is NOT a substitute for the governance ledger.

**What domainspec has that Arcanum lacks natively:**
- **Two-append discipline** — `SKILL.md:1-12`; `append-dispatch.cjs` branches on `isClose = rec.close_of != null` (`:258-259`), both branches `fs.appendFileSync` (`:352,:385`), never overwrite. `created`/`closed` stamped by appender (`:39`), uncforgeable at authoring.
- **Append-only enforcement hook** — `enforce-append-only-dispatch.cjs` (101 lines), PreToolUse on `Edit|MultiEdit|Write|NotebookEdit|Bash|PowerShell`; path-canonicalizes + matches the ledger (`:44-46`), denies direct mutation (`:80-87`), Bash read-only allowlist defaults-to-deny (`:52-72`), **no escape hatch** by design (`:12-16`), fail-open (`:98`).
- **Agent-reminder nudge** — `remind-register-dispatch.cjs` (27 lines), fires on every `Agent` call, emits `additionalContext` (`:21-23`), writes nothing (a hook can't author intent).
- **Workflow-deny** — `block-workflow.cjs` (32 lines), `permissionDecision:"deny"` (`:23`) forcing dispatch through the governed `Agent` path.
- **Schema-validate-or-reject + idempotency** — `append-dispatch.cjs`: strict incoming validation exit 2 (`validateDispatch :131-225`, `validateClose :227-253`; unknown/removed/legacy keys `:133-138`; P5 anti_bias/angle conditionals `:185-199`; `anti_bias_global` `:201-204`; connection/loop_cap rules `:207-223`); structure-only ledger self-check exit 1 refusing a corrupt ledger (`:299-333`); idempotent on `dispatch_id`/`close_of` (`:337-339,:357-360`).
- **Per-user Claude installer** — `install.cjs` (143 lines) writes `~/.claude/hooks/` + `~/.claude/skills/register-dispatch/` + the three `PreToolUse` entries in `~/.claude/settings.json` (`:100-133`); REPLACE-semantics, BOM-tolerant, non-destructive. `install.cjs:28`: "the appender is harness-neutral; only the hook wiring here is Claude-specific."

**Confirmed install state:** all three hooks live in `~/.claude/hooks/` + wired in `~/.claude/settings.json:3-30`; `register-dispatch` in `~/.claude/skills/`. So Arcanum **already uses** this discipline — but only by adopting the domainspec toolchain; it is **not native to `bootstrap_arcanum.sh`**, which installs no `~/.claude` hook surface.

**B's direct contest of max-reuse:**
1. **Intent cannot be hook-derived.** `goal`/`context`/`angle`/`anti_bias`/`initial_prompt` are authored, not observable tool-call properties; no hook reconstructs `"anti_bias_global": "ship-the-ready-path optimism vs structural-cost skepticism"` from a raw `Agent` call (README `:83-84`). The observed-run lifecycle records capability invocations, not authored dispatch intent.
2. **A ledger without append-only enforcement is not trustworthy.** Arcanum's `.arcanum/observability/hooks/` has only `.gitkeep`; nothing denies an Edit/Write to a ledger. domainspec's enforcer denies regardless of instruction context. Stated policy ≠ mechanically enforced.
3. **Arcanum's capability ledger doesn't even exist yet** — `signals/` absent; the `.codex/hooks` are Codex-scoped and unproven under Claude; `runs/` empty. The observed-run lifecycle is **unproven under Claude**.
4. **Corruption-at-next-write is domainspec-only** — `append-dispatch.cjs:299-333` refuses to append to a structurally corrupt ledger; Arcanum has no analog for `subagents-dispatch.yaml`.

**B's portability verdict:** the whole governance toolchain is ~400 lines, zero-dep, **already installed**; portable as-is EXCEPT `install.cjs` (Claude-specific) — the real gap is `bootstrap_arcanum.sh` growing a Claude hook-wiring step so a clean Arcanum install on a new machine gets the governance surface without a manual `node install.cjs`.

---

## The recorded tension (A × B)

Both are right about **different planes** — the disagreement is real but resolves into a *partition*, not a winner:

- **A is right on the CAPABILITY-TELEMETRY plane** (`signals/sigil-invocations.jsonl`): the writer + observed-run lifecycle + dedupe/index/reflection/recovery machinery is mature and reused as-is. Building a second writer is the move §12.1 forbids.
- **B is right on the DISPATCH-GOVERNANCE plane** (`subagents-dispatch.yaml`): the two-append/append-only/model-authored discipline is a distinct data model that Arcanum's scripts do NOT provide, and it is what makes a governance ledger trustworthy. It is already globally installed but not native to Arcanum's bootstrap.
- **The genuine open disagreement:** does the observed-run lifecycle's `parent_run_id` + checkpoint structure already cover L1/L2/L3 (A) or is it a different contract entirely (B)? Resolution: it covers the *telemetry* L1/L3 skeleton, but the *governance* fields (lane/verdict/edges/intent/anti_bias) are exactly the half it does not carry — so both halves are needed, joined by `dispatch_id`/`run_id` (the §12 fusion). Neither "reuse" nor "adopt" alone is the answer.
