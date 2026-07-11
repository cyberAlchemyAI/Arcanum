# Live Presentation Preset

Preset ID: `live_presentation`

Use this Whisper preset when a person will present slides in a room or call. The
preset treats the presentation as a performed conversation supported by a
screen, not as an essay divided into rectangles or a schema rendered as text.

## Use When

- The artifact will be presented aloud.
- Audience thinking time, questions, reveals, or discussion are part of the
  experience.
- The source contains formal models, schemas, research, or authoring metadata
  that must be interpreted into room-native language.
- HTML or browser validation will follow editorial approval.

Do not use this preset for a document merely called a deck when nobody will
present it. Use the appropriate memo, business-plan, or document transport and
derive a deck substrate instead.

## Required Surfaces

- `projected_copy`: what the audience reads.
- `spoken_copy`: what the presenter says.
- `speaker_notes`: private delivery and evidence support.
- `interaction_prompt`: what the audience is genuinely invited to consider or
  do.
- `authoring_metadata`: story state, pedagogy, consequence, source mapping, and
  construction intent. This surface is never projected.

## Mandatory Audition

Before generating the complete presentation, produce only three representative
moments:

1. `opening`: establishes the room's first concrete tension.
2. `tension`: makes the unresolved problem felt without explaining it away.
3. `reveal`: names or reframes something the audience has already encountered.

Show the operator only projected and spoken copy during approval. Keep notes and
authoring metadata available for audit but outside the approval view. Stop when
voice approval is `pending` or `rejected`.

## Non-Negotiables

- Write for the room, not for the source schema.
- Never project story-state, consequence, validation, or facilitation language.
- Do not make slide titles read like instructions to the author.
- Do not put the answer inside the question.
- Introduce formal vocabulary after its concrete need is visible.
- Keep one visible thought per audience moment.
- Read spoken copy aloud before asking for approval.
- Treat browser tests as implementation evidence only.

## Invocation Shape

```text
Use whisper preset live_presentation.
Audience: <who is in the room>
Room outcome: <what should change for them>
Source material: <paths or notes>
Presentation conditions: <duration, presenter, interaction level>
First output: three-moment language audition only
```

Use [audition-template.md](audition-template.md) for the approval artifact and
`preset.yaml` for the complete transport contract.
