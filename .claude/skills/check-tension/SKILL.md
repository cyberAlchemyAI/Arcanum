---
name: check-tension
description: Init-time anti-bias gate. Before the human confirm, two independent agents verify a proposed dispatch sheet is genuinely tensioned against the rubric this skill owns — the four anti-bias tests plus a cross-group coherence check; the sheet reaches the human only if BOTH pass. Any reproval or disagreement returns it to the strategist. Gate infrastructure: not itself a dispatch, not subject to its own gate.
---

# check-tension — the init-time anti-bias gate

Anti-bias is enforced **only at initialization**: the guarantee is that the agents of a
dispatch are tensioned **by design**, checked here *before* the human confirm. There is **no
post-dispatch realization check**. This skill is the gate and **owns the rubric below**; it
owns no dispatch field and no type judgment.

## When it runs

Between **Propose** and **Confirm** in the dispatch lifecycle — the step the
`domainspec-subagents-strategy` skill defines — for any sheet that has a **subject group**: a
group with `n ≥ 2` and role `investigate` or `evaluate`. A sheet with no subject group has
nothing to tension; the gate passes trivially.

## The two agents (independent)

Both read the **proposed sheet** — the `groups`, each agent's `angle`, each group's
`anti_bias` (field meanings owned by the `register-dispatch` skill) — and judge it against the
rubric below. Read-only: neither writes to the source tree.

| agent | does |
|---|---|
| **checker** («aponta») | applies tests 1–5 to every subject group; returns `PASS`, or per-pair / per-group apontamentos naming the exact failing test + a concrete fix |
| **reviewer** («revisa») | forms its **own** verdict on the same sheet, then marks agree / disagree on each of the checker's apontamentos — guards against both laxity and over-strictness in the checker |

Spawn both in ONE message (parallel) — two **distinct, independent** agents; never the same
identity for both, since the reviewer's independence is the whole point. As gate
infrastructure they carry no agent-pool identity and write nothing to it.

Each **apontamento** is structured, not prose, so the strategist can act on it mechanically:

- **target** — the failing subject group (and the unordered pair, for tests 2 / 4).
- **test** — which test fired (1 / 2 / 3 / 4 / 5).
- **fix** — one concrete revision (e.g. "re-axis a_j from precedent-attack to
  definitional-attack").

The checker returns `PASS` or a list of apontamentos. The reviewer returns its **own**
`PASS`/list plus an agree/disagree flag on each of the checker's apontamentos.

## The rubric — the four anti-bias tests + a cross-group check

Tests 1–4 are the four anti-bias tests every subject group must survive; test 5 is the fifth,
cross-group coherence check applied once per sheet.

The axis vocabulary (closed — test 1 checks `anti_bias` against it):

- **methodology** — empirical / formal / adversarial / historical / computational
- **source-corpus** — e.g. arXiv-categorical / physics-journals / dissent-literature / textbook-canon / backward-citation-tree
- **attack-vector** (skeptics only) — precedent / vacuity / definitional / scope / counter-example
- **temporal-prior** — modern-only / historical-lineage / mixed-with-decade-bins

Per subject group — REJECT if any fires:

- **Test 1 — axis.** `anti_bias` names one canonical axis above, or an explicitly declared composite of them. Outside the vocabulary → REJECT.
- **Test 2 — clone.** No two `angle`s share the same core noun phrase — tokenize, drop
  stopwords, and the pair must yield ≥ 2 distinct primary verbs *or* nouns → else REJECT.
- **Test 3 — spread.** `investigate`: ≥ 2 distinct axes across the angles; all sharing one
  methodology *or* one corpus → REJECT. `evaluate`: no two skeptics share an attack-vector
  (precedent + vacuity + definitional = three; three "find problems" = one) → else REJECT.
- **Test 4 — evidence.** Every unordered pair carries its predicted-disagreement sentence
  ("a_i runs X, a_j runs Y on the [axis] axis; a bias in a_i would be exposed by a_j") →
  else REJECT. Writing this per pair is what forces real tension instead of asserting it.

Once per sheet (not per group):

- **Test 5 — global coherence.** When ≥ 2 groups have `n ≥ 2`, each subject group's
  `anti_bias` must be a plausible **specialization** of the sheet's `anti_bias_global` theme,
  not an unrelated axis → else REJECT. (Uncoordinated axes across groups drift.)

A group passing tests 1–4, and a sheet passing test 5, PASSES — no residual judgment beyond
the evidence sentences.

> **This gate checks only the *tension* half of the anti-bias guarantee.** The *partition*
> half — angles non-overlapping AND covering the goal — is checked earlier by the
> `domainspec-subagents-strategy` skill. A sheet must pass both; partition first, then this
> gate.

## Outcome — only "both PASS" goes forward

- **Both agents PASS** → the sheet proceeds to the human **Confirm**.
- **Either agent reproves** → return to the strategist with the consolidated apontamentos;
  revise and re-run the gate.
- **The two disagree** (one passes, one reproves; or they contradict on a point) → **also
  return to the strategist.** Ambiguity is not good enough — the strategist revises until both
  pass cleanly. The human never adjudicates the gate.
