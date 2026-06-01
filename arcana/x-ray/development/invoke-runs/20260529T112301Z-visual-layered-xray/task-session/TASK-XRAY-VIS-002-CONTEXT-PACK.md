# Task Session Context Pack: SWU-XRAY-VIS-002

## Scope

Execute `SWU-XRAY-VIS-002` from `WORK-PACK.md`.

## Selected Task

- Task: `TASK-XRAY-VIS-002`
- SWU: `SWU-XRAY-VIS-002`
- Objective: add a static layered HTML/SVG example package for the revised `x-ray` contract.

## Controlling Sources

- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- `arcana/x-ray/examples/context-to-html-shape.md`

## Write Scope

- `arcana/x-ray/examples/visual-layered-order-ingestion-source.md`
- `arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json`
- `arcana/x-ray/examples/visual-layered-order-ingestion.html`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/task-session/TASK-XRAY-VIS-002-RESULT.md`

## Hard Constraints

- Keep `x-ray` status as seed.
- Do not require remote rendering.
- Use L0 static HTML/CSS/SVG only.
- Mark evidence-backed facts and inference explicitly.
- Do not implement a reusable renderer yet.

## Gate Verdict

pass

Dependencies are satisfied by completed `SWU-XRAY-VIS-001`. The selected write scope is bounded and does not overlap with future validator code.

