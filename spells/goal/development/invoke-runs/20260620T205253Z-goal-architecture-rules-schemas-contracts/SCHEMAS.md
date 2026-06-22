---
artifact_id: GOAL-SCHEMAS-001
artifact_type: schema-inventory
target: arcanum/spells/goal
status: promoted
created_at: 2026-06-20
---

# Goal Spell Schemas

## Schema Policy

These schemas are public generic goal spell handoff artifact schemas. They do
not replace behavioral contracts. A schema proves shape; the corresponding
contract decides authority, meaning, and pass/block behavior.

## Schema Inventory

| Schema | Path | Covers | Contract |
| --- | --- | --- | --- |
| Decision profile schema | `arcanum/spells/goal/decision-profile.schema` | Public runtime policy shape and neutral defaults. | Decision profile boundary. |
| Frontier snapshot schema | `arcanum/spells/goal/schemas/frontier-snapshot.schema.json` | Per-round Craft frontier snapshot. | Frontier contract. |
| Execution receipt schema | `arcanum/spells/goal/schemas/execution-receipt.schema.json` | Terminal delegated owner receipt. | Execution contract. |
| Staged delta schema | `arcanum/spells/goal/schemas/staged-delta.schema.json` | Reviewable source-change proposal. | Staging contract. |
| Approval token schema | `arcanum/spells/goal/schemas/approval-token.schema.json` | Batch-specific apply authorization. | Approval contract. |
| Goal loop result schema | `arcanum/spells/goal/schemas/goal-loop-result.schema.json` | Final spell output contract. | Goal Loop Result output contract. |
| Telemetry signal schema | `arcanum/spells/goal/schemas/telemetry-signal.schema.json` | Round/final observability signal. | Telemetry contract. |

## Common Enums

| Name | Values |
| --- | --- |
| Result status | `PASS`, `STOP`, `BLOCK`, `FLAG` |
| Risk tier | `T0`, `T1`, `T2`, `T3` |
| Receipt status | `closed`, `blocked`, `timed-out`, `handed-off` |
| Delta operation | `add`, `update`, `delete`, `move`, `annotate` |
| Promotion state | `staged`, `held`, `approved`, `rejected`, `applied`, `blocked` |
| Approval state | `approved`, `rejected`, `held`, `expired` |

## Validation Commands

```bash
python3 -m json.tool arcanum/spells/goal/decision-profile.schema
find arcanum/spells/goal/schemas -name '*.json' -print -exec python3 -m json.tool {} \; >/tmp/goal-schema-parse.log
```

## Open Schema Questions

| Question | Status | Route |
| --- | --- | --- |
| Should schemas be promoted out of the Invoke run into `spells/goal/schemas/`? | resolved | Promoted during Spellcraft register/install. |
| Should Dispatch Spec route shape be referenced or embedded? | deferred | Use reference first; embed only if implementation needs a local extension. |
| Should Craft ledger row schemas be imported? | no | Craft owns ledger schema. Goal only consumes frontier/staging artifacts. |
