---
template_id: invoke.architecture
template_type: architecture
applies_to:
  - design
  - plan
  - full
required_inputs:
  - architecture_intent
  - source_contracts
  - scope_boundary
optional_inputs:
  - discovery_mode
  - existing_interfaces
  - constraints
output_files:
  - ARCHITECTURE.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - source contracts present or discovery mode approved
  - six required views present
  - dependency and interface rules recorded
  - decision log populated
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# Architecture Plan: {capability-name}

## Architecture Intent

{what the architecture must make possible}

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | {path or decision} | yes or no | {notes} |

## View 1: Context View

Describe the external actors, neighboring systems, and ownership boundary.

## View 2: High-Level Structure View

Describe the major parts and their responsibilities.

## View 3: Low-Level Components View

Describe the internal components, their responsibilities, and local collaboration rules.

## View 4: Workflow Process View

Describe the main flows, state transitions, failure paths, and compensation behavior.

## View 5: Decision Flow View

Describe the policies, decision points, branching rules, and selected outcomes.

## View 6: Dependency Interface View

Describe internal and external dependencies, interface contracts, and boundary rules.

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| {constraint} | {source} | {impact} |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | {rule} | {component or interface} | {check} |

## Decision Log

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-001 | {decision} | {options} | {reason} |

## Risks

| Risk ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | {risk} | {mitigation} | {owner} |

## Downstream Planning Notes

- Implementation-plan inputs: {needed inputs}
- Work-pack implications: {handoff notes}
- Validation implications: {checks}

## Design Transport Notes

{how this architecture should be carried into follow-on artifacts}

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}