# Invoke Plan Transport: Necronomicon

## Source

- Observed capability: `invoke`
- Invoke mode: `plan`
- Target artifact: `necronomicon`
- Target owner: Necronomicon spell development cycle

## Outputs

- Implementation plan: `spells/necronomicon/development/IMPLEMENTATION-PLAN.md`
- Implementation layering: `spells/necronomicon/development/IMPLEMENTATION-LAYERING.md`
- Work-pack: `spells/necronomicon/development/WORK-PACK.md`

## Transport Summary

The Necronomicon restart has been planned around a substrate-first implementation path. L0 proves inventory retrieval, authority classification, gap recording, and owner-correct handoff. Bootstrap and route configuration move to L1 after L0 evidence exists.

## Target Artifact Gaps

| Gap | Owner | Next Route |
| --- | --- | --- |
| Canonical README still needs substrate-first synchronization. | Necronomicon | task-session |
| L0 schema examples and fixtures are not yet written. | Necronomicon | task-session |
| Bootstrap-generated adapter instructions remain route/bootstrap-first until updated. | Necronomicon | task-session after contract sync |

## Invoke Gaps

No invoke-specific blocker found. The plan is usable as a target development handoff.

## Recommended Next Route

`task-session` for `SWU-NEO-001` and `SWU-NEO-002`.
