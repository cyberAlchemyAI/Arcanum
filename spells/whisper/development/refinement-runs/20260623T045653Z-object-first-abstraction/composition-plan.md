# Composition Plan - Object, the First Abstraction

- **Spell:** whisper
- **Transport:** `substack_research_post`
- **Source substrate:** `text-intent-substrate.yaml`
- **Parent draft:** `../20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md`
- **Selected candidate:** `merged_systems_explainer`
- **Draft target:** `DRAFT-SUBSTACK-003.md`
- **Length target:** 900-1,800 words

## Candidate Rationale

`merged_systems_explainer` is the selected route because it preserves Draft 02's
reflective, systems-minded thesis while borrowing `learning_distill` as the
explanatory camera. The draft should feel like a sequel, not a restart: Draft 02
said that language can become a tool-making medium; this post explains the first
mechanism after naming.

Rejected routes remain available as local moves:

- `literary_quote_bridge`: use Shakespeare/Korzybski only as optional allusion
  after the bridge is working. Do not let the reference become the structure.
- `arcanum_internal_deepening`: use Arcanum primitives as the proof example, but
  keep the main path legible to readers who are not inside the system.

## Narrative Anchor

Draft 02 ends by asking the reader to name one workflow, give it purpose and
constraints, and treat the name as an object they can revise. The sequel opens
there:

> A name gives us a handle. An object gives the handle a shape.

One running analogy carries the draft: **handle to shape**. A name is the handle
that lets us point at a recurring pattern. An object is the shaped thing we can
pick up, turn around, inspect, revise, and eventually encode into a schema.

## Core Claim

After naming, the first useful abstraction is `Object`: a bounded model of the
named thing. In primitive terms:

- **Properties** are what the concept carries, remembers, protects, or depends
  on.
- **Methods** are what the concept can do, trigger, change, or refuse.
- **Schema** is the next abstraction that makes those parts inspectable,
  portable, and reusable.

## Section Plan

| # | Part ID | Job | Draft Moves |
| - | ------- | --- | ----------- |
| 1 | `bridge_from_draft_02` | Establish sequence continuity | Refer to the prior instruction without summarizing the whole post. Open with the question: what happens after a workflow has a name? |
| 2 | `surprising_problem_name_is_not_model` | Create the Veritasium-style tension | Show that naming lets us point, but does not yet tell us structure, action, or failure modes. |
| 3 | `one_running_analogy_handle_to_shape` | Give the reader a durable image | Use "handle" for name and "shape" for object. Keep this analogy throughout; do not add a second big metaphor. |
| 4 | `object_as_first_abstraction` | Define Object without programming intimidation | Object means a bounded thing we can inspect. Mention software only to say this is more primitive than a programming tutorial. |
| 5 | `properties_as_structure` | Explain structure | Properties are the object's memory and boundary. Use a named workflow example, such as `reader-grounded opening` or `reference-first`. |
| 6 | `methods_as_action` | Explain action | Methods are available moves: start, refuse, revise, validate, delegate, close. Keep verbs concrete. |
| 7 | `arcanum_mapping_alias_sigil_spell_schema` | Ground the model in Arcanum | Alias names the handle. Sigil governs an object-like capability. Spell composes capabilities. Schema exposes the body's fields, gates, and checks. |
| 8 | `small_reader_recipe` | Give the practical click | Ask the reader to choose one named workflow, list three properties, list three methods, and add one validation check. |
| 9 | `honest_limits_and_translation_warning` | Preserve trust | Say a model can be useful without being complete. Warn that private jargon is a failed interface, not a superior abstraction. |
| 10 | `reflective_close` | Set up the next abstraction | Close by showing that once a name has object shape, schema becomes the way to share and reuse it. |

## Paragraph-Level Draft Map

| Paragraphs | Part IDs | Target Effect |
| ---------- | -------- | ------------- |
| 1-2 | `bridge_from_draft_02`, `surprising_problem_name_is_not_model` | The reader feels the sequel snap into place. |
| 3-4 | `one_running_analogy_handle_to_shape`, `object_as_first_abstraction` | The mechanism becomes simple before vocabulary expands. |
| 5-7 | `properties_as_structure`, `methods_as_action` | The reader can distinguish structure from action in a concept. |
| 8-9 | `arcanum_mapping_alias_sigil_spell_schema` | Arcanum becomes an example of the primitive model, not an internal detour. |
| 10-11 | `small_reader_recipe`, `honest_limits_and_translation_warning` | The reader gets a usable exercise plus guardrails. |
| 12 | `reflective_close` | The post lands on schema as the natural next step. |

## Opening Contract

The opening must begin from the prior post's final move, not from an external
authority or a definition.

Recommended opening shape:

1. "In the last post, I ended with a small instruction..."
2. "That sounds simple until you try it."
3. "Because naming something is not the same as understanding it."
4. "The name has to become a model."
5. "The smallest useful model is an object."

Avoid opening with Shakespeare, Korzybski, OOP, or Arcanum. Those are later
supports, not the door.

## Example Thread

Use one small running example alongside the analogy. Recommended example:
`reader-grounded opening`.

- Name: `reader-grounded opening`
- Properties: target reader, reader state, opening constraint, forbidden
  opening moves, success signal
- Methods: start from lived experience, reject abstract opening, introduce
  source after handle exists, validate first paragraph
- Validation check: first paragraph starts with reader-facing situation before
  external authority

This example ties back to Draft 02's own opening contract and keeps Arcanum
nearby without requiring the reader to learn all of Arcanum first.

## Arcanum Translation

Use this mapping lightly and in public-safe terms:

- `alias`: a small handle for a repeatable move.
- `sigil`: a governed capability with purpose, process, constraints, and
  validation.
- `spell`: a route that composes capabilities into a larger movement.
- `schema`: the visible body of the model: fields, gates, dependencies, and
  checks.

Do not explain the whole Arcanum system. The point is that Arcanum is a live
example of naming becoming modeling, not a product pitch.

## Reference Policy

References are optional seasoning, not structure.

- Shakespeare's "what's in a name" can appear as a light contrast only after the
  bridge is established. Use allusion unless the exact source is verified.
- Korzybski's map/territory frame can support the modeling point, but only as a
  checked paraphrase or verified citation.
- Carroll/Humpty Dumpty can be reserved for the warning about private naming
  systems. Use only if the draft needs that extra turn.

No direct quote should enter the draft until source text and wording are
verified.

## Voice Rules

- Keep Draft 02's reflective systems voice: thoughtful, operational, and
  research-native.
- Use `learning_distill` as camera: one surprising problem, one running analogy,
  one visible mechanism, one practical exercise.
- Define every technical term before it is allowed to carry weight.
- Prefer short, concrete sentences when explaining properties and methods.
- Use Arcanum terms as examples after the mechanism is clear.
- Keep the reader in the room: "you can name...", "you can ask...", "try..."
- Do not say or imply that natural language replaces engineering.
- Do not turn Object into an OOP lesson.

## Draft Prompts

Use these as local drafting prompts for each part:

- What did Draft 02 leave the reader holding?
- What does the name let us do that we could not do before?
- What does the name still fail to tell us?
- Where is the boundary of this named thing?
- What must it remember?
- What can it do?
- What should it refuse?
- What check tells us the model helped?
- How does this prepare schema as the next abstraction?

## Validation Checklist

- [ ] Opens as a sequel to Draft 02, not as a standalone reset.
- [ ] Uses one running analogy: handle to shape.
- [ ] Defines Object before any software association dominates.
- [ ] Explains properties as structure/memory/boundary.
- [ ] Explains methods as action/verbs/available moves.
- [ ] Includes one concrete named-workflow example.
- [ ] Maps Arcanum primitives without turning into internal documentation.
- [ ] Includes a small reader exercise.
- [ ] States honest limits around over-modeling and private jargon.
- [ ] Avoids unverified direct quotes.
- [ ] Keeps the draft within 900-1,800 words.
- [ ] Ends by setting up schema as the next abstraction.

## Draft Gate

Ready for drafting when:

- `text-intent-substrate.yaml` is present and selected candidate is
  `merged_systems_explainer`.
- This composition plan exists.
- Any direct quote has a verified source, or references remain paraphrase/allusion.

Current status: **ready for draft**, with citation integrity flagged for direct
quotation only.
