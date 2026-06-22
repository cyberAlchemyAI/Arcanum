---
tags: [vault, discovery, multi-agent, validator, subagents-strategy, anti-bias, spec-lifecycle]
node_type: discovery
is_session: false
layer: ontology, application
nature: procedural
status: active
version: 0.3.0
last_updated: 2026-06-15
---

# Anti-Bias Vector Composition — Validator Check

> Operational rules that enforce **Principle 5 (pairwise tension)** of the subagents-strategy
> constitution (v0.5.2). They run at the **confirm gate** over the dispatch sheet — the
> dispatch row's `groups` JSON column — *before* the dispatch is registered. This check is the **semantics owner** the
> constitution's four-test rule (`proposal.md` §P5, lines 124–129) points at; it is
> **additional** to the partition check ("angles non-overlapping AND covering" — see
> §Relationship to the partition check below).

> **v0.2.0 realignment note.** This file previously spoke the pre-v0.5.2 schema
> (`dispatch.yaml`, a `composition` block of **layers**, the retired `theorem-research`
> skill). v0.2.0 rewrites it to the v0.5.2 vocabulary: **`groups`** (not layers), group
> `role ∈ {investigate, evaluate, synthesize, meta-evaluate}`, agent
> `role ∈ {explorer, skeptic, writer, auditor}`, the per-group **`anti_bias`** axis, the
> per-agent **`angle`**, and the dispatch-wide **`anti_bias_global`**. Siblings
> `examples.md` and `literature.md` still carry old-schema worked shapes — pending the same
> pass. `principle.md` is realigned alongside this file.

> **v0.3.0 — post-dispatch realization removed (2026-06-15).** Anti-bias is now enforced
> **only at initialization** (the pre-dispatch Tests 1–4 below). The former post-dispatch
> "tension realization" checklist (Items 9–12) and the `Dissent:`-line / claim-ID contract it
> rested on are **retired**: self-declared per-agent dissent proved forgeable and fragile, and
> a flat parallel round cannot produce cross-citation by construction. The guarantee is that
> agents are tensioned **by design**, checked at the confirm gate; substance is not policed
> after the fact. The `Dissent:`-line element of the
> `agents-input-output` discovery is thereby superseded (that discovery's broader I/O
> contract — envelope, claim-IDs, anchors, verbatim, the P9 6-item checklist — stands); see
> its v1.1.0 note.

---

## Where the check lives (enforcement split)

Principle 5 has two halves, enforced in two different places — do not conflate them:

| Half | What | Enforced by | Failure mode |
|------|------|-------------|--------------|
| **Presence conditionals** | group `anti_bias` is present at `n ≥ 2`; `anti_bias_global` is present when ≥ 2 groups have `n ≥ 2` | **appender** (`append-dispatch.cjs`), mechanically, **exit 2** | record rejected at registration |
| **Tests 1–4** (axis / clone / spread / evidence) | the substance — is the axis real, are the angles distinct, is genuine disagreement pre-registered | **the `check-tension` gate** — two independent agents, before the human confirm | sheet returned to the strategist for revision |

The appender guarantees the **fields exist**; it does not judge whether they are *meaningful*.
That judgment is tests 1–4, checked at the confirm gate — this file owns it.

---

## When the check runs

**One** point in the dispatch lifecycle (constitution §3): **pre-dispatch (strict), at the
confirm gate.** After the strategist authors the sheet and before the human's affirmative /
before the dispatch row is appended. Failure blocks the dispatch — the sheet must be revised
and re-gated (P2). There is **no post-dispatch anti-bias check**: the guarantee is that the
agents are tensioned **by design at initialization**, not that disagreement is policed after
the fact.

---

## Pre-dispatch checklist (the four tests)

The validator runs the following over each **subject group**. A sheet is rejected if any
**R** test fires; the **G** tests must pass for the sheet to be accepted. These are the
operational form of the constitution's tests 1–4 (`proposal.md:124-129`).

### Step 1. Identify subject groups

**Item 1.** Parse the sheet's `groups` array. A **subject group** is any group with
`n ≥ 2` whose group `role ∈ {investigate, evaluate}` (its agents are `explorer`s or
`skeptic`s). Groups with `role ∈ {synthesize, meta-evaluate}` are out of scope (single-agent
by construction / single-check). Groups with `n == 1` are out of scope (no pair to tension).

**Item 2.** For each subject group, read the per-agent **`angle`** and the group **`anti_bias`**.
A subject group missing `anti_bias`, or any agent missing `angle`, fails here — but note this
is *also* the appender's presence conditional (exit 2), so a well-formed sheet never reaches
the gate with these absent. The gate's job starts at Item 3.

### Step 2. Classify the axis

**Item 3.** The group `anti_bias` names the tension axis; each `angle` is a position on it.
The four canonical axes (constitution closed vocabulary):

- **Methodology** — empirical / formal / adversarial / historical / computational.
- **Source-corpus** — e.g. arXiv-categorical / physics-journals / dissent-or-critical-literature / textbook-canon / backward-citation-tree.
- **Attack-vector** (skeptics) — precedent-attack / vacuity-attack / definitional-attack / scope-attack / counter-example-attack.
- **Temporal-prior** — modern-only / historical-lineage / mixed-with-decade-bins.

### Step 3. Red-flag tests (R — reject if fired)

**Item 4. Axis test (constitution test 1).** The group `anti_bias` must name one of the four
canonical axes, or an **explicitly declared composite** of them. Anything outside this
vocabulary → REJECT. (Closure governs per-group `anti_bias` only — `anti_bias_global` is
free-text and is never vocabulary-checked.)

**Item 5. Clone test (constitution test 2).** Any two `angle`s in the group share the same
core noun phrase → REJECT. Specific check: tokenize the angle strings, drop stopwords, and
verify the remaining content words yield at least two distinct primary verbs *or* nouns
across the pair. The angles are not differentiated along any load-bearing axis.

**Item 6. Spread test (constitution test 3).**
- In an `investigate` group: if all agents share one methodology, *or* all share one source
  corpus → REJECT. A pass requires at least two distinct axes represented across the group's
  angles. (Corpus monoculture defeats an explorer group; the corpus *is* its bias source.)
- In an `evaluate` group: any two skeptics share the same attack-vector gate → REJECT. Three
  "find problems with the argument" agents are one attack vector; precedent + vacuity +
  definitional are three.

### Step 4. Green-light tests (G — must pass)

**Item 7. Evidence test (constitution test 4) — pairwise predicted disagreement.** For every
unordered pair `(a_i, a_j)` in a subject group, the sheet must carry a written sentence of the
form: *"a_i runs [value_i], a_j runs [value_j] on the [axis] axis; a bias internal to a_i
along this axis would be exposed by a_j."* Any pair missing its sentence → REJECT. These
sentences are not decoration — writing the predicted disagreement per pair is what forces the
strategist to design genuine tension rather than assert it, and gives the tensioning reviewer
something concrete to check.

**Item 8. `anti_bias_global` coherence.** When ≥ 2 groups have `n ≥ 2`, the sheet carries a
dispatch-wide `anti_bias_global` theme (appender-enforced presence). The gate additionally
checks that each subject group's `anti_bias` axis is a plausible **specialization** of that
theme, not an unrelated axis — uncoordinated axes across groups drift (constitution §5).

A sheet that passes Items 4–8 PASSES — no residual judgment call beyond the sentences.

---

## Relationship to the partition check

The `domainspec-subagents-strategy` chain already checks two conditions on a group's angle set:

- **Non-overlapping.** No two agents investigate the same *concern*.
- **Covering.** Together the angles span the macro goal — no part is unaddressed.

These are **partition** conditions: *which subset of the goal each angle covers*. They do not
ask *which direction each angle points within its subset*. Tensioned-pairwise is strictly
stronger: a group can pass non-overlapping-and-covering and fail tension — four explorers
partitioning the goal into four disjoint sub-questions, each using the same arXiv-keyword
methodology. Clean partition, complete coverage, uncancelled bias term. The gate runs **both**:
partition first, then tension (this file). A sheet must pass both to be dispatched.

---

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [principle.md](./principle.md) | `derives-from` | The principle this validator operationalizes. Tests R (Items 4–6) enforce its negative form; tests G (Items 7–8) its positive form. |
| [literature.md](./literature.md) | `cites` | Adversarial-collaboration and groupthink lineage behind the tensioning requirement (Mill, Kahneman-Klein, Hong-Page). (Old-schema worked shapes pending realignment.) |
| [examples.md](./examples.md) | `instances` | Worked good/bad group shapes that exercise these tests. (Pending v0.5.2 realignment.) |
| `internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md` | `operationalized-by` ↔ | Constitution §P5 / lines 124–129 name this file as the semantics owner of the four-test rule; this file is the operational expansion. The constitution owns the enforcement split (appender vs gate). |
