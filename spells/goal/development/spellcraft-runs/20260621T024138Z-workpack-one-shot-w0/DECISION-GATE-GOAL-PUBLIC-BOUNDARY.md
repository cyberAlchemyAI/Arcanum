# Decision Gate: Goal Public-Boundary Repair

## Decision Gate Result

- Target scope: `arcanum/spells/goal` W0 public-boundary repair
- Result: PASS
- Decisions resolved: 1
- Blockers remaining: 0
- Decision artifact: `arcanum/spells/goal/development/spellcraft-runs/20260621T024138Z-workpack-one-shot-w0/DECISION-GATE-GOAL-PUBLIC-BOUNDARY.md`
- Deferred decisions: runtime source/write scope remains deferred until W0 passes.
- Assumptions recorded: public `arcanum` carries generic contracts and schemas only; the private root repository carries the filled schema instance.
- Validation: approval token and public-boundary repair validation required after apply.
- Next step: proceed with the approved staged repair.

## Selected Decision

The user selected the public/private split policy on 2026-06-21: public
`arcanum` should contain only generic spell contracts, public schemas, neutral
defaults, opaque handles, and public-safe development evidence. The consuming
root repository owns the filled decision-profile instance.

Decision record: `DECISION-RECORD-GOAL-PUBLIC-BOUNDARY-001.md`

Approval token: `APPROVAL-TOKEN-GOAL-PUBLIC-BOUNDARY-001.json`

## Blocker Decision

Question: How should the public goal spell package repair the private
provenance/profile literals and stale Craft state?

### Option 1 - Approve Staged Public-Boundary Repair (Recommended)

- Benefit: Unblocks W0 by removing private local provenance from public
  artifacts and syncing authored-artifact state.
- Cost or risk: Mutates the Craft ledger and human view, so it must be reviewed
  as the exact staged batch.
- When to choose: Choose this if the public spell package should be clean and
  self-contained before runtime SWUs.
- Downstream impact: After apply and validation, W1 runtime skeleton work can
  proceed.

### Option 2 - Keep Private Provenance In Craft State

- Benefit: Preserves current provenance detail exactly.
- Cost or risk: Keeps W0 blocked because the public spell package continues to
  contain private path/profile literals.
- When to choose: Choose only if public-boundary policy is intentionally being
  relaxed for this package.
- Downstream impact: Runtime SWUs remain blocked by the current goal boundary.

### Option 3 - Move Provenance To A Private Parent Artifact Later

- Benefit: Avoids active Craft mutation now while preserving a path for private
  provenance outside the public submodule.
- Cost or risk: W0 remains blocked until the private artifact exists and public
  Craft state is scrubbed.
- When to choose: Choose if the repair should be split into a private-parent
  handoff first.
- Downstream impact: The work-pack goal pauses before W1.

### Explain / More Context

This option does not resolve the gate. Ask for more context if you want the
source evidence and downstream consequences expanded before choosing one of the
real options.

## Recommendation

Choose Option 1. It is the smallest repair that satisfies the existing
public/private boundary and keeps the full work-pack stream moving without
weakening approval semantics.
