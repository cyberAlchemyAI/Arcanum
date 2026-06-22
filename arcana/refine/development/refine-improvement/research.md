# Refine-Improvement Research — Collected Lane Returns (verbatim)

Dispatch: 2026-06-18-refine-improvement-strategy. Eight lanes concatenated verbatim below; synthesis adjudication lives in findings.md.


================================================================
## LANE FILE: g0-meadows-systems-leverage.md
================================================================

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


================================================================
## LANE FILE: g0-christensen-jtbd.md
================================================================

# Lane A — Christensen JTBD: The Hiring Problem of /refine

Status: research lane (Lane A — challenge the problem, not the proposals)
Date: 2026-06-18
Lens: Clayton Christensen jobs-to-be-done; outcome-defined, solution-independent.

## Stance

I hold the target state fixed: a `/refine` that **reliably turns vague targets
into good refined outputs at acceptable cost** (SKILL.md objective, lines 14–16).
I do not argue the canonical ten-stage loop is too long, too single-track, or
anchoring-prone. The anchoring framing in `TWO-LANE-DISCIPLINE.md` (lines 22–31)
diagnoses a *process* defect — "nobody was assigned to disagree." Lane A's claim
is sharper and prior to that: even a loop that disagreed perfectly with itself
would still fail if **its outputs do not get hired** for the job users actually
have. Anchoring is a hypothesis about *why outputs might be weak*; it is not the
same as whether weak-or-strong outputs do the job. Frame the real problem as an
**unmet outcome**, not a process pathology and not a pure cost story.

## The job refine is hired for

People do not want a refinement loop. They want to **stop being stuck on a vague
target and start the next real move with justified confidence.** README.md states
the situation precisely: users "have a target, concern, folder, repository area,
or rough idea, but not a refined model of what should be built, designed,
planned, or deferred" (README.md lines 7–9). The functional job-to-be-done:

> "When I have a vague target and cannot responsibly act on it, help me reach a
> committed next move I can trust — so I can leave refinement and do real work."

The hiring test is the *handoff*, not the loop. Refine itself names this: its
real product is "recommended next routes" produced "only after the final
synthesis" (SKILL.md lines 305, 255). Task Session and Sigil Development are the
jobs downstream (README.md line 38). So refine is hired to **produce a trusted
launch point for the next route.** Three artifacts carry that load:

1. the **non-executed plan** (Invoke Plan, stage 9),
2. the **freeform RESULT.md synthesis** (Refine-owned, stage 10),
3. the **recommended-next-routes** block (RESULT.md, result.md lines 38–40).

## Where the outputs fail the job

A JTBD failure is not "low quality writing" — it is the output **not advancing
the user toward the hire-able next move.** Three structural failures, each
distinct from anchoring and from cost:

**F1 — The non-executed plan is hired to be executed, but is built to never be.**
Stage 9 produces a plan "or blocked reason" (REFINEMENT-LOOP.md line 82) that is
by construction *non-executed* (SKILL.md line 49, anti-pattern lines 367, 370).
The user's job is to act; the deliverable is defined as the thing that does not
act, then hands to a *separate* Task Session that re-derives execution context.
The plan's fitness for hiring is never tested inside refine — there is no gate
asking "would Task Session accept this plan as-is?" The output can be internally
valid (every stage `pass`) yet unhireable downstream. This is an outcome gap, not
a friction gap: even free and fast, an un-executable plan does the wrong job.

**F2 — RESULT.md synthesis is graded on loop completion, not on decision the user
can carry.** The synthesis is required to be "produced from stage artifacts
rather than a route proposal" (promotion-gate, SKILL.md line 360) and the
template (result.md) is a stage-verdict ledger: ten `pass|flag|block` rows plus a
one-line "Final synthesis: `<summary or blocked reason>`" (result.md lines 14,
26–36). The quality bar (SKILL.md lines 308–326) measures *process completeness*
— dispatch validated, receipts collected, manifest materialized — never *whether
the user can now decide.* A run that completes all ten stages and emits a vague
one-line synthesis passes the bar while failing the job. The job's success metric
("I can trust my next move") is **absent from the contract entirely.**

**F3 — Recommended-next-routes is the load-bearing output and the least
governed.** This is the literal hire moment, yet it is a free-text list appended
after synthesis (result.md lines 38–40) with no contract on *why* a route fits,
no acceptance criteria the next owner could check, and no traceability from the
synthesis to the recommendation. SKILL.md gives it one process line (line 305)
and lists it as an observability field (line 346) — but no quality requirement.
The one artifact the user must act on is the one with no fitness test.

## Why this is not the anchoring problem (and not cost)

Anchoring (Lane Z's territory) says the *content* converges on the first framing.
Even granting that, F1–F3 persist: a perfectly de-anchored, genuinely-best plan
still (F1) isn't validated as executable, (F2) is graded on completeness not
decidability, and (F3) hands off through an ungoverned route list. The defects
live in the **output contract and its fitness tests**, not in idea selection.

Nor is this the friction/cost framing. Cost asks "is the loop too expensive for
the value?" The JTBD failure holds *at any cost*: drive cost to zero and the
outputs still do not demonstrably get hired, because nothing in refine measures
hire-ability. The acceptable-cost half of the target state is necessary but not
sufficient; refine could be cheap and still never get hired.

## The reframed problem statement (solution-independent)

> Refine's core problem is **outcome-blindness at the handoff**: it is hired to
> deliver a trusted, executable next move, but its outputs (non-executed plan,
> completion-graded synthesis, ungoverned route list) are tested for *loop
> integrity*, never for *hire-ability* — so a fully successful run can still
> leave the user unable to confidently take the next step.

The fix space (held open, not chosen): add a hire-ability fitness test — e.g. a
"would the next owner accept this?" gate on the plan, a decidability criterion on
synthesis, and an acceptance contract on each recommended route. Whether that is
a new stage, a gate overlay, or a downstream-acceptance receipt is a design
question for synthesis, not for this lane.

## Residue / owner

- Open: is "hire-ability" measurable inside refine, or only observable downstream
  when Task Session accepts/rejects the plan? Owner: synthesis lane.
- Open: does F3 (route governance) overlap Dispatch Spec's territory, or is it
  refine-owned per SKILL.md line 255? Owner: ownership-boundary review.


================================================================
## LANE FILE: g1-alexander-external-modes.md
================================================================

# G1 — External Design-Method Modes for /refine

Status: research lane (read-only survey + proposal)
Date: 2026-06-18
Question: Do different refinement PROBLEM-CLASSES need different `/refine` MODES?

## Why this is open

`refine/SKILL.md` keeps a **fixed canonical ten-stage loop** and varies only two
dials: `preset` (compact/standard/full/deep — "tune budget and configuration; they
do not remove stages", SKILL.md §preset-policy, lines 278-287) and `technique
overlays` (`baseline_sequence` plus seven optional overlays, §technique-overlay-policy,
lines 101-126). Both dials are *single-track*: they amplify or decorate one
generation→critique→repair→plan pipeline. The anchoring failure named in
`projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md` (lines 22-30: "the most
expensive failure mode is anchoring: shipping the first framing because nobody was
assigned to disagree with it") is *structural*, not a budget shortfall — a deeper
preset spends more tokens elaborating the same first framing. So the question is
whether refinement is one problem with intensity knobs, or several distinct
problem-classes that need genuinely different loop shapes (modes).

## External precedent — what each tradition says about distinct phases

1. **Double Diamond (UK Design Council, 2004).** Design alternates two *opposite*
   cognitive operations: **divergent** (open the space, generate options) and
   **convergent** (close the space, select/commit) — run twice, once over the
   *problem* (discover/define) and once over the *solution* (develop/deliver).
   The load-bearing claim: divergence and convergence are different activities that
   *fail when collapsed*. Refine's loop is almost entirely convergent (one Define,
   one Design, one Plan, each immediately critiqued and distilled toward a single
   unit). It has no first-class divergent mode.

2. **Christopher Alexander — pattern languages & "unfolding" (*A Pattern Language*,
   1977; *The Timeless Way of Building*, 1979; *The Nature of Order*, 2002).** Two
   distinct moves: (a) **diagnosing structure** — naming the recurring
   forces/centers already latent in a situation (a pattern is a problem-in-context
   plus a resolution of forces), and (b) **structure-preserving transformation** —
   making the *smallest* change that strengthens existing centers rather than
   imposing a new plan. This is a *repair/strengthen* operation distinct from
   greenfield design. Refine's `x_ray` overlay touches (a) but there is no mode
   whose whole purpose is incremental structure-preserving improvement of an
   already-good artifact.

3. **Design Science / DSR (Hevner et al. 2004; Simon, *The Sciences of the
   Artificial*, 1969).** Design is a **build-and-evaluate cycle against an
   explicit objective**, and Simon frames real design as **satisficing under
   bounded rationality** — find an option that *meets* criteria, don't search for
   the optimum. The relevant distinction: *generate-then-evaluate-against-a-fixed-
   criterion* (constraint satisfaction) vs. open generation. Refine's
   `toy_game_for_low_cost_falsification` overlay gestures at evaluation but it is
   optional decoration, not a criterion-first mode.

4. **IDEO / d.school design thinking (Brown 2009; Plattner d.school model).**
   Canonical non-linear phases: **Empathize → Define → Ideate → Prototype → Test.**
   The two operations refine lacks cleanly are **Ideate** (deliberately produce
   *many* competing concepts before judging — "defer judgment, go for quantity")
   and **Reframe** (the Define phase's job is to *rewrite the problem statement*,
   not the solution — the classic "you've been solving the wrong problem"). Two-Lane
   Discipline's Lane A is exactly this reframe move ("challenge the problem, not the
   idea", TWO-LANE-DISCIPLINE.md lines 22-30).

**Convergent precedent across all four:** every mature design tradition treats
*opening the space* and *closing the space* as different activities, and treats
*greenfield design* and *improving an existing thing* as different activities.
Refine currently only does one of these well (closing the space on a greenfield-ish
single concept). That is the root of the anchoring failure.

## Proposed top-down taxonomy of refinement problem-classes → modes

The taxonomy is cut along two axes the precedent agrees on:
**(X) is the problem-statement settled or contested?** and
**(Y) is there a prior artifact to preserve, or are we generating from scratch?**

| Mode | Problem-class it serves | External anchor | Canonical stages it re-tunes |
| --- | --- | --- | --- |
| **`converge` (default)** | Problem is settled; one promising concept exists; goal is a clean plan. This is today's behavior. | Double Diamond *convergent*; Simon satisficing | Whole loop unchanged (Define→…→Plan, single track). |
| **`diverge`** | Solution space is under-explored; risk of premature commitment to first concept. | Double Diamond *divergent*; IDEO *Ideate* | Forces `tournament_for_alternatives` on; **Invoke Design runs N≥2 sibling concepts**, Distill becomes *select-among-alternatives* not *repair-one*; adds a convergence-criteria gate before Plan. |
| **`reframe`** | The *problem statement itself* is suspect; the named target may be the wrong target. | IDEO *Define/Empathize*; Two-Lane *Lane A*; Schön reframing | Splits **Invoke Define into two tensioned framings (advocate + alternative problem-statement)**; Interrogation `refine-review` adjudicates which problem to solve *before* any Design; Distill selects the problem, not the solution. |
| **`strengthen`** | A prior artifact already works; goal is the *smallest structure-preserving improvement*, not a redesign. | Alexander structure-preserving transformation; *unfolding* | Context Builder ingests the existing artifact as protected baseline; `x_ray` on to surface existing centers; Design is constrained to *minimal delta*; Distill Repair becomes the primary stage; Plan emits a change-set, not a from-scratch plan. |
| **`evaluate`** | A concept exists and the real risk is *whether it survives a test*, not whether it reads well. | Design Science build-and-evaluate; Two-Lane *Lane Z* zig-zag falsification | Criterion is fixed **before** Design (pre-registration, cf. `experiment` skill); forces `toy_game_for_low_cost_falsification`; Interrogation must run the concept "into at least one real counterexample" (TWO-LANE-DISCIPLINE.md lines 19-20), not a friendly demo. |

### How the modes relate to the existing dials

- Modes are **orthogonal to `preset`**: any mode can run compact…deep. Preset stays
  a budget dial; mode becomes a *loop-shape* dial. This is the key correction —
  depth was being asked to do a job (escape anchoring) it structurally cannot do.
- Modes **compose with, but supersede, overlays**: each mode pins a *required*
  overlay set (e.g. `diverge` ⇒ `tournament`; `evaluate` ⇒ `toy_game`) so overlays
  stop being optional decoration for the problem-class that depends on them.
- `diverge` + `reframe` are the two modes that directly fix the anchoring failure:
  they introduce genuine *tension* (≥2 competing artifacts that must be adjudicated)
  into a loop that is otherwise mono-track. They are the refine-level analogue of
  Two-Lane Discipline applied to a single target rather than a research tower.

### Default-selection heuristic (top-down)

1. No prior artifact + settled problem → `converge`.
2. No prior artifact + many plausible solutions → `diverge`.
3. Suspect/vague problem statement → `reframe` (run first, can hand off to another mode).
4. Good prior artifact, incremental ask → `strengthen`.
5. Concept exists, survival is the open risk → `evaluate`.

A run may chain modes (`reframe` → `diverge` → `evaluate`); the canonical ten
stages remain the substrate — modes re-tune stage *configuration, multiplicity,
and gate criteria*, never delete a stage (preserving SKILL.md §canonical-loop,
lines 37-52, and the §preset-policy invariant that dials do not remove stages).


================================================================
## LANE FILE: g1-simon-internal-modes.md
================================================================

# g1-simon — Do problem-classes need different /refine MODES?

Lane question: derive any /refine *modes* bottom-up from refine's own canonical
ten-stage loop and observed internal evidence. Admit a mode only when a real,
observed failure or usage gap earns it. Prefer parameterizing the single loop.

## Method (read-only)

I read the contract surface (`SKILL.md`, `REFINEMENT-LOOP.md`), the existing
parameterization (presets + overlays), and the internal development evidence
(`WORK-PACK.md`, `VALIDATION.md`, `SELF-REFINEMENT-2026-05-24.md`,
`TASK-MATRIX.md`, `LIVE-EXAMPLE-SEEDS.md`, the `development/runs/` harness records).
A "mode" here means a *named variant that changes which stages run or the loop's
control flow* — distinct from a preset (budget tuning) or an overlay (per-stage
config). Below, each candidate mode is admitted only on cited observed evidence.

## What the system already parameterizes (so a mode would have to beat this)

The single loop is fixed at ten stages and is *not* allowed to drop stages:
"Presets tune budget, depth, and configuration; they do not remove stages"
(`SKILL.md` line 39; `REFINEMENT-LOOP.md` line 57). Variation is already carried
by two orthogonal axes:

- **Presets** `compact|standard|full|deep` tune budget only
  (`SKILL.md` lines 278-287; `REFINEMENT-LOOP.md` lines 117-124).
- **Technique overlays** (`route_menu_for_ambiguity`, `dialectic_for_tension`,
  `tournament_for_alternatives`, `xray_for_hidden_structure`,
  `toy_game_for_low_cost_falsification`, `memory_residue_for_context_recovery`,
  `protected_context_for_external_or_sensitive_evidence`) change stage config,
  gates, and validation expectations but "do not remove required stages"
  (`SKILL.md` lines 101-126; `REFINEMENT-LOOP.md` lines 85-114).

This is the key bottom-up finding: the loop authors *already chose* to map
problem-class variation onto overlays, not modes. Any proposed mode must show an
observed failure that overlay-or-preset parameterization cannot reach.

## Problem-classes actually observed, and where they land

The internal evidence names exactly these distinct problem-classes — and each one
is already handled by a *trigger into the single loop*, not a mode:

| Observed problem-class (evidence) | Already handled by |
| --- | --- |
| New-sigil-seed from a vague idea (`TASK-MATRIX.md` refine-xray-new; `LIVE-EXAMPLE-SEEDS.md` Example 1) | compact/standard preset + baseline sequence |
| Existing work-pack / SWU as source, skip seed creation (`TASK-MATRIX.md` refine-existing-target-medium; `SELF-REFINEMENT-2026-05-24.md` "Seed needed: no" branch, lines 44-48) | seed-needed decision (process step 1, `SKILL.md` line 290), not a mode |
| Blocked: missing dispatch/handoff/receipt (`TASK-MATRIX.md` refine-blocked-medium; `VALIDATION.md` line 19 "Status: block" as valid evidence) | block path is intrinsic to every stage, not a mode |
| Broad architecture/package refinement (`TASK-MATRIX.md` refine-observability-complex; `LIVE-EXAMPLE-SEEDS.md` Example 2) | full/deep preset + `xray_for_hidden_structure` overlay |
| Next-route recommendation after synthesis (`TASK-MATRIX.md` refine-next-route-complex) | post-synthesis step (process step 16), not a mode |

Every observed class is reachable by (preset × overlay × seed-needed decision).
No observed class required a control-flow variant that the existing axes cannot
express. This is direct evidence *against* mode proliferation.

## Candidate modes, judged on earned-or-not

1. **"discovery vs design vs plan" output modes** — REJECT as proliferation.
   The ten-stage loop already *contains* Define, Design, and Plan as ordered
   stages (`SKILL.md` lines 44-51). The user's desired output (seed / design /
   non-executed plan) is named in the description line 3 and selected by the seed
   proposal's "done criteria" field (process step 3, `SKILL.md` line 292), not by
   forking the loop. Splitting these into modes would re-introduce the exact
   drift the design rejected in `SELF-REFINEMENT-2026-05-24.md` (Distill rejected
   "Add a new refinement engine ... Duplicates REFINEMENT-LOOP.md and increases
   drift risk", lines 83). No observed failure earns it.

2. **"existing-work-pack preflight" mode** — REJECT; it is a *decision*, not a mode.
   The self-refinement run found a real gap (SELF-REFINE-001, medium: examples
   only covered seed + blocked, not the existing-work-pack branch,
   `SELF-REFINEMENT-2026-05-24.md` lines 56-57). But the fix it chose was an
   *example + the "Seed needed: no" branch* inside the same loop (lines 44-48,
   90-100), explicitly keeping the "seed/preflight controller" as the single
   selected unit (Distill, lines 76-85). The gap was a documentation gap, not a
   missing mode.

3. **"blocked / preflight-only" mode** — REJECT; block is a universal verdict.
   Observed `Status: block` runs (`VALIDATION.md` line 19) are explicitly "valid
   blocked evidence, not promotion evidence" produced by the *same* loop hitting
   a missing-field gate. The harness already distinguishes a proposal from
   manifest-backed loop evidence (`VALIDATION.md` line 15) without a separate
   mode. Making block a mode would let a run *choose* to stop early — the opposite
   of the contract's intent.

4. **"broad architecture / repository-area" mode** — REJECT; covered by preset+overlay.
   The one complex live target (observability package, `LIVE-EXAMPLE-SEEDS.md`
   Example 2) expects "full architecture/design refinement seed" reachable by
   `full`/`deep` preset plus the hidden-structure overlay. No stage needed to be
   added or removed.

5. **A genuine *interaction* mode: proposal-only vs run-through.** — EARNED, but it
   already exists as the permission gate, not a new mode. The single most
   load-bearing observed failure is `REFINE_LIVE_VALIDATION=flag`: "sigil-new-low
   output does not prove the refinement loop ... executed through required stage
   evidence" — the run "can only produce a proposal"
   (`development/runs/20260524T225248Z.md`; `LIVE-EXAMPLE-SEEDS.md` Example 1
   "flag or block the run if it can only produce a proposal"). This is a real,
   recurring gap (proposal produced, loop not executed). But the contract already
   has the two states as a *gate*: the `Refine Run Strategy Proposal` then a
   human permission gate before runtime-backed stages (`SKILL.md` lines 77-99,
   222-251). The fix is hardening that gate's *completion accounting*
   (flag/block when only a proposal exists), not adding a mode. Parameterize, do
   not proliferate.

## Verdict

**No new MODE is earned.** Every observed problem-class and every observed
failure is reachable through the existing three parameterization axes — presets
(budget), technique overlays (per-stage config/gates), and the seed-needed +
permission decisions inside the single canonical loop. The internal evidence
actively argues against modes: the only design alternative that *was* a mode-like
fork ("Add a new refinement engine") was explicitly rejected for drift risk
(`SELF-REFINEMENT-2026-05-24.md` line 83), and the self-refinement gaps were
closed with examples and a decision branch, not a fork.

The one real, recurring failure (proposal emitted but loop not executed) is a
**gate-accounting bug in the single loop**, not a missing mode. Recommended
improvement, framed as parameterization not modes:

- Harden the proposal→run completion gate: a materialized run that stops at the
  proposal must record `flag`/`block` with the missing stage evidence (already
  the harness's intent, `runs/20260524T225248Z.md`), so "proposal-only" can never
  silently pass as a completed refinement.

Modes considered and rejected as proliferation: output-mode (discovery/design/
plan), existing-work-pack mode, blocked/preflight-only mode, broad-architecture
mode. Each collapses into a preset, overlay, or decision the loop already owns.


================================================================
## LANE FILE: g2-spivak-maximal-reuse.md
================================================================

# g2 — Spivak lane: maximal principled reuse of the subagents-strategy machinery in `/refine`

**Lens:** FORMAL / integration. Treat `/refine` as a *consumer* of the dispatch
algebra, not a parallel orchestrator. Each subagents-strategy mechanism is a
morphism that already exists; refine should compose them, not re-invent them.

**Problem (lane-independent):** `/refine` runs a single deterministic track —
the canonical ten stages, each one owner, each one critic — so the *design* it
elaborates is never confronted by a structurally opposed design. Its critique
stages (Interrogation, Distill repair) attack *the artifact's quality*, never
*the artifact's framing*. That is the anchoring failure TWO-LANE-DISCIPLINE.md
names: "shipping the first framing because nobody was assigned to disagree with
it" (`TWO-LANE-DISCIPLINE.md`, Lane A rationale). Refine's own
`anti-patterns` warns against freeform prose replacing stages, but says nothing
about framing monoculture (`arcanum/arcana/refine/SKILL.md` §anti-patterns).

The subagents-strategy stack is exactly the missing apparatus: it manufactures
*structurally opposed* agents and proves the opposition before a human commits.
Below, each mechanism is mapped onto one refine stage or overlay.

## The mapping (mechanism → refine stage/overlay)

| subagents-strategy mechanism | refine stage / overlay it owns | how |
|---|---|---|
| `dispatch_type: research` | **Stage 4, Research Decision** (`bounded-research` / `research-if-gap-appears`) | Refine already has a research decision; today it is unregistered. Make `bounded-research` and any `if-gap` trigger emit a real `research` dispatch with a `working_folder` (research requires one — `register-dispatch` top-level table, `working_folder`). This is a pure widening: the stage's "named external-context gap" (`SKILL.md` §research-policy) becomes the dispatch `goal`. |
| `dispatch_type: review` | **Stages 3, 7, 10** (Interrogation `refine-review` / `refine-design-review` / `refine-final`) | Each interrogation is a single-agent critique today. Re-cast as a `review` dispatch — inline by default, so no `working_folder` cost (`register-dispatch`, `working_folder` "Optional for `review`"). Review judgment (attack lenses, severity taxonomy) is owned by the review type skill; refine stops defining critique form and routes to it. |
| `dispatch_type: experiment` | **`toy_game_for_low_cost_falsification` overlay** (already in `SKILL.md` §technique-overlay-policy) | The overlay says a selected abstraction may need "a controlled failure test before planning." That is precisely an `experiment` dispatch: a criterion frozen *before* the probe, verdict SURVIVED/FALSIFIED/INVALID (`domainspec-subagents-strategy` routing table; criterion is a `working_folder` artifact, never a column). The overlay fires between Distill (5) and Invoke Design (6). |
| **anti-bias vector composition** | **the seed/dispatch-design step** (process steps 4–5) where the *second lane* is authored | This is the load-bearing reuse. To break single-track, refine must spawn an n≥2 **subject group** whose two agents hold *opposed framings* of the same underlying problem. Anti-bias composition is the design rule for that opposition: micro-vectors "structurally opposed … not merely non-overlapping" (`anti-bias-vector-composition/SKILL.md`, principle). Map the canonical axes onto framing: Lane Z = advocate angle, Lane A = alternative-framing angle, tensioned on the **methodology** or **source-corpus** axis (closed vocabulary, same skill §four-canonical-axes). The `anti_bias` axis names *why the two refinements cannot collapse into one*. |
| **check-tension gate (Tests 1–4)** | **a new gate inside the strategy-preview/permission step** (process steps 7–8) | Refine already pauses for a human "Run Strategy Proposal" confirm. Insert the check-tension gate *before* that human confirm, exactly where the router places it ("between Propose and Confirm" — `check-tension/SKILL.md` §when-it-runs). The two independent agents verify the two refinement lanes are genuinely tensioned (Test 2 clone / Test 4 evidence) so the human never confirms a fake-opposition pair. This is the formal guarantee that the two-lane discipline is *real*, not decorative — directly answering TWO-LANE-DISCIPLINE.md's "honest only if it ran the idea into at least one real counterexample." Gate agents are infrastructure: no ledger row, not self-gated (`check-tension` §infrastructure). |
| **register-dispatch ledger (two appends, `exit_reason` vocab)** | **fused with the run-manifest contract** (`RUN-MANIFEST.md` / `evidence-index.json`) | Refine's manifest is a private evidence folder; the dispatch ledger is the repo-wide append-only record. Make every refine-spawned dispatch (research, the review interrogations, the experiment overlay, the two-lane subject group) emit its **dispatch row at spawn** and **close row at termination** (`register-dispatch` §two-appends, P3 append-only). Refine's per-stage `pass\|flag\|block` verdicts map onto the close-row `exit_reason` closed vocabulary `resolved \| loop_ceiling_reached \| dissent_irreconcilable \| user_abort \| error`. Crucially: a two-lane synthesis that cannot adjudicate closes `dissent_irreconcilable`, not `pass` — refine gains a *first-class vocabulary for honest non-convergence* it currently lacks. `max_loops`/`loop_cap`/`layers` (three dials, three scopes) replace refine's ad-hoc preset budget knobs. |
| **robot_talks** | **the Final Interrogation → synthesis seam** (stage 10) and the two-lane join | P7: `robot_talks: true` → the group *synthesizes* rather than concats; a downstream synthesizer "MUST receive each agent's initial AND final positions" (`domainspec-subagents-strategy` P14). Refine's final synthesis is the natural adjudicator of the two lanes — bind the two-lane subject group `robot_talks: true` so the lanes discuss and the synthesis sees collapse vs. genuine-convergence. This *is* TWO-LANE-DISCIPLINE.md's "synthesis (adjudication)" step, with its bridge-decision verdicts (`borrow-carefully \| analogy-only \| block \| promotion-candidate \| future-work`) recorded as the refine `RESULT.md` per-claim verdicts. |

## What refine becomes

A first-class dispatch consumer: the canonical ten stages stay, but stages 3/4/7/10
and the toy-game overlay each *route to a LIVE dispatch_type* instead of running
private single-agent prose. The single track splits into a tensioned n≥2 subject
group (anti-bias composition designs it, check-tension proves it, the human
confirms it once), and every spawned dispatch lands two rows in the shared ledger
with honest `exit_reason`s. `final_approver: parent` stays the one human gate
refine already has (P12 / `SKILL.md` §strategy-preview-and-permission).

## Boundary the maximal version must respect

The two-lane group is a **subject group** (`investigate`/`evaluate`), so anti-bias
applies; the synthesis writer and any auditor are single-owner and are *not*
gate-checked (`anti-bias-vector-composition` §where-it-applies). Refine must not
register its check-tension agents (infrastructure, no row). And refine stays
non-executing: bridge decisions are local, promotion needs a separate
`task-session` (TWO-LANE-DISCIPLINE.md §synthesis) — consistent with refine's
existing "Task Session … out of the loop except as optional next-route"
(`SKILL.md` §quality-bar).


================================================================
## LANE FILE: g2-goldratt-minimal-reuse.md
================================================================

# Lane G2 — Goldratt minimal-reuse: what /refine should *borrow*, not *import*

**Lens:** Theory-of-Constraints / adversarial-cost. Every mechanism imported from the
subagents-strategy machinery is judged by one test: does relieving refine's binding
constraint pay for the coupling and maintenance it adds — or does it just add another
unused technique name to the route?

That failure mode is already named by refine itself: a successful run must
"select technique overlays based on target evidence rather than **decorating the route
with unused technique names**" (`refine/SKILL.md` quality-bar, line 314; restated at
line 322: "cite dispatch techniques only when they are expressed by steps, gates,
handoffs, or validation notes"). So refine has *already declared* that importing
vocabulary it does not exercise is a defect. The adversarial-cost lens just extends that
rule from techniques to whole mechanisms.

## The bottleneck constraint

Refine is not throughput-bound (its ten stages are fixed and cheap to schedule) and not
quality-bound at the artifact level (each stage capability owns its own validation). Its
binding constraint sits at **one point**: the moment refine decides to *spawn
role-bound sibling subagents* and present that decision to the operator.

That is the only place where refine's output can be *systematically wrong rather than
merely thin*. Everywhere else a weak stage produces a weak-but-honest artifact. But when
`subagent_strategy.status` is `recommended`/`required` (`refine/SKILL.md`
strategy-preview, lines 88–97; process step 11, line 300), refine spawns n≥2 agents
whose returns it then synthesizes — and if those agents share a hidden bias, refine
synthesizes a **confidently false** seed/design/plan and hands it forward as the run
deliverable. A correlated-bias sibling set is the one input that defeats refine's own
downstream interrogation, because the critique stage inherits the same blind spot.

**The constraint to relieve: refine's multi-agent stages can emit a confident synthesis
over agents that were never verified to be genuinely tensioned.** Refine already requires
operator *permission* to spawn (lines 93–97), but permission is a willingness gate, not a
bias gate — the operator confirms *that* subagents run, not *that they disagree by
design*. Relieving this constraint improves refine more than any other change because it
is the only defect that is silent.

## Mechanism-by-mechanism: borrow as discipline vs import as dependency

| Mechanism | Subagents-strategy role | Pays for itself in refine? | Verdict |
|---|---|---|---|
| **check-tension** | Two independent agents run validator Tests 1–4 before the human confirm; only "both PASS" advances (`check-tension/SKILL.md` lines 6–58) | **Yes — directly relieves the bottleneck.** Refine's only systematically-wrong output comes from untensioned siblings; this is the exact gate. | **BORROW as discipline** |
| **anti-bias vectors** | Design principle behind P5 pairwise tension (router line 29) | Yes, but only as the *content* of the discipline above — refine needs the four-test rubric, not a second skill dependency. | **BORROW (subsumed by check-tension)** |
| **dispatch_types** | Router routes by `research \| review \| experiment` (LIVE) to type skills (router lines 43–50) | **No.** Refine's stages are already typed by capability (`invoke`, `interrogation`, `distill`); a second type taxonomy adds a parallel routing surface with no new decision. | **IMPORT-only-if-already-spawning** |
| **ledger / register-dispatch** | Append-only telemetry, two rows per dispatch (`register-dispatch/SKILL.md` lines 8–13) | **Partly.** Refine already materializes its own run manifest + evidence-index (`refine/SKILL.md` lines 169–191). A second append-only ledger duplicates that bookkeeping. | **IMPORT only when refine actually fans out** |
| **robot_talks** | Group synthesizes vs concats; P7/P14 binding (router lines 30, 37) | **No.** Refine owns its *own* final synthesis stage (`refine-final`, line 50; ownership-boundary line 255). Importing robot_talks would put a second synthesis owner inside a loop that already has one. | **DO NOT IMPORT** |

## Why most of it is discipline, not dependency

The adversarial cost of *importing* (taking a dependency) is threefold: (1) refine must
track the imported skill's version and re-validate when it changes; (2) refine's route
gains fields/enums it may not exercise — the exact "decoration" its own quality-bar
forbids; (3) two owners now touch the same concern (e.g. synthesis: refine-final *and*
robot_talks), violating the single-owner boundary refine already maintains
(ownership-boundary, lines 253–264).

The adversarial cost of *borrowing as discipline* is near-zero: refine adopts the
**behavior** (verify tension before synthesizing over siblings) without inheriting the
**form** (a registered dispatch row, a dispatch_type, a robot_talks flag). The
subagents-strategy machinery is, on this lens, a *worked example of how to do
multi-agent work safely* — and refine should copy the lesson, not link the library.

Concretely:

- **The one import that pays:** a check-tension-shaped gate, but **scoped to refine's
  own spawn point** (process step 11). Refine already stops for operator permission
  there; add a tension check *before* that stop, so the operator only ever confirms a
  sibling set that an independent double-check found genuinely tensioned — mirroring the
  router's "the human Confirm only ever sees a sheet that passed an independent
  double-check" (`check-tension/SKILL.md` line 58). This is one gate at one place, not a
  new dependency graph.

- **Everything else stays discipline.** Refine cites anti-bias *reasoning* in its seed
  proposal's subagent section; it does **not** grow a `dispatch_type`, a second ledger,
  or a `robot_talks` field. If a refine run ever genuinely fans out beyond its own loop
  (the helper-vs-dispatch boundary, router P11, line 14 — itself "provisional"), *that*
  is the trigger to register in the real ledger — not refine's default path.

## Bottom line

Refine has exactly one silent-failure constraint: synthesizing over un-verified-tensioned
siblings. Relieve it by **borrowing check-tension's discipline at refine's existing spawn
gate** — the four-test verification of pairwise tension before the operator confirm.
Borrow anti-bias as the rubric content of that gate. **Import** the ledger and
dispatch_type only on the rare path where refine truly fans out beyond its own loop.
**Do not import** robot_talks at all — refine already owns its synthesis. The rest of the
machinery is a lesson to copy, not a library to link; importing it would be precisely the
"unused technique name" decoration refine's own quality-bar already prohibits.


================================================================
## LANE FILE: g3-gigerenzer-early-gate.md
================================================================

# Lane G3 — Gigerenzer Early Gate

Status: lane proposal (refine-improvement)
Stance: break anchoring **early and cheap** — a fast-and-frugal gate, not a heavyweight late audit.

## The question this lane answers

WHERE and HOW should refine break anchoring? This lane argues the break must
happen at the **front** of the loop — in the seed and at Distill (stage 5) —
before Design (stage 6) commits resources to one framing. The canonical loop
selects THE coherent unit at Distill and then designs from it at Redefine /
Design (`arcanum/arcana/refine/SKILL.md` `<canonical-loop>` stages 5–6). Once
Design runs, every downstream stage (Interrogation 2, Distill Repair, Plan,
Synthesis) inherits that unit. So the anchor that matters is set *at Distill*,
and the only cheap place to challenge it is *before or at* Distill.

## Why early-and-cheap (fast-and-frugal)

The expensive failure mode is anchoring: "shipping the first framing because
nobody was assigned to disagree with it"
(`projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md`, Lane A rationale).
A full second lane (a parallel Lane-A alternative solution) is the thorough fix,
but it doubles design cost. A Gigerenzer-style move is the opposite bet: one
fast heuristic placed at the decision point beats an exhaustive parallel search
that arrives too late and over budget. The `compact` preset, where most refine
runs will live, explicitly wants "shortest stage outputs" and a repair pass that
"may block quickly" (`SKILL.md` `<preset-policy>`). An early gate fits that
budget; a second design lane does not.

## Mechanism (two cheap moves, both before Design)

### (a) Required solution-independent underlying-problem field in the seed

Add a REQUIRED field to `REFINE-SEED-PROPOSAL.md` (today the seed carries
"target, source context, write scope, done criteria, validation surface, preset,
research mode, and planned stage configuration" — `SKILL.md` process step 3;
no problem field). The new field must:

- state the **underlying problem solution-independently** — the gap, not the fix.
  This is the discipline's "name the gap before naming the fix"
  (`TWO-LANE-DISCIPLINE.md`, "Stating the underlying problem"), pulled forward
  into refine's seed.
- state the problem in **2+ framings** (e.g. "specs drift from code" vs. "code
  has no machine-checkable contract"), and **choose one with a recorded reason**.

Two framings cost a sentence each. They force the author to notice that the
problem itself is a choice, which is precisely where anchoring takes hold. The
recorded reason makes the choice auditable later (the run manifest already
indexes seed artifacts — `SKILL.md` `<run-manifest-contract>`).

### (b) A falsification gate at Distill, before Design

Distill "selects THE coherent unit" (stage 5). Before that unit is allowed to
pass into Design (stage 6), it must **survive one pre-registered
counterexample** — a single failure case written down *before* Distill runs, not
discovered afterward. This borrows the discipline's honesty test: a pass is
honest "only if it ran the idea into at least one real counterexample, not just
a friendly demo" (`TWO-LANE-DISCIPLINE.md`, Lane Z). It also matches refine's
existing optional `toy_game_for_low_cost_falsification` overlay, which calls for
"a controlled failure test before planning" (`SKILL.md`
`<technique-overlay-policy>`) — but this lane makes a minimal version
**required and earlier** (at Distill, not at Plan), not opt-in.

Gate verdict: the distilled unit either SURVIVES the pre-registered
counterexample (proceed to Design) or is FALSIFIED (return to Distill / Define
with the counterexample recorded as residue). The counterexample is registered
in the seed alongside the chosen problem framing, so it cannot be retrofitted to
whatever Distill happens to produce.

## Claim: the anchor forms early, in Distill

The load-bearing claim is that anchoring is *already set* by the time stage 5
ends. Distill's job is to pick one unit (`SKILL.md` `<required-capabilities>`,
distill row: "Select the coherent unit"). Every later stage refines that pick;
none re-opens it cheaply. Therefore an anti-anchoring intervention placed after
Distill is fighting sunk design cost, while one placed *in the seed and at the
Distill boundary* is nearly free. Break it where it forms.

## Honest weakness

A pre-registered gate can be satisfied **perfunctorily**. An author who has
already anchored will pick a *weak* counterexample — one the favored unit was
always going to survive — and a *cosmetic* second framing that is really the
first framing reworded. The gate then certifies the anchor instead of breaking
it. Pre-registration controls *timing* (you can't retrofit the test), but it
does **not** control *adversariality* (you can pre-register a friendly test).
This is the exact gap the two-lane discipline closes with a *separate owner* for
Lane A — divergence enforced by independence, not by the advocate's good faith.
The early gate trades that guarantee away for speed: it assumes the author will
write a genuinely hostile counterexample, and that assumption is unenforced. A
cheap partial mitigation is to require the counterexample come from a different
problem framing than the chosen one (so the two cheap moves reinforce each
other), but this narrows perfunctoriness without eliminating it.


================================================================
## LANE FILE: g3-hewitt-late-dispatch.md
================================================================

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
