# TASK-DFE-CLAIM

Implementation detail: [CLAIM.md](../details/CLAIM.md).

## Smallest Working Units

### SWU-DFE-003: Enforce Digest-Bound Claims

- Layer / wave: L1 / W3
- Status: dependency-bound
- Dependency: SWU-DFE-002 owner receipt
- Goal / primary behavior: compare-and-set at most one active claim against the exact
  map digest.

#### Source Anchors

FR-06, invariant 5, Persistence/Concurrency extension, DFE-FIX-002 and 004.

#### Split Analysis

Stale and competing-claim handling share one atomic admission decision.
Expiration and distributed recovery are not required for single-process
fixture proof and remain deferred.

#### Exact Write Scope

1. `spells/goal/development/decision-frontier-experiment/runtime/claims.py`
2. `spells/goal/development/decision-frontier-experiment/fixtures/active-claim.json`
3. `spells/goal/development/decision-frontier-experiment/fixtures/stale-claim.json`
4. `spells/goal/development/decision-frontier-experiment/fixtures/expected/claim-accepted.json`
5. `spells/goal/development/decision-frontier-experiment/fixtures/expected/claim-rejected-stale.json`
6. `spells/goal/development/decision-frontier-experiment/scripts/run_claim_fixtures.py`
7. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-003/baseline.json`
8. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-003/claim-validation.json`
9. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-003/task-session-receipt.json`
10. `spells/goal/development/decision-frontier-experiment/session-evidence/SWU-DFE-003/owner-receipt.json`

#### Done And Evidence

- only an eligible unclaimed node at the current digest can be claimed;
- stale and competing claims fail without replacing the active fixture;
- frontier reports `active_claim` deterministically;
- DFE-FIX-002 and 004 pass.

Planned command:
`python3 spells/goal/development/decision-frontier-experiment/scripts/run_claim_fixtures.py`.

#### Execution Owner And Handoff

- Recommendation: `subagent`; fallback: `local-fallback` inside the selected
  Task Session.
- Selection-bound context: this task file, shared files, contract/reducer
  sources, and SWU-DFE-002 terminal and closeout receipts.
- Known blockers: 002 is unexecuted; expiry and distributed recovery remain
  intentionally outside the acceptance boundary.
- Expected result: ten targets and a fail-closed claim receipt with
  `authority_effect: none`.

#### Closeout

Allowed deltas: `artifact_added`, `artifact_changed`, `evidence_added`.
The Invoke Refresh owner validates exact before/after claim bytes. Passing closeout makes
SWU-DFE-004 eligible and unselected.
