---
module: inventory-interface-link-index
status: block
docType: decision-record
decisionGate: interface-indexing-open-gate
updatedAt: 2026-06-08
owner: inventory
---

# Decision Gate: Inventory Interface And Indexing Open Gate

## Target Scope

Inventory interface, linking, indexing, and first interface-driven pilot slice.

## Consequential Work Blocked

Pilot slice mutation is blocked until the pilot target is explicitly confirmed.

Starting `SWU-INT-001` is not blocked. The active work-pack already marks the
skill contract update as ready, and it does not require choosing a pilot target.

## Context Evidence

| Evidence | Signal |
| --- | --- |
| `../READINESS.md` | Design readiness passes, implementation is ready for the first bounded task-session, and auto behavior/templates/validator/pilot are not started. |
| `../WORK-PACK.md` | `TASK-INT-001` is ready; template, validator, and pilot tasks are sequenced behind it. |
| `../EXECUTION-PACK.md` | `W-INT-0` is ready; later waves are blocked by the task sequence. |
| `../INTERFACE-ARCHITECTURE.md` | Inventory should infer target, ask confirmation, then write a bounded slice. |
| `../INDEX-TECHNIQUE-RESEARCH.md` | Index templates are designed but not implemented as production templates. |
| `../LINKING-DISCIPLINE.md` | Link/index validation rules are known and need validator implementation. |
| `../VALIDATOR-SURFACE-DECISION.md` | Agent/runtime validator surface selected as shell plus `jq`; human UI deferred. |
| `EVIDENCESET-DECISION.md`, `POC-GATES-DECISION.md` | Evidence-card model can continue; canonical EvidenceSet promotion remains deferred until minimal schema design. |

## Open Decisions And Gaps

| ID | Type | Classification | State | Blocks | Next action |
| --- | --- | --- | --- | --- | --- |
| D-INT-001 | pilot target | blocker | unresolved | `TASK-INT-005` pilot slice mutation | User confirms first pilot target after interface/index templates exist. |
| D-INT-002 | EvidenceSet production promotion | deferrable | deferred | canonical EvidenceSet behavior only | Run minimal candidate schema design before production promotion. |
| D-INT-003 | human UI/browser interface | deferrable | deferred | full human UI only | Revisit after chat-first interface and shell plus `jq` validation become hard to inspect. |
| D-INT-004 | SQLite/vector/semantic search | deferrable | deferred | advanced retrieval only | Revisit after deterministic JSON indexes prove the shape. |
| G-INT-001 | default `$inventory` contract | sequencing gap | not-started | downstream templates and pilot | Execute `SWU-INT-001`. |
| G-INT-002 | target proposal and chat-view templates | sequencing gap | not-started | pilot proof | Execute `SWU-INT-002` after `SWU-INT-001`. |
| G-INT-003 | index/link templates | sequencing gap | not-started | validator and pilot proof | Execute `SWU-INT-003` after `SWU-INT-001`. |
| G-INT-004 | link/index validator | sequencing gap | not-started | pilot proof | Execute `SWU-INT-004` after templates. |
| G-INT-005 | first interface-driven pilot slice | blocked gap | not-started | feature proof | Execute `SWU-INT-005` after contract, templates, validator, and pilot target confirmation. |
| G-INT-006 | readiness/docs synchronization | sequencing gap | not-started | promotion/readiness claim | Execute `SWU-INT-006` after pilot passes. |

## Blocker Decision

### D-INT-001: Which first interface-driven pilot target should Inventory use?

| Option | Benefit | Cost or Risk | Choose when | Downstream impact |
| --- | --- | --- | --- | --- |
| A. Arcanum vs Sigils Library Authority | Exercises authority conflict, source owners, exclusions, non-authority links, and decision handoff. | Higher conceptual tension; must not resolve authority itself. | The goal is to prove Inventory handles governance-sensitive knowledge safely. | Strong first proof for confirmation UX, link discipline, and gap/risk queue. |
| B. Inventory self-slice | Exercises the Inventory package itself and keeps sources local to the active work. | May be too self-referential and less representative of user lookup needs. | The goal is fastest local validation with minimal source hunting. | Good validator proof, weaker cross-owner authority proof. |
| C. Craft recursive ledger stressor | Exercises grouped evidence and candidate EvidenceSet pressure. | Risks mixing the active interface MVP with deferred EvidenceSet promotion work. | The goal is to stress grouped evidence after core interface/index behavior exists. | Better as second pilot or EvidenceSet schema task, not first interface proof. |
| D. User-selected current-session topic | Most faithful to live user intent. | Can be too ephemeral unless session evidence is captured durably. | The user wants Inventory to prove the exact current conversation flow. | Requires a session-derived source record and stricter confirmation wording. |

## Recommended Option

Option A: Arcanum vs Sigils Library Authority.

Rationale: the active architecture already uses this as the example target, and
it exercises the most important Inventory boundary: record evidence and route
authority questions without deciding them.

## Selected Option

Unresolved.

## Result

`BLOCK` for `TASK-INT-005` pilot slice mutation.

`PASS` for `SWU-INT-001`, `SWU-INT-002`, `SWU-INT-003`, and `SWU-INT-004`
execution in documented order, provided no new blocker appears.

## Remaining Blockers

1. First interface-driven pilot target selection before pilot slice mutation.

## Deferred Decisions

- Canonical EvidenceSet promotion.
- Human UI/browser interface.
- SQLite, vector, semantic search, and automatic graph inference.

## Assumptions

- JSON remains the canonical machine index format.
- Markdown remains the human-readable projection format.
- Inventory links remain read models, not Ontology Vault relations or
  Definitions Governance acceptance.
- Archived whole-Arcanum and whole-repository research packs remain evidence,
  not active development tracks.

## Next Step

Ask the user to select the first pilot target when `TASK-INT-005` is reached.
