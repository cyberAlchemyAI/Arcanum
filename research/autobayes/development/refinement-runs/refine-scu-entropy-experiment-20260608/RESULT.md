---
profile: refine
run_id: refine-scu-entropy-experiment-20260608
type: refine-result
status: pass
preset: full
research_mode: no-research
dispatch: REFINE-DISPATCH.json
dispatch_validation: pass
last_updated: 2026-06-08
---

# Refine Result — How to Measure the SCU Entropy U-Curve

## Answer in one paragraph

You make "SCU is the local minimum of entropy" falsifiable by **stopping treating
entropy as one axis**. The tournament showed the most literal entropy proxy
(semantic-entropy dispersion) is **monotone *decreasing*, not U-shaped** — it is only the
*left* arm (under-determination). The U exists only when a descending **spread** arm
(`H_spread`) is composed with an ascending **overload/residue** arm (`E_energy`). So the
experiment measures three separate proxy curves against unit size, and the falsifiable
claim is not "a U exists" but "**the arms cross at an interior `r*` that is invariant
across coding choices and co-locates with blind-rated SCU quality.**" That is testable,
and it can fail.

## The experiment (what to actually build)

- **Independent variable:** unit size `r(u)` = cross-unit relations/obligations per unit,
  swept by **re-bundling the same obligations** on a fixed, difficulty-matched corpus
  (difficulty held constant — the key confound control).
- **Three separate y-axes (never blended):**
  - **Proxy A — semantic-entropy dispersion** (Miller–Madow-corrected semantic-cluster
    entropy over N=20 samples): measures `H_spread`; predicts the **descending left arm**.
  - **Proxy B — two-part MDL** `bits(schema|ctx)+bits(residue|repair)`: carries both arms
    by construction, so its U is free; its *content* is the **minimizer `r*`** and that
    `r*`'s **invariance** across reference models/serializations.
  - **Proxy C — residue / validation-failure rate** (per-obligation normalized, hard
    repair budget): measures the realized `E_energy` trace; predicts the **ascending right
    arm**; cheapest, run first as a screen.
- **Independent H2 axis:** a **blind SCU-quality rubric** (frozen, raters blind to size and
  proxy values).
- **Pre-registered prediction (the spine):** A descends, C ascends, B's `r*` is interior
  and codebook-invariant, and all minima co-locate with the blind-rubric quality peak.
- **Falsified if:** A is flat/rising (no real spread), or B's `r*` moves with the codebook
  (artifact), or all proxies are monotone, or minima don't track blind SCU quality.

## Why it can fail honestly (the hard part)

A two-part code *guarantees* a U, so a naive experiment is unfalsifiable. The pilot review
forced six pre-registration locks that make failure recordable — chiefly: **demote B's U
to zero-information** (only `r*` invariance + co-location count), and **cap Proxy C's
repair budget** so a flat overload arm cannot be re-narrated as "absorbed pressure." The
cheapest decisive test is the **pilot**: 4 sizes × 6 items × N=3 × 4 codings (~288 calls +
~24 blind ratings) measuring only B's `r*` dispersion and rubric co-location. If `r*` sits
at an edge or moves with the codebook, the program stops before any expensive sweep.

## Conceptual payoff

The refinement *sharpened the Craft claim itself*: "SCU = local minimum of entropy" is only
coherent if "entropy" means the **composite bundle** (`H_spread` + `E_energy` + `R_rel` +
`A_att`), not `H_spread` alone — empirically retro-validating the four-way split proposed in
the [entropy definition card](../../tracks/craft-entropy-definition-card.md). This is a
candidate input to residue **R1** (the term-split decision-gate); it does not edit the Craft
definition.

## Stage evidence

| Stage | Capability | Status |
|---|---|---|
| 1 Context baseline | context-builder | pass |
| 2 Invoke Define | invoke | pass |
| 3 Interrogation refine-review | interrogation | flag (4 repairs) |
| 4 Research decision | refine | pass (no-research) |
| 5 Distill select | distill | pass |
| 6 Invoke Design (tournament) | invoke + 3 subagents | pass |
| 7 Interrogation design-review | interrogation | flag (5 locks) |
| 8 Distill Repair (pilot) | distill + 1 subagent | pass |
| 9 Invoke Plan | invoke | pass |
| 10 Final synthesis | interrogation + refine | pass |

## Open residue / next routes

- **R3 (this run):** advanced from "unmeasured axis" to "falsifiable, pre-registered,
  pilot-scoped design." Remaining: actually run it — route to **`experiment-harness`**.
- **New residue R6:** the U is a *composition* of arms, not a single-axis property — feed
  back into R1 (term-split decision-gate) for the Craft definition owner.
- **Next routes:** `experiment-harness` (run Wave 0→1), then `decision-gate` on R1. No edit
  to `CRAFT-INITIAL-DEFINITION.md` from this run.
