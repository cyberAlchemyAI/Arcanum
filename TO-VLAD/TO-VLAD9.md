---
to: Vlad
from: Victor (anti-bias role-set reconciliation, verified on disk)
re: "The anti-bias-vector-composition principle encodes FOUR agent roles, but the enforced register-dispatch schema is at FIVE — `synthesizer` was added in tooling and never back-propagated to the governing prose. Ratify the fifth role, or declare Arcanum deliberately stays at four."
date: 2026-06-30
audit-against: "Arcanum: formulae/anti-bias-vector-composition/reference/{principle.md,validator-check.md}. domainspec: vault/constitution/{domainspec-subagents-strategy-constitution.md@0.3.0, research-constitution.md@0.2.0, domainspec-subagents-strategy-constitution.v0.4.0-draft.md}. Enforced tooling: ~/.claude/skills/register-dispatch/SKILL.md (schema v0.6.0) + append-dispatch.cjs (the live validator)."
status: draft for discussion — single-point reconciliation
---

# To Vlad — the anti-bias role-set says four; the validator that actually runs says five

Ninth pass. One point, narrow and verifiable: there is a **role-set version skew** between
the prose that *describes* our dispatch discipline and the schema that *enforces* it. The
prose says four agent roles. The enforced schema says five. The fifth role — `synthesizer` —
is real, is running today, and is undocumented in every governing file in both repos.

I verified every claim below on disk.

## 1. What the prose says — four roles, in three places

The anti-bias principle is explicit and load-bearing:

> "agents with `role ∈ {explorer, skeptic, writer, auditor}`"
> — `formulae/anti-bias-vector-composition/reference/principle.md:52`

That file pins itself to **constitution v0.5.2** (`principle.md:14`). And the four-role set is
not Arcanum-local — domainspec agrees, twice:

- `research-constitution.md:25` (v0.2.0): "names **four canonical roles** (explorer · skeptic · writer · auditor)".
- `research-constitution.md:357`: "The four canonical roles `explorer | skeptic | writer | auditor` (R4–R8)."
- Even the forward-looking `domainspec-subagents-strategy-constitution.v0.4.0-draft.md:355` still writes "the **four agent roles** `explorer | skeptic | writer | auditor`".

So as far as the *written law* of either repo is concerned, there are four agent roles, and
"synthesize" is only a **group/wave role** (`waves[].role ∈ {investigate, evaluate, synthesize, meta-evaluate}`) — the *writer* is the agent that fills a synthesize group (`principle.md:61`: "`synthesize` group (writer). Single agent by construction").

## 2. What the validator says — five roles

The `register-dispatch` skill is not documentation; it is the **deterministic appender that
validates every dispatch record and refuses non-conforming ones** (it is what I run to register
a dispatch; it ran today). Its schema is **v0.6.0**, and its agent-role enum is:

> `role` ✅ — `explorer | synthesizer | skeptic | writer | auditor`. Pipeline order:
> explorers gather → **synthesizer** reconciles their returns into a candidate picture
> (n:1, exchanges with reviewers, may pull more from explorers) → skeptics attack →
> **writer** persists `findings.md` (n:1) → auditor.
> — `~/.claude/skills/register-dispatch/SKILL.md`, schema v0.6.0

The close-row schema confirms it independently: the `agents_spawned.tree` is "keyed by agent
role — `explorer | synthesizer | skeptic | writer | auditor` — plus a `helpers` bucket." Five.

So `synthesizer` has been promoted from a *group role done by the writer* to a **first-class
agent role distinct from the writer**: the synthesizer *reconciles explorer returns into a
candidate picture* (n:1, fan-in), the writer *persists the findings artifact* (n:1). They are
two different jobs that the four-role set collapsed into one.

## 3. The skew, stated plainly

| Source | Version | Agent roles | `synthesizer` an agent role? |
|---|---|---|---|
| Arcanum `anti-bias .../principle.md` | refs v0.5.2 | explorer · skeptic · writer · auditor | No — it's a group role |
| domainspec `research-constitution.md` | 0.2.0 | explorer · skeptic · writer · auditor | No |
| domainspec subagents-strategy (live) | 0.3.0 | explorer · skeptic · writer · auditor | No |
| domainspec subagents-strategy (draft) | 0.4.0 | explorer · skeptic · writer · auditor | No |
| **`register-dispatch` (enforced)** | **0.6.0** | **explorer · synthesizer · skeptic · writer · auditor** | **Yes — n:1 reconciler** |

The enforced schema is **three minor versions ahead** of the live constitution and **one
ahead** of the version the anti-bias principle pins to. The fifth role exists in the only
artifact that can reject a malformed dispatch, and in none of the artifacts that explain what
a dispatch is.

**Correction to my own earlier framing:** I had been citing "five roles" as if it were already
canonical. It is canonical *in the tool*, not in the *principle*. The principle is not wrong —
it is pinned to v0.5.2, where four was correct. The defect is that nobody bumped the principle
when the schema split synthesizer out.

## 4. Where the fifth role lands in the anti-bias rule (the easy part)

Adding `synthesizer` does **not** disturb the tension logic, and this is the reassuring part.
The principle's tension rule applies only to subject groups with `n ≥ 2` — explorers
(`investigate`) and skeptics (`evaluate`). The synthesizer, exactly like the writer, is **n:1
by construction** (one agent reconciling fan-in). So it joins the *"does not apply"* set:

> **Does not apply:** `synthesize` group (**synthesizer**, then writer). Single agents by
> construction; nothing to tension against.

That is the whole edit to `principle.md:61` — promote "synthesize group (writer)" to
"synthesize group (synthesizer → writer)", and add `synthesizer` to the role enum on line 52.
No new tension axis, no change to `validator-check.md`'s pairwise rule. The retired-`evaluator`
note (`principle.md:58`) stays as-is — that was a different call (a 5th role that *was*
rejected); this is a 5th role that the schema *already adopted*.

## 5. The decision for you

This is a cross-repo canonicalization call, so it is yours:

- **Ratify (recommended).** Bump the anti-bias principle to the five-role set, citing the
  register-dispatch v0.6.0 schema as the authority, and place `synthesizer` in the
  "does not apply" set (§4 above). Then flag — separately — that the domainspec
  `research-constitution` (0.2.0) and `subagents-strategy-constitution` (live 0.3.0, draft
  0.4.0) carry the *same* stale four, and owe the same bump so the written law matches the
  enforced schema in both repos.
- **Or declare four deliberate.** If `synthesizer` is meant to be a *tooling-only*
  convenience (a fan-in helper, not a governed role), then say so in the principle explicitly
  — "the schema records a `synthesizer` agent for ledger accounting; the governed role-set is
  four; synthesis is a writer responsibility" — so the next reader does not trip on the skew.

What is **not** an option is leaving it silent: a validator that enforces five against a
constitution that names four is exactly the kind of drift the dispatch governance is supposed
to prevent. Right now the governance layer disagrees with itself about how many roles it has.

Secondary note (do not let it expand this pass): the pre-dispatch enforcer people sometimes
call the "validator" is the **`check-tension` gate** run at the confirm step
(`validator-check.md`), not an agent role. If we ratify five, worth one sentence in the
principle to keep "validator (the gate)" from being misread as "validator (a sixth role)."

— V.
