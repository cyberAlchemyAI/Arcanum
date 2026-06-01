# Craft Ledger Type Examples

## Purpose

Validate the current Craft recursive-ledger type model with concrete examples before designing the minimal ledger schema.

This artifact satisfies `CRAFT-REFINE-001` from [WORK-PACK.md](WORK-PACK.md). It is intentionally small: enough to test nested contexts, cross-context relations, blockers, enablers, gates, operational lanes, role hints, and the blocker refinement rule.

## Source Contract

Primary sources:

- [WORK-PACK.md](WORK-PACK.md), task `CRAFT-REFINE-001`
- [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md)
- [CRAFT-RECURSIVE-LEDGER-DEFINE.md](CRAFT-RECURSIVE-LEDGER-DEFINE.md)
- [CRAFT-RECURSIVE-LEDGER-GLOSSARY.md](CRAFT-RECURSIVE-LEDGER-GLOSSARY.md)

## Context Rows

| context_id | parent_id | title | purpose | stage | gate | next_move |
| --- | --- | --- | --- | --- | --- | --- |
| CTX-CRAFT | root | Craft Development | Develop Craft as an operational method and candidate capability. | design | flag | Refine recursive-ledger examples, then schema. |
| CTX-LEDGER | CTX-CRAFT | Recursive Ledger MVP | Define the file-backed ledger for nested contexts and cross-context blockers/enablers. | design | flag | Convert examples into schema. |
| CTX-TYPES | CTX-LEDGER | Type And Lane Model | Stabilize condition types, lanes, role hints, and blocker refinement. | validate | pass | Feed examples into schema design. |
| CTX-SCHEMA | CTX-LEDGER | Ledger Schema | Define minimal context, artifact, relation, and typed-item rows. | idea | block | Wait for examples from CTX-TYPES. |
| CTX-SCORING | CTX-LEDGER | Priority Scoring | Later rank contexts by blockers, enablers, readiness, and impact. | idea | block | Wait for schema and examples. |

## Artifact Rows

| artifact_id | owner_context_id | path | artifact_type | status | notes |
| --- | --- | --- | --- | --- | --- |
| ART-TYPE-SYSTEM | CTX-TYPES | `development/craft/CRAFT-LEDGER-TYPE-SYSTEM.md` | type-system | active | Defines condition types, lanes, role hints, and blocker refinement rule. |
| ART-WORK-PACK | CTX-LEDGER | `development/craft/WORK-PACK.md` | work-pack | active | Owned by the recursive-ledger context; not the whole ledger. |
| ART-EXAMPLES | CTX-TYPES | `development/craft/CRAFT-LEDGER-TYPE-EXAMPLES.md` | examples | active | This artifact. |
| ART-SCHEMA | CTX-SCHEMA | `development/craft/CRAFT-RECURSIVE-LEDGER-DESIGN.md` | schema-design | planned | Target output for CRAFT-REFINE-002. |

## Typed Blocker Rows

| item_id | kind | base_type | context_type | primary_lane | secondary_lanes | source_id | target_id | status | refinement_status | default_role | delegation_route | closure_condition | evidence | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-RAW-001 | blocker | `design_blocker` | `ledger.cross_context_relation_blocker` | `blocker_refiner` | `tech`, `business` | CTX-TYPES | CTX-SCHEMA | active | raw | `blocker_refiner` | `/refine` | Refine source/target relation semantics, then assign final primary lane. | User introduced cross-project blockers/enablers; type system is candidate. | Schema work should not proceed from a vague relation blocker. |
| BLK-SCHEMA-001 | blocker | `dependency_blocker` | none | `planner` | `tech` | CTX-TYPES | CTX-SCHEMA | active | refined | `planner` | `/refine CRAFT-REFINE-002` | `ART-EXAMPLES` exists and covers required examples. | [WORK-PACK.md](WORK-PACK.md) says schema depends on examples. | Schema design depends on examples being complete enough. |
| BLK-SCORING-001 | blocker | `sequence_blocker` | none | `planner` | `business`, `tech` | CTX-SCHEMA | CTX-SCORING | active | refined | `planner` | deferred | Ledger schema exists and includes future scoring placeholders. | [WORK-PACK.md](WORK-PACK.md) defers scoring. | Scoring before schema would overfit unknown fields. |
| BLK-AUDIT-001 | blocker | `authority_blocker` | `ledger.audit_trace_gate` | `auditor` | `governance`, `validator` | ART-TYPE-SYSTEM | CTX-LEDGER | active | typed | `governance_reviewer` | human review | Decide whether audit trace is mandatory for MVP or later validation. | Type system adds auditor lane and audit trace gate. | Audit responsibility exists but MVP strictness is undecided. |

## Gate Rows

| item_id | kind | base_type | context_type | primary_lane | secondary_lanes | source_id | target_id | status | refinement_status | default_role | delegation_route | closure_condition | evidence | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GATE-TYPES-001 | gate | `validation_gate` | `ledger.qa_evidence_gate` | `qa` | `validator` | ART-EXAMPLES | CTX-TYPES | pass | refined | `qa_owner` | manual review | Examples cover all CRAFT-REFINE-001 required cases. | This artifact includes contexts, blockers, enablers, gates, lanes, and role hints. | Type examples are sufficient for next schema refinement. |
| GATE-BLOCKER-001 | gate | `blocker_refinement_gate` | `ledger.blocker_refinement_gate` | `blocker_refiner` | `auditor` | BLK-RAW-001 | BLK-RAW-001 | block | raw | `blocker_refiner` | `/refine` | `BLK-RAW-001` reaches `refined` or is explicitly waived. | Type system requires refinement before resolution. | Raw blocker cannot be marked resolved. |
| GATE-SCHEMA-001 | gate | `readiness_gate` | none | `validator` | `tech`, `business` | ART-EXAMPLES | CTX-SCHEMA | pass | refined | `validator` | `/refine CRAFT-REFINE-002` | Every example row has a target schema field candidate. | This artifact names fields needed by the schema. | Schema refinement can begin. |

## Enabler Rows

| item_id | kind | base_type | context_type | primary_lane | secondary_lanes | source_id | target_id | status | refinement_status | default_role | delegation_route | closure_condition | evidence | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ENA-DEF-001 | enabler | `definition_enabler` | none | `business` | `validator` | ART-WORK-PACK | CTX-TYPES | active | refined | `product_owner` | none | Work-pack acceptance criteria remain stable. | [WORK-PACK.md](WORK-PACK.md) names required examples. | The work-pack defines what "enough examples" means. |
| ENA-TECH-001 | enabler | `design_enabler` | `ledger.schema_shape_gate` | `tech` | `integrator` | ART-EXAMPLES | CTX-SCHEMA | active | refined | `architect` | `/refine CRAFT-REFINE-002` | Schema design consumes these fields without inventing new categories. | Example rows include schema-like columns. | Examples provide the skeleton for schema fields. |
| ENA-VALID-001 | enabler | `validation_enabler` | `ledger.qa_evidence_gate` | `validator` | `qa`, `auditor` | GATE-TYPES-001 | CTX-SCHEMA | active | refined | `validator` | manual review | Reviewer can trace each required example to a row. | Gate row `GATE-TYPES-001`. | Validation evidence enables schema refinement. |

## Cross-Context Relations

| relation_id | source_id | target_id | type | status | reason | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| REL-CONTAINS-001 | CTX-CRAFT | CTX-LEDGER | contains | active | Recursive Ledger MVP is part of Craft development. | [DURABLE-SESSION-CONTEXT.md](DURABLE-SESSION-CONTEXT.md) |
| REL-CONTAINS-002 | CTX-LEDGER | CTX-TYPES | contains | active | Type/lane model belongs to recursive ledger MVP. | [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) |
| REL-BLOCKS-001 | CTX-TYPES | CTX-SCHEMA | blocks | active | Schema needs examples before fields stabilize. | `BLK-SCHEMA-001` |
| REL-BLOCKS-002 | CTX-SCHEMA | CTX-SCORING | blocks | active | Scoring depends on schema fields. | `BLK-SCORING-001` |
| REL-ENABLES-001 | ART-EXAMPLES | CTX-SCHEMA | enables | active | Examples can now drive schema refinement. | `ENA-TECH-001` |

## Blocker Refinement Walkthrough

`BLK-RAW-001` demonstrates the required lifecycle.

Initial state:

```text
raw blocker: "cross-context blockers/enablers are unclear"
```

Refinement step:

```text
base_type: design_blocker
context_type: ledger.cross_context_relation_blocker
primary_lane: blocker_refiner
secondary_lanes: tech, business
closure_condition: refine source/target relation semantics, then assign final primary lane
delegation_route: /refine
```

Allowed next state:

```text
raw -> typed -> refined
```

Disallowed state:

```text
raw -> resolved
```

This shows why `blocker_refiner` is not the same thing as the final owner. The refiner prepares the blocker so `tech`, `business`, `auditor`, or another lane can resolve or validate it with evidence.

## Coordination Example

`BLK-RAW-001` needs multiple lanes:

| Lane | Why It Is Needed |
| --- | --- |
| `blocker_refiner` | Clarifies the blocker before resolution. |
| `tech` | Determines whether relation semantics are implementable in the schema. |
| `business` | Confirms whether cross-context blocker/enabler meaning matches the operator's project-management intent. |

The ledger should treat this as a coordination need, not silently pick one lane.

## Review Notes

Potential refinements:

- `owning lane` in artifact blockers/enablers may need to become a real lane or a schema rule.
- `blocker_refiner` works better as a role-like lane than as a domain lane; the schema should allow lifecycle lanes and expertise lanes together.
- `auditor` and `validator` are close but not identical: validator confirms evidence satisfies a gate; auditor checks trace, provenance, and process.

## Result

- Status: pass
- Reason: The example set covers every required case in `CRAFT-REFINE-001` and exposes schema decisions for `CRAFT-REFINE-002`.
