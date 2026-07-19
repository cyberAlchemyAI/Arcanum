# Video Essay Transport Contract

## Identity

- Transport ID: `video_essay_model_input_package`
- Proof status: candidate
- Target runtime: 10-12 minutes
- Target voice length: 1,500-1,750 words
- Target public: curious technical builders, including people with practical
  AI-tool experience but no prior Arcanum vocabulary
- Objective: replace the model "making is executing an instruction" with the
  model "making is a governed way of testing and improving representations"
- Desired residue: the viewer can explain why a locally correct artifact may
  still fail its intent, and can distinguish Craft from CyberAlchemy

## Style Boundary

The production may use misconception-first teaching, curiosity gaps, concrete
experiments, delayed terminology, clear turns, honest boundaries, and a
zoom-out ending. These are general explanatory techniques. The package must
not imitate the distinctive wording, delivery, persona, visual identity, or
editing signature of any living creator.

## Audience Surfaces

| Surface | Audience receives it | Responsibility |
| --- | --- | --- |
| Voice copy | hears | Natural spoken argument with timing and pauses. |
| Written copy | sees | Titles, labels, questions, and definitions that can be read before the shot changes. |
| Visual scene | sees | Concrete evidence, spatial relation, comparison, or mechanism. It must do explanatory work. |
| Sound direction | hears | Sparse cues that clarify a turn, mismatch, return, or stop. |
| Citation card | sees when needed | Compact source or honesty-boundary attribution. |

## Production Surfaces

| Surface | Consumer | Responsibility |
| --- | --- | --- |
| Voice-model input | speech model | Clean narration only, segmented for independent generation and pickup recording. |
| Visual-model prompt | image/video model | One bounded shot with subject, action, framing, continuity, duration, and exclusions. |
| Shot list | editor | Segment timing, assets, text, transition, and source ownership. |
| Edit decision list | editor | Assembly order, handles, overlaps, pickup points, and audio bridges. |
| Source trace | reviewer | Distinguishes sourced definitions, synthesis, analogy, and authorial metaphor. |
| Authoring metadata | Whisper | Concept state, prior model, reveal, evidence, uncertainty, and validation intent. |

## Segment Contract

Every generated segment must carry:

```yaml
segment_id: VID-CAM-000
act_id: ACT-00
duration_seconds: 0
story_job: ""
concepts: []
prior_model: ""
voice_copy: ""
written_copy: []
visual_mode: live_action | generated_video | generated_still | motion_graphic | screen_capture
visual_prompt: ""
negative_prompt: ""
continuity_assets: []
camera_and_motion: ""
sound_direction: ""
transition_in: ""
transition_out: ""
source_refs: []
claim_posture: source | synthesis | analogy | metaphor
editor_notes: ""
```

Segments must be independently generatable. A model prompt cannot rely on
"the previous scene" without naming the exact continuity asset, state, and
camera relationship it needs.

## Voice Rules

- Write for breath, not for silent reading.
- Average sentence length should remain conversational; use a longer sentence
  only when its cadence carries a deliberate build.
- One paragraph should express one spoken move.
- Terms appear after their visual witness and remain stable afterward.
- Definitions use the sequence: what it is, how we can know it, what it is not,
  and what decision it changes.
- The narrator may say "we" when sharing an investigation, but must not use it
  to smuggle in agreement.
- The script must state where Craft is an operational model or analogy rather
  than an empirically validated universal theory.

## Written-Copy Rules

- One visible thought at a time.
- No authoring instructions, scene labels, or schema fields on screen.
- Prefer a question, contrast, or compact definition over a duplicate subtitle.
- A definition card may use at most two short lines plus the term.
- Technical names such as `schema`, `residue`, and `recomposition` appear only
  after the viewer has watched the corresponding relation happen.

## Visual Rules

- The perfect wrong door is the persistent anchor, not a disposable cold open.
- Every abstraction returns to a spatial change in the doorway, blueprint,
  hinge assembly, wall, or route through the building.
- Red thread or red tracing paper represents meaningful mismatch; it must not
  be generic warning decoration.
- Nested frames represent layers only after a local repair fails.
- A thread returning from a component to the full doorway represents
  recomposition.
- Avoid decorative abstraction, illegible generated text, fake interfaces,
  excessive particles, and atmospheric footage that carries no claim.
- Generated shots must reserve clean space for editorial text rather than ask
  the model to render precise typography.

## Completion Checks

The package can pass only when:

1. The operator explicitly approves the voice audition.
2. Every load-bearing concept in the concept map appears in the script or is
   explicitly deferred.
3. Every concept is witnessed before it is named.
4. Spoken definitions match their source posture and honesty boundary.
5. Craft and CyberAlchemy are neither collapsed nor presented as unrelated.
6. Every segment can be generated, voiced, replaced, and edited independently.
7. Voice-model and visual-model inputs contain no authoring commentary.
8. The source trace resolves every `source_ref` used by the shot list.
9. The HTML review surface exposes voice, written copy, visual prompt, and
   sources without overlapping or hiding content.
10. Browser checks pass at desktop and mobile review widths.

Pedagogical effectiveness is not a browser-testable completion claim. It
remains a future audience-validation route.
