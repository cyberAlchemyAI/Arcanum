# Validation Strategy

## Purpose

Bind every planned behavior to deterministic positive, negative, parity, and
live-evidence checks without treating planned commands as executed proof.

## Validation Levels

| Level | Target | Required Evidence | Owner |
| --- | --- | --- | --- |
| V0 | schemas and fixture shape | schema validator output and negative fixture diagnostics | selected Task Session |
| V1 | compiler mechanics | exact object, payload, and receipt hashes across replay | selected Task Session |
| V2 | selection and rendering | coverage, deduplication, ordering, budget, and output parity receipts | selected Task Session |
| V3 | cache and usage semantics | stale/corrupt/base/tokenizer mutants and separated measurement fields | selected Task Session |
| V4 | reusable behavior | paired Experiment Harness run with coverage parity and actual usage when available | Sigil Development |
| V5 | canonical integration | public hygiene, contract compatibility, generated-parity receipt where an admitted mirror exists | Sigil Development |

## Planned Deterministic Command Surface

These commands describe the target interface. They are not available until
their owning SWU implements them.

```bash
python3 transmutations/context-builder/scripts/validate_context_request.py \
  transmutations/context-builder/development/fixtures/request/valid-single-selector.json

python3 transmutations/context-builder/scripts/compile_context_pack.py \
  --repository-root . \
  --request transmutations/context-builder/development/fixtures/request/valid-single-selector.json \
  --output-root transmutations/context-builder/development/fixtures/actual/single-selector

python3 transmutations/context-builder/scripts/validate_context_pack.py \
  transmutations/context-builder/development/fixtures/actual/single-selector/pack-receipt.json
```

Each task file narrows these commands to its exact outputs and fixtures.

## Witness Mapping

| Witness | Owning SWU | Gate |
| --- | --- | --- |
| DCC-FIX-001, DCC-FIX-003, DCC-FIX-006 | SWU-DCC-002 | L0 replay/freshness |
| request malformed and duplicate-ID mutants | SWU-DCC-001 | L0 schema |
| DCC-FIX-002, DCC-FIX-004, DCC-FIX-005, DCC-FIX-007, DCC-FIX-008 | SWU-DCC-003 | L1 selection |
| DCC-FIX-011, DCC-FIX-012 | SWU-DCC-004 | L1 parity/injection |
| DCC-FIX-009 | SWU-DCC-005 | L2 measurement |
| DCC-FIX-010 and corrupt-cache mutant | SWU-DCC-006 | L2 reuse |
| paired baseline/candidate live contract | SWU-DCC-007 | L3 reusable behavior |
| public hygiene and canonical compatibility | SWU-DCC-008 | L3 lifecycle integration |

## Invariants

1. A passing compile covers every required obligation.
2. Current source bytes outrank cache, Inventory, and earlier receipts.
3. Same admitted inputs and compiler versions produce byte-identical outputs.
4. Persisting multiple evidence formats never implies multiple runtime payloads.
5. Missing token or runtime evidence remains explicitly unknown.
6. A failed negative fixture is a blocker, not a warning.
7. Live cost evidence is comparable only when source snapshot and obligation
   coverage are equal.
8. No command or receipt grants lifecycle promotion.

## Public Boundary Check

Every public fixture and canonical change is scanned for consumer-local absolute
paths, private project names, raw private prose, credentials, and cache bodies.
A sanitized structural fixture is acceptable; mechanical redaction of private
meaning into the public package is not.

## Validation Ceiling

This strategy is Plan evidence. None of its future commands or witnesses have
run as part of Invoke.
