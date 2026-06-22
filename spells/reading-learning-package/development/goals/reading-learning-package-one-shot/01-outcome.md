# Outcome

## Selected Stream

- Source work-pack: [../../WORK-PACK.md](../../WORK-PACK.md)
- Selected one-shot stream: `RLP-FULL-SPELL-ONE-SHOT`
- Ordered units: `SWU-RLP-001` through `SWU-RLP-009`
- One-shot mode: yes
- Handoff pack: [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RESULT.md](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RESULT.md)
- Handoff index: [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/evidence-index.json](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/evidence-index.json)

## Required Outcome

Implement and test the complete `reading-learning-package` spell as a reusable candidate under `arcanum/spells/reading-learning-package/`.

The spell should turn a completed `research-tower` result plus source artifacts into a reader-facing learning package with:

- source intake and gap behavior,
- preset selection and example-driven core interview,
- `preset-profile.yaml`,
- Whisper-compatible `text-intent-substrate.yaml`,
- `composition-plan.md`,
- `manuscript.md`,
- `source-trace.md`,
- `learning-package.html`,
- `learning-package.pdf` when renderer evidence exists or an explicit renderer-gap flag when it does not,
- `validation-report.md`,
- preset fixtures for `deep_voice_reading`, `quick_video`, and `medium_explanation`.

## Ordered Scope

| Order | Unit | Required outcome |
| --- | --- | --- |
| 1 | `SWU-RLP-001` | Candidate Spellcraft contract exists without copying full sigil bodies. |
| 2 | `SWU-RLP-002` | Tower/source intake blocks missing required evidence and emits source-context handles for valid input. |
| 3 | `SWU-RLP-003` | Preset-profile schema and starter presets exist and parse. |
| 4 | `SWU-RLP-004` | One-question preset menu and example-driven SCU interview record accepted/rejected evidence. |
| 5 | `SWU-RLP-005` | Preset profile bridges into Whisper text intent substrate with all SCU cores. |
| 6 | `SWU-RLP-006` | Composition plan, manuscript, and source trace are assembled from source handles. |
| 7 | `SWU-RLP-007` | HTML/PDF assembly renders PDF or emits HTML plus explicit renderer gap. |
| 8 | `SWU-RLP-008` | Fixtures cover deep, quick, and medium preset outputs. |
| 9 | `SWU-RLP-009` | Final validation reports pass/flag/block and no-promotion boundaries. |

## Completion Definition

The one-shot goal is complete only when the implementation artifacts, fixtures, and validation reports prove all ordered units above, or when a `BLOCK` report explains the exact unmet gate and next input.
