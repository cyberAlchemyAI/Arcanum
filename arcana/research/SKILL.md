---
name: research
description: >
  Operating guide for running a `dispatch_type: research` subagent dispatch: shape it, find
  the evidence, run it, gate it, and write research.md + findings.md. Routed here from
  domainspec-subagents-strategy.
---

# research — operating guide for `dispatch_type: research`

<stage-handoff-contract>
Before a blocking sequential or zig-zag edge advances, the producing group must
emit an `arcanum.stage-handoff.v0.1` JSON record and pass
`node arcana/subagent-strategy/scripts/validate-stage-handoff.cjs <handoff.json>`.
The record binds the dispatch and edge identities, verdict, and evidence refs.
`needs_feedback` also binds the typed defect, repair owner group, feedback edge,
and remaining loop budget. Only `ready` unlocks the downstream group.
</stage-handoff-contract>

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
| `synthesizer` | monocular reconciliation — reconciles explorer returns and exchanges with skeptics; does not persist files | heavier for heavy synthesis |
| `writer` | "great research, no record" — persists `findings.md` after skeptic convergence | heavier for exact citation-preserving writing |
| `auditor` | "passed because nothing was checked" — evaluates `findings.md` after the writer | mid — checking, not generating |

Model is guidance, not law — chosen per agent by task difficulty, validated at the confirm gate.

**Topology** — the canonical shape:

```
explorers (n 2–4, pairwise tensioned)
   │ sequential
synthesizer (1 synthesizer) ◀──zig-zag──▶ reviewers (skeptics; robot_talks when the
   ▲                          │        question needs confrontation, not collection)
   └┄┄┄ feedback (conditional) ┄┘
                                      │ sequential
                                      ▼
                                 writer (1 writer) ──sequential──▶ auditor
```

The feedback back-edge exists only when there is a reviewer group AND material may be missing —
never by default. After skeptic convergence, a separate writer persists `findings.md`; an optional
auditor evaluates that file downstream. Final approval follows the router rather than being inferred
from the auditor's presence.

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

- **`research.md`** — the agent returns pasted in verbatim, after a one-section `## Objective`
  preamble. Wrap every return in a uniquely identified stable heading and preserve its original
  source locators. The strategist writes it by hand; it is transcription, so never dispatch an
  agent to do it. → How: the `domainspec-research-writing` skill
  (`.claude/skills/custom/domainspec-research-writing.md`)
- **`findings.md`** — the synthesis that turns those returns into usable claims, opening
  **Objective → Results → Context**. Every load-bearing claim cites the return it rests on. The
  downstream `writer` persists it after the synthesizer↔skeptic exchange converges.
  → How: the `domainspec-findings-writing` skill (`.claude/skills/custom/domainspec-findings-writing.md`)
- **One-agent dispatches** — persist original citations and reproducible details for every
  executable observation or independent recomputation directly in `findings.md`; never cite an
  agent return that was not persisted.

When `research-initial-definitions.md` registers Research Questions, put a **Research-question
coverage** section in `findings.md` before the candidate matrix. Include one row for every registered
RQ in the confirmed dispatch scope and one explicit row for every registered RQ outside it; never
omit an RQ silently. Mark an RQ outside the confirmed dispatch subset `deferred` and state why that
dispatch excluded it, unless an authoritative scope decision retired it; then mark it `retired` and
cite that decision.

| RQ id | status | answer | addressable evidence | contrary evidence / material uncertainty | boundary |
|---|---|---|---|---|---|

Apply these rules to each row:

- Use `answered`, `unresolved`, `deferred`, or `retired` as the status. Use `answered` only when the
  cited evidence resolves the entire RQ within its exact confirmed scope. If support is partial,
  use `unresolved`, record the supported partial conclusion, and name the exact residual gap. Never
  record a positive answer without evidence.
- Cite every load-bearing claim. Label support as `documentary assertion`, `executable observation`,
  `independent recomputation`, or `formal proof`; do not treat these evidence classes as interchangeable.
- Make `findings.md` self-contained enough to audit the answer. Cite original sources when available;
  when relying on collected material, cite its stable return ID in `research.md` and the original
  source when available, without duplicating the transcript. Treat `research.md` as a raw evidence
  trail, not as accepted evidence by itself.
- For `unresolved`, cite the material inspected and checks attempted, then name the exact remaining
  gap. Do not infer absence from failure to find evidence.
- For `deferred`, retain the reason. For `retired`, cite the authoritative scope decision.
- State material contrary evidence, residual uncertainty, and the boundary beyond which the answer
  does not apply; use an explicit `none found in <scope>` only when the inspected scope is named.

Keep RQ coverage orthogonal to candidate judgment. After the coverage section, put one verdict row
per candidate. **Ownership is a label, not a verdict**: the `owner` column is always filled (a
citation, or `precedent-clean`), and being owned never puts KILL in the verdict column.

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
|---|---|---|---|---|---|

- **GO** — witnessed and sound. `use-mode` says how: `build-from-owned` (owned but unused — name
  the owner + the artifact/job it builds; cite honestly, never claim novel), `already-deployed`
  (owned and already wired — provenance only), or `novel-attempt` (precedent-clean — name the
  claim, its anchor, and the first obligation a follow-up faces). An owned-but-unused result is a
  GO, not a negative.
- **KILL** — **only** no-witness (non-vacuity) or tautological (definitional collapse); bank it as
  a **typed negative**: what it would have contributed + the exact fact that zeroed it. **Owned is
  not a KILL.** A clean KILL is a successful run.

## 5. Close

Close with the one-line answer to the dispatch `goal`. The dispatch is `resolved` when the
`final_approver` accepts — and for research, acceptance includes checking that the findings
citations hold. Require the auditor and final approver to verify per-RQ coverage, evidence, status
discipline, and boundaries whenever Research Questions were registered.

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
