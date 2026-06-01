# User Ledger Implementation Layering

## Objective

Build the smallest useful `user-ledger` candidate package before runtime storage or command installation.

## L0: Fixture Proof

Question: Can the ledger represent the minimum rows needed by Translate and Guide?

Deliverables:

- `USER-LEDGER-SCHEMA.yml`
- `USER-LEDGER-FIXTURE.md`
- validation notes proving concept state, vocabulary preference, and receipt references.

Promotion evidence:

- schema parses,
- fixture has one domain anchor, one vocabulary preference, one concept state, one receipt ref, one residue row.

## L1: Receipt Intake

Question: Can Translate/Guide receipts update ledger state without overclaiming mastery?

Deliverables:

- receipt update rules,
- clarified-vs-mastered fixture,
- failed analogy residue fixture.

Promotion evidence:

- passive "I understand" cannot create mastery,
- teach-back or transfer can create mastery.

## L2: Governance And Visibility

Question: Are local memory boundaries explicit enough for runtime work?

Deliverables:

- visibility policy rows,
- reset/export/defer notes,
- promotion split validation.

Promotion evidence:

- canonical promotion is blocked without separate owner review.

## L3: Runtime Candidate

Question: Is the package ready for command/runtime implementation?

Deliverables:

- sigil-development handoff,
- task-session work-pack,
- optional runtime adapter design.

Promotion evidence:

- L0-L2 fixtures pass and user approves runtime storage behavior.
