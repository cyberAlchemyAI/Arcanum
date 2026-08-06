# TASK-SRG-CONTRACT — Versioned semantic contract

## Smallest Working Units

### SWU-SRG-001 — Plan Semantic Manifest schema

- Primary behavior: define one fail-closed schema for a non-authoritative semantic plan epoch.
- Dependencies: none.
- Write scope: new canonical manifest schema and its positive/negative fixture documents under `arcanum/spells/work-pack-readiness-audit/`.
- Done: schema requires component/unit digests, ready frontier, selection-required, runtime-pending, zero authority, and zero mutation readiness; rejects material/admission authority.
- Split analysis: constants and digest structure must validate together to give the manifest one coherent identity; configuration activation remains SWU-002.
- Verification: Draft 2020-12 schema check plus positive and negative fixture validation.
- Owner: Spellcraft lifecycle worker; local fallback permitted only under the same write scope.
- Result: structured receipt with touched paths, schema checks, blockers, and no promotion claim.

### SWU-SRG-002 — Opt-in profile schemas

- Primary behavior: add explicit `selected-unit-at-task-session` activation and pending-selection report semantics while preserving strict defaults.
- Dependencies: SWU-SRG-001.
- Write scope: `audit-config-v2.schema.json`, `audit-report-v2.schema.json`, selection-handoff schema, and schema fixtures.
- Done: existing configs remain valid; new profile cannot emit `mutation_ready=true`; defect and pending routes are distinct.
- Split analysis: config activation, report state, and handoff route are one versioned external contract; runner behavior remains SWU-004.
- Verification: legacy/new schema fixture matrix.
- Owner: Spellcraft lifecycle worker.

## Closeout

Terminal receipts synchronize this task, `stages/09-work-pack.md`, and `stages/09-handoff-state.json` through the exact closeout contract in the Work Pack. Unique successors: 001→002→003.
