# From Table to Text Slide Schema

## Purpose

This is the first beginner Craft presentation. Learners begin with the ordinary
question, "What would you need to build this table?" Their answers become a
sketch, the sketch earns the term `schema`, and that relation is transported to
software that helps someone write.

The authoritative machine view is
`CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.yml`. The HTML deck embeds that data
mechanically through `build-deck.py`.

## Teaching Promise

The learner follows five moments:

1. Inspect one table and think privately about what its construction requires.
2. Add short answers to a live Mentimeter word cloud, then recover four useful
   groups: materials, tools, measurements, and steps.
3. Decide which answers belong on a drawing and use them to make one buildable
   sketch.
4. Compare a table picture with that buildable sketch and name the function the
   second one performs: `schema`.
5. Ask what would play the same role in writing software, then shape an
   adaptable text mold.

The governing relation is:

> A table sketch acts as a schema when it selects the parts, dimensions,
> relations, and conditions that building and checking must preserve.

For writing software, the analogous schema preserves purpose, audience,
meaning, evidence, shape, voice, and ending before sentences are generated.

## Adaptability Boundary

There is no honest fixed outline for "any text." An email, essay, set of
instructions, and presentation require different body parts and checks.

The reusable layer keeps stable questions:

- What should the text do?
- Who must understand or act?
- What meaning must remain true?
- What supports it?
- How should it sound?
- Where should the reader arrive?

The selected text type then supplies its required parts, order, emphasis, and
checks. The mold fixes the questions, not the final form.

## Mentimeter Contract

Configure the supplied Mentimeter presentation as a word cloud with this exact
question:

> What would you need to build this?

The table must be visible during a fifteen-second private pause. The first
reveal mounts the iframe. The second reveal unmounts it and brings the room's
concrete vocabulary back into the presentation.

The remote Mentimeter configuration is an external dependency. Local browser
validation proves that the iframe appears and loads at the declared moment; a
presenter preflight must still prove the live response path.

## Stateful Slide Contract

| Field | Responsibility |
| --- | --- |
| `id` | Stable slide identity used by navigation and hash routing. |
| `story_state` | Authoring-only causal condition at this point in the lesson. |
| `visual` | Renderer used for the persistent witness. |
| `states` | Ordered learner-visible states. |
| `states[].visible` | Evidence currently available to the learner. |
| `states[].learner_prompt` | The one decision or reflection requested now. |
| `states[].accepted_inputs` | Inputs that may cause the declared transition. |
| `states[].transition_to` | The only next state for the current activation. |
| `states[].consequence` | Authoring-only account of what becomes true after the transition. |
| `states[].earned_term` | Zero or one formal term activated in this state. |
| `states[].validation_check` | Authoring-only observable learner response expected from the state. |
| `viewport` | Essential content required on desktop and before the first mobile fold. |
| `focus_behavior` | Which element owns activation and navigation keys. |

## Surface Boundary

Audience-facing surfaces contain only the title, current prompt, visible
details, live word cloud, and earned term. Speaker notes own pacing and
facilitation. Story state, consequence, validation intent, chapter, and
viewport rules remain authoring metadata and may not be projected.

## Formal-Term Gate

`schema` is the only formal term in this presentation. It appears only after
learners have supplied build needs, selected which needs belong on a sketch,
and compared a recognizable picture with a structure that can guide building
and checking.

The later writing slides reuse the earned relation without introducing another
formal Craft term.

## Completion Boundary

The presentation ends with:

> A reusable writing mold fixes the questions, not the final form.

A later presentation may follow how a selected writing schema becomes an
artifact and how the result is checked. Those ideas are intentionally outside
this deck.
