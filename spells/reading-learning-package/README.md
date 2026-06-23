# Reading Learning Package

Status: reusable spell
Canonical id: `reading-learning-package`
Aliases: none
Scope: library
Lifecycle owner: `spellcraft`

## Purpose

`reading-learning-package` composes a personalized learning package from a completed
`research-tower` result and source artifacts. It preserves tower evidence as
source authority, uses a Whisper-compatible text intent substrate for composition,
and emits traceable reading artifacts with HTML/PDF fallback behavior.

## Required Sigils

| Sigil | Role |
| --- | --- |
| `research-tower` | Supplies the completed learning pack, claim ledger, source records, definitions, notation, and residue that remain source authority. |
| `whisper` | Owns text-intent substrate interpretation, SCU core composition, manuscript shaping, and composition-quality validation. |

## Optional Sigils

| Sigil | Use When |
| --- | --- |
| `experiment-harness` | Reusable spell behavior needs fixture-backed validation, validation reports, or telemetry-ready examples. |
| `task-session` | Runtime implementation, renderer integration, or package repair needs a bounded executable work unit. |
| `codex-goal-profile` | A bounded implementation or validation SWU should be converted into one native Codex `/goal` handoff. |

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

## Prerequisites

- Python 3 is available for the stdlib runtime and fixture runner.
- `tower_root` points to a completed tower-like source package with
  `FINAL-LEARNING-PACK.md`.
- Claim evidence exists under the tower, normally
  `tracks/paper-claim-ledger.md`.
- `output_root` is writable and isolated from canonical source artifacts.
- The selected preset exists in `runtime/presets.json`.
- PDF rendering is optional; when no deterministic renderer is available, HTML
  fallback plus a renderer gap is valid.

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

## Shared State

| State | Producer | Consumer |
| --- | --- | --- |
| `source-context.md` | Tower intake | Preset selection, source trace, validation |
| `preset-profile.yaml` | Preset selection and core interview | Whisper substrate and package assembly |
| `preset-preview.md` | Preset selection | Human review and validation evidence |
| `text-intent-substrate.yaml` | Whisper substrate bridge | Package assembly and Whisper-compatible review |
| `composition-plan.md` | Whisper substrate bridge | Manuscript, HTML, source trace, validation |
| `source-trace.md` | Package assembly | Trace gate and no-promotion boundary |
| `validation-report.md` | Validation | Spellcraft review, experiment harness, and follow-up routing |

## Authority Boundaries

| Capability | Owns | Boundary |
| --- | --- | --- |
| `research-tower` | Final learning pack, claim ledger, definitions, notation, residue, and source authority. | This spell consumes tower artifacts by path/handle and does not rewrite tower evidence. |
| `whisper` | SCU cores, composition planning, drafting, validation, and learning residue. | This spell emits a compatible substrate and does not claim Whisper internals. |
| `reading-learning-package` | Orchestration, package artifacts, source trace, renderer fallback, and validation report. | Generated learning artifacts are not canonical source evidence. |
| `spellcraft` | Lifecycle validation, reusable spell readiness, and promotion receipts. | This package is reusable once registry, generated surface, and validation evidence pass. |

## Handoff Artifacts

| Handoff | Artifact | Receiving Owner |
| --- | --- | --- |
| Tower source intake | `source-context.md` plus referenced tower paths | `reading-learning-package` |
| Whisper composition bridge | `text-intent-substrate.yaml` and `composition-plan.md` | `whisper` review or downstream composition work |
| Reader package output | `manuscript.md`, `learning-package.html`, optional `learning-package.pdf` | Human reader or publication workflow |
| Validation receipt | `validation-report.md` and `validation/results/fixture-report.md` | `spellcraft` and `experiment-harness` |
| Runtime repair route | validation residue and renderer gap | `task-session` or `codex-goal-profile` when executable work is needed |

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

## Failure Policy

- Return `block` when the tower root, final pack, claim evidence, preset, source
  policy, or trace mapping is missing.
- Return `flag` when the package is useful but carries non-blocking residue,
  especially deterministic PDF renderer absence.
- Return `pass` only when source, preset, Whisper substrate, trace, fallback,
  and no-promotion gates are satisfied.
- Do not promote generated learning text, HTML, PDF, preset profiles, or
  validation reports into tower source authority.
- Route runtime implementation or renderer integration through `task-session`;
  route reusable behavior proof through `experiment-harness`.

## Local Customization

Consuming repositories may customize preset defaults, answer capture, renderer
adapter selection, output roots, and validation strictness. They must not rewrite
`research-tower` or `whisper` contracts from this spell. Local installations should
adapt paths under `.arcanum/spells/reading-learning-package/` while preserving the
source-authority and no-promotion boundaries.

## Observability

Reusable runs should preserve the selected preset, source gate result, Whisper
substrate status, renderer result, validation status, residue, and next route.
When repository observability is available, emit the following spell-level
signals.

| Signal | When Emitted |
| --- | --- |
| `reading_package_started` | Compose begins after source context is requested. |
| `source_context_ready` | Tower intake passes. |
| `preset_profile_approved` | Preset profile and preview are written. |
| `whisper_plan_ready` | Substrate and composition plan are written. |
| `pdf_rendered_or_flagged` | PDF stage exits with render or fallback. |
| `reading_package_validated` | Validation report is written. |

## Experiment Harness

Current fixture harness:

- Runner: `validation/run-fixtures.py`
- Report: `validation/results/fixture-report.md`
- Presets covered: `deep_voice_reading`, `quick_video`, `medium_explanation`
- Negative fixture: missing source evidence blocks before composition
- Expected renderer behavior: HTML exists; PDF absence is a `flag` with an
  explicit renderer gap, not a failed package

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

Registry status: promoted in `registry/SPELLS.md`.
Reusable readiness is backed by Spellcraft review, fixture evidence, generated
runtime surface validation, and a promotion receipt. The current public-safe
fixture suite reports overall `pass` with expected renderer fallback flags in
per-package validation reports.

## Output Contract

Return:

```markdown
## Reading Learning Package Result

- Mode: compose | preset-interview | validate-package
- Spell: reading-learning-package
- Preset: <deep_voice_reading | quick_video | medium_explanation>
- Status: pass | flag | block
- Source context: <path>
- Preset profile: <path>
- Whisper substrate: <path>
- Composition plan: <path>
- Manuscript: <path>
- Source trace: <path>
- HTML package: <path>
- PDF package: <path | renderer gap>
- Validation report: <path>
- Residue: <renderer/source/trace gaps or none>
- Next route: spellcraft | experiment-harness | task-session | none
```

## No-Promotion Rule

Generated manuscripts, HTML, PDFs, preset profiles, and validation reports are learning artifacts. They do not promote tower vocabulary, claims, or source records into canon.
