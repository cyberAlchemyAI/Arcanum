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
  - design_selection_result
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
  - natural-person plus changed semantic-contract trigger is proved
  - success failure recovery correction and reversibility are covered
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# UX Plan: {workflow-name}

## Selection Contract

Select this template only when both conditions hold:

1. at least one `human_actor` is a natural person who reads, decides, acts,
   recovers, navigates, or performs assistive operation through the surface;
2. at least one rendered surface has a new or changed human-facing semantic contract.

The `DesignSelectionResult` must select `ux-plan` with disposition `required`
and cite the actor/surface signals. Files, APIs, receipts, generated evidence,
backend-only changes, and semantics-preserving style tokens do not trigger UX
by themselves.

Positive examples: changed focus meaning, reflow that changes reading/operation
order, changed accessible name, changed recovery choices, or operator-visible
evidence that changes a decision.

Negative examples: a backend protocol with no human effect, a static generated
artifact, or a style token whose semantic and assistive behavior is unchanged.

## User Goals

| Goal | Actor | Success Signal |
| --- | --- | --- |
| {goal} | {actor} | {signal} |

## Actors

| Actor | Needs | Constraints |
| --- | --- | --- |
| {actor} | {needs} | {constraints} |

## Journeys

| Journey | Start State | Success state | Failure and recovery | Correction/reversibility | Notes |
| --- | --- | --- | --- | --- | --- |
| {journey} | {start} | {success} | {failure and recovery} | {how the user corrects or reverses} | {notes} |

## Surfaces

| Surface | Purpose | Entry Points | Exit Points |
| --- | --- | --- | --- |
| {surface} | {purpose} | {entry} | {exit} |

## State Model

| State | User Meaning | Allowed Transitions | Error Behavior |
| --- | --- | --- | --- |
| {state} | {meaning} | {transitions} | {error behavior} |

## Visible State And Evidence Meaning

| Visible state/evidence | Meaning to the actor | Allowed decision/action | Staleness or uncertainty cue | Owner |
| --- | --- | --- | --- | --- |
| {receipt, status, projection, or message} | {bounded meaning} | {action} | {how uncertainty is exposed} | {exact owner} |

Do not imply approval, completion, readiness, or authority beyond the evidence
state carried by the source receipt.

## Interaction Flows

| Flow | Steps | Risk | Recovery |
| --- | --- | --- | --- |
| {flow} | {steps} | {risk} | {recovery} |

## Content Requirements

| Content | Surface | Purpose | Claim/evidence bound | Constraint | Owner |
| --- | --- | --- | --- | --- | --- |
| {content} | {surface} | {purpose} | {what the text may and may not claim} | {constraint} | {owner} |

## Accessibility Considerations

| Consideration | Applies To | Required Response | Acceptance owner |
| --- | --- | --- | --- |
| focus order and visible focus | {surface/flow} | {response} | {owner} |
| reflow and reading/operation order | {surface/flow} | {response} | {owner} |
| contrast and non-color meaning | {surface/flow} | {response} | {owner} |
| accessible names and relationships | {surface/flow} | {response} | {owner} |
| keyboard and assistive operation | {surface/flow} | {response} | {owner} |

## Responsive Semantics

| Viewport/input condition | Information retained | Actions retained | Order/relationship retained | Recovery behavior | Owner |
| --- | --- | --- | --- | --- | --- |
| {condition} | {information} | {actions} | {semantic order} | {recovery} | {owner} |

Responsive changes must preserve meaning and operability, not merely fit the
same content into a different width.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| {risk} | {impact} | {mitigation} |

## Acceptance Signals

| Signal | Positive/negative | Exact evidence selector | Accountable owner | Validator owner |
| --- | --- | --- | --- | --- |
| {signal} | positive or negative | {selector} | {owner} | {owner} |

## Handoff Boundaries

- Architecture handoff: {needed or deferred}
- Implementation-plan handoff: {needed or deferred}
- Research handoff: {needed or deferred}

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}
