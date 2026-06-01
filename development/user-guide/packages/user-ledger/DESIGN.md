# User Ledger Design

## Invoke Result

- Mode: full authoring package, design slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/user-ledger/`
- Phase status: `pass`
- Mode contract: `spells/invoke/design.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Next route: `sigil-development`

## View 1: Context

`user-ledger` is the memory boundary for the User/Translate/Guide stack.

```text
User Ledger
  -> read handles for Translate and Guide
  -> receipt intake from Translate and Guide
  -> user-local glossary and concept states
  -> protected visibility rules
```

## View 2: High-Level Structure

| Component | Responsibility |
| --- | --- |
| Ledger schema | Defines row families and required fields. |
| Fixture ledger | Human-readable seed rows for validation. |
| Receipt intake | Accepts proposed updates from Translate/Guide. |
| Mastery gate | Prevents passive confirmation from becoming mastery. |
| Visibility policy | Controls local storage, export, reset, and promotion boundaries. |

## View 3: Low-Level Components

Candidate row families:

- `profile_seed`
- `domain_anchor`
- `vocabulary_preference`
- `concept_state`
- `receipt_ref`
- `glossary_entry`
- `residue`
- `visibility_rule`

Minimum `concept_state` statuses:

- `unknown`
- `exposed`
- `clarified`
- `practiced`
- `transferable`
- `mastered`
- `stale`

## View 4: Workflow Process

```text
install or session evidence
  -> profile/domain/vocabulary seed
  -> Translate or Guide reads handles
  -> Translate or Guide emits receipt
  -> user-ledger validates update proposal
  -> update concept state, glossary, preference, or residue
```

## View 5: Decision Flow

| Condition | Decision |
| --- | --- |
| Receipt proposes mastered state without active evidence. | Downgrade to `clarified` or reject. |
| Receipt includes failed analogy. | Add residue and avoidance/preference note. |
| Receipt proposes canonical definition update. | Block; route to Inventory/Ontology owner separately. |
| User requests reset/export. | Use visibility policy; runtime implementation deferred. |

## View 6: Dependency Interface

| Dependency | Direction | Contract |
| --- | --- | --- |
| Translate | reads/writes via receipt | Reads vocabulary/domain handles; returns translation receipts. |
| Guide | reads/writes via receipt | Reads concept states; returns guide receipts and mastery prompts. |
| Inventory/Ontology | outbound only | User glossary is local unless separate promotion review occurs. |

## Design Decisions

- User ledger owns memory; it does not own explanation or translation behavior.
- Receipts store summaries and evidence, not full transcripts by default.
- `clarification_turns` is interaction friction, not a user ability score.
