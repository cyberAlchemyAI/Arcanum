# Validation Contracts: Task Session Governance Runner

All witnesses are planned contracts until an implementation receipt proves them.

## Fixture families

| Witness | Fixture family | Required result |
| --- | --- | --- |
| TSGR-FIX-001 | current 25 decision-policy cases plus extracted evaluator parity | byte-stable equivalent outcome for every case |
| TSGR-FIX-002 | repeated prepare against identical synthetic repository | identical ticket material and phase digests except declared clock fields |
| TSGR-FIX-003 | missing, tied, stale, and mismatched SWU inputs | block before run-state or target write |
| TSGR-FIX-004 | baseline/staged/live digest matrix | exactly one of `apply`, `already-present-exact-output`, `conflict` |
| TSGR-FIX-005 | declared and undeclared write/output matrix | only the exact declared set passes |
| TSGR-FIX-006 | executor write-order cases | only a final terminal receipt passes |
| TSGR-FIX-007 | interruption around reconcile and atomic commit boundaries | safe resume, no partial or duplicate non-idempotent effect |
| TSGR-FIX-008 | closeout pass/no-op/block/timeout/unjoined cases | only joined `pass` or `no-op` admits terminal close |
| TSGR-FIX-009 | unique, none, and ambiguous successor cases | unique emits cursor; none records terminal; ambiguous blocks |
| TSGR-FIX-010 | repeated observation key | one accepted append plus one deduplicated no-op |
| TSGR-FIX-011 | public-boundary scan | no consumer names, private prose, absolute consumer paths, or payload bodies |

## Reused regression sets

- Task Session decision/validation policy: `25/25`.
- nearest-SWU resolution: `11/11`.
- mutation admission: `23/23`.
- Continuation Router: `6/6`.

The implementation must rerun these sets; this Design record does not substitute for
their later execution.

## End-to-end synthetic cases

Use temporary repositories with product-neutral names and bytes. Required cases:

- exact apply;
- exact output already present;
- divergent live target;
- undeclared write;
- undeclared validation output;
- missing declared output;
- acceptance-critical validation failure;
- named noncritical residue that does and does not falsify done criteria;
- hook timeout and malformed owner receipt;
- output-only re-admission pass and block;
- crash/restart at each checkpoint;
- observer deduplication.

## Experiment contract

`TSGR-EXP-001`, owned only by TSGR-010, pairs the same fixture-backed SWU governance scenario through the
current agent-led path and the runner path. Measure:

- elapsed governance time;
- number of operator/agent intervention points;
- number of repeated source reads;
- acceptance coverage and verdict;
- evidence bytes and private-output truncation.

No speed threshold is preselected. Promotion is blocked if the runner is faster but
acceptance coverage weakens or verdicts diverge.
