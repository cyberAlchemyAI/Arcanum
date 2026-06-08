---
template_id: invoke.refresh
template_type: refresh
applies_to:
  - refresh
required_inputs:
  - source_evidence
  - target_artifact_inventory
  - refresh_scope
  - evidence_date
  - mutation_mode
optional_inputs:
  - source_session_reference
  - known_blocker_ids
  - expected_next_route
  - apply_approval
output_files:
  - REFRESH-REPORT.md
  - refresh-report.json
  - REFRESH-PATCH-PROPOSAL.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - source evidence present
  - target artifact inventory present
  - every delta maps to a refresh signal
  - apply-approved requires explicit approval
  - no-op can pass without patch proposal
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-25
updated_at: 2026-05-25
---

# Refresh Report: {refresh-title}

## Identity

- Source session reference: `{source-session-reference-or-none}`
- Evidence date: `{yyyy-mm-dd}`
- Refresh scope: `{scope}`
- Mutation mode: `{proposal-only | apply-approved}`
- Target lifecycle owner: `{owner}`

## Source Signals

| Signal ID | Type | Source | Claim | Confidence | Mutation Safety |
| --- | --- | --- | --- | --- | --- |
| `{signal-id}` | `{evidence_added | blocker_opened | blocker_resolved | status_changed | route_changed | artifact_drift | no_op}` | `{path#selector}` | `{claim}` | `{high | medium | low}` | `{safe | needs_review | blocked}` |

## Target Artifact Inventory

| Artifact | Owner | Current Claim | Refresh Relevance |
| --- | --- | --- | --- |
| `{path}` | `{owner}` | `{current-state}` | `{why inspected}` |

## Delta Summary

| Delta | Target Artifact | Proposed State | Evidence |
| --- | --- | --- | --- |
| `{delta-class}` | `{path}` | `{state}` | `{signal-id}` |

## Proposed Changes

- `{change proposal or none}`

## Applied Changes

- `{applied change or n/a}`

## Skipped Changes

| Candidate Change | Reason Skipped |
| --- | --- |
| `{candidate}` | `{reason}` |

## Blockers And Gaps

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| `{gap}` | `{owner}` | `{open | deferred | blocked | resolved}` | `{action}` |

## Validation

- `{command or review check}`

## Next Route

- Recommended route: `{task-session | workflow-reflect | invoke plan | deferred}`
- Rationale: `{why}`

## Gate Result

- Status: `{pass | flag | block | no-op}`
- Reason: `{gate-result-summary}`
