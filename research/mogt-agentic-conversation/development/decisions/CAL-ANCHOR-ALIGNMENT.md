---
name: MOGT Calibration Anchor-Alignment Decision
description: Decision record resolving the borderline-positive anchor disagreement before MOGT production reviewer scoring.
created: 2026-06-11
target_scope: mogt-reviewer-calibration
result: PASS
source_decision: user directive "conservative one" via decision-gate, 2026-06-11
governs:
  - MOGT-REVIEWER-CALIBRATION-SET.md
  - MOGT-REVIEWER-RUBRIC-DRAFT.md
---

# Decision: Borderline-Positive Anchor Alignment

## Context

Calibration scoring surfaced a single systematic disagreement before MOGT
production reviewer scoring could proceed. On borderline-positive decision
cases, a human reviewer scored more leniently than every model reviewer:

- The MODEL_Y lane flagged **3 rows** above the `0.25` adjudication threshold
  (`MOGT-REVIEWER-CALIBRATION-SET.md`, "Human vs MODEL_Y adjudication notes").
- A **6-model x 2-reviewer rig** (the pending MODEL_X lane) confirmed the same
  pattern: 5 models (Sonnet, Gemini, Grok, DeepSeek, Opus) form a tight
  consensus cluster (within-model max disagreement 0.00-0.10) that lands in the
  0.70-0.85 band on those rows, while the human gave 1.0. GPT-4o is an outlier
  (0.50 within-model swing, anchor-only scoring) and is excluded from the
  consensus.

This is therefore a genuine **anchor interpretation** disagreement, not reviewer
noise: it reproduces across 5 independent model lanes plus MODEL_Y, all in the
same direction.

## Decision 1 (BLOCKER — RESOLVED)

**Question:** When a decision is *acceptable but weakly justified / defensible
but not provably best*, where does the rubric anchor sit — the human-generous
read (1.0) or the model-conservative read (0.70-0.85)?

**Considered options:**

| Option | Benefit | Cost / Risk | When to choose |
| --- | --- | --- | --- |
| Conservative (model-consensus) anchor | Reserves the 1.0 anchor for decisions whose optimality/justification is explicitly derived from the trace; aligns scoring with 5-model + MODEL_Y consensus; protects claim thresholds from inflation. | Reviewers must resist rewarding plausible-but-unproven decisions; slightly harsher pass bar. | When evidence must defend a claim against scrutiny (this project). |
| Generous (human) anchor | Easier reviewer agreement on "looks right" cases. | Inflates acceptance/quality/overhead scores; weakens MOGT-C1/C2/C4 evidence; contradicted by all 6 model lanes. | When scoring is advisory, not claim-bearing. |

**Selected option:** **Conservative (model-consensus) anchor.**

**Rationale:** User directive "conservative one" (2026-06-11). It is also the
better-supported option on the evidence — the conservative band is the
consensus of 5 independent models *and* MODEL_Y, and it matches the rubric's own
anchor wording (below). The generous read effectively scores the 0.5 and 1.0
anchors as interchangeable, which collapses the rubric's discrimination on
exactly the cases that decide MOGT-C1/C2/C4.

### Resolved anchor binding

The rubric anchors (`MOGT-REVIEWER-RUBRIC-DRAFT.md`) are read as written:
`1.0` requires the trace to *establish* the positive judgment, not merely
*permit* it. Binding for the 3 flagged rows and any like them:

| Dimension | Trace situation | Conservative anchor | NOT |
| --- | --- | --- | --- |
| `acceptance_score` | Action defensible but trades away another objective (e.g. quality 0.82->0.72, safety 0.91->0.86) and is not shown to be best | ~0.70 ("acceptable but weakly justified", trending toward justified) | 1.0 ("accepted and well justified") |
| `decision_quality_score` | Selected action is a frontier member but optimality vs other frontier members is asserted, not derived | ~0.75-0.80 ("plausible / among-best but not unambiguously optimal") | 1.0 ("among the best available") |
| `overhead_acceptability` | Overhead tolerable but no defined operating-envelope threshold is present in the trace | ~0.70 ("tolerable with caveats") | 1.0 ("clearly acceptable for operational use") |
| `quality_retention` | Self-reported retention improves over baseline (e.g. 0.82) with the value asserted in-trace | ~0.78-0.80 | 1.0 reserved for derived/verified improvement |

**Rule of thumb (reusable):** Reserve the `0.90-1.0` band for decisions whose
trade-off resolution *and* optimality (or acceptability against a stated
envelope) are explicitly derivable from the trace. "Frontier member but
optimality not established", "defensible but trades off another objective", and
"tolerable but no numeric envelope" all land in `0.70-0.85`.

## Decision 2 (DEFERRABLE — recommendation recorded, not blocking)

**Question:** What is GPT-4o's role in the reviewer panel?

**Recommendation (from calibration evidence, not a user choice):** GPT-4o is
**panel-voice only, never a solo reviewer**. It is the only model with a
within-model disagreement above `0.25` (0.50 on `traceability_coverage`), scores
in anchor-only increments (0.0/0.5/1.0) with shallow rationale, and is
systematically biased (low on borderline-positive, high on easy). It is excluded
from the conservative-consensus definition above. Revisit if a final production
panel composition is chosen.

## Assumptions recorded

- The pasted 6-model rig results stand in for the previously-pending **MODEL_X
  lane**. The 5-model consensus (excluding GPT-4o) is treated as the calibration
  ground truth alongside MODEL_Y.
- Failure-case scoring (`CAL-FAIL-OPAQUE`) needs no adjustment: full cross-lane
  agreement (frontier_traceability = 0.00 across all 12 sessions).

## Remaining blockers / deferred items (do NOT block this decision)

These remain open before live evidence collection but are outside this gate:

1. Record concrete model ids/versions for the MODEL_X and MODEL_Y lanes
   (currently placeholders).
2. Record human reviewer identities.
3. Final calibration sign-off and production panel composition (incl. GPT-4o
   panel-voice decision above).
4. Resolve rubric "Open Decisions": scenario count per experiment, agreement
   statistic beyond the disagreement threshold.

## Authority note

This decision resolves only the anchor-alignment blocker. It does **not**
authorize live experiments, evidence-status mutation, or paper claim updates —
the rubric's evidence boundary still applies.
