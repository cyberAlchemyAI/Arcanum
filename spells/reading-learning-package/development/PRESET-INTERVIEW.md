---
title: Reading Learning Package Preset Interview
status: draft
updatedAt: 2026-06-20
owner: Arcanum maintainers
scope: spell-interview-contract
---

# Preset Interview Contract

## Purpose

The spell must not build a generic preset from bare questionnaire answers. It
should use a short, example-driven interview so the user can react to concrete
miniature outputs and improve the preset during setup.

## Interview Cadence

Ask one high-discrimination question at a time. Each question should include:

1. A short purpose line.
2. Two or three quick examples.
3. A "mix or rewrite" option.
4. A one-sentence explanation of how the answer changes the output.
5. The current preset delta recorded after the answer.

## Step 1: Preset Menu

Question:

> Which learning package preset should we start from?

| Choice | Example Output Shape | Tradeoff |
| --- | --- | --- |
| `deep_voice_reading` | "A chaptered PDF that walks slowly through the idea, with patient explanations and source-linked sidebars." | Best for durable learning; slower to create and review. |
| `quick_video` | "A two-minute script plus one-page PDF that makes one sharp idea memorable." | Fast and vivid; leaves nuance in source appendix. |
| `medium_explanation` | "A 5-8 page guide that explains the core model, shows examples, and ends with what to read next." | Balanced; may need careful scoping to avoid becoming long. |
| `custom_from_examples` | "Show me two mini examples and let me combine them." | Best when the user's taste is not represented by presets. |

## Step 2: Resonance Core

Question:

> Which voice should the package lean toward?

Examples:

- `patient_teacher`: "Let's slow this down. The paper is doing one strange
  thing very carefully: it separates what is visible from what can be inferred."
- `field_notebook`: "The useful clue is not the theorem yet; it is the residue
  left when the source evidence stops answering."
- `crisp_briefing`: "Core point: this tower gives you a reusable claim ledger,
  not a summary. Use it to decide what can be taught safely."

Record:

```yaml
resonance_core:
  accepted_examples:
    - <example id or user rewrite>
  rejected_examples:
    - <example id or reason>
  tone:
  voice:
  style_register:
  emotional_residue:
  forbidden_feels:
```

## Step 3: Relevance Core

Question:

> Who is the reader, and what should the package assume about them?

Examples:

- `curious_builder`: "Knows the project context, wants a usable mental model,
  does not want academic throat-clearing."
- `technical_reviewer`: "Needs source traceability, definitions, and explicit
  misuse warnings before trusting the explanation."
- `smart_outsider`: "Has no local Arcanum context, needs concrete examples and
  terms introduced without internal shorthand."

Record:

```yaml
relevance_core:
  target_public:
  reader_state:
  assumed_knowledge:
  likely_objections:
  authority_mode:
  reader_reward:
```

## Step 4: Trajectory Core

Question:

> What movement should the package perform?

Examples:

- `from_confusion_to_map`: "Start with why the source feels hard, then build the
  map, then show how to use it."
- `from_claim_to_practice`: "Start with one claim, unpack the evidence, then
  turn it into a practical reading protocol."
- `from_story_to_system`: "Open with a vivid moment, then reveal the source
  structure and end with reusable rules."

Record:

```yaml
trajectory_core:
  narrative_anchor:
  introduction_strategy:
  body_parts:
  ending_strategy:
  length:
  must_include:
  must_avoid:
```

## Step 5: Preset Refinement Check

Show a compact preview before drafting:

```text
Preset: <id>
Voice: <one sentence>
Reader: <one sentence>
Movement: <one sentence>
Output: <PDF/script/reading guide shape>
Example opening:
  <3-5 sentences generated from tower/source handles>
```

Then ask:

> Keep this direction, or should I bend the preset before composing?

Allowed answers:

- `keep`
- `more patient`
- `more concrete`
- `more technical`
- `more narrative`
- `shorter`
- `longer`
- free-form rewrite

## Preset Profile Schema

```yaml
preset_profile:
  preset_id: deep_voice_reading | quick_video | medium_explanation | custom_from_examples
  source:
    tower_root: <path>
    source_artifacts:
      - <path>
  resonance_core: {}
  relevance_core: {}
  trajectory_core: {}
  examples:
    accepted:
      - id: <example or user rewrite>
        reason: <why>
    rejected:
      - id: <example or user rewrite>
        reason: <why>
  pdf_preferences:
    page_size: letter | a4 | unset
    citation_style: inline | footnote | appendix
    density: spacious | standard | compact
  approval:
    preset_preview_status: approved | revise | blocked
```

## Failure Policy

- If the user cannot choose a preset, use `custom_from_examples` and show two
  contrasting previews.
- If a core remains vague, draft only a preset preview and return `flag`.
- If source artifacts are missing, block composition and route to tower/source
  repair.
- If PDF preferences are unknown, default to `standard` density and appendix
  citations, but record the default in `preset-profile.yaml`.
