# WORK-PACK: Guide

## Invoke Result

- Mode: full authoring package, plan slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/guide/`
- Phase status: `pass`
- Mode contract: `spells/invoke/plan.md`
- Work-pack: single-file
- Complexity: medium flag, held to low execution until dependencies pass
- Next route: `spellcraft` after dependencies

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | medium |
| outputMode | single-file for candidate package; split later if spellcraft expands |
| executionPackRef | n/a |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Objective Summary

Prepare Guide as an orchestrator only after User and Translate fixture evidence exists.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| G-S-001 | Static guide route fixture | L0 | User L0, Translate L0 | Route review |
| G-S-002 | Translate integration | L1 | G-S-001, Translate receipt schema | Receipt linkage review |
| G-S-003 | Dispatch governance | L2 | G-S-002 | Budget/gate review |
| G-S-004 | Spellcraft handoff | L3 | G-S-003 | spellcraft readiness review |

## Task Status Board

| Task ID | Goal | Layer | Gate Status | Status |
| --- | --- | --- | --- | --- |
| GUIDE-001 | Create static `/guide this architecture` route fixture. | L0 | pass | completed |
| GUIDE-002 | Add Translate call and guide receipt linkage. | L1 | pass | completed |
| GUIDE-003 | Add bounded research/subagent dispatch gates. | L2 | pass | completed |
| GUIDE-004 | Prepare spellcraft handoff. | L3 | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-GUIDE-001 | GUIDE-001 | SWU-USER-001, SWU-TRANSLATE-002 | `development/user-guide/packages/guide/` | Static route fixture exists. | Route review: no live subagent dispatch. | local-fallback |
| SWU-GUIDE-002 | GUIDE-002 | SWU-GUIDE-001, SWU-TRANSLATE-003 | `development/user-guide/packages/guide/` | Guide route references Translate receipt. | Boundary review. | local-fallback |
| SWU-GUIDE-003 | GUIDE-003 | SWU-GUIDE-002 | `development/user-guide/packages/guide/` | Dispatch budget/gates documented. | Governance review. | local-fallback |
| SWU-GUIDE-004 | GUIDE-004 | SWU-GUIDE-003 | `development/user-guide/packages/guide/` | Spellcraft handoff ready. | Handoff review. | manual |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| GUIDE-B-001 | package | User L0 fixture evidence is required. | user-ledger | resolved by `user-ledger/USER-LEDGER-SCHEMA.yml` and `user-ledger/USER-LEDGER-FIXTURE.md`. |
| GUIDE-B-002 | package | Translate L0 fixture evidence is required. | translate | resolved by `translate/TRANSLATE-SCHEMA.yml` and `translate/TRANSLATE-FIXTURES.md`. |
| GUIDE-B-003 | spellcraft | First spellcraft target must be selected: narrow `guide-architecture` or generic `guide`. | guide/spellcraft | resolved: selected `guide-architecture` first, then generalize. |

## Gate

Guide package evidence is complete through handoff. Mutation-capable spellcraft may proceed for the first target `guide-architecture`.

## Completion Evidence

| SWU ID | Evidence |
| --- | --- |
| SWU-GUIDE-001 | `GUIDE-ROUTE-SCHEMA.yml`, `GUIDE-ROUTE-FIXTURE.md`, `task-session-GUIDE-001.md` |
| SWU-GUIDE-002 | `GUIDE-TRANSLATE-INTEGRATION.md`, `task-session-GUIDE-002.md` |
| SWU-GUIDE-003 | `DISPATCH-GOVERNANCE.md`, `task-session-GUIDE-003.md` |
| SWU-GUIDE-004 | `SPELLCRAFT-HANDOFF.md`, `task-session-GUIDE-004.md` |
