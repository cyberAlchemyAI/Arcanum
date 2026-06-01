# User Ledger Mastery Fixtures

## Purpose

Prove that User ledger distinguishes passive clarification from active mastery.

## Fixture A: Passive Confirmation

Receipt:

| Field | Value |
| --- | --- |
| receipt_ref_id | URR-GUIDE-PASSIVE-001 |
| source | guide |
| source_receipt_id | GUIDE-RECEIPT-PASSIVE-001 |
| proposed_update | User says "I understand schema now"; set schema to mastered. |
| status | rejected |

Ledger decision:

| Field | Value |
| --- | --- |
| concept | schema |
| evidence_type | user_confirmation |
| allowed_status | clarified |
| blocked_status | mastered |
| reason | Passive confirmation does not prove retrieval, transfer, or contrast. |

## Fixture B: Teach-Back

Receipt:

| Field | Value |
| --- | --- |
| receipt_ref_id | URR-GUIDE-TEACHBACK-001 |
| source | guide |
| source_receipt_id | GUIDE-RECEIPT-TEACHBACK-001 |
| proposed_update | User explains schema as "the rule for what shape data or an artifact must have before the system accepts it." |
| status | accepted |

Ledger decision:

| Field | Value |
| --- | --- |
| concept | schema |
| evidence_type | teach_back |
| allowed_status | mastered |
| reason | User recalled and explained the primitive in target-domain language. |

## Fixture C: Transfer

Receipt:

| Field | Value |
| --- | --- |
| receipt_ref_id | URR-TRANSLATE-TRANSFER-001 |
| source | translate |
| source_receipt_id | TRANSLATE-RECEIPT-TRANSFER-001 |
| proposed_update | User maps "schema" from software data validation to sales qualification fields. |
| status | accepted |

Ledger decision:

| Field | Value |
| --- | --- |
| concept | schema |
| evidence_type | transfer |
| allowed_status | transferable |
| reason | User applied the primitive to a different domain. |

## Fixture D: Failed Analogy

Receipt:

| Field | Value |
| --- | --- |
| receipt_ref_id | URR-TRANSLATE-FAILED-001 |
| source | translate |
| source_receipt_id | TRANSLATE-RECEIPT-FAILED-001 |
| proposed_update | Music harmony analogy for architecture dependency boundaries confused the user. |
| status | accepted |

Ledger decision:

| Field | Value |
| --- | --- |
| residue_kind | failed_analogy |
| vocabulary_preference | avoid harmony analogy for dependency boundaries unless user asks |
| mastery_update | none |
| reason | Failed analogy is future-route evidence, not mastery evidence. |
