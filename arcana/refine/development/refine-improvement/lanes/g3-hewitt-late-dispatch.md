# G3 — Hewitt Late Dispatch: a Governed Tensioned Parallel Fork at Design

Position: refine should break anchoring with a **LATE, STRONG, governed,
tensioned PARALLEL subagent dispatch placed at the Design stage** — two lanes run
as *actual subagents*, not as a single-agent rhetorical exercise, governed by the
`check-tension` gate plus the dispatch ledger.

## Where refine breaks anchoring today, and why it is weak

Refine's canonical loop already carries the technique vocabulary for this. The
`dialectic_for_tension` overlay binds `dialectic`, `zig_zag`, and `residue_ledger`
"when the target has competing principles or likely disagreement," and
`tournament_for_alternatives` binds `tournament`, `pareto_gate`, and
`recomposition_proof` "when several plausible designs … must be compared"
(SKILL.md, technique-overlay-policy, lines 112–113). Both require "roles and
convergence criteria" (line 121). The `subagent_strategy` field can mark sibling
agents `none | recommended | required | blocked` (line 67) and, when
`recommended`/`required`, must carry "role, join-policy, receipt, context, and
authorization details" (line 68).

The weakness is **enforcement strength, not vocabulary.** Overlays "change stage
configuration, validation expectations, gates, evidence requirements"
(line 103) — they are *configuration*, applied inside whichever single agent is
running the stage. A `dialectic` run by one model is the model arguing with
itself: a cheap gate. It can *check* that two positions were written down, but it
cannot **force** a genuinely different idea, because both positions share one
context window and one prior commitment. This is exactly the failure
TWO-LANE-DISCIPLINE names: "the most expensive failure mode is anchoring:
shipping the first framing because nobody was assigned to disagree with it"
(TWO-LANE-DISCIPLINE.md, lines 30–31). Assignment to a *separate owner* is the
mechanism — not a richer prompt.

## The design: two real subagent lanes at Design

Map the two-lane discipline directly onto refine's Design stage (canonical loop
stage 6, Invoke Redefine/Design, SKILL.md line 47):

- **Lane Z (zig-zag, explore the idea).** Takes the distilled unit as given and
  "builds it out by alternating generation and critique," running it "into at
  least one real counterexample, not just a friendly demo"
  (TWO-LANE-DISCIPLINE.md, lines 10–20). This is refine's existing `zig_zag`
  overlay, but executed by its own subagent.
- **Lane A (alternatives, challenge the problem).** "Holds the underlying problem
  fixed and proposes a genuinely different solution" and "is not allowed to
  produce a variant of Lane Z's idea" (TWO-LANE-DISCIPLINE.md, lines 22–27). This
  is the adversarial owner. Its non-overlap is structural, not advisory.

These run as a **parallel** group: under the strategy lifecycle, "Agents inside a
group run in parallel" once READY (subagents-strategy SKILL.md, line 20), and
parallelism is itself a declared dispatch trigger — "independent tasks"
(line 12). Set `subagent_strategy: required` so Design cannot proceed
single-agent.

## Why governance makes it STRONG, not just expensive

Three governance hooks turn the parallel fork from a cost into an enforced anchor
break:

1. **`check-tension` before the human confirm.** Refine's strategy preview and
   permission gate (SKILL.md, lines 77–99) is the natural seam. Per the strategy
   lifecycle, "two independent agents verify the sheet is genuinely tensioned
   (Tests 1–4); the sheet reaches the human only if **both PASS**, otherwise it
   returns … for revision" (subagents-strategy SKILL.md, line 18; P5, line 29).
   A Lane A that is merely a Z-variant fails this gate and is sent back. This is
   the executable enforcement a cheap in-context dialectic lacks.
2. **The ledger.** Each lane is registered with its angle and the `anti_bias`
   axis (register-dispatch); the dispatch row + close row make the tension
   *auditable after the fact*, not just asserted.
3. **Adjudicating synthesis.** A tower "closes only when a synthesis … names what
   problem each lane actually solved vs. only reframed" and issues a per-claim
   bridge decision (TWO-LANE-DISCIPLINE.md, lines 41–50). This maps onto refine's
   Distill Repair (stage 8) and Refine-owned final synthesis (stage 10) — the
   join is parent-owned, matching P12 `final_approver: parent` and P7 derived
   aggregation (subagents-strategy SKILL.md, lines 30, 32).

A cheap gate "cannot FORCE a genuinely different idea" — it can only score the
text it is handed. An adversarial parallel agent, *owned separately and gated by
check-tension*, is structurally prevented from producing the friendly variant,
because a different owner with a non-overlap constraint and a PASS/FAIL gate is a
harder constraint than any prompt instruction inside one context.

## The honest weakness: the anchor may already be set by stage 6

The damaging admission: by Design (stage 6) **Distill has already committed to one
unit.** Refine's canonical order runs Distill at stage 5 — "Select the coherent
unit" (SKILL.md, lines 31, 46) — *before* Design at stage 6. A late fork at
Design therefore inherits a single distilled unit as its shared starting point.
Lane Z faithfully explores that unit; but Lane A is asked to "hold the underlying
problem fixed and propose a genuinely different solution" (TWO-LANE-DISCIPLINE.md,
line 22) when the problem framing it should fork from may already have been
collapsed into the chosen unit at Distill. Late dispatch breaks *design-level*
anchoring (how the chosen unit is built out) but **cannot retroactively break
unit-selection anchoring** committed one stage earlier. The strongest lanes still
run downstream of the very commitment most likely to be the anchor.

### Where to place the fork (addressing the weakness)

Two honest options, neither free:

- **Keep the fork at Design (stage 6), but require Lane A to fork the *underlying
  problem statement*, not the distilled unit.** TWO-LANE-DISCIPLINE mandates a
  one-sentence solution-independent problem statement that "both lanes are
  measured against … not against the hypothesis" (lines 32–38). If Distill (stage
  5) is required to *emit that problem statement as a separate output* alongside
  the selected unit, Lane A can fork the problem even though it dispatches at
  stage 6. This is the cheapest change: it adds one required output to Distill and
  one non-overlap constraint to Lane A, and keeps the existing late seam.
- **Move the fork earlier, to bracket Distill (between stage 5 and 6).** Run the
  two lanes as competing *inputs* to a tournament-style Distill rather than
  consumers of its single output — `tournament_for_alternatives` with
  `pareto_gate` (SKILL.md, line 113). This breaks unit-selection anchoring
  directly but is more expensive (two distilled units to repair and recompose)
  and risks a non-joinable synthesis; TWO-LANE-DISCIPLINE warns two lanes is "the
  minimum that creates real tension while staying joinable by one parent
  synthesis" (lines 53–56), and forking before Distill strains that joinability.

Recommendation: **Design-stage fork (option 1) with Distill emitting the
solution-independent problem statement.** It is the *late, strong, governed*
position the question argues for, it reuses the existing permission seam and
check-tension gate, and it converts the honest weakness into a single concrete
requirement on the prior stage rather than a structural rebuild of the loop. The
residual, stated plainly: even with the emitted problem statement, the *evidence
baseline* both lanes share was assembled once at Context Builder (stage 1), so
deep framing anchoring upstream of Distill remains untouched by any Design-stage
fork.
