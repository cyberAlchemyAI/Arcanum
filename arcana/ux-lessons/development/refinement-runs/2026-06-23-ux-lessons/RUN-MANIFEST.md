# Run Manifest — 2026-06-23-ux-lessons

Refine run for the new capability `ux-lessons`. Refine owns this folder, the seed, dispatch request, runtime handoff, research decision, evidence index, and final synthesis. Stage capabilities own their artifacts (referenced, not copied).

| # | Stage | Owner | Receipt | Status |
| - | ----- | ----- | ------- | ------ |
| — | Seed proposal | refine | `REFINE-SEED-PROPOSAL.md` | written |
| — | Dispatch (validated) | dispatch-spec | `REFINE-DISPATCH.json` (VALIDATION=pass) | pass |
| — | Runtime handoff | refine | `RUNTIME-HANDOFF.md` | complete |
| 1 | Context baseline | context-builder | `stages/01-context-baseline.md` | pass |
| 2 | Invoke Define | invoke | `stages/02-define.md` | pass |
| 3 | Interrogation refine-review | interrogation | `stages/03-review.md` (+2 subagent receipts) | pass |
| 4 | Research decision | refine | `stages/04-research-decision.md` | pass (no-research) |
| 5 | Distill | distill | `stages/05-distill.md` | pass |
| 6 | Invoke Design | invoke | `stages/06-design.md` | pass |
| 7 | Interrogation design-review | interrogation | `stages/07-design-review.md` | flag (DR-1..3, non-blocking) |
| 8 | Distill Repair (toy_game) | distill | `stages/08-distill-repair.md` + `stages/08-toygame-xray-session.md` | pass (survived) |
| 9 | Invoke Plan | invoke | `stages/09-plan.md` | pass |
| 10 | Final + Synthesis | interrogation+refine | `RESULT.md` | pass |

## Subagent receipts
- `stages/receipt-precedent-boundary-auditor.md` — Role A (minimize-new-surface). Verdict: build-from-owned; biggest risk = duplicate store.
- `stages/receipt-reuse-architect.md` — Role B (maximize-reuse-richness). Schemas + worked example `detail-beside-the-subject`.
- Anti-bias axis: minimize-new-surface ⇄ maximize-reuse-richness. Join: parent_synthesis.

## Decisions
- capability_shape = **thin sigil**; pattern_store_location = **arcanum public** (borrow architecture-pattern-inventory card shape).
- Overlays triggered: baseline_sequence, xray, route_menu, memory_residue, toy_game. Not triggered: tournament, dialectic (recorded).

## Evidence integrity
Every stage has an artifact path; no stage marked `pass` without an existing artifact. toy_game evidence artifact present.
