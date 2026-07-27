# TASK-DRE-01: Runtime Emission

## Objective

Add the Distill-owned producer and prove complete event sequences for both
execution paths without changing the accepted consumer contract.

## Dependencies

- Sigil Development acceptance of `DEC-DRE-001`.
- [Shared context](../shared/context.md).

## SWU-DRE-001 — Single Event Producer

- Primary behavior: append one schema-valid event with optimistic ledger digest.
- Split analysis: schema validation and append are not independently useful;
  the transaction is the smallest producer proof.
- Write scope:
  - `arcanum/arcana/distill/scripts/emit-runtime-event.py`
  - `arcanum/arcana/distill/development/fixtures/runtime-emission/`
  - `arcanum/arcana/distill/development/run-distill-runtime-emission-fixtures.sh`
- Done: one capability-probe event appends; malformed event and stale digest do
  not write.
- Validation: focused emitter runner plus accepted schema validation.
- Execution owner: manual through Sigil Development.
- Handoff: only a passing result may select DRE-002.

## SWU-DRE-002 — True-Subagent Sequence

- Primary behavior: emit the complete accepted boundary sequence using stable,
  distinct native invocation references.
- Split analysis: role starts/results and reconciliation cannot pass separately
  because the resolver accepts only a closed sequence.
- Dependencies: DRE-001.
- Write scope: emitter, true-subagent fixtures, focused runner.
- Done: emitted ledger resolves; same role ID, changed run/path, missing
  boundary, and order drift block.
- Validation: existing Invoke resolver plus producer-invoking fixture.
- Execution owner: manual through Sigil Development.
- Handoff: only a passing result may select DRE-003.

## SWU-DRE-003 — Role-Simulation Sequence

- Primary behavior: emit the complete accepted fallback boundary sequence with
  labeled roles and no native invocation references.
- Split analysis: role boundaries form one resolver-accepted fallback trace.
- Dependencies: DRE-002.
- Write scope: emitter, simulation fixtures, focused runner.
- Done: emitted ledger resolves; invented native IDs and path drift block; role
  boundary shape matches true-subagent output.
- Validation: existing Invoke resolver plus cross-path check.
- Execution owner: manual through Sigil Development.
- Handoff: only a passing result may select DRE-004.
