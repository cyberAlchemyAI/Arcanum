# TASK-WIR-MODES — Executable Mode Truth

Each unit owns exactly one mode and either supplies an atomic canonical producer plus validator or downgrades every public/machine status claim to the proven level.

## SWU-WIR-006
- Behavior: Define final-bundle production/status reconciliation.
- Dependencies: SWU-WIR-005.
- Write scope: Define schemas, producer, tests, status/docs, generated mirrors.
- Done/validation: exact source → spec/glossary/transport/evidence receipt atomically; identity gate consumed; invalid input leaves no outputs; status matches evidence.
- Closeout: owner `invoke-define`; expected `SWU-WIR-006-RESULT.json`; successor 007.

## SWU-WIR-007
- Behavior: Design final-bundle production/status reconciliation.
- Dependencies: SWU-WIR-006.
- Write scope: Design schemas, producer, tests, status/docs, generated mirrors.
- Done/validation: exact manifest/denominator/selection → six-view/glossary/transport bundle atomically; fixed-point and wrong-owner negatives; no partial publication.
- Closeout: owner `invoke-design`; expected `SWU-WIR-007-RESULT.json`; successor 008.

## SWU-WIR-008
- Behavior: Handoff production/status reconciliation.
- Dependencies: SWU-WIR-007.
- Write scope: Handoff schema, producer, validator, tests, templates/status, generated mirrors.
- Done/validation: exact source-session and Context Builder receipt produce one bounded handoff; whole-transcript, missing obligation, stale source, and execution-continuation coverage negatives block.
- Closeout: owner `invoke-handoff`; expected `SWU-WIR-008-RESULT.json`; successor 009.

## SWU-WIR-009
- Behavior: Refresh report/apply production/status reconciliation.
- Dependencies: SWU-WIR-008.
- Write scope: Refresh schema, producer/applicator, tests, templates/status, generated mirrors.
- Done/validation: proposal outputs or approved patch family stage and publish atomically; exact approval/material/target equality; no-op; stale receipt and partial-apply rollback negatives.
- Closeout: owner `invoke-refresh`; expected `SWU-WIR-009-RESULT.json`; successor 011.

For every unit, split analysis retains one mode because each mode has a distinct source/output contract and can pass independently. Baseline hashes are mandatory; admitted deltas are `create|update`; publication and external effects remain forbidden.
