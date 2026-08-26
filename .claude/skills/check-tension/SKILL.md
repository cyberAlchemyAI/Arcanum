---
name: check-tension
description: Init-time anti-bias gate. Before the human confirm, two independent agents verify a proposed dispatch sheet is genuinely tensioned (validator-check Tests 1–4); the sheet reaches the human only if BOTH pass — any reproval or disagreement returns it to the strategist. Gate infrastructure: not itself a dispatch, not subject to its own gate.
---

# check-tension — the init-time anti-bias gate

Anti-bias is enforced **only at initialization** (owner decision 2026-06-15): the guarantee
is that the agents of a dispatch are tensioned **by design**, checked here *before* the human
confirm. There is **no post-dispatch realization check** — the `Dissent:`-line apparatus was
retired (`.claude/skills/anti-bias-vector-composition/reference/validator-check.md` v0.3.0).
This skill is the gate; it owns no field and no type judgment.

## When it runs

Between **Propose** and **Confirm** in the lifecycle (router §3), for any sheet that has a
**subject group** — a group with `n ≥ 2` and role `investigate` or `evaluate`. A sheet with
no subject group has nothing to tension; the gate passes trivially.

## The two agents (independent)

Both read the **proposed sheet** — the `groups`, each agent's `angle`, each group's
`anti_bias` (field meanings owned by `register-dispatch`) — and judge it against the rubric
below. Read-only: neither writes to the source tree.

| agent | does |
|---|---|
| **checker** («aponta») | applies Tests 1–4 to every subject group; returns `PASS`, or per-pair / per-group apontamentos naming the exact failing test + a concrete fix |
| **reviewer** («revisa») | forms its **own** verdict on the same sheet, then marks agree / disagree on each of the checker's apontamentos — guards against both laxity and over-strictness in the checker |

Spawn both in ONE message (parallel). Draw `agent_name`s from
`telemetry/agents/agent-pool.yaml` (`auditor` / `skeptic` `role_fit`); never the same name for
both — the reviewer's independence is the whole point.

## The rubric — validator-check Tests 1–4 (not duplicated here)

Owner: `.claude/skills/anti-bias-vector-composition/reference/validator-check.md` Items 1–8.
Per subject group:

- **Test 1 — axis.** `anti_bias` names one canonical axis (methodology / source-corpus /
  attack-vector / temporal-prior) or a declared composite. Outside the vocabulary → REJECT.
- **Test 2 — clone.** No two `angle`s share the same core noun phrase → else REJECT.
- **Test 3 — spread.** Not all agents share one methodology/corpus (`investigate`) or one
  attack-gate (`evaluate`) → else REJECT.
- **Test 4 — evidence.** Every unordered pair carries its predicted-disagreement sentence
  ("a_i runs X, a_j runs Y on the [axis] axis; a bias in a_i would be exposed by a_j") →
  else REJECT.

## Outcome — only "both PASS" goes forward

- **Both agents PASS** → the sheet proceeds to the human **Confirm**.
- **Either agent reproves** → return to the strategist with the consolidated apontamentos;
  revise and re-run the gate.
- **The two disagree** (one passes, one reproves; or they contradict on a point) → **also
  return to the strategist.** Ambiguity is not good enough — the strategist revises until both
  pass cleanly. The human never adjudicates the gate.

The human Confirm therefore only ever sees a sheet that passed an independent double-check.

## Infrastructure, not a dispatch

The gate's two agents are **infrastructure** — like the appender:

- they are **not registered** as a dispatch in the ledger (no row); they are reported in the
  parent's narration;
- they are **not themselves subject to the gate** (no infinite regress).

## How the router uses it

The router runs this gate at the end of **Propose**, before presenting the sheet to the human
(router §3 / Pointers). It does not change registration, running, or close — those are
unchanged.
