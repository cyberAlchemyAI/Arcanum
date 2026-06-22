## Invoke Validation Fixture Result

- Fixture: INV-PLAN-SPLIT-001
- User request: Plan implementation for a Mars habitat supply approval workflow that needs staged rollout and governance checks.
- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: arcanum/spells/invoke/plan.md
- Outputs: artifacts/mars-habitat-supply/IMPLEMENTATION-PLAN.md, artifacts/mars-habitat-supply/IMPLEMENTATION-LAYERING.md, artifacts/mars-habitat-supply/work-pack/README.md, artifacts/mars-habitat-supply/EXECUTION-PACK.md, .arcanum/necronomicon/sessions/demo/invoke-transports/plan.md
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Glossary consistency: pass
- Dispatch techniques: sequence, scu_swu_reduction, recomposition_proof, validation_loop, owner_boundary_check, handle_handoff, residue_ledger, execution_receipt_handoff; validation status pass; full dispatch n/a
- Distill validation: pass; recomposition proof pass; gap count 0
- Implementation layering: artifacts/mars-habitat-supply/IMPLEMENTATION-LAYERING.md with global L0-L3 decision boundaries
- Work-pack: artifacts/mars-habitat-supply/work-pack/README.md, split
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete
- Smallest working units: complete
- Template/profile selection: implementation-plan plus standalone implementation-layering, work-pack, and module-formulae execution-pack companions
- Validation strategy: unit checks, fixture replay, governance checks, and release-readiness evidence mapped to every delivery slice
- Decisions: use split work-pack; require execution-pack handoff; plan per-layer slices before execution
- Unresolved gaps: none blocking
- Next route: task-session

## Per-Layer Planning Slices

| Layer | Slice | Tasks | Dependencies | Validation Evidence | Blockers | Promotion Criteria |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | smallest supply request proof and decision unlocked | TASK-L0-intake, TASK-L0-state | approved source contracts | fixture replay for intake and state transition | none | evidence shows request intake and approval state can work end to end |
| L1 | repeatable operator workflow and hardening | TASK-L1-review, TASK-L1-notes | L0 evidence | repeat workflow checks and operator note fixtures | none | L0 proof remains stable across repeated requests |
| L2 | governance, reliability, validation, and degraded-mode slice | TASK-L2-audit, TASK-L2-validation | L1 repeatability | audit trail checks and degraded approval-state evidence | none | L1 guarantees preserved with governance controls |
| L3 | packaging, release, and rollout slice | TASK-L3-packaging, TASK-L3-release | L2 governance evidence | release-readiness checklist and transport report | none | L2 evidence supports pilot-ready rollout |

## Implementation Detail Specs

| Task ID | Detail Status | Inputs | Outputs | Implementation Notes | Edge Cases | Validation Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-L0-intake | complete | supply request payload, approved glossary terms | normalized request draft | Validate required fields, normalize item category labels, preserve operator-provided urgency, and attach initial approval status before persistence is planned. | missing item category, unsupported urgency, empty operator note | intake fixture and required-field checks |
| TASK-L0-state | complete | normalized request draft, approval status catalog | initial status record | Assign the initial status from the approved status catalog; reject unknown statuses; record the source design ref used for the status decision. | unknown approval status, duplicate initial status | state initialization fixture |
| TASK-L1-review | complete | request draft, category matrix, urgency matrix | review route decision | Classify item category first, then apply urgency triage; category determines reviewer pool and urgency determines ordering within that pool. | category match tie, urgency not supplied | classification and triage matrix checks |
| TASK-L1-notes | complete | operator note, request id, actor id | note record linked to request | Store note text with actor and request association; preserve original note order; do not derive approval status from note text. | empty note, repeated note submission | note traceability check |
| TASK-L2-audit | complete | status transitions, note records, actor events | audit trail plan | Emit an audit entry for every status transition and note update; include previous state, next state, actor, timestamp source, and reason when supplied. | missing actor, forbidden transition | audit fixture and forbidden-transition check |
| TASK-L2-validation | complete | delivery slices, blocker ledger, validation rules | validation checklist | Map each slice to at least one automated or reviewable check; block when a blocker affects acceptance criteria. | validation missing for a slice, blocker severity unknown | validation coverage report |
| TASK-L3-packaging | complete | work-pack tasks, execution waves, validation checklist | execution-pack handoff | Group tasks by layer order; only allow parallel tasks when dependencies and layer promotion evidence are satisfied. | wave dependency cycle, missing promotion evidence | execution-pack wave review |
| TASK-L3-release | complete | execution-pack handoff, plan transport | pilot readiness route | Route to task-session with work-pack gate status, unresolved gaps, and non-mutation boundary preserved. | unresolved acceptance blocker, missing transport evidence | handoff readiness checklist |

## Smallest Working Units

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification Command |
| --- | --- | --- | --- | --- | --- |
| SWU-MHS-001 | TASK-L0-intake | Validate supply request required fields. | request intake module and intake fixtures | required-field acceptance evidence | `run intake required-field fixture` |
| SWU-MHS-002 | TASK-L0-intake | Normalize item category and urgency hints. | request normalization helper and fixtures | normalized draft evidence | `run intake normalization fixture` |
| SWU-MHS-003 | TASK-L0-state | Assign initial approval status. | approval status initializer | initial status fixture evidence | `run approval initialization fixture` |
| SWU-MHS-004 | TASK-L1-review | Classify item category by ordered rules. | category classifier and rule fixtures | classification matrix evidence | `run category classification fixture` |
| SWU-MHS-005 | TASK-L1-review | Apply urgency triage after classification. | urgency triage helper and fixtures | urgency precedence evidence | `run urgency triage fixture` |
| SWU-MHS-006 | TASK-L1-notes | Link operator note to request. | operator note model and fixtures | note traceability evidence | `run operator note fixture` |
| SWU-MHS-007 | TASK-L2-audit | Emit audit entry for status transition. | audit event writer and transition fixtures | audit trail evidence | `run transition audit fixture` |
| SWU-MHS-008 | TASK-L2-validation | Map validation checks to delivery slices. | validation checklist and fixture report | validation coverage evidence | `run validation coverage check` |
| SWU-MHS-009 | TASK-L3-packaging | Group execution tasks by layer and dependency. | execution-pack wave manifest | wave dependency evidence | `run execution-pack review` |
| SWU-MHS-010 | TASK-L3-release | Prepare task-session handoff route. | work-pack handoff and plan transport | handoff readiness evidence | `run handoff readiness review` |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | approved design refs -> plan artifacts -> task-session handoff | every artifact consumes explicit prior handles | pass |
| scu_swu_reduction | layer-mapped waves and SWU manifest | each SWU is smaller than its parent task and still executable | pass |
| recomposition_proof | SWU manifest -> approved design | SWUs recompose into the habitat supply workflow | pass |
| validation_loop | delivery slices and SWUs | each slice and SWU has evidence | pass |
| owner_boundary_check | Invoke plan -> task-session | Invoke does not claim execution authority | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | SWU-MHS-001 through SWU-MHS-010 each map to one parent task. |
| Recomposition proof | pass | L0-L3 slices recompose into the approved supply workflow. |
| Hidden acceptance-critical gaps | pass | none blocking |
| Deferred complexity | pass | release packaging remains L3 and execution remains deferred |
| Navigation to first executable unit | pass | start at SWU-MHS-001 after Task Session selection |

### Task-Local SWU Lists

#### TASK-L0-intake

## Smallest Working Units

- SWU-MHS-001: Validate supply request required fields.
- SWU-MHS-002: Normalize item category and urgency hints.

#### TASK-L0-state

## Smallest Working Units

- SWU-MHS-003: Assign initial approval status.

#### TASK-L1-review

## Smallest Working Units

- SWU-MHS-004: Classify item category by ordered rules.
- SWU-MHS-005: Apply urgency triage after classification.

#### TASK-L1-notes

## Smallest Working Units

- SWU-MHS-006: Link operator note to request.

#### TASK-L2-audit

## Smallest Working Units

- SWU-MHS-007: Emit audit entry for status transition.

#### TASK-L2-validation

## Smallest Working Units

- SWU-MHS-008: Map validation checks to delivery slices.

#### TASK-L3-packaging

## Smallest Working Units

- SWU-MHS-009: Group execution tasks by layer and dependency.

#### TASK-L3-release

## Smallest Working Units

- SWU-MHS-010: Prepare task-session handoff route.
