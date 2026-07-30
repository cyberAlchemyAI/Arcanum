# Planned Witness Contracts

| ID | Contract | Expected observation |
| --- | --- | --- |
| DFE-FIX-001 | diamond dependency | only the two root decisions are eligible; stable lexical order |
| DFE-FIX-002 | claimed root | claimed node is excluded with `active_claim`; other eligible root remains |
| DFE-FIX-003 | invalid-graph matrix | cycle, duplicate ID, unknown endpoint, invalid state, and invalid route each fail before frontier output |
| DFE-FIX-004 | stale claim | digest mismatch rejects claim without state mutation |
| DFE-FIX-005 | fog graduation | fog is excluded until a precise question and owner are supplied |
| DFE-FIX-006 | out-of-scope retention | node remains excluded and retained without destination redraw |
| DFE-FIX-007 | reconciliation transition matrix | add, invalidate, supersede, and unblock proposals preserve causal history and never mutate the input map |
| DFE-FIX-008 | decision/execution separation | resolution changes no task, SWU, or execution status |
| DFE-FIX-009 | deterministic replay | canonical outputs are byte-identical over repeated runs |
| DFE-FIX-010 | authority hash | bounded canonical inputs have identical before/after hashes |
| DFE-FIX-011 | HITL stop | controller emits a human route and cannot auto-resolve |
| DFE-FIX-012 | Way Clear predicate | receipt appears only with no open precise node and no unresolved fog |

## Witness Rules

- Every fixture is synthetic and contains no private project prose.
- Expected and observed values remain separate.
- A failed mutant that produces output is a blocker.
- Fixture pass supports only the named behavior.
- Cross-capability benefit and canonical adoption require later evidence.
