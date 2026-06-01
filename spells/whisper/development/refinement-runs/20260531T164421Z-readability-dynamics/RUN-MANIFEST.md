# Refine Run Manifest

Run ID: `20260531T164421Z-readability-dynamics`

Target: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html`

Status: `flag`

Preset: `full`

Research mode: `bounded-research`

## Objective

Refine the Whisper drafting and review model so paragraph walls are no longer treated as a styling problem only. The refinement asks whether Whisper needs a governed readability/rhythm layer between `draft_artifact` and `review_html`, how this relates to academic writing and reading research, whether the repository already has a compatible substrate, and what the next executable integration path should be.

## Current Finding

Whisper already has:

- `composition_parts` for part-level delegation and validation.
- `pareto_tournament` for global and part-triggered candidate selection.
- `review_html` for stable browser comments and Playwright payload extraction.
- `validate-whisper-draft.py` for opening contract, Pareto completeness, length, and basic substrate checks.

Whisper does not yet have:

- A readability dynamics schema.
- Beat-level rendering for review HTML.
- Validator checks for paragraph density, sentence rhythm, abstraction load, scan path, or discourse-move coverage.
- An academic grounding note connecting Whisper's writing controls to discourse structure, cohesion, cognitive load, genre moves, and typography.

## Dispatch Strategy Preview

Selected overlays:

- `baseline_sequence`: preserve the canonical ten-stage Refine loop.
- `xray_for_hidden_structure`: the visible problem is paragraph walls, but the hidden object is text rhythm, discourse movement, and review granularity.
- `tournament_for_alternatives`: compare three integration options instead of assuming CSS, schema, or validator work is the only route.
- `protected_context_for_external_or_sensitive_evidence`: external academic sources may inform local schema design but do not become canonical Arcanum truth without owner review.

Subagent strategy: `none`

Authorization: `not_needed` for this local synthesis. Runtime command-backed execution remains flagged because the `dispatch-spec` command is unavailable on the local Arcanum command surface.

## Validation

- Dispatch schema validation: `pass` with no blocks or flags via `python3 formulae/dispatch-spec/scripts/validate-dispatch.py spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/REFINE-DISPATCH.json --json`.
- Command resolution: `context-builder`, `invoke`, `distill`, and `interrogation` resolve locally; `dispatch-spec` does not resolve locally.
- Runtime execution: flagged, not dispatched through the full command-backed route in this turn.

## Stage Evidence

| Stage | Owner | Status | Artifact |
| --- | --- | --- | --- |
| 01 Context Builder evidence baseline | `context-builder` | pass | `stages/01-context-builder.md` |
| 02 Invoke Define | `invoke` | pass | `stages/02-invoke-define.md` |
| 03 Interrogation refine-review | `interrogation` | pass | `stages/03-interrogation-refine-review.md` |
| 04 Research decision | `refine` | pass | `stages/04-research-decision.md` |
| 05 Distill | `distill` | pass | `stages/05-distill.md` |
| 06 Invoke Redefine / Design | `invoke` | pass | `stages/06-invoke-design.md` |
| 07 Interrogation design review | `interrogation` | pass | `stages/07-interrogation-design-review.md` |
| 08 Distill Repair | `distill` | pass | `stages/08-distill-repair.md` |
| 09 Invoke Plan | `invoke` | pass | `stages/09-invoke-plan.md` |
| 10 Final synthesis | `refine` | pass | `stages/10-final-synthesis.md` |

## Required Artifacts

- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `RUNTIME-HANDOFF.md`
- `RESULT.md`
- `evidence-index.json`
