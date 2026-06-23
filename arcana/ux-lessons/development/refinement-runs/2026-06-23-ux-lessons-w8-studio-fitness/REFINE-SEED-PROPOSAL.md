# Refine Seed Proposal — W8: ux-pattern → studio fitness mapping

- **Run id:** 2026-06-23-ux-lessons-w8-studio-fitness · **Preset:** compact · **Research:** no-research · **Subagents:** none

## Raw operator intent
Refine W8 (taken off the deferred shelf): design how a ux-lessons `ux-pattern` maps into ui-prototyping-studio's existing UX-constraint exploit/explore fitness, naming buildable-now vs blocked-on-OQ-5/evaluator. Design only; build stays blocked.

## Target boundary
The **producer-side mapping** `ux-pattern → studio FitnessSignal/FitnessVector` — NOT the studio fitness mechanism (already specced in SPEC.md §3 "UX-constraint exploit/explore fitness `[DEFERRED]`" and `projects/ui-prototyping-studio/development/refinement-runs/20260618-ux-constraints-exploit-explore-spec/`).

## Source context (local, in-repo)
- Studio fitness model (SPEC.md:169-200): `GenerationMode{explore,exploit}`; **hard gates** = L1 a11y + L2 layout + deterministic L3 (binary, fail⇒discard); **soft gradient** = L4 cognitive/attention + laws-of-ux + subjective L3 (scored, never discards); human objective weights soft terms. Signal never gates disposal (DEC-REVERSIBILITY-NOT-GATING-026).
- Types: `FitnessSignal`, `FitnessVector(preference -1|0|1 / severity / confidence 0..1 / dimension)`, `FitnessSignalSource(human|test|risk|telemetry|governance)`.
- ux-lessons `ux-pattern.consumer_intake.validator` already pre-sorts claims into 5 authority classes (hard_gate/soft_flag/screenshot_review/human_study/not_automatable).
- Blockers: per-candidate constraint evaluator (axe/layout runner + ux-evidence-validator in the cycle) does not exist; **OQ-5** (soft-score weights + scoring functions).

## Done criteria
Dispatch validated; compact 10-stage loop; x-ray structure map of the mapping; toy_game on `detail-beside-the-subject`; RESULT with buildable-now vs blocked split + parked-plan unblock conditions.

## Write scope
This run folder only. No studio edits, no build, no commits.

## Validation surface
Mapping uses only existing studio FitnessVector fields (no invented fields); honesty rule preserved (anecdote → low confidence, never a hard gate); producer/consumer boundary preserved.

## Planned stage configuration
Compact 10-stage loop. Overlays: baseline_sequence, xray_for_hidden_structure, route_menu_for_ambiguity, toy_game_for_low_cost_falsification. No subagents.
