# User Ledger Define

## Invoke Result

- Mode: full authoring package, define slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/user-ledger/`
- Phase status: `pass`
- Mode contract: `spells/invoke/define.md`
- Template/profile selection: sigil candidate family scaffold
- Next route: `sigil-development`

## Objective

Define `user-ledger` as a candidate sigil that owns protected learning-profile state for a user: prior domain anchors, vocabulary preferences, concept states, glossary mastery evidence, Guide/Translate receipts, residue, and visibility rules.

## Intent Record

The User ledger exists so Guide and Translate can adapt to the user without pretending every interaction is canonical truth or permanent identity. It should help the system learn how to explain better, not diagnose the user.

## Scope

In scope:

- local protected ledger schema,
- domain anchors,
- vocabulary preferences,
- concept state rows,
- glossary mastery evidence,
- receipt storage rules,
- consent and visibility rules,
- fixture handles usable by Translate before runtime storage exists.

Out of scope:

- Guide orchestration,
- translation logic,
- research dispatch,
- canonical Inventory/Ontology promotion,
- hidden profiling,
- persistent runtime storage implementation,
- registry or command installation.

## Core Terms

| Term | Definition |
| --- | --- |
| profile seed | Optional initial information from onboarding or install game. |
| domain anchor | A domain the user knows and can use as an explanation bridge. |
| vocabulary preference | A user-local term, alias, style, or avoided wording. |
| concept state | The user's current evidence-backed status for one concept. |
| mastery evidence | Active evidence such as teach-back, retrieval, transfer, or correct contrast. |
| receipt | Bounded record from Guide or Translate proposing a ledger update. |
| residue | Confusion, failed bridge, open question, or deferred learning gap. |

## Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| Ledger can store domain anchors without claiming identity diagnosis. | Schema rows and fixtures. |
| Ledger can store vocabulary preferences used by Translate. | `vocabulary_preference` fixture. |
| Ledger can distinguish clarified from mastered. | `concept_state` fixture with mastery evidence rule. |
| Ledger receives but does not generate Guide/Translate decisions. | Receipt boundary in design. |
| User-local glossary does not promote canonical definitions. | Promotion split in design and validation. |

## Open Gaps

- Exact persistence format is candidate-only.
- Privacy/visibility policy needs validation before runtime.
- Export/reset behavior is deferred to a later package layer.
