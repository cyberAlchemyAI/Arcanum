# Runtime Handoff: Integration Spec Refine

Status: executed
Run ID: 20260616T144535Z-integration-spec-refine
Dispatch: `REFINE-DISPATCH.json`

## Objective

Run the canonical Refine loop for a proposed public Arcanum `integration-spec` package after the operator confirmed stage execution and recommended subagent delegation.

## Strategy Permission State

- Runtime-backed stages: approved and executed.
- Subagent execution: approved and executed.
- External research: bounded-research selected by the operator and recorded in `stages/04-bounded-research.md`.
- Current state: final synthesis completed.

## Native Capability Handles

| Stage | Capability | Handle status |
| --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | available in current native skill list |
| Invoke Define | `invoke` | available in current native skill list |
| Interrogation refine-review | `interrogation` | available in current native skill list |
| Research decision | `refine` | parent-owned |
| Distill | `distill` | available in current native skill list |
| Invoke Redefine / Design | `invoke` | available in current native skill list |
| Interrogation refine-design-review | `interrogation` | available in current native skill list |
| Distill Repair | `distill` | available in current native skill list |
| Invoke Plan | `invoke` | available in current native skill list |
| Final Interrogation and Synthesis | `interrogation` plus parent `refine` | available plus parent-owned |

## Proposed Subagents

| Role | Purpose | Authorization |
| --- | --- | --- |
| `lane-z-integration-spec-advocate` | Build and critique the IntegrationSpec hypothesis. | completed |
| `lane-a-alternatives-challenger` | Solve the same problem without a new IntegrationSpec package. | completed |
| `taxonomy-standards-mapper` | Map DomainSpec and external standards without promoting vocabulary. | completed |

Join policy: parent synthesis. All spawned roles returned receipts and reached terminal closeout.

## Deferred Fields

- Package creation: deferred to a later approved route.
- Definitions/taxonomy changes: deferred to definitions-governance if needed.
- DomainSpec template mutation: deferred to a later approved route.
- Formula validator implementation: deferred to a later approved route.
