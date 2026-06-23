# Run Manifest — 2026-06-23-ux-lessons-w8-studio-fitness

Compact, design-only refine of W8 (ux-pattern → studio fitness mapping). Parent dispatch: `2026-06-23-ux-lessons`.

| # | Stage | Owner | Receipt | Status |
| - | ----- | ----- | ------- | ------ |
| — | Seed | refine | `REFINE-SEED-PROPOSAL.md` | written |
| — | Dispatch | dispatch-spec | `REFINE-DISPATCH.json` (VALIDATION=pass) | pass |
| — | Runtime handoff | refine | `RUNTIME-HANDOFF.md` | complete |
| 1 | Context baseline | context-builder | `stages/01-context.md` | pass |
| 2 | Invoke Define | invoke | `stages/02-define.md` | pass |
| 3 | Interrogation refine-review | interrogation | `stages/03-review.md` | pass |
| 4 | Research decision | refine | `stages/04-research.md` | pass (no-research) |
| 5 | Distill | distill | `stages/05-distill.md` | pass |
| 6 | Invoke Design | invoke | `stages/06-design.md` | pass |
| 7 | Interrogation design-review | interrogation | `stages/07-design-review.md` | flag (DR-1,2 repaired) |
| 8 | Distill Repair (toy_game) | distill | `stages/08-distill-repair.md` + `stages/08-toygame.md` | pass (survived) |
| 9 | Invoke Plan (parked) | invoke | `stages/09-plan.md` | pass |
| 10 | Final + Synthesis | interrogation+refine | `RESULT.md` | pass |

## Decisions
- capability_shape = **new mode `emit-studio-fitness`**; scope = **design + parked adapter spec**; ownership = **ux-lessons projects, studio owns cycle/weights/evaluator**.
- Subagents: none (compact; studio fitness already specced). dialectic/tournament not triggered.

## Key finding
The mapping **reuses the validator claim map**: hard_gate→studio hard gate (only if checkable ∧ signal≥repeated), soft_flag/screenshot_review→soft `FitnessVector` (confidence=f(signal_strength)), human_study→human objective residue. Build blocked on studio axe/layout evaluator + OQ-5.

## Evidence integrity
Every stage has an artifact; toy_game evidence present; dispatch validated before stages.
