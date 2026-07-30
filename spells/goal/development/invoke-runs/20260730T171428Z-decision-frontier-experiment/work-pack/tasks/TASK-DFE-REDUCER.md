# TASK-DFE-REDUCER

Implementation detail: [REDUCER.md](../details/REDUCER.md).

## Smallest Working Units

### SWU-DFE-002: Derive A Reason-Complete Frontier

- Layer / wave: L0 / W2
- Status: dependency-bound
- Dependency: passing owner receipt for SWU-DFE-001
- Goal / primary behavior: derive deterministic eligibility and exclusion reasons
  from one validated map.

#### Source Anchors

FR-03, FR-04, FR-05, FR-11; DFE-FIX-001, 006, and 009.

#### Split Analysis

Canonicalization and reduction could be separate functions, but neither has an
independent acceptance boundary: canonical bytes are the reducer's
reproducibility output. Claims remain separate because they write state.

#### Exact Write Scope

1. `spells/goal/development/decision-frontier-experiment/runtime/frontier.py`
2. `spells/goal/development/decision-frontier-experiment/fixtures/fog-map.json`
3. `spells/goal/development/decision-frontier-experiment/fixtures/scope-map.json`
4. `spells/goal/development/decision-frontier-experiment/fixtures/invalidated-map.json`
5. `spells/goal/development/decision-frontier-experiment/fixtures/expected/diamond-frontier.json`
6. `spells/goal/development/decision-frontier-experiment/fixtures/expected/fog-frontier.json`
7. `spells/goal/development/decision-frontier-experiment/fixtures/expected/scope-frontier.json`
8. `spells/goal/development/decision-frontier-experiment/fixtures/expected/invalidated-frontier.json`
9. `spells/goal/development/decision-frontier-experiment/scripts/run_frontier_fixtures.py`
10. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-002/baseline.json`
11. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-002/frontier-validation.json`
12. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-002/task-session-receipt.json`
13. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-002/owner-receipt.json`

#### Done And Evidence

- exact frontier and stable reasons match all four golden fixtures;
- fog, out-of-scope, and invalidated nodes are retained but excluded;
- two clean runs are byte-identical;
- reducer has no write or external effect;
- DFE-FIX-001, 006, and 009 receipts pass; fog and invalidated-state checks are
  internal reducer assertions whose lifecycle witness is owned by SWU-DFE-004.

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/run_frontier_fixtures.py --replay 2`.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback` inside the selected
  Task Session.
- Selection-bound context: this task file, shared files, SPEC, ARCHITECTURE,
  witness matrix, and SWU-DFE-001 terminal and closeout receipts.
- Known blockers: 001 is unexecuted; this SWU is not selected.
- Expected result: thirteen declared targets and exact reason/replay evidence;
  no stateful claim write.

#### Closeout

Allowed deltas: `artifact_added`, `evidence_added`. The Invoke Refresh owner replays the
fixtures. Passing closeout makes SWU-DFE-003 eligible and unselected.
