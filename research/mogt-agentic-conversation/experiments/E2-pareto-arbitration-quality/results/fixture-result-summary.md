# Result Summary: `E2`

Run data: `research/mogt-agentic-conversation/development/fixtures/mogt-runtime-decision-receipts.jsonl`

Evidence class: dry-run fixture

## Integrity

| Check | Decision | Evidence |
| --- | --- | --- |
| Schema validation | pass | Validator command completed before this summary was generated. |
| Required metadata | pass | 1 row(s): fixture-e2-pareto-guided-001. |
| Protocol deviations | pass | 0 deviation(s) recorded. |

## Metrics

| Metric | Value | Interpretation |
| --- | --- | --- |
| `decision_quality_score` | 0.880 | Fixture mean over 1 row(s). |
| `regret_or_proxy` | 0.030 | Fixture mean over 1 row(s). |
| policy regimes | pareto_guided | Regimes represented in this fixture slice. |
| selected actions | ask_clarifying_question | Runtime choices summarized from fixture rows. |

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
