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
  - design_scope_manifest
  - design_selection_result
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

## Closed Scope

- System of interest: {target id}
- `DesignScopeManifest`: {path and input digest}
- `DesignDenominatorReceipt`: {path and receipt digest}
- `DesignSelectionResult`: {path and result digest}

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

## Significant Behavior Scenario

Use a runtime scenario only when an external effect, durable state,
operational claim, or human recovery is present. Otherwise use a deterministic
artifact/evidence scenario.

| Stimulus | Preconditions | Ordered response | Failure/recovery | Observable evidence | Acceptance owner |
| --- | --- | --- | --- | --- | --- |
| {stimulus} | {preconditions} | {response} | {failure/recovery} | {evidence} | {owner} |

## Concern-to-view trace

| Concern ID | Primary class | Signal IDs | Disposition | Accountable owner | Contributing owners | Artifact owner | Validator owner | View/extension | Evidence selectors | Revisit condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {concern} | {class} | {signals} | required, recommended, not-applicable-with-rationale, or block | {owner} | {owners} | {owner} | `invoke-design-selection-validator` | {view} | {selectors} | {condition or n/a} |

## Planned Witness Contracts

| Fixture ID | Claim ID | Polarity | Target | Input/violation | Expected result | Execution owner | Phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {fixture} | {claim} | positive or negative | {target} | {input} | {result} | {owner} | plan, implementation, or validation |

| Validator contract ID | Claim ID | Target contract | Accepted digest/binding | Verdicts | Stale receipt | Self issue | Validator owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {validator} | {claim} | {contract} | {digest/rule} | pass and fail | reject | reject | {owner} |

Planned witness contracts are not executed Plan evidence.

## Triggered architecture extensions

Keep all six baseline views. Add only rows selected `required`:

| Output ID | Trigger | Required architecture content |
| --- | --- | --- |
| `architecture:authority-trust` | admission, privilege, trust | authority and enforcement placement |
| `architecture:state-event` | lifecycle legality | state/event rules and forbidden transitions |
| `architecture:persistence-concurrency` | store, queue, writer | ordering, idempotency, concurrency |
| `architecture:failure-compensation` | external/irreversible effect | retry, partial effect, compensation, rollback |
| `architecture:integration-versioning` | evolving interface/protocol | compatibility and recovery |
| `architecture:migration-rollout` | representation/deployment transition | conversion, staging, rollback |
| `architecture:data-lifecycle` | data/log sink | purpose, access, retention, deletion |
| `architecture:security-abuse` | adversarial boundary | abuse cases, controls, residual risk |
| `architecture:quality` | measurable service/resource claim | quality scenario and threshold |

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| {constraint} | {source} | {impact} |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | {rule} | {component or interface} | {check} |

## Decision Log

| Decision ID | Status | Concern IDs | Decision | Alternatives | Criteria | Positive consequences | Negative consequences/trade-offs | Evidence | Revisit trigger |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | proposed, accepted, superseded, or rejected | {concerns} | {decision} | {options} | {criteria} | {positive} | {negative/trade-offs} | {evidence} | {trigger} |

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
