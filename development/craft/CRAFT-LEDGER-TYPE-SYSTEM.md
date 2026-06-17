# Craft Ledger Type System

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: Craft recursive ledger MVP
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `development/craft/CRAFT-LEDGER-TYPE-SYSTEM.md`
- Template selection: generic define artifact
- Decisions: define base condition types for blockers, gates, and enablers; add operational lanes such as tech, business, QA, validator, and auditor; allow context-specific subtypes; defer role delegation execution
- Unresolved gaps: exact schema encoding, lane catalog, conflict resolution between multiple types/lanes, validation examples
- Next route: design

## Objective

Define a candidate type system for Craft recursive ledger blockers, gates, and enablers.

The type system should let the ledger say not only that a context is blocked, gated, or enabled, but what kind of condition is involved and which operational lane is responsible. Later, those types can support routing and delegation:

```text
condition type + operational lane -> role -> responsible capability or human
```

This keeps the MVP simple while preserving a clean path toward role-aware orchestration.

## Source Intent

The user wants:

- types for blockers,
- types for gates,
- types for enablers,
- base types shared by every context,
- context-specific types for specialized work,
- a clear relation between types and operational lanes such as tech, business, QA, validator, and auditor,
- a future association from typed lane to role so the ledger can delegate work by responsibility.

## Type Model

Ledger typing has four layers:

| Layer | Purpose | Example |
| --- | --- | --- |
| Base condition type | Shared vocabulary that says what kind of blocker, gate, or enabler exists. | `decision_blocker`, `artifact_gate`, `validation_enabler` |
| Operational lane | Shared vocabulary that says which expertise lane owns or reviews the condition. | `tech`, `business`, `qa`, `validator`, `auditor` |
| Context-specific type | Local subtype that carries domain meaning inside one context family. | `spell_validation_blocker`, `schema_design_gate` |
| Role mapping | Future delegation rule from condition type plus lane to responsible role. | `validation_blocker + qa -> QA validator` |

The MVP should implement condition types, lanes, and context-specific subtypes as data. Role mapping should be modeled but not automated yet.

## Base Type Principles

1. A condition type names the cause or responsibility, not just the surface status.
2. A type should be stable enough to survive context movement.
3. Context-specific types should extend base types instead of replacing them.
4. Operational lanes should name the kind of expertise needed, not the person or tool.
5. Role mapping should be many-to-one friendly: multiple type/lane pairs may map to the same role.
6. One ledger item may carry multiple types or lanes when a blocker or enabler has mixed causes.

## Base Blocker Types

| Type | Meaning | Typical Lane |
| --- | --- | --- |
| `decision_blocker` | Progress requires a human, product, governance, or trade-off decision. | business or governance |
| `definition_blocker` | Terms, scope, objective, requirement, or expected artifact are unclear. | business |
| `design_blocker` | Structure, architecture, relationship, interface, or boundary is unresolved. | tech |
| `dependency_blocker` | Required upstream context, artifact, task, or external condition is incomplete. | planner or tech |
| `artifact_blocker` | Required artifact is missing, stale, invalid, or contradictory. | owning lane |
| `validation_blocker` | Required validation is missing or failing. | qa or validator |
| `authority_blocker` | The ledger cannot determine who owns the next move or promotion authority. | governance |
| `resource_blocker` | Work is blocked by time, tooling, access, compute, budget, or availability. | operations |
| `sequence_blocker` | Work is not ready because another ordered step must happen first. | planner |
| `recomposition_blocker` | Local work cannot be reattached cleanly to the parent or upper context. | tech or integrator |

## Base Gate Types

Gate types classify the check that must pass before a context can move forward.

| Type | Meaning | Gate Result Values |
| --- | --- | --- |
| `definition_gate` | Objective, scope, terms, and output are clear enough. | pass, flag, block |
| `design_gate` | Structure can hold the required relationships and constraints. | pass, flag, block |
| `plan_gate` | Next work is decomposed into executable units with dependencies. | pass, flag, block |
| `artifact_gate` | Required artifacts exist and are current enough. | pass, flag, block |
| `validation_gate` | Tests, review, or checks prove enough of the claim. | pass, flag, block |
| `authority_gate` | Ownership, route, and promotion authority are known. | pass, flag, block |
| `blocker_refinement_gate` | A blocker has been refined before resolution is allowed. | pass, flag, block |
| `recomposition_gate` | The context can rejoin its parent or downstream consumers. | pass, flag, block |
| `risk_gate` | Known risks are acceptable or explicitly deferred. | pass, flag, block |
| `readiness_gate` | The context is ready for execution, handoff, or closure. | pass, flag, block |

## Base Enabler Types

| Type | Meaning | Typical Lane |
| --- | --- | --- |
| `definition_enabler` | Clarifies scope, objective, terms, requirement, or expected artifact. | business |
| `design_enabler` | Provides structure, relationships, schema, interface, or architecture. | tech |
| `dependency_enabler` | Completes an upstream condition required by another context. | planner or tech |
| `artifact_enabler` | Produces or updates an artifact another context needs. | owning lane |
| `validation_enabler` | Supplies evidence that makes progress safe. | qa or validator |
| `authority_enabler` | Clarifies ownership, route, or promotion authority. | governance |
| `resource_enabler` | Provides tooling, access, budget, compute, or time. | operations |
| `sequence_enabler` | Completes an ordered step and opens the next one. | planner |
| `recomposition_enabler` | Adds the bridge needed to reconnect child work to parent context. | tech or integrator |

## Operational Lanes

Operational lanes classify the kind of expertise, review, or ownership needed. A lane is not yet a person, agent, tool, or final delegation route.

| Lane | Responsibility | Common Conditions |
| --- | --- | --- |
| `business` | Product intent, requirements, user value, scope, priority, acceptance meaning, and trade-off decisions. | definition blockers, decision blockers, requirement gates |
| `tech` | Architecture, implementation design, interfaces, data shape, integration, feasibility, and technical dependencies. | design blockers, dependency blockers, recomposition gates |
| `qa` | Test planning, test coverage, defect confirmation, regression safety, and acceptance test readiness. | validation blockers, validation gates |
| `validator` | Independent confirmation that evidence satisfies the stated gate or acceptance criterion. | validation gates, readiness gates, artifact gates |
| `auditor` | Traceability, compliance with process, promotion evidence, decision provenance, and governance conformance. | authority gates, audit gates, promotion blockers |
| `governance` | Ownership, lifecycle authority, policy, promotion permission, and route legitimacy. | authority blockers, decision blockers, promotion gates |
| `planner` | Sequencing, dependency ordering, SWU/task decomposition, and cross-context coordination. | sequence blockers, dependency gates |
| `operations` | Runtime access, tooling, budget, deployment, environment, compute, and availability constraints. | resource blockers, readiness gates |
| `integrator` | Recomposition between child and parent contexts, bridge contracts, and downstream compatibility. | recomposition blockers, recomposition gates |
| `blocker_refiner` | Clarifies raw blockers into typed, owned, evidence-backed blocker records before any resolution claim. | blocker refinement gates, active blockers |

Lane selection should answer:

```text
What kind of responsibility is needed to resolve, validate, or review this item?
```

Role mapping later answers:

```text
Who or what should take that responsibility in this repository?
```

## Context-Specific Types

A context-specific type specializes a base type.

Recommended shape:

```text
<context_family>.<specific_type>
```

Examples:

| Context Family | Context-Specific Type | Extends | Meaning |
| --- | --- | --- | --- |
| `craft` | `craft.scu_selection_blocker` | `design_blocker` | The context cannot proceed because the smallest coherent unit is unclear. |
| `craft` | `craft.residue_classification_gate` | `validation_gate` | Residue must be classified before reflection or next-layer routing. |
| `ledger` | `ledger.schema_shape_gate` | `design_gate` | Ledger fields and relation shape are stable enough to create examples. |
| `ledger` | `ledger.cross_context_relation_blocker` | `design_blocker` | Cross-context blocker/enabler semantics are not precise enough. |
| `ledger` | `ledger.business_acceptance_gate` | `definition_gate` | Business acceptance meaning is clear enough to validate context progress. |
| `ledger` | `ledger.qa_evidence_gate` | `validation_gate` | QA evidence exists for the context's claimed readiness. |
| `ledger` | `ledger.audit_trace_gate` | `authority_gate` | Decision, evidence, and ownership trace are reviewable. |
| `ledger` | `ledger.blocker_refinement_gate` | `blocker_refinement_gate` | A blocker has a refined type, lane, owner hint, closure condition, and evidence path before resolution. |
| `invoke` | `invoke.template_selection_blocker` | `decision_blocker` | Template family choice is ambiguous or unsupported. |
| `task_session` | `task_session.execution_handoff_gate` | `readiness_gate` | One SWU is bounded enough for execution handoff. |

## Role Mapping Model

Role mapping is deferred as automation, but the type system should reserve fields for it.

Candidate role fields:

| Field | Purpose |
| --- | --- |
| `primary_lane` | Operational lane usually responsible for this type. |
| `secondary_lanes` | Other lanes that may review or contribute. |
| `default_role` | Future local role usually responsible for this type/lane pair. |
| `allowed_roles` | Future local roles that may handle this type/lane pair. |
| `delegation_route` | Future route such as `decision-gate`, `invoke`, `task-session`, or human review. |
| `requires_human` | Whether this type cannot be auto-resolved. |
| `role_confidence` | How mature the mapping is: `candidate`, `active-local`, `promoted-by-owner`, or `deprecated`. |
| `owner_ref` | Optional local owner, team, policy, or row reference that backs the mapping. |
| `role_notes` | Short explanation of why the role mapping is appropriate. |

Initial lane-to-role sketch:

| Lane | Candidate Roles | Notes |
| --- | --- | --- |
| `business` | `product_owner`, `domain_owner`, `decision_owner` | Defines value, acceptance meaning, and business trade-offs. |
| `tech` | `architect`, `engineer`, `technical_owner` | Owns technical feasibility, design, and implementation constraints. |
| `qa` | `qa_owner`, `test_owner` | Owns test coverage and defect validation. |
| `validator` | `validator`, `reviewer` | Confirms evidence satisfies gates; may be independent from artifact creator. |
| `auditor` | `auditor`, `governance_reviewer` | Reviews traceability, provenance, authority, and process compliance. |
| `governance` | `governance_owner`, `policy_owner`, `lifecycle_owner` | Owns authority, promotion, route, and policy decisions. |
| `planner` | `planner`, `delivery_owner` | Owns sequence, dependencies, and task decomposition. |
| `operations` | `operator`, `platform_owner` | Owns environment, tooling, access, and runtime constraints. |
| `integrator` | `integrator`, `bridge_owner` | Owns recomposition and compatibility across contexts. |
| `blocker_refiner` | `blocker_refiner`, `refinement_owner` | Owns blocker clarification before resolution; may route to `/refine`. |

## Blocker Refinement Rule

Every blocker must pass through refinement before it can be marked resolved.

Allowed blocker lifecycle:

```text
raw -> typed -> refined -> resolution_proposed -> resolved
```

Blocked shortcut:

```text
raw -> resolved
typed -> resolved
```

Refinement means the blocker has:

- a base blocker type,
- a primary operational lane,
- an optional context-specific type,
- source and target IDs,
- a reason,
- evidence or source anchor,
- a closure condition,
- a suggested role or route,
- a record of whether `/refine` was run or explicitly waived by a human decision.

The `blocker_refiner` role owns this transition. It does not necessarily resolve the blocker. It prepares the blocker so the right lane, role, or route can resolve it without guessing.

Default route:

```text
blocker_refinement_gate -> blocker_refiner -> /refine
```

## Blocker Row Anatomy

A blocker row should answer six questions before anyone tries to close it.

| Question | Field(s) | Why It Matters |
| --- | --- | --- |
| What kind of blocker is this? | `kind`, `base_type`, `context_type` | Prevents every blocker from becoming a vague "something is wrong" note. |
| Where does it apply? | `source_id`, `target_id` | Shows what raised the blocker and what cannot safely move. |
| Who owns the next responsibility? | `primary_lane`, `secondary_lanes` | Separates technical, product, governance, validation, and audit concerns. |
| What local handler is suggested? | `default_role`, `allowed_roles`, `delegation_route` | Gives the next agent or human a starting route without pretending delegation already happened. |
| What would prove it closed? | `closure_condition`, `evidence`, `decision_ref` | Makes closure testable instead of mood-based. |
| What state is it in? | `status`, `refinement_status` | Prevents raw blockers from being resolved without refinement or waiver. |

Recommended blocker minimum:

```yaml
item_id: BLK-EXAMPLE-001
kind: blocker
base_type: validation_blocker
context_type: example.acceptance_evidence
primary_lane: validator
secondary_lanes:
  - product
source_id: CTX-EXAMPLE-ROOT
target_id: CTX-EXAMPLE-ROOT
status: active
refinement_status: refined
default_role: evidence_reviewer
allowed_roles:
  - evidence_reviewer
  - validator
delegation_route: task-session
requires_human: false
role_confidence: candidate
closure_condition: A receipt proves the acceptance check passed against the agreed fixture.
evidence: ART-ACCEPTANCE-PLAN
decision_ref: none
reason: The context cannot pass until acceptance evidence exists.
```

## Role Schema Anatomy

The role schema is deliberately two-step:

```text
lane -> local role -> route or human owner
```

The lane is stable project vocabulary. The role is local project vocabulary.
This matters because two repositories may both use the `validator` lane while
using different local roles, teams, or commands to do validation.

| Concept | Example | Rule |
| --- | --- | --- |
| Lane | `validator` | Names the responsibility type. |
| Role | `evidence_reviewer` | Names the local handler. |
| Route | `task-session` | Suggests the workflow that may perform the work. |
| Owner reference | `DEC-AUTHORITY-MODEL-001` or `policy/owners.md` | Backs the assignment with authority. |

Role fields are advisory until one of these backs them:

- an owner policy,
- a decision row,
- a route contract,
- a receipt from the role or route,
- an explicit human statement recorded as evidence.

## Typed Item Resolution Matrix

| Kind | Normal Positive State | What Closes It | Human Required? |
| --- | --- | --- | --- |
| Blocker | `resolved` | Closure condition plus evidence, receipt, linked decision, or waiver. | Sometimes; always when `requires_human: true`. |
| Gate | `pass` | Gate condition plus validation evidence. | Depends on gate type. |
| Enabler | `pass` | Evidence that the enabler exists and unlocks the target. | Usually no. |
| Gap | `resolved`, `waived`, or `superseded` | Treatment completed, explicitly waived, or replaced by a newer gap. | Often when treatment is `waive` or `defer`. |
| Decision | `closed` | Selected option, rationale, impact, and evidence. | Yes. |

Dispatch validation is not enough to close a blocker. It proves that a route is
well shaped, not that the work was executed or that the closure condition was
satisfied.

## Lane Conflict Rules

Mixed-lane blockers should not hide responsibility conflict. Use these rules:

1. `primary_lane` owns the next move.
2. `secondary_lanes` identify contributors or reviewers.
3. If `business` and `tech` disagree, keep the blocker active until a decision row records the selected interpretation.
4. If `validator` or `auditor` is a secondary lane, closure needs independent review evidence.
5. If `blocker_refiner` is the primary lane, the item is not ready for final resolution.
6. If no lane clearly owns the item, use `authority_blocker` or `decision_blocker` and route to `decision-gate`.
7. If one item has multiple unrelated causes, split it into separate blockers instead of overloading `base_type`.

## Candidate Type Record

```yaml
type_id: validation_blocker
kind: blocker
label: Validation blocker
definition: Required validation is missing or failing.
extends: null
primary_lane: qa
secondary_lanes:
  - validator
default_role: qa_owner
allowed_roles:
  - qa_owner
  - validator
  - artifact_owner
delegation_route: task-session
requires_human: false
role_confidence: candidate
```

Context-specific example:

```yaml
type_id: ledger.cross_context_relation_blocker
kind: blocker
label: Cross-context relation blocker
definition: Cross-context blocker/enabler semantics are not precise enough to design the ledger safely.
extends: design_blocker
context_family: ledger
primary_lane: tech
secondary_lanes:
  - business
  - auditor
default_role: architect
allowed_roles:
  - architect
  - domain_owner
  - governance_reviewer
delegation_route: invoke design
requires_human: false
role_confidence: candidate
```

Lane-specific gate example:

```yaml
type_id: ledger.audit_trace_gate
kind: gate
label: Audit trace gate
definition: Decision, evidence, ownership, and promotion trace are reviewable.
extends: authority_gate
context_family: ledger
primary_lane: auditor
secondary_lanes:
  - validator
  - business
default_role: governance_reviewer
allowed_roles:
  - auditor
  - governance_reviewer
  - validator
delegation_route: human review
requires_human: true
role_confidence: candidate
```

## Ledger Item Fields

Every blocker, gate, or enabler row should be able to carry type data.

Minimum fields:

| Field | Purpose |
| --- | --- |
| `item_id` | Stable local ID. |
| `kind` | blocker, gate, or enabler. |
| `base_type` | Shared base type. |
| `primary_lane` | Main operational lane responsible for the item. |
| `secondary_lanes` | Optional supporting or review lanes. |
| `context_type` | Optional context-specific type. |
| `source_id` | Source context, artifact, decision, or condition. |
| `target_id` | Target context, artifact, decision, or condition. |
| `status` | active, proposed, resolved, rejected, pass, flag, or block. |
| `default_role` | Future role inferred from type plus lane. |
| `allowed_roles` | Local roles allowed to handle the item. |
| `delegation_route` | Future suggested route. |
| `requires_human` | Whether the item needs human or governance authority before closure. |
| `role_confidence` | Maturity of the role mapping. |
| `owner_ref` | Optional owner, policy, or row reference that backs the role mapping. |
| `role_notes` | Explanation of the role mapping. |
| `refinement_status` | raw, typed, refined, resolution_proposed, resolved, or waived. |
| `closure_condition` | Evidence or condition required before the blocker can be resolved. |
| `evidence` | File, section, decision, validation, or user statement. |
| `reason` | Why this item exists. |

## Validation Rules

1. Every blocker must have a base blocker type.
2. Every gate must have a base gate type.
3. Every enabler must have a base enabler type.
4. Every context-specific type must extend exactly one base type.
5. A context-specific type cannot change the `kind` of its base type.
6. Every typed ledger item must have a primary lane.
7. A role mapping may be absent in the MVP, but the absence must be explicit.
8. A type or lane that requires human judgment must not be silently delegated to automation.
9. Multiple active blockers with different primary lanes should produce a coordination need, not a hidden priority choice.
10. `auditor` and `validator` lanes should be independent from the artifact-producing lane when evidence quality matters.
11. A blocker cannot be marked `resolved` unless `refinement_status` is `refined`, `resolution_proposed`, or `waived`.
12. A `waived` blocker refinement requires an explicit human decision record.
13. The default next route for raw or typed-but-unrefined blockers is `/refine`.
14. A row with `requires_human: true` cannot close from route-shape evidence alone.
15. Role fields are advisory unless backed by `owner_ref`, `decision_ref`, local policy, or route evidence.
16. When lanes conflict, the next move must name the coordination or decision route.

## Open Gaps

| Gap | Why It Matters | Next Action |
| --- | --- | --- |
| Lane catalog is only candidate. | Delegation quality depends on stable lane names and boundaries. | Validate against example ledger rows. |
| Role catalog is only sketched. | Local role names should emerge from real usage and repository conventions. | Validate after lanes work. |
| Type names may need compaction. | Too many verbose types could make the ledger hard to maintain. | Create examples and prune. |
| Context-specific type inheritance is not encoded yet. | Future automation needs a parseable relation. | Decide Markdown/JSON/YAML representation. |
| Multiple type/lane conflicts are unresolved. | A blocker may be both technical and business related, or validator and auditor related. | Add conflict policy during design. |
| Delegation routes are not executable. | MVP is still file-backed and reviewable. | Defer runtime integration. |
| Blocker refinement waiver policy is not designed. | Some urgent blockers may need human-approved bypass. | Define waiver shape during schema refinement. |

## Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| Base blocker, gate, and enabler type sets exist. | Tables in this artifact. |
| Context-specific types can extend base types. | Context-specific examples in this artifact. |
| Type records reserve lane and role-mapping fields. | Candidate type record includes primary lane, secondary lanes, default role, and route fields. |
| Business, tech, QA, validator, and auditor relationships are explicit. | Operational lanes section and examples include those lanes. |
| Blocker refinement is required before resolution. | Blocker refinement rule and validation rules require `/refine` or explicit waiver before resolved status. |
| Automation is deferred without losing the delegation path. | Role mapping is modeled, not executed. |
| Human-required decisions remain gated. | Validation rule prevents silent automation for human judgment types. |

## Gate Result

- Status: pass
- Reason: The type-system baseline is specific enough to feed the recursive ledger design. Remaining issues are design choices, not blockers for the next artifact.
