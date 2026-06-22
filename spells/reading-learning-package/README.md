# Reading Learning Package

Status: reusable spell candidate
Canonical id: `reading-learning-package`
Lifecycle owner: `spellcraft`

## Purpose

`reading-learning-package` composes a personalized learning package from a completed
`research-tower` result and source artifacts. It preserves tower evidence as
source authority, uses a Whisper-compatible text intent substrate for composition,
and emits traceable reading artifacts with HTML/PDF fallback behavior.

## Trigger Conditions

| Trigger | Route |
| --- | --- |
| User provides a tower root and asks for a readable learning package. | Run tower intake, preset/core interview, Whisper substrate bridge, package assembly, and validation. |
| User asks for a quick explainer or short video-ready package. | Use the `quick_video` preset and produce a script-shaped handout plus source sheet. |
| User wants long-form reading or narration. | Use the `deep_voice_reading` preset. |
| User wants a balanced guide. | Use the `medium_explanation` preset. |
| Tower evidence is missing. | Block before composition and report the missing source gate. |

## Modes

| Mode | Runtime command | Purpose |
| --- | --- | --- |
| `compose` | `python3 arcanum/spells/reading-learning-package/runtime/reading_learning_package.py compose ...` | End-to-end package creation. |
| `preset-interview` | `python3 arcanum/spells/reading-learning-package/runtime/reading_learning_package.py preset-interview ...` | Build a preset profile and preview without drafting the full package. |
| `validate-package` | `python3 arcanum/spells/reading-learning-package/runtime/reading_learning_package.py validate-package ...` | Validate an existing package output folder. |

## Required Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `tower_root` | yes | Must contain `FINAL-LEARNING-PACK.md` and claim evidence such as `tracks/paper-claim-ledger.md`. |
| `output_root` | yes | Receives package artifacts. |
| `preset_id` | yes | One of `deep_voice_reading`, `quick_video`, or `medium_explanation`. |
| `answers` | no | Optional JSON answer fixture or captured interview answers. Defaults are visible and recorded. |
| `source_artifacts` | no | Extra source handles; the tower final pack and claim ledger are always recorded when present. |

## Outputs

| Output | Required | Description |
| --- | --- | --- |
| `source-context.md` | yes | Tower/source handles and intake result. |
| `preset-profile.yaml` | yes | Preset choice, SCU core preferences, accepted/rejected examples, and approval state. |
| `preset-preview.md` | yes | Compact preview of voice, reader, movement, and output shape. |
| `text-intent-substrate.yaml` | yes | Whisper-compatible substrate; Whisper remains composition authority. |
| `composition-plan.md` | yes | Package structure, source-use policy, and validation checklist. |
| `manuscript.md` | yes | Reader-facing draft. |
| `source-trace.md` | yes | Claim-to-source mapping. |
| `learning-package.html` | yes | Print-ready HTML package. |
| `learning-package.pdf` | when renderer exists | Created only when a deterministic renderer succeeds. |
| `validation-report.md` | yes | Pass/flag/block result, renderer state, gates, residue, and next route. |

## Authority Boundaries

| Capability | Owns | Boundary |
| --- | --- | --- |
| `research-tower` | Final learning pack, claim ledger, definitions, notation, residue, and source authority. | This spell consumes tower artifacts by path/handle and does not rewrite tower evidence. |
| `whisper` | SCU cores, composition planning, drafting, validation, and learning residue. | This spell emits a compatible substrate and does not claim Whisper internals. |
| `reading-learning-package` | Orchestration, package artifacts, source trace, renderer fallback, and validation report. | Generated learning artifacts are not canonical source evidence. |
| `spellcraft` | Lifecycle validation and reusable spell readiness. | This package is a candidate until Spellcraft review accepts it. |

## Phase Contract

| Phase | Entry Criteria | Exit Criteria | Failure Behavior |
| --- | --- | --- | --- |
| Tower intake | `tower_root` supplied. | Final pack and claim evidence found, or a blocked gap is recorded. | Block on missing tower root, final pack, or claim evidence. |
| Preset selection | Source context available. | Preset id selected and defaults loaded. | Block on unknown preset. |
| Core interview | Preset selected. | Resonance, relevance, and trajectory cores include accepted/rejected examples. | Flag if answers are defaulted; block if core evidence is absent. |
| Whisper substrate | Preset profile approved. | Substrate records all SCU cores, source handles, and validation checks. | Block if substrate lacks source-use policy. |
| Package assembly | Composition plan ready. | Manuscript, source trace, HTML, and PDF or renderer gap exist. | Flag missing renderer; block unsupported source claims. |
| Validation | Outputs exist. | Validation report records pass/flag/block and no-promotion boundary. | Return residue and next route. |

## Gates

| Gate | Required Evidence | Result |
| --- | --- | --- |
| Source gate | Final pack and claim evidence exist. | pass/block |
| Preset gate | Preset profile records selected preset and examples. | pass/flag/block |
| Whisper gate | Substrate includes resonance, relevance, trajectory, source handles, and validation checks. | pass/block |
| Trace gate | Load-bearing manuscript sections map to source handles or residue. | pass/block |
| PDF gate | PDF exists or renderer gap is explicit while HTML exists. | pass/flag |
| Promotion gate | Package states it is learning output, not source authority. | pass/block |

## Observability Signals

| Signal | When Emitted |
| --- | --- |
| `reading_package_started` | Compose begins after source context is requested. |
| `source_context_ready` | Tower intake passes. |
| `preset_profile_approved` | Preset profile and preview are written. |
| `whisper_plan_ready` | Substrate and composition plan are written. |
| `pdf_rendered_or_flagged` | PDF stage exits with render or fallback. |
| `reading_package_validated` | Validation report is written. |

## Runtime Examples

Compose the synthetic medium fixture:

```bash
python3 arcanum/spells/reading-learning-package/runtime/reading_learning_package.py compose \
  --tower-root arcanum/spells/reading-learning-package/fixtures/demo-tower \
  --output-root arcanum/spells/reading-learning-package/validation/results/manual-medium \
  --preset medium_explanation \
  --answers arcanum/spells/reading-learning-package/fixtures/preset-answers/medium_explanation.json
```

Run the full fixture suite:

```bash
python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py
```

## Validation Examples

| Example | Expected Result |
| --- | --- |
| Valid tower with `medium_explanation` | Source context, preset profile, substrate, manuscript, source trace, HTML, and validation report. |
| Missing claim evidence | Block before composition. |
| `quick_video` preset | Script-shaped manuscript and compact handout HTML; no video rendering claim. |
| Renderer unavailable | `learning-package.html` exists, `learning-package.pdf` is absent, and validation report is `flag` with renderer gap. |

## Registry Readiness

Registry status: candidate.
Reusable readiness requires Spellcraft review after the fixture suite reports pass or acceptable flag.

## No-Promotion Rule

Generated manuscripts, HTML, PDFs, preset profiles, and validation reports are learning artifacts. They do not promote tower vocabulary, claims, or source records into canon.
