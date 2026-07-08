---
name: domainspec-subagents-strategy
description: >
  Route any subagent dispatch — check the dispatch trigger, hold the human confirm gate,
  enforce the universal invariants, then route by dispatch_type to the owning type skill
  (research, review, and experiment are LIVE; code, plan, and suggestion are reserved).
  The record/sheet form and its field definitions are owned by the register-dispatch skill.
  This skill defines no field and no type-specific judgment — it routes.
---

# domainspec-subagents-strategy — the dispatch router

**What this is.** The entry point for every subagent dispatch. It decides *whether* to
dispatch, holds the one human gate, enforces the rules that hold for **every** dispatch_type,
and hands off to the type skill that owns the type-specific judgment. It defines no field and
makes no type-specific call — it routes.

**The chain.** router (this skill) → type skill (`research` / `review` / `experiment`) →
form (`register-dispatch`). This skill is the first link.

## 1. When to dispatch — and what is not a dispatch

Dispatch only when at least one trigger holds:

- **synthesis** — 3+ sources to combine
- **context protection** — raw output ≫ what the parent actually needs
- **isolation** — discardable exploration you don't want in the parent's context
- **parallelism** — genuinely independent tasks

None hold → **work inline**. A dispatch is the multiplication step; don't pay its cost for
work one context window can do.

**Helper rule.** A single agent spawned *by* a running agent, inside that parent's scope, is
**not** a dispatch: no row, no gate. It is reported after the fact in the parent's
`agents_spawned`. It becomes a real dispatch the moment it **fans out (2+)** or **outgrows the
parent's scope**. *(The exact helper-vs-dispatch boundary is provisional — an open question,
not settled law.)*

## 2. The lifecycle — four steps, every dispatch

1. **Propose.** The strategist fills the sheet — consulting the routing table and the
   type skill for type-specific judgment (see **Routing by dispatch_type**) — and proposes it in chat. For each tensioned pair it
   states the question on which the two agents are predicted to disagree. **Before the sheet
   reaches the human, run the check-tension gate:** two independent agents verify the sheet is
   genuinely tensioned; the sheet advances only if **both PASS**, otherwise it returns here for
   revision.
2. **Confirm.** The human's explicit affirmative — see the **human gate** below. Nothing persists and nothing runs
   before it.
3. **Register + run.** Append the **dispatch row**, then schedule groups **by dependency**: a
   group is READY when every group with a `sequential` or `zig-zag` edge into it has produced
   what it must respond to (a `zig-zag` edge counts only in its `from`→`to` direction — the
   `from` endpoint opens the exchange). Launch all READY groups concurrently; `feedback` edges
   never count as dependencies; a sheet with no connections declares its groups independent;
   declared order is a narration tiebreak only. **Agents inside a group always run in parallel**
   — one message, each with its own briefing and context. An agent error degrades to a
   **partial group result** that downstream groups and the `final_approver` must be told about.
4. **Close.** Report `exit_reason` + `agents_spawned` in chat **and** in the findings doc, and
   append the **close row**.

Two appends (dispatch row, close row), one ledger, **append-only** — rows are never edited in
place. The record shape, the appender, and the close-row mechanics are owned by the
**register-dispatch** skill.

## 3. The human gate

The strategist proposes the filled sheet in chat; the human confirms, revises, or abandons.
**Nothing dispatches — and no row is written — before the confirm.** Confirmation is an
**explicit affirmative** from the human; silence or a question is **not** confirmation. Once
confirmed, the sheet is **frozen**: any strategist edit after confirm re-enters this gate.

There is exactly **one human gate** — this entry confirm. The close is report-only (plus the
close row); no second human gate exists. The human never loses the power to abandon
(`user_abort`).

## 4. Routing by dispatch_type

Route by `dispatch_type` to the skill that owns that type's judgment. A **LIVE** type has a
populated skill; routing to a **RESERVED** type is not allowed — **refuse and tell the user**
the type is not yet populated.

| dispatch_type | status | route to |
|---|---|---|
| `research` | **LIVE** | the **research** skill — canonical shape, roles, gates, research.md + findings.md |
| `review` | **LIVE** | the **review** skill — red-team judgment: attack lenses, severity taxonomy, verification discipline, change-request findings |
| `experiment` | **LIVE** | the **experiment** skill — pre-registered criterion freeze, validity gates, SURVIVED/FALSIFIED/INVALID verdict (propose phase only: INVALID may be rendered here; SURVIVED/FALSIFIED are rendered at the separate downstream run) |
| `code` | **RESERVED** | none — must not be dispatched until populated |
| `plan` | **RESERVED** | none — must not be dispatched until populated |
| `suggestion` | **RESERVED** | none — must not be dispatched until populated |

A LIVE row must point to an existing skill — that is a consistency check, not the source of
the type's judgment. Promoting a RESERVED type to LIVE is an owner act, not a strategist call.

## 5. Universal invariants — every dispatch_type

- **Pairwise tension.** Any group of n ≥ 2 agents must be **pairwise tensioned**: for every
  pair a competent observer could predict, in advance, a question on which they disagree. The
  group names the axis (`anti_bias`, drawn from **methodology | source-corpus | attack-vector |
  temporal-prior**, or a declared composite); each agent takes a position (`angle`).
  Non-overlapping is not enough. This is enforced by the **check-tension** skill at the confirm
  gate (the Propose step) — an untensioned sheet goes back to the strategist for revision.

- **Aggregation is derived, never a field.** `robot_talks: true` → the group **synthesizes**;
  otherwise the group **concatenates**. A bare concat is intermediate plumbing — it feeds a
  downstream synthesize group or the `final_approver`; it is never the dispatch's final
  deliverable.

- **Claim ≤ proof** in every artifact the dispatch produces.

- **Final approval.** Every dispatch names a `final_approver` holding the last accept/reject
  with a does-this-fit-the-whole mandate. It is either `parent` (default — the strategist
  session and the human behind it) **or** a **dedicated approver group**: one agent whose role
  is `auditor` and that does **no other work** in the dispatch. An approver may **never** sit in
  a working group — **self-approval is prohibited**. If the approver's group never runs (early
  abort, upstream error), approval **falls back to `parent`**. The approver receives the **full
  `working_folder`**. When the approver is an agent it *recommends* accept/reject; the human gate
  remains the single entry confirm (see the **human gate**).

- **Three dials, smallest scope wins.** See the **three dials** below.

- **exit_reason.** Closed vocabulary. See below.

- **Trust-but-verify.** If a subagent wrote files or claimed a check passed, inspect the actual
  diff / run the actual check before treating it as done.

- **Meta and lineage.** A dispatch *about* dispatching (planning what to research, or
  redesigning the framework) is marked `meta: true`. `parent_dispatch_id` exists **only** on a
  dispatch that a meta dispatch planned, pointing back to it; it is absent on every top-level
  dispatch. A meta-planned child is a new sheet and **re-enters the confirm gate** — the human
  gate has no meta exception.

- **Robot-talks binding.** See below.

## 6. The three dials

Three dials, three scopes. Given "the reviewers should get two passes":

| dial | scope | use it when |
|---|---|---|
| `layers: 2` | the group | two independent passes over the same material, no conversation between them |
| `loop_cap: 2` | the edge | two rounds of conversation between two groups (`zig-zag`/`feedback`) |
| `max_loops: 2` | the dispatch | the `final_approver` rejected and asked for the entire sequence again |

**One scenario, one dial. If two seem to fit, the smallest scope wins.** (`loop_cap` lives only
on `zig-zag`/`feedback` edges; `max_loops` is the whole-graph brake — the harness refuses run
N+1, and a re-run fires only on a `final_approver` rejection.)

## 7. exit_reason

Report one value at close, from this **closed vocabulary**:

| value | meaning |
|---|---|
| `resolved` | the `final_approver` accepted / no contradiction remains — nothing else counts as resolved |
| `loop_ceiling_reached` | hit a loop ceiling (an edge `loop_cap` or `max_loops`) without converging |
| `dissent_irreconcilable` | agents did not reconcile after the ceiling |
| `user_abort` | the human abandoned at the gate — this value can never disappear |
| `error` | technical failure that leaves the dispatch unable to produce its deliverable |

**Precedence, when more than one applies:**
`user_abort` > `error` > `dissent_irreconcilable` > `loop_ceiling_reached` > `resolved`.
(A ceiling hit that leaves positions unreconciled is `dissent_irreconcilable`; a
`final_approver` rejection the human chooses not to re-run is an abandonment → `user_abort`.)

Report `exit_reason` with 1–2 sentences of context, alongside `agents_spawned` (total + spawn
tree keyed by agent role, helpers in their own bucket, + loops used) — in chat, in the findings
doc, and on the close row.

## 8. Robot-talks binding

A group with `robot_talks: true` (meaningful only at n ≥ 2): after their parallel runs the
agents come back and **discuss** — each confronts the others' outputs along the group's declared
tension — before the group returns one result. That group additionally **follows the
robot-talks skill** for the discussion.

Two rules the router enforces here:

- **Single gate.** Where the robot-talks procedure would prescribe an additional human gate,
  this router's single-gate rule (the human gate) governs — there is still only the one entry confirm.
- **Collapse detection.** A synthesizer sitting downstream of any robot-talks group whose
  positions feed it **must receive each of that group's agents' initial AND final positions**,
  so premature convergence / collapse is detectable.

## Pointers — single owners

- **Form (record/sheet fill mechanics) + field definitions** — the **register-dispatch** skill:
  the field tables and enums, the two appends, the appender, the close row, `invoked_by`. Every
  field's definition lives there, not here.
- **Type judgment** — the type skill for the dispatch_type: the **research**, **review**, and
  **experiment** skills.
- **Init-time tension gate** — the **check-tension** skill: the two independent agents that
  verify the sheet is genuinely tensioned before the human confirm; only "both PASS" reaches the
  human. It owns the runnable rubric.
- **Robot-talks discussion** — the **robot-talks** skill (bound by any `robot_talks: true`
  group; single-gate rule above governs).
- **Agent names** — the allowed-names pool at `telemetry/agents/agent-pool.yaml`; never invent a
  name outside it.
