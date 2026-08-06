# TASK-PEP-CLASSIFIER: Read-bounded entry classification

## SWU-PEP-002

Primary behavior: classify prerequisite state before Context Builder.

### Inputs

- validated L0 schemas;
- exact selected work-pack and task/SWU handles;
- optional typed prerequisite and satisfaction receipt.

### Outputs

- pure classifier;
- phase/read trace;
- fast-block receipt;
- classifier fixtures.

### Algorithm

1. Read the selected work pack, selected unit contract, prerequisite record, and referenced satisfaction receipt only.
2. Validate identities, scope, source digests, owner uniqueness, and fingerprint.
3. If no prerequisite exists and the entry contract is current, return `satisfied`.
4. If a current plan-once manifest owns expected material pending, return `plan-once-selection-ready`.
5. If one current prerequisite is unsatisfied, return `unmet` and the exact route/authorization tuple.
6. Return `ambiguous|stale|invalid` for all non-unique or contradictory cases.
7. Emit skipped-phase evidence for Context Builder, implementation inspection, target hashing, mutation admission, and target writes.

### Acceptance

- instrumented fixtures enforce the input-category and phase budget;
- wall time is recorded but never solely determines pass;
- no unmatched prerequisite falls through to ordinary Task Session context work.

### Validation

```bash
python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/test_classifier.py
```
