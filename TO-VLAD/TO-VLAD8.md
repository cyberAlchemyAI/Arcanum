---
to: Vlad
from: Victor (subagent dispatch-governance model, synthesized)
re: "A methodology to govern domainspec-theorem's USER-INITIATED subagent dispatches — the composition model (Dispatch/Wave/Layer/Agent + typed DAG connections), strategy-as-typed-object, the mode-conflation finding, and how all of it maps onto Arcanum's dispatch-spec"
date: 2026-06-11
audit-against: "Arcanum: .claude/skills/{dispatch-spec,robot-talks,refine,spellcraft}/SKILL.md, development/craft/SKILL.md + …/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-DISPATCH.json. domainspec: vault/constitution/{domainspec-subagents-strategy-constitution.md@0.3.0, research-constitution.md}, internal_tools/subagents-dispatch-hooks/ (README + register-dispatch SKILL + hooks)"
status: draft for discussion — design handoff
---

# To Vlad — governing the repo's user-initiated subagent dispatches, and where it meets dispatch-spec

Eighth pass. The prior seven argued about individual Arcanum objects in their own
neighbourhoods. This one steps up a level: it is a **methodology argument** for how
domainspec-theorem should govern the subagents a *user* fires by hand, and it ends in a
single decision that only you should make — because the honest finding is that you and I
are building the **same dispatch-governance system twice**, and the redundancy is the real
cost.

I have verified every claim below against files on disk. Where my own brief was wrong or
loose, I say so inline (sections 1, 3, and 5 each carry a correction).

## 1. Scope split — "govern the subagents" is two subjects, not one

The first thing to refuse is the framing "let's govern the repo's subagents" as one task.
It is two, and they share a library but nothing else load-bearing:

| | (A) **Dispatch** | (B) **Automation** |
|---|---|---|
| Trigger | user-initiated, here-and-now | event / schedule |
| Lifetime | bounded — spawn → join → close | recurring / reactive |
| Carries | a task | cross-firing **state**: idempotency, debounce, retry, drift |
| Graded on | coverage / fidelity / independence | reliability / false-trigger-rate / drift |
| Registry shape | one row per dispatch | one row per *rule*, plus a fire-history |

They **share** the composition library — the same Wave/Layer/Agent vocabulary, the same
typed connections, the same role catalogue. They **differ** in lifecycle and in what a
grade even means. domainspec's existing machinery is already squarely an (A) system: the
strategy constitution's whole lifecycle (R3, seven steps, spawn-confirm-collect-close) and
the dispatch ledger (`subagents-dispatch.yaml`, "one row per dispatch") are dispatch-shaped,
not automation-shaped (`internal_tools/subagents-dispatch-hooks/README.md`, the format
block; `…/domainspec-subagents-strategy-constitution.md` R3).

**This handoff is about (A) only.** (B) — recurring/reactive automation — is deferred. I
flag it because the instinct to "just add cron/event triggers to the same spec" is exactly
the conflation that produces an ungovernable object: a reliability concern wearing a
coverage grade.

## 2. The composition model for (A) — four levels plus typed connections

```text
Dispatch
└── Wave            (a functional band: "explore", "review", "synthesize")
    └── Layer       (one group/pass inside a wave — a wave can STACK several)
        └── Agent   (one spawned subagent, one role, one angle)

   …with first-class, typed CONNECTIONS between layers/waves → a DAG
```

The non-obvious level is **Layer-inside-Wave**. A review wave is not one pass — it is, e.g.,
three review layers (a correctness layer, a security layer, a style layer) that all sit in
the same functional band but are distinct passes with distinct rosters. Collapsing wave and
layer loses exactly that "several passes, one purpose" structure. domainspec already has the
Layer primitive (`…strategy-constitution.md` R25 spec: `layers[]` with `layer_id`, `role`,
`mode`, `n`, `parallel`, `agents[]`) — what it lacks is the **Wave** band above it. Arcanum
has neither name (it has flat `steps[]`; see section 5).

### The deliberate amendment: connections form a DAG, not a line

This is the one place the model **breaks** current domainspec law, and I want it explicit
rather than smuggled in. Base rule **R30** mandates **linear** composition: *"Composition
is linear: layer N runs after layer N−1. There is no DAG and no `depends_on:` field on
agents."* R30 is what **closed** `OQ-mixed-dag-schema` (`…strategy-constitution.md` §13
Resolved; R30 text).

Promoting connections to a typed DAG **reopens `OQ-mixed-dag-schema`**. That is a real
amendment with a real cost — R30's linearity is load-bearing for the lifecycle-is-linear
premise (P-SS-9). I am not hand-waving it as "obviously better." The case for reopening:
the moment a synthesize layer needs inputs from *two* non-adjacent upstream layers (the
normal shape of explorer→writer with a skeptic branch alongside), linear N−1 sequencing
either forces a false ordering or smuggles the real edge into prose. The DAG makes the edge
typed and checkable. **Decision for you to weigh, not a fait accompli** — see section 6.

## 3. Strategy = a typed object = (distinct role-set + distinct grading criterion)

A "strategy" is not a mode and not a workflow. It is the pair **(role-set, grader)**. Two
dispatches are the *same strategy* iff they draw from the same role-set and are graded on
the same criterion. This is the level Arcanum never names (section 5).

| Strategy | Role-set | Graded on | Status |
|---|---|---|---|
| `research` | explorer · skeptic · writer · auditor | coverage from angle; **claim ≤ proof**; schema/citation fidelity | **real today** |
| `code` | implementer · reviewer · tester | correctness; tests pass | **forecast, not yet real** |
| `review` | (auditors of an existing artifact) | defects found | honest candidate |
| `plan` | (decide-before-build roles) | decision quality | honest candidate |
| `refine` | discovery → design → plan loop | (Arcanum's canonical 10-stage) | Arcanum-suggested 5th |

**Correction to my own brief:** I listed `code` as "real today" alongside `research`. On
disk it is *not*. `research` is fully real — `research-constitution.md` names the four
roles (R4–R8: explorer graded on coverage R5, writer on schema/citation fidelity R7,
auditor on role-coverage/dissent R8) and the claim≤proof discipline is the corpus closure
mark. `code`, by contrast, lives only as **OQ-code-category**: *"when `category: code` is
unlocked … do the four roles stay the same? Likely yes for skeptic|auditor; explorer|writer
may split into coder|reviewer"* (`research-constitution.md` OQ list). So `code` is a
forecast of a split, not an installed role-set. The table above is corrected accordingly —
this matters because over-claiming `code` as built would itself violate the repo's own
claim≤proof rule, which would be an embarrassing place to break it.

`refine` is the genuinely new shape Arcanum contributes: a discovery→design→plan **loop**
(`refine/SKILL.md` `<canonical-loop>`, ten stages: context → define → review → research-
decision → distill → design → design-review → repair → plan → final-synthesis). It is a
strategy in our sense — a fixed role-set with its own grader (stage-receipt completeness) —
that domainspec has no equivalent of.

## 4. The sharp finding — "mode" is jamming five categories into one enum

Both systems have a field called `mode`, and **both overload it**. This is the load-bearing
analytical result of the pass.

- domainspec R19 enum: `single | task-fan-out | robot-talks | sequential | ping-pong |
  pipeline` (`…strategy-constitution.md` R19).
- Arcanum dispatch-spec step `pattern` enum: `route | sequential | fanout | dialectic |
  tournament | distill | xray | decision | validation | toy_game | synthesis | handoff`
  (`dispatch-spec/SKILL.md` Validation Rule 3 — note: the actual on-disk enum includes
  `xray` and `toy_game`, which my brief's list dropped).

Lay the two enums side by side and they are not lists of peers. They are **five different
categories wearing one field name**:

| Real category | Examples currently mislabelled "mode" | Where it belongs in our model |
|---|---|---|
| **Cardinality** | `single`, `task-fan-out` / `fanout` | **Layer** property |
| **Interaction pattern** | `robot-talks`, `dialectic`, `tournament`, `ping-pong` | **Layer** property |
| **Topology / connection** | `sequential`, `route`, `pipeline`, (zig-zag) | **Connection** (the DAG edge) |
| **Function** | `distill`, `synthesis`, `validation`, `decision` | **Role** (not a mode at all) |
| **Technique / overlay** | pareto, x-ray, memory-loop, recomposition | **Overlay** (orthogonal to all) |

The clean factoring:

```text
Layer       carries  →  cardinality + interaction-pattern
Connection  carries  →  topology
Role        carries  →  function
Overlay     is        →  orthogonal, attaches anywhere
```

That `function` words like `distill`/`synthesis`/`validation` sit in a *mode* enum is the
tell: those are **roles** — what an agent is *for* — masquerading as a *how-they-compose*.
Arcanum half-knows this: its `subagent_strategy.roles[]` exists separately
(`dispatch-spec/SKILL.md` Subagent Strategy), yet `synthesis`/`distill`/`validation` *also*
appear in the `pattern` enum. Two homes for one concept.

**The 1:1 that proves the category is real.** Arcanum's `robot-talks` sigil *is*
domainspec's `robot-talks` mode — same multi-agent parallel-investigation-for-tensions
pattern, decompose-by-concern, human-gate, session-preserve (`robot-talks/SKILL.md` whole
body ≈ `…strategy-constitution.md` R20 + robot-talks-constitution). The same named thing
shows up as a *sigil* in one system and a *mode value* in the other. That is direct
evidence that **"interaction pattern" is its own category** — not a peer of `single`
(cardinality) and not a peer of `sequential` (topology). A taxonomy where `robot-talks` and
`single` are sibling enum values is a taxonomy that has flattened three axes into one.

## 5. Arcanum ↔ our model — near-isomorphic, with a clean maturity split

The two systems are close enough to align almost element-for-element:

| Our model | Arcanum dispatch-spec | Anchor |
|---|---|---|
| Dispatch | `dispatch` (`dispatch_id`, `intent`, `gates`) | `dispatch-spec/SKILL.md` Rule 1 |
| Layer | `step` | `dispatch-spec/SKILL.md` `steps[]` |
| Connection (typed edge) | typed input source: `frame`/`handle`/`decision`/`ledger` | Rule 4 ("non-first steps must name an input source") |
| Mode | step `pattern` | Rule 3 |
| Gate | `gates[]` | Rule 1, Output Contract |
| Trigger | technique-overlay `trigger` | Rule 12; REFINE-DISPATCH `technique_overlays[].trigger` |

**Arcanum is more mature on four things we lack:**

1. **Technique-overlay catalog.** A named, triggered, step-scoped overlay library —
   `baseline_sequence`, `dialectic_for_tension`, `tournament_for_alternatives`,
   `xray_for_hidden_structure`, `toy_game_for_low_cost_falsification`,
   `memory_residue_for_context_recovery`, `protected_context_for_external_…`
   (`refine/SKILL.md` `<technique-overlay-policy>`; instantiated concretely in
   `REFINE-DISPATCH.json` `technique_overlays[]`, each with `trigger` + `applies_to_steps`
   + `validation_expectation`). This is exactly our **Overlay** axis, already built.
2. **Subagent-lifecycle closeout.** A ledger that *proves every spawned agent reached a
   terminal join and terminal close* — `status=pass` is invalid while any agent is
   unjoined/unclosed; blocked/timed-out spawns only pass as *named residue with a reroute*
   (`dispatch-spec/SKILL.md` Rules 23–25, `<Subagent Lifecycle>`). domainspec has R31
   exit-reasons per dispatch, but **no per-agent join/close proof** — a real AFK-safety gap.
3. **Human-permission gate before spawning.** `authorization=requires_user_permission`
   until the operator approves; the orchestrator must *show the strategy and ask* before any
   delegated spawn (`dispatch-spec/SKILL.md` Rule 22; `refine/SKILL.md`
   `<strategy-preview-and-permission>`). domainspec has this too (R6a confirm gate) — call
   it a tie, slightly sharper on the Arcanum side.
4. **Boundary / owner accounting.** `boundary_evidence`, owner-boundary checks, promotion
   guardrails ("execution evidence must not promote Inventory/Ontology/glossary/sigil/spell"
   — Rules 9, 20; `REFINE-DISPATCH.json` `g05-owner-boundary`).

**We are more mature on two things Arcanum lacks:**

1. **The explicit Wave band.** domainspec has the Layer (R25 `layers[]`); the Wave
   (functional band stacking several layers) is a level above what Arcanum's flat `steps[]`
   expresses. Neither has Wave *named* yet, but our Layer model is the closer base to build
   it on.
2. **Strategy as a typed object.** Arcanum **diffuses roles across per-step overlays** and
   **never names a dispatch-wide strategy**. Its `subagent_strategy` block describes *this
   run's* roles/parallelism/join (`dispatch-spec/SKILL.md` `<Subagent Strategy>`), but there
   is no notion of `research` vs `code` vs `refine` as reusable typed (role-set, grader)
   objects. domainspec's `research-constitution.md` *is* exactly that: a named strategy with
   a fixed role-set and a fixed grader. That is the one genuinely structural thing we have
   that Arcanum doesn't.

**Correction to my brief:** I should not call `refine` purely an Arcanum *overlay* — it is
Arcanum's closest thing to a *named strategy* (a fixed 10-stage role-set with its own
grader). So the "Arcanum never names a strategy" claim has one near-exception: `refine` is a
strategy in all but the explicit (role-set, grader) typing. I keep the claim but note the
edge.

## 6. The decision for you

domainspec and Arcanum are building **near-isomorphic dispatch-governance systems**
(section 5's table is element-for-element). Maintaining both is the actual redundancy — not
any single missing feature. Two specs, two validators, two overlay vocabularies, two
lifecycle ledgers, drifting independently, is the cost.

The recommendation I'd defend:

- **Pick a canonical source.** On the evidence, Arcanum's `dispatch-spec` is the more
  complete *substrate* (overlay catalog + lifecycle proof + boundary accounting are all
  built and validated).
- **Align domainspec's model onto it** — Dispatch=dispatch, Layer=step, Connection=typed
  input edge, Overlay=technique-overlay.
- **Add the two things Arcanum lacks**: the **Wave** band, and **strategy-as-typed-object**
  (`research`/`code`/`review`/`plan`/`refine` as reusable (role-set, grader) pairs).
- **Decide the DAG question explicitly** (section 2): adopting typed connections reopens
  `OQ-mixed-dag-schema`, which R30 deliberately closed in favour of linear composition.
  Arcanum's `steps[]` + typed input sources already lean DAG-ward (a step names *which*
  upstream frame/handle/ledger it consumes — that is an edge, not a line). So aligning to
  Arcanum *de facto* reopens the question regardless. Better to reopen it on purpose.

I am not deciding this for you because it is a genuine cross-repo ownership call with a real
trade (one canonical spec + migration cost, vs. two specs kept deliberately separate with a
sync discipline). That is your weigh, not mine.

## 7. What is already built (so you know the state, not just the design)

The (A)-side ledger is live and global, independent of which spec wins:

| Artifact | What it is | Path |
|---|---|---|
| `subagents-dispatch.yaml` | the governance **ledger** — one row per dispatch; `agents` is a JSON column carrying each agent's `angle`; `anti_bias` carries the `{axis, pairs}` tension | `<repo-root>/subagents-dispatch.yaml` (written by the skill) |
| `register-dispatch` | the **skill** that authors a row (deterministic appender, idempotent on `dispatch_id`, UTF-8 file arg so PowerShell's UTF-16 pipes can't corrupt it) | `internal_tools/subagents-dispatch-hooks/skills/register-dispatch/` |
| `remind-register-dispatch.cjs` | PreToolUse·`Agent` hook — *reminds* the model to register (can't author angle/anti_bias itself, so it nudges, doesn't write) | `…/hooks/remind-register-dispatch.cjs` |
| `block-workflow.cjs` | PreToolUse·`Workflow` hook — denies the `Workflow` tool; repo mandates `Agent`/`research` instead | `…/hooks/block-workflow.cjs` |

Installed **globally per user** (`~/.claude/settings.json` + `~/.claude/skills/`), so it
applies to every repo including ones created later; `install.cjs` reproduces it on any
machine, zero runtime deps, fail-open
(`internal_tools/subagents-dispatch-hooks/README.md`, Design properties). This ledger is the
governance layer — deliberately distinct from the research skill's per-folder `dispatch.yaml`
*roster* and from `agents-telemetry/` SQLite *usage measurement* (README, "Why a skill").
Note the honest caveat already on record: population depends on the model invoking the skill;
the hook nudges but cannot enforce (README, Caveats).

---

## The one decision

**Do we collapse domainspec's dispatch governance onto Arcanum's `dispatch-spec` as the
single canonical substrate — adopting its overlay catalog, per-agent lifecycle-close proof,
and boundary accounting — and then add the only two things Arcanum lacks (the Wave band and
strategy-as-typed-object), accepting that this reopens `OQ-mixed-dag-schema` (R30's linear-
composition closure) in favour of a typed connection DAG?**

Yes → one spec, one validator, one overlay vocabulary; domainspec contributes Wave +
strategy-typing upstream; I open the R30 amendment.
No → we keep two near-isomorphic systems and owe a written sync discipline so they don't
drift — which is the cost I'd want us to name out loud rather than absorb silently.

— V.
