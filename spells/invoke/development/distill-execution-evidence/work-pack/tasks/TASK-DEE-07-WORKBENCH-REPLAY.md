# TASK-DEE-07: Workbench Replay

Status: in-progress on 2026-07-17 after DEE-012; DEE-013 selected under its lifecycle receipt.

## Objective

Evaluate the current Workbench package through the accepted evidence path and append, never
rewrite, the controlling result.

Selection gate: blocked until accepted canonical/generated paths, replay command, and exact
Workbench/observability write paths are named.

## SWU-DEE-012: Replay Validation

- Status: selected under
  [SPELLCRAFT-DEE-012-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-012-LIFECYCLE-RECEIPT.md).

- Primary behavior: execute Distill Validate over the current repaired Workbench plan and emit
  an evidence/result set bound to that package.
- Acceptance boundary: validator produces pass, owned flag, or block with recomputed eleven-SWU
  agreement and resolvable role/process evidence.
- Split analysis: replay execution/result is independent of synchronizing Workbench route
  fields, which remains DEE-013.
- Dependencies: DEE-011.
- Source anchors: current Workbench plan/layering/work-pack/handoff/gaps and historical run.
- Write scope: new replay evidence and validator result only.
- Done criteria: historical evidence byte-preserved; result references it as predecessor.
- Acceptance evidence: validator report and provenance checks.
- Validation: replay command, eleven-SWU count check, JSON/JSONL parse.
- Execution owner: task-session with true subagents when supported.
- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-012-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-012-LIFECYCLE-RECEIPT.md).

## SWU-DEE-013: Superseding Status And Route

- Status: selected under
  [SPELLCRAFT-DEE-013-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-013-LIFECYCLE-RECEIPT.md).

- Primary behavior: append replay status and derive Workbench handoff eligibility from the
  validator result.
- Acceptance boundary: historical record unchanged; new status/observability agrees with the
  replay result; Task Session route exists only when permitted.
- Split analysis: status synchronization and route derivation are one projection behavior;
  replay evidence generation remains DEE-012.
- Dependencies: DEE-012.
- Source anchors: replay validator result and Workbench continuation artifacts.
- Write scope: Workbench result/status/Craft continuation and append-only observability.
- Done criteria: no stale five-versus-eleven ambiguity in the superseding record.
- Acceptance evidence: sync and append-only reports.
- Validation: Workbench tests, Craft consistency, JSONL parse, history digest comparison.
- Execution owner: task-session.
