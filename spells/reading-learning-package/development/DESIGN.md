---
title: Reading Learning Package Design
status: draft
updatedAt: 2026-06-20
owner: Arcanum maintainers
scope: spell-design
observedCapability: invoke
targetLifecycleOwner: spellcraft
---

# Reading Learning Package Design

## Design Intent

The spell composes a source-backed learning artifact from an existing tower. It
keeps research authority and writing authority separate:

```text
research-tower evidence
  -> source handles and claim boundaries
  -> preset interview
  -> Whisper text intent substrate
  -> composition plan
  -> manuscript and source trace
  -> PDF assembly
  -> validation and residue
```

## Context View

| Actor | Need | Constraint |
| --- | --- | --- |
| User/operator | Turn a tower result into a learning PDF without manually re-summarizing everything. | Wants preference-sensitive presets, not generic templates. |
| Reader/viewer | Receive a package matched to length, voice, and learning goal. | Must be able to trust source-backed claims. |
| Spell runner | Compose tower evidence, Whisper output, and PDF assembly. | Must preserve owner boundaries and traceability. |
| Spellcraft | Convert this development package into an installed spell if accepted. | Must validate phases, gates, observability, and experiment harness. |

## High-Level Structure View

| Component | Responsibility | Owner |
| --- | --- | --- |
| Tower intake | Verify required tower/source artifacts and source-kind boundaries. | `research-tower` / spell adapter |
| Preset interview | Select and customize preset through examples and SCU cores. | `structured-interview-kits` / spell |
| Whisper substrate | Convert preset, reader, and source handles into SCU substrate. | `whisper` |
| Composition planner | Produce reading/script/manuscript plan from selected preset. | `whisper` |
| Manuscript builder | Assemble source-backed reading package draft. | spell runtime |
| PDF assembler | Render Markdown/HTML into PDF and record renderer evidence. | spell runtime / `task-session` implementation |
| Validator | Check source trace, preset fit, PDF artifact, and no-promotion boundary. | spell runtime / Spellcraft validation |

## Low-Level Components View

| Artifact | Format | Required Fields |
| --- | --- | --- |
| `preset-profile.yaml` | YAML | preset id, tower root, source paths, SCU cores, examples accepted/rejected, PDF preferences, approval. |
| `text-intent-substrate.yaml` | YAML | Whisper resonance/relevance/trajectory cores, transport schema, validation checks. |
| `composition-plan.md` | Markdown | body parts, source-use rules, examples, ending, PDF sections, validation checklist. |
| `manuscript.md` | Markdown | title, reading body, examples, source notes, open residue appendix. |
| `source-trace.md` | Markdown table | manuscript section, source artifact, source kind, claim status, residue. |
| `learning-package.html` | HTML | print-ready content, stable section anchors, source appendix. |
| `learning-package.pdf` | PDF | rendered output; required when renderer exists. |
| `validation-report.md` | Markdown | pass/flag/block checks and gaps. |

## Workflow Process View

| Phase | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- |
| 1. Tower intake | `tower_root`, `source_artifacts` | `source-context.md` or blocked gap | Required tower files and source handles exist. | Block and route to `research-tower` repair when final pack or claim evidence is missing. |
| 2. Preset selection | Source context | selected preset id | User selects preset or custom-from-examples. | Ask one menu question; block only if no output target is identifiable. |
| 3. Core interview | selected preset | `preset-profile.yaml` | Resonance, relevance, trajectory each have accepted/rejected example evidence. | Return `flag` with preview-only if a core remains vague. |
| 4. Whisper composition | preset profile, source context | substrate and composition plan | Whisper validation checklist exists and cites source handles. | Route to `decision-gate` for consequential audience/objective conflict. |
| 5. Manuscript/PDF assembly | composition plan | Markdown, HTML, PDF or renderer gap | Source trace covers load-bearing claims; renderer command is deterministic. | If renderer unavailable, produce HTML/Markdown and flag PDF render gap. |
| 6. Validation/residue | all outputs | validation report | Preset fit, source trace, no-promotion, and PDF checks pass or flag. | Block on unsupported source claims; flag on stylistic or renderer gaps. |

## Decision Flow View

```text
Is tower/source evidence complete?
  no -> research-tower repair / source-context gap
  yes -> ask preset menu

Preset chosen?
  no -> custom_from_examples with two previews
  yes -> run SCU core interview

Cores approved?
  no -> preview-only flag or ask next core question
  yes -> Whisper substrate and composition plan

Renderer available?
  yes -> render PDF and validate
  no -> emit Markdown/HTML plus flagged PDF gap

Unsupported claim found?
  yes -> block or move claim to residue/source appendix
  no -> package pass/flag based on preset fit and PDF evidence
```

## Dependency Interface View

| Dependency | Interface | Boundary |
| --- | --- | --- |
| `research-tower` | Consume tower artifacts by path: final pack, claim ledger, glossary, definitions, notation, source record, open residue. | Does not rewrite tower unless repair route is explicitly invoked. |
| `whisper` | Provide `text_intent_substrate`, candidate selection, composition plan, draft/validation. | Does not claim source authority. |
| `structured-interview-kits` | One-question cadence with example choices and approval capture. | Does not silently choose user voice preferences. |
| `distill` | Validate smallest coherent package unit and recomposition into preset output. | Does not replace Whisper composition. |
| `task-session` | Execute bounded renderer/manuscript implementation SWUs after Spellcraft accepts package. | Does not own spell lifecycle. |
| `experiment-harness` | Validate reusable examples across presets before promotion readiness. | Blocks broad reuse if absent. |

## Preset Transport Contracts

| Preset | Whisper Transport Interpretation | PDF Shape |
| --- | --- | --- |
| `deep_voice_reading` | Long-form explanatory reading/narration manuscript. | Chaptered PDF with source appendix and optional narration notes. |
| `quick_video` | Short explainer script plus compact learning handout. | One-page or short PDF containing script, storyboard beats, and source sheet. |
| `medium_explanation` | Medium guide with practical examples. | 5-8 page PDF with sections, examples, and next-reading appendix. |

## Validation Strategy

| Check | Pass Evidence |
| --- | --- |
| Tower evidence | Required paths exist; missing source evidence is flagged before drafting. |
| Preset interview | `preset-profile.yaml` records selected preset and example-based core choices. |
| Whisper fit | `text-intent-substrate.yaml` and `composition-plan.md` include SCU cores and validation checks. |
| Source trace | Every load-bearing claim in `manuscript.md` maps to tower/source artifact or residue. |
| PDF render | Deterministic command produces `learning-package.pdf`, or renderer gap is explicit. |
| No promotion | Output states it is a learning package, not canonical source authority. |

## Distill Validation

Verdict: `pass-with-flag`

Smallest coherent unit: one preset-customized learning package from one tower
root and source artifact set.

Recomposition proof: the SCU recomposes into the requested spell because it
contains tower intake, preset interview, Whisper composition, PDF assembly, and
validation. The flag is that actual renderer choice and experiment-harness
fixtures remain implementation work.

## Open Design Gaps

| Gap | Owner | Repair Route |
| --- | --- | --- |
| PDF renderer selection is environment-dependent. | Spellcraft / Task Session | First SWU checks `pandoc`, browser print, or local HTML-to-PDF fallback. |
| No reusable examples exist yet for all three presets. | Experiment Harness | Add fixtures after spell contract draft exists. |
| Saved custom presets need persistence policy. | Spellcraft | Decide whether local presets live under output root, `.arcanum`, or spell state. |
