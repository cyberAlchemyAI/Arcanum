# Reading Learning Package Fixture Report

Generated: 2026-06-23T03:52:27Z

Overall status: `pass`

| Fixture | Check | Result |
| --- | --- | --- |
| deep_voice_reading | compose | pass |
| deep_voice_reading | validate-package | pass |
| quick_video | compose | pass |
| quick_video | validate-package | pass |
| medium_explanation | compose | pass |
| medium_explanation | validate-package | pass |
| missing-source | source gate blocks | pass |

## Evidence

- Preset variants: `deep_voice_reading`, `quick_video`, `medium_explanation`.
- Valid tower fixture: `arcanum/spells/reading-learning-package/fixtures/demo-tower`.
- Missing-source fixture: `arcanum/spells/reading-learning-package/fixtures/missing-tower`.
- Output root: `arcanum/spells/reading-learning-package/validation/results/outputs`.
- HTML/PDF fallback: validation reports flag renderer gaps when no deterministic renderer is available.
- No-promotion boundary: validation reports keep generated learning output separate from source authority.

## Failures

- none
