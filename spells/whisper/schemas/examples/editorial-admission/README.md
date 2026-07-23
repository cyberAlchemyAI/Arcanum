# Editorial Admission Schema Fixtures

This directory proves the shape boundary for Whisper editorial run receipts and correction events. It does not evaluate whether a requested generation or final status is correct.

## Package

- `schema-fixture-manifest.json` declares causal pass/fail cases as operations over complete base instances.
- `bases/run-good-complete-newcomer.json` is the full positive run-receipt instance.
- `bases/correction-good.json` is the positive correction-event instance.
- `run-schema-fixtures.py` applies each case and validates it with Draft 2020-12.
- `schema-test-report.json` is the checked replay result.

The operation form keeps negative cases focused: each case removes, replaces, or adds only the field needed to cause its recorded schema result.

## Covered boundaries

- all four evidence axes are separate and required;
- present human axes carry artifact and surface digests;
- approval records require approval kind and prompt identity;
- multiple approval records require a selected approval ID;
- comprehension records require a reviewer, question IDs, answers, and a human outcome;
- numeric semantic scoring fields are rejected;
- `not_required` comprehension is accepted only when the profile permits it;
- post-apply evidence requires producer and review stages;
- unknown statuses and malformed digests are rejected;
- residue accepts additive detail without weakening the closed receipt envelope.

Reference equality, selected-record identity, question-set equality, stage inequality, digest recomputation, generation decisions, and status ceilings are policy checks owned by later units.

## Replay

```bash
python3 arcanum/spells/whisper/schemas/examples/editorial-admission/run-schema-fixtures.py
```

The command must exit zero and its JSON output must equal `schema-test-report.json`.
