# Validation

- Latest report: `development/runs/20260722T131259Z.md` (local generated evidence)
- Status: flag
- Reason: one low-complexity runtime body exists; medium and complex runtime bodies plus registrar integration evidence are still missing.

## Checks

- Harness layout exists.
- Fixture pairs exist.
- Example prompts cover low, medium, and complex cases when applicable.
- Real outputs are not save summaries.
- Latest run report is linked after validation.

## Current Evidence

- Harness validation: pass.
- Profile validation: pass (`sigil-development`).
- Contract check: pass for the tracked low-complexity native output.
- Anti-Pattern hits: none in the low-complexity output.
- Workflow gaps: none in the low-complexity output.

## Promotion Blockers

- Run and preserve real medium and complex result bodies.
- Validate one consuming runtime profile end to end.
- Prove one dispatch event and one paired close event through a deterministic
  registrar.
- Regenerated Codex and Claude packages exist for the Arcanum checkout and its
  current consuming repository; personal runtime migration remains separate.
