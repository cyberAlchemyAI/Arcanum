# TASK-DEE-03: Semantic And Provenance Validator

Status: completed on 2026-07-17 after DEE-004 and DEE-005 evidence passed.

## Objective

Derive the only handoff-authoritative Distill result from accepted evidence and reviewed
artifacts.

Selection gate: blocked until the Spellcraft receipt names the canonical validator owner,
implementation language, and exact write paths.

## Algorithm

```text
validate(request, receipt, eventStore, reviewedInputs, invokeResult):
  require schemas valid
  require receipt/request/run identity agrees
  events = resolve every receipt.event_ref
  require event order and execution path agree
  require role separation or valid ordered simulation boundaries
  require rounds <= budget and allowed termination
  require every objection categorized and reconciled
  require required techniques traced or readiness downgraded
  require reviewed-input provenance passes accepted policy
  require receipt/result/work-pack/observability verdicts and counts agree
  derive status and mutation_handoff_allowed; never trust authored status
```

## SWU-DEE-004: Role And Process Semantics

- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-004-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-004-LIFECYCLE-RECEIPT.md).
- Primary behavior: validate role path, event ordering, rounds, termination, objections,
  reconciliation, and techniques.
- Acceptance boundary: focused unit tests discriminate valid and invalid process traces.
- Split analysis: these checks jointly determine whether a Distill process completed; input
  provenance/cross-artifact checks are independently testable in DEE-005.
- Dependencies: DEE-002, DEE-003.
- Source anchors: `DESIGN.md#Validation-Rules`, Distill quality bar/output contract.
- Write scope: validator semantic core and unit tests.
- Done criteria: diagnostics are stable and fail closed.
- Acceptance evidence: semantic test report.
- Validation: deterministic validator unit suite.
- Execution owner: task-session.
- Completion evidence: `work-pack/results/SWU-DEE-004-RESULT.md`.

## SWU-DEE-005: Provenance And Cross-Artifact Agreement

- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-005-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-005-LIFECYCLE-RECEIPT.md).
- Primary behavior: reject stale, unresolved, or contradictory reviewed-input and result
  evidence under the lifecycle-accepted provenance policy.
- Acceptance boundary: exact accepted provenance passes; changed content, unresolved handles,
  verdict/count mismatch, or stale work-pack binding blocks.
- Split analysis: provenance and cross-artifact agreement share the single decision of whether
  the result applies to these reviewed inputs; role semantics remain DEE-004.
- Dependencies: DEE-004.
- Source anchors: `DESIGN.md#Validation-Rules`, accepted DEC-DEE-001 receipt.
- Write scope: provenance resolver, cross-artifact checks, focused fixtures.
- Done criteria: validator result alone controls `mutation_handoff_allowed`.
- Acceptance evidence: provenance/mismatch test report.
- Validation: deterministic focused and integration suites.
- Execution owner: task-session.
- Completion evidence: `work-pack/results/SWU-DEE-005-RESULT.md`.
