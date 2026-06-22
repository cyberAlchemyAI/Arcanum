---
title: Reading Learning Package Define
status: draft
updatedAt: 2026-06-20
owner: Arcanum maintainers
scope: spell-development
observedCapability: invoke
targetLifecycleOwner: spellcraft
targetSpell: reading-learning-package
---

# Reading Learning Package Define

## Mission

`reading-learning-package` is a candidate spell that converts a governed research
tower plus source artifacts into a personalized reading package and PDF-ready
learning artifact.

The spell should help a user learn from a tower result without reopening the
research task. It should ask for a preset, refine that preset through a guided
interview with quick examples, compose a manuscript using `whisper`, and render a
traceable PDF package.

## User Intent Captured

The user asked for a new spell development package that:

- uses `research-tower` and `whisper`;
- takes a tower result and source artifacts as input;
- creates learning packages in reading form;
- composes a PDF with the content;
- asks which preset the user wants;
- ships starter presets for long voice in-depth explanations, quick videos, and
  medium-length explanation;
- interviews the user about the SCU cores;
- uses quick examples during the interview so presets improve from preference
  evidence instead of generic questionnaire answers.

## Ownership Boundary

| Owner | Owns | Does Not Own |
| --- | --- | --- |
| `invoke` | This definition, design, plan, dispatch trace, and Spellcraft handoff package. | Spell installation, canonical contract promotion, runtime execution. |
| `spellcraft` | Spell lifecycle mutation, phase/gate design, install/adapt, validate, observe, reflect. | Internal `research-tower` or `whisper` sigil contracts. |
| `research-tower` | Source-backed tower structure, claim ledger, glossary, definitions, notation, final learning pack, residue. | Reader-specific composition or PDF layout. |
| `whisper` | SCU cores, preset-sensitive text intent substrate, candidate tournament, composition plan, draft, validation, learning residue. | Source-claim authority or PDF renderer implementation. |
| `task-session` | Bounded implementation SWUs after Spellcraft accepts the handoff. | Spell lifecycle approval. |

## Input Contract

| Input | Required | Notes |
| --- | --- | --- |
| `tower_root` | yes | Folder created by `research-tower`; must include `FINAL-LEARNING-PACK.md` or an equivalent final pack. |
| `source_artifacts` | yes | Tower source record, claim ledger, definitions, glossary, notation, examples, or explicit external source paths. |
| `output_root` | yes | Target folder for package draft, source trace, PDF source, and rendered PDF. |
| `preset_id` | yes, selected interactively | One of `deep_voice_reading`, `quick_video`, `medium_explanation`, or a saved custom preset. |
| `reader_context` | yes, interviewed | Who the package teaches, what they already know, and what they should be able to do after reading. |
| `SCU core preferences` | yes, interviewed | Resonance, relevance, and trajectory cores refined through example choices. |
| `pdf_constraints` | optional | Page size, citation style, length cap, visual density, source appendix preference. |

## Output Contract

| Output | Owner | Required In L0 | Notes |
| --- | --- | --- | --- |
| `preset-profile.yaml` | reading-learning-package | yes | Selected preset plus user-specific core preferences and examples accepted/rejected. |
| `text-intent-substrate.yaml` | `whisper` via spell | yes | Whisper-compatible SCU substrate derived from tower and interview. |
| `composition-plan.md` | `whisper` via spell | yes | Sections, examples, source-use policy, PDF parts, and validation checklist. |
| `manuscript.md` | reading-learning-package | yes | Reading artifact assembled from source-backed content and Whisper plan. |
| `source-trace.md` | reading-learning-package | yes | Maps manuscript sections to tower/source artifacts and open residue. |
| `learning-package.html` | reading-learning-package | yes | Print-ready intermediate with styles and anchors. |
| `learning-package.pdf` | reading-learning-package | yes when renderer available; otherwise flagged | PDF rendering must have a deterministic command or a blocked renderer gap. |
| `validation-report.md` | reading-learning-package | yes | Checks source trace, preset fit, Whisper validation, PDF render, and no-promotion boundary. |

## Starter Presets

| Preset ID | Default Use | Length / Shape | Initial Bias | Must Ask |
| --- | --- | --- | --- | --- |
| `deep_voice_reading` | Long voice, in-depth explanations for careful reading or narration. | 4,000-8,000 words; chaptered PDF; optional narration notes. | Essayistic, patient, source-rich, explanatory. | Which voice feels alive without becoming performative? |
| `quick_video` | A short video-ready learning package plus compact PDF handout. | 60-180 second script; one-page source sheet; optional storyboard blocks. | Hook-first, compressed, concrete, high contrast. | What should the viewer remember after one minute? |
| `medium_explanation` | Balanced reading guide for someone who wants substance without a long essay. | 1,200-2,500 words; 5-8 pages; structured sections. | Clear, practical, concept-first. | What should be explained deeply, and what can stay in the appendix? |

Presets are not final templates. They are seed profiles improved through the
interview. The spell must preserve example-driven user choices as evidence in
`preset-profile.yaml`.

## Core Interview Model

The spell interviews the user through Whisper's three SCU cores:

| Core | Question Type | Required Evidence |
| --- | --- | --- |
| `resonance_core` | What should the learning package feel and sound like? | At least one accepted example and one rejected example. |
| `relevance_core` | Who is the reader/viewer, what do they know, and what reward do they need? | Reader state, assumed knowledge, and likely objection. |
| `trajectory_core` | What movement should the package perform? | Opening shape, learning sequence, ending/action, length. |

Each core interview should offer quick examples instead of asking abstract
preference questions alone. Example choices must be editable by the user.

## Non-Goals

- Do not rerun or mutate the tower unless missing required tower artifacts block
  source traceability.
- Do not promote tower vocabulary into canon.
- Do not claim source authority from a polished PDF.
- Do not treat quick-video output as an actual video renderer in L0.
- Do not require a specific PDF engine before the renderer capability is checked.

## Dispatch Technique Trace

| Technique | How It Shapes This Package |
| --- | --- |
| `sequence` | Tower evidence, preset interview, Whisper composition, PDF assembly, and validation run in order. |
| `route_menu` | Preset selection is a bounded menu with custom-preset escape hatch. |
| `artifact_contract_bridge` | Tower and Whisper output contracts become package artifacts and validation checks. |
| `handle_handoff` | Source artifacts are passed by path/handle, not copied into false authority. |
| `owner_boundary_check` | Invoke, Spellcraft, research-tower, Whisper, and Task Session authorities remain split. |
| `approval_semantics_map` | Preset/core preferences require user approval before drafting. |
| `validation_loop` | PDF, source trace, preset fit, and Whisper validation are checked before pass. |
| `residue_ledger` | Missing renderer, incomplete tower evidence, and unresolved voice choices stay visible. |
| `concrete_path_evidence` | Claims must cite tower/source paths. |

## Define Gate

Status: `pass-with-handoff`

Reason: the spell identity, input/output contracts, presets, interview model, and
owner boundaries are explicit. Spellcraft must own installation and lifecycle
validation.
