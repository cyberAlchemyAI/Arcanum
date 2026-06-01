# Refine Result: User Ledger And Guide

## Verdict

Status: `pass-with-runtime-caveat`

The refinement identifies a coherent first unit for the new framework part: `User Learning Ledger + Guide Interaction Receipt`.

The local dispatch schema validates, and the run preserves the canonical ten-stage refine evidence surface. Full command-backed execution is caveated because `dispatch-spec` and `runtime-handoff` are not registered local Arcanum commands.

## Selected Design

`User` should start as a protected learning ledger, not a broad identity profile.

`Guide` should start as an interaction loop that adapts explanation moves from evidence and writes bounded receipts after blocker resolution or clarification confirmation.

The first contract is:

```text
Guide section
  -> explanation strategy
  -> user response
  -> clarification friction
  -> active evidence if mastery is claimed
  -> guide receipt
  -> proposed User ledger update
  -> glossary entry or residue
```

## Candidate Family

### User Sigil Candidates

| Candidate | Purpose |
| --- | --- |
| `user-ledger` | Own the protected learning ledger schema and update rules. |
| `user-profile-seed` | Store optional install-game profile seed rows. |
| `user-vocabulary-map` | Track vocabulary preferences, aliases, disliked terms, and source-domain language. |
| `user-mastery-glossary` | Store user-local mastered definitions with evidence. |

### Guide Sigil Candidates

| Candidate | Purpose |
| --- | --- |
| `guide-section-receipt` | Record what Guide tried, what worked, what failed, and what update is proposed. |
| `guide-bridge-selector` | Choose source-domain bridges based on the User ledger. |
| `guide-concept-ladder` | Move from concrete example to meta pattern to abstract primitive. |

### Spell Candidates

| Candidate | Purpose |
| --- | --- |
| `cyberalchemy-install-game` | Elicit prior domains, vocabulary anchors, primitive familiarity, and curiosity paths. |
| `guide-clarify-blocker` | Resolve a blocker and create a receipt for ledger improvement. |
| `guide-domain-bridge` | Explain across domains, with mapping limits. |
| `guide-master-definition` | Add a user glossary entry after active evidence. |
| `guide-generalize` | Help the user move from a specific example to reusable system thinking. |

## Learning Techniques To Encode

| Technique | Guide Behavior |
| --- | --- |
| Scaffolding/fading | Start supportive; reduce support when user can explain or transfer. |
| Analogical encoding | Compare multiple examples to reveal the shared schema. |
| Self-explanation | Ask the user to explain why the example works. |
| Retrieval practice | Ask for recall or teach-back before mastery. |
| Knowledge tracing | Track concept state over time with transparent statuses, not hidden diagnosis. |
| Concept mapping | Link primitives and prerequisites across domains. |

## First Ledger Shape

Minimum row families:

- `profile_seed`
- `domain_anchor`
- `vocabulary_preference`
- `concept_state`
- `guide_receipt`
- `bridge_pattern`
- `glossary_entry`
- `residue`
- `consent_visibility`

Key rule: `clarification_turns` describes interaction friction, not user ability.

Key rule: glossary mastery requires active evidence: teach-back, retrieval, transfer, blocker resolution with explanation, or correct contrast against a nearby concept.

## CyberAlchemy Install Game

The install game should be optional, replayable, and short. It should create profile seed evidence by asking the user to pick domains, compare translation cards, sort primitive cards, mark confidence, and try one transfer card.

It should help the system learn where to start, not decide who the user is.

## Concept Library

Start with a small software/systems primitive seed:

- data,
- schema,
- form,
- API,
- request/response,
- axios,
- constitution,
- behavior,
- system.

The library should be extensible. If a domain library is missing, Guide can still produce a one-off bridge receipt and leave residue for future library growth.

## Validation Fixtures

Use these examples as the first test corpus:

1. Explain a software architecture decision in sales terms.
2. Explain a scientific formula in software engineering terms.
3. Explain a civil construction plan in musician terms.
4. Confirm that passive "I understand" creates `clarified`, not `mastered`.
5. Confirm that teach-back plus transfer can create `mastered`.
6. Confirm that a failed analogy creates residue and avoids repeating the same bridge blindly.

## Recommended Next Routes

1. Run `invoke define/design/plan` for `development/user-guide/`.
2. Create candidate schemas: `USER-LEDGER-SCHEMA.yml` and `GUIDE-RECEIPT-SCHEMA.yml`.
3. Run `task-session` for the validation fixture corpus.
4. After fixtures pass, run `sigil-development` for `user-ledger` and `guide-section-receipt`.
5. After sigil contracts stabilize, run `spellcraft` for `cyberalchemy-install-game` and `guide-domain-bridge`.

## Runtime Caveat

The dispatch route validates locally, but this run did not honestly execute every command-backed stage through `tools/arcanum --exec` because `dispatch-spec` and `runtime-handoff` commands are absent from the local command surface.
