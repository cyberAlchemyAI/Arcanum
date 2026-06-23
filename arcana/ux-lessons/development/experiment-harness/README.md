# ux-lessons — Experiment Harness

Reusable-behavior evidence for the `ux-lessons` sigil. Each example is a **hand-run** of one mode with a **real output body** (the actual produced artifact), not a save-summary.

These examples are distinct from the design-time `toy_game` (in `../refinement-runs/2026-06-23-ux-lessons/stages/08-toygame-xray-session.md`): the toy_game proved the *design* was not falsified; this harness proves the *sigil contract* produces conformant artifacts across complexity levels.

## Fixture
The 2026-06-23 x-ray HTML iteration session (`refine-skill-xray.html`) — the only real captured session available. It yielded three real moves:
- **M1** — added a 3D isometric tilt; reverted (illegible); re-added a gentler tilt; reverted again on request. (*recurred within the session*)
- **M2** — moved per-layer detail from a drill panel below the stack to a sticky right-rail beside it.
- **M3** — added an optional guided "build the stack" tour.

## Examples
| # | Complexity | Mode(s) | Output body | Status |
| - | ---------- | ------- | ----------- | ------ |
| 01 | low | `capture` | `examples/01-capture-low.md` — one `lesson` (anecdote) from M3 | pass |
| 02 | medium | `distill` + `emit-validator` | `examples/02-distill-emit-validator-medium.md` — `detail-beside-the-subject` pattern (seed) + validator claim map | pass |
| 03 | complex | `capture` + `promote` + `emit-studio` | `examples/03-promote-emit-studio-complex.md` — M1 lesson, anecdote→repeated (within-session), studio intent | flag |

## How to run (native)
There is no Codex executor for this sigil — it is native (Read/Write). To re-run an example: follow the `<process>` steps in `../../SKILL.md` for the named mode against the fixture, then diff the produced artifact against the example's output body and the schema in SKILL.md.

## Validation
See `VALIDATION-REPORT.md` for per-example conformance against the `lesson`/`ux-pattern` schemas, the evidence enum, the anecdote→no-hard-gate honesty rule, and the no-invented-consumer-fields guard.

## Honest limits
- Only one real session exists, so **true cross-session promotion (`repeated → cross_session`) is NOT demonstrated** — example 03 uses within-session recurrence as a proxy and flags this.
- Live consumer ingestion is **not** exercised here: example 02's validator claim map is a `spec`-stage handoff (not a calibrated gate); example 03's studio intent is shape-validated against the SPEC, not applied to a live studio session.
