# TASK-005: Build Telemetry Reporting And Dashboard-Ready API

## Objective

Expose reliable operator-facing reports and dashboard-ready API views from persisted run evidence without recomputing oracle results in the UI layer.

## Layer And Slice Mapping

- Layer: L3
- Slice: S-005
- Wave: [W3](../waves/W3.md)

## Source Contracts

- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
- [../../WORK-PACK.md](../../WORK-PACK.md)

## Dependencies

- TASK-003 for minimum reporting.
- TASK-004 for complete multi-suite reporting.

## Implementation Detail

Inputs:

- Persisted run results.
- Telemetry events.
- Score results and artifact links.

Outputs:

- Campaign report generator.
- Dashboard-ready API endpoints or static data contract.
- Minimal React dashboard when frontend scope is approved.

Implementation notes:

1. Define read models for campaign summary, per-run detail, score components, and trajectory cost.
2. Generate a static report first to validate evidence links.
3. Add API endpoints or data exports that mirror those read models.
4. Build UI only after data contracts are stable.
5. Keep dashboard display read-only over score evidence.

Edge cases:

- Missing artifact links must show as evidence gaps, not silently disappear.
- Incomplete runs must remain visible with terminal reason.
- Aggregate metrics must exclude quarantined tasks unless explicitly requested.

## Smallest Working Units

### SWU-HARNESS-009

- Goal: implement campaign report read models and static report generation.
- Dependencies: SWU-HARNESS-006.
- Write scope: reporting modules and report fixtures.
- Done criteria: report links aggregate metrics to per-run evidence and telemetry cost.
- Acceptance evidence: report snapshot review.
- Verification: report snapshot test or reviewable generated sample.
- Execution owner: subagent.
- Handoff note: do not compute new oracle outcomes in report code.

### SWU-HARNESS-010

- Goal: implement dashboard-ready API or minimal UI over the stable report model.
- Dependencies: SWU-HARNESS-009.
- Write scope: API/UI modules and smoke tests.
- Done criteria: operator can inspect campaign summary, per-run status, score components, and telemetry events.
- Acceptance evidence: UI/API smoke check.
- Verification: API smoke command or frontend test command.
- Execution owner: local-fallback.
- Handoff note: keep visual scope secondary to evidence traceability.

## Synchronization Rules

SWU-HARNESS-010 starts only after report read models are stable.

## Completion Evidence

- Dashboard/API displays persisted score and telemetry data.
- Campaign report can be regenerated from stored artifacts.
