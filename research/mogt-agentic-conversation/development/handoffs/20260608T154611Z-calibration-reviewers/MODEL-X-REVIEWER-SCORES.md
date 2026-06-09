---
name: MOGT Model X Reviewer Scores
description: Independent score tables from the two isolated Model X reviewer sessions for the MOGT calibration set.
created: 2026-06-09
source_handoff: HANDOFF-MODEL-X-REVIEWERS.md
reviewer_lane: model_x
model_id: claude-opus-4-8 (Model X lane; actual id was unspecified in handoff, resolved to current model)
disagreement_threshold: 0.25
status: model-x-lane-complete-awaiting-task-session-cross-lane-comparison
---

# MOGT Model X Reviewer Scores

Two isolated Model X reviewer sessions scored the calibration set independently.
Neither reviewer saw the other's scores, the policy regime label, the human
lane, or the Model Y lane before submitting. No live experiments were run; no
evidence status, paper sections, or publication claims were touched.

## MODEL_X_REVIEWER_1 (→ Reviewer A lane)

| Example | Dimension | Score | Short rationale | Uncertainty flag |
| --- | --- | --- | --- | --- |
| CAL-E1-EASY | `traceability_coverage` | 1.0 | Objective vectors for both candidates, selected action, selection reason, and principal tradeoff are all explicit and inspectable. | low |
| CAL-E1-EASY | `acceptance_score` | 0.5 | Action ("answer now") is acceptable and justified by lower cost/latency, but Candidate B offers higher quality and safety, so the choice is defensible yet weakly justified rather than clearly best. | medium |
| CAL-E2-AMBIGUOUS | `decision_quality_score` | 0.5 | Selected action (ask clarifying question) is a plausible frontier member, but it is not demonstrably among the best — C dominates it on quality/safety and frontier membership alone does not establish optimality. | medium |
| CAL-E2-AMBIGUOUS | `frontier_traceability` | 1.0 | Frontier note explicitly marks D as dominated and names A/B/C as frontier members with a stated tie-break rule; dominance status is fully auditable. | low |
| CAL-E4-BOUNDARY | `overhead_acceptability` | 0.5 | Overhead ratio 0.78 with one extra tool call and 520 tokens sits near the boundary; tolerable with caveats but no stated envelope threshold confirms acceptability. | medium |
| CAL-E4-BOUNDARY | `quality_retention` | 1.0 | Reported quality retention 0.82 with quality improving over the heuristic alternative; quality stays strong under overhead limits. | low |
| CAL-FAIL-OPAQUE | `traceability_coverage` | 0.0 | Candidate actions and objective vectors not recorded; rationale is "seemed best". Decision is opaque. | low |
| CAL-FAIL-OPAQUE | `acceptance_score` | 0.0 | Final answer only "plausible but not auditable" with no justification; reviewer should reject rather than reward an unverifiable action. | low |
| CAL-FAIL-OPAQUE | `decision_quality_score` | 0.0 | No candidates or objective vectors recorded, so quality of the selected action cannot be established; scored conservatively as poor due to missing evidence. | low |
| CAL-FAIL-OPAQUE | `frontier_traceability` | 0.0 | Frontier/dominance note explicitly absent; no objective vectors. Not auditable. | low |
| CAL-FAIL-OPAQUE | `overhead_acceptability` | 0.0 | Token and latency high relative to a simple answer with no explanation; overhead is unexplained and unacceptable. | low |
| CAL-FAIL-OPAQUE | `quality_retention` | 0.0 | No baseline or quality figures provided; quality is unauditable, so retention cannot be evidenced and is scored conservatively at the failure anchor. Missing: any quality/baseline metric. | medium |

## MODEL_X_REVIEWER_2 (→ Reviewer B lane)

| Example | Dimension | Score | Short rationale | Uncertainty flag |
| --- | --- | --- | --- | --- |
| CAL-E1-EASY | `traceability_coverage` | 1.0 | Objective vectors for both candidates, selected action, selection reason, and principal tradeoff are all explicit and inspectable. | low |
| CAL-E1-EASY | `acceptance_score` | 0.5 | Action is acceptable and justified by lower overhead, but B has materially higher quality (0.82 vs 0.72) and safety (0.91 vs 0.86); justification is reasonable but not clearly optimal, so weakly justified. | medium |
| CAL-E2-AMBIGUOUS | `decision_quality_score` | 0.5 | Selected action (A) is a plausible frontier member, but C dominates on quality/safety at higher overhead and the tie-break does not establish A as among the best; plausible, not clearly optimal. | medium |
| CAL-E2-AMBIGUOUS | `frontier_traceability` | 1.0 | Frontier membership (A, B, C) and dominated candidate (D) are explicitly noted with a stated tie-break rule; fully auditable. | low |
| CAL-E4-BOUNDARY | `overhead_acceptability` | 0.5 | Overhead ratio 0.78 with +1 tool call and added tokens (520, 1500 ms) sits near the boundary; tolerable with caveats but not clearly acceptable, and no envelope threshold is given to confirm. | medium |
| CAL-E4-BOUNDARY | `quality_retention` | 0.5 | Reported quality retention 0.82 indicates quality is roughly at/near baseline rather than a clear improvement; no explicit baseline value provided to confirm gain. | medium |
| CAL-FAIL-OPAQUE | `traceability_coverage` | 0.0 | Candidate actions and objective vectors are not recorded and rationale is "seemed best"; decision rationale is opaque. | low |
| CAL-FAIL-OPAQUE | `acceptance_score` | 0.0 | Action is not auditable; plausible final answer must not be rewarded when justification is absent. Reviewer rejects. | low |
| CAL-FAIL-OPAQUE | `decision_quality_score` | 0.0 | No objective vectors or alternatives recorded; selection quality cannot be established and cannot be credited as plausible against absent evidence. | low |
| CAL-FAIL-OPAQUE | `frontier_traceability` | 0.0 | Frontier/dominance note is explicitly absent; not auditable. | low |
| CAL-FAIL-OPAQUE | `overhead_acceptability` | 0.0 | Token and latency are high relative to a simple answer with no justification; overhead is unexplained and unacceptable. | low |
| CAL-FAIL-OPAQUE | `quality_retention` | 0.0 | Quality is "plausible but not auditable" with no baseline or measurement; conservatively scored at floor since retention cannot be evidenced. | medium |

## Within-Model Difference Table (Reviewer 1 vs Reviewer 2)

Adjudication required when `|R1 - R2| > 0.25`.

| Example | Dimension | R1 | R2 | Difference | Adjudication Required? |
| --- | --- | --- | --- | --- | --- |
| CAL-E1-EASY | `traceability_coverage` | 1.0 | 1.0 | 0.00 | no |
| CAL-E1-EASY | `acceptance_score` | 0.5 | 0.5 | 0.00 | no |
| CAL-E2-AMBIGUOUS | `decision_quality_score` | 0.5 | 0.5 | 0.00 | no |
| CAL-E2-AMBIGUOUS | `frontier_traceability` | 1.0 | 1.0 | 0.00 | no |
| CAL-E4-BOUNDARY | `overhead_acceptability` | 0.5 | 0.5 | 0.00 | no |
| CAL-E4-BOUNDARY | `quality_retention` | 1.0 | 0.5 | 0.50 | **yes** |
| CAL-FAIL-OPAQUE | `traceability_coverage` | 0.0 | 0.0 | 0.00 | no |
| CAL-FAIL-OPAQUE | `acceptance_score` | 0.0 | 0.0 | 0.00 | no |
| CAL-FAIL-OPAQUE | `decision_quality_score` | 0.0 | 0.0 | 0.00 | no |
| CAL-FAIL-OPAQUE | `frontier_traceability` | 0.0 | 0.0 | 0.00 | no |
| CAL-FAIL-OPAQUE | `overhead_acceptability` | 0.0 | 0.0 | 0.00 | no |
| CAL-FAIL-OPAQUE | `quality_retention` | 0.0 | 0.0 | 0.00 | no |

### Disagreement summary

- 1 of 12 dimensions exceeds the `0.25` threshold: **CAL-E4-BOUNDARY / `quality_retention`** (R1=1.0, R2=0.5, diff=0.50).
- Source of disagreement: R1 read reported retention 0.82 plus "quality improving over the heuristic alternative" as a clear improvement (anchor 1.0); R2 read 0.82 with no explicit baseline value as roughly-baseline (anchor 0.5). The trace gives a retention number but no explicit baseline, which is the ambiguity both reviewers flagged.
- This disagreement must be adjudicated before production scoring (per calibration gate rule 3 and rubric calibration pass rule).

## Next Route

Return both score tables to a `task-session` continuation for:
1. cross-lane comparison against the human and Model Y reviewer lanes;
2. adjudication of the one flagged within-model disagreement (CAL-E4-BOUNDARY / `quality_retention`);
3. recording calibration notes before any live evidence collection.

This artifact does not complete calibration and does not authorize live runs.
