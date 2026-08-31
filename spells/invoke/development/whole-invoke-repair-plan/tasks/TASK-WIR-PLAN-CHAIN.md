# TASK-WIR-PLAN-CHAIN — Source to Owner-Decision Closure

## SWU-WIR-003

- Primary behavior: atomic complete Plan package compilation from one versioned machine source.
- Split analysis: schema and compiler must change together because output atomicity is the acceptance boundary; consumers remain separate.
- Dependencies: SWU-WIR-002.
- Write scope: Plan source schema/compiler/tests/docs and generated mirrors.
- Done: complete split package, execution projection, audit config, deterministic human views, and producer receipt publish together only after two WPRA PASS rehearsals.
- Validation: invalid-source/no-output, second-run-block/no-output, stale route/write/effect, future-create-output, and exact-byte determinism tests.
- Closeout sync: owner `invoke-plan`; expected `SWU-WIR-003-RESULT.json`; successor SWU-WIR-004.

## SWU-WIR-004

- Primary behavior: real no-effect consumer transformations replace adapters and schema-only substitutes.
- Split analysis: all named consumer boundaries join one closure receipt; request family remains separately versioned.
- Dependencies: SWU-WIR-003.
- Write scope: consumer rehearsal adapters, production transformation entrypoints, schemas, tests.
- Done: WPRA, readiness, Task Session entry/admission/governance, precloseout, owner closeout, terminal, and continuity execute their installed transformations twice deterministically.
- Validation: substitution detection, missing consumer, changed runner identity, partial topology, and false-PASS negatives.
- Closeout sync: owner `invoke-preacceptance`; expected `SWU-WIR-004-RESULT.json`; successor SWU-WIR-005.

## SWU-WIR-005

- Primary behavior: one canonical owner request/response family end to end.
- Split analysis: producer, validators, and bridge compatibility are inseparable for one round-trip contract.
- Dependencies: SWU-WIR-004.
- Write scope: request/response schemas, producer, response validator, bridge, compatibility fixtures/tests.
- Done: one selected writer family; historical readers remain; stale effect/authority/review/graph bindings block.
- Validation: canonical emit/validate/re-emit round trip and cross-version mismatch denominator.
- Closeout sync: owner `invoke-owner-decision`; expected `SWU-WIR-005-RESULT.json`; successor SWU-WIR-006.
