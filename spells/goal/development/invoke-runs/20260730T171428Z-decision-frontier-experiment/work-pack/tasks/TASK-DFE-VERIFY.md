# TASK-DFE-VERIFY

## VERIFY-DFE-001: Independent Closure

- Layer / wave: L3 / W8
- Type: closure-only exemption; not a mutation SWU
- Dependency: owner receipts for SWU-DFE-001 through 007

Capture before/after SHA-256 for the bounded canonical inputs named in
`CONTEXT.md`, then reconcile every witness, scoped delta, terminal receipt, and
owner receipt against [TRACEABILITY.md](../shared/TRACEABILITY.md). Confirm
there is no missing evidence, expected/observed collapse, private content,
canonical mutation, tracker operation, or decision/task state coupling.

### Output

The reviewer may write only:

1. `spells/goal/development/decision-frontier-experiment/session-evidence/VERIFY-DFE-001/authority-hashes.json`
2. `spells/goal/development/decision-frontier-experiment/session-evidence/VERIFY-DFE-001/closure-receipt.json`

DFE-FIX-010 passes only when the exact canonical hashes match. The receipts are
evidence, not implementation mutation. A pass makes
READINESS-DFE-001 eligible and unselected. Any contradiction reopens the exact
owning SWU or Invoke artifact.
