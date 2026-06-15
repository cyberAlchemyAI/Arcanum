# Refine Result: Craft Deterministic Row Updater

## Status

- Target: `arcana/craft`
- Status: `pass`
- Preset: `compact`
- Research: `no-research`
- Canonical mutation: not run
- Dispatch: `REFINE-DISPATCH.json`
- Runtime-backed Refine loop: executed locally through parent-owned stage artifacts.

## Refined Synthesis

Craft should create a deterministic row update planner, but not a direct row
mutator and not necessarily a public CLI in the first slice.

The planner is the safety-critical primitive hidden inside CSV writeback:

```text
ledger + schema + row selector + proposed delta + expected hash
  -> pass | flag | block
  -> deterministic patch plan or no-op/block report
```

CSV import should later call this planner for each normalized CSV row delta. The
importer should not own all reconciliation semantics itself.

## Final Decision

Create the row update planner as an internal deterministic dry-run primitive
first. Defer direct YAML apply mode, arbitrary nested edits, multi-row
transactions, and public CLI exposure until fixture evidence exists.

## First Safe SWU

`SWU-CRU-001`: add the row update planner contract and toy fixture expectations.

Write scope for that later task:

- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/README.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/fixtures/craft-row-update-planner/`

## Stage Evidence

- Context Builder evidence baseline: pass, `stages/S01-CONTEXT-BUILDER.md`
- Invoke Define: pass, `stages/S02-INVOKE-DEFINE.md`
- Interrogation refine-review: pass, `stages/S03-INTERROGATION-REFINE-REVIEW.md`
- Research decision: pass, `stages/S04-RESEARCH-DECISION.md`
- Distill: pass, `stages/S05-DISTILL.md`
- Invoke Redefine / Design: pass, `stages/S06-INVOKE-DESIGN.md`
- Interrogation refine-design-review: pass, `stages/S07-INTERROGATION-DESIGN-REVIEW.md`
- Distill Repair: pass, `stages/S08-DISTILL-REPAIR.md`
- Invoke Plan: pass, `stages/S09-INVOKE-PLAN.md`
- Final Interrogation and Synthesis: pass, `stages/S10-FINAL-INTERROGATION-SYNTHESIS.md`

## Open Residue

- Decide later whether to expose `craft-index plan-row-update` as a CLI or keep
  the planner internal.
- Direct apply mode remains blocked.
- Multi-row transactions remain blocked.
- Runtime mirror refresh remains blocked until canonical source validation
  passes in a later task.

## Recommended Next Route

Run `task-session` for `SWU-CRU-001` from `WORK-PACK.md`. Do not implement
direct YAML mutation in that route.
