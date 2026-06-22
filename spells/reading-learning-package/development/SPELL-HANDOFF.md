# Spell Handoff: reading-learning-package

## Spell Identity

- Name: Reading Learning Package
- Canonical ID: `reading-learning-package`
- Scope: reusable library spell candidate
- Owning surface: `arcanum/spells/reading-learning-package/`
- Observed authoring capability: `invoke`
- Lifecycle owner: `spellcraft`

## Purpose

Compose a personalized learning PDF from a completed research tower and source
artifacts by combining source-backed tower evidence with Whisper's composition
lifecycle and an example-driven preset interview.

## Trigger Conditions

| Trigger | User Signal | Route |
| --- | --- | --- |
| Create reading package from tower | User provides `tower_root` and asks for a readable/PDF learning artifact. | Run tower intake, preset interview, Whisper composition, PDF assembly. |
| Create quick explainer from tower | User asks for quick-video or short script from tower. | Use `quick_video` preset and produce script plus PDF handout. |
| Customize voice/reader profile | User asks to tune cores, voice, audience, or format. | Run preset interview preview before drafting. |
| Missing source evidence | Tower lacks final pack, claim ledger, or source record. | Block and route to `research-tower` repair/update. |

## Modes

| Mode | Purpose | Required Inputs | Outputs |
| --- | --- | --- | --- |
| `compose` | Main end-to-end package creation. | tower root, source artifacts, preset choice, core preferences, output root. | preset profile, substrate, plan, manuscript, source trace, HTML/PDF, validation. |
| `preset-interview` | Build or revise a preset profile without drafting full package. | preset seed, target reader, source/tower handles. | `preset-profile.yaml`, preview, approval status. |
| `validate-package` | Check existing package outputs. | output root and source handles. | validation report and residue. |
| `refresh-preset` | Update a saved preset from user feedback. | prior preset profile, new examples/comments. | revised preset profile and learning residue. |

## Required Sigils And Spells

| Capability | Type | Required | Notes |
| --- | --- | --- | --- |
| `research-tower` | sigil | yes | Supplies tower evidence and source boundaries; spell consumes artifacts by handle. |
| `whisper` | spell | yes | Supplies SCU cores, composition plan, drafting, validation, learning residue. |
| `structured-interview-kits` | sigil | yes | Runs one-question preset/core interview. |
| `distill` | sigil | yes | Validates smallest coherent package unit and recomposition. |
| `context-builder` | sigil | yes | Selects bounded tower/source context for Whisper. |

## Optional Capabilities

| Capability | Activation Rule | Notes |
| --- | --- | --- |
| `task-session` | Implementation or long draft work needs bounded execution. | Executes one SWU; does not own spell lifecycle. |
| `experiment-harness` | Reusable spell validation or preset fixtures are needed. | Required before promotion readiness. |
| `decision-gate` | Audience/objective/persistence choice blocks composition. | Route only consequential decisions. |
| `feature-glossary` | Package needs stable local vocabulary before drafting. | Useful when tower terms are dense or contested. |

## Shared State

| State Item | Owner | Persistence | Notes |
| --- | --- | --- | --- |
| `source_context` | reading-learning-package | per run | Paths and source-kind boundaries from tower/source artifacts. |
| `preset_profile` | reading-learning-package | per run; optionally saved | User-shaped preset and examples. |
| `text_intent_substrate` | whisper | per run | Whisper SCU substrate. |
| `composition_plan` | whisper | per run | Body parts and validation checklist. |
| `source_trace` | reading-learning-package | per output | Claim-to-source mapping. |
| `validation_report` | reading-learning-package | per output | Pass/flag/block checks. |
| `learning_residue` | whisper / spell | per run | Durable lessons, not canonical voice. |

## Phase Contract

| Phase | Entry Criteria | Exit Criteria | Failure Behavior |
| --- | --- | --- | --- |
| Tower intake | `tower_root` and source paths supplied. | Required source handles exist or gap is explicit. | Block on missing final pack or claim evidence. |
| Preset menu | Source context available. | Preset id selected or custom-from-examples selected. | Ask one menu question; no silent default if user is present. |
| Core interview | Preset id selected. | Resonance, relevance, and trajectory cores approved with examples. | Flag preview-only when a core is vague. |
| Whisper composition | Preset profile approved. | Substrate and composition plan produced. | Route consequential conflict to decision-gate. |
| Package assembly | Composition plan ready. | Manuscript, source trace, HTML, PDF or renderer gap. | Block unsupported claims; flag missing renderer. |
| Validation | Package outputs exist. | Validation report pass/flag/block. | Return residue and next route. |

## Gates

| Gate | Required Evidence | Result |
| --- | --- | --- |
| Source gate | Tower final pack, claim ledger or equivalent source evidence, source record or source-record gap. | pass/flag/block |
| Preset gate | Preset selected and user examples recorded. | pass/flag/block |
| Core gate | SCU cores complete and approved. | pass/flag/block |
| Whisper gate | Substrate and composition plan satisfy Whisper validation. | pass/flag/block |
| Trace gate | Load-bearing manuscript claims map to source handles or residue. | pass/block |
| PDF gate | PDF exists or renderer gap is explicit. | pass/flag |
| Promotion gate | Package states it is learning output, not canonical source authority. | pass/block |

## Observability

| Signal | When Emitted | Consumer |
| --- | --- | --- |
| `reading_package_started` | Tower intake begins. | Spellcraft / observability |
| `preset_profile_approved` | User approves preset/core preview. | Whisper / spell |
| `whisper_plan_ready` | Composition plan exists. | Package assembly |
| `pdf_rendered_or_flagged` | PDF stage exits. | Validation report |
| `reading_package_validated` | Final validation completes. | Spellcraft / reflection |

## Validation Examples

| Example | Expected Result |
| --- | --- |
| Valid tower + `medium_explanation` | Source context, preset profile, substrate, manuscript, source trace, HTML/PDF or renderer flag. |
| Missing final tower pack | Block before Whisper drafting. |
| `quick_video` with technical reader | Script plus compact PDF handout; no claim of video rendering. |
| User rejects all voice examples | Custom preset path asks for rewrite and returns preview-only flag until approved. |

## Registry Readiness

- Registry entry required: yes, after Spellcraft validation.
- Alias required: optional; candidate aliases could include `learning-pack`, `reading-pack`, `tower-to-pdf`.
- Documentation status: candidate.
- Experiment harness status: required before reusable promotion readiness.

## Spellcraft Handoff

- Handoff status: ready-with-flags.
- Handoff notes:
  - Install/adapt spell only after reviewing `DEFINE.md`, `DESIGN.md`,
    `PRESET-INTERVIEW.md`, `IMPLEMENTATION-LAYERING.md`, and `WORK-PACK.md`.
  - Do not copy full `research-tower` or `whisper` instructions into the spell.
  - Preserve `research-tower` as source authority and `whisper` as composition
    authority.
  - Treat PDF renderer selection and preset fixtures as implementation/validation
    gaps, not as blockers for design handoff.

## Gate Result

- Status: flag
- Reason: spell identity, phases, gates, capabilities, and handoff are explicit;
  runtime implementation and experiment fixtures remain downstream lifecycle work.
