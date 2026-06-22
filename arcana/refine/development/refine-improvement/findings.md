# Refine-Improvement Synthesis — findings.md (post-review final)

Dispatch: 2026-06-18-refine-improvement-strategy
Discipline: `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md`
Synthesizer adjudicates eight lanes (G0–G3); zig-zag revised once against G5
reviewers (Kahneman non-vacuity; Wittgenstein definitional). Claims demoted to
proof, never inflated.

## 0. What the review changed (revision log)

The draft anchored its #1 move on **delivery is the binding constraint** (C1),
inferred from ONE blocked run (`20260524T225844Z-sigil-new-low`, pass=0 block=10)
plus the fixture harness. Kahneman built the missing witness: the live x-ray
refinement runs of 2026-05-29 → 05-31. I verified them directly
(`arcana/x-ray/development/refinement-runs/*/evidence-index.json`):

```
20260524T225844Z-sigil-new-low:        10 stages  pass=0  block=10  (the cited run)
20260529T110749Z-visual-layered-xray:  10 stages  pass=8  block=0
20260529T122108Z-component-library:    10 stages  pass=9  block=0
20260529T124546Z-schema-readiness:     10 stages  pass=9  block=0  flag=1
20260530T010327Z-ui-playwright-repair: top-level Status only (no stage array)
20260531T152122Z-arcanum-xray:         no evidence-index
```

Three runs reach all ten stages with **no blocked stage** (two with top
`status: pass`, one `flag`; pass=8–9, block=0), a real `## Final
Synthesis`, and a `## Recommended Next Route`
(`20260529T124546Z-schema-readiness/RESULT.md`, verified: named ordered routes
`SWU-XRAY-VIS-006A`/`006B`, explicit "keep `SWU-XRAY-VIS-005` first"). Therefore
"runs reliably block" / "zero end-to-end refinements" is **false on current
evidence**. Four changes follow:

1. **C1 DEMOTED** from binding-constraint/first-move to a dated, narrow claim
   (cold-target brittleness). Delivery-first is no longer evidenced. Re-ranked.
2. **C3 SHARPENED** to a concrete refine-internal RESULT.md predicate (the
   circular "would Task Session accept this?" is dropped) — the passing runs
   satisfy it, the blocked run does not.
3. **C5 SPLIT** — converge/diverge/strengthen/evaluate killed as re-skins of
   existing machinery; only `reframe` carried forward and merged into C10/G3-Hewitt.
4. **C6 KEPT** but re-billed as **measurement-honesty**, decoupled from C1.

## 1. What each lane actually solved vs. only reframed

### G0 — challenges the problem

- **G0-Meadows (structural friction / blocking).** Witnessed a real defect ON THE
  05-24 cold run (all ten stages blocked; sigil stuck `pilot`,
  `REFINEMENT-LOOP.md:6`) AND a real *measurement* defect: the harness reports
  health on empty runs (`runs/20260525T002839Z.md` records
  `REFINE_LIVE_VALIDATION=pass` over the all-blocked artifact). But the
  generalization "runs do not reach value" is **falsified** by the three later
  passing x-ray runs. What survives is: (a) cold-target delivery is brittle
  (narrow, dated); (b) the measurement is dishonest (this is C6, and it is the
  durable finding).
- **G0-Christensen (outcome-blindness at the handoff).** SOLVED a distinct,
  still-live problem: the three load-bearing outputs are tested for loop
  integrity, never for fitness. The *contract* has no fitness test (F1
  `SKILL.md:49`; F2 quality-bar `SKILL.md:308-326`; F3 route free-text
  `result.md:38-40`). Note the empirical nuance Kahneman surfaced: the passing
  runs *do* emit decidable, named routes — so F3 is "contract silent," not
  "outputs vacuous." This sharpens C3 rather than killing it.

### G1 — do we need new modes

- **G1-Simon (internal evidence): NO new mode earned.** Every problem-class maps
  to preset × overlay × seed-needed decision; the one mode-like fork ("add a
  refinement engine") was rejected for drift
  (`SELF-REFINEMENT-2026-05-24.md:83`). The one recurring real failure is
  proposal-emitted-but-loop-not-executed — a gate-accounting bug
  (`runs/20260524T225248Z.md`).
- **G1-Alexander (external precedent): 5 modes.** Analogy-only; no internal
  witness. After Wittgenstein's collapse test, four of the five are re-skins.

**Adjudication: G1-Simon wins on evidence.** Of Alexander's five modes, only
`reframe` survives the collapse test (it operates on the problem-unit; no current
overlay re-states the problem). It is merged into C10. The rest are killed (see §C5).

### G2 — integration

- **G2-Goldratt (minimal reuse): BORROW check-tension's discipline at refine's
  existing spawn gate; do not import ledger/dispatch_type/robot_talks.** Refine
  has NO anti-bias gate at its spawn point, so this is genuinely new, not a re-skin.
- **G2-Spivak (maximal reuse).** Terms well-defined but referents empty under
  current behavior (stages 3/4/7/10 do not yet produce tensioned siblings).
  `future-work`.

**Adjudication: Goldratt wins on cost.**

### G3 — where to break anchoring

- **G3-Gigerenzer (early/cheap):** pre-registered falsification gate at Distill.
  Self-admitted weakness: controls timing, not adversariality.
- **G3-Hewitt (late/strong):** Distill emits a *solution-independent problem
  statement*; Lane A forks the problem, not the unit. This IS the `reframe`
  mechanism. Strongest anti-anchoring design — but future-work.

**Adjudication: both SOUND on the conditional "if anchoring is the binding
constraint."** That conditional is now *weaker still*: with runs finishing,
anchoring is the plausible next-order quality concern, but it is unwitnessed.
Anti-anchoring stays future-work; C10 (= reframe = Hewitt) leads it.

## 2. Bridge decisions per load-bearing claim

| # | Load-bearing claim | Rests on (cite) | Bridge decision |
|---|---|---|---|
| C1 | Cold-target delivery is brittle (one run blocked all 10 stages) — does NOT generalize | G0-Meadows (`20260524T225844Z-sigil-new-low/evidence-index.json` pass=0 block=10) | **borrow-carefully (dated/narrow)** |
| C2 | Front-loaded scaffold taxes path-to-first-value | G0-Meadows Claim 3 (`SKILL.md:54-75,177-185`) | **borrow-carefully** |
| C3 | Output *contract* has no fitness test; outputs can be unhireable | G0-Christensen (`SKILL.md:308-326`; `result.md:38-40`) | **promotion-candidate (with predicate below)** |
| C4 | No new mode earned; variation carried by preset×overlay×decision | G1-Simon (`SELF-REFINEMENT-2026-05-24.md:83`) | **borrow-carefully** |
| C5 | Four of five external modes are re-skins; only `reframe` is new | G1-Alexander + Wittgenstein collapse test | **rejected (4) / fold into C10 (`reframe`)** |
| C6 | `REFINE_LIVE_VALIDATION=pass` co-exists with blocked output — mismeasurement | G1-Simon + validator (no rule requiring non-blocked RESULT.md); `runs/20260525T002839Z.md` | **promotion-candidate (measurement-honesty)** |
| C7 | Borrow check-tension discipline at spawn gate; not form | G2-Goldratt (`check-tension/SKILL.md:6-58`) | **borrow-carefully** |
| C8 | Maximal dispatch-algebra integration | G2-Spivak (referents empty today) | **future-work** |
| C9 | Early cheap anti-anchor gate at Distill | G3-Gigerenzer (unenforced adversariality) | **future-work** |
| C10 | Distill emits solution-independent problem statement (= `reframe`); late governed fork | G3-Hewitt + C5 `reframe` | **future-work (leading anchoring candidate)** |

### Definitions pinned (per Wittgenstein change-asks 2 & 4)

- **"Completed run"** (shared by C1 and C6, authored once): the loop produces the
  preset's declared terminal artifact (seed | design | non-executed plan) with
  **no blocked required stage**. C6 = the gate that *enforces* this; C1 = the path
  change that makes it *satisfiable* on cold targets. They are not independent.
- **"Hire-ability" (C3), operational, refine-internal, non-circular:** a
  `RESULT.md` passes iff its `## Recommended Next Route` names ≥1 route as an
  existing-or-proposable owner unit (SWU/task id) carrying (i) a stated
  precondition/ordering, (ii) a done-criterion, and (iii) no unresolved blocker —
  i.e. the `dispatch-spec`/`task-session` *input contract* as the fitness
  predicate. **Verified discriminating:** `schema-readiness/RESULT.md` satisfies
  it (`SWU-XRAY-VIS-006A/006B`, "keep VIS-005 first"); the all-blocked 05-24 run
  does not. This replaces the circular "would Task Session accept this?".

### Top 3 bridge decisions (most load-bearing, re-ranked)

1. **C6 promotion-candidate** — measurement-honesty; the one accept-tier item that
   survived a fresh witness intact. Make the harness stop reporting health on
   empty runs.
2. **C3 promotion-candidate** — now buildable: a concrete RESULT.md route predicate.
3. **C2 borrow-carefully** — keep path-to-first-value lean (the brittleness C1 saw
   on cold targets is real even though it does not generalize).

## 3. Verdict matrix

| candidate | owner | witnessed? | sound? | verdict | use-mode |
|---|---|---|---|---|---|
| Gate-accounting / health-on-empty-runs fix (C6) | harness owner | yes (validator + run) | yes | accept | promotion-candidate |
| Hire-ability route predicate (C3) | refine + ownership-boundary review | yes (passing vs blocked run discriminate) | yes | accept | promotion-candidate |
| Lean path-to-first-value (C2) | refine-sigil maintainer | partial | yes | accept | borrow-carefully |
| No new mode earned (C4) | refine-sigil maintainer | yes (internal) | yes | accept | borrow-carefully |
| check-tension discipline at spawn gate (C7) | refine-sigil maintainer | partial | yes | accept | borrow-carefully |
| Cold-target delivery brittleness (C1) | refine-sigil maintainer | yes (one dated run only) | yes (narrow) | accept-narrow | borrow-carefully |
| `reframe` mode (ex-C5) folded into C10 | future design lane | no | yes | defer | future-work |
| converge/diverge/strengthen/evaluate (ex-C5) | — | no | re-skins | reject | killed |
| Maximal dispatch-algebra integration (C8) | dispatch-spec owner | no | referents empty | defer | future-work |
| Early Distill anti-anchor gate (C9) | future design lane | no | partial | defer | future-work |
| Late governed Design fork + reframe (C10) | future design lane | no | yes | defer | future-work |

## 4. Ordered recommendation — what to do to /refine first

Delivery-first is OUT (C1 does not generalize; three live runs finish). The
binding issue is **measurement honesty then fitness**: the harness must stop
certifying empty/blocked runs as healthy, then refine's handoff must carry a
checkable acceptance predicate.

1. **Fix the measurement (C6 — first, cheapest, highest-trust).** Make
   `REFINE_LIVE_VALIDATION` require a **completed run** (per §2 definition: terminal
   artifact, no blocked required stage). A run that stops at the proposal records
   `flag`/`block` with the missing-stage evidence. Stops health-on-empty-runs.
2. **Add the hire-ability route predicate at the handoff (C3).** Enforce the
   §2 RESULT.md predicate (named owner-unit route + precondition + done-criterion +
   no open blocker). Passing x-ray runs already satisfy it; make it a gate, not luck.
3. **Keep path-to-first-value lean on cold targets (C1+C2).** Cold-start
   brittleness is the residue of the 05-24 run; ensure a refined seed is reachable
   without a fully validated `REFINE-DISPATCH.json`. Not a system-wide rebuild.
4. **Then, on finished loops, borrow check-tension's discipline at the spawn gate
   (C7)** — behavior, not form.
5. **Defer anchoring fixes (C8, C9, C10) to future-work.** Promote C10
   (Distill emits the solution-independent problem statement = `reframe`, the one
   surviving mode) as the leading anchoring candidate when a problem-class the
   existing axes cannot express is actually witnessed.

## 5. Residue (named owners)

- The five later live runs must be re-read before any future "runs block" / "zero
  end-to-end" claim; do not anchor on the first materialized artifact. — Owner:
  synthesizer (this revision discharges it once).
- Does the C3 route predicate belong to refine or overlap Dispatch Spec territory
  (`SKILL.md:255`)? — Owner: ownership-boundary review.
- C6 and C1 share one "completed run" definition; if it drifts, the gate and the
  path-fix decouple incoherently. — Owner: harness owner + refine maintainer (joint).
- Pre-registered anti-anchor gates control timing not adversariality
  (G3-Gigerenzer); only a separate owner fixes it. — Owner: future design lane.
- `reframe` is the only surviving novel mode and is still unwitnessed; revisit only
  when a finished loop surfaces a problem-class existing axes cannot express. —
  Owner: refine-sigil maintainer / future design lane.
- Deep upstream anchoring at Context Builder (stage 1) is untouched by any
  Distill/Design-stage fork (G3-Hewitt residual). — Owner: future design lane.

---
Zig-zag note: this is the final revised version (loop_cap 2, one revision used).
Every accept claim cites a witnessed artifact; C1 is explicitly narrowed to one
dated run after Kahneman's falsification; C3's predicate is verified to
discriminate passing vs blocked runs; C5's four re-skins are killed per
Wittgenstein with named existing owners; C6 is re-billed measurement-honesty and
decoupled from delivery. Claim ≤ proof throughout.

---

## Dispatch close

- **dispatch_id:** `2026-06-18-refine-improvement-strategy` (`dispatch_type: research`)
- **exit_reason:** `resolved` — final_approver (Vlachopulos auditor) ACCEPTed after the P9 citation check; one minor wording flag fixed (§0: "no blocked stage", two `pass`/one `flag`).
- **agents_spawned:** 12 total — explorer 8, writer 1, skeptic 2, auditor 1; loops_used 1 (one zig-zag revision). Plus 2 check-tension gate agents (infrastructure, unregistered).
- **One-line answer:** Fix the measurement first (C6 — stop certifying empty/blocked runs as healthy), then add a concrete RESULT.md hire-ability route predicate at the handoff (C3); delivery-first and the anchoring/two-lane fixes are **not** the first move.
