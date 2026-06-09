---
name: MOGT Model X Reviewer Calibration Handoff
description: Invoke handoff for two Model X reviewer sessions scoring the MOGT calibration set.
created: 2026-06-08
mode: handoff
handoff_type: execution-continuation
reviewer_lane: model_x
reviewer_count: 2
model_placeholder: MODEL_X
phase_status: pass
---

# Handoff: Model X Reviewers

## Identity

- Source session reference: current MOGT repair session
- Target artifact: `research/mogt-agentic-conversation/development/MOGT-REVIEWER-CALIBRATION-SET.md`
- Model lane: `MODEL_X`
- Target lifecycle owner: MOGT repair pack
- Next route after return: `task-session`

## New Session Prompt

Use this prompt twice in isolated sessions running `MODEL_X`, changing only the
reviewer id.

```text
You are MODEL_X_REVIEWER_<1_OR_2> for the MOGT calibration set.

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
and say what is missing. Do not adjudicate; adjudication happens after the
reviewer pair submits independent scores.
```

## Reviewer Assignments

| Reviewer ID | Model | Visibility Rule | Output |
| --- | --- | --- | --- |
| MODEL_X_REVIEWER_1 | `MODEL_X` | Must not see reviewer 2, human, or Model Y scores first. | Model X score table 1. |
| MODEL_X_REVIEWER_2 | `MODEL_X` | Must not see reviewer 1, human, or Model Y scores first. | Model X score table 2. |

## Obligation Coverage Matrix

| Obligation | Coverage |
| --- | --- |
| Score all calibration examples | pass |
| Use finalized rubric anchors | pass |
| Preserve within-model independence | process-required |
| Avoid live experiment mutation | pass |
| Preserve E3 second-wave default | pass |

## Selected Context

- Calibration examples and score sheet live in `MOGT-REVIEWER-CALIBRATION-SET.md`.
- Rubric anchors and disagreement rule live in `MOGT-REVIEWER-RUBRIC-DRAFT.md`.
- Any score difference greater than `0.25` is adjudicated after both Model X reviewers return scores.

## Gaps And Blockers

- Actual `MODEL_X` model id/version is not chosen in this handoff.
- This handoff does not complete calibration until both isolated Model X reviewer sessions return scores.

## Next-Session Start Prompt

Start with the prompt above for `MODEL_X_REVIEWER_1`, then separately for
`MODEL_X_REVIEWER_2`.

## Next Route

Return both score tables to a `task-session` continuation for comparison against
human and Model Y lanes.
