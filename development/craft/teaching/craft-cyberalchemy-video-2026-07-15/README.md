# Craft And CyberAlchemy Video Essay

Status: full draft, production package ready for model generation and edit
Transport: candidate `video_essay_model_input_package`
Runtime: 11:46
Voice length: 1,525 words
Target public: curious technical builders who use or encounter AI agents

## Start Here

1. Open [the full browser review](review.html) to inspect all 22 scenes and
   leave scene-addressed comments.
2. Send [the clean voice input](VOICE-MODEL-INPUT.md) to the selected voice
   model.
3. Generate scene clips from [the visual-model prompts](VISUAL-MODEL-PROMPTS.yml).
4. Assemble the result with [the edit decision list](EDIT-DECISION-LIST.md) and
   [shot-list source](SHOT-LIST.yml).

The complete voice, on-screen language, visual prompts, timing, source posture,
and edit instructions are projections of `SHOT-LIST.yml`. Run
`python3 build-video-package.py` from this folder after changing the source.

## Story

The video begins with a perfectly built door that opens into a wall. The
contradiction breaks the prior model that good execution necessarily produces
the right artifact. The door then becomes an instrument for discovering
intention, objective, boundary, schema, translation, artifact, validation,
residue, coherent units, layers, and recomposition.

Craft is named only after its mechanism is visible. CyberAlchemy follows as
the governance that makes the learning inspectable, navigable, reusable, and
capable of surviving handoff. The video ends by returning the governing
question to the viewer's next human-or-AI build.

## Production Package

- [Shot-list source](SHOT-LIST.yml): canonical scene data for all generated
  production views.
- [Full voice script](FULL-VOICE-SCRIPT.md): read-through script with act and
  scene boundaries.
- [Voice-model input](VOICE-MODEL-INPUT.md): clean narration without authoring
  metadata.
- [On-screen written copy](ON-SCREEN-WRITTEN-COPY.md): exact overlays, roles,
  positions, and durations.
- [Visual-model prompts](VISUAL-MODEL-PROMPTS.yml): one independently
  generatable prompt package per scene.
- [Edit decision list](EDIT-DECISION-LIST.md): timing, transitions, sound,
  continuity, and editor notes.
- [Browser review](review.html): interactive scene, source, and comment review.

## Design And Evidence

- [Transport contract](TRANSPORT-CONTRACT.md): production surfaces, segment
  schema, boundaries, and completion checks.
- [Concept map](CONCEPT-MAP.md): definitions, epistemic roles, visual witnesses,
  and honesty boundaries for every load-bearing concept.
- [Composition plan](COMPOSITION-PLAN.md): narrative acts, scene inventory,
  visual grammar, and model-input strategy.
- [Source trace](SOURCE-TRACE.md): source, synthesis, analogy, and metaphor
  boundaries.
- [Approved voice audition](VOICE-AUDITION.md): the opening, tension, and reveal
  gate that preceded full drafting.
- [Validation report](VALIDATION-REPORT.md): structural, editorial, source, and
  browser evidence with explicit proof limits.
- [Whisper result](WHISPER-RESULT.md): lifecycle status and next route.

## Review Adapter

`review.template.html` and `build-video-package.py` generate `review.html`.
Comments persist in browser `localStorage` and export through
`window.VideoReview.getAgentPayload()`. `audition-review.html`,
`build-audition-review.py`, and `whisper-review-substrate.yml` preserve the
approved pre-draft audition as history.

## Current Residue

- The visual prompts are complete but have not yet been tested against a
  visual-generation model. Prompt fitness is therefore unverified.
- The voice script is approved and structurally validated, but a generated
  voice performance has not been reviewed.
- Pedagogical effectiveness remains a hypothesis until audience evidence
  exists. Source fidelity, schema validity, and browser quality do not prove
  that viewers learned the distinctions.
