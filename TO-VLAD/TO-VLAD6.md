---
to: Vlad
from: Victor (subagent-dispatch design, synthesized)
re: "Arcanum/Craft — sixth pass: composing and observing multi-agent dispatches in Craft's vocabulary (the per-Wave model)"
date: 2026-06-08
audit-against: "development/craft/ @ HEAD (2026-06-08) + domainspec subagents-strategy work; benchmark = domainspec/vault/discovery/subagent-dispatch-observability/discovery.md"
status: draft for discussion — implementation handoff
---

# To Vlad — composing and observing subagent dispatches, in Craft's words

Sixth pass, and a different kind of memo from the prior five. Those five
*audited* an Arcanum object and reported a gap. This one *hands you a converged
design* to implement: a model for **composing and observing multi-agent subagent
dispatches**, reconciling the domainspec "subagent strategy" line of work with the
vocabulary Craft already publishes in `development/craft/`. The discovery half
(three-level observability) is already written and anchored in real data at
`domainspec/vault/discovery/subagent-dispatch-observability/discovery.md`; this
memo carries the *composition* half it depends on, expressed in Craft terms so the
two halves speak one language.

The governing discipline, same as ever: **do not invent vocabulary Craft already
provides.** Where Craft has a term — Wave, Stage Worker, Stage Receipt, Operational
Lane, Route Handoff, Route Event, `pass | flag | block`, the
Define → Design → Plan → Execute → Validate → Reflect cycle — I reuse it and name
the mapping explicitly. Where the design needs something Craft does not yet have
(typed edges between Waves, a per-Wave `mode`), I say so and ground the new term in
the nearest Craft relation. The intentional divergences from Craft are listed in
their own section at the end so they are visible, not smuggled.

---

## The one-sentence thesis (everything below is a subset of this)

A dispatch is **not** characterized by a single global "topology" or "mode" — it is
a **sequence/graph of Waves**, each Wave carrying its own `mode` and `intent`, with
the relationships between Waves expressed as **typed edges** (`consumes`,
`reviews`, `reopens`); the old global enums (`sequential | zig-zag | parallel |
pipeline`) **dissolve** because they are now *emergent properties of the edge set*,
not a label you pick up front.

---

## 1. Composition is per-Wave, not a global topology (the MECE fix)

The earlier framing asked "what topology is this dispatch?" and offered a flat enum
(`sequential | zig-zag | parallel | pipeline`). That is the wrong unit. It is not
MECE: a real dispatch can be parallel *and* pipelined *and* have a reactive loop in
it, all at once, so a single label either lies or forces an arbitrary choice.

The fix maps cleanly onto a Craft term Craft already owns. Craft's planning ladder
is `Plan → Waves → Tasks → SWUs` (`CRAFT-INITIAL-DEFINITION.md#plan`). A **Wave** is
the stage/layer unit. So:

- A **dispatch** is a Plan (Craft: a run/Plan).
- A **Wave** is one stage of that dispatch. **Wave = the discovery's `layer`.**
  (Map note: domainspec calls this `layer`; Craft calls it `Wave`. Use **Wave** in
  Craft-facing artifacts; the observability schema keeps `layer_id` as the FK name to
  avoid breaking the already-frozen discovery contract — they are the same object.)

Each Wave carries its **own** shape and purpose:

- **`mode`** — how the agents *within* the Wave relate: `single | fan-out |
  zig-zag`. (Use **`zig-zag`**, never `ping-pong`, as the canonical name for the
  reactive/alternating shape.)
- **`intent`** — what the Wave is *for* (its phase/purpose; see §5).

The four old global enums are not deleted by fiat — they **dissolve**, because each
is now derivable from the edge set between Waves:

| Old global label | Emerges from |
| --- | --- |
| `sequential` | a Wave that `consumes` a prior Wave (forward data edge) |
| `parallel` | two Waves with **no edge** between them |
| `zig-zag` | Waves that alternate / feed back (a `reopens` edge exists) |
| `pipeline` | a chain of Waves with **differing `mode`s** — automatic, not a chosen label |

If you ever feel the need to write the global label down, that is the smell that the
edge set is underspecified. Record the edges; the topology is a query result.

---

## 2. Typed edges between Waves (replaces `reacts_to`)

The relationship between two Waves is a **typed edge**, not a flat free-text
`reacts_to`. Three edge types cover the design, each grounded in a relation Craft
already publishes:

| Edge | Meaning | Craft grounding |
| --- | --- | --- |
| `consumes` | Wave B uses Wave A's output as input — forward data dependency. | Craft `dependency` (`dependency_blocker` / `dependency_enabler`, `CRAFT-LEDGER-TYPE-SYSTEM.md`); a Cross-Context Relation of kind dependency. |
| `reviews` | Wave B is a review **of** target Wave A. | A review Wave whose Operational Lane is `validator`/`auditor` over A's artifact. |
| `reopens` | the **cyclic back-edge**: a `block` verdict from a review Wave reactivates the prior Wave it reviewed. | Craft `residue_opened` + `recomposition` (`route_event_type` enum in `CRAFT-INTERACTION-LEDGER-SCHEMA.yml`): a blocked receipt opens residue and forces recomposition rather than closing the context. |

`reopens` is the only edge that creates a cycle. Everything else is a DAG.

---

## 3. Cyclic Waves are bounded loops, not chaos

The Wave graph is a **DAG plus bounded feedback edges**. The single source of cycles
is `reopens`:

1. A review Wave (lane `validator`) emits `block` on the Wave it `reviews`.
2. That `block` creates a `reopens` edge back to the reviewed Wave.
3. The reviewed Wave re-runs (Craft: residue opened → recomposition attempted).
4. The whole loop is bounded by a **`loop_cap`** budget.
5. If still `block` after the cap, the dispatch **closes** with a typed exit reason —
   `reviewer_rejected_twice` or `loop_cap_reached` — never an open-ended retry.

This mirrors Craft's hard rule that a **blocked receipt cannot close a context**
(`CX-R004`): the loop exists precisely so a `block` is forced through recomposition
rather than silently absorbed, and `loop_cap` is the stop-criterion that keeps the
reflection from running forever.

> Open question — **`loop_cap` default.** I am proposing a default of **1** (one
> re-run, then close with a typed exit), on the reasoning that a reviewer who blocks
> the same artifact twice is signalling a definition/design problem one altitude up,
> not an execution problem the same Wave can fix. I do not have usage data to defend
> 1 over 2. Treat the value as the open knob; the *mechanism* (bounded, typed exit)
> is the load-bearing part.

---

## 4. Verdict vocabulary: adopt Craft's `pass | flag | block`

Drop any `pass | fail | mixed`. The universal Wave/review verdict is Craft's
**`pass | flag | block`** (`CRAFT-LEDGER-TYPE-SYSTEM.md` gate result values;
`receipt_status` enum in `CRAFT-INTERACTION-LEDGER-SCHEMA.yml`):

- `pass` — clean.
- `flag` — soft concern; surfaced, does not stop the dispatch.
- `block` — hard stop; triggers the `reopens` edge.

This is a straight rename and the discovery's `layer.closed.verdict` enum
(`pass | fail | mixed | n/a`) should move to `pass | flag | block | n/a` to match.
`flag` carries the soft-concern signal that `mixed` was clumsily standing in for.

---

## 5. Lanes vs Roles — keep BOTH, at different levels

This is the cut that stops the two vocabularies from competing. They do not compete
because they live on **different objects**:

- **Operational Lane** is a property of the **Wave**. Craft term, used verbatim:
  `validator | auditor | qa | tech | business | planner | governance | operations |
  integrator | blocker_refiner` (`CRAFT-LEDGER-TYPE-SYSTEM.md#operational-lanes`). It
  names the **accountability / expertise domain** of that Wave.
- **Role** is a property of the **agent (Stage Worker)**. It is the **epistemic
  function**: `explorer | skeptic | writer | reviewer | implementer`. It names what
  that worker *does*.

Worked instance: a review Wave has **lane `validator`**; the agents inside it have
**role `reviewer`**.

Two sub-rules that keep the role set small:

- **"Reviewer" is one role, not several.** It is `reviewer(check = content | format
  | both)`. Content-review and format-review are *checks* on the same review role,
  not separate roles. Resist the pressure to mint `format-reviewer` /
  `content-reviewer` — that is role proliferation the discovery already flagged.
- **Reviewers attach per-Wave via Craft's `secondary_lanes`.** Craft's conflict
  policy (`CRAFT-LEDGER-TYPE-SYSTEM.md`, validation rule 10) already says
  `secondary_lanes` are required reviewers and that **`auditor`/`validator` as a
  secondary lane requires review evidence before closure**, independent of the
  artifact-producing lane. We adopt that as-is: **every work Wave declares
  `validator`/`auditor` as secondary lanes → review happens at every step**, ideally
  ≥2 reviewers, **tier-aware**: ≥2 where the Wave produces a durable artifact
  (research / doc / code), lighter (0–1) for ephemeral lookups.

> Open risk — **lanes-vs-roles coexistence.** This is the part most likely to drift
> in practice: a reader will be tempted to collapse `validator` (lane) and `reviewer`
> (role) into one word because in the common case they co-occur. They must not be
> collapsed — the lane answers *"what expertise is accountable for this Wave"* and the
> role answers *"what does this worker do"*, and they cross (a `tech` Wave can contain
> a `skeptic` role; a `validator` Wave contains `reviewer` roles). If you see a single
> field trying to carry both, that is the regression.

---

## 6. Orchestrator and Synthesizer are parent functions, not child agents

Both are enacted by the **parent skill**, not spawned as child Stage Workers. The
rationale matters because the tempting move is to spawn them:

- **Orchestrator** = the runtime coordinator that orders how Waves initialize. This
  is the **parent skill's job**, not a child agent. Craft is explicit: the
  orchestrator *is a context*, not a worker
  (`CRAFT-REFINE-RUNTIME-STRATEGY.md` — "the orchestrator is a context"; "Refine is
  an orchestrator, not a monolithic model-backed command"). domainspec says the same
  of its strategist: *enacted by the skill, not a subagent*. **Spawning the
  orchestrator as a child doubles the control flow and duplicates ownership of the
  dispatch** — exactly the Codex-inside-Codex recursion that timed out in
  `CRAFT-REFINE-001/002`. Do not do it.
- **Synthesizer** = collecting final outputs and handing them to the parent to report
  to the user. Treat this as a **mechanical handoff done by the parent** — gather the
  Stage Receipts, hand up — **not** a deep-synthesis child agent.

> Flag, explicit — **synthesizer bias bottleneck.** The mechanical-handoff framing
> holds *only while synthesis is mechanical*. The moment it becomes genuine N-Wave
> synthesis (a single reader collapsing the conclusions of many tensioned Waves into
> one narrative), it is the known **"single synthesizer" bias bottleneck**: a lone,
> un-tensioned reader can quietly collapse a tensioned layer back to one viewpoint,
> undoing the whole reason for fanning out. If you reach that point, the synthesizer
> must itself become **reviewable** — a Wave with its own `reviews` edge — not a
> trusted final voice. Mark the transition; do not let it happen silently.

---

## 7. Intent / phase placement — adopt Craft's cycle, diverge on one point

Adopt Craft's cycle verbatim as the `intent` axis:

```text
Define → Design → Plan → Execute → Validate → Reflect
```

**One intentional divergence from Craft: Research is a first-class step AFTER
Define, not folded into Define.**

- Craft treats research as an *input to* Define (`CRAFT-INITIAL-DEFINITION.md#define`
  lists "research" among Define's inputs).
- We make **Research its own step, between Define and Design.** Rationale: Define
  produces the *unknowns / scope / residue ledger*; Research *resolves* those
  unknowns; its output feeds Design or becomes a `discovery.md`. **You cannot research
  well what you have not yet defined** — hence research-after-define. This is a
  deliberate departure, recorded as such in §10.

A full user flow is freely composable from Waves. Concrete worked example —
Define → Research → (optional `discovery.md`) → Implement, with a review Wave after
each work Wave:

| Wave | `intent` | `mode` | Operational Lane (primary / secondary) | edges in |
| --- | --- | --- | --- | --- |
| W1 | Define | `single` | business / validator | — |
| W2 | Research | `fan-out` | tech / validator, auditor | `consumes` W1 |
| W3 | Review (of research) | `single` | validator / — | `reviews` W2; `reopens` W2 on `block` |
| W4 | Implement | `single` | tech / validator, auditor | `consumes` W2 |
| W5 | Review (of implementation) | `zig-zag` | validator / — | `reviews` W4; `reopens` W4 on `block` |

Read this table as the *whole* topology specification: there is no separate global
"this is a pipeline" tag. W1→W2→W4 is sequential-by-`consumes`; W3 and W5 are review
Waves with bounded `reopens` back-edges; if W2 and a hypothetical W2′ had no edge
between them they would be parallel. The `discovery.md` after W3 is optional and
emitted only when Research's output is durable enough to promote.

---

## 8. Observability — three nesting levels (summarized; full schema in the discovery)

The recording contract is already written and frozen in structure at
`domainspec/vault/discovery/subagent-dispatch-observability/discovery.md`. Here is the
summary aligned to Craft's ledger, so the two artifacts use one vocabulary. All three
levels are **flat, append-only JSONL rows joined by FK** (`dispatch_id` / `wave_id` /
`agent_id`) — not nested objects. Each of `dispatch` and `agent` emits `started` +
`closed` so a crash leaves a visible `started`-without-`closed`.

### Level 1 — `dispatch` (Craft: the Plan / run)

`goal` (required — monitoring field #1), `output_root` (path), **`dispatch_kind`**
(`standard | meta`; **meta** = a Wave whose Stage Worker is *itself* an
orchestrator / sub-Plan — the nesting case, joined by `parent_dispatch_id`),
`intent`, `started`/`closed` with a typed **`exit_reason`** (`success |
loop_cap_reached | reviewer_rejected_twice | dissent_irreconcilable | user_abort |
unrecoverable_error`).

### Level 2 — `wave` (the highest-value governance level)

`lane`, `mode`, `intent`, the typed edges (`consumes` / `reviews` / `reopens`),
`n_reviewers`, `dissent_count`, `verdict` (`pass | flag | block`). This level answers
the governance question that today's single-level log cannot — *"did ≥2 reviewers run,
and was there dissent?"* — which is why it is the highest-value addition.

### Level 3 — `agent` / Stage Worker — adopt Craft's **Stage Receipt** verbatim

The `agent.closed` row **is** a Craft Stage Receipt
(`CRAFT-REFINE-RUNTIME-STRATEGY.md` worker-return YAML). Reuse its fields exactly:

```yaml
stage_id            # the agent/stage id
result: pass | flag | block | timeout
artifact_path
files_touched: [ ... ]
validation: [ ... ]
blockers: [ ... ]
handoff_note
```

…**plus** what the agent *received* (the initialization that vanishes today —
domainspec's audit found the rendered prompt is persisted nowhere):

```yaml
briefing   # full text the agent received — DECISION: stored verbatim (open knob: sidecar file if rows get large)
angle      # the assigned sub-goal
inputs: [ ... ]
model      # model assigned by the orchestrator
sources:   # REQUIRED for external-research agents; [] otherwise
  - { cite: "...", kind: paper|url|doc|repo-file, status: verified|reading|unread|refutes }
```

### Logging rule — **log what would otherwise vanish**

- A **reviewer's verdict** and an **explorer's source list** vanish from chat once the
  dispatch closes → they get full rows.
- A **frontmatter / edges normalizer** makes a real semantic judgment, but that
  judgment **materializes in the versioned artifact** (the edges land in the file,
  diffable in git) → it is self-recording → it earns only a lightweight
  **`normalizers_applied`** mark on the *caller's* row, **no forensic row of its own.**
  The test is durability of the output, not whether a judgment occurred.

### Two more contracts

- **Per-agent prose record is conditional on `intent`.** The ≤200-word prose file is
  written **only when the agent's reasoning *is* the product** (research, decision).
  For a code/doc edit the deliverable is the diff and `prose_file` is null. Structured
  provenance always lives in the Stage Receipt regardless, so no fact is written twice.
- **Mandatory emit gate.** Every dispatch MUST emit `dispatch.started` +
  `dispatch.closed`. A dispatch that emits nothing **did not happen** as far as
  monitoring is concerned and an audit flags it. This is the construct that closes the
  "ungoverned channel" failure (the discovery counts 32 multi-agent folders that ran
  emitting nothing). The *enforcement mechanism* — a thin wrapper/hook so emission is
  structural, not author-discipline — is the discovery's OQ-3.

---

## 9. What maps to what (the crosswalk, one place)

| This design | Craft term (verbatim) | Source anchor |
| --- | --- | --- |
| dispatch | Plan / run | `CRAFT-INITIAL-DEFINITION.md#plan` |
| Wave (= discovery `layer`) | Wave | `Plan → Waves → Tasks → SWUs` |
| agent | Stage Worker / bounded worker | `CRAFT-REFINE-RUNTIME-STRATEGY.md` |
| `agent.closed` row | Stage Receipt (worker-return YAML) | `CRAFT-REFINE-RUNTIME-STRATEGY.md` |
| Wave `lane` | Operational Lane | `CRAFT-LEDGER-TYPE-SYSTEM.md#operational-lanes` |
| reviewers per Wave | `secondary_lanes` (validator/auditor) | `CRAFT-LEDGER-TYPE-SYSTEM.md` rule 10 |
| verdict | `pass \| flag \| block` | gate result / `receipt_status` |
| `consumes` edge | `dependency` | `dependency_*` types |
| `reviews` edge | review Wave over an artifact | lane `validator`/`auditor` |
| `reopens` edge | `residue_opened` + `recomposition` | `route_event_type` enum |
| handoff to a Wave | Route Handoff | `CRAFT-INTERACTION-LEDGER-SCHEMA.yml` |
| an ordered log entry | Route Event | `CRAFT-INTERACTION-LEDGER-SCHEMA.yml` |
| `intent` axis | Define → Design → Plan → Execute → Validate → Reflect | Craft Cycle |
| orchestrator | a context, not a worker | `CRAFT-REFINE-RUNTIME-STRATEGY.md` |

---

## 10. Intentional divergences from Craft (visible, not smuggled)

Three places where this design knowingly departs from `development/craft/`. Each is a
choice with a reason, not an oversight:

1. **Research is a first-class step *after* Define.** Craft folds research into Define
   as an input. We split it out and place it between Define and Design — you cannot
   research what you have not yet defined; Define produces the unknowns, Research
   resolves them. (§7.)
2. **Reviewers are a per-Wave default, not deferred.** Craft models role mapping and
   delegation as `deferred` (`CRAFT-LEDGER-TYPE-SYSTEM.md` role-mapping is "modeled now
   but automation is deferred"). We turn on the `secondary_lanes` review requirement as
   an **active default** — validator/auditor on every durable-artifact Wave, tier-aware
   — rather than waiting for the deferred automation. We use Craft's own
   `secondary_lanes` mechanism to do it, so the divergence is in *when it fires*, not in
   the vocabulary.
3. **Lane-on-Wave + Role-on-agent split.** Craft has Operational Lanes but no separate
   epistemic-role axis on the worker. We add the `role` axis on the Stage Worker and
   keep the Lane axis on the Wave. New vocabulary (`explorer | skeptic | writer |
   reviewer | implementer`) is introduced *only* here, only because Craft has no term
   for the worker's epistemic function — everything else reuses a Craft word.

---

## 11. Known risks and open questions (said plainly, not papered over)

- **`loop_cap` default is a guess.** Proposed 1; no usage data behind it. (§3.)
- **Synthesizer bias bottleneck.** Mechanical-handoff framing is safe only while
  synthesis stays mechanical; genuine N-Wave synthesis must be made reviewable. (§6.)
- **Lanes-vs-roles will be under pressure to collapse.** The common case
  (`validator` lane + `reviewer` role co-occurring) invites merging them into one
  field; that merge is the regression to watch for. (§5.)
- **`intent` and `topology`/`mode` value-enums stay `provisional`** in the
  observability contract until the domainspec vocabulary-unification work closes — the
  *structure* is frozen, the *values* are not. Freezing the values now would coin yet
  another parallel vocabulary, the exact disease this whole line of work is ending.
- **`briefing` stored verbatim** buys perfect reproducibility at the cost of row size;
  the fallback (a sidecar file referenced by path) is the knob if rows get large, not a
  revert to params-only.

---

## Three sharpest questions, in order

1. **`loop_cap` — default 1, or 2?** (Decides how many recomposition attempts a
   blocked Wave gets before a typed exit.)
2. **Does the lane-on-Wave / role-on-agent split survive contact with implementation,
   or does it collapse to one field in practice?**
3. **Where does the emit gate get enforced** — a parent-skill wrapper, a hook, or an
   audit-only check — so that "every dispatch emits started+closed" is structural and
   not author-discipline?

— V.
