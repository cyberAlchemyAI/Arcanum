---
template_id: invoke.sigil
template_type: sigil
applies_to:
  - define
  - design
  - full
required_inputs:
  - sigil_identity
  - purpose
  - inputs
  - outputs
optional_inputs:
  - modes
  - runtime_adapter_expectations
  - observability
  - validation_examples
output_files:
  - SIGIL-HANDOFF.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - sigil identity present
  - purpose present
  - inputs and outputs explicit
  - sigil-development handoff recorded
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# Sigil Handoff: {sigil-name}

## Sigil Identity

- Name: {sigil-name}
- Purpose: {purpose}
- Owning surface: {directory or registry location}

## Inputs

| Input | Required | Validation Rule |
| --- | --- | --- |
| {input} | yes or no | {rule} |

## Outputs

| Output | Consumer | Contract |
| --- | --- | --- |
| {output} | {consumer} | {contract} |

## Modes

| Mode | Trigger | Behavior |
| --- | --- | --- |
| {mode} | {trigger} | {behavior} |

## Interaction Contract

| Interaction | Producer | Consumer | Failure Behavior |
| --- | --- | --- | --- |
| {interaction} | {producer} | {consumer} | {failure behavior} |

## Runtime Adapter Expectations

| Expectation | Required | Notes |
| --- | --- | --- |
| {expectation} | yes or no | {notes} |

## Observability

| Signal | Trigger | Payload Summary |
| --- | --- | --- |
| {signal} | {trigger} | {payload summary} |

## Validation Examples

| Example | Expected Result |
| --- | --- |
| {example} | {result} |

## Sigil-Development Handoff

- Handoff status: ready, flagged, or blocked
- Handoff notes: {notes}

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}