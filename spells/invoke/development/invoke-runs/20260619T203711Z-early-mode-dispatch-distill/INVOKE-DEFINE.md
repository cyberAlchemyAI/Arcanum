# Invoke Define Artifact

## Intent

Harden early Invoke modes so `define` and `design` benefit from the same Dispatch Spec discipline introduced for `plan`, without turning early modes into mutation-ready execution owners.

## Scope

- Target spell: `invoke`
- Target modes: `define`, `design`
- Target repository area: `arcanum/spells/invoke/`
- Generated mirror: `.agents/skills/invoke/`
- Validation surface: `arcanum/spells/invoke/development/run-validation-fixtures.sh`

## Problem Statement

The root Invoke contract now says every mode records a Dispatch Spec technique trace and that `plan`, `full`, and `validate` run automatic Distill validation before mutation-capable handoff. `define` and `design` have not yet encoded how that rule should appear at their own earlier lifecycle depth.

The missing piece is not more execution machinery. It is a small mode-specific contract:

- `define` should expose a light Dispatch trace that explains template, glossary, and next-route decisions.
- `define` should run an optional Distill sanity check only when the target definition is broad, ambiguous, or likely to split into multiple specs.
- `design` should expose a stronger Dispatch trace that explains profile/template, companion evidence, boundary, and route decisions.
- `design` should run a design-unit Distill check to prove the design stays small enough for downstream plan mode and records gaps when it does not.

## Decisions

- Keep Task Session execution authority out of `define` and `design`.
- Keep mandatory automatic Distill validation for `plan`, `full`, and `validate`; early modes get lighter checks matched to their artifact depth.
- Require output fields for Dispatch and Distill status in both `define` and `design` results so invoker examples and fixtures can validate the behavior.
- Update validation fixtures to guard the new output contract.

## Glossary

| Term | Definition |
| --- | --- |
| Early-mode Dispatch trace | A compact record of Dispatch Spec techniques used to justify mode routing, gates, and owner boundaries before plan mode. |
| Define Distill sanity check | Optional definition-scope check that reduces an overbroad or ambiguous target to one coherent spec/glossary unit. |
| Design-unit Distill check | Design-stage validation that the architecture/design bundle is still one coherent planning unit or records an explicit split/gap. |
| Mutation-capable handoff | A route to `task-session`, runtime execution, or another owner that may change source artifacts. |

## Dispatch Technique Trace

| Technique | Use |
| --- | --- |
| `sequence` | Define contract hardening feeds design hardening, then fixture validation. |
| `owner_boundary_check` | Early Invoke modes may author governed artifacts but do not own execution. |
| `artifact_contract_bridge` | Mode output fields become fixture-validation obligations. |
| `validation_loop` | Fixture runner must prove the contract after implementation. |
| `scu_swu_reduction` | The executable package is reduced to one SWU: early-mode Dispatch/Distill contract hardening. |

## Distill Validation

- Status: pass
- Smallest coherent unit: add early-mode Dispatch/Distill status to `define` and `design` contracts plus fixture validation.
- Gap found: generated mirrors must sync after canonical contract changes.
- Recomposition target: root Invoke discipline remains true across `define`, `design`, and `plan`.

## Next Route

Proceed to design, then plan, then Task Session for `TASK-IDD-001`.
