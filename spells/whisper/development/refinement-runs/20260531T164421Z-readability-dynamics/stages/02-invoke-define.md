# Stage 02: Invoke Define

Status: `pass`

## Definition

The refinement target is a missing Whisper layer: `readability_dynamics`.

This layer should sit between `draft_artifact` and `review_html`.

It should not replace `composition_parts`; it should refine how each part becomes readable, reviewable units.

## Proposed Category

Category: `text_flow_and_readability_governance`

Subcategories:

- `discourse_structure`: claim, evidence, background, contrast, elaboration, implication, invitation.
- `cohesion_and_coherence`: how sentences and sections connect into a mental model.
- `cognitive_load_management`: segmenting, signaling, pre-training, pacing, and abstraction rate.
- `genre_move_structure`: expected moves for Substack research posts, introductions, fundraising copy, slides, and articles.
- `typographic_information_design`: line length, spacing, hierarchy, callouts, scan path, and mobile readability.
- `review_addressability`: mapping visible units to stable agent-editable anchors.

## Why The Current Draft Feels Blocky

The current draft is organized as meaningful paragraphs, but the review surface has one visible form:

`paragraph -> review block -> paragraph text`

That means the reader gets the same visual and cognitive affordance for:

- a hook,
- a bridge,
- an example,
- a definition,
- a concession,
- an implication,
- an invitation.

Whisper currently knows these roles in the schema, but the renderer and validator do not use them to shape the reading experience.

## Refined Objective

Add a schema and validation layer that can transform draft prose into a sequence of readable beats while preserving author intent and agent-editable review anchors.

