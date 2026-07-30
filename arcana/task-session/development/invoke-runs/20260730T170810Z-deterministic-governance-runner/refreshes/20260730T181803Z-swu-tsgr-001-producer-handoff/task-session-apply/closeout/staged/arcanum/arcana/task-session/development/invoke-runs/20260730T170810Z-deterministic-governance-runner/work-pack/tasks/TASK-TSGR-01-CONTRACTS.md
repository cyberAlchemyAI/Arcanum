# TASK-TSGR-01: Production Contracts

Layer: L0  
Dependencies: accepted `SWU-TSGR-000`

## SWU-TSGR-001 — production governance evaluator

Exact write scope:

- `arcana/task-session/scripts/evaluate-governance.py`
- `arcana/task-session/schemas/governance-evaluation-request.schema.json`
- `arcana/task-session/schemas/governance-evaluation-receipt.schema.json`
- `arcana/task-session/development/fixtures/governance-evaluation-cases.json`
- `arcana/task-session/development/validate-governance-evaluator.py`

Done criteria:

- evaluator is pure except for its named receipt output;
- every current decision-policy fixture has golden parity;
- malformed request, stale policy digest, unknown kind, and invalid outcome block;
- development evaluator duplication is identified for later removal or delegation,
  not silently left as competing authority.

Validation:

```text
python3 arcana/task-session/development/validate-governance-evaluator.py
python3 arcana/task-session/development/validate-decision-validation-policy.py
```

Acceptance evidence: parity matrix and schema-negative receipt.

Execution status: completed by
`work-pack/results/SWU-TSGR-001-RESULT.json` with result `pass`. Live validation
reported `golden=25/25`, `negative=5/5`, `schema=4/4`, and zero undeclared
outputs. The declared policy-validator command omits its two required positional
arguments; the same validator passed as the named accepted equivalent with
repository root `..` and canonical directory `arcana/task-session`. Development
evaluator duplication remains explicit residue for later removal or delegation.

## SWU-TSGR-002 — runner envelope family

Exact write scope:

- `arcana/task-session/schemas/governance-run-request.schema.json`
- `arcana/task-session/schemas/execution-ticket.schema.json`
- `arcana/task-session/schemas/governance-phase-receipt.schema.json`
- `arcana/task-session/schemas/executor-receipt.schema.json`
- `arcana/task-session/schemas/governance-terminal-receipt.schema.json`
- `arcana/task-session/development/fixtures/governance-run-contract-cases.json`
- `arcana/task-session/development/validate-governance-run-contracts.py`

Done criteria:

- every envelope is closed, versioned, and digest-bindable;
- predecessor, idempotency, allowed-write/output, timeout, and closeout fields are
  mandatory where applicable;
- fixtures reject shell strings, missing owner identity, skipped predecessor, and
  unbounded output.

Validation:

```text
python3 arcana/task-session/development/validate-governance-run-contracts.py
```

Acceptance evidence: positive/negative schema matrix.

Execution status: selected as the unique dependency-ready successor. Selection
does not authorize mutation; a fresh context pack, material handoff, and Task
Session admission remain required.

Both SWUs use the common closeout contract in
`work-pack/shared/EXECUTION-CONTROL.md`. The unique successors are TSGR-002 and
TSGR-003 respectively.
