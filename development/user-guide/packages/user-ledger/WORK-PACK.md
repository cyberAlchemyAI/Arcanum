# WORK-PACK: User Ledger

## Invoke Result

- Mode: full authoring package, plan slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/user-ledger/`
- Phase status: `pass`
- Mode contract: `spells/invoke/plan.md`
- Work-pack: single-file
- Complexity: low
- Next route: `sigil-development`

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | low |
| outputMode | single-file |
| executionPackRef | n/a |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Objective Summary

Create the first candidate `user-ledger` schema and fixture package.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| U-S-001 | Schema and fixture baseline | L0 | Define/design package | YAML parse and fixture review |
| U-S-002 | Receipt update rules | L1 | U-S-001 | clarified vs mastered fixture |
| U-S-003 | Visibility policy | L2 | U-S-002 | promotion split review |

## Task Status Board

| Task ID | Goal | Layer | Gate Status | Status |
| --- | --- | --- | --- | --- |
| USER-001 | Create `USER-LEDGER-SCHEMA.yml` and `USER-LEDGER-FIXTURE.md`. | L0 | pass | completed |
| USER-002 | Add receipt update rules and mastery evidence fixtures. | L1 | pass | completed |
| USER-003 | Add visibility policy and promotion boundary validation. | L2 | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-USER-001 | USER-001 | none | `development/user-guide/packages/user-ledger/` | Schema and fixture exist with minimum row families. | YAML parse plus manual fixture checklist. | local-fallback |
| SWU-USER-002 | USER-002 | SWU-USER-001 | `development/user-guide/packages/user-ledger/` | Mastery update rules and fixtures exist. | Passive confirmation cannot produce mastered. | local-fallback |
| SWU-USER-003 | USER-003 | SWU-USER-002 | `development/user-guide/packages/user-ledger/` | Visibility and promotion boundary are documented. | Canonical promotion blocked without owner review. | local-fallback |

## Blockers

None for L0. Runtime storage remains deferred.

## Completion Evidence

| SWU ID | Evidence |
| --- | --- |
| SWU-USER-001 | `USER-LEDGER-SCHEMA.yml`, `USER-LEDGER-FIXTURE.md`, `task-session-USER-001.md` |
| SWU-USER-002 | `RECEIPT-UPDATE-RULES.md`, `MASTERY-FIXTURES.md`, `task-session-USER-002.md` |
| SWU-USER-003 | `VISIBILITY-POLICY.md`, `PROMOTION-BOUNDARY-VALIDATION.md`, `task-session-USER-003.md` |
