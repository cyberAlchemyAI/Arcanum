---
template_id: invoke.generic
template_type: generic
applies_to:
  - define
  - design
  - plan
required_inputs:
  - goal
  - scope
  - source_evidence
  - output_depth
optional_inputs:
  - constraints
  - existing_artifacts
  - preferred_next_route
output_files:
  - GENERIC.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - required inputs present
  - specialized-family eligibility checked
  - unresolved gaps recorded
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# Generic Invoke Artifact: {artifact-name}

## Objective

Describe the outcome this artifact must make possible.

## Scope

- In scope: {included responsibilities}
- Out of scope: {excluded responsibilities}
- Target user or operator: {actor}

## Source Evidence

| Evidence ID | Source | Relevance |
| --- | --- | --- |
| E-001 | {path or note} | {why this source matters} |

## Specialized Family Eligibility

| Family | Eligible | Rationale |
| --- | --- | --- |
| research | yes or no | {reason} |
| architecture | yes or no | {reason} |
| implementation-plan | yes or no | {reason} |
| spell | yes or no | {reason} |
| sigil | yes or no | {reason} |
| ux-plan | yes or no | {reason} |

## Output Depth

- Requested depth: {brief | standard | detailed}
- Selected depth: {brief | standard | detailed}
- Selection rationale: {why this depth fits}

## Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| {criterion} | {evidence path or check} |

## Open Gaps

| Gap ID | Description | Severity | Next Action |
| --- | --- | --- | --- |
| G-001 | {gap} | low, medium, or high | {next action} |

## Next Route

- Recommended route: {research | architecture | implementation-plan | spellcraft | sigil-development | deferred}
- Reason: {route rationale}

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}