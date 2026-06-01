# Task Session Context Pack: CRAFT-MVP-002

## Scope

- Work-pack: [CRAFT-MVP-WORK-PACK.md](../../CRAFT-MVP-WORK-PACK.md)
- Task: `CRAFT-MVP-002`
- Objective: represent blocker refinement and waiver behavior in [LEDGER.md](../../LEDGER.md).
- Runtime: local
- Runtime handoff: none

## Controlling Sources

| Source | Control |
| --- | --- |
| [CRAFT-MVP-WORK-PACK.md](../../CRAFT-MVP-WORK-PACK.md) | Task contract, done criteria, and validation surface. |
| [CRAFT-LEDGER-SCHEMA.yml](../../CRAFT-LEDGER-SCHEMA.yml) | `typed_items`, `decisions`, validation rules `VAL-006` and `VAL-007`, and blocker lifecycle constraints. |
| [LEDGER.md](../../LEDGER.md) | Current ledger fixture to update. |
| [CRAFT-MVP-DESIGN.md](../../CRAFT-MVP-DESIGN.md) | Decision flow for blocker resolution and waiver behavior. |

## Write Scope

Allowed:

- update `development/craft/LEDGER.md`,
- update `development/craft/CRAFT-MVP-WORK-PACK.md` for task status evidence,
- write this task-session evidence folder.

Not allowed:

- generated index creation,
- scoring or role delegation automation,
- runtime/refine interface mutation,
- package README/session sync, which remains for `CRAFT-MVP-004`.

## Gate Checks

| Gate | Result | Evidence |
| --- | --- | --- |
| Exactly one task selected | pass | User selected `CRAFT-MVP-002`. |
| Previous fixture exists | pass | `LEDGER.md` exists from `CRAFT-MVP-001`. |
| Required YAML lifecycle fields exist | pass | `CRAFT-LEDGER-SCHEMA.yml` defines `refinement_status`, `decision_ref`, and waiver decision rows. |
| Write scope clear | pass | Ledger plus task evidence and work-pack status only. |
| Runtime delegation required | n/a | Local execution is sufficient. |
| Blocker ambiguity | pass | Waiver can be represented with optional `decision_ref`; no schema refine required. |

## Decision Pack

| Decision | Selected | Rationale |
| --- | --- | --- |
| Add lifecycle examples as separate blocker rows or mutate existing rows only. | Add separate rows and close the existing trace blocker. | Separate rows make raw, typed, refined, resolved, and waived states independently reviewable without erasing prior fixture history. |

## Execution Obligations

1. Add at least one raw or typed blocker that is not resolved.
2. Add at least one refined blocker with `status = resolution_proposed`.
3. Add at least one resolved blocker with closure evidence.
4. Add at least one waived blocker linked to a waiver decision row.
5. Ensure `blocker_refiner` is primary only while clarification is still active.
6. Preserve validator/auditor evidence requirements before closure.

## Validation Surface

Manual and scripted review against:

- `VAL-006`: every blocker includes `refinement_status` and `closure_condition`.
- `VAL-007`: a blocker with status `resolved` has refinement evidence or a linked waiver decision.
- no blocker with `refinement_status = raw` has `status = resolved`.
- waived blockers have `decision_ref` pointing at a decision row with `decision_type = waiver`.
