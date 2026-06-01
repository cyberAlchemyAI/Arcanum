# TASK-007: Implement Shell Plus jq Validator Runtime

## Objective

Implement the first executable Inventory evidence-card validator as a fast agent/runtime surface using shell plus `jq`.

The human-facing validator UI is intentionally deferred.

## Source Contracts

- `../../VALIDATOR-SURFACE-DECISION.md`
- `../../READINESS.md`
- `../../templates/evidence-card-lint.md`
- `../../../templates/evidence-card-schema.md`
- `../../pilot/evidence-card/`

## Batch Policy

`SWU-INV-KS-010`, `SWU-INV-KS-011`, and `SWU-INV-KS-012` may run in the same task-session batch because:

- all depend only on completed `TASK-001` through `TASK-006`;
- their write scopes are disjoint;
- none writes shared readiness or task-session evidence.

`SWU-INV-KS-013` must run after those three complete.

## Smallest Working Units

### SWU-INV-KS-010

- Goal: Add `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`.
- Dependencies: TASK-001 through TASK-006.
- Write scope: `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`.
- Done criteria: validator checks required fields, controlled vocabularies, selector shape, full/minimal profile rules, `promotion_owner` terminal-status pairing, relation candidate notices, handoff `source_refs`, and packet non-authority text.
- Validation: `bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card`
- Execution owner: local-fallback.
- Handoff status: completed.
- Evidence: `../../task-session/TASK-007-RESULT.md`.

### SWU-INV-KS-011

- Goal: Add invalid examples fixture.
- Dependencies: TASK-001 through TASK-006.
- Write scope: `arcana/inventory/development/pilot/evidence-card/invalid-examples.json`.
- Done criteria: fixture includes selector, enum, owner/status, relation notice, and minimal-profile misuse examples.
- Validation: `jq empty arcana/inventory/development/pilot/evidence-card/invalid-examples.json`.
- Execution owner: local-fallback.
- Handoff status: completed.
- Evidence: `../../task-session/TASK-007-RESULT.md`.

### SWU-INV-KS-012

- Goal: Add validator runtime contract notes.
- Dependencies: TASK-001 through TASK-006.
- Write scope: `arcana/inventory/development/VALIDATOR-RUNTIME.md`.
- Done criteria: document names shell plus `jq` as agent/runtime surface, keeps human UI deferred, and states batch execution rules.
- Validation: `rg -n "shell|jq|agent/runtime|human UI|batch" arcana/inventory/development/VALIDATOR-RUNTIME.md`.
- Execution owner: local-fallback.
- Handoff status: completed.
- Evidence: `../../task-session/TASK-007-RESULT.md`.

### SWU-INV-KS-013

- Goal: Run validator and synchronize readiness evidence.
- Dependencies: SWU-INV-KS-010, SWU-INV-KS-011, SWU-INV-KS-012.
- Write scope: `arcana/inventory/development/READINESS.md`, `arcana/inventory/development/task-session/`.
- Done criteria: validator result is recorded; human UI remains deferred; any remaining blocker is named.
- Validation: validator run plus readiness grep.
- Execution owner: local-fallback.
- Handoff status: completed.
- Evidence: `../../task-session/TASK-007-RESULT.md`.

## Synchronization

After `SWU-INV-KS-013`, update `WORK-PACK.md`, `EXECUTION-PACK.md`, and this task file with completion evidence.

## Completion Evidence

| SWU | Status | Evidence | Validation |
| --- | --- | --- | --- |
| SWU-INV-KS-010 | completed | `arcana/inventory/scripts/validate-evidence-card-fixtures.sh` | `bash -n` and validator run |
| SWU-INV-KS-011 | completed | `invalid-examples.json` | `jq empty` |
| SWU-INV-KS-012 | completed | `VALIDATOR-RUNTIME.md` | `rg -n "shell|jq|agent/runtime|human UI|batch"` |
| SWU-INV-KS-013 | completed | `READINESS.md`, `TASK-007-RESULT.md` | validator run plus readiness sync |
