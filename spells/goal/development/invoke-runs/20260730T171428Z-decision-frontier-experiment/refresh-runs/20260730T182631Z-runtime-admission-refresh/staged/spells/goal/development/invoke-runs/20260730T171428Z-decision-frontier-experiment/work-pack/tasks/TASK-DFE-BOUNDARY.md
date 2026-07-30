# TASK-DFE-BOUNDARY

Implementation detail: [BOUNDARY.md](../details/BOUNDARY.md).

## Objective

Prove three distinct control boundaries without allowing one passing concern
to hide another: human routing, decision-terminal evaluation, and
decision-versus-execution non-collapse.

## Smallest Working Units

### SWU-DFE-005: Enforce The HITL Stop

- Layer / wave: L2 / W5
- Status: dependency-bound
- Dependency: SWU-DFE-004 owner receipt
- Goal / primary behavior: route a human-owned frontier node and stop without
  synthesizing a resolution or reconciliation proposal.

#### Source Anchors

FR-07, invariant 6, State/Event extension, DFE-FIX-011.

#### Split Analysis

HITL routing has an independently reviewable negative boundary. It is
therefore separate from Way Clear and execution-state assertions.

#### Exact Write Scope SWU-DFE-005

1. `spells/goal/development/decision-frontier-experiment/runtime/hitl.py`
2. `spells/goal/development/decision-frontier-experiment/fixtures/hitl-map.json`
3. `spells/goal/development/decision-frontier-experiment/fixtures/expected/hitl-route.json`
4. `spells/goal/development/decision-frontier-experiment/scripts/run_hitl_fixture.py`
5. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-005/baseline.json`
6. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-005/hitl-validation.json`
7. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-005/task-session-receipt.json`
8. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-005/owner-receipt.json`

#### Done And Evidence

- the route receipt names the human owner and exact decision/map digest;
- no answer, resolution receipt, or reconciliation proposal is produced;
- DFE-FIX-011 passes and a synthetic auto-resolution mutant fails.

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/run_hitl_fixture.py`.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback` in the selected Task
  Session.
- Context: this SWU, shared files, Goal control boundary, reconciliation
  results, and SWU-DFE-004 receipts.
- Known blockers: 004 is unexecuted; this SWU is unselected.
- Expected result: eight exact targets and a passing HITL stop receipt.

#### Closeout

Use the shared contract. Allowed deltas: `artifact_added`,
`evidence_added`. Passing Invoke Refresh closeout makes SWU-DFE-006 eligible and
unselected.

### SWU-DFE-006: Evaluate The Strict Way Clear Predicate

- Layer / wave: L2 / W6
- Status: dependency-bound
- Dependency: SWU-DFE-005 owner receipt
- Goal / primary behavior: emit Way Clear only when no in-scope precise open
  decision and no unresolved fog remains.

#### Source Anchors

FR-09, invariant 7, State/Event extension, DFE-FIX-012.

#### Split Analysis

Way Clear is a pure independently reviewable predicate. It is separate from
human routing and from the effect of decision closure on execution state.

#### Exact Write Scope SWU-DFE-006

1. `spells/goal/development/decision-frontier-experiment/runtime/way_clear.py`
2. `spells/goal/development/decision-frontier-experiment/fixtures/way-clear-map.json`
3. `spells/goal/development/decision-frontier-experiment/fixtures/way-clear-open-mutant.json`
4. `spells/goal/development/decision-frontier-experiment/fixtures/way-clear-fog-mutant.json`
5. `spells/goal/development/decision-frontier-experiment/fixtures/expected/way-clear.json`
6. `spells/goal/development/decision-frontier-experiment/scripts/run_way_clear_fixtures.py`
7. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-006/baseline.json`
8. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-006/way-clear-validation.json`
9. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-006/task-session-receipt.json`
10. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-006/owner-receipt.json`

#### Done And Evidence

- terminal fixture emits one digest-bound Way Clear receipt;
- open-decision and unresolved-fog mutants each block;
- receipt changes no decision or execution state;
- DFE-FIX-012 passes.

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/run_way_clear_fixtures.py`.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback`.
- Context: this SWU, shared files, frontier/reconciliation contracts, and
  SWU-DFE-005 receipts.
- Known blockers: 005 is unexecuted; this SWU is unselected.
- Expected result: ten exact targets and three predicate observations.

#### Closeout

Allowed deltas: `artifact_added`, `evidence_added`. Passing Invoke Refresh closeout
makes SWU-DFE-007 eligible and unselected.

### SWU-DFE-007: Prove Decision Closure Does Not Complete Execution

- Layer / wave: L2 / W7
- Status: dependency-bound
- Dependency: SWU-DFE-006 owner receipt
- Goal / primary behavior: prove resolution and Way Clear bytes never change a
  task, SWU, or Goal execution-node state.

#### Source Anchors

FR-10, invariants 7 and 8, State/Event extension, DFE-FIX-008.

#### Split Analysis

Non-collapse is an independently acceptable cross-state invariant. It reads
the prior receipts but owns no HITL or terminal predicate behavior.

#### Exact Write Scope SWU-DFE-007

1. `spells/goal/development/decision-frontier-experiment/fixtures/execution-state.json`
2. `spells/goal/development/decision-frontier-experiment/fixtures/decision-closure.json`
3. `spells/goal/development/decision-frontier-experiment/fixtures/expected/execution-state-unchanged.json`
4. `spells/goal/development/decision-frontier-experiment/scripts/run_noncollapse_fixture.py`
5. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-007/baseline.json`
6. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-007/noncollapse-validation.json`
7. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-007/task-session-receipt.json`
8. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-007/owner-receipt.json`

#### Done And Evidence

- exact before/after execution-state bytes match;
- decision resolution and Way Clear remain evidence inputs only;
- a mutant that marks a task/SWU complete fails;
- DFE-FIX-008 passes.

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/run_noncollapse_fixture.py`.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback`.
- Context: this SWU, shared files, Task Session/Goal read-only boundaries, and
  SWU-DFE-001 through 006 receipts.
- Known blockers: 006 is unexecuted; adapter and canonical representation are
  later lifecycle gaps.
- Expected result: eight exact targets and byte-identity evidence.

#### Closeout

Allowed deltas: `artifact_added`, `evidence_added`. Passing Invoke Refresh closeout
makes VERIFY-DFE-001 eligible and unselected.
