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
