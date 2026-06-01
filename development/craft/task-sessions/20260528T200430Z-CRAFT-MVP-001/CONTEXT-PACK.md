# Task Session Context Pack: CRAFT-MVP-001

## Scope

- Work-pack: [CRAFT-MVP-WORK-PACK.md](../../CRAFT-MVP-WORK-PACK.md)
- Task: `CRAFT-MVP-001`
- Objective: create [LEDGER.md](../../LEDGER.md) as the first readable recursive ledger fixture from [CRAFT-LEDGER-SCHEMA.yml](../../CRAFT-LEDGER-SCHEMA.yml).
- Runtime: local
- Runtime handoff: none

## Controlling Sources

| Source | Control |
| --- | --- |
| [CRAFT-MVP-WORK-PACK.md](../../CRAFT-MVP-WORK-PACK.md) | Task contract, done criteria, write scope, and validation surface. |
| [CRAFT-LEDGER-SCHEMA.yml](../../CRAFT-LEDGER-SCHEMA.yml) | Row-family order, required fields, enums, validation rules, and blocker lifecycle. |
| [CRAFT-LEDGER-TYPE-EXAMPLES.md](../../CRAFT-LEDGER-TYPE-EXAMPLES.md) | Seed rows for contexts, artifacts, relations, typed items, and gates. |
| [CRAFT-MVP-DESIGN.md](../../CRAFT-MVP-DESIGN.md) | Architecture boundary and decision flow. |
| [CRAFT-MVP-DEFINE.md](../../CRAFT-MVP-DEFINE.md) | MVP scope and acceptance criteria. |

## Write Scope

Allowed:

- create `development/craft/LEDGER.md`,
- update `development/craft/CRAFT-MVP-WORK-PACK.md` for task status evidence,
- write this task-session evidence folder.

Not allowed:

- canonical registry, command, runtime, sigil, or spell mutation,
- scoring or role delegation automation,
- generated index creation,
- blocker waiver proof beyond the initial fixture unless needed to keep the task valid.

## Gate Checks

| Gate | Result | Evidence |
| --- | --- | --- |
| Exactly one task selected | pass | `CRAFT-MVP-001` is the first ready task. |
| Required schema exists | pass | `CRAFT-LEDGER-SCHEMA.yml` parsed successfully in prior refresh validation. |
| Required examples exist | pass | `CRAFT-LEDGER-TYPE-EXAMPLES.md` contains seed rows. |
| Write scope clear | pass | Only `LEDGER.md`, task-session evidence, and work-pack status sync are in scope. |
| Runtime delegation required | n/a | Local task-session execution is sufficient. |
| Blocker ambiguity | pass | No acceptance-affecting schema ambiguity before mutation. |

## Execution Obligations

1. Use the row-family order from the YAML schema: contexts, artifacts, relations, typed items, decisions.
2. Update statuses from the examples to reflect that type examples, schema rationale, YAML schema, define/design, visual design, and MVP work-pack now exist.
3. Represent work-packs as artifacts, not as the ledger root.
4. Include cross-context blocker and enabler rows.
5. Keep runtime/refine interface artifacts visible as side-thread artifacts, not core Craft MVP blockers.

## Validation Surface

Manual review against:

- `VAL-001`: every context has a unique `context_id`,
- `VAL-002`: every non-root context references an existing `parent_id`,
- `VAL-003`: every artifact references an existing `owner_context_id`,
- `VAL-004`: every relation source and target references an existing ID,
- `VAL-005`: every typed item includes `kind`, `base_type`, `primary_lane`, `source_id`, `target_id`, `status`, and `reason`.
