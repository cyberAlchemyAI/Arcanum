# TASK-SRG-PRODUCER — Deterministic plan producer

## Smallest Working Units

### SWU-SRG-003 — Semantic normalizer

- Primary behavior: resolve declared selectors and produce canonical component and per-unit digests from normalized selected values.
- Dependencies: SWU-SRG-002.
- Inputs: binding selectors, complete unit contract, normalizer version.
- Algorithm: resolve each JSON Pointer; preserve array order where contractually ordered; sort object keys; reject floats/non-JSON/unknown selectors; build closed component payloads; hash canonical UTF-8 JSON; keep whole-file hashes as provenance only.
- Write scope: audit-owned normalizer module and deterministic unit tests.
- Edge cases: missing selector, duplicate binding ID, unordered data without an explicit normalization rule, unknown schema version, byte-only change outside selected value.
- Done: repeated values yield identical digests; semantic changes alter the named component; status-only changes do not.
- Split analysis: selector resolution and canonical hashing cannot pass independently because partial normalization would create incompatible epoch identities.
- Verification: normalizer fixture suite, including status-only equivalence and command-cwd mutation.
- Owner: Spellcraft lifecycle worker.

### SWU-SRG-004 — Plan-once audit projection

- Primary behavior: emit the semantic manifest and pending-selection route without material packages.
- Dependencies: SWU-SRG-003.
- Algorithm: run existing plan/receipt checks; invoke the normalizer; classify missing material as pending only for the new profile; emit manifest and selection handoff; emit Refresh signals only for actual defects; preserve strict branch byte behavior.
- Write scope: audit runner, output renderer, plan-once fixtures, and README phase/output text.
- Done: five-unit no-material case passes plan scope, returns pending, and names explicit selection; strict case still blocks.
- Split analysis: classification and output routing form one observable behavior; semantic normalizer is already isolated in 003.
- Verification: v1, strict v2, and plan-once audit suites.
- Owner: Spellcraft lifecycle worker.

## Closeout

Use the Work Pack closeout contract. Unique successors: 003→004→005.
