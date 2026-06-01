# WORK-PACK: Translate

## Invoke Result

- Mode: full authoring package, plan slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/translate/`
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

Create the first candidate `translate` schema and fixture package.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| T-S-001 | Translate schema | L0 | User handles understood | YAML parse |
| T-S-002 | Translation fixture corpus | L0 | T-S-001 | Four fixture reviews |
| T-S-003 | Receipt schema | L1 | T-S-002 | User-ledger compatibility review |
| T-S-004 | Guide-call contract | L2 | T-S-003 | Boundary review |

## Task Status Board

| Task ID | Goal | Layer | Gate Status | Status |
| --- | --- | --- | --- | --- |
| TRANSLATE-001 | Create `TRANSLATE-SCHEMA.yml`. | L0 | pass | completed |
| TRANSLATE-002 | Create fixture corpus with three positive translations and one failed analogy. | L0 | pass | completed |
| TRANSLATE-003 | Create `TRANSLATE-RECEIPT-SCHEMA.yml`. | L1 | pass | completed |
| TRANSLATE-004 | Define Guide-call contract and research-needed flag. | L2 | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-TRANSLATE-001 | TRANSLATE-001 | none | `development/user-guide/packages/translate/` | Schema captures request, term map, bridge map, limits, target definition. | YAML parse and field checklist. | local-fallback |
| SWU-TRANSLATE-002 | TRANSLATE-002 | SWU-TRANSLATE-001 | `development/user-guide/packages/translate/` | Fixture corpus covers all four examples. | Manual fixture checklist. | local-fallback |
| SWU-TRANSLATE-003 | TRANSLATE-003 | SWU-TRANSLATE-002 | `development/user-guide/packages/translate/` | Receipt schema includes ledger update proposal and user handle refs. | Compatibility review against user-ledger package. | local-fallback |
| SWU-TRANSLATE-004 | TRANSLATE-004 | SWU-TRANSLATE-003 | `development/user-guide/packages/translate/` | Guide-call contract exists. | Boundary review: Guide calls Translate; Translate does not research. | local-fallback |

## Blockers

Translate runtime implementation waits for at least fixture validation through L0.

## Completion Evidence

| SWU ID | Evidence |
| --- | --- |
| SWU-TRANSLATE-001 | `TRANSLATE-SCHEMA.yml`, `task-session-TRANSLATE-001.md` |
| SWU-TRANSLATE-002 | `TRANSLATE-FIXTURES.md`, `task-session-TRANSLATE-002.md` |
| SWU-TRANSLATE-003 | `TRANSLATE-RECEIPT-SCHEMA.yml`, `task-session-TRANSLATE-003.md` |
| SWU-TRANSLATE-004 | `GUIDE-CALL-CONTRACT.md`, `task-session-TRANSLATE-004.md` |
