# Experiment Harness State — ux-lessons

- **Status:** `flag` (initialized; 3 conformance-passing examples authored; promotion still blocked on real cross-session + live-consumer evidence).
- **Owner:** `experiment-harness`. Harness lives in `experiment-harness/` (README + examples + VALIDATION-REPORT).

## What is done
The harness is initialized with three real-output-body examples — see `experiment-harness/`:
| # | Complexity | Modes | Verdict |
| - | ---------- | ----- | ------- |
| 01 | low | `capture` (M3 guided tour → lesson, anecdote) | pass |
| 02 | medium | `distill` + `emit-validator` (`detail-beside-the-subject` + claim map) | pass |
| 03 | complex | `capture` + `promote` + `emit-studio` (M1 3D-revert, within-session `repeated`) | flag |

Validation: `experiment-harness/VALIDATION-REPORT.md`. Two pass, one flag; all conform to the schemas, evidence enum, and honesty rule.

## Why promotion is STILL blocked (named)
- **Only one real session exists** → true cross-session promotion (`repeated → cross_session`) is not provable; example 03 uses within-session recurrence as an honest proxy.
- **Live consumer ingestion not exercised** → example 02's validator claim map is a `--mode spec` handoff (not calibrated); example 03's studio intent is shape-validated, not applied.

## Unblock condition (for promotion)
Capture a **second real iteration session**, demonstrate `repeated → cross_session` promotion, and run live consumer ingestion (ux-evidence-validator `fixture-plan`→`calibrate`; ui-prototyping-studio annotation apply). Then re-run this harness and re-check `<promotion-gate>` in SKILL.md.

## Founding fixture (design-time, not harness evidence)
`refinement-runs/2026-06-23-ux-lessons/stages/08-toygame-xray-session.md` — toy_game survived. Design-time falsification, distinct from the harness above.

## Deferred (named) downstream blocks
- ui-prototyping-studio **variant/fitness** intake: blocked on studio **OQ-5** + an axe-core/layout-overflow fitness evaluator.

## Deferred (named) downstream blocks
- ui-prototyping-studio **variant/fitness** intake: blocked on studio **OQ-5** + an axe-core/layout-overflow fitness evaluator.
