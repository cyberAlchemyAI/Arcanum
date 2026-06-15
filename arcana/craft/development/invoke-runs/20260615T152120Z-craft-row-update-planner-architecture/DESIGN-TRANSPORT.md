# Design Transport: Craft Row Update Planner Architecture

## Transport Summary

Invoke design produced a proposal architecture bundle for the Craft row update
planner. It converts the Refine recommendation into a six-view architecture
artifact with glossary consistency and an implementation-layering seed.

## Mode Evidence

| Phase | Evidence | Verdict |
| --- | --- | --- |
| Context Builder | Source refs from row-updater Refine result and Craft schema/docs. | pass |
| Structured Interview | No blocker ambiguity; proposal scope already confirmed by operator. | pass |
| Inventory | Module Formulae architecture-bundle template selected. | pass |
| Invoke Design | `INVOKE-DESIGN-ARCHITECTURE.md` with six required views. | pass |

## Source Contracts

- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/RESULT.md`
- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/stages/S06-INVOKE-DESIGN.md`
- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/stages/S08-DISTILL-REPAIR.md`
- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/WORK-PACK.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/templates/ledger.schema.yml`

## Boundary

This Invoke run is non-mutating. It did not edit Craft canonical source,
scripts, generated mirrors, publication state, or parent gitlinks.

## Next Route

Use `task-session` for `SWU-CRU-001` if the architecture is accepted for
execution. Use `invoke plan` only if the row-updater plan needs to be regenerated
from this architecture bundle rather than using the existing work-pack.
