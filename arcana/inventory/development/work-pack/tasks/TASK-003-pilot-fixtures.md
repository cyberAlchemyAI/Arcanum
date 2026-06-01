# TASK-003: Create Pilot Fixtures

## Objective

Create bounded CyberAlchemy pilot fixtures that prove the evidence-card schema, index, and retrieval contract.

## Source Contracts

- `../shared/SOURCE-CONTRACTS.md`
- `../../CONCEPT-MODEL.md`
- `../../FLOWS-POLICIES.md`

## Smallest Working Units

### SWU-INV-KS-005

- Goal: Add `arcana/inventory/development/pilot/evidence-card/pilot-cards.json`.
- Dependencies: TASK-002.
- Write scope: `arcana/inventory/development/pilot/evidence-card/pilot-cards.json`.
- Done criteria: at least 10 cards; mix includes two source-summary, three concept, one method, three claim, and one question.
- Validation: `jq empty arcana/inventory/development/pilot/evidence-card/pilot-cards.json` plus card mix review.
- Execution owner: subagent.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-005-CONTEXT.md`, `../../task-session/SWU-INV-KS-005-RESULT.md`.

### SWU-INV-KS-006

- Goal: Add `pilot-index.json` and `pilot-retrieval.json`.
- Dependencies: SWU-INV-KS-005.
- Write scope: `arcana/inventory/development/pilot/evidence-card/pilot-index.json`, `arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json`.
- Done criteria: index references pilot card IDs; retrieval includes selected and excluded matches.
- Validation: `jq empty arcana/inventory/development/pilot/evidence-card/pilot-index.json arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json`
- Execution owner: subagent.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-006-CONTEXT.md`, `../../task-session/SWU-INV-KS-006-RESULT.md`.

## Synchronization

After completion, unblock handoff examples.

## Completion Evidence

| SWU | Status | Evidence | Validation |
| --- | --- | --- | --- |
| SWU-INV-KS-005 | completed | `arcana/inventory/development/pilot/evidence-card/pilot-cards.json` | `jq empty`; mix review: 11 cards, 2 source-summary, 3 concept, 1 method, 4 claim, 1 question |
| SWU-INV-KS-006 | completed | `pilot-index.json`, `pilot-retrieval.json` | `jq empty`; ID consistency: 11 referenced IDs, no missing references |
