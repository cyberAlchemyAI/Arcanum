# Arcanum Spell: discovery to inventory

<!-- arcanum:capability-id discovery-to-inventory -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command arcanum-spell-discovery-to-inventory -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-spell-discovery-to-inventory-<UTC timestamp>`.
- `capability.id`: `discovery-to-inventory`
- `capability.kind`: `spell`
- `capability.tier`: `spell`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum spell `discovery-to-inventory` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `discovery-to-inventory`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/discovery-to-inventory/README.md

````markdown
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
````
