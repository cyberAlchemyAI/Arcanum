---
name: MOGT Reviewer Calibration Set
description: Reviewer calibration examples for first-wave MOGT live evidence scoring.
created: 2026-06-08
status: examples-ready-reviewer-scoring-required
source_rubric: MOGT-REVIEWER-RUBRIC-DRAFT.md
e3_scope: second-wave
---

# MOGT Reviewer Calibration Set

## Purpose

Provide the 3-5 calibration examples required before production reviewer
scoring. These examples are synthetic calibration materials derived from local
fixture structures and protocol expectations. They are not live experiment
evidence.

## Calibration Gate

Production scoring remains blocked until:

1. at least two independent reviewers score all examples;
2. every first-wave score dimension is represented;
3. disagreements greater than `0.25` on a shared dimension are adjudicated;
4. calibration notes are saved before live evidence collection starts.

## Dimension Coverage

| Dimension | Covered By |
| --- | --- |
| `traceability_coverage` | CAL-E1-EASY, CAL-FAIL-OPAQUE |
| `acceptance_score` | CAL-E1-EASY, CAL-FAIL-OPAQUE |
| `decision_quality_score` | CAL-E2-AMBIGUOUS, CAL-FAIL-OPAQUE |
| `frontier_traceability` | CAL-E2-AMBIGUOUS, CAL-FAIL-OPAQUE |
| `overhead_acceptability` | CAL-E4-BOUNDARY, CAL-FAIL-OPAQUE |
| `quality_retention` | CAL-E4-BOUNDARY, CAL-FAIL-OPAQUE |

E3 `conflict_resolution_quality` is excluded from first-wave calibration
because E3 remains second-wave by default.

## Scoring Instructions

Reviewers must score independently using `0..1` anchors from
`MOGT-REVIEWER-RUBRIC-DRAFT.md`.

Reviewers should not see the policy regime label during initial scoring. The
calibration lead may reveal the policy regime after initial scores are recorded
for discussion and adjudication.

Use this shared disagreement rule:

- if two reviewer scores differ by more than `0.25` on the same dimension,
  record an adjudication note before production scoring.

## Example CAL-E1-EASY

### Scenario

A conversation agent must decide whether to answer immediately or ask a narrow
clarifying question before selecting a tool route. The trace includes candidate
actions, objective vectors, a selected action, and a principal tradeoff.

### Reviewer-Visible Trace

```text
Candidate A: answer now with available context.
Objective vector: quality 0.72, cost 0.92, latency 0.88, safety 0.86.

Candidate B: ask a narrow clarification.
Objective vector: quality 0.82, cost 0.70, latency 0.68, safety 0.91.

Selected action: answer now.
Selection reason: enough context exists and overhead is lower.
Principal tradeoff: lower peak quality for lower cost and latency.
```

### Dimensions To Score

- `traceability_coverage`
- `acceptance_score`

### Calibration Intent

Easy traceability case. Reviewers should recognize that the tradeoff is visible,
even if they disagree about whether the selected action is the best one.

## Example CAL-E2-AMBIGUOUS

### Scenario

A conversation agent must choose among a clarifying question, proceeding with an
assumption, running a full deliberation panel, or answering quickly without
trace. The frontier includes multiple plausible actions with different
overhead/quality profiles.

### Reviewer-Visible Trace

```text
Candidate A: ask clarifying question.
Objective vector: quality 0.86, cost 0.74, latency 0.70, safety 0.91.

Candidate B: proceed with explicit assumption.
Objective vector: quality 0.68, cost 0.82, latency 0.86, safety 0.72.

Candidate C: run full deliberation panel.
Objective vector: quality 0.91, cost 0.42, latency 0.38, safety 0.90.

Candidate D: answer quickly without tradeoff trace.
Objective vector: quality 0.58, cost 0.82, latency 0.86, safety 0.70.

Selected action: ask clarifying question.
Frontier note: Candidate D is dominated; A, B, and C are frontier members.
Tie-break note: quality then safety, while avoiding full-panel overhead.
```

### Dimensions To Score

- `decision_quality_score`
- `frontier_traceability`

### Calibration Intent

Ambiguous Pareto case. Reviewers should discuss why frontier membership alone
does not automatically make the selected action optimal.

## Example CAL-E4-BOUNDARY

### Scenario

A conversation agent uses an explicit weighted objective policy instead of a
short heuristic. Quality improves, but the run adds one tool call and more
tokens. The case is close to the acceptable overhead boundary.

### Reviewer-Visible Trace

```text
Selected action: single-agent explicit objective decision.
Reported quality retention: 0.82.
Overhead acceptability ratio: 0.78.
Token cost: 520.
Latency: 1500 ms.
Turn count: 2.
Tool calls: 1.

Alternative: heuristic shortcut.
Reported quality lower, overhead lower.

Alternative: multi-agent deliberation.
Reported quality higher, overhead much worse.
```

### Dimensions To Score

- `overhead_acceptability`
- `quality_retention`

### Calibration Intent

Boundary overhead case. Reviewers should align on what counts as acceptable
overhead when quality is retained but the operational burden increases.

## Example CAL-FAIL-OPAQUE

### Scenario

A conversation agent selects an action quickly. The record lacks objective
vectors for alternatives, does not identify the principal tradeoff, and records
high overhead after the fact. Reviewers must score this as a failure case even
if the final answer appears plausible.

### Reviewer-Visible Trace

```text
Candidate actions: not recorded.
Objective vectors: not recorded.
Selected action: answer immediately.
Selection reason: "seemed best".
Frontier/dominance note: absent.
Token cost: high relative to expected simple answer.
Latency: high relative to expected simple answer.
Quality note: plausible but not auditable.
```

### Dimensions To Score

- `traceability_coverage`
- `acceptance_score`
- `decision_quality_score`
- `frontier_traceability`
- `overhead_acceptability`
- `quality_retention`

### Calibration Intent

Failure case. Reviewers should not reward a plausible final answer when the
decision trace is not auditable and overhead is unexplained.

## Reviewer Score Sheet

Reviewer lane: `MODEL_Y` (Reviewer A = MODEL_Y_REVIEWER_1, Reviewer B =
MODEL_Y_REVIEWER_2). Scores collected via two isolated independent reviewer
sessions per the `20260608T154611Z-calibration-reviewers` handoff. Human and
Model X lanes remain pending.

| Example | Dimension | Reviewer A Score | Reviewer B Score | Difference | Adjudication Required? | Adjudication Note |
| --- | --- | --- | --- | --- | --- | --- |
| CAL-E1-EASY | `traceability_coverage` | 1.0 | 0.95 | 0.05 | no | Both judge the trace fully inspectable (1.0 anchor); B's minor deduction for only two candidates shown. |
| CAL-E1-EASY | `acceptance_score` | 0.7 | 0.7 | 0.00 | no | Agreement: action accepted and justified but trades quality/safety vs Candidate B; defensible rather than clearly best. |
| CAL-E2-AMBIGUOUS | `decision_quality_score` | 0.75 | 0.7 | 0.05 | no | Agreement: selected action is a frontier member, plausible/among-best but not unambiguously optimal vs Candidate C. |
| CAL-E2-AMBIGUOUS | `frontier_traceability` | 1.0 | 0.9 | 0.10 | no | Both find frontier/dominance auditable; B deducts slightly because dominance is asserted, not derived from vectors. |
| CAL-E4-BOUNDARY | `overhead_acceptability` | 0.6 | 0.65 | 0.05 | no | Agreement: tolerable-with-caveats; both flag absence of a defined operating-envelope threshold. |
| CAL-E4-BOUNDARY | `quality_retention` | 0.8 | 0.8 | 0.00 | no | Agreement: reported retention 0.82 improves over heuristic; value self-reported in trace. |
| CAL-FAIL-OPAQUE | `traceability_coverage` | 0.0 | 0.05 | 0.05 | no | Agreement: rationale opaque (0.0 anchor); B's minimal nonzero only because the selected action is named. |
| CAL-FAIL-OPAQUE | `acceptance_score` | 0.1 | 0.15 | 0.05 | no | Agreement: plausible-but-unauditable answer is rejected per calibration intent. |
| CAL-FAIL-OPAQUE | `decision_quality_score` | 0.15 | 0.1 | 0.05 | no | Agreement: no candidates/vectors recorded; quality unsubstantiated, scored near zero. |
| CAL-FAIL-OPAQUE | `frontier_traceability` | 0.0 | 0.0 | 0.00 | no | Agreement: frontier/dominance note absent (exact 0.0 anchor). |
| CAL-FAIL-OPAQUE | `overhead_acceptability` | 0.1 | 0.1 | 0.00 | no | Agreement: high unexplained cost/latency, no acceptability ratio. |
| CAL-FAIL-OPAQUE | `quality_retention` | 0.2 | 0.2 | 0.00 | no | Agreement: no baseline; retention indeterminate, scored low conservatively. |

## Human Reviewer Lane (cross-lane comparison vs MODEL_Y)

Human reviewer scored independently after the MODEL_Y lane, using the same
0..1 rubric anchors. "Gap" is the maximum absolute difference between the human
score and either MODEL_Y reviewer; gaps greater than `0.25` are flagged for
adjudication before production scoring.

| Example | Dimension | Human Score | Model Y (R1/R2) | Max Gap | Adjudication Required? |
| --- | --- | --- | --- | --- | --- |
| CAL-E1-EASY | `traceability_coverage` | 0.8 | 1.0 / 0.95 | 0.20 | no |
| CAL-E1-EASY | `acceptance_score` | 1.0 | 0.7 / 0.7 | 0.30 | yes |
| CAL-E2-AMBIGUOUS | `decision_quality_score` | 1.0 | 0.75 / 0.7 | 0.30 | yes |
| CAL-E2-AMBIGUOUS | `frontier_traceability` | 1.0 | 1.0 / 0.9 | 0.10 | no |
| CAL-E4-BOUNDARY | `overhead_acceptability` | 1.0 | 0.6 / 0.65 | 0.40 | yes |
| CAL-E4-BOUNDARY | `quality_retention` | 1.0 | 0.8 / 0.8 | 0.20 | no |
| CAL-FAIL-OPAQUE | `traceability_coverage` | 0.0 | 0.0 / 0.05 | 0.05 | no |
| CAL-FAIL-OPAQUE | `acceptance_score` | 0.1 | 0.1 / 0.15 | 0.05 | no |
| CAL-FAIL-OPAQUE | `decision_quality_score` | 0.1 | 0.15 / 0.1 | 0.05 | no |
| CAL-FAIL-OPAQUE | `frontier_traceability` | 0.0 | 0.0 / 0.0 | 0.00 | no |
| CAL-FAIL-OPAQUE | `overhead_acceptability` | 0.1 | 0.1 / 0.1 | 0.00 | no |
| CAL-FAIL-OPAQUE | `quality_retention` | 0.2 | 0.2 / 0.2 | 0.00 | no |

### Human vs MODEL_Y adjudication notes

- Three rows exceed the `0.25` threshold, all in the same direction: the human
  scored borderline-positive decisions more leniently than the conservative
  MODEL_Y lane.
  - `CAL-E1-EASY / acceptance_score`: human 1.0 vs Model Y 0.7. Human treats
    the speed/cost trade as clearly correct; Model Y notes the chosen action
    gave up quality (0.82 -> 0.72) and safety (0.91 -> 0.86).
  - `CAL-E2-AMBIGUOUS / decision_quality_score`: human 1.0 vs Model Y 0.7-0.75.
    Human reads "ask clarifying question" as best-available; Model Y holds that
    frontier membership alone does not establish optimality vs Candidate C.
  - `CAL-E4-BOUNDARY / overhead_acceptability`: human 1.0 vs Model Y 0.6-0.65.
    Human accepts the overhead outright; Model Y flags the missing defined
    operating-envelope threshold and scores it as tolerable-with-caveats.
- Failure case (`CAL-FAIL-OPAQUE`) shows full human/Model Y agreement: both
  refuse to reward a plausible-but-unauditable answer.
- Recommended anchor alignment before production scoring: agree on how
  generously to score borderline-acceptable decisions and what overhead counts
  as "clearly acceptable" absent a numeric envelope.

## Calibration Notes (MODEL_Y lane)

- Two independent isolated `MODEL_Y` reviewer sessions scored all 12 pending
  rows. Within-model independence preserved (neither saw the other's scores).
- All first-wave dimensions represented; E3 `conflict_resolution_quality`
  excluded as second-wave by default.
- Maximum within-model disagreement is `0.10` (`frontier_traceability` on
  CAL-E2-AMBIGUOUS); no row exceeds the `0.25` adjudication threshold, so no
  Model Y adjudication is required.
- Open gap: the actual `MODEL_Y` model id/version was not chosen in the source
  handoff; record it before production scoring.

## Current Status

MODEL_Y lane scored (within-model pass) and the human reviewer lane scored,
with cross-lane comparison recorded. Human/Model Y agreement is strong on the
failure case and clarity dimensions, with 3 flagged disagreements (>0.25) on
borderline-positive decisions where the human scored more leniently.

Calibration is NOT yet complete. Remaining before production scoring or live
evidence approval:
1. Resolve the 3 human/Model Y adjudication rows (anchor-alignment discussion).
2. Score the Model X reviewer lane (still pending).
3. Save final calibration sign-off, ideally via a `task-session` continuation.
