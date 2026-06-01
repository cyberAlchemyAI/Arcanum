# Implementation Layering: Refine Runtime Stage Receipts

## Purpose

Repair native Refine runtime evidence semantics so handoff stubs cannot be counted as completed owner-stage artifacts.

## Source Evidence

| Source | Use |
| --- | --- |
| `development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/CONTRACT-AUDIT.md` | Primary blocker evidence. |
| `tools/arcanum` | Runtime orchestration implementation surface. |
| `arcana/refine/SKILL.md` | Canonical Refine contract. |
| `arcana/refine/REFINEMENT-LOOP.md` | Required run manifest, dispatch, and stage evidence rules. |
| `arcana/refine/templates/evidence-index.json` | Expected evidence shape. |

## Layer Model

| Layer | Question | Scope | Excluded | Promotion Evidence |
| --- | --- | --- | --- | --- |
| L0 | Can native Refine stop treating local-skill handoff stubs as pass? | Stage artifact classification in `tools/arcanum`. | Rewriting stage commands or adapters. | A local-skill handoff stub yields `flag` or `block`, not `pass`. |
| L1 | Can a native Refine run always materialize and validate the required dispatch contract? | `REFINE-DISPATCH.json` creation/validation before stages. | Changing Refine's ten-stage semantics. | Dispatch file exists and `validate-dispatch.py` passes before stage execution. |
| L2 | Can manifest/index evidence distinguish handoff, receipt, artifact, and blocked states? | Evidence index and run manifest schema/content. | Full telemetry redesign. | Evidence index records stage evidence kind and required artifact paths. |
| L3 | Can Craft validation rerun produce honest status and package state? | Regression run and Craft state sync. | Craft promotion. | Refine validation is pass only with real stage receipts, otherwise flag/block with exact next route. |

## Boundary Decisions

| Decision | Selected | Rationale |
| --- | --- | --- |
| Treat local-skill output as a handoff until receipt evidence exists. | yes | The adapter explicitly says it does not spawn a nested model-backed process. |
| Keep the repair inside `tools/arcanum` first. | yes | The observed misclassification is in the native root orchestration wrapper. |
| Preserve command-surface routes. | yes | `dispatch-spec` and `runtime-handoff` are now working and should not be reopened. |
| Defer Craft promotion. | yes | The issue is runtime evidence semantics, not Craft method readiness. |

## Gate Result

`pass`

Ready for work-pack execution planning.
