# TASK-DFE-RECONCILE

Implementation detail: [RECONCILE.md](../details/RECONCILE.md).

## Smallest Working Units

### SWU-DFE-004: Stage Reconciliation Proposals

- Layer / wave: L1 / W4
- Status: dependency-bound
- Dependency: SWU-DFE-003 owner receipt
- Goal / primary behavior: transform a valid resolution receipt into an immutable,
  causal proposal without changing the input decision map.

#### Source Anchors

FR-08, invariants 4 and 8, State/Event extension, DFE-FIX-005 and 007.

#### Split Analysis

Resolution validation and reconciliation could be separate modules, but a
validated receipt with no bounded proposal has no experiment utility, while a
proposal without validation violates the causal boundary. Retain one SWU.

#### Exact Write Scope

1. `spells/goal/development/decision-frontier-experiment/runtime/reconcile.py`
2. `spells/goal/development/decision-frontier-experiment/fixtures/fog-resolution.json`
3. `spells/goal/development/decision-frontier-experiment/fixtures/invalidation-resolution.json`
4. `spells/goal/development/decision-frontier-experiment/fixtures/add-resolution.json`
5. `spells/goal/development/decision-frontier-experiment/fixtures/supersede-resolution.json`
6. `spells/goal/development/decision-frontier-experiment/fixtures/unblock-resolution.json`
7. `spells/goal/development/decision-frontier-experiment/fixtures/expected/fog-reconciliation.json`
8. `spells/goal/development/decision-frontier-experiment/fixtures/expected/invalidation-reconciliation.json`
9. `spells/goal/development/decision-frontier-experiment/fixtures/expected/add-reconciliation.json`
10. `spells/goal/development/decision-frontier-experiment/fixtures/expected/supersede-reconciliation.json`
11. `spells/goal/development/decision-frontier-experiment/fixtures/expected/unblock-reconciliation.json`
12. `spells/goal/development/decision-frontier-experiment/scripts/run_reconciliation_fixtures.py`
13. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-004/baseline.json`
14. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-004/reconciliation-validation.json`
15. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-004/task-session-receipt.json`
16. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-004/owner-receipt.json`

#### Done And Evidence

- receipt ID, owner route, node ID, and source digest validate;
- fog graduation requires a precise question and owner;
- add, invalidate, supersede, and unblock proposals preserve causal history;
- input map hash is unchanged;
- output is explicitly `proposal` authority;
- DFE-FIX-005 and 007 pass.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback` inside the selected
  Task Session.
- Selection-bound context: this task file, shared files, reconciliation design,
  claim contract, and SWU-DFE-003 terminal and closeout receipts.
- Known blockers: 003 is unexecuted; accepted Craft representation remains a
  later Design gap and is not part of this SWU.
- Expected result: sixteen targets and proposal-only causal receipts with unchanged
  source-map bytes.

#### Closeout

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/run_reconciliation_fixtures.py`.
Allowed deltas: `artifact_added`, `evidence_added`. Passing Invoke Refresh closeout receipt
makes SWU-DFE-005 eligible and unselected.
