# Discovery To Inventory

## Identity

- Canonical ID: `discovery-to-inventory`
- Aliases: none
- Scope: library

Discovery To Inventory composes `scope-interview`, `feature-glossary`, and `inventory` so early discovery becomes persistent reusable knowledge.

## Trigger Conditions

- A user has a vague idea, brownfield project, or unclear project scope.
- Discovery findings should not disappear into chat history.
- Vocabulary and decisions should become reusable inventory entries.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| ----- | ------------- | ------------- |
| `scope-interview` | Build the discovery baseline. | greenfield, brownfield, or auto |
| `feature-glossary` | Clarify local vocabulary. | create or update |
| `inventory` | Install or update reusable knowledge entries. | install, ingest, backfill |

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| ----- | ----- | ----- | ------ | ---- | -------------- |
| 1 | `scope-interview` | project idea or repository | discovery baseline | observed, stated, and hypothesized content separated | block on unresolved scope gate |
| 2 | `feature-glossary` | discovery baseline and source docs | glossary | terms link to evidence | flag unresolved vocabulary |
| 3 | `inventory` | baseline and glossary | inventory entries | index and log updated | flag missing source coverage |
| 4 | spell report | phase outputs | discovery-to-inventory report | blockers named | report partial when discovery remains open |

## Observability

Record questions asked, decisions captured, glossary terms, entries created, unresolved scope gaps, and next discovery actions.

## Output Contract

Return a report with discovery verdict, glossary coverage, inventory updates, blockers, and recommended next discovery or planning step.