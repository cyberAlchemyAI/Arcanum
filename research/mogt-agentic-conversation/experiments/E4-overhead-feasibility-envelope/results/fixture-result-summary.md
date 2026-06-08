# Result Summary: `E4`

Run data: `research/mogt-agentic-conversation/development/fixtures/mogt-runtime-decision-receipts.jsonl`

Evidence class: dry-run fixture

## Integrity

| Check | Decision | Evidence |
| --- | --- | --- |
| Schema validation | pass | Validator command completed before this summary was generated. |
| Required metadata | pass | 2 row(s): fixture-e4-weighted-sum-001, fixture-e4-bargaining-guided-001. |
| Protocol deviations | pass | 0 deviation(s) recorded. |

## Metrics

| Metric | Value | Interpretation |
| --- | --- | --- |
| `overhead_acceptability_ratio` | 0.720 | Fixture mean over 2 row(s). |
| `quality_retention` | 0.830 | Fixture mean over 2 row(s). |
| `reviewer_burden` | 0.300 | Fixture mean over 2 row(s). |
| policy regimes | bargaining_guided, weighted_sum | Regimes represented in this fixture slice. |
| selected actions | single_agent_decision, safety_role_compromise | Runtime choices summarized from fixture rows. |

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
