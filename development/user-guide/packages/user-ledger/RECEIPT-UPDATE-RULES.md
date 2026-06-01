# User Ledger Receipt Update Rules

## Purpose

Define how User ledger evaluates receipt update proposals from Translate, Guide, install game, or manual records.

## Update Rule Table

| Rule ID | Input | Allowed Update | Blocked Update | Reason |
| --- | --- | --- | --- | --- |
| UR-001 | Passive user confirmation such as "I understand" | `concept_state.status = clarified` | `mastered` | Passive confirmation is useful but not active mastery evidence. |
| UR-002 | Teach-back in the user's own words | `concept_state.status = mastered` when accurate enough for purpose | none | Teach-back proves recall and explanation. |
| UR-003 | Retrieval without seeing the answer | `concept_state.status = practiced` or `mastered` depending on quality | none | Retrieval is active evidence. |
| UR-004 | Transfer to a new example | `concept_state.status = transferable` or `mastered` | none | Transfer proves the concept is not tied to one analogy. |
| UR-005 | Correct contrast between neighboring concepts | `concept_state.status = mastered` when contrast is stable | none | Contrast shows boundary understanding. |
| UR-006 | Failed analogy or disliked metaphor | Add `residue` and optional `vocabulary_preference` | mastery increase | Failed bridges should guide future explanation, not inflate mastery. |
| UR-007 | Receipt proposes canonical definition update | Add local glossary note or route to owner | direct Inventory/Ontology promotion | User ledger is local memory, not canonical knowledge authority. |

## Evaluation Order

1. Check receipt source and source receipt id.
2. Check proposed update target row.
3. Check evidence type.
4. Apply mastery evidence gate.
5. Apply visibility and promotion boundary.
6. Accept, reject, or defer the proposed update.

## Mastery Evidence Gate

`mastered` requires at least one of:

- teach-back,
- retrieval,
- transfer,
- contrast,
- blocker resolution with user explanation of what changed.

`user_confirmation` alone can create at most `clarified`.
