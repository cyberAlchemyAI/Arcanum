# Result Summary: `E1`

Run data: `research/mogt-agentic-conversation/development/fixtures/mogt-runtime-decision-receipts.jsonl`

Evidence class: dry-run fixture

## Integrity

| Check | Decision | Evidence |
| --- | --- | --- |
| Schema validation | pass | Validator command completed before this summary was generated. |
| Required metadata | pass | 1 row(s): fixture-e1-heuristic-001. |
| Protocol deviations | pass | 0 deviation(s) recorded. |

## Metrics

| Metric | Value | Interpretation |
| --- | --- | --- |
| `traceability_coverage` | 0.760 | Fixture mean over 1 row(s). |
| `acceptance_score` | 0.740 | Fixture mean over 1 row(s). |
| policy regimes | heuristic | Regimes represented in this fixture slice. |
| selected actions | answer_with_current_context | Runtime choices summarized from fixture rows. |

## Success Criteria

| Criteria ID | Target | Decision | Notes |
| --- | --- | --- | --- |
| fixture-validation | Rows validate locally before summary generation | fixture-ready | Evidence classes: synthetic_fixture. |
| evidence-boundary | Do not claim live experiment support | pass | Summary is explicitly fixture-only. |

## Claim Impact

Claim status update allowed: no

Recommendation: Do not update publication claims or evidence status. Use this as dry-run fixture readiness evidence only.

## Next Step

1. Run the S4 fixture validation report gate after SWU-MOGT-HARNESS-002, 003, and 004 result files exist.
