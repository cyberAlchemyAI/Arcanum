# Guide Architecture Validation Experiment

## Purpose

Validate that `guide-architecture` can guide a bounded architecture target without owning Translate internals or User-ledger writes.

## Profile

- Experiment profile: `spellcraft`
- Runtime status: manual/static fixtures only
- Promotion status: blocked until candidate dependencies mature

## Fixture Set

| Fixture | Purpose | Expected Verdict |
| --- | --- | --- |
| `fixtures/ARCHITECTURE-BOUNDARY-GUIDE.md` | Happy path using sales-to-architecture translation. | pass |
| Future fixture: missing target scope | Proves phase 1 blocks. | block |
| Future fixture: unsafe analogy | Proves target-domain definition is preserved. | flag |

## Validation Questions

1. Does every phase have input, output, gate, and failure policy?
2. Does the spell call Translate instead of copying Translate internals?
3. Does the spell propose User-ledger updates instead of writing them?
4. Does the spell block live research/subagent dispatch without budget?
5. Does the spell define observability fields?

## Current Result

`flag`

The spell contract is structurally valid, but reusable-behavior validation is not complete because `user-ledger` and `translate` remain local candidate packages rather than canonical sigils.
