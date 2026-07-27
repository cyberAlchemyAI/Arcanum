# Decision Gate: Phase-Accurate Block Receipts

## Decision

How should one canonical Inventory operation receipt represent causal facts
that do not exist because execution stopped at an earlier phase?

## Evidence

- `SWU-IFR-002` requires receipts for `tooling-unavailable`,
  `baseline-blocked`, and `invalid-request` in that precedence.
- The accepted v1 schema requires complete runtime, input, baseline, and
  candidate digests for every status.
- The L0 kernel correctly rejects missing or non-digest values.
- Invented sentinel digests would misrepresent unavailable evidence.

## Options

### A. One phase-aware receipt schema — recommended

Keep one receipt schema and one stdout contract, but make causal availability
explicit. Each phase-bound section records an evidence state such as
`observed`, `unavailable`, or `not-reached`; digests are required only when the
state is `observed`. JSON Schema status/phase constraints and kernel invariants
reject contradictory combinations.

Trade-off: revises L0 schema, kernel, and tests before L1 resumes.

### B. Separate preflight-block receipt schema

Use a smaller schema for failures before complete operation inputs exist, then
retain `inventory.operation-receipt.v1` for fully bound attempts.

Trade-off: simpler individual schemas, but consumers must branch across receipt
types and the accepted one-operation-receipt contract changes more deeply.

### Rejected: sentinel digests

Hashing empty strings or inserting fixed placeholder digests makes unavailable
evidence appear observed. This is not an admissible option.

## Recommendation

Choose A. It preserves one receipt stream and makes causal incompleteness
machine-checkable without fabricating proof.

## Required Lifecycle Action

Sigil Development should add or approve a bounded L0 repair unit that may
change:

```text
arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json
arcana/inventory/lib/operation-receipt.cjs
arcana/inventory/test/operation-receipt.test.cjs
```

After that repair passes, reselect `SWU-IFR-002`. Task Session must not widen
the current L1 write scope implicitly.
