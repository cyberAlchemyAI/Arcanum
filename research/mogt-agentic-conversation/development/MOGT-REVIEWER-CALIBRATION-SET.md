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

| Example | Dimension | Reviewer A Score | Reviewer B Score | Difference | Adjudication Required? | Adjudication Note |
| --- | --- | --- | --- | --- | --- | --- |
| CAL-E1-EASY | `traceability_coverage` | pending | pending | pending | pending | pending |
| CAL-E1-EASY | `acceptance_score` | pending | pending | pending | pending | pending |
| CAL-E2-AMBIGUOUS | `decision_quality_score` | pending | pending | pending | pending | pending |
| CAL-E2-AMBIGUOUS | `frontier_traceability` | pending | pending | pending | pending | pending |
| CAL-E4-BOUNDARY | `overhead_acceptability` | pending | pending | pending | pending | pending |
| CAL-E4-BOUNDARY | `quality_retention` | pending | pending | pending | pending | pending |
| CAL-FAIL-OPAQUE | `traceability_coverage` | pending | pending | pending | pending | pending |
| CAL-FAIL-OPAQUE | `acceptance_score` | pending | pending | pending | pending | pending |
| CAL-FAIL-OPAQUE | `decision_quality_score` | pending | pending | pending | pending | pending |
| CAL-FAIL-OPAQUE | `frontier_traceability` | pending | pending | pending | pending | pending |
| CAL-FAIL-OPAQUE | `overhead_acceptability` | pending | pending | pending | pending | pending |
| CAL-FAIL-OPAQUE | `quality_retention` | pending | pending | pending | pending | pending |

## Current Status

Calibration examples are ready for independent reviewer scoring.

This artifact does not complete calibration by itself. It must be updated with
two independent reviewer score columns and adjudication notes before production
scoring or live evidence approval.
