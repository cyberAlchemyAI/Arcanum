# TASK-DFE-CONTRACT

Implementation detail: [CONTRACT.md](../details/CONTRACT.md).

## Smallest Working Units

### SWU-DFE-001: Close Contract And Graph Validation

- Layer / wave: L0 / W1
- Status: first candidate, not selected
- Dependencies: W0 baseline
- Goal / primary behavior: reject invalid decision-map and receipt inputs before any
  reducer or stateful write.

#### Source Anchors

FR-01, FR-02, invariants 1-5, Persistence/Concurrency and Data Lifecycle
extensions, DFE-FIX-003.

#### Split Analysis

Schemas without graph mutants would not prove a fail-closed boundary; mutants
without versioned schemas would not define accepted input. Retain them as one
unit. The reducer is independently useful and remains SWU-DFE-002.

#### Exact Write Scope

1. `spells/goal/development/decision-frontier-experiment/README.md`
2. `spells/goal/development/decision-frontier-experiment/schemas/decision-map.schema.json`
3. `spells/goal/development/decision-frontier-experiment/schemas/frontier-snapshot.schema.json`
4. `spells/goal/development/decision-frontier-experiment/schemas/claim.schema.json`
5. `spells/goal/development/decision-frontier-experiment/schemas/resolution.schema.json`
6. `spells/goal/development/decision-frontier-experiment/schemas/reconciliation.schema.json`
7. `spells/goal/development/decision-frontier-experiment/schemas/way-clear.schema.json`
8. `spells/goal/development/decision-frontier-experiment/fixtures/diamond-map.json`
9. `spells/goal/development/decision-frontier-experiment/fixtures/cycle-map.json`
10. `spells/goal/development/decision-frontier-experiment/scripts/validate_contracts.py`
11. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-001/baseline.json`
12. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-001/contract-validation.json`
13. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-001/task-session-receipt.json`
14. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-001/owner-receipt.json`

#### Done And Evidence

- all positive schema fixtures validate;
- duplicate ID, unknown endpoint, cycle, invalid state, and invalid route
  mutants fail before output;
- fixtures are synthetic and source schemas declare no authority effect;
- DFE-FIX-003 receipt binds exact bytes;
- scoped diff contains only the fourteen targets.

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/validate_contracts.py`.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback` inside the selected
  Task Session; manual-only execution is not required.
- Selection-bound context: this task file, shared context/decisions/gaps/
  traceability/closeout, SPEC, ARCHITECTURE, WITNESS-CONTRACTS, exact canonical
  read-only sources, and W0 baseline.
- Known blockers: Spellcraft acceptance and explicit selection are absent.
- Expected result: fourteen declared targets plus a passing terminal receipt;
  no canonical or tracker delta.

#### Closeout

Use the shared closeout contract. Allowed deltas:
`artifact_added`, `evidence_added`. The Invoke Refresh owner validates the command and exact
inventory. Passing closeout makes SWU-DFE-002 eligible and unselected.
