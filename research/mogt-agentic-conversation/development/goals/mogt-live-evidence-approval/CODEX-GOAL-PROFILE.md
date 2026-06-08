---
name: Codex Goal Profile - MOGT Live Evidence Approval
selected_unit: MOGT-LIVE-EVIDENCE-APPROVAL
readiness: pass
created: 2026-06-08
---

# Codex Goal Profile Result

## Source Context

- `research/mogt-agentic-conversation/development/MOGT-S4-DRY-RUN-REHEARSAL-REPORT.md`
- `research/mogt-agentic-conversation/development/MOGT-REVIEWER-RUBRIC-DRAFT.md`
- `research/mogt-agentic-conversation/development/MOGT-LIVE-EXPERIMENT-APPROVAL-CHECKLIST.md`

## Selected Unit

`MOGT-LIVE-EVIDENCE-APPROVAL`

Readiness: pass.

The task is an approval gate, not a live execution route. The rubric is
finalized as the scoring gate, E3 is second-wave by default, and calibration is
required before production scoring.

## Native Goal

```text
/goal Execute MOGT-LIVE-EVIDENCE-APPROVAL as an approval-gate task, not a live experiment. Work from research/mogt-agentic-conversation/development/goals/mogt-live-evidence-approval/ and read 01-outcome.md, 02-verification.md, 03-constraints-boundaries.md, 04-iteration-stop.md, and 05-reporting.md before editing. Use the rehearsal report, finalized reviewer rubric, live approval checklist, evidence status, and E1-E4 protocols. Keep E3 second-wave by default, require 3-5 calibration examples before production scoring, do not run live experiments, and stop with BLOCK if approval cannot be decided from local evidence.
```

## Verification Surface

Approval decision artifact with local checks over rubric, calibration,
protocol gates, E3 default, live-run parameters, and evidence mutation policy.

## Boundaries

Write only the approval result, checklist update, and optional next goal pack.
Do not run live experiments or mutate evidence status/paper results.

## Handoff Pack

This goal uses local source context listed in `README.md`; no separate JSON
context index exists yet.

Strict coverage: pass for local approval-gate authoring.

## Fallback Exploration

Named gaps only. If bounded external research is needed, report `research-gap`
instead of browsing inside the approval task.

## Stop Condition

Stop with `BLOCK` if approval cannot be decided from local evidence without
running live experiments or expanding write scope.
