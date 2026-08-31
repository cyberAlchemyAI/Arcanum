# Define Intent Coverage Fixture Summary

- Result: `pass`
- Matrix digest: `cb89a771d0dc65760ec06372d9a55847cf123b731a996b14b7f345df1d82fc9b`
- Cases: 13
- Deterministic two-run cases: 13
- Incident identities checked: 9
- Frozen v1 contract identities checked: 3
- Failures: 0

| Case | Expected | Observed | Deterministic | Codes |
| --- | --- | --- | --- | --- |
| PASS-MIXED-THREE | pass | pass | true | - |
| PASS-CEL-COMPLETE | pass | pass | true | - |
| BLOCK-CEL-MISSING-INVARIANT | block | block | true | MISSING_BOUNDARY, MISSING_CONCEPT |
| BLOCK-PLAN-FOUR-TERM-SHELL | block | block | true | MISSING_BOUNDARY, MISSING_CONCEPT, MISSING_RELATIONSHIP |
| BLOCK-PLAN-HISTORICAL-DISCARD | block | block | true | HISTORICAL_SEMANTICS_DISCARDED |
| BLOCK-UNASSESSED-FACET | block | block | true | FACET_UNASSESSED |
| BLOCK-UNCOVERED-OBLIGATION | block | block | true | OBLIGATION_UNCOVERED |
| BLOCK-ORPHAN-PROBE | block | block | true | ORPHAN_PROBE |
| BLOCK-EMPTY-CIRCULAR-CONSUMERS | block | block | true | EMPTY_CIRCULAR_CONSUMER_DENOMINATOR |
| BLOCK-MISSING-REQUIRED-RELATIONSHIP | block | block | true | MISSING_RELATIONSHIP |
| PASS-PLAN-EXPANDED-18 | pass | pass | true | - |
| BLOCK-POST-CLOSURE-DEFINITION-REMOVAL | block | block | true | ADMISSION_CLOSURE_DRIFT, MISSING_BOUNDARY, MISSING_CONCEPT, MISSING_RELATIONSHIP |
| BLOCK-POST-CLOSURE-RELATION-REMOVAL | block | block | true | ADMISSION_CLOSURE_DRIFT, MISSING_RELATIONSHIP |
