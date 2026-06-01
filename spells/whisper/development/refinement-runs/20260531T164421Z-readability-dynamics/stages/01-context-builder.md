# Stage 01: Context Builder Evidence Baseline

Status: `pass`

## Local Evidence

Whisper already models text production as a governed artifact lifecycle:

- `text_intent_substrate`
- `transport_schema`
- `scu_candidate_set`
- `pareto_consensus`
- `composition_plan`
- `draft_artifact`
- `review_html`
- `validation_report`
- `learning_residue`

The current review HTML contract is addressable and useful, but paragraph-level only. `build-whisper-review-html.py` parses markdown into prose paragraphs and renders one `review-block` per paragraph. This creates stable comment targets, but it also makes the visible reading unit equal to the markdown paragraph.

`text-intent-substrate.yaml` already has `composition_parts` with roles such as `introduction`, `reference_bridge`, `research_context`, `core_insight`, `live_example`, `implications`, and `invitation`. It also has a two-tier Pareto policy where part-level mini-tournaments run for delegated, revised, or validation-failed parts, not for every paragraph.

`validate-whisper-draft.py` checks Pareto completeness, opening contract compliance, required terms, word count, character count, and citation/reference placement. It does not check paragraph density, rhetorical movement, scan path, sentence rhythm, or abstraction load.

## Problem Shape

The issue is not simply that paragraphs are too long. The issue is that the current lifecycle does not separate:

- semantic part: what role the section plays,
- discourse move: what relationship the unit performs,
- rhythm unit: how much text the reader must process before a pause,
- visual treatment: how the review page should render that unit,
- validation: what makes the unit readable enough for the transport.

## Existing Constraint

Any fix must preserve the review payload contract:

- stable `block_id`
- stable `part_id`
- selected text
- comment type and requested change mode
- original source text
- extraction through `window.WhisperReview.getAgentPayload()`

