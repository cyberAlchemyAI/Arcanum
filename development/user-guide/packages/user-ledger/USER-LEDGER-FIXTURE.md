# User Ledger Fixture

## Purpose

First human-readable fixture for `USER-LEDGER-SCHEMA.yml`.

## Control Fields

| Field | Value |
| --- | --- |
| fixture_id | `user-ledger.fixture.001` |
| schema_ref | `USER-LEDGER-SCHEMA.yml` |
| status | candidate |
| runtime_store | deferred |

## Profile Seed Rows

| profile_seed_id | source | summary | visibility |
| --- | --- | --- | --- |
| UPS-INSTALL-001 | install_game | User selected sales, software, and music as familiar domains during onboarding fixture. | local_private |

## Domain Anchor Rows

| domain_anchor_id | domain | confidence | evidence | visibility |
| --- | --- | --- | --- | --- |
| UDA-SALES-001 | sales | high | User can reason about pipeline, qualification, offer, objection, and closing. | local_private |
| UDA-MUSIC-001 | music | medium | User can reason about rhythm, harmony, arrangement, and rehearsal. | local_private |

## Vocabulary Preference Rows

| vocabulary_preference_id | preference_type | term_or_style | action | evidence |
| --- | --- | --- | --- | --- |
| UVP-CONCRETE-FIRST-001 | style | concrete example before abstraction | prefer | Prior guide refinement requested moving from specific to meta to abstract. |
| UVP-NO-HIDDEN-JUDGMENT-001 | safety | clarification_turns | define carefully | Clarification count must describe interaction friction, not user ability. |

## Concept State Rows

| concept_state_id | concept | status | evidence_type | evidence_ref | last_receipt_ref |
| --- | --- | --- | --- | --- | --- |
| UCS-SCHEMA-001 | schema | clarified | user_confirmation | User recognized schema as a shape rule after explanation. | URR-GUIDE-001 |
| UCS-API-001 | api | exposed | none | Mentioned as software primitive; no active evidence yet. | none |

## Receipt Reference Rows

| receipt_ref_id | source | source_receipt_id | proposed_update | status |
| --- | --- | --- | --- | --- |
| URR-GUIDE-001 | guide | GUIDE-RECEIPT-FIXTURE-001 | Set schema concept state to clarified after passive confirmation. | accepted |
| URR-TRANSLATE-001 | translate | TRANSLATE-RECEIPT-FIXTURE-001 | Prefer sales pipeline terms when explaining software architecture. | proposed |

## Glossary Entry Rows

| glossary_entry_id | term | user_definition | concept_state_ref | canonical_promotion_status |
| --- | --- | --- | --- | --- |
| UGE-SCHEMA-001 | schema | A shape rule for what counts as valid data or artifact structure. | UCS-SCHEMA-001 | user-local-only |

## Residue Rows

| residue_id | kind | summary | next_action |
| --- | --- | --- | --- |
| URS-API-001 | open_question | API has been introduced but not practiced through teach-back or transfer. | Guide should ask for a small request/response example. |

## Visibility Rule Rows

| visibility_rule_id | scope | rule | enforcement |
| --- | --- | --- | --- |
| UVR-LOCAL-001 | all user-ledger rows | Store as local protected context by default. | Do not export or promote without explicit user action. |
| UVR-CANONICAL-001 | glossary_entry | User-local glossary is not canonical Inventory/Ontology. | Block canonical promotion without owner review. |

## Fixture Review

This fixture covers all L0 row families needed for User handles:

- profile seed,
- domain anchor,
- vocabulary preference,
- concept state,
- receipt ref,
- glossary entry,
- residue,
- visibility rule.
