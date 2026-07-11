# Craft Causal Class Slide Schema

## Purpose

This schema defines a beginner Craft class as a sequence of observable teaching states, not a list of slide contents. A formal term is earned only after learners inspect a witness, make or predict a consequential choice, and observe the result.

The authoritative machine view is `CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.yml`. The HTML deck embeds that data mechanically through `build-deck.py`.

The schema also separates what the audience sees from what the author and
presenter need. The HTML may project only the slide title, current learner
prompt, current visible details, and an earned term. Story state, consequence,
validation intent, viewport rules, and focus behavior are authoring metadata.
They must never appear as slide copy.

## Audience

Beginning developers with some experience asking an AI to build software.

## Teaching Promise

The learner follows one small desk through a complete causal history:

1. A generic object becomes a bounded target.
2. The class chooses fast corner attachments.
3. Facts make the stability risk visible.
4. A schema fixes what counts as a valid result.
5. A plan orders the work without replacing the schema.
6. An artifact exists and can be inspected.
7. Validation compares it with the earlier commitments.
8. The table wobbles, producing named residue.
9. A shim closes level but not sideways stability.
10. A lower build receives an explicit boundary and return interface.
11. It earns layer status only after lower residue plus local and upper validation.
12. Recomposition returns the result and the work stops at acceptable residue.
13. A student-dashboard failure lets learners recognize the same reasoning in software.
14. Learners reconstruct the method before seeing the final name, Craft.

The shim scene is a deliberate beginner witness. It is not a claim that every lower-layer trial must begin with a failed repair.

## Stateful Slide Contract

Each slide declares:

| Field | Responsibility |
|---|---|
| `id` | Stable slide identity used by navigation and hash routing. |
| `story_state` | Authoring-only causal condition at this point in the story. |
| `visual` | Renderer used for the persistent witness. |
| `states` | Ordered learner-visible states. |
| `states[].visible` | Evidence currently available to the learner. |
| `states[].learner_prompt` | The one decision or prediction requested now. |
| `states[].accepted_inputs` | Inputs that may cause the declared transition. |
| `states[].transition_to` | The only next state for the current activation. |
| `states[].consequence` | Authoring-only account of what becomes true after the transition. |
| `states[].earned_term` | Zero or one formal term activated in this state. |
| `states[].validation_check` | Authoring-only observable learner response expected from the state. |
| `viewport` | Essential desktop and mobile information obligations. |
| `focus_behavior` | Ownership of keyboard input and propagation behavior. |
| `notes` | Presenter-only spoken direction, timing, and cautions. |

## Surface Contract

| Surface | Content | Projected? |
|---|---|---|
| Projected copy | slide title, current learner prompt, visible details, earned term | yes |
| Spoken copy | natural delivery carried in speaker notes | no |
| Interaction prompt | current learner prompt and reveal control | when active |
| Authoring metadata | chapter, story state, consequence, validation check, focus and viewport rules | never |

Browser validation must fail when authoring metadata selectors or values appear
in the projected narrative surface.

## Interaction Invariants

- One input causes at most one state transition.
- Enter and Space on a focused scene never bubble into slide navigation.
- A terminal state never resets through another activation.
- Formal terms are absent before their witness and consequence.
- Authoring metadata is not projected.
- Speaker notes are hidden by default and open in an overlay.
- Desktop presentation states fit within the supported viewport.
- Mobile may scroll, but witness, current prompt, primary action, progress, and navigation appear before the first fold.
- The state survives scrolling, focus changes, and notes toggling.

## Formal Terms

Only seven formal terms are introduced: `schema`, `artifact`, `validation`, `residue`, `craft layer`, `recomposition`, and `Craft`.

Define, research, design, plan, execute, and reflect remain ordinary verbs. The first class omits entropy. The smallest coherent unit remains a plain-language comparison rather than a new acronym.

## Slide Map

| Slide | Primary movement | Earned term |
|---|---|---|
| S01 | Generic table -> bounded target | none |
| S02 | Plausible options -> recorded choice | none |
| S03 | Unknowns -> facts that change design | none |
| S04 | Candidate descriptions -> chosen validity structure | schema |
| S05 | Unordered work -> executable sequence | none |
| S06 | Drawing -> inspectable result | artifact |
| S07 | Obligations -> explicit comparison | validation |
| S08 | Prediction -> caused wobble | residue |
| S09 | Shim -> remaining sideways failure | none |
| S10 | Hidden decisions -> candidate lower boundary | none |
| S11 | Local pass -> upper pass -> lower residue | craft layer |
| S12 | Lower result -> upper closure | recomposition |
| S13 | Plausible dashboards -> concrete student task | none |
| S14 | Learner reconstruction -> final name | Craft |

## Validation Boundary

Static and browser checks can verify schema parity, transition exclusivity, reveal order, focus behavior, viewport layout, and accessible control state. They cannot prove that the teaching works for beginners.

Pedagogical effectiveness remains a hypothesis until learner trials test independent choice, explanation, delayed recall, and transfer.
