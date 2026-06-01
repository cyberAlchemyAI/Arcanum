# Refine Seed Proposal

## Target

Whisper readability and review dynamics for:

- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html`
- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md`
- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`

## Operator Intent

The current draft reads like large text blocks. The text is not dynamic or easy enough to read. The operator wants to know whether this can be manipulated by schema and validation, how academic fields study this problem, how it should be integrated into Whisper, and whether Arcanum already has enough machinery to support it.

## Refinement Objective

Define the smallest coherent Whisper extension that governs readability dynamics without turning the system into arbitrary visual styling. The extension must preserve the current schema-first and validator-backed direction:

- Author intent remains governed by `text_intent_substrate`.
- Composition remains controlled by `composition_parts` and Pareto dynamics.
- Review remains addressable through `review_html`.
- Future revisions can consume Playwright-extracted comments and produce targeted change options.

## Source Context

Local evidence:

- `spells/whisper/README.md` defines `review_html`, stable comment blocks, and the draft artifact lifecycle.
- `text-intent-substrate.yaml` already defines `composition_parts`, `pareto_tournament`, and part-level mini-tournament triggers.
- `build-whisper-review-html.py` currently parses markdown into paragraph blocks and renders each paragraph as one review block.
- `validate-whisper-draft.py` validates opening contract, Pareto completeness, required terms, and length constraints, but not readability dynamics.

External research focus:

- Discourse structure and rhetorical relations.
- Cohesion, coherence, readability, and computational text features.
- Cognitive load, segmenting, and signaling.
- Genre moves for research-style introductions.
- Typography and information design for screen reading.

## Done Criteria

The refinement is complete when it answers:

1. What is the correct category for this concern?
2. What already exists in Whisper?
3. What is missing?
4. What schema substrate should be added?
5. What validator should enforce it?
6. What HTML review behavior should change?
7. What next task-session SWU should implement first?

## Validation Surface

- `REFINE-DISPATCH.json` validates against the dispatch schema.
- Final result distinguishes existing artifact contracts from proposed mutations.
- Recommended implementation is staged and does not mutate the current schema without a task-session.
- Academic grounding is cited as external supporting context, not promoted as canonical local doctrine.

## Preset And Research

Preset: `full`

Research mode: `bounded-research`, selected because the operator explicitly asked how academia studies the problem.

