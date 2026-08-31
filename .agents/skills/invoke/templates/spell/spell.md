---
template_id: invoke.spell
template_type: spell
applies_to:
  - define
  - design
  - full
required_inputs:
  - spell_identity
  - trigger_conditions
  - mode_contracts
optional_inputs:
  - required_sigils
  - required_spells
  - shared_state
  - observability
output_files:
  - SPELL-HANDOFF.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - spell identity present
  - trigger conditions present
  - at least one mode contract present
  - spellcraft handoff recorded
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# Spell Handoff: {spell-name}

## Spell Identity

- Name: {spell-name}
- Purpose: {purpose}
- Owning surface: {directory or registry location}

## Trigger Conditions

| Trigger | User Signal | Route |
| --- | --- | --- |
| {trigger} | {signal} | {mode or handoff} |

## Modes

| Mode | Purpose | Required Inputs | Outputs |
| --- | --- | --- | --- |
| {mode} | {purpose} | {inputs} | {outputs} |

## Required Sigils And Spells

| Capability | Type | Required | Notes |
| --- | --- | --- | --- |
| {capability} | sigil or spell | yes or no | {notes} |

## Optional Capabilities

| Capability | Activation Rule | Notes |
| --- | --- | --- |
| {capability} | {rule} | {notes} |

## Shared State

| State Item | Owner | Persistence | Notes |
| --- | --- | --- | --- |
| {item} | {owner} | {scope} | {notes} |

## Phase Contract

| Phase | Entry Criteria | Exit Criteria | Failure Behavior |
| --- | --- | --- | --- |
| {phase} | {entry} | {exit} | {failure behavior} |

## Gates

| Gate | Required Evidence | Result |
| --- | --- | --- |
| {gate} | {evidence} | pass, flag, or block |

## Observability

| Signal | When Emitted | Consumer |
| --- | --- | --- |
| {signal} | {event} | {consumer} |

## Validation Examples

| Example | Expected Result |
| --- | --- |
| {example} | {result} |

## Registry Readiness

- Registry entry required: yes or no
- Alias required: yes or no
- Documentation status: candidate, reviewed, or approved

## Spellcraft Handoff

- Handoff status: ready, flagged, or blocked
- Handoff notes: {notes}

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}