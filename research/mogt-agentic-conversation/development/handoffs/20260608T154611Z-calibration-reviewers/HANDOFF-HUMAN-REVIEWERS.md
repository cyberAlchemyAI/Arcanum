---
name: MOGT Human Reviewer Calibration Handoff
description: Invoke handoff for two human reviewers scoring the MOGT calibration set.
created: 2026-06-08
mode: handoff
handoff_type: execution-continuation
reviewer_lane: human
reviewer_count: 2
phase_status: pass
---

# Handoff: Human Reviewers

## Identity

- Source session reference: current MOGT repair session
- Target artifact: `research/mogt-agentic-conversation/development/MOGT-REVIEWER-CALIBRATION-SET.md`
- Target lifecycle owner: MOGT repair pack
- Next route after return: `task-session`

## Plain-Language Option

For a non-technical human reviewer, hand them `HUMAN-REVIEWER-GUIDE-PLAIN.md`
(in this same folder) instead of the prompt below. It walks through the same 4
examples in everyday language, with a blank score sheet to fill in, and maps the
plain questions back to the rubric dimensions for the lead.

## New Session Prompt

Use this prompt for each human reviewer, changing only the reviewer id.

```text
You are HUMAN_REVIEWER_<A_OR_B> for the MOGT calibration set.

Read only:
- research/mogt-agentic-conversation/development/MOGT-REVIEWER-CALIBRATION-SET.md
- research/mogt-agentic-conversation/development/MOGT-REVIEWER-RUBRIC-DRAFT.md

Do not inspect another reviewer's scores or rationale before submitting yours.
Do not run live experiments. Do not update evidence status, paper sections, or
publication claims.

Score every pending row assigned to the reviewer score sheet using values from
0.0 to 1.0. Return a Markdown table with:

| Example | Dimension | Score | Short rationale | Uncertainty flag |

Use the rubric anchors. If the trace is missing evidence, score conservatively
and say what is missing. Do not adjudicate; adjudication happens after both
human reviewers submit independent scores.
```

## Reviewer Assignments

| Reviewer ID | Role | Visibility Rule | Output |
| --- | --- | --- | --- |
| HUMAN_REVIEWER_A | independent human scorer | Must not see B, Model X, or Model Y scores first. | Human A score table. |
| HUMAN_REVIEWER_B | independent human scorer | Must not see A, Model X, or Model Y scores first. | Human B score table. |

## Obligation Coverage Matrix

| Obligation | Coverage |
| --- | --- |
| Score all calibration examples | pass |
| Use finalized rubric anchors | pass |
| Preserve reviewer independence | process-required |
| Avoid live experiment mutation | pass |
| Preserve E3 second-wave default | pass |

## Selected Context

- Calibration examples and score sheet live in `MOGT-REVIEWER-CALIBRATION-SET.md`.
- Rubric anchors and disagreement rule live in `MOGT-REVIEWER-RUBRIC-DRAFT.md`.
- Any score difference greater than `0.25` is adjudicated after both reviewers return scores.

## Gaps And Blockers

- Human identity and scheduling are outside the repository.
- This handoff does not complete calibration until both reviewers return scores.

## Next-Session Start Prompt

Start with the prompt above for `HUMAN_REVIEWER_A`, then separately for
`HUMAN_REVIEWER_B`.

## Next Route

Return both score tables to a `task-session` continuation for
`SWU-MOGT-REPAIR-001` adjudication and synchronization.
