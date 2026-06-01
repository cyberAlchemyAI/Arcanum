# Craft Recursive Ledger Design

## Purpose

Define the minimal schema rationale for Craft's recursive ledger MVP.

This artifact satisfies `CRAFT-REFINE-002` from [WORK-PACK.md](WORK-PACK.md). It is shaped by [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md), and keeps the MVP file-backed, YAML-defined, and reviewable.

## Design Decision

Use a YAML schema contract with a Markdown-first ledger fixture and stable IDs.

The schema contract is [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml). Optional structured indexes can be generated later, but the first ledger fixture should remain readable and editable without a runtime command.

## Ledger File Shape

Recommended initial files:

| File | Purpose | Required For MVP |
| --- | --- | --- |
| `CRAFT-LEDGER-SCHEMA.yml` | Structured schema contract for row families, fields, enums, validation rules, and blocker lifecycle. | yes |
| `LEDGER.md` | Human-readable recursive context ledger. | yes |
| `ledger-index.json` | Optional machine-readable index generated from or aligned with the ledger. | no |
| `examples.md` | Optional examples or fixtures for schema validation. | no |

In the current development package, [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md) acts as the example fixture.

## Core Row Families

The MVP ledger has five row families:

1. contexts,
2. artifacts,
3. relations,
4. typed items,
5. decisions.

Typed items cover blockers, gates, and enablers in one schema because they share the same routing, evidence, lane, and refinement fields.

## Context Rows

Context rows define recursive project-like units.

Required fields:

| Field | Required | Description |
| --- | --- | --- |
| `context_id` | yes | Stable local ID, e.g. `CTX-LEDGER`. |
| `parent_id` | yes | Parent context ID or `root`. |
| `title` | yes | Human-readable context name. |
| `purpose` | yes | Why this context exists. |
| `stage` | yes | Current lifecycle stage. |
| `gate` | yes | Current context gate: `pass`, `flag`, or `block`. |
| `next_move` | yes | Next responsible move. |
| `owned_artifacts` | no | Artifact IDs or paths owned by this context. |
| `notes` | no | Short residue, decision, or context note. |

Allowed `stage` values for MVP:

```text
idea, define, design, plan, execute, validate, reflect, blocked, closed
```

Example mapping:

- `CTX-CRAFT`, `CTX-LEDGER`, `CTX-TYPES`, `CTX-SCHEMA`, and `CTX-SCORING` from [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md) all fit this schema.

## Artifact Rows

Artifact rows define files, records, work-packs, validations, and handoffs owned by contexts.

Required fields:

| Field | Required | Description |
| --- | --- | --- |
| `artifact_id` | yes | Stable local ID, e.g. `ART-WORK-PACK`. |
| `owner_context_id` | yes | Primary owning context. |
| `path` | yes | File path or artifact reference. |
| `artifact_type` | yes | Type label such as `work-pack`, `schema-design`, `examples`, `validation`. |
| `status` | yes | `planned`, `active`, `stale`, `superseded`, `closed`. |
| `notes` | no | Ownership or usage note. |

Boundary rule:

A work-pack can be an artifact owned by a context, but it is not the whole recursive ledger.

Example mapping:

- `ART-WORK-PACK` is owned by `CTX-LEDGER`.
- `ART-EXAMPLES` is owned by `CTX-TYPES`.
- `ART-SCHEMA` is owned by `CTX-SCHEMA`.

## Relation Rows

Relation rows connect contexts, artifacts, decisions, or typed items.

Required fields:

| Field | Required | Description |
| --- | --- | --- |
| `relation_id` | yes | Stable local ID. |
| `source_id` | yes | Source context, artifact, decision, or item ID. |
| `target_id` | yes | Target context, artifact, decision, or item ID. |
| `type` | yes | Relationship kind. |
| `status` | yes | `active`, `proposed`, `resolved`, `rejected`, `superseded`. |
| `reason` | yes | Why the relation exists. |
| `evidence` | no | Source file, row, decision, or validation evidence. |

Allowed `type` values for MVP:

```text
contains, blocks, enables, depends_on, informs, supersedes
```

Example mapping:

- `REL-CONTAINS-001` maps parent-child context nesting.
- `REL-BLOCKS-001` maps a cross-context blocker.
- `REL-ENABLES-001` maps examples enabling schema design.

## Typed Item Rows

Typed item rows represent blockers, gates, and enablers.

Required fields:

| Field | Required | Description |
| --- | --- | --- |
| `item_id` | yes | Stable local ID. |
| `kind` | yes | `blocker`, `gate`, or `enabler`. |
| `base_type` | yes | Base condition type from [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md). |
| `context_type` | no | Context-specific subtype or `none`. |
| `primary_lane` | yes | Main operational lane. |
| `secondary_lanes` | no | Supporting or review lanes. |
| `source_id` | yes | Source context, artifact, decision, or condition. |
| `target_id` | yes | Target context, artifact, decision, or condition. |
| `status` | yes | Current item status. |
| `refinement_status` | yes for blockers; optional for gates/enablers | Blocker refinement lifecycle state. |
| `default_role` | no | Candidate future role inferred from type plus lane. |
| `delegation_route` | no | Suggested future route. |
| `closure_condition` | yes for blockers/gates; optional for enablers | Evidence or condition required for closure. |
| `evidence` | no | Source anchor or validation evidence. |
| `reason` | yes | Why this item exists. |

Allowed `kind` values:

```text
blocker, gate, enabler
```

Allowed `status` values:

```text
active, proposed, pass, flag, block, resolution_proposed, resolved, rejected, waived
```

Allowed `refinement_status` values:

```text
raw, typed, refined, resolution_proposed, resolved, waived
```

## Decision Rows

Decision rows record explicit human or governance choices, especially waivers.

Required fields:

| Field | Required | Description |
| --- | --- | --- |
| `decision_id` | yes | Stable local ID. |
| `scope_id` | yes | Context, artifact, item, or relation affected. |
| `decision_type` | yes | `selection`, `waiver`, `deferral`, `approval`, `rejection`. |
| `selected` | yes | Chosen option. |
| `rationale` | yes | Why the choice was made. |
| `evidence` | no | Source, reviewer, or artifact reference. |
| `status` | yes | `active`, `superseded`, `closed`. |

Waiver rule:

Any blocker with `refinement_status = waived` must link to a decision row with `decision_type = waiver`.

## Blocker Refinement Lifecycle

Blockers cannot be marked resolved directly from raw or typed states.

Allowed lifecycle:

```text
raw -> typed -> refined -> resolution_proposed -> resolved
```

Waiver lifecycle:

```text
raw|typed -> waived
```

Waiver requires a decision row.

Validation rule:

```text
if kind == blocker and status == resolved:
  refinement_status must be refined, resolution_proposed, resolved, or waived
  closure_condition must be present
  evidence must be present or waiver decision must be linked
```

## Conflict Policy

Multiple lanes or types are allowed, but they must not be silently collapsed.

Rules:

1. `primary_lane` owns the next move.
2. `secondary_lanes` are required reviewers or contributors.
3. If `primary_lane` is `blocker_refiner`, the item is not ready for final resolution.
4. If `auditor` or `validator` is listed as a secondary lane, closure needs review evidence.
5. If `business` and `tech` disagree on a blocker meaning, status remains `flag` or `block` until a decision row records the selected interpretation.
6. Multiple base types should be avoided in MVP rows. Use one `base_type` plus `secondary_lanes` and explain mixed causes in `reason`.

## Validation Rules

1. Every context has a unique `context_id`.
2. Every non-root context references an existing `parent_id`.
3. Every artifact references an existing `owner_context_id`.
4. Every relation source and target references an existing ID.
5. Every typed item has `kind`, `base_type`, `primary_lane`, `source_id`, `target_id`, `status`, and `reason`.
6. Every blocker has `refinement_status` and `closure_condition`.
7. Every blocker marked `resolved` has refinement evidence or a waiver decision.
8. Every gate has a closure condition.
9. Every enabler has enough evidence or reason to explain what it enables.
10. Work-pack artifacts remain artifacts, not the ledger root.

## Future Scoring Placeholders

Scoring remains deferred, but the schema preserves future inputs:

| Future Signal | Existing Field Source |
| --- | --- |
| blocker count | typed item rows where `kind = blocker` |
| blocker severity | future optional field; not in MVP |
| enabler count | typed item rows where `kind = enabler` |
| downstream impact | relation rows targeting downstream contexts |
| lane load | `primary_lane` and `secondary_lanes` |
| validation confidence | gate rows and evidence fields |
| age / staleness | future optional timestamp fields; not in MVP |
| priority | future optional decision or scoring field; not in MVP |

## Example Trace

| Example Row | Schema Family | Required Fields Covered |
| --- | --- | --- |
| `CTX-LEDGER` | context | `context_id`, `parent_id`, `title`, `purpose`, `stage`, `gate`, `next_move` |
| `ART-WORK-PACK` | artifact | `artifact_id`, `owner_context_id`, `path`, `artifact_type`, `status` |
| `REL-BLOCKS-001` | relation | `relation_id`, `source_id`, `target_id`, `type`, `status`, `reason`, `evidence` |
| `BLK-RAW-001` | typed item | blocker type, lanes, source/target, refinement state, closure condition |
| `GATE-BLOCKER-001` | typed item | gate type, blocker refinement gate, block status |
| `ENA-TECH-001` | typed item | enabler type, tech lane, schema-design route |

## Open Questions

| Question | Why It Matters | Suggested Next Action |
| --- | --- | --- |
| Should `blocker_refiner` be a lane, role, or lifecycle state? | Examples show it behaves like a lifecycle responsibility rather than a domain lane. | Keep as lane for MVP; revisit after more examples. |
| Should `owning lane` become a real lane? | Artifact blockers/enablers need an owner when artifacts are shared. | Add `owner_lane` later only if examples require it. |
| Should structured JSON be generated or authored directly? | Direct JSON may increase rigidity too early. | Keep YAML schema plus Markdown fixture; defer JSON generation. |
| Should timestamps be MVP fields? | Scoring and staleness eventually need them. | Defer until scoring is active. |

## Result

- Status: pass
- Reason: The schema represents every row family in the example artifact, distinguishes condition type, lane, and role hint, includes blocker refinement fields, keeps work-pack as an owned artifact, and does not require runtime command integration.
