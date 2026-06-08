---
name: MOGT Reviewer Rubric Draft
description: Draft reviewer rubric for future MOGT claim-bearing experiment runs.
created: 2026-06-08
status: finalized_for_approval_gate
approval_status: approved_as_scoring_gate_not_live_authorization
---

# MOGT Reviewer Rubric

## Purpose

Define the reviewer scoring contract needed before MOGT fixture mechanics can
become claim-bearing experiment evidence.

This rubric is approved as the scoring gate contract. It is not live-run
authorization: production scoring still requires a completed calibration set,
approved model/run parameters, closed protocol gates, and an explicit live
experiment approval decision.

## Scope Decision

E3 negotiation stability is second-wave by default.

First live approval should target E1, E2, and E4 unless the operator explicitly
approves E3 inclusion after an E3-specific dry-run package or protocol repair.

## Review Process

| Requirement | Draft Rule | Approval Status |
| --- | --- | --- |
| Reviewer count | At least two independent reviewers per scored run. | approved |
| Blinding | Reviewers should not see the policy regime label until after scoring. | approved |
| Calibration | Reviewers must score 3-5 calibration examples before production scoring. | required-before-live |
| Disagreement handling | Differences above the threshold trigger adjudication. | approved |
| Inter-rater agreement | Report agreement or disagreement rate per metric family. | approved |
| Reviewer burden | Record elapsed review time or reviewer burden estimate. | approved |
| E3 scope | E3 defaults to second-wave unless explicitly approved. | approved |

## Score Dimensions

All scores use `0..1`, where higher is better unless explicitly noted.

| Dimension | Applies To | Anchor 0.0 | Anchor 0.5 | Anchor 1.0 |
| --- | --- | --- | --- | --- |
| `traceability_coverage` | E1 | Decision rationale is opaque. | Some objectives/tradeoffs are visible. | Objectives, tradeoffs, and selected action are fully inspectable. |
| `acceptance_score` | E1 | Reviewer rejects the action. | Action is acceptable but weakly justified. | Action is accepted and well justified. |
| `decision_quality_score` | E2 | Selected action is clearly poor. | Selected action is plausible. | Selected action is among the best available options. |
| `frontier_traceability` | E2 | Frontier/dominance status is not auditable. | Frontier logic is partially visible. | Frontier and dominated actions are auditable. |
| `conflict_resolution_quality` | E3 | Negotiation deadlocks or worsens disagreement. | Negotiation reaches a plausible but fragile resolution. | Negotiation converges cleanly with preserved quality. |
| `overhead_acceptability` | E4 | Cost/latency/review burden is unacceptable. | Overhead is tolerable with caveats. | Overhead is clearly acceptable for operational use. |
| `quality_retention` | E4 | Quality drops below baseline. | Quality is roughly baseline. | Quality improves or stays strong under overhead limits. |

## Derived Metrics

| Metric | Source | Draft Interpretation |
| --- | --- | --- |
| `dominated_selection` | Calculator or adjudicated objective vectors | `true` means the selected action was dominated by another feasible candidate. |
| `frontier_membership` | Calculator or adjudicated objective vectors | `true` means no feasible candidate dominated the selected action. |
| `regret_or_proxy` | Reviewer or calculator estimate | Lower is better; must be non-negative. |
| `overhead_acceptability_ratio` | Token, latency, turn count, tool calls, reviewer burden | Higher means more runs remain inside the preferred operating envelope. |
| `cycle_count` | Turn-level negotiation trace | Lower is better for E3. |
| `convergence_status` | Negotiation trace | `converged` is preferred; deadlock/oscillation require adjudication. |

## Claim Impact Thresholds

| Claim | Minimum Evidence Shape | Draft Claim-Impact Rule |
| --- | --- | --- |
| MOGT-C1 | E1 paired baseline and explicit-objective runs | Support only if traceability improves materially without unacceptable acceptance loss. |
| MOGT-C2 | E2 heuristic, weighted-sum, and Pareto-guided comparison | Support only if Pareto-guided selection reduces dominated choices and preserves quality. |
| MOGT-C3 | E3 baseline and negotiation-enabled conflict scenarios | Second-wave by default. Support only if E3 is explicitly approved and convergence improves or cycle count drops without quality loss. |
| MOGT-C4 | E4 overhead envelope across policy complexity | Support only if benefits remain inside token, latency, turn, and reviewer-burden limits. |

## Calibration Requirements

Before live scoring:

1. Select 3-5 calibration examples spanning easy, ambiguous, and failure cases.
2. Have reviewers score independently.
3. Compare reviewer scores and resolve anchor misunderstandings.
4. Record calibration notes before production scoring.
5. Decide whether score variance is acceptable.

Calibration pass rule:

- At least two reviewers complete all calibration examples.
- Every score dimension used in production appears in at least one calibration
  example.
- Any score disagreement greater than `0.25` on a shared dimension is discussed
  and adjudicated before production scoring.
- Calibration notes are saved before live evidence collection starts.

## Open Decisions

- Scenario count per experiment.
- Whether bounded prior-art refresh is required before live approval.
- Exact agreement statistic beyond the required disagreement threshold.

## Evidence Boundary

This rubric is a scoring gate artifact. It does not authorize live experiments,
evidence-status mutation, or paper claim updates.
