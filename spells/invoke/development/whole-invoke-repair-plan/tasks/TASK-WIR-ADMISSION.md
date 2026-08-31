# TASK-WIR-ADMISSION — Trust and Regression Baseline

## SWU-WIR-001

- Primary behavior: mode-specific producer-owned evidence admission.
- Split analysis: schema, resolver, and tests form one independently reviewable trust boundary; preacceptance repair is separate.
- Dependencies: none.
- Write scope: capability status schema, resolver, mode table, focused tests, generated Invoke mirrors.
- Source anchors: INV-AUDIT-001 and 007 evidence paths.
- Done: self-issued, missing, stale, wrong-owner, wrong-mode, incomplete-evidence, and generic-receipt bypasses block; historical reads remain supported.
- Validation: focused resolver tests plus mode-specific negative matrix and generated parity.
- Closeout sync: exact canonical/generated inventory; baseline hashes; admitted deltas `create|update`; owner `invoke`; expected result `SWU-WIR-001-RESULT.json`; successor SWU-WIR-002 only on PASS.

## SWU-WIR-002

- Primary behavior: canonical `joined_driver_digest` fixture production and regression.
- Split analysis: fixture producer/schema/test alignment is one narrow regression boundary.
- Dependencies: SWU-WIR-001.
- Write scope: preacceptance fixture builders and tests only; schema changes only if evidence proves mismatch.
- Done: all preacceptance closure tests construct the required digest and the full suite is green.
- Validation: canonical preacceptance aggregate and missing/stale/wrong digest negatives.
- Closeout sync: exact test/fixture inventory; owner `invoke-preacceptance`; expected result `SWU-WIR-002-RESULT.json`; successor SWU-WIR-003 only on PASS.

Expected result shape follows `.agents/skills/invoke/plan.md` and includes files, commands/results, blockers, residue, and reroute.
