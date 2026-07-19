# TASK-DEE-05: Evidence Fixtures

Status: completed on 2026-07-17 after DEE-008 through DEE-010 evidence passed.

## Objective

Prove the validator discriminates execution evidence instead of merely checking labels or
schema presence.

Selection gate: blocked until accepted schema/validator owners and exact fixture/runner paths
are named. TASK-DEE-05 owns evidence fixture data; TASK-DEE-04 owns shared Invoke runner
integration.

## SWU-DEE-008: Resolvable Positive

- Status: selected under
  [SPELLCRAFT-DEE-008-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-008-LIFECYCLE-RECEIPT.md).

- Primary behavior: one valid evidence set resolves to expected pass.
- Acceptance boundary: request, events, receipt, reviewed inputs, and Invoke result agree.
- Split analysis: one fixture owns one outcome and cannot be split further.
- Dependencies: DEE-002, DEE-003, DEE-004, DEE-005.
- Write scope: positive fixture set and expected diagnostics.
- Validation: focused positive fixture command.
- Execution owner: task-session.
- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-008-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-008-LIFECYCLE-RECEIPT.md).

## SWU-DEE-009: Missing Evidence Negative

- Status: selected under
  [SPELLCRAFT-DEE-009-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-009-LIFECYCLE-RECEIPT.md).

- Primary behavior: an applicable Invoke mode with missing required evidence returns block.
- Acceptance boundary: expected mode-level missing-evidence diagnostic and no handoff
  permission.
- Split analysis: one failure class and one expected outcome.
- Dependencies: DEE-002, DEE-004, DEE-007.
- Write scope: missing-evidence fixture and expectation.
- Validation: focused missing-evidence command.
- Execution owner: task-session.
- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-009-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-009-LIFECYCLE-RECEIPT.md).

## SWU-DEE-010: Schema-Complete Fabrication Negative

- Status: selected under
  [SPELLCRAFT-DEE-010-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-010-LIFECYCLE-RECEIPT.md).

- Primary behavior: prove fabricated evidence detectors with isolated corruption cases and one
  combined fail-closed integration case.
- Acceptance boundary: schema passes; each one-corruption case emits its expected diagnostic;
  the combined case proves only fail-closed integration and need not reach every diagnostic.
- Split analysis: the detector matrix shares one adversarial evidence contract and runner;
  cases remain separate fixture instances so short-circuiting cannot masquerade as coverage.
- Dependencies: DEE-003, DEE-005.
- Write scope: fabricated fixture/event store/input mutation and expectations.
- Validation: focused fabricated-evidence command plus full suite.
- Execution owner: task-session.
- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-010-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-010-LIFECYCLE-RECEIPT.md).
