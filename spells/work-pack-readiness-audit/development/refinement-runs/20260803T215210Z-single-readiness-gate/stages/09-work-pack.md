# Work Pack — Single readiness gate

## Identity and objective

- Work Pack ID: `WP-SINGLE-READINESS-GATE`
- Complexity: medium
- Output mode: split
- Target owners: `spellcraft` for Work Pack Readiness Audit; `sigil-development` for Task Session
- Objective: implement the repaired contract in `stages/08-single-gate-contract.json` without changing legacy strict behavior or weakening live mutation admission.
- Current gate: `implemented-validated`
- Selected SWU: none

## Source design

- `stages/02-invoke-define.md`
- `stages/06-invoke-design.md`
- `stages/07-admission-boundary-critic.json`
- `stages/08-distill-repair.md`
- `stages/08-single-gate-contract.json`
- `stages/09-implementation-layering.md`

## SWU manifest

| SWU | Parent task | Layer | Primary behavior | Dependencies | Successor |
| --- | --- | --- | --- | --- | --- |
| `SWU-SRG-001` | `TASK-SRG-CONTRACT` | L0 | define Plan Semantic Manifest schema | none | `SWU-SRG-002` |
| `SWU-SRG-002` | `TASK-SRG-CONTRACT` | L0 | add explicit plan-then-admit config/report profile | 001 | `SWU-SRG-003` |
| `SWU-SRG-003` | `TASK-SRG-PRODUCER` | L1 | canonicalize selected semantic values and unit digests | 002 | `SWU-SRG-004` |
| `SWU-SRG-004` | `TASK-SRG-PRODUCER` | L1 | emit plan-once manifest, pending state, and selection route | 003 | `SWU-SRG-005` |
| `SWU-SRG-005` | `TASK-SRG-CONSUMER` | L2 | define selection request/receipt schemas | 004 | `SWU-SRG-006` |
| `SWU-SRG-006` | `TASK-SRG-CONSUMER` | L2 | verify current selected-unit semantic epoch | 005 | `SWU-SRG-007` |
| `SWU-SRG-007` | `TASK-SRG-CONSUMER` | L2 | bind material and admission contracts to selection identity and baselines | 006 | `SWU-SRG-008` |
| `SWU-SRG-008` | `TASK-SRG-CONSUMER` | L2 | require single-use admission receipt for mutating execution | 007 | `SWU-SRG-009` |
| `SWU-SRG-009` | `TASK-SRG-INTEGRATION` | L3 | prove cross-capability success and adversarial failures | 008 | `SWU-SRG-010` |
| `SWU-SRG-010` | `TASK-SRG-INTEGRATION` | L3 | document and sync generated runtime packages | 009 | none |

The original planning projection selected no SWU and recommended
`SWU-SRG-001`, subject to Spellcraft lifecycle admission and explicit
selection.

Implementation closeout: the behavior planned by all ten SWUs was implemented
through the consolidated owner-authorized run recorded in
`../IMPLEMENTATION-RESULT.json`; this is not a claim that ten independent Task
Session terminal receipts were issued.
No successor was auto-executed, and no runtime selection or mutation authority
is implied by this status projection.

## Waves and task contracts

- `work-pack/waves/W0-CONTRACT.md` → `work-pack/tasks/TASK-SRG-CONTRACT.md`
- `work-pack/waves/W1-PRODUCER.md` → `work-pack/tasks/TASK-SRG-PRODUCER.md`
- `work-pack/waves/W2-CONSUMER.md` → `work-pack/tasks/TASK-SRG-CONSUMER.md`
- `work-pack/waves/W3-INTEGRATION.md` → `work-pack/tasks/TASK-SRG-INTEGRATION.md`

## Global invariants

1. Existing v1 and strict v2 configurations retain their current missing-material block and Refresh route.
2. Plan-once pass means selection-ready only: selected unit null, mutation ready false.
3. Semantic identity is derived from normalized selected values, never merely from whole mutable Work Pack bytes.
4. Lifecycle/status receipts are current eligibility evidence but are outside immutable plan semantics.
5. Exactly one selection receipt binds an audited unit, current dependencies, lifecycle eligibility, and explicit confirmation.
6. Material and admission artifacts bind task, SWU, epoch, unit digest, attempt, validation, targets, baselines, owner, authority, and publication.
7. Every mutating adapter requires a current single-use admission receipt; the terminal receipt records its digest.
8. Invoke Refresh remains the closeout owner and the real semantic-plan repair owner.

## Validation strategy

- Schema: Draft 2020-12 checks and positive/negative examples.
- Unit: deterministic semantic normalization and category-specific drift codes.
- Audit: existing v1/v2 suites plus new plan-once fixtures.
- Task Session: selection, material identity, live baseline, replay, and adapter-gate fixtures.
- Integration: audit → selection → material → live admission → terminal receipt; no second audit command.
- Packaging: targeted generated-skill sync and canonical/generated parity.

## Closeout synchronization contract

Every SWU terminal receipt must bind:

- this Work Pack and its matching parent task contract;
- the exact source target inventory from the task file;
- live pre-mutation baseline digests captured by the material owner;
- validation commands and results;
- allowed delta classes: `evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`, `route_changed`;
- expected owner receipt: one schema-valid `invoke:refresh:apply-approved` closeout receipt;
- the unique successor in the SWU manifest, returned but never executed automatically.

Closeout synchronization may update this Work Pack, the parent task, and `stages/09-handoff-state.json`; it may not execute the successor, change authority, publish, or promote.

## Original blockers and disposition

- A real consumer remains mutation-blocked until its selected unit has a live,
  baseline-bound material package; this is the intended admission boundary,
  not an implementation blocker.
- The schema and normalizer work is implemented and locally validated.
- The Refine generator relative-output validation bug remains separate residue.
- Canonical sources validated before the generated mirrors were selectively
  synchronized; parity now passes.

## Next route

Implementation and generated-package parity are complete. Future consumers may
opt into `selected-unit-at-task-session`; legacy strict v2 remains the default.
Any later semantic contract change routes through Invoke Refresh and readiness
re-audit. Ordinary selection, material production, execution evidence, and
closeout-status changes use the new selection/admission route without a second
pre-execution audit.
