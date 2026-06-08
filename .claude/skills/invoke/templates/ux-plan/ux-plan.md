---
template_id: invoke.ux-plan
template_type: ux-plan
applies_to:
  - define
  - design
  - full
required_inputs:
  - user_goals
  - workflow_scope
  - target_actors
optional_inputs:
  - surfaces
  - state_model
  - content_requirements
  - accessibility_considerations
output_files:
  - UX-PLAN.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - user goals present
  - workflow scope present
  - target actors present or inferable
  - handoff boundaries recorded
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# UX Plan: {workflow-name}

## User Goals

| Goal | Actor | Success Signal |
| --- | --- | --- |
| {goal} | {actor} | {signal} |

## Actors

| Actor | Needs | Constraints |
| --- | --- | --- |
| {actor} | {needs} | {constraints} |

## Journeys

| Journey | Start State | End State | Notes |
| --- | --- | --- | --- |
| {journey} | {start} | {end} | {notes} |

## Surfaces

| Surface | Purpose | Entry Points | Exit Points |
| --- | --- | --- | --- |
| {surface} | {purpose} | {entry} | {exit} |

## State Model

| State | User Meaning | Allowed Transitions | Error Behavior |
| --- | --- | --- | --- |
| {state} | {meaning} | {transitions} | {error behavior} |

## Interaction Flows

| Flow | Steps | Risk | Recovery |
| --- | --- | --- | --- |
| {flow} | {steps} | {risk} | {recovery} |

## Content Requirements

| Content | Surface | Purpose | Constraint |
| --- | --- | --- | --- |
| {content} | {surface} | {purpose} | {constraint} |

## Accessibility Considerations

| Consideration | Applies To | Required Response |
| --- | --- | --- |
| {consideration} | {surface or flow} | {response} |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| {risk} | {impact} | {mitigation} |

## Acceptance Signals

| Signal | Evidence | Owner |
| --- | --- | --- |
| {signal} | {evidence} | {owner} |

## Handoff Boundaries

- Architecture handoff: {needed or deferred}
- Implementation-plan handoff: {needed or deferred}
- Research handoff: {needed or deferred}

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}