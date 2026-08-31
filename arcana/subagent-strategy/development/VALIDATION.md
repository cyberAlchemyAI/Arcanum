# Validation

- Latest deterministic maintenance run: `2026-08-26`
- Prior live report: `development/runs/20260722T131259Z.md` (local generated evidence)
- Status: flag
- Reason: the DomainSpec-derived temporary-JSON to append-only-YAML registrar
  is implemented, but a migrated historical ledger and a live end-to-end
  register/run/close execution are still missing.

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
- Exact-sheet confirmation fixture: pass for refreshed exact-byte machine
  gates, confirmation invalidation after any byte change, and required
  reconfirmation before registration.
- Stage-handoff readiness fixture: pass for `needs_feedback`, repair-owner
  routing, declared-edge enforcement, and preservation of downstream revision
  capacity.
- Default registrar battery: pass (`94` cases) for strict v0.6.1 dispatch and
  close validation, JSON-column YAML emission, structural self-check,
  grandfathering, idempotency, exact sheet digest, non-mutating `--check`,
  governed `--consume`, failure preservation, and temp-path containment.
- Runtime composition evidence predating v0.4.0 is historical and does not
  validate the new exact-sheet/YAML lifecycle.
- Contract check: pass for the tracked low-complexity native output.
- Anti-Pattern hits: none in the low-complexity output.
- Workflow gaps: none in the low-complexity output.
- Required observer pass: `severe-gap`; it identified incomplete composite
  readiness, companion-only Test 4 evidence, approval-contract drift, stale
  gate vocabulary, and an impossible checker/reviewer sequencing rule.
- Incident fixture: the prior unpooled-approver and companion-evidence shape is
  now rejected before confirmation. This is deterministic evidence, not a live
  dispatch receipt.
- Byte-change incident fixture: mechanically changed bytes rerun all machine
  gates and invalidate the prior confirmation. This is deterministic evidence,
  not a live dispatch receipt.
- Runtime deployment: regenerated Codex and Claude packages match their
  canonical sources; the explicitly requested personal Codex
  `domainspec-subagents-strategy` copy matches the generated Codex overlay.

## Promotion Blockers

- Run and preserve real medium and complex result bodies.
- Validate one consuming runtime profile end to end.
- Preserve one repaired research run where the type owner returns
  `needs_feedback`, the declared explorer route supplies the missing binding,
  and the rechecked handoff returns `ready`.
- Prove one v0.6.1 confirmed dispatch row and one paired close row through the
  deterministic registrar with both temporary JSON records consumed.
- Import the eligible current per-topic JSON/JSONL lifecycle evidence into the
  central YAML ledger without rewriting or deleting historical sources.
- Integrate registrar admission with the native orchestration path so no host
  spawn can precede a confirmed YAML dispatch row.
