# Translate Implementation Layering

## L0: Translation Fixture Proof

Question: Can Translate produce a valid bridge with target truth preserved?

Deliverables:

- `TRANSLATE-SCHEMA.yml`
- `TRANSLATE-FIXTURES.md`

Fixtures:

- sales terms -> software architecture decision,
- software engineering terms -> scientific formula,
- musician terms -> civil construction plan,
- failed analogy with target-definition preservation.

## L1: Receipt Rules

Question: Can Translate produce receipts that User can safely evaluate?

Deliverables:

- `TRANSLATE-RECEIPT-SCHEMA.yml`
- receipt fixtures with `ledger_update_proposal`.

## L2: Integration Boundary

Question: Can Guide call Translate without translation logic leaking into Guide?

Deliverables:

- Guide-call contract,
- research-needed flag,
- target-definition guardrail.

## L3: Runtime Candidate

Question: Is Translate ready for command/runtime implementation?

Deliverables:

- sigil-development result,
- validation report,
- runtime handoff.
