# Validation Report

Generated: 2026-06-23T03:52:26Z

Overall status: `flag`

Preset: `quick_video`

| Gate | Result | Evidence |
| --- | --- | --- |
| Source gate | pass | `source-context.md` |
| Preset gate | pass | `preset-profile.yaml` and `preset-preview.md` |
| Whisper gate | pass | `text-intent-substrate.yaml` and `composition-plan.md` |
| Trace gate | pass | `source-trace.md` |
| PDF gate | flag | no deterministic PDF renderer found; HTML fallback emitted |
| Promotion gate | pass | Generated package is labelled learning output, not source authority. |

## Missing Required Outputs

- none

## Residue

- PDF renderer status: no deterministic PDF renderer found; HTML fallback emitted
- Source authority remains with `research-tower`.
- Composition authority remains with `whisper`.
