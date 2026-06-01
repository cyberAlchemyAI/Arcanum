# Runtime Handoff

Status: `flag`

Adapter: local artifact synthesis

Dispatch route: `REFINE-DISPATCH.json`

## Strategy Permission State

Subagent strategy: `none`

Authorization: `not_needed`

Reason: the refinement can be synthesized from local artifacts plus bounded external research. No role-bound sibling agents are needed before the next implementation SWU.

## Command Surface

Resolved locally:

- `context-builder`
- `invoke`
- `distill`
- `interrogation`

Not resolved locally:

- `dispatch-spec`

Runtime implication: the dispatch shape validates cleanly with `formulae/dispatch-spec/scripts/validate-dispatch.py`, but command-backed execution of a full `dispatch-spec` stage is flagged because the command is not installed on `tools/arcanum --resolve`.

## Handoff Objective

Implement a Whisper readability dynamics layer that:

- Extends `text-intent_substrate` with a `readability_dynamics` or `text_rhythm_layer` section.
- Adds beat-level metadata for paragraphs, claims, bridges, examples, questions, pauses, and callouts.
- Lets `build-whisper-review-html.py` render more than one visual unit from one prose paragraph when the schema requires it.
- Adds a validator that checks paragraph density, scan path, abstraction load, sentence rhythm, and discourse-move coverage.
- Preserves `block_id`, `part_id`, selected text, issue/request/priority, and Playwright payload extraction.

## Next Executable Route

Recommended: `task-session`

First SWU:

`SWU-WHISPER-READABILITY-001`: add a non-breaking readability dynamics schema section and validator-only checks without changing the draft content.

Second SWU:

`SWU-WHISPER-READABILITY-002`: update review HTML generation so a draft can be rendered as beats, micro-heads, pull quotes, examples, and questions while still exporting addressable agent payloads.

Third SWU:

`SWU-WHISPER-READABILITY-003`: regenerate `DRAFT-SUBSTACK-002.review.html`, validate it in a browser over localhost, and use exported comments as revision input.
