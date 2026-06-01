# Stage 06: Invoke Redefine / Design

Status: `pass`

## Proposed Schema Section

```yaml
readability_dynamics:
  layer_id: substack_research_post_readability_v1
  source_candidate_set: executable_language_research_note
  defaults:
    max_words_per_paragraph: 120
    target_words_per_beat:
      min: 20
      max: 75
    max_consecutive_dense_paragraphs: 1
    require_scan_anchor_every_n_blocks: 3
  discourse_moves:
    allowed:
      - hook
      - claim
      - evidence
      - bridge
      - example
      - contrast
      - concession
      - implication
      - invitation
      - pause
  visual_treatments:
    allowed:
      - prose
      - short_paragraph
      - micro_heading
      - pull_quote
      - callout
      - example_box
      - question_line
      - transition_line
  rhythm_units:
    - beat_id: b001
      block_id: p001
      part_id: reader_grounded_opening_hook
      discourse_move: hook
      rhythm_role: opening_handle
      visual_treatment: short_paragraph
      validation:
        max_words: 80
        must_include_any:
          - name
          - language
          - workflow
    - beat_id: b002
      block_id: p002
      part_id: reader_grounded_opening_hook
      discourse_move: claim
      rhythm_role: thesis_turn
      visual_treatment: prose
      validation:
        max_words: 100
```

## Integration Point

Add `readability_dynamics` to the substrate under the same owner as `composition_parts`. The first implementation should not require rewriting the draft. It should parse the existing draft, infer metrics, and report which blocks need readability treatment.

## Validator Rules

The validator should emit `pass`, `flag`, or `block`.

Initial checks:

- `paragraph_word_count`: flag if any prose paragraph exceeds the configured max.
- `sentence_count_variance`: flag if too many consecutive long sentences appear.
- `abstraction_density`: flag when a block has many abstract/internal terms and no example.
- `scan_anchor_spacing`: flag if no micro-heading, question, callout, or transition anchor appears across too many blocks.
- `discourse_move_coverage`: flag if required body parts lack at least one expected move.
- `review_anchor_integrity`: block if beat splitting breaks block or part mapping.

## Review HTML Rules

`build-whisper-review-html.py` should be able to render:

- paragraph blocks when no readability layer exists,
- beat blocks when `readability_dynamics.rhythm_units` exists,
- child beat anchors inside a paragraph block when one paragraph must remain source-stable,
- visual treatments such as micro-head, pull quote, question line, example box, and transition line.

## Agent Revision Rules

When comments are extracted by Playwright, the agent should propose changes at the smallest stable anchor:

- `beat_id` when present,
- otherwise `block_id`,
- always preserving `part_id`.

Change options should include:

- split into beats,
- add micro-heading,
- convert abstraction into example,
- add question or pause,
- move bridge later,
- strengthen cohesion signal,
- route part-level mini-tournament.

