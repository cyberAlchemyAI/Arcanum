# TASK-DEE-02: Evidence Substrate

## Objective

Implement the lifecycle-accepted request, receipt/result, and append-only runtime event
contracts.

Selection gate: blocked until the Spellcraft receipt names the canonical owner and exact write
paths for both SWUs.

## SWU-DEE-002: Evidence Schemas

- Status: completed on 2026-07-17.

- Primary behavior: validate the structural shape and version of run request, receipt, and
  validation result artifacts.
- Acceptance boundary: valid shapes parse; missing identity, budget, role trace, techniques,
  verdict, or result fields fail schema validation.
- Split analysis: request/receipt/result form one versioned projection contract; runtime event
  emission is independently testable and remains DEE-003.
- Dependencies: DEE-001.
- Source anchors: `DESIGN.md#3-Information-And-Type-View`.
- Write scope: lifecycle-accepted schema and schema-test paths only.
- Done criteria: schemas, valid fixtures, malformed fixtures, deterministic validation.
- Acceptance evidence: schema test report.
- Validation: accepted schema validator command plus `jq`/parser checks.
- Execution owner: task-session after Spellcraft handoff.
- Completion evidence: [SWU-DEE-002-RESULT.md](../results/SWU-DEE-002-RESULT.md).
- Experiment evidence: focused structural runner passed 10 of 10 checks; execution proof and
  mutation readiness remain outside this SWU.

## SWU-DEE-003: Runtime Event Contract

- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-003-LIFECYCLE-RECEIPT.md](../../SPELLCRAFT-DEE-003-LIFECYCLE-RECEIPT.md).
- Primary behavior: represent ordered runtime evidence for true-subagent and role-simulation
  paths without invented identities.
- Acceptance boundary: both valid event sequences resolve; same-role identities, missing
  boundaries, invalid ordering, or simulated native IDs block.
- Split analysis: the two paths share one event grammar and one resolver boundary, so splitting
  by path would duplicate the acceptance contract.
- Dependencies: DEE-001.
- Source anchors: `DESIGN.md#4-Operation-And-Flow-View`, Distill runtime-role policy.
- Write scope: exact event schema, append/resolve adapter, fixture, runner, and evidence paths in
  the Spellcraft receipt.
- Done criteria: ordered event grammar and tests for both paths.
- Acceptance evidence: resolver test report.
- Validation: deterministic event resolution suite.
- Execution owner: Task Session, one SWU only.
- Completion evidence: [SWU-DEE-003-RESULT.md](../results/SWU-DEE-003-RESULT.md).
- Experiment evidence: focused event runner passed 21 of 21 checks; semantic validation and
  mutation readiness remain outside this SWU.
