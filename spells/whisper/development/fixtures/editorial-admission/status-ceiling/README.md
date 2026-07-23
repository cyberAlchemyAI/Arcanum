# Final-Status Ceiling Fixtures

This suite proves one pure decision: the strongest final status a typed Whisper run may claim. It does not decide whether generation was admissible, recompute digests, compare selected record IDs, or score human language and comprehension.

## Rule order

1. Validate the receipt schema; invalid envelopes block.
2. Apply candidate or unproven transport ceilings.
3. Apply required editorial-audition, newcomer-comprehension, and post-apply-review gates.
4. Apply active correction invalidation.
5. Apply explicit source/structure and implementation/render flags or blocks.
6. Respect an already computed generation block without recomputing generation policy.
7. Limit the result by the requested status.

Reason codes remain in that order. Existing `computed_decisions.status` values are ignored and recomputed so a stale optimistic receipt cannot certify itself.

## Fixture form

`status-ceiling-fixtures.json` defines causal operations over the schema-valid run receipt from the receipt-schema package. Each case changes only the inputs needed for its expected ceiling, final status, and ordered reasons.

The checked result is `status-ceiling-test-report.json`.

## Replay

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py \
  --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/status-ceiling
```

The command must exit zero and its JSON output must equal the checked report.

## Deferred binding

This unit consumes typed evidence states. Exact digest recomputation, selected-record equality, approval-kind admissibility, question-set equality, and prior-artifact detection remain evidence-binding work. Until that binder exists, digest-mismatch baseline controls are not enforced by this evaluator.
