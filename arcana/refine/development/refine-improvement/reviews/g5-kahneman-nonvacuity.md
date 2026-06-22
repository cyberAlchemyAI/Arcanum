# G5 Review — SKEPTIC, attack-vector NON-VACUITY (Kahneman)

Reviewer: G5 skeptic, zig-zag with synthesizer.
Method: for each accept-verdict candidate I built the smallest concrete witness —
does it do work, or pass trivially / without changing any refine outcome?

## Headline verdict

The synthesis is **internally coherent but evidentially stale**. The accept-tier
rests on ONE blocked run (`sigil-new-low`, 2026-05-24) and the harness
fixture-runs, while **five later live refinement runs (2026-05-29 → 05-31, committed
2026-06-01, seventeen days before findings.md) are never read**. Those runs
falsify the load-bearing C1 claim and materially weaken C3. The Kahneman trap I
was asked to guard against fired in reverse: a *witnessed-but-superseded* defect
was waved through as the current binding constraint.

## Witnesses built

### C1 (delivery is the binding constraint) — CUT to *partial / stale*

Smallest witness: enumerate every live refinement run, not just the cited one.

```
20260524T225844Z-sigil-new-low:        pass=0 flag=0 block=10   (the cited run)
20260529T110749Z-visual-layered-xray:  pass=8 flag=2 block=0
20260529T122108Z-component-library:    pass=9 flag=1 block=0
20260529T124546Z-schema-readiness:     pass=9 flag=1 block=0
20260530T010327Z-ui-playwright-repair: (empty index)
20260531T152122Z-arcanum-xray:         (no index)
```

(`arcana/x-ray/development/refinement-runs/*/evidence-index.json`.)

Three of these reach all ten stages with `Status: pass`, a real `## Final
Synthesis`, and a `## Recommended Next Route` (e.g.
`.../20260529T124546Z-schema-readiness/RESULT.md`). So "runs reliably block before
producing a refined seed" and "**zero** successful end-to-end refinements"
(findings §1 G0-Meadows; Lane A Claim 1–2) are **false against current evidence**.
C1 is real for the 05-24 run but does NOT generalize. It is inferred from one
blocked run plus the fixture harness, exactly the failure mode the prompt named.
**Change-ask: CUT C1 from "binding constraint / first move" to a narrow,
dated claim** ("the earliest live run blocked; delivery brittleness is real on
cold targets"), and re-rank — delivery is no longer demonstrably the binding
constraint.

### C3 (hire-ability gate) — SHARPEN; criterion is currently VACUOUS

Witness 1 (measurability): I tried to state a pass/fail for "hire-ability" from
the lane. It gives none — "would the next owner accept this?" has no checkable
predicate, so **any RESULT.md could claim to pass it**. As written, C3's gate is
the vacuous criterion the attack-vector targets. The lane itself defers this
(residue: "is hire-ability measurable inside refine, or only downstream").

Witness 2 (does the defect still hold?): F3 says recommended-next-routes is
"ungoverned free text" that fails the job. But `schema-readiness/RESULT.md`
emits **named, ordered, acceptance-checkable routes** (`SWU-XRAY-VIS-006A` lane
schema + validator; `006B` component schemas; explicit "keep VIS-005 first").
That is decidable and traceable to the synthesis. So F3's "least governed / no
acceptance criteria" claim is **already only partly true in practice** — the
output contract is silent, but produced routes are not vacuous.
**Change-ask: KEEP C3's diagnosis (the *contract* has no fitness test) but
SHARPEN to a measurable predicate before promotion** — e.g. "RESULT.md must name
≥1 route as an existing/proposable owner unit (SWU/task id) with an explicit
precondition," which the passing runs already satisfy and the blocked run does
not. Without a concrete predicate, do not promote C3; it is a relabel.

### C6 (proposal→run gate-accounting fix) — KEEP; non-vacuous, does real work

Witness: read the validator. `run-validation-fixtures.sh` accepts a stage with
`status: block` as long as it carries `blocked_reason`, and only emits `BLOCK`
when a stage claims `status: pass` with a missing artifact (lines ~226–250).
There is **no rule that REFINE_LIVE_VALIDATION require a non-blocked RESULT.md**.
Confirmed empirically: `runs/20260525T002839Z.md` records
`REFINE_LIVE_VALIDATION=pass` while the underlying live output was the all-blocked
artifact. So C6's proposed fix changes behavior — it is not present today and is
not a relabel. **Change-ask: KEEP C6, but it is mostly a measurement-honesty fix,
not a delivery fix** — it makes blocks legible, it does not make runs finish. Its
findings billing as "the cheapest win where Meadows + Simon converge" survives;
its implied coupling to C1-as-binding-constraint does not.

## Bias flag (Kahneman)

The redundancy guard: C1 and C3 are *witnessed* on the 05-24 run, which made them
feel "real," and the later passing runs were never queried — availability /
anchoring on the first materialized artifact. C6 is the one accept-tier item that
survives a fresh witness intact.

## Change-asks (compact)

- **CUT** C1 from binding-constraint/first-move → dated narrow claim; re-rank the
  ordered recommendation (delivery-first is no longer evidenced).
- **SHARPEN** C3: replace "hire-ability" with a checkable RESULT.md predicate
  (named owner-unit route + precondition); else it is vacuous — defer, don't
  promote.
- **KEEP** C6 unchanged in substance; re-bill as measurement-honesty, decoupled
  from C1.
- **ADD residue**: synthesis must read the live `x-ray/.../refinement-runs/`
  before any "zero end-to-end" / "runs block" claim. — Owner: synthesizer.
