---
stage: Invoke Plan
owner: invoke
status: pass
---

# Plan: Next Steps

## Immediate Task Session

Create and execute `MOGT-S4-DRY-RUN-REHEARSAL`.

### Objective

Use the completed fixture harness to rehearse the S4 evidence route and produce
the artifacts needed to decide whether live experiments can be approved.

### Write Scope

- `research/mogt-agentic-conversation/development/MOGT-S4-DRY-RUN-REHEARSAL-REPORT.md`
- `research/mogt-agentic-conversation/development/MOGT-REVIEWER-RUBRIC-DRAFT.md`
- `research/mogt-agentic-conversation/development/MOGT-LIVE-EXPERIMENT-APPROVAL-CHECKLIST.md`
- optional goal pack under `research/mogt-agentic-conversation/development/goals/`

### Verification

- Re-run fixture JSONL validator.
- Re-run Pareto/frontier calculator.
- Re-run summary generator or verify generated summaries are current.
- Check E1-E4 protocol readiness against the reviewer rubric draft.
- Confirm no live experiments were run and evidence status was not mutated.

### Done Criteria

- Dry-run rehearsal report exists.
- Reviewer rubric draft exists.
- Live-experiment approval checklist exists.
- Checklist has a clear verdict: approve-ready, repair-needed, or research-gap.

## After Rehearsal

1. If approve-ready: create a live-evidence approval gate and split E1/E2/E4/E3
   into execution goals.
2. If repair-needed: fix protocol or rubric gaps first.
3. If research-gap: request bounded prior-art refresh before claim-bearing work.

## Deferred Work

- Live model calls.
- Reviewer scoring.
- Evidence-status update.
- Paper result rewrite.
- Tool absorption into canonical Arcanum contracts.
