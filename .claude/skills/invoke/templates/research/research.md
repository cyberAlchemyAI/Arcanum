---
template_id: invoke.research
template_type: research
applies_to:
  - define
  - design
  - plan
required_inputs:
  - research_question
  - scope_boundary
  - source_scope
optional_inputs:
  - prior_findings
  - excluded_sources
  - confidence_threshold
output_files:
  - RESEARCH.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - research question present
  - source scope present
  - evidence table populated
  - contradictions recorded
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# Research Brief: {topic}

## Research Question

{question to answer}

## Scope Boundaries

- Included: {included scope}
- Excluded: {excluded scope}
- Evidence boundary: {repository-only | external allowed | mixed}

## Source Plan

| Source Type | Selection Rule | Minimum Count |
| --- | --- | --- |
| repository artifact | {rule} | {count} |
| external source | {rule or out of scope} | {count} |

## Source Ledger

| Source ID | Source | Status | Notes |
| --- | --- | --- | --- |
| S-001 | {path, URL, or citation} | selected | {notes} |

## Evidence Table

| Evidence ID | Source ID | Claim | Support Level | Notes |
| --- | --- | --- | --- | --- |
| E-001 | S-001 | {claim} | supports, contradicts, or uncertain | {notes} |

## Contradictions

| Conflict ID | Evidence IDs | Summary | Resolution |
| --- | --- | --- | --- |
| C-001 | E-001, E-002 | {conflict} | {resolved, unresolved, deferred} |

## Claim Status

| Claim | Status | Confidence | Reason |
| --- | --- | --- | --- |
| {claim} | supported, partial, unsupported, or unknown | low, medium, or high | {reason} |

## Synthesis

{concise synthesis grounded in evidence}

## Unresolved Gaps

| Gap ID | Gap | Impact | Next Step |
| --- | --- | --- | --- |
| G-001 | {gap} | {impact} | {next step} |

## Decision Options

| Option | Evidence Basis | Trade-Off |
| --- | --- | --- |
| {option} | {evidence IDs} | {trade-off} |

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}