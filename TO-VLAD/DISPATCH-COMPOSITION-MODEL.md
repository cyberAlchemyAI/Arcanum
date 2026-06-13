---
to: Vlad & Victor
from: consolidated (TO-VLAD6 + TO-VLAD8 + on-subject slice of TO-VLAD7)
re: the converged dispatch-composition model
date: 2026-06-13
status: consolidated — supersedes TO-VLAD6, TO-VLAD8, on-subject slice of TO-VLAD7
---

# The Dispatch-Composition Model

> This document **supersedes** TO-VLAD6 (per-Wave model, 2026-06-08), TO-VLAD8
> (Dispatch/Wave/Layer/Agent + dispatch-spec crosswalk, 2026-06-11), and the
> composition slice of TO-VLAD7 (2026-06-10) as the current reading of the model.
> Those three memos stay **frozen** as the provenance behind this one — do not edit,
> delete, or revive demoted claims from them. Where a claim was killed in a memo, it
> does not return here.

## 0. What this consolidates, and why

The prior memos converged on one object from three angles, and the angles had begun to
disagree in their margins. This document fixes the convergence so there is a single
current statement to build against.

It **consolidates TO-VLAD6** (which owns the typed-edge vocabulary, the verdict
alphabet, the three observability levels, and the lanes-vs-roles split) **plus TO-VLAD8**
(which owns the four-level ontology, strategy-as-typed-object, the mode-conflation
finding, and the dispatch-spec crosswalk) **plus the composition slice of TO-VLAD7**
(the discovery pipeline read as one more instance of the same split-and-compose move).

The relationship between 6 and 8 is **v1 → v2 of the same ontology**: 6 collapsed Wave
and Layer into a single per-Wave unit; 8 split them and reconciled with domainspec's
pre-existing `Layer` primitive (constitution R25). **8 is the newer and correct reading
where they diverge** — this document uses 8's four-level shape and notes where 6 was
coarser. From TO-VLAD7 only the composition observation enters (§11), bounded to one
section; everything else in 7 (x-ray rendering, visual lanes, the research→x-ray spell)
stays out — see §10.

Subset rule throughout: every claim here stands on plain engineering merit. Framework
vocabulary appears only where it predicts something the engineering-only reading would
miss. Prior art is cited in the body, not rediscovered.

## 1. The ontology — Dispatch / Wave / Layer / Agent

A user-initiated subagent dispatch is a four-level object with typed connections between
the middle levels forming a DAG:

```text
Dispatch
└── Wave            (a functional band: "explore", "review", "synthesize"; carries intent)
    └── Layer       (one group/pass inside a wave — a wave can STACK several;
                     carries mode = cardinality + interaction-pattern, role, n, parallel)
        └── Agent   (one spawned subagent, one role, one angle)

   …with first-class, typed CONNECTIONS between layers/waves → a DAG
```

The load-bearing distinction is **Layer-inside-Wave** (TO-VLAD8 §2). A review wave is
not one pass — it can be three review layers (correctness, security, style) sitting in
one functional band but with distinct rosters. Collapsing wave and layer loses exactly
that "several passes, one purpose" structure.

TO-VLAD6 collapsed these two into a single per-Wave unit (TO-VLAD6 §1: "Wave = the
discovery's `layer`"). That was the coarser v1 reading. 8 separates them and grounds the
Layer level in the primitive domainspec already has — `layers[]` with `layer_id`, `role`,
`mode`, `n`, `parallel`, `agents[]` (constitution R25, cited TO-VLAD8 §2). The **Wave**
band — the functional grouping that stacks several layers — is the level domainspec lacks
a name for and the one this model contributes upstream.

Maturity: the Layer primitive is **operant** in the domainspec constitution. The Wave
band is **draft** — named here, not yet installed as a field.

## 2. Typed connections and the single bounded cycle

The relationship between two layers/waves is a **typed edge**, not a free-text
`reacts_to`. TO-VLAD6 owns this vocabulary (TO-VLAD6 §2). Three edge types:

| Edge | Meaning | Cycle? |
|---|---|---|
| `consumes` | B uses A's output as input — forward data dependency. | no (DAG) |
| `reviews` | B is a review **of** target A. | no (DAG) |
| `reopens` | the cyclic back-edge: a `block` verdict from a review reactivates the wave it reviewed. | **yes — the only cycle** |

`reopens` is the sole source of cycles; everything else is a DAG (TO-VLAD6 §2–3). The
cycle is **bounded**, not open:

1. A review wave (lane `validator`) emits `block` on the wave it `reviews`.
2. That `block` creates a `reopens` edge back to the reviewed wave.
3. The reviewed wave re-runs.
4. The loop is bounded by a `loop_cap` budget.
5. If still `block` after the cap, the dispatch **closes** with a typed exit reason —
   `reviewer_rejected_twice` or `loop_cap_reached` — never an open-ended retry
   (TO-VLAD6 §3).

The old global topology enums (`sequential | zig-zag | parallel | pipeline`) **dissolve**:
each is now an emergent property of the edge set, not a label chosen up front (TO-VLAD6
§1). `sequential` = a wave that `consumes` a prior one; `parallel` = two waves with no
edge; the reactive/feedback shape = a `reopens` edge exists; `pipeline` = a chain of waves
with differing modes. If you feel the need to write the global label down, the edge set is
underspecified — record the edges; the topology is a query result.

These edges map onto Arcanum's typed input sources — `frame` / `handle` / `decision` /
`ledger` (and `human_answer` / `external_context`) (dispatch-spec Rule 4: "non-first steps
must name at least one input source").
A step that names which upstream frame/handle/ledger it consumes *is* an edge, not a line.

`loop_cap` default is an **open knob** (TO-VLAD6 §3 proposed 1, on the reasoning that a
reviewer who blocks the same artifact twice is signalling a definition/design problem one
altitude up, not an execution problem the same wave can fix; no usage data defends 1 over
2). The *mechanism* — bounded, typed exit — is the load-bearing part; the *value* is not
settled.

## 3. Strategy as a typed object

A strategy is not a mode and not a workflow. It is the pair **(role-set, grader)**
(TO-VLAD8 §3). Two dispatches are the *same strategy* iff they draw from the same role-set
and are graded on the same criterion.

| Strategy | Role-set | Graded on | Status |
|---|---|---|---|
| `research` | explorer · skeptic · writer · auditor | coverage from angle; **claim ≤ proof**; schema/citation fidelity | **real today** |
| `review` | auditors of an existing artifact | defects found | honest candidate |
| `plan` | decide-before-build roles | decision quality | honest candidate |
| `code` | implementer · reviewer · tester | correctness; tests pass | **FORECAST — not real** |
| `refine` | discovery → design → plan loop (10 stages) | stage-receipt completeness | Arcanum's contribution / near-strategy |

`research` is the one **fully real** strategy on disk — in **domainspec**, not Arcanum:
`domainspec/vault/constitution/research-constitution.md` names the four roles (R4–R8: explorer
graded on coverage R5, writer on schema/citation fidelity R7, auditor on role-coverage/dissent
R8), and claim≤proof is the corpus closure mark. Arcanum has no equivalent named (role-set,
grader) — which is exactly the asymmetry §8 rests on.

`code` is marked **forecast, not real**, and the reason matters: TO-VLAD8 corrected its own
brief here (TO-VLAD8 §3, "Correction to my own brief"). On disk, `code` lives only as
`OQ-code-category` — a forecast that explorer|writer *may* split into coder|reviewer — not
an installed role-set. Over-claiming `code` as built would itself violate the repo's
claim≤proof rule, which would be an embarrassing place to break it. So it stays forecast.

`refine` is the genuinely new shape Arcanum contributes: a discovery→design→plan **loop**
(`refine/SKILL.md` `<canonical-loop>`, ten stages) with its own grader (stage-receipt
completeness). It is a strategy in all but the explicit (role-set, grader) typing — a
near-strategy, not a pure overlay (TO-VLAD8 §5 correction).

## 4. The mode-conflation finding

Both systems have a field called `mode`, and both **overload it**. This is the load-bearing
analytical result of the work (TO-VLAD8 §4).

- domainspec R19 enum: `single | task-fan-out | robot-talks | sequential | ping-pong |
  pipeline`.
- Arcanum dispatch-spec step `pattern` enum: `route | sequential | fanout | dialectic |
  tournament | distill | xray | decision | validation | toy_game | synthesis | handoff`
  (dispatch-spec Rule 3, verified on-disk including `xray` and `toy_game`).

Laid side by side these are not lists of peers — they are **five categories wearing one
field name**. The clean factoring:

```text
Layer       carries  →  cardinality + interaction-pattern
Connection  carries  →  topology
Role        carries  →  function
Overlay     is        →  orthogonal, attaches anywhere
```

| Real category | Mislabelled "mode" examples | Belongs on |
|---|---|---|
| **Cardinality** | `single`, `task-fan-out` / `fanout` | **Layer** |
| **Interaction pattern** | `robot-talks`, `dialectic`, `tournament`, `zig-zag` | **Layer** |
| **Topology** | `sequential`, `route`, `pipeline` | **Connection** (the DAG edge) |
| **Function** | `distill`, `synthesis`, `validation`, `decision` | **Role** — not a mode at all |
| **Overlay** | pareto, x-ray, memory-loop, recomposition | **Overlay** — orthogonal to all |

That `function` words like `distill`/`synthesis`/`validation` sit in a *mode* enum is the
tell: those are **roles** — what an agent is *for* — masquerading as how-they-compose.
Arcanum half-knows this: `subagent_strategy.roles[]` exists separately, yet
`synthesis`/`distill`/`validation` *also* appear in the `pattern` enum — two homes for one
concept.

**The 1:1 that proves the category is real.** Arcanum's `robot-talks` sigil *is*
domainspec's `robot-talks` mode — the same multi-agent parallel-investigation-for-tensions
pattern, decompose-by-concern, human-gate, session-preserve (`robot-talks/SKILL.md` ≈
constitution R20). The same named thing is a *sigil* in one system and a *mode value* in
the other. That is direct evidence that "interaction pattern" is its own category — not a
peer of `single` (cardinality) and not a peer of `sequential` (topology). A taxonomy where
`robot-talks` and `single` are sibling enum values has flattened three axes into one.

(Killed: `mode` as a coherent single axis. It is not one — do not restore it as one field.)

## 5. Lanes vs Roles; orchestrator and synthesizer as parent functions

Two vocabularies that look like competitors do not compete, because they live on
**different objects** (TO-VLAD6 §5). Keep **both**, at different levels:

- **Operational Lane** is a property of the **Wave**:
  `validator | auditor | qa | tech | business | …`. It names the
  **accountability / expertise domain** of that wave.
- **Role** is a property of the **Agent**:
  `explorer | skeptic | writer | reviewer | implementer`. It names the **epistemic
  function** — what that worker *does*.

Worked instance: a review wave has **lane `validator`**; the agents inside it have
**role `reviewer`**. They cross — a `tech` wave can contain a `skeptic` role; a `validator`
wave contains `reviewer` roles. The regression to watch for is a single field trying to
carry both (TO-VLAD6 §5 open risk). "Reviewer" is **one role**, parameterized as
`reviewer(check = content | format | both)` — content-review and format-review are *checks*,
not separate roles. (Killed: `format-reviewer` / `content-reviewer` as separate roles.)

The policy that *generates* L2's `n_reviewers` (§7): every work wave that produces a
**durable artifact** declares `validator`/`auditor` as secondary lanes and is reviewed by
**≥2** reviewers; ephemeral lookups take 0–1. Review is tier-aware and an **active default**,
not a deferred nicety (TO-VLAD6 §5, §10) — without this rule, L2's `n_reviewers` column has no
policy producing it.

**Orchestrator and Synthesizer are functions of the parent skill, not child agents**
(TO-VLAD6 §6):

- **Orchestrator** = the runtime coordinator that orders how waves initialize — the parent
  skill's job. Craft is explicit that "the orchestrator is a context," not a worker.
  Spawning it as a child **doubles the control flow and duplicates ownership** of the
  dispatch — exactly the recursion that timed out in `CRAFT-REFINE-001/002`. Do not do it.
- **Synthesizer** = collecting final outputs and handing them up to the parent — a
  mechanical handoff, not a deep-synthesis child agent.

(Killed: orchestrator/synthesizer as child agents.)

Honest flag carried forward: the mechanical-handoff framing for the synthesizer holds
*only while synthesis is mechanical*. The moment it becomes genuine N-wave synthesis (one
reader collapsing many tensioned waves into one narrative), it is the **single-synthesizer
bias bottleneck** — a lone un-tensioned reader can quietly collapse a tensioned layer back
to one viewpoint. At that point the synthesizer must itself become a wave with its own
`reviews` edge. Mark the transition; do not let it happen silently.

## 6. Verdict vocabulary

The universal wave/review verdict is **`pass | flag | block`** (TO-VLAD6 §4):

- `pass` — clean.
- `flag` — soft concern; surfaced, does not stop the dispatch.
- `block` — hard stop; triggers the `reopens` edge.

(Killed: `pass | fail | mixed`. `flag` carries the soft-concern signal `mixed` was clumsily
standing in for; `block` is the hard stop that fires `reopens`.)

## 7. Observability and per-stage logging

Three nesting levels, all **flat append-only JSONL rows joined by FK** (`dispatch_id` /
`wave_id` / `agent_id`) — not nested objects (TO-VLAD6 §8). Each of `dispatch` and `agent`
emits `started` + `closed`, so a crash leaves a visible `started`-without-`closed`.

**L1 — `dispatch`.** `goal` (required), `output_root`, `dispatch_kind`
(`standard | meta`; **meta** = a wave whose worker is itself an orchestrator/sub-Plan, the
nesting case joined by `parent_dispatch_id`), `intent`, `started`/`closed` with a typed
`exit_reason` (`success | loop_cap_reached | reviewer_rejected_twice |
dissent_irreconcilable | user_abort | unrecoverable_error`).

**L2 — `wave`** (the highest-value governance level). `lane`, `mode`, `intent`, the typed
edges (`consumes` / `reviews` / `reopens`), `n_reviewers`, `dissent_count`, `verdict`
(`pass | flag | block`). This answers the governance question a single-level log cannot:
*did ≥2 reviewers run, and was there dissent?*

**L3 — `agent`** = a **Stage Receipt verbatim** plus what the agent *received*. The
receipt fields (`stage_id`, `result`, `artifact_path`, `files_touched`, `validation`,
`blockers`, `handoff_note`) come straight from Craft's worker-return YAML; the received
half (`briefing`, `angle`, `inputs`, `model`, `sources[]` with per-source
`status: verified|reading|unread|refutes`) captures the initialization that vanishes today
— the rendered prompt is persisted nowhere (TO-VLAD6 §8).

**Logging rule — log what would otherwise vanish.** A reviewer's verdict and an explorer's
source list disappear from chat once the dispatch closes → they get full rows. A
frontmatter/edges normalizer makes a real judgment, but it **materializes in the versioned
artifact** (the edges land in the file, diffable in git) → it is self-recording → it earns
only a lightweight `normalizers_applied` mark on the caller's row, no forensic row of its
own. The test is durability of the output, not whether a judgment occurred. The per-agent
prose record is itself conditional on `intent`: the ≤200-word reasoning file is written only
when the agent's *reasoning* is the product (research, decision); for a code/doc edit the
deliverable is the diff and `prose_file` is null (TO-VLAD6 §8).

**Mandatory emit gate.** Every dispatch MUST emit `dispatch.started` + `dispatch.closed`. A
dispatch that emits nothing **did not happen** as far as monitoring is concerned, and an
audit flags it. This closes the ungoverned-channel failure (the discovery counts 32
multi-agent folders that ran emitting nothing).

### Fusing the two halves — domainspec × Arcanum logging

*(This section is grounded in direct on-disk verification — `tools/arcanum`,
`evidence-index.json`, `sigil-invocations.jsonl`, `subagents-dispatch.yaml` — not in the three
source memos. It is new synthesis, flagged as such per the subset rule.)*

The two repos have **complementary, non-overlapping** logging strengths, and the model
adopts both:

- **Arcanum** has a per-stage **stage-row + schema-validated receipt indexed by
  `dispatch_id`** — *operant* via `tools/arcanum` (`refine_stage_receipt_is_valid`,
  `evidence-index.json`). But its central ledger (`sigil-invocations.jsonl`) holds only a
  **single bootstrap record in one proof folder — zero cross-run rows** — the per-stage
  discipline exists; the cross-run spine does not.
- **domainspec** has a central cross-run ledger that is **populated**
  (`subagents-dispatch.yaml`: a dispatch row + a close row per dispatch — *operant*). But
  it logs **per dispatch, not per stage** — the cross-run spine exists; the per-stage rows
  do not.

The model takes **(stage-row + schema-validated receipt per `dispatch_id`)** from Arcanum
and **(append-only cross-run queryable ledger)** from domainspec. These are not rival
designs; they are two halves of one logging contract, and neither repo has both today.

## 8. Crosswalk onto Arcanum's dispatch-spec

The two systems align almost element-for-element (TO-VLAD8 §5, verified against
`formulae/dispatch-spec/SKILL.md`):

| This model | Arcanum dispatch-spec | Anchor |
|---|---|---|
| Dispatch | `dispatch` (`dispatch_id`, `intent`, `gates`) | Rule 1 |
| Layer | `step` | `steps[]` |
| Connection (typed edge) | typed input source `frame`/`handle`/`decision`/`ledger` (+ `human_answer`/`external_context`) | Rule 4 |
| Mode | step `pattern` | Rule 3 |
| Gate | `gates[]` | Rule 1 / Output Contract |
| Overlay | technique-overlay | Rule 12 |

**Arcanum is more mature** on: the technique-overlay catalog (named, triggered, step-scoped
overlays — the Overlay axis, already built); subagent-lifecycle closeout (Rules 23–25 — a
ledger that proves every spawned agent reached terminal join + terminal close; blocked/
timed-out spawns pass only as named residue with a reroute — a per-agent AFK-safety proof
domainspec lacks); the human-permission gate before spawning (Rule 22); and boundary/owner
accounting (Rules 9, 20).

**This model is more mature** on: the explicit **Wave band** (Arcanum has flat `steps[]`,
no functional-band level above the step), and **strategy-as-typed-object** (Arcanum diffuses
roles across per-step overlays and never names a dispatch-wide reusable (role-set, grader);
domainspec's `research-constitution.md` *is* exactly that, and Arcanum has no counterpart).

## 9. The discovery pipeline as one more composition (the on-subject slice of TO-VLAD7)

This is the only part of TO-VLAD7 that enters, bounded to this section. TO-VLAD7's central
observation is that several subsystems are **the same move along different axes**: split an
opaque target into typed perspectives, hold an evidence/inference boundary, then compose
(TO-VLAD7 §1). The discovery pipeline `research → discovery agent → two-view split` is the
same split-and-compose shape this model formalizes — split by epistemic role, hold the
reference-status boundary, compose into a node.

The reusable piece for *this* model: **a research dispatch produces a graph with provenance
baked in** — L1 per-agent records, L2 ledger, L3 discovery, references-with-status, dissent
records, closure marks (TO-VLAD7 §4). That graph connects directly to the observe-model of
§7: the three logging levels are precisely the provenance a downstream consumer needs. The
research dispatch is not just a worker roster — its *output is a typed, provenance-bearing
graph*, which is why the L1/L2/L3 contract is load-bearing rather than bookkeeping.

Everything else in TO-VLAD7 stays out (§10).

## 10. What this model deliberately leaves out

For honesty about what was considered and cut:

- **The whole x-ray subsystem** — rendering, visual lanes, the two-view↔x-ray mapping, the
  research→x-ray "understand-then-show" spell. TO-VLAD7 itself rules x-ray a seed-status,
  unpromoted, optional *display surface* downstream of the governance chain — "not part of
  the governance chain — yet" (TO-VLAD7 §5). It is not a peer of the discovery machinery and
  has no place in this model's composition or governance core.
- **The automation axis (B).** TO-VLAD8 §1 split "govern the subagents" into two subjects:
  (A) **dispatch** — user-initiated, bounded, spawn→join→close, graded on coverage/fidelity;
  and (B) **automation** — event/schedule-triggered, recurring, carrying cross-firing state
  (idempotency, debounce, retry, drift), graded on reliability/false-trigger-rate. **This
  model is (A) only.** (B) is deferred — adding cron/event triggers to the same spec is the
  conflation that produces an ungovernable object: a reliability concern wearing a coverage
  grade. Not killed, deferred.
- **`code` as a real strategy** — forecast only (§3). It is in the table marked forecast so
  the shape is visible, not so it can be claimed as built.
- **The authoring intent-cycle.** The `intent` field rides on the L1/L2 logging rows (§7),
  but its *vocabulary* — the Define → Research → Design → Plan → Reflect authoring lifecycle,
  and TO-VLAD6's deliberate research-after-Define divergence from Craft (TO-VLAD6 §7, §10) — is
  **not enumerated or re-litigated here**. That cycle is the *authoring* lifecycle a dispatch
  serves; this model governs dispatch *composition*, which is orthogonal to it. Named, not
  dropped — it stays owned by TO-VLAD6 until a separate pass promotes it.
- **A single coherent `mode` axis** — there is none; `mode` jams five categories (§4).
- **The global topology enum chosen up front** — dissolved into the edge set (§2).

## 11. Open debts

Said plainly, not papered over:

- **`OQ-mixed-dag-schema` is reopened, not settled.** Promoting connections to a typed DAG
  breaks base rule **R30** ("Composition is linear: layer N runs after layer N−1. There is
  no DAG and no `depends_on:` field on agents"), which is what *closed* `OQ-mixed-dag-schema`
  in the first place (TO-VLAD8 §2). The case for reopening: the moment a synthesize layer
  needs inputs from two non-adjacent upstream layers, linear N−1 sequencing either forces a
  false ordering or smuggles the real edge into prose. Aligning to Arcanum's `steps[]` +
  typed input sources reopens it *de facto* regardless. This is a live amendment with a real
  cost (R30's linearity is load-bearing for the lifecycle-is-linear premise P-SS-9) — carried
  as **open debt**, not as a decided thing. (Killed: R30-linearity as settled.)
- **Arcanum's central ledger is effectively empty.** `sigil-invocations.jsonl` holds a single
  bootstrap record in one proof folder, no cross-run rows (§7). The
  per-stage receipt discipline is real and operant; the cross-run spine that would make it
  queryable across runs is not populated. The fusion in §7 is the design that closes this,
  but the closing is **work not yet done** — see §12 for the concrete wiring (the writer
  already exists; what is actually missing is a Claude hook surface and an envelope producer).
- **`loop_cap` default** — proposed 1, no usage data (§2). Mechanism settled; value open.

## 12. Implementation note — wiring the logging fusion (domainspec × Arcanum)

This is the concrete HOW under §7's fusion. It is an **integration plan, not built code**, and
it revises one claim §7 made that a closer on-disk look corrected.

### 12.1 The correction §7 needed

§7 framed domainspec's populated ledger as "the missing half." Closer reading revises this:
**Arcanum already has a deterministic ledger writer** — `framework/observability/scripts/
observe-invocation.sh` validates an invocation-envelope, dedupes by key, appends one row to
`signals/sigil-invocations.jsonl`, maintains the `by-sigil` / `by-capability` reference indexes,
and updates `reflection-state.json`. It is **not missing a writer**. It is missing three things:

1. **A Claude hook surface.** The writer is driven by **Codex** hooks (`.codex/hooks.json`:
   `UserPromptSubmit` opens an envelope → `PostToolUse` appends evidence → `Stop` closes and
   calls the writer). There is **no `.claude/settings.json` hooks block**, so under Claude Code
   nothing fires and no envelope is produced — a concrete reason the ledger is empty.
2. **The scaffold run.** `signals/`, `tmp/`, `reflection-state.json` exist only as `.gitkeep`
   placeholders; the `observability-setup` Formula that materializes them was never run at root.
3. **An envelope under Claude.** The envelope is opened only for a recognized `/command` or
   `$skill` token under the Codex hook; a domainspec-style dispatch never produces one.

So "port the domainspec appender as Arcanum's writer" is the **wrong move** — it would duplicate
and fight an owner that already exists, breaking its dedupe / index / counter logic.

### 12.2 Two kinds of log, not one

The deeper reason they do not collide: the two repos log **different kinds of thing**.

- **Authored dispatch-spec** (domainspec `register-dispatch`): the *intent* of a fan-out —
  `goal`, per-agent `angle`, the `anti_bias` axis, `connections`. A hook **cannot derive these**;
  they are design decisions the model must author. domainspec logs them via a **model-invoked
  skill**, deliberately *not* an auto-logger.
- **Derived behavioral signals** (Arcanum `signal-observer`): `quality-pass`,
  `anti-pattern-hit`, `output-drift` — derived *automatically* post-run from the envelope,
  hook-first, on the principle "the system must not rely on the agent remembering."
- **Per-stage receipts** (§7 L3): the validated execution evidence per stage.

Three planes, cross-referenced by `dispatch_id` / `run_id` — not one ledger one repo lacks. The
fusion is to let each plane be written by whoever *can* write it, and join them by key.

### 12.3 The plug point — producer, not replacement

domainspec's contribution lands cleanly as an **envelope/record producer** (a textbook
**Formula**: stateless, deterministic, schema-validate-or-reject, idempotent) feeding the
*existing* `observe-invocation.sh`, which stays the sole ledger-writing authority:

- The domainspec appender emits an `invocation-envelope.json` (per
  `framework/observability/templates/`) carrying the authored fields (`goal` / `angle` /
  `anti_bias`) as a typed extension, then either writes the default `tmp/latest-invocation.json`
  and calls the writer, or drops a `pending-envelope.json` for the `Stop` hook to close.
- The owner keeps append, dedupe, indexes, counters. domainspec becomes one more envelope
  producer alongside the Codex hooks — exactly the role the `observed-invocation-loop` spec
  already assigns to "Codex hook or wrapper."

End-state under Authority-Bound Composition: **Arcanum owns the ledger contract + writer; the
authored-semantics layer is a typed envelope extension; domainspec consumes.** Consistent with
Arcanum-as-source-of-truth.

### 12.4 How domainspec wired it (the reference)

The mechanism worth porting is not the appender alone but the **discipline around it**.
domainspec's `internal_tools/subagents-dispatch-hooks/` is Node-only, zero-dependency, installed
per-user to `~/.claude`:

- **Three `PreToolUse` hooks.** (1) a **reminder-nudge** on `Agent` — prompts the model to
  register, writes nothing itself (a hook cannot author intent); (2) a **deny** on `Workflow` —
  forces dispatch through the governed path; (3) an **append-only enforcer** on
  `Edit|Write|Bash|…` that blocks any direct mutation of the ledger (closing a dispatch is an
  appended `close_of` event, never an edit).
- **A model-invoked skill** (`register-dispatch`) that authors the row — the deliberate split:
  the hook guarantees the model is *reminded*; the model supplies the semantics the hook cannot
  derive.
- **A deterministic appender** (`append-dispatch.cjs`): strict schema-validate-or-reject
  (exit 2), idempotent on `dispatch_id` / `close_of`, a structure-only pre-append self-check that
  refuses a corrupt ledger (exit 1) while grandfathering old rows.
- **A per-user installer** — harness-specific at the install layer, harness-neutral at the
  appender.

The load-bearing design choice — **two appends (spec at dispatch, close at termination),
model-authored, append-only-enforced** — is exactly what Arcanum's per-dispatch plane lacks, and
it ports as the envelope-producer plus a Claude hook surface.

### 12.5 The wiring to add in Arcanum

1. **A `.claude/settings.json` hooks block** mirroring the three Codex events
   (`UserPromptSubmit` / `PostToolUse` / `Stop` exist in both harnesses) — the one real harness gap.
2. **Run `observability-setup`** at the repo root to materialize `signals/` + `reflection-state.json`.
3. **The envelope-producer Formula** carrying the authored `goal` / `angle` / `anti_bias` fields.
4. **Preserve model-invoked authoring** for those semantic fields. Reconcile the two philosophies
   by plane: the hook captures what it can automatically (envelope skeleton, tool events, run
   boundaries) — **hook-first for *existence***; the model enriches with the intent a hook cannot
   derive — **model-authored for *meaning***.

### 12.6 Honest residue

- This is an **integration plan, not built**. The Arcanum side is baseline-ready scripts that
  were **never exercised** (empty ledger), not a proven pipeline.
- The model-invoked (domainspec) vs hook-first (Arcanum) philosophies are a **real tension**,
  resolved above by plane (existence vs meaning) but not yet tested.
- Reconciliation with `observed-invocation-loop` and the deprecated `.arcanum/runtimes/` adapter
  model must be explicit (cite-don't-rediscover) before this becomes its own TO-VLAD memo.

---

— consolidated from TO-VLAD6 + TO-VLAD8 + the composition slice of TO-VLAD7.
