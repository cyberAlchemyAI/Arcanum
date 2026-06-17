# Craft Recursive Ledger

## Purpose

This is the first human-readable ledger fixture for the Craft recursive-ledger MVP.

Schema authority lives in [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml). This Markdown ledger instantiates that schema so the current Craft development state can be reviewed before generated indexes, scoring, runtime commands, or role delegation automation exist.

## Control Fields

| Field | Value |
| --- | --- |
| ledger_id | `craft.recursive_ledger.fixture` |
| schema_ref | [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml) |
| schema_version | `0.1.0` |
| owner_context_id | `CTX-LEDGER` |
| status | `active-fixture` |
| generated_index | `deferred` |
| created_by_task | `CRAFT-MVP-001` |

## Context Rows

| context_id | parent_id | title | purpose | stage | gate | next_move | owned_artifacts | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CTX-CRAFT | root | Craft Development | Develop Craft as an operational method and candidate capability. | design | flag | Execute the recursive-ledger MVP, then decide broader Craft architecture route. | ART-SESSION-LEDGER, ART-INITIAL-DEFINITION, ART-MVP-DEFINE, ART-MVP-DESIGN, ART-MVP-WORK-PACK | Candidate package only; no canonical promotion yet. |
| CTX-LEDGER | CTX-CRAFT | Recursive Ledger MVP | Create a YAML-backed ledger for nested contexts, artifacts, lifecycle state, blockers, gates, enablers, decisions, and cross-context relations. | validate | pass | Sync package state in CRAFT-MVP-004. | ART-LEDGER-SCHEMA, ART-LEDGER, ART-MVP-LAYERING, ART-MVP-WORK-PACK, ART-LEDGER-VALIDATION | Current MVP context. |
| CTX-TYPES | CTX-LEDGER | Type And Lane Model | Stabilize condition types, operational lanes, role hints, and blocker refinement. | validate | pass | Use type/lane rows as seed evidence for ledger fixture and validation. | ART-TYPE-SYSTEM, ART-EXAMPLES | Refined by CRAFT-REFINE-001. |
| CTX-SCHEMA | CTX-LEDGER | Ledger Schema | Define YAML schema authority plus Markdown fixture shape for recursive ledger rows. | validate | pass | Validate fixture rows against YAML rules. | ART-SCHEMA-RATIONALE, ART-LEDGER-SCHEMA | Refined by CRAFT-REFINE-002 and refreshed to YAML. |
| CTX-FIXTURE | CTX-LEDGER | Ledger Fixture | Instantiate the schema as the first readable Craft operational ledger. | validate | pass | Validate lifecycle rows in CRAFT-MVP-003. | ART-LEDGER | Created by CRAFT-MVP-001 and lifecycle traces added by CRAFT-MVP-002. |
| CTX-VALIDATION | CTX-LEDGER | Ledger Validation | Manually validate schema rules, blocker lifecycle, waiver behavior, and open flags. | validate | pass | Sync package state in CRAFT-MVP-004. | ART-LEDGER-VALIDATION | Completed by CRAFT-MVP-003. |
| CTX-SCORING | CTX-LEDGER | Priority Scoring | Later rank contexts by blockers, enablers, readiness, lane load, and downstream impact. | idea | block | Wait for multiple valid ledger states. | none | Explicitly deferred. |
| CTX-RUNTIME-SIDE-THREAD | CTX-CRAFT | Runtime Interface Side Thread | Track runtime/refine interface artifacts without making them Craft MVP acceptance criteria. | design | flag | Keep linked as side-thread context only. | ART-REFINE-RUNTIME-STRATEGY, ART-SKILL-RUNTIME-HANDOFF | Split from core Craft MVP. |

## Artifact Rows

| artifact_id | owner_context_id | path | artifact_type | status | notes |
| --- | --- | --- | --- | --- | --- |
| ART-SESSION-LEDGER | CTX-CRAFT | `development/craft/SESSION-LEDGER.md` | session-ledger | active | Durable artifact, decision, gap, and next-route ledger. |
| ART-INITIAL-DEFINITION | CTX-CRAFT | `development/craft/CRAFT-INITIAL-DEFINITION.md` | source-baseline | active | Initial Craft definition and research synthesis. |
| ART-CRAFT-TUTORIAL | CTX-CRAFT | `development/craft/CRAFT-TUTORIAL.md` | tutorial | active | First-reader tutorial using Guide sequencing and plain-language composition. |
| ART-CRAFT-TUTORIAL-HTML | CTX-CRAFT | `development/craft/CRAFT-TUTORIAL.html` | tutorial-html | active | Visual tutorial companion for readers new to Craft. |
| ART-RECURSIVE-LEDGER-DEFINE | CTX-LEDGER | `development/craft/CRAFT-RECURSIVE-LEDGER-DEFINE.md` | define-baseline | active | Broader feature definition for recursive ledger. |
| ART-RECURSIVE-LEDGER-GLOSSARY | CTX-LEDGER | `development/craft/CRAFT-RECURSIVE-LEDGER-GLOSSARY.md` | glossary | active | Candidate recursive-ledger vocabulary. |
| ART-TYPE-SYSTEM | CTX-TYPES | `development/craft/CRAFT-LEDGER-TYPE-SYSTEM.md` | type-system | active | Condition types, lanes, role hints, and blocker refinement rule. |
| ART-REFINE-WORK-PACK | CTX-LEDGER | `development/craft/WORK-PACK.md` | work-pack | closed | Completed refinement work-pack for CRAFT-REFINE-001 and CRAFT-REFINE-002. |
| ART-EXAMPLES | CTX-TYPES | `development/craft/CRAFT-LEDGER-TYPE-EXAMPLES.md` | examples | active | Refined typed examples. |
| ART-SCHEMA-RATIONALE | CTX-SCHEMA | `development/craft/CRAFT-RECURSIVE-LEDGER-DESIGN.md` | schema-rationale | active | Rationale and Markdown fixture guidance now pointing at YAML schema authority. |
| ART-LEDGER-SCHEMA | CTX-SCHEMA | `development/craft/CRAFT-LEDGER-SCHEMA.yml` | yaml-schema | active | Structured schema authority for row families, fields, enums, and validation rules. |
| ART-MVP-DEFINE | CTX-CRAFT | `development/craft/CRAFT-MVP-DEFINE.md` | invoke-define | active | Define artifact for the file-backed recursive-ledger MVP. |
| ART-MVP-DESIGN | CTX-CRAFT | `development/craft/CRAFT-MVP-DESIGN.md` | invoke-design | active | Six-view architecture and plan handoff notes. |
| ART-MVP-DESIGN-HTML | CTX-CRAFT | `development/craft/CRAFT-MVP-DESIGN.html` | visual-design | active | Visual HTML companion for the MVP architecture. |
| ART-MVP-LAYERING | CTX-LEDGER | `development/craft/CRAFT-MVP-IMPLEMENTATION-LAYERING.md` | implementation-layering | active | L0-L2 boundaries for fixture, blocker lifecycle proof, and validation. |
| ART-MVP-WORK-PACK | CTX-LEDGER | `development/craft/CRAFT-MVP-WORK-PACK.md` | work-pack | active | Execution plan for LEDGER.md, blocker traces, validation, and sync. |
| ART-LEDGER | CTX-FIXTURE | `development/craft/LEDGER.md` | ledger-fixture | active | This artifact. |
| ART-LEDGER-VALIDATION | CTX-VALIDATION | `development/craft/LEDGER-VALIDATION.md` | validation | active | Manual validation artifact created by CRAFT-MVP-003. |
| ART-REFINE-RUNTIME-STRATEGY | CTX-RUNTIME-SIDE-THREAD | `development/craft/CRAFT-REFINE-RUNTIME-STRATEGY.md` | side-thread-strategy | active | Runtime strategy candidate; not core MVP acceptance. |
| ART-SKILL-RUNTIME-HANDOFF | CTX-RUNTIME-SIDE-THREAD | `development/craft/ARCANUM-SKILL-RUNTIME-HANDOFF.md` | handoff | active | Handoff for a separate runtime interface thread. |

## Relation Rows

| relation_id | source_id | target_id | type | status | reason | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| REL-CONTAINS-001 | CTX-CRAFT | CTX-LEDGER | contains | active | Recursive Ledger MVP is part of Craft development. | ART-MVP-DEFINE |
| REL-CONTAINS-002 | CTX-LEDGER | CTX-TYPES | contains | active | Type/lane model belongs to the recursive-ledger MVP. | ART-TYPE-SYSTEM |
| REL-CONTAINS-003 | CTX-LEDGER | CTX-SCHEMA | contains | active | Schema authority belongs to the recursive-ledger MVP. | ART-LEDGER-SCHEMA |
| REL-CONTAINS-004 | CTX-LEDGER | CTX-FIXTURE | contains | active | Ledger fixture instantiates the schema. | ART-LEDGER |
| REL-CONTAINS-005 | CTX-LEDGER | CTX-VALIDATION | contains | active | Validation is the next layer after fixture and blocker traces. | ART-MVP-WORK-PACK |
| REL-CONTAINS-006 | CTX-LEDGER | CTX-SCORING | contains | active | Priority scoring is a deferred child context. | BLK-SCORING-001 |
| REL-INFORMS-001 | ART-EXAMPLES | ART-LEDGER-SCHEMA | informs | resolved | Type examples shaped the YAML schema contract. | ART-SCHEMA-RATIONALE |
| REL-INFORMS-002 | ART-LEDGER-SCHEMA | ART-LEDGER | informs | active | YAML schema controls this Markdown fixture. | CRAFT-MVP-001 |
| REL-ENABLES-001 | ART-LEDGER-SCHEMA | CTX-FIXTURE | enables | active | A structured schema makes fixture instantiation possible. | ENA-SCHEMA-001 |
| REL-ENABLES-002 | ART-LEDGER | CTX-VALIDATION | enables | active | Validation can begin once blocker traces are added to this fixture. | CRAFT-MVP-002 |
| REL-BLOCKS-001 | BLK-BLOCKER-TRACE-001 | CTX-VALIDATION | blocks | resolved | Full validation needed blocker lifecycle and waiver examples; traces now exist. | BLK-RESOLVED-TRACE-001 |
| REL-BLOCKS-002 | CTX-SCHEMA | CTX-SCORING | blocks | active | Scoring depends on multiple valid ledger states. | BLK-SCORING-001 |
| REL-INFORMS-003 | ART-REFINE-RUNTIME-STRATEGY | CTX-RUNTIME-SIDE-THREAD | informs | active | Runtime strategy is tracked as side-thread context. | SESSION-LEDGER |
| REL-INFORMS-004 | DEC-WAIVER-AUDIT-001 | BLK-WAIVED-AUDIT-001 | informs | active | Waiver decision explicitly permits the blocker to close without normal refinement. | CRAFT-MVP-002 |

## Typed Item Rows

| item_id | kind | base_type | context_type | primary_lane | secondary_lanes | source_id | target_id | status | refinement_status | default_role | delegation_route | closure_condition | evidence | decision_ref | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-BLOCKER-TRACE-001 | blocker | `sequence_blocker` | `ledger.blocker_refinement_gate` | `planner` | `blocker_refiner`, `auditor` | ART-LEDGER | CTX-VALIDATION | resolved | resolved | `planner` | `task-session CRAFT-MVP-002` | `LEDGER.md` includes raw or typed, refined, resolved, and waived blocker traces. | BLK-RAW-RELATION-001, BLK-REFINED-SCHEMA-001, BLK-RESOLVED-TRACE-001, BLK-WAIVED-AUDIT-001 | none | Lifecycle trace blocker is closed by the rows added in CRAFT-MVP-002. |
| BLK-SCORING-001 | blocker | `sequence_blocker` | none | `planner` | `business`, `tech` | CTX-SCHEMA | CTX-SCORING | active | refined | `planner` | deferred | Multiple valid ledger states exist and scoring inputs are evident. | ART-MVP-DEFINE | none | Scoring before validated ledger states would overfit unknown fields. |
| BLK-RUNTIME-SCOPE-001 | blocker | `authority_blocker` | none | `governance` | `operations`, `tech` | CTX-RUNTIME-SIDE-THREAD | CTX-LEDGER | active | refined | `governance_owner` | separate thread | Runtime/refine interface decisions remain outside Craft MVP acceptance. | ART-SKILL-RUNTIME-HANDOFF | none | Runtime work is related but not owned by the ledger MVP task sequence. |
| BLK-RAW-RELATION-001 | blocker | `design_blocker` | `ledger.cross_context_relation_blocker` | `blocker_refiner` | `tech`, `business` | CTX-FIXTURE | CTX-VALIDATION | active | raw | `blocker_refiner` | `/refine` | Clarify whether cross-context relation semantics need additional fields before final validation. | CRAFT-MVP-002 | none | Raw blocker remains unresolved and demonstrates the blocked shortcut. |
| BLK-REFINED-SCHEMA-001 | blocker | `validation_blocker` | `ledger.schema_shape_gate` | `validator` | `tech`, `qa` | ART-LEDGER | CTX-VALIDATION | resolution_proposed | refined | `validator` | manual review | Confirm the fixture rows satisfy YAML schema fields and relation references. | CRAFT-MVP-001 validation output | none | Refined blocker is ready for validation review but not automatically resolved. |
| BLK-RESOLVED-TRACE-001 | blocker | `validation_blocker` | `ledger.blocker_refinement_gate` | `validator` | `qa`, `auditor` | ART-LEDGER | CTX-FIXTURE | resolved | resolved | `validator` | none | Fixture includes raw, refined, resolved, and waived blocker examples with evidence. | CRAFT-MVP-002 ledger rows | none | This row proves a resolved blocker with closure evidence. |
| BLK-WAIVED-AUDIT-001 | blocker | `authority_blocker` | `ledger.audit_trace_gate` | `auditor` | `governance`, `validator` | ART-LEDGER | CTX-VALIDATION | waived | waived | `governance_reviewer` | waiver decision | Accept audit-trace strictness as deferred for MVP validation while preserving explicit decision evidence. | DEC-WAIVER-AUDIT-001 | DEC-WAIVER-AUDIT-001 | This row proves a waived blocker linked to a waiver decision. |
| GATE-SCHEMA-001 | gate | `validation_gate` | `ledger.schema_shape_gate` | `validator` | `tech` | ART-LEDGER-SCHEMA | CTX-SCHEMA | pass | refined | `validator` | manual review | YAML parses and exposes five row families plus validation rules. | ART-LEDGER-SCHEMA | none | Schema authority is structured enough to instantiate the fixture. |
| GATE-FIXTURE-001 | gate | `artifact_gate` | none | `validator` | `qa` | ART-LEDGER | CTX-FIXTURE | pass | refined | `validator` | manual review | Ledger has all five row-family sections and current artifact rows. | CRAFT-MVP-001 | none | Fixture exists and can be reviewed. |
| GATE-VALIDATION-001 | gate | `readiness_gate` | none | `validator` | `qa`, `auditor` | CTX-FIXTURE | CTX-VALIDATION | pass | refined | `validator` | `task-session CRAFT-MVP-003` | Blocker lifecycle traces exist before full validation. | CRAFT-MVP-002 | none | CRAFT-MVP-003 can now validate schema and lifecycle rules. |
| ENA-SCHEMA-001 | enabler | `design_enabler` | `ledger.schema_shape_gate` | `tech` | `validator` | ART-LEDGER-SCHEMA | ART-LEDGER | active | refined | `architect` | none | YAML schema remains the row-family authority. | ART-LEDGER-SCHEMA | none | The YAML contract enables consistent ledger fixture rows. |
| ENA-EXAMPLES-001 | enabler | `validation_enabler` | `ledger.qa_evidence_gate` | `validator` | `qa`, `auditor` | ART-EXAMPLES | ART-LEDGER | active | refined | `validator` | none | Example rows remain traceable to fixture rows. | ART-EXAMPLES | none | Examples provide realistic seed evidence for the fixture. |
| ENA-PLAN-001 | enabler | `sequence_enabler` | none | `planner` | `tech` | ART-MVP-WORK-PACK | CTX-FIXTURE | active | refined | `planner` | `task-session` | CRAFT-MVP-001 task contract remains stable. | ART-MVP-WORK-PACK | none | The work-pack makes the fixture task executable. |

## Decision Rows

| decision_id | scope_id | decision_type | selected | rationale | evidence | status |
| --- | --- | --- | --- | --- | --- | --- |
| DEC-SCHEMA-FORMAT-001 | ART-LEDGER-SCHEMA | selection | YAML schema contract plus Markdown ledger fixture | The schema should be structured and machine-readable, while the first ledger should stay human-reviewable. | User correction: "schema should be in yml" | active |
| DEC-MVP-BOUNDARY-001 | CTX-LEDGER | deferral | defer scoring, generated indexes, runtime integration, and role delegation automation | The MVP should prove schema and ledger behavior before adding automation. | ART-MVP-DEFINE | active |
| DEC-RUNTIME-SPLIT-001 | CTX-RUNTIME-SIDE-THREAD | selection | keep runtime/refine interface as side-thread context | Runtime interface work spans command adapters and observation envelopes, so it should not be core Craft MVP acceptance. | ART-SKILL-RUNTIME-HANDOFF | active |
| DEC-REFINE-HISTORY-001 | ART-REFINE-WORK-PACK | approval | preserve completed refinement work-pack as historical evidence | The first work-pack completed CRAFT-REFINE-001 and CRAFT-REFINE-002 and should not be overwritten by MVP execution. | WORK-PACK.md change log | active |
| DEC-WAIVER-AUDIT-001 | BLK-WAIVED-AUDIT-001 | waiver | defer strict audit-trace blocker for MVP validation | The MVP must prove waiver representation, but strict audit-trace policy belongs to broader validation design after the first ledger fixture is reviewed. | CRAFT-MVP-002 | active |

## Side-Thread Notes

Runtime/refine-interface artifacts are visible in this ledger so Craft can remember the dependency shape, but they are not blockers for `CRAFT-MVP-001` or `CRAFT-MVP-002`.

Core MVP execution remains:

```text
CRAFT-MVP-001 -> CRAFT-MVP-002 -> CRAFT-MVP-003 -> CRAFT-MVP-004
```

## Deferred Index

`ledger-index.json` remains deferred. The next validation task should decide whether a generated index is useful after the Markdown fixture and blocker lifecycle traces pass review.
