# Guide Dispatch Governance

## Purpose

Define the first bounded rules for Guide research and subagent dispatch.

## Dispatch Principle

Guide can dispatch research, x-ray, Inventory lookup, or subagents only when the guide route cannot proceed from available context.

Guide must record:

- why dispatch is needed,
- which capability is called,
- input boundary,
- expected output,
- budget,
- stop condition,
- evidence returned.

## Dispatch Classes

| Class | Use When | Owner | Runtime Status |
| --- | --- | --- | --- |
| `xray` | Hidden architecture or workflow structure blocks explanation. | x-ray | future callable |
| `inventory_lookup` | Existing concept/artifact definitions may exist. | inventory | future callable |
| `bounded_research` | External facts are missing. | research/subagent | gated |
| `translate` | Vocabulary/domain bridge is needed. | translate | callable after Translate package |
| `context_builder` | Source context must be selected before explanation. | context-builder | callable |

## Budget Rules

| Rule ID | Rule |
| --- | --- |
| GDG-001 | Static route fixtures cannot execute live subagents. |
| GDG-002 | Runtime Guide dispatch must name a budget before calling research/subagents. |
| GDG-003 | Missing target-domain definition routes to Translate or Inventory before explanation. |
| GDG-004 | If dispatch returns uncertainty, Guide must preserve it as a flag, not smooth it into certainty. |
| GDG-005 | User ledger updates remain proposals until User accepts or validates them. |

## Stop Conditions

Guide must stop or flag when:

- target context is missing,
- Translate returns `missing_target_definition`,
- research output is contradictory,
- requested dispatch exceeds budget,
- user memory write would happen without User ledger validation.
