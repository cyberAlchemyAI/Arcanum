# Result Summary: `ACM-OR1-LME-REPRO`

Run data: `fixtures/passing.synthetic.jsonl`

Evidence class: `synthetic_fixture`

## Integrity

| Check | Decision | Evidence |
| --- | --- | --- |
| Schema and cross-row validation | pass | 4 contiguous rows validated. |
| Required metadata | pass | Run `fixture-or1-pass-001` has one manifest and one summary. |
| Protocol deviations | pass | 0 deviation(s) recorded. |
| Append-only shape | pass | One run, contiguous indices, unique question IDs, summary last. |

## Metrics

| Metric | Value | Interpretation |
| --- | --- | --- |
| question count | 2 | Validated question-result rows. |
| correct count | 1 | Rows whose binary judge verdict is `CORRECT`. |
| overall accuracy | 0.500 | Fixture arithmetic only. |
| `single-session-user` | 1/1 (1.000) | Category fixture slice. |
| `multi-session` | 0/1 (0.000) | Category fixture slice. |

## Success Criteria

| Criteria ID | Target | Decision | Notes |
| --- | --- | --- | --- |
| fixture-positive | Passing fixture validates | pass | Schema, metadata, sequence, and metrics accepted. |
| evidence-boundary | Raw or fixture evidence cannot update claim status | pass | Every row has `claim_status_update_allowed=false`. |
| live-adjudication | 500 official questions plus resolved published-run pin | blocked | Synthetic fixture intentionally does not satisfy live requirements. |

## Claim Impact

Claim status update allowed: no

Recommendation: Do not update C10 or the tower's evidence status. Use this summary only as dry-run fixture-readiness evidence.

## Remaining Blockers

- exact published-run harness revision;
- reconciliation of the public 50-versus-500 question mismatch;
- original or independently generated per-question artifacts;
- live credentials, cost authorization, and an admitted execution unit.

## Next Step

1. Defer live execution until an approved task-session owns the pinned protocol, credentials, cost, and raw-artifact capture.
