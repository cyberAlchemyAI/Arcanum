---
name: research
description: >
  Operating guide for running a `dispatch_type: research` subagent dispatch: shape it, find
  the evidence, run it, gate it, and write research.md + findings.md. Routed here from
  domainspec-subagents-strategy.
---

# research — operating guide for `dispatch_type: research`

**What this is.** You are running a research dispatch: a fan-out of subagents that finds what
**already exists and can be used**, then records it. 

**What is produced.** `research.md` + `findings.md` in the `working_folder`, carrying a verdict on
every candidate. That is the whole deliverable.

**The procedure.** Shape it → Find the evidence → Run it → Gate it → Write the outputs → Close.

## 1. Shape it

Pick the agents, their topology, and their tensions.

**Roles** — each guards one failure mode; no agent guards two:

| `role` | guards against | model |
|---|---|---|
| `explorer` | monoculture — each generates under **one tensioned angle** | lighter — sweeps are mechanical |
| `skeptic` | folklore / vacuity — each attacks **one named gate** | heavier — adversarial work is hard |
| `writer` | "great research, no record" — the synthesizer, conventionally a single writer | heavier for heavy synthesis |
| `auditor` | "passed because nothing was checked" — meta-evaluates downstream of the reviewers, owns the verdict | mid — checking, not generating |

Model is guidance, not law — chosen per agent by task difficulty, validated at the confirm gate.

**Topology** — the canonical shape:

```
explorers (n 2–4, pairwise tensioned)
   │ sequential
synthesizer (1 writer) ◀──zig-zag──▶ reviewers (skeptics; robot_talks when the
   ▲                          │        question needs confrontation, not collection)
   └┄┄┄ feedback (conditional) ┄┘
```

The feedback back-edge exists only when there's a reviewer/auditor group AND material may be
missing — never by default. An optional `auditor` group placed downstream of the reviewers is the
natural dedicated `final_approver`.

**Tension** — classify every angle on four axes: **methodology** (empirical / formal / adversarial
/ historical / computational), **source-corpus**, **attack-vector** (the skeptic gate),
**temporal-prior** (modern-only / historical-lineage / mixed).

- **Reject before proposing** if: all angles share one core noun phrase; all explorers share one
  methodology or corpus; all skeptics share one gate.
- **Green-light** when: for every explorer pair you can write "a_i runs [X], a_j runs [Y] on the
  [axis] axis; a bias in a_i would be exposed by a_j" — and ≥2 distinct axes appear across the group.

## 2. Find the evidence

Each explorer **retrieves** — it does not recall. A claim rests on a source the explorer can point
to (a URL, a file path, a citation), never on model memory. Recall is a starting hypothesis; the
retrieved source is the proof.

**Where each explorer looks is set by its tension axes** (see **Shape it**). `source-corpus` and `temporal-prior`
assign each explorer a distinct search surface so the group covers the space instead of
overlapping — e.g. one sweeps current literature, one the foundational lineage, one the internal
repos for prior art.

**Two directions, both run before a candidate is judged:**

- **External** — locate with `WebSearch`, then read the actual source with `WebFetch`. A snippet is
  not a read. This is where papers and references come from.
- **Internal (ownership)** — search our own repos with `Grep`/`Glob` (and the `inventory` skill
  where installed) for an existing owner. This is what the `precedent` gate stands on: "already
  owned here" is retrieved, not assumed.

**Each explorer returns the locator per candidate** — what it found and where. A sweep that names
its surface and tools and comes back empty certifies `precedent-clean`; an unnamed "found nothing"
certifies nothing.

## 3. Run it

Spawn each group's agents with the Agent tool — **ALL agents of a group in ONE message**, so they
run in parallel. Each agent's `initial_prompt` is its launch prompt.

Schedule groups **by dependency**: a group is READY when every group with a `sequential`/`zig-zag`
edge into it has produced what it must respond to (zig-zag counts only in its `from`→`to`
direction — the `from` endpoint opens the exchange). Launch all READY groups concurrently;
independent chains run side by side. `feedback` edges never count as dependencies; a sheet with no
connections declares its groups independent. Declared order is a narration tiebreak only.

## 4. Write the outputs

Results land in the `working_folder` (a docs path, confirmed at the gate). Which files depends on
how many agents ran:

| agents | files |
|---|---|
| **2 or more** | `research.md` + `findings.md` |
| **1** | `findings.md` only |

- **`research.md`** — the agent returns pasted in verbatim. The strategist writes it by hand; it's
  transcription, so never dispatch an agent to do it. → How: the `domainspec-research-writing` skill (`.claude/skills/custom/domainspec-research-writing.md`)
- **`findings.md`** — the synthesis that turns those returns into usable claims. Every load-bearing
  claim cites the return it rests on. The strategist writes it, or hands it to a `writer` agent.
  → How: the `domainspec-findings-writing` skill (`.claude/skills/custom/domainspec-findings-writing.md`)

**Findings shape** — one verdict row per candidate. **Ownership is a label, not a verdict**: the
`owner` column is always filled (a citation, or `precedent-clean`), and being owned never puts KILL
in the verdict column.

## 5. Close

Close with the one-line answer to the dispatch `goal`. The dispatch is `resolved` when the
`final_approver` accepts — and for research, acceptance includes checking that the findings
citations hold.

## Standing rules

1. **Claim ≤ proof** — for research, demote, never inflate.
2. **Keystone claims carry their collapse-test inline** — the one fact that would zero the claim, on the same line.
3. **Precedent-first** — no `novel` verdict ships before a `precedent` skeptic ran. A found owner is
   not a kill; it relabels the candidate `build-from-owned` (cite, deploy, never claim novel), and
   every artifact touching an owned result carries its owner label.
4. **Read-only by default** — research agents write only into `working_folder`, never the source tree.

## Names

Draw `agent_name` from `telemetry/agents/agent-pool.yaml` (ordered `role_fit`). Prefer the primary
`role_fit` entry and a `field` fit to the corpus. Never reuse a name within one dispatch (the
skeptic/auditor prohibition is the hard case). Never invent a name outside the pool.

## See also

- **Router** — `.claude/skills/domainspec-subagents-strategy/SKILL.md`: triggers, human gate,
  anti-bias principle, lifecycle, `final_approver`, `exit_reason` vocabulary. Nothing here overrides it.
- **Record/sheet mechanics + field definitions** — `register-dispatch`
  (`.claude/skills/register-dispatch/SKILL.md`): the two appends, the appender, validation, enums.
