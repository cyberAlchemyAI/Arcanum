# Evidence Harness Validation

Status: `pass-for-fixture-readiness`

Checked: `2026-07-31`

Mode: `dry-run + validate + summarize`

Evidence class: `synthetic_fixture`

## Commands And Results

### Positive Fixture

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_longmemeval_jsonl.py fixtures/passing.synthetic.jsonl
```

```text
PASS fixtures/passing.synthetic.jsonl (4 row(s), 2 question result(s))
```

### Negative Control

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_longmemeval_jsonl.py fixtures/failing.synthetic.jsonl
```

Expected result: exit `1` with 17 errors. The validator rejected:

- a forbidden claim-status update;
- malformed source hashes and revisions;
- a resolved published-run pin inside a synthetic fixture;
- non-synthetic model/provider identities;
- an unknown top-level field forbidden by the schema;
- judge/correctness disagreement;
- duplicate and non-contiguous record indices;
- non-monotonic timestamps;
- duplicate question IDs;
- manifest, category, model, and summary mismatches.

### Deterministic Summary

```bash
diff -u results/passing-fixture-summary.md \
  <(PYTHONDONTWRITEBYTECODE=1 python3 tools/summarize_longmemeval_run.py fixtures/passing.synthetic.jsonl)
```

Result: `PASS`, byte-identical output.

## Structural Checks

| Check | Result | Receipt |
| --- | --- | --- |
| Schema JSON parse | pass | Draft 2020-12 document loaded by Python JSON parser |
| Validator/summarizer syntax | pass | Both sources compiled in-memory without bytecode writes |
| Relative Markdown links | pass | 6 Markdown files, zero unresolved relative targets |
| Trailing whitespace | pass | Markdown, Python, JSON, and JSONL scope clean |
| Placeholder scan | pass | No template placeholders remain |
| Public/private boundary | pass | No private-pillar terms in the public bundle |
| Live-data separation | pass | `data/` contains zero JSONL files |
| Claim-update guard | pass | Schema fixes the field to `false`; passing fixture contains no `true` row |
| Generated cache cleanup | pass | No `__pycache__` remains |

## Fixture Metrics

| Metric | Value | Boundary |
| --- | --- | --- |
| question rows | 2 | Synthetic only |
| correct rows | 1 | Synthetic only |
| accuracy | 0.500 | Tests arithmetic, not C10 |
| categories | single-session-user, multi-session | Does not represent benchmark coverage |

## Evidence-Status Boundary

Preserved. The fixture proves evidence mechanics only. It does not update C10,
close OR1, validate Maximem Synap, reproduce LongMemEval, or authorize live
execution.

## Remaining Blockers

1. Resolve the exact harness revision used by the paper's reported run.
2. Reconcile the public 50-versus-500 question mismatch.
3. Obtain original per-question artifacts or authorize an independent run.
4. Pin exact model revisions, provider configuration, prompts, and dataset hash.
5. Admit a live task-session with credentials, cost approval, and artifact-store
   ownership.
6. Route validated live analysis to a separate claim-adjudication owner.

## Next Route

`deferred`: when the blockers have owners and live execution is authorized, use
`task-session` for one pinned run. Do not execute live experiments from this
fixture-readiness receipt.
