# Task Session Context Pack: SWU-XRAY-VIS-005

## Scope

Execute `SWU-XRAY-VIS-005` from `WORK-PACK.md`.

## Selected Task

- Task: `TASK-XRAY-VIS-005`
- SWU: `SWU-XRAY-VIS-005`
- Objective: add a documentation-first visual component library and user-extension nudge for `x-ray`.

## Controlling Sources

- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/RESULT.md`
- `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/stages/06-design.md`
- `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/stages/08-repair.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`

## Write Scope

- `arcana/x-ray/library/README.md`
- `arcana/x-ray/library/components.md`
- `arcana/x-ray/library/patterns.md`
- `arcana/x-ray/library/user-shapes-template.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/task-session/TASK-XRAY-VIS-005-RESULT.md`

## Hard Constraints

- Add a small starter library only; do not build a renderer engine.
- Preserve `x-ray` seed status.
- Preserve the evidence/inference boundary for every reusable visual.
- Include the required starter shapes, connectors, charts, and patterns.
- Nudge the user to add custom shapes, charts, or patterns without making custom visuals mandatory.
- Do not add schemas in this SWU; schemas are sequenced behind the completed library.

## Decision Pack

- Component form: documentation-first Markdown entries with pseudo-markup sketches. Selected because it supports future schema work without prematurely freezing a renderer.
- User nudge location: both process/output contract and README. Selected because execution behavior and package discovery both need the extension prompt.

## Gate Verdict

pass

Dependencies are satisfied by completed `SWU-XRAY-VIS-004`; the selected write scope is documentation and synchronization only.
