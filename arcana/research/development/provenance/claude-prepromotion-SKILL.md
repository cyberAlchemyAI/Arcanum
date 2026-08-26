---
name: research
description: >
  Subagent dispatch for synthesis, adversarial check, multi-perspective audit, or
  precedent sweep — routed here from domainspec-subagents-strategy as the LIVE type
  skill for `dispatch_type: research`. Defines research-type judgment only: roles as
  epistemic functions, skeptic gates, the canonical shape, tension design, and the
  findings verdict matrix. Trivial single lookups stay inline and never reach this skill.
---

# research — type skill for `dispatch_type: research`

**Purpose (read first).** Research is **not** novelty-hunting. Its job is to find what **already
exists and can be used** — owned, citable results deployable as building material. A
`build-from-owned` finding is a **first-class success**, not a kill; `novel-attempt`
(precedent-clean) is one outcome among several, not the goal. (Normative orientation — what we
value, not a measured frequency.) Finding an owner is a *win*: owned kills a novelty *claim*,
never a *use*. The only failures are `no-witness` and `tautological`.

This is the **LIVE type skill** for `dispatch_type: research` — one of the LIVE types under
constitution v0.6.0 (another is `dispatch_type: review` — `.claude/skills/review/SKILL.md`,
populated 2026-06-12). Division of law:

- **When/whether + universal law** (triggers, human gate, anti-bias principle, lifecycle,
  `final_approver`, `exit_reason` vocabulary) — the router,
  `.claude/skills/domainspec-subagents-strategy/SKILL.md`. Route back there; nothing here
  overrides it.
- **Record/sheet mechanics** (the two appends, the appender, validation) —
  `register-dispatch` (`.claude/skills/register-dispatch/SKILL.md`).
- **Field definitions** — inline in `register-dispatch` (read there); constitution §5
  (`internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md`)
  is upstream authority only, not a routine read. This skill defines no field; it says which
  **values** a good research dispatch puts in them.

## Roles as epistemic functions

Each role guards a distinct failure mode; no agent guards two.

| agent `role` | guards against | model guidance |
|---|---|---|
| `explorer` | monoculture — generation under **one tensioned angle** each | lighter — sweeps are mechanical |
| `skeptic` | folklore / vacuity — attacks **one named gate** each | heavier — adversarial work is hard |
| `writer` | "great research, no record" — the synthesizer, **conventionally a single writer (the §6 skeleton's `n: 1`)** | heavier for heavy synthesis |
| `auditor` | "passed because nothing was checked" — meta-evaluates, **placed by its incoming edge, downstream of the reviewers**, owns the verdict matrix | mid — checking, not generating |

A group's function is read off its agents' roles, its workflow position off its `connections`.

The model column is **guidance, not law**: `model` is chosen per agent by task difficulty
(constitution §5) and the human validates it at the confirm gate.

There is no `evaluator` role — criteria-scoring is a `skeptic` with a stated gate.

## Skeptic gates

One gate per skeptic, never two:

- **precedent** (ownership attribution — formerly `precedent-kill`) — is this already owned?
  Find the owner, not just "something similar". **Finding an owner is NOT a kill** — research
  exists to find what *already exists and can be used*, not only what is new. A found owner is a
  *positive* result: it *labels* the candidate `build-from-owned` (owner exists, repo does not
  yet deploy it — cite honestly and build) or `already-deployed`; an empty search certifies
  `precedent-clean` → `novel-attempt`. This gate never emits a terminal KILL.
- **non-vacuity** — build the smallest concrete witness by hand, or force a closed negative.
- **definitional-soundness** — does it collapse to something already named, re-skinned?

A skeptic group is tensioned by construction when its gates differ; explorers need
explicit axis spread (below). The terminal KILLs come only from `non-vacuity` (no-witness) and
`definitional-soundness` (tautological) — never from `precedent`.

## Canonical shape on the v0.6.0 chassis

```
explorers (a group of `explorer`s, n 2–4, pairwise tensioned)
   │ sequential
synthesizer (1 `writer`) ◀──zig-zag──▶ reviewers (`skeptic`s;
   ▲                          │         robot_talks when the question
   └┄┄┄┄ feedback (conditional) ┄┘       needs confrontation, not collection)
```

The feedback back-edge is instantiated only when there is a reviewer/auditor group AND
material may be missing (Principle 6) — never by default. The older research pattern "writer drafts
candidates before skeptics attack them" **is** this synthesizer-midfield: same flow,
chassis names. The `auditor` sits in an optional group (its single agent's role is
`auditor`) placed by its incoming edge, downstream of the reviewers — which also makes it
the natural **dedicated `final_approver`** (Principle 12:
sole member, no other work, never in a working group).

**Early stop:** a confirmed kill — no candidate survives its collapse-test (no-witness or
tautological) — ends the dispatch early: bank the typed negative, then CLOSE `exit_reason:
resolved` (a confirmed-kill early-stop is a successful close, not an error). **Being OWNED is
NOT a confirmed kill and does not early-stop** — a found owner relabels the candidate
`build-from-owned` and the dispatch continues; the lone exception is owned **and already
deployed**, recorded as `already-deployed` provenance (still not a negative).
Approval follows P12, it does not mint new semantics: if the dispatch declared a dedicated
approver group (its single agent's role is `auditor`) and the early stop skips that group,
approval falls back to `parent` (P12's group-never-runs fallback); if `final_approver` is `parent`, `parent`
accepts directly. Either way the dispatch closes `resolved` once the negative is accepted.

## How to run

Spawn each group's agents with the Agent tool — ALL agents of a group in ONE message, so
they run in parallel. Each agent's `initial_prompt` is its launch prompt. Groups are
scheduled **by dependency** (constitution P4, amended 2026-06-12): a group is READY when
every group with a `sequential`/`zig-zag` edge into it has produced what it must respond
to (zig-zag counts only in its `from`→`to` direction — the `from` endpoint opens the
exchange); launch all READY groups concurrently (independent chains run side by side);
`feedback` edges never count as dependencies; a sheet with no connections declares its
groups independent. Declared order is narration tiebreak only.

## Tension design (Principle 5, research-specific)

Classify every angle along the four axes — **methodology** (empirical / formal /
adversarial / historical / computational), **source-corpus**, **attack-vector** (the
skeptic gate), **temporal-prior** (modern-only / historical-lineage / mixed).

Rules from `vault/discovery/anti-bias-vector-composition/validator-check.md` — codified
since 2026-06-12 as the binding four-test PASS/REJECT decision rule in constitution
Principle 5 (axis vocabulary / clone / spread / evidence; the axis vocabulary is closed
to the four axes above or a declared composite):

- **Reject before proposing:** all angles in a group share the same core noun phrase; all
  explorers share one methodology or one source corpus; all skeptics share one gate →
  fix the sheet before it reaches the human gate.
- **Green-light:** for every explorer pair you can write the sentence "a_i runs [X], a_j
  runs [Y] on the [axis] axis; a bias in a_i would be exposed by a_j" — and at least two
  distinct axes appear across the group.

## Outputs (Principle 9 applied)

- **n ≥ 2:** `<working_folder>/research.md` (collected returns, verbatim) +
  `<working_folder>/findings.md` (cited synthesis — every load-bearing claim cites the
  collected return it rests on; the `final_approver` checks this).
- **n = 1:** `<working_folder>/findings.md` only.
- `working_folder`: a docs path (§5 `working_folder`).
- The constitutional requirement is the FILES, not who writes them — the strategist may
  write `findings.md` itself or delegate (no mandatory writer-agent machinery).

**Findings shape** — per candidate, a row in the verdict matrix. **Ownership is a label, not a
verdict**: the `owner` column is always filled (a citation, or `precedent-clean`) and being owned
never puts KILL in the verdict column:

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
|---|---|---|---|---|---|

- **GO** — witnessed and sound. `use-mode` says how: `build-from-owned` (owned but unused — name
  the owner + the artifact/job it builds; cite honestly, never claim novel), `already-deployed`
  (owned and already wired — provenance only), or `novel-attempt` (precedent-clean — name the
  claim, its anchor, and the first obligation a follow-up faces). An owned-but-unused result is a
  GO, not a negative.
- **KILL** — **only** no-witness (non-vacuity) or tautological (definitional collapse); banked as
  a **typed negative**: what it would have contributed + the exact fact that zeroed it. **Owned is
  not a KILL.** A clean KILL is a successful run.

Close with the one-line answer to the dispatch `goal`. Per §5, `resolved` = the
`final_approver` accepted; for research, acceptance includes the P9 citation check.

## Standing rules

1. **Claim ≤ proof** (P10, universal — see the router): for research, demote, never inflate.
2. **Keystone claims carry their collapse-test inline** — the one fact that would zero them, same line.
3. **Precedent-first** — no "novel" verdict ships before a `precedent` skeptic ran. But a found
   owner is **not** a kill: research exists to find what already exists and can be used. A found
   owner relabels the candidate `build-from-owned` (cite, deploy, never claim novel); owned demotes
   only the novelty claim, and every artifact touching an owned result carries its owner label.
4. **Read-only by default** — research agents write only into `working_folder`, never the source tree.

## Names

Draw `agent_name` from `telemetry/agents/agent-pool.yaml` (ordered `role_fit`).
Prefer the primary `role_fit` entry and a `field` fit to the corpus. Never reuse a name
within one dispatch — the skeptic/auditor prohibition is the hard case of it. Never
invent a name outside the pool.

## Profiles

Repo-specific profiles may specialize this skill — the domainspec-lean-formalization
`research` skill (`domainspec-lean-formalization/.claude/skills/research/SKILL.md`,
sibling repo; unverifiable from this repo) is the math profile (old pre-v0.5.x schema,
pending realignment), as is
`vault/constitution/research-constitution.md` here (cite as pending realignment; do not
import its R-numbered machinery).
