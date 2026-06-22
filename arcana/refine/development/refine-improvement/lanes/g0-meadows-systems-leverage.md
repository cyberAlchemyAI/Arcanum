# Lane A — Systems-Leverage Reframing of the /refine Problem

Role: Lane A (challenge the PROBLEM, not the proposals).
Lens: Meadows systems-leverage — intervene where the smallest change moves the
most behavior, not where the loudest defect sits.
Target state held fixed: a /refine that reliably turns vague targets into good
refined seeds/designs/plans at acceptable cost.

## Claim 0 — The named problem ("anchoring") is real but low-leverage

`TWO-LANE-DISCIPLINE.md` frames the failure as anchoring: one single-track loop
elaborates the first idea, nothing disagrees with the *choice* of idea
(`projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md:29-31`). That is a
*quality-of-output* defect. But anchoring can only bite on runs that reach the
output stage. The internal evidence says runs do not get there.

## Claim 1 — In practice, /refine almost never reaches its value-producing stages

Proof: The only materialized live output reports `Status: block` with **every
selected loop stage blocked** — "It is not promotion evidence because every
selected loop stage is blocked in the manifest"
(`arcanum/arcana/refine/development/LIVE-XRAY-RUN-REVIEW.md:17-18`). The observer
report records the sigil stuck in `flag`/pilot precisely because "the x-ray live
output exists, but it reports `Status: block` and `Promotion evidence: no`"
(`arcanum/arcana/refine/development/SIGIL-DEVELOPMENT-OBSERVER-REPORT.md:32`,
`:38`). `REFINEMENT-LOOP.md:6` still marks the sigil `Status: pilot`. So the
binding constraint is **reaching the value stages at all**, not the quality of an
idea once produced.

## Claim 2 — The structural gate decoupled "passes validation" from "produces value"

Proof: Run `20260525T002839Z.md` shows `QUALITY_BAR_STATUS=pass`,
`REFINE_LIVE_VALIDATION=pass`, `VALIDATION=pass` across all five regimes
(`runs/20260525T002839Z.md:44-62`) — while the underlying live output is the same
all-stages-blocked artifact. The harness validates the *shape of the contract*,
not delivered refinement. Across runs the aggregate is
`14 QUALITY_BAR_STATUS=pass` yet only `4 REFINE_LIVE_VALIDATION=pass` and zero
successful end-to-end refinements (grep over `development/runs/*.md`). The system
reports health while users get blocks.

## Claim 3 — The friction load is front-loaded before any value is returned

Before stage 1 produces anything, a materialized run must author and *validate*
`REFINE-DISPATCH.json` against `dispatch.schema.yml`, or the whole run is `block`
(`SKILL.md:54-75`, `:73`). The run folder mandates seven required artifacts —
`RUN-MANIFEST.md`, `evidence-index.json`, `REFINE-SEED-PROPOSAL.md`,
`REFINE-DISPATCH.json`, `RUNTIME-HANDOFF.md`, `RESULT.md`, `stages/`
(`SKILL.md:177-185`). Then a strategy-preview + explicit permission gate must
clear *before any stage runs*, and a second permission gate covers subagents
(`SKILL.md:93-97`, process steps 7-8 at `SKILL.md:296-297`). Ten stages follow,
each requiring a native receipt or it blocks (`SKILL.md:128-150`). The user pays
the full setup tax (dispatch authoring + schema validation + two gates) up front
and only *then* discovers whether the ten capability handles resolve.

## The Lane A reframing: the core problem is STRUCTURAL FRICTION / ADOPTION, not anchoring

> /refine's binding constraint is that its mandatory pre-value scaffolding
> (ten fixed stages × ten capability dependencies + REFINE-DISPATCH.json schema
> validation + two permission gates) makes the path to first value so long and
> so brittle that runs reliably block before producing a refined seed — so the
> idea-quality defect (anchoring) is downstream of a delivery defect and rarely
> gets a chance to occur.

This is a genuinely different problem than anchoring. Anchoring says *the output
is the wrong shape of good*. Lane A says *there is almost no output*. A two-lane
fix (add Lane A dissent) **adds an eleventh-plus stage and a second dispatch
branch** to a loop that already cannot finish ten — it pushes the wrong leverage
point, increasing friction to fix quality on runs that never reach quality. In
Meadows terms, two-lane discipline operates at the level of *information flows /
rules*; the binding constraint here is lower and harder: the *structure of the
delivery pipeline itself* (stocks-and-flows / system goal), which dominates.

## Highest-leverage intervention points (ranked)

1. **Decouple value delivery from the dispatch-spec scaffold (highest).** Make a
   refined seed reachable *without* a validated `REFINE-DISPATCH.json` — let the
   route artifact become optional hardening for deep runs, not a `block`
   precondition (`SKILL.md:73`). This directly removes the front-loaded tax in
   Claim 3 and the all-stages-blocked failure in Claim 1.

2. **Collapse the ten fixed stages into a value-first minimum, expandable on
   demand.** The "presets tune budget but never remove stages" rule
   (`SKILL.md:39`, `REFINEMENT-LOOP.md:57`) is the structural cause of the long
   path. A `compact` preset that produces seed + one critique + plan (3 stages)
   would let a run *finish*; deeper stages become opt-in.

3. **Fix the gate that confuses shape-validation with value
   (`runs/20260525T002839Z.md:44-62`).** Make `REFINE_LIVE_VALIDATION` require a
   non-blocked `RESULT.md`, so the system stops reporting health on empty runs.
   This is a measurement-leverage point: you cannot improve what you mismeasure.

4. **Reduce the ten hard capability dependencies / receipt requirements**
   (`SKILL.md:128-150`) and the double permission gate (`SKILL.md:93-97`) — each
   is an independent block source. Fewer mandatory native handles = fewer ways to
   block before value.

## What this lane does NOT claim

It does not deny anchoring exists; `TWO-LANE-DISCIPLINE.md:29-31` is sound about
output quality. It claims anchoring is the *second* problem to solve — fix
delivery (let runs finish), then the idea-quality dissent becomes a cheap overlay
on a working loop rather than another block-prone branch on a broken one.
