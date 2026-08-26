---
name: experiment
description: Subagent dispatch that PROPOSES and pre-registers a falsifiable experiment — the designer authors a success/failure criterion fixed BEFORE any run and the skeptic validity-checks it, producing a frozen criterion.md. Running the probe and adjudicating survived-vs-falsified is a SEPARATE downstream step, not part of this dispatch. Routed here from domainspec-subagents-strategy as the LIVE type skill for `dispatch_type: experiment`. Defines experiment-type judgment only — the pre-registered criterion, the design-time validity gates, and the SURVIVED/FALSIFIED/INVALID verdict vocabulary (SURVIVED/FALSIFIED rendered later, at run). Use research when the question is whether a NEW claim survives by coverage; use review to attack an EXISTING artifact; use experiment when you are pre-registering a probe against a criterion fixed BEFORE running.
---

# experiment — pre-registration (proposal) type skill

The LIVE type skill for `dispatch_type: experiment`. **When/whether to dispatch** and all
universal law — triggers, the human gate, lifecycle, `final_approver`, `exit_reason`, the
invariants — live in the **router** (`.claude/skills/domainspec-subagents-strategy/SKILL.md`);
nothing here overrides it. **Record/sheet mechanics** — the two appends, the appender,
validation — and the inline **field definitions** you actually read live in
**register-dispatch** (`.claude/skills/register-dispatch/SKILL.md`). Constitution §5
(`internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md`)
is the upstream authority for those fields only — not a routine read. This skill defines no
field; it says what a good **experiment** dispatch contains.

**What this dispatch is — propose, don't run.** An experiment dispatch **pre-registers** a
falsifiable experiment: the `designer` authors a success/failure criterion and the `skeptic`
attacks its internal validity, producing a **frozen, validity-checked `criterion.md`** — the
experiment proposal. **Running the probe and adjudicating survived-vs-falsified is a separate
downstream step**, not part of this dispatch (the run phase, below). The deliverable here is a
proposal good enough to run later and re-adjudicate deterministically — not a result.

## The grader is the differentiator (peer, not re-skin)

Experiment is a peer of its siblings because its **grader** differs, not because its roles are
renamed:

| Type | Grader |
|---|---|
| research | coverage / claim ≤ proof |
| review | severity × flaw-verification over an existing artifact |
| **experiment** | **falsification against a pre-registered criterion + internal validity + reproducibility** |

The load-bearing property is **pre-registration**: the criterion is frozen *before* the result
exists (research is judged *after*, by coverage). This dispatch owns the pre-registration and the
**internal-validity + reproducibility-by-design** half of the grader; **falsification is rendered
later, by the run** (below). Justify experiment by its **grader**, never its roles — renamed roles
over the same grader is a re-skin, not a type (the vacuity trap).

## Roles — experiment semantics over the existing enums (NO new enum values)

This dispatch (propose) uses the first two; the run phase (separate, downstream) uses the last two:

| Conceptual role | `agents[].role` | phase | function / guards against |
|---|---|---|---|
| designer | writer | **propose (here)** | authors the pre-registered criterion (an artifact) — guards against post-hoc criteria |
| skeptic | skeptic | **propose (here)** | attacks internal validity *at design time* — guards against a criterion that does not test the hypothesis |
| runner | explorer | run (later) | runs the probe = reasoning/investigation, NOT code execution — produces the raw result |
| adjudicator | auditor | run (later) | renders the verdict against the frozen criterion — guards against moving the goalposts |

A group's function is read off its agents' roles, its workflow position off its `connections`.
A propose dispatch may be as small as one `designer` (n = 1); a `skeptic` is added whenever the
criterion's validity is worth attacking before freeze (almost always).

## Criterion freeze — topology + immutability, never a column

Pre-registration is enforced by **topology + the human-gate freeze + immutability**, never a
schema field:

- The `designer` authors the criterion and the `skeptic` attacks it; the criterion lands in
  `working_folder` as a durable artifact and is **frozen at the P2 human gate** — before any run
  exists. That is what "pre-registered" means here.
- The frozen criterion is **read-only downstream**: any edit after freeze is a *new* criterion
  (re-enters the P2 gate as a fresh proposal), never an in-place mutation. That immutability is
  what makes "pre-registered" verifiable against an artifact: the criterion file exists and
  predates any result.
- The criterion lives as the designer's output artifact in `working_folder` — **never a ledger
  column**. The appender rejects `success_metric` as an unknown key; a criterion column would
  repeat the vacuity error v0.5.2 killed.
- experiment is a LIVE type, so `working_folder` is **REQUIRED** (appender).

## The criterion artifact — what `criterion.md` must contain

The criterion is the designer's frozen output; this is **artifact content, not a ledger field**
(the column boundary above stands). Saying what makes a criterion adjudicable and re-derivable is
the skill's job — it defines no field. A good criterion artifact pins, *before any run*:

- **One falsifiable hypothesis** — a single claim whose falsifying observation you can name; not
  two claims joined by "and".
- **Non-goals** — what the probe explicitly does *not* test. This is what keeps the hypothesis a
  single claim, not scope decoration.
- **The falsification condition + a mechanical verdict rule** — the observable(s) that will decide
  the outcome and a rule mapping them to a verdict deterministically. The rule resolves **only**
  into `SURVIVED` / `FALSIFIED` / `INVALID` — never an execution-status tier (`pass/flag/block`);
  that mapping is deferred (Reserved boundary). Structure (a metric, a threshold, a counted shape)
  is encouraged where it sharpens determinism, but it lives **in the artifact** — never promoted to
  a registry column.
- **The discrimination check** — both outcomes must be informative: state what a SURVIVED *and* a
  FALSIFIED each would teach. A criterion only one outcome could ever produce fails the skeptic's
  non-discrimination axis (below) — fix it at design time, before freeze, not after.
- **Pre-registered names/categories** — any label, bucket, or category the probe will use, fixed
  before it sees data; guards against post-hoc naming.

This content is what lets a later adjudicator re-derive the same verdict from the same frozen
criterion + result (the reproducibility property below). It is guidance on the artifact, owned
here; it adds no field to the sheet or the ledger.

## Validity gates — the skeptic's axes (checked at design time, before freeze)

The skeptic attacks the criterion's internal validity **before it is frozen** — these are design
properties, checkable without running anything:

- **confounds** — a result would be explained by something other than the hypothesis.
- **non-discrimination** — the criterion would pass/fail regardless of the hypothesis (it does not
  test the hypothesis).
- **reproducibility absent** — the verdict would not be deterministically re-derivable from the
  frozen criterion + a result.

A criterion that nothing could falsify is **INVALID by design** — it never reaches freeze; it goes
back to the designer. Catching this here, before any run, is the whole point of proposing
separately from running.

## Verdict vocabulary (defined here; SURVIVED/FALSIFIED rendered at run)

| verdict | rendered | meaning |
|---|---|---|
| **INVALID** | propose (here) | the skeptic knocked down internal validity — the criterion does not test the hypothesis; redesign before freeze |
| **SURVIVED** | run (later) | adjudicated against the frozen criterion — the probe did not falsify the hypothesis |
| **FALSIFIED** | run (later) | adjudicated against the frozen criterion — the probe falsified it |

This dispatch closes `resolved` when the `final_approver` accepts a **frozen, validity-checked
`criterion.md`** (the proposal is ready to run later). If the skeptic finds the design
unfalsifiable, that **INVALID** outcome is a successful detection — the criterion goes back to the
designer, and a re-designed criterion is a *new* dispatch, not a non-close. SURVIVED/FALSIFIED
belong to the later run and never close this dispatch. Contrast: research = GO/…/KILL; review =
UPHELD/REFUTED/DOWNGRADED. The verdict vocabulary does **not** map onto execution-status
(`pass/flag/block`) — that cross-project unification is deferred (Arcanum F1).

## Canonical shape (v0.6.0 chassis)

This dispatch (propose) — designer authors, skeptic attacks, criterion frozen at the P2 gate:

```
designer ◀──zig-zag──▶ skeptic   ⇒  frozen criterion.md
```

The skeptic checks validity in `zig-zag` (or parallel) with the designer; **zig-zag/feedback carry
`loop_cap`**. A `feedback` back-edge is conditional (P6) — here, when the skeptic's validity attack
means the criterion must be re-designed before freeze. A bare n = 1 designer (no skeptic) is
allowed for a trivial pre-registration but forgoes the design-time validity check.

The **run is a separate downstream dispatch** (not authored here): it consumes the frozen
`criterion.md` read-only and renders SURVIVED/FALSIFIED.

```
(later, separate)  runner ──sequential──▶ adjudicator   ⇒  experiment.md + findings.md
```

## Reserved boundary (state it; do not block on it)

- The **run phase is downstream** — this skill stops at the frozen proposal. How the run is
  dispatched (a follow-up run step, manual, or a future runner) is out of scope here.
- The **code-execution runner is RESERVED** — gated on the `code` type landing with an execution
  substrate. A run needing to execute code waits for `code` LIVE; the narrow run is
  reasoning/investigation over artifacts, not code execution.
- **Reproducibility = deterministic RE-ADJUDICATION** — another agent, same frozen criterion +
  result, reaches the same verdict — NOT re-execution. The criterion artifact is authored *here*
  to make that possible later.

## Inherited rule (cited, not invented)

`final_approver` may never sit in a working group (constitution P12 / §5). In the propose dispatch
the designer and skeptic are working-group members, so neither may double as `final_approver` —
use `parent` or a dedicated approver group (its single agent's role is `auditor`). The same rule
binds the run's adjudicator later.

## Outputs (P9 pattern, experiment flavor)

This dispatch (propose) produces **one artifact** in `working_folder`:

- **`criterion.md`** — the frozen, validity-checked pre-registration (the content above). This is
  the dispatch's deliverable. With a skeptic in the loop, `criterion.md` records that it passed the
  design-time validity gates (or carries the INVALID finding that sent it back for redesign).

The **later run** (separate dispatch) produces the other two, against the frozen `criterion.md`:

- **`experiment.md`** — the runner's probe + raw result, persisted verbatim.
- **`findings.md`** — the adjudication: every load-bearing verdict citing the **criterion +
  result** it rests on, ending in SURVIVED/FALSIFIED.

The requirement is the FILES, not who writes them. Append/close mechanics are
**register-dispatch**'s — do not restate them here.

## Names

Draw `agent_name` from `telemetry/agents/agent-pool.yaml` (ordered `role_fit`). Falsification fits
the philosophy-of-science figures: **Popper, Lakatos, Hume, Feyerabend, Kuhn**
(`role_fit: [skeptic, writer]`) for this dispatch's skeptic/designer; primary-`role_fit` explorers
for the run's runner; an `auditor` fit (**Vlachopulos, Loregian, Brandenburg**) for the run's
adjudicator. Never reuse a name within one dispatch; never invent one — and the skeptic that
attacks validity is never the designer whose criterion it attacks (P12's spirit at agent scale).
