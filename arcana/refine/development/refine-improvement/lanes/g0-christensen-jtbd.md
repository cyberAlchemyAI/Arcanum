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
