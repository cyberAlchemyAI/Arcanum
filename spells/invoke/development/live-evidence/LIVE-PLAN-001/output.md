## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: spells/invoke/plan.md
- Outputs: arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/IMPLEMENTATION-PLAN.md, arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/implementation-layering.md, arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/work-pack.md, arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/plan-transport.md
- Design views: pass; six-view design bundle covers supply request intake, item category classification, urgency triage, approval status transition, and operator note capture
- Glossary consistency: pass for supply request, item category, urgency, approval status, operator note, and unresolved planning question
- Implementation layering: arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/implementation-layering.md; L0, L1, L2, and L3 planning slices complete
- Work-pack: arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/work-pack.md; split
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete
- Smallest working units: complete
- Template/profile selection: selected implementation-plan family, standalone implementation-layering companion, standalone work-pack companion, and module-formulae execution-pack handoff; eligible because approved design outputs are stable, complexity is medium, seven execution tasks are required, and L0-L3 layer planning plus SWUs are mandatory
- Validation strategy: contract, rule-table, state-transition, persistence, audit, and reviewable evidence checks mapped to every delivery slice
- Decisions: plan mode only; no source mutation; split work-pack; execution handoff routes to task-session after selecting one SWU
- Unresolved gaps: no blocker gaps; unresolved planning question is a first-class domain field and workflow object, not a planning blocker
- Next route: task-session

# Implementation Plan: Mars Habitat Supply Request Module

## Implementation Objective

Plan implementation for a Mars habitat supply request module from approved design outputs.

The module must let habitat operators create and manage a supply request using the approved terms: supply request, item category, urgency, approval status, operator note, and unresolved planning question. The plan must remain non-mutating and execution-ready: it decomposes the work into seven tasks, L0-L3 layer slices, detailed domain logic specs, validation strategy, split work-pack evidence, and execution-pack handoff.

## Source Design References

| Ref ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SD-001 | Approved six-view design bundle | yes | Covers intake, classification, triage, status transition, and note capture. |
| SD-002 | Glossary consistency report | yes | Pass for all approved terms. |
| SD-003 | Design transport approval | yes | Design outputs are approved for plan consumption. |
| SD-004 | Plan-mode constraint | yes | Plan must not execute tasks or mutate source code. |

## Delivery Boundary

- Included: implementation plan, global implementation-layering artifact, split work-pack, execution-pack handoff, L0-L3 per-layer planning slices, task implementation-detail specs, SWU manifest, validation strategy, blocker ledger, and plan transport evidence.
- Excluded: source-code edits, runtime execution, database migration execution, upstream design mutation, glossary promotion, deployment, and task execution.
- Deferral rules: execution begins only after task-session receives this plan and a single SWU is selected.

## Complexity And Output Mode

| Field | Value | Evidence |
| --- | --- | --- |
| Complexity | medium | Seven tasks, four output artifact families, L0-L3 layering, domain rules, and SWU decomposition exceed low-complexity limits. |
| Task estimate | seven tasks | TASK-SR-001 through TASK-SR-007. |
| Output mode | split | Required for medium complexity. |
| Execution-pack handoff | required | Included as handoff evidence; no execution performed. |
| SWUs | required | Complete shared manifest and task-local lists included. |

## Delivery Slices

| Slice ID | Outcome | Dependencies | Validation |
| --- | --- | --- | --- |
| S-001 | Domain contract and intake baseline for supply request | Approved glossary and six-view design | Contract review, validation matrix, and intake scenario checks. |
| S-002 | Item category classification and urgency triage rules | S-001 | Rule-table tests and edge-case evidence. |
| S-003 | Approval status transition policy | S-001, S-002 | State-transition table tests and invalid-transition checks. |
| S-004 | Operator note and unresolved planning question handling | S-001, S-003 | Persistence/audit review and workflow scenario checks. |
| S-005 | Read model, audit evidence, and execution readiness | S-001 through S-004 | End-to-end scenario review, traceability matrix, and execution-pack readiness check. |

## Dependency Plan

| Dependency | Needed By | Readiness | Risk |
| --- | --- | --- | --- |
| Approved design bundle | all tasks | ready | Low; explicitly approved for plan consumption. |
| Approved glossary terms | all tasks | ready | Low; consistency pass recorded. |
| Persistence/storage pattern | TASK-SR-007 | partial | Must be selected during execution from host application patterns. |
| Authorization policy | TASK-SR-005, TASK-SR-007 | partial | Plan assumes caller identity is available; final role names may be host-specific. |
| Notification or downstream fulfillment system | none in this plan | deferred | Out of implementation boundary. |

## Global Implementation Layering

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether a supply request can be represented, validated, and submitted. | Domain model plus intake command/API contract. | Supply request fields, item category input, urgency input, initial approval status, operator note input, unresolved planning question input. | Automated category/urgency policy, status workflow hardening, persistence packaging. | Contract tests and intake scenario evidence. | Continue to L1 when valid and invalid intake cases are distinguishable. |
| L1 | After this layer, we know whether classification and triage are repeatable. | Deterministic category and urgency rule services. | Ordered item category classification, urgency triage, explainable rule outputs. | Multi-operator approval policy, audit packaging, release readiness. | Rule-table evidence and edge-case matrix. | Continue to L2 when rules are deterministic and explainable. |
| L2 | After this layer, we know whether reliability and governance hold. | Approval status state machine plus note/question handling. | Approval status transition policy, operator note append/validation, unresolved planning question lifecycle. | Scale packaging and operational rollout. | State-transition tests, audit review, validation evidence. | Continue to L3 when invalid transitions and malformed notes/questions are rejected. |
| L3 | After this layer, we know whether the module is packageable for pilot execution. | Persistence/read model/audit readiness slice. | Durable state mapping, query/read model, audit trail, task-session handoff evidence. | Production deployment and fulfillment-system integration. | End-to-end review, traceability, readiness checklist. | Pilot through task-session after SWU selection. |

## Per-Layer Planning Slices

### L0 Planning Slice

| Field | Value |
| --- | --- |
| Tasks | TASK-SR-001, TASK-SR-002 |
| Dependencies | Approved design bundle, glossary pass |
| Validation evidence | Domain contract review, intake validation scenarios |
| Blockers | none |
| Promotion criteria | Supply request can be created with approved terms and invalid inputs produce explicit validation errors. |
| SWUs | SWU-SR-001, SWU-SR-002, SWU-SR-003, SWU-SR-004 |

### L1 Planning Slice

| Field | Value |
| --- | --- |
| Tasks | TASK-SR-003, TASK-SR-004 |
| Dependencies | L0 intake contract |
| Validation evidence | Classification and triage rule-table checks |
| Blockers | none |
| Promotion criteria | Item category and urgency are deterministically produced or explicitly flagged for operator resolution. |
| SWUs | SWU-SR-005, SWU-SR-006, SWU-SR-007, SWU-SR-008 |

### L2 Planning Slice

| Field | Value |
| --- | --- |
| Tasks | TASK-SR-005, TASK-SR-006 |
| Dependencies | L0 request state, L1 category/urgency results |
| Validation evidence | Approval status transition checks, note/question audit checks |
| Blockers | none |
| Promotion criteria | Approval status transitions are governed and operator notes/unresolved planning questions preserve traceability. |
| SWUs | SWU-SR-009, SWU-SR-010, SWU-SR-011, SWU-SR-012 |

### L3 Planning Slice

| Field | Value |
| --- | --- |
| Tasks | TASK-SR-007 |
| Dependencies | L0-L2 complete |
| Validation evidence | Persistence/read-model review, audit evidence, execution-pack handoff |
| Blockers | none |
| Promotion criteria | Module has pilot-ready storage, query, audit, and execution handoff evidence. |
| SWUs | SWU-SR-013, SWU-SR-014 |

## Task Decomposition

| Task ID | Slice ID | Layer | Task | Done When |
| --- | --- | --- | --- | --- |
| TASK-SR-001 | S-001 | L0 | Define supply request domain contract and validation model. | Approved terms are represented with field-level validation and error outputs. |
| TASK-SR-002 | S-001 | L0 | Plan supply request intake command/API. | Intake maps operator input to a validated supply request draft or validation failure. |
| TASK-SR-003 | S-002 | L1 | Plan item category classification. | Ordered classification rules produce category, confidence, and evidence. |
| TASK-SR-004 | S-002 | L1 | Plan urgency triage. | Urgency is computed by deterministic precedence rules with edge-case handling. |
| TASK-SR-005 | S-003 | L2 | Plan approval status transition state machine. | Valid and invalid transitions are fully specified with audit evidence. |
| TASK-SR-006 | S-004 | L2 | Plan operator note and unresolved planning question handling. | Notes and questions are captured, validated, linked, and reviewable. |
| TASK-SR-007 | S-005 | L3 | Plan persistence, read model, audit trail, and execution readiness. | Storage/read models and pilot readiness checks are mapped without execution. |

## Implementation Detail Specs

| Task ID | Detail Status | Inputs | Outputs | Implementation Notes | Edge Cases | Validation Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-SR-001 | complete | Approved glossary, design bundle, field requirements | SupplyRequest model, validation errors | Define fields: requestId, requestedBy, itemName, itemCategory, quantity, urgency, approvalStatus, operatorNote[], unresolvedPlanningQuestion[], createdAt, updatedAt. Use enums for itemCategory, urgency, approvalStatus. Initial approvalStatus defaults to Draft before submission. | Missing itemName, zero/negative quantity, unknown enum value, note too long, duplicate unresolved question text. | Model review checklist and validation matrix. |
| TASK-SR-002 | complete | Operator intake payload | Supply request draft or validation failure | Pseudocode: normalize payload; validate required fields; attach operator identity; initialize approvalStatus=Draft; run field validators; return draft when valid; return structured errors when invalid; do not classify or triage unless explicitly invoked by later tasks. | Missing operator identity, whitespace-only item name, decimal quantity when only integer supplies are allowed, client-provided approvalStatus ignored on create. | Intake scenario table for valid create and invalid create. |
| TASK-SR-003 | complete | itemName, optional itemCategory hint, approved category vocabulary | Classified itemCategory with confidence and evidence | Ordered rules: 1. If explicit itemCategory hint matches approved enum, accept with source=operator_hint. 2. Else match itemName tokens against category dictionary. 3. If one category has clear match, assign with source=rule_match. 4. If multiple categories match, select highest priority category and emit unresolved planning question. 5. If none match, set category=Unclassified and emit unresolved planning question. | Ambiguous item names, unsupported category, synonym collision, operator hint conflicts with item name. | Rule-table tests covering explicit hint, synonym match, ambiguity, and no-match. |
| TASK-SR-004 | complete | itemCategory, quantity, operator urgency hint, habitat safety flags, unresolved question count | urgency value with rationale | Ordered precedence: 1. Safety-critical flag sets urgency=Critical. 2. Life-support category shortage sets High. 3. Operator High hint is accepted unless contradicted by low-risk category and no safety flag. 4. Routine replenishment defaults Medium. 5. Informational or duplicate requests default Low. Always return rationale codes. | Missing safety flag, contradictory operator hint, high quantity for low-risk item, unresolved planning question present for safety-critical item. | Triage precedence tests and rationale snapshot review. |
| TASK-SR-005 | complete | current approvalStatus, requested transition, actor role, validation state | new approvalStatus or transition error | State machine: Draft -> Submitted; Submitted -> UnderReview or Rejected; UnderReview -> Approved, Rejected, or NeedsInfo; NeedsInfo -> Submitted after question response; Approved -> FulfillmentQueued; Rejected terminal; FulfillmentQueued terminal for this module. Guards: only creator can submit Draft; reviewer can review Submitted; approver can approve UnderReview; open unresolved planning question blocks Approved except emergency override with reason. | Reopening terminal states, approving with unresolved planning question, duplicate transition, missing actor role, stale version. | State-transition table tests, invalid-transition tests, audit entry review. |
| TASK-SR-006 | complete | operator note payload, unresolved planning question payload, supply request ID, actor identity | appended note/question records and validation errors | Operator note handling: append-only list; trim whitespace; reject empty note; store author, timestamp, visibility, body, linked status. Unresolved planning question handling: create question with status=Open, source=classification/triage/reviewer/operator, questionText, requiredBeforeStatus optional. Resolve only with answer text, resolver, timestamp. Approval checks read open questions. | Empty note, oversized note, duplicate question, resolving already resolved question, deleting notes, question without source. | Note append tests, question open/resolve tests, audit trail review. |
| TASK-SR-007 | complete | domain events, request state, task outputs | persistence mapping, read model, audit view, handoff checklist | Persist supply request aggregate with append-only events: RequestCreated, CategoryClassified, UrgencyTriaged, ApprovalStatusChanged, OperatorNoteAdded, PlanningQuestionOpened, PlanningQuestionResolved. Read model exposes list/detail filters by approvalStatus, itemCategory, urgency, and unresolved question presence. Audit view orders events by timestamp and version. | Event ordering conflict, stale write version, missing audit actor, partial read-model rebuild, unknown legacy enum. | Persistence mapping review, read-model query scenarios, audit chronology check, execution readiness checklist. |

## Domain Logic Detail

### Item Category Classification

Inputs:

- `itemName`
- optional `itemCategoryHint`
- approved item category vocabulary
- category synonym dictionary
- current supply request ID

Outputs:

- `itemCategory`
- `classificationConfidence`
- `classificationEvidence`
- optional unresolved planning question

Pseudocode:

```text
classifyItemCategory(request):
  normalizedName = normalize(request.itemName)
  if validEnum(request.itemCategoryHint):
    return category(
      value=request.itemCategoryHint,
      confidence="high",
      evidence=["operator_hint"]
    )

  matches = matchTokens(normalizedName, categorySynonyms)

  if matches.count == 1:
    return category(
      value=matches[0].category,
      confidence="medium",
      evidence=matches[0].tokens
    )

  if matches.count > 1:
    selected = sortByPriority(matches)[0]
    openQuestion(
      source="classification",
      text="Item category is ambiguous for " + request.itemName,
      requiredBeforeStatus="Approved"
    )
    return category(
      value=selected.category,
      confidence="low",
      evidence=matches.allTokens
    )

  openQuestion(
    source="classification",
    text="Item category is not recognized for " + request.itemName,
    requiredBeforeStatus="Approved"
  )
  return category(value="Unclassified", confidence="low", evidence=[])
```

Validation evidence:

- Explicit category hint is accepted only when it is an approved item category.
- Unknown category hint is rejected or ignored with a validation error according to host API convention.
- Ambiguous classification opens an unresolved planning question.
- Unclassified request cannot be approved until resolved unless an emergency override policy is explicitly implemented later.

### Urgency Triage

Inputs:

- item category
- quantity
- operator urgency hint
- safety-critical flag
- current stock or shortage signal when available
- unresolved planning question count

Outputs:

- urgency
- urgency rationale codes
- optional unresolved planning question

Ordered rules:

1. If safety-critical flag is true, urgency is `Critical`.
2. If item category is life-support or medical and shortage signal is active, urgency is `High`.
3. If operator urgency hint is `Critical` without safety evidence, set urgency `High` and open unresolved planning question asking for criticality evidence.
4. If operator urgency hint is `High` and no contradiction exists, urgency is `High`.
5. If item category is routine supply and no shortage exists, urgency is `Medium`.
6. If request is duplicate, informational, or low quantity for non-critical category, urgency is `Low`.
7. If required triage data is missing, keep the safest non-terminal urgency and open unresolved planning question.

Validation evidence:

- Critical precedence overrides all lower hints.
- Missing data produces rationale and question rather than silent downgrade.
- Contradictory hints remain reviewable.

### Approval Status Transition

Inputs:

- current approval status
- requested approval status
- actor identity and role
- validation state
- unresolved planning question state
- expected version

Outputs:

- accepted transition with audit event
- rejected transition with reason

Transition table:

| Current | Allowed Next | Guard |
| --- | --- | --- |
| Draft | Submitted | Request is valid and actor is creator or authorized operator. |
| Submitted | UnderReview | Actor has reviewer role. |
| Submitted | Rejected | Actor has reviewer role and rejection reason is present. |
| UnderReview | Approved | Actor has approver role and no blocking unresolved planning question is open. |
| UnderReview | Rejected | Actor has approver role and rejection reason is present. |
| UnderReview | NeedsInfo | Actor has reviewer or approver role and at least one unresolved planning question is open. |
| NeedsInfo | Submitted | Required question responses are present. |
| Approved | FulfillmentQueued | Fulfillment handoff actor or service is authorized. |
| Rejected | none | Terminal in this module. |
| FulfillmentQueued | none | Terminal in this module. |

Validation evidence:

- Every allowed transition has a positive scenario.
- Every disallowed transition has an error scenario.
- Approval with open blocking unresolved planning question is rejected.
- Stale version transition is rejected.

### Operator Note Handling

Inputs:

- supply request ID
- actor identity
- note body
- optional visibility
- current approval status

Outputs:

- appended operator note
- validation error

Rules:

1. Notes are append-only.
2. Empty or whitespace-only notes are rejected.
3. Notes include author, timestamp, body, visibility, and approval status at time of note.
4. Notes do not mutate approval status.
5. Notes are audit-visible.
6. Notes may link to an unresolved planning question when provided.

Validation evidence:

- Add note succeeds with valid note.
- Empty note fails.
- Existing notes remain unchanged after append.
- Note audit entry includes actor and timestamp.

### Unresolved Planning Question Handling

Inputs:

- supply request ID
- source
- question text
- optional requiredBeforeStatus
- actor identity
- optional answer text for resolution

Outputs:

- open or resolved unresolved planning question
- validation error

Rules:

1. Questions can be opened by classification, triage, reviewer, approver, or operator workflows.
2. Duplicate open questions with same normalized text and source are rejected or merged according to host duplicate policy.
3. Questions start with status `Open`.
4. Resolution requires answer text, resolver identity, and timestamp.
5. Open questions marked `requiredBeforeStatus=Approved` block approval.
6. Resolved questions remain audit-visible and cannot be deleted.

Validation evidence:

- Open question from ambiguous classification.
- Open question blocks approval.
- Resolve question permits approval when no other blocking questions remain.
- Re-resolving a resolved question fails.

## Smallest Working Units Manifest

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification Command Or Reviewable Check |
| --- | --- | --- | --- | --- | --- |
| SWU-SR-001 | TASK-SR-001 | Define supply request fields and approved enums. | Domain model files or module contract docs. | Field list and enum list match approved glossary. | Review domain contract against glossary consistency report. |
| SWU-SR-002 | TASK-SR-001 | Define validation errors for required fields and enum constraints. | Domain validation module or contract docs. | Validation matrix covers missing, malformed, and unknown values. | Run or review validation matrix scenarios. |
| SWU-SR-003 | TASK-SR-002 | Specify intake command/API input and output shapes. | API contract or command handler boundary. | Intake accepts valid request and returns structured errors for invalid request. | Review intake examples and schema. |
| SWU-SR-004 | TASK-SR-002 | Specify draft creation behavior and default approval status. | Intake command handler or domain service. | New request starts as Draft and ignores client-supplied status. | Review create scenario and default-status check. |
| SWU-SR-005 | TASK-SR-003 | Implement classification rule table. | Classification policy module or spec. | Ordered rules are encoded with evidence output. | Rule-table review for hint, match, ambiguity, no-match. |
| SWU-SR-006 | TASK-SR-003 | Add unresolved planning question output for ambiguous classification. | Classification policy and question interface. | Ambiguous and unclassified items open blocking questions. | Review ambiguous classification scenario. |
| SWU-SR-007 | TASK-SR-004 | Implement urgency precedence rules. | Urgency triage policy module or spec. | Critical, high, medium, and low paths have rationale codes. | Triage precedence scenario review. |
| SWU-SR-008 | TASK-SR-004 | Add triage missing-data and contradiction handling. | Urgency policy and question interface. | Missing or contradictory evidence opens reviewable question. | Review contradiction and missing-data scenarios. |
| SWU-SR-009 | TASK-SR-005 | Define approval status state machine. | Approval workflow module or spec. | Transition table maps all allowed and terminal states. | State-transition table review. |
| SWU-SR-010 | TASK-SR-005 | Add transition guards and audit event requirements. | Approval workflow and audit contract. | Invalid role, stale version, and open blocking question are rejected. | Invalid-transition scenario review. |
| SWU-SR-011 | TASK-SR-006 | Implement append-only operator note handling. | Note service/module or spec. | Notes validate body and preserve audit metadata. | Note append and empty-note review. |
| SWU-SR-012 | TASK-SR-006 | Implement unresolved planning question open/resolve handling. | Question service/module or spec. | Open questions block approval and resolved questions remain auditable. | Question lifecycle scenario review. |
| SWU-SR-013 | TASK-SR-007 | Map persistence events and aggregate state. | Persistence mapping or storage adapter spec. | Event list supports rebuild of request state and audit chronology. | Persistence mapping review. |
| SWU-SR-014 | TASK-SR-007 | Map read model, filters, and execution readiness checklist. | Query/read model and execution-pack handoff. | Query fields cover status, category, urgency, and open-question presence. | Read-model scenario review and readiness checklist. |

## Task-Local Smallest Working Units

### TASK-SR-001 Smallest Working Units

- SWU-SR-001: Define supply request fields and approved enums.
- SWU-SR-002: Define validation errors for required fields and enum constraints.

### TASK-SR-002 Smallest Working Units

- SWU-SR-003: Specify intake command/API input and output shapes.
- SWU-SR-004: Specify draft creation behavior and default approval status.

### TASK-SR-003 Smallest Working Units

- SWU-SR-005: Implement classification rule table.
- SWU-SR-006: Add unresolved planning question output for ambiguous classification.

### TASK-SR-004 Smallest Working Units

- SWU-SR-007: Implement urgency precedence rules.
- SWU-SR-008: Add triage missing-data and contradiction handling.

### TASK-SR-005 Smallest Working Units

- SWU-SR-009: Define approval status state machine.
- SWU-SR-010: Add transition guards and audit event requirements.

### TASK-SR-006 Smallest Working Units

- SWU-SR-011: Implement append-only operator note handling.
- SWU-SR-012: Implement unresolved planning question open/resolve handling.

### TASK-SR-007 Smallest Working Units

- SWU-SR-013: Map persistence events and aggregate state.
- SWU-SR-014: Map read model, filters, and execution readiness checklist.

## Work-Pack Evidence

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | No blocker ambiguity prevents execution handoff. |
| complexity | medium | Seven tasks and split output required. |
| outputMode | split | Required by plan contract. |
| implementationPlanRef | arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/IMPLEMENTATION-PLAN.md | Planned output path. |
| executionPackRef | arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/module-formulae/execution-pack.md | Handoff only; no execution. |
| layeringArtifactRef | arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass/implementation-layering.md | L0-L3 complete. |
| activeLayerWindow | L0 | Execution should begin at L0 unless task-session selects a later review-only SWU. |
| readinessProfile | pilot | Module is planned for pilot readiness, not production deployment. |

## Execution-Pack Handoff

| Wave | Objective | Tasks | Entry Gate | Exit Gate |
| --- | --- | --- | --- | --- |
| W0 | Baseline lock and SWU selection | all tasks, no mutation | Plan artifacts reviewed | One SWU selected for task-session execution. |
| W1 | L0 intake proof | TASK-SR-001, TASK-SR-002 | W0 pass | Valid supply request draft can be represented and submitted. |
| W2 | L1 deterministic rules | TASK-SR-003, TASK-SR-004 | W1 pass | Classification and urgency produce rationale and question outputs. |
| W3 | L2 governance workflow | TASK-SR-005, TASK-SR-006 | W2 pass | Status transitions, notes, and questions are governed. |
| W4 | L3 pilot readiness | TASK-SR-007 | W3 pass | Persistence, read model, audit, and handoff checks are complete. |

Parallelization boundary:

- TASK-SR-003 and TASK-SR-004 may run in parallel after TASK-SR-001 and TASK-SR-002 are accepted.
- TASK-SR-005 depends on outputs from TASK-SR-003 and TASK-SR-004.
- TASK-SR-006 can begin after TASK-SR-001 but must align with TASK-SR-005 before approval blocking is finalized.
- TASK-SR-007 begins after L2 behavior is stable.

## Validation Strategy

| Check ID | Check | Scope | Tool Or Evidence |
| --- | --- | --- | --- |
| V-001 | Glossary term coverage | all tasks | Review against approved glossary consistency report. |
| V-002 | Domain validation matrix | TASK-SR-001, TASK-SR-002 | Required-field and enum validation scenario table. |
| V-003 | Intake command scenarios | TASK-SR-002 | Valid create, invalid create, client-supplied status ignored. |
| V-004 | Classification rule-table evidence | TASK-SR-003 | Explicit hint, synonym match, ambiguous match, no match. |
| V-005 | Urgency precedence evidence | TASK-SR-004 | Critical, high, medium, low, contradiction, missing data. |
| V-006 | Approval state-transition evidence | TASK-SR-005 | Allowed transitions, disallowed transitions, terminal states, stale version. |
| V-007 | Operator note evidence | TASK-SR-006 | Append-only note, empty note rejection, audit metadata. |
| V-008 | Unresolved planning question evidence | TASK-SR-006 | Open, block approval, resolve, duplicate handling. |
| V-009 | Persistence and read-model review | TASK-SR-007 | Event mapping, query filters, audit chronology. |
| V-010 | Execution readiness review | all tasks | SWU manifest complete, task-session route explicit, no mutation performed in plan mode. |

## Blocker Ledger

| Blocker ID | Blocker | Impact | Resolution |
| --- | --- | --- | --- |
| none | No blocker-level planning ambiguity remains. | n/a | Proceed to task-session after selecting one SWU. |

## Unresolved Gap Ledger

| Gap ID | Scope | Status | Notes |
| --- | --- | --- | --- |
| GAP-SR-001 | Host persistence technology | non-blocking | Execution worker must use existing host application persistence conventions. |
| GAP-SR-002 | Final role names for reviewer/approver | non-blocking | Plan specifies role capabilities; host application may map concrete role names. |
| GAP-SR-003 | Category synonym dictionary contents | non-blocking | Rule mechanism is specified; exact dictionary can be populated during execution from approved inventory. |

## Plan Transport Evidence

| Transport Field | Value |
| --- | --- |
| Source stage | approved design outputs |
| Target stage | governed implementation planning |
| Transport status | pass |
| Mutations performed | none |
| Upstream artifacts changed | none |
| Plan artifacts prepared | implementation plan, implementation-layering artifact, split work-pack, execution-pack handoff |
| Governance checks | complexity, L0-L3 layering, implementation details, SWUs, validation strategy, blocker ledger, next route |

## Closure Criteria

| Criterion | Evidence |
| --- | --- |
| Implementation plan is execution-ready | Seven tasks include implementation-detail specs and task-local SWUs. |
| Layering is complete | L0, L1, L2, and L3 slices include tasks, dependencies, validation, blockers, and promotion criteria. |
| Work-pack is split and ready | Work-pack evidence includes medium complexity, split mode, and execution-pack handoff. |
| Domain logic is specified | Classification, triage, approval status transition, operator note, and unresolved planning question handling include rules, inputs, outputs, edge cases, and validation evidence. |
| Plan mode stayed non-mutating | No task execution, source edit, upstream mutation, or glossary promotion performed. |
| Next route is clear | Route to task-session with one selected SWU. |

## Next Route Evidence

- Recommended next route: task-session.
- Entry condition: select exactly one SWU from the SWU manifest before mutation-capable execution.
- First recommended SWU: SWU-SR-001.
- Reason: L0 must establish the supply request field and enum contract before intake, classification, triage, or approval workflow work begins.
- Execution warning: if task-session receives a task with multiple SWUs and no selected SWU, it must ask for the specific SWU before source mutation starts.

## Gate Result

- Status: pass
- Reason: Approved design outputs are present, glossary consistency passed, design transport is approved, plan mode remained non-mutating, medium-complexity output requirements are satisfied, L0-L3 planning slices are complete, implementation-detail specs cover every execution task, SWU decomposition is complete, validation strategy is mapped, blocker ledger has no blockers, and next route is explicit.