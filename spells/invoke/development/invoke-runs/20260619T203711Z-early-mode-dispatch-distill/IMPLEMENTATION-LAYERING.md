# Implementation Layering

## Layer Map

| Layer | Scope | Decision |
| --- | --- | --- |
| L0 Contract | Canonical `define.md` and `design.md` mode contracts. | Add Dispatch/Distill obligations and output fields. |
| L1 Validation | Fixture runner and expected outputs. | Check early-mode fields in standalone and integration fixtures. |
| L2 Runtime Surface | Generated `.agents/skills/invoke/` mirrors. | Sync after canonical edits. |
| L3 Experiment Evidence | Invoke development package and Task Session result. | Preserve implementation receipt and validation evidence. |

## Cross-Layer Rules

- Canonical files are patched before generated mirrors.
- Fixture validation proves the public contract before claiming completion.
- Early modes do not gain execution authority.
- Plan mode remains the mutation-handoff gate for mandatory automatic Distill validation.

## Validation Strategy

- `bash -n arcanum/spells/invoke/development/run-validation-fixtures.sh`
- `arcanum/spells/invoke/development/run-validation-fixtures.sh`
- `git diff --check` scoped to touched surfaces

## Dispatch Technique Trace

- `sequence`: canonical contract -> generated mirror -> fixture validation.
- `state_namespace_boundary`: development package stays under `development/invoke-runs/`; canonical contract changes stay under `spells/invoke/`.
- `validation_loop`: validation report is required evidence.

## Distill Validation

- Status: pass
- Smallest implementation layer: L0 contract and L1 validation together.
- Rationale: contract-only changes would be easy to drift; validation-only changes would lack owner semantics.
