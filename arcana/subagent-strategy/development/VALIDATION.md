# Validation

- Latest deterministic maintenance run: `2026-07-28`
- Prior live report: `development/runs/20260722T131259Z.md` (local generated evidence)
- Status: flag
- Reason: schema 0.8.0 now closes pair evidence, identity, and approver
  admission before one confirmation request, but the first repaired live
  dispatch and preserved medium and complex runtime bodies are still missing.

## Checks

- Harness layout exists.
- Fixture pairs exist.
- Example prompts cover low, medium, and complex cases when applicable.
- Real outputs are not save summaries.
- Latest run report is linked after validation.

## Current Evidence

- Harness validation: pass.
- Profile validation: pass (`sigil-development`).
- Confirmation-readiness fixtures: pass for stale form-version warning,
  unpooled approver rejection, companion-only tension-evidence rejection,
  complete canonical pair coverage, and exactly one normal confirmation
  request.
- Stage-handoff readiness fixture: pass for `needs_feedback`, repair-owner
  routing, declared-edge enforcement, and preservation of downstream revision
  capacity.
- Registrar readiness tests: pass (`125` cases), including exact digest output,
  no ledger mutation, schema 0.8.0 pair coverage, pool eligibility, identity
  uniqueness, approver admission, reserved-type rejection, grandfathering,
  and post-confirmation mutation rejection. The battery requires an
  unrestricted child-process environment; the in-sandbox nested-spawn result
  is not product evidence.
- Runtime composition: pass (`34` cases) for public core plus declared DomainSpec
  Codex and Claude overlays.
- Contract check: pass for the tracked low-complexity native output.
- Anti-Pattern hits: none in the low-complexity output.
- Workflow gaps: none in the low-complexity output.
- Required observer pass: `severe-gap`; it identified incomplete composite
  readiness, companion-only Test 4 evidence, approval-contract drift, stale
  gate vocabulary, and an impossible checker/reviewer sequencing rule.
- Incident fixture: the prior unpooled-approver and companion-evidence shape is
  now rejected before confirmation. This is deterministic evidence, not a live
  dispatch receipt.
- Runtime deployment: regenerated Codex and Claude packages match their
  canonical sources; the explicitly requested personal Codex
  `domainspec-subagents-strategy` copy matches the generated Codex overlay.

## Promotion Blockers

- Run and preserve real medium and complex result bodies.
- Validate one consuming runtime profile end to end.
- Preserve one repaired research run where the type owner returns
  `needs_feedback`, the declared explorer route supplies the missing binding,
  and the rechecked handoff returns `ready`.
- Prove one schema 0.8.0 post-repair dispatch event and one paired close event
  through the deterministic registrar without an avoidable second
  confirmation.
