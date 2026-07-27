# Validation

- Latest deterministic maintenance run: `2026-07-27`
- Prior live report: `development/runs/20260722T131259Z.md` (local generated evidence)
- Status: flag
- Reason: confirmation-readiness is now covered deterministically, but the first
  repaired live dispatch and preserved medium and complex runtime bodies are
  still missing.

## Checks

- Harness layout exists.
- Fixture pairs exist.
- Example prompts cover low, medium, and complex cases when applicable.
- Real outputs are not save summaries.
- Latest run report is linked after validation.

## Current Evidence

- Harness validation: pass.
- Profile validation: pass (`sigil-development`).
- Confirmation-readiness fixture: pass for stale form-version warning and block
  before the human gate.
- Stage-handoff readiness fixture: pass for `needs_feedback`, repair-owner
  routing, declared-edge enforcement, and preservation of downstream revision
  capacity.
- Registrar readiness tests: pass (`111` cases), including exact digest output,
  no ledger mutation, reserved-type rejection, and no-self-approval rejection.
- Runtime composition: pass (`26` cases) for public core plus declared DomainSpec
  Codex and Claude overlays.
- Contract check: pass for the tracked low-complexity native output.
- Anti-Pattern hits: none in the low-complexity output.
- Workflow gaps: none in the low-complexity output.
- Live pending-sheet probe: correctly blocked before confirmation because the
  working auditor is also named as final approver. The sheet was not repaired,
  confirmed, registered, or dispatched during maintenance.

## Promotion Blockers

- Run and preserve real medium and complex result bodies.
- Validate one consuming runtime profile end to end.
- Preserve one repaired research run where the type owner returns
  `needs_feedback`, the declared explorer route supplies the missing binding,
  and the rechecked handoff returns `ready`.
- Prove one post-repair dispatch event and one paired close event through the
  deterministic registrar without an avoidable second confirmation.
- Regenerated Codex and Claude packages exist for the Arcanum checkout and its
  current consuming repository; personal runtime migration remains separate.
