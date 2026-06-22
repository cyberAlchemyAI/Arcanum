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
