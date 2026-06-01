# Stage 10: Final Synthesis

Status: `pass`

## Answer

Yes, there is a strong way to manipulate this, and Whisper already has most of the foundation. The missing piece is a `readability_dynamics` layer.

This is not only typography. The category is `text_flow_and_readability_governance`: a bridge between discourse structure, cohesion/coherence, cognitive load, genre moves, typography, and agent-addressable review.

## What Already Exists

Whisper has:

- author intent substrate,
- transport schema,
- Pareto candidate selection,
- composition parts,
- draft validation,
- commentable review HTML,
- Playwright-extractable agent payloads.

This is enough to integrate the idea cleanly.

## What Is Missing

Whisper does not yet model the difference between:

- a semantic part,
- a paragraph,
- a discourse move,
- a reader beat,
- a visual treatment,
- a review anchor.

Because of that, a paragraph can be correct by schema and still feel like a wall.

## Recommended Integration

Add:

```text
draft_artifact -> readability_dynamics -> review_html -> review_payload -> revision_plan
```

The first schema should include:

- `rhythm_units`
- `beat_id`
- `block_id`
- `part_id`
- `discourse_move`
- `rhythm_role`
- `visual_treatment`
- `validation`

The first validator should flag:

- long paragraphs,
- consecutive dense blocks,
- missing scan anchors,
- missing examples after abstraction-heavy claims,
- weak discourse move coverage,
- broken review anchor mapping.

## Next Route

Run `task-session` for `SWU-WHISPER-READABILITY-001` first. Do not start with a draft rewrite. Start with schema and validator, then renderer, then browser validation, then revision from comments.

