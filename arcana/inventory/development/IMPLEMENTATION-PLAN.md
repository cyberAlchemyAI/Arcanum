---
module: inventory-evidence-card
version: current
status: validator-layer-ready
updatedAt: 2026-05-27
docType: implementation-plan
---

# Implementation Plan: Inventory Evidence-Card

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `../../../spells/invoke/plan.md`
- Outputs: `IMPLEMENTATION-PLAN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`
- Template/profile selection: standalone implementation-layering and work-pack companions, split output
- Work-pack: `WORK-PACK.md`
- Next route: task-session

## Objective

Move the refreshed development package into production Inventory artifacts through bounded SWUs: templates first, fixtures second, handoff and docs third, readiness fourth, and a fast agent/runtime validator fifth.

## Delivery Slices

| Slice | Goal | Dependencies | Exit Condition |
| --- | --- | --- | --- |
| S1 | Promote static template contracts. | development templates | Production template files exist and review checks pass. |
| S2 | Add pilot fixtures and retrieval examples. | S1 | Pilot JSON parses and satisfies card mix/index/retrieval rules. |
| S3 | Add handoff examples and docs updates. | S2 for handoff, S1 for docs | Packets preserve non-authority; README/SKILL explain behavior. |
| S4 | Record readiness, glossary candidates, and gaps. | S1-S3 | Acceptance criteria are checked or explicitly deferred. |
| S5 | Implement shell plus `jq` validator for agents. | S1-S4 and validator surface decision | Validator runs against pilot fixtures and reports authority/schema failures quickly. |

## Task Decomposition

| Task ID | Description | Layer | Owner | Complexity | Depends On |
| --- | --- | --- | --- | --- | --- |
| TASK-001 | Promote evidence-card schema and authoring templates. | L0 | local-fallback | medium | none |
| TASK-002 | Promote lint and index/retrieval contracts. | L0-L1 | local-fallback | medium | TASK-001 |
| TASK-003 | Create bounded CyberAlchemy pilot fixtures. | L1 | subagent | medium | TASK-002 |
| TASK-004 | Create downstream handoff examples. | L2 | subagent | medium | TASK-003 |
| TASK-005 | Update Inventory README and SKILL contracts. | L2 | local-fallback | medium | TASK-002 |
| TASK-006 | Verify readiness and record glossary candidates. | L3 | local-fallback | low | TASK-001..TASK-005 |
| TASK-007 | Implement shell plus `jq` agent/runtime validator. | L4 | local-fallback | medium | TASK-001..TASK-006 |

## Work-Pack Mapping

| Implementation Plan Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Delivery Slices | `WORK-PACK.md` task board | Each slice maps to one or more task rows. |
| Layer Decisions | task and wave layer fields | Every task maps to L0-L3. |
| Task Decomposition | split task contracts | Each task file owns SWUs. |
| Validation Strategy | gate checks and task validation | Preserve command/review checks. |

## Validation Strategy

| Validation Type | Target | Method |
| --- | --- | --- |
| Template coverage | `arcana/inventory/templates/` | `rg` for schema fields and controlled vocabularies. |
| JSON fixture parse | `development/pilot/evidence-card/*.json` | `jq empty`. |
| Authority boundary | README/SKILL/templates/fixtures | `rg` and manual review for non-authority language. |
| Work-pack structure | `development/work-pack/` | task/wave count and SWU references. |
| POC decision gates | `POC-VALIDATION.md`, pilot cards, retrieval, handoff packets | Check source slice, card size, selector quality, validation strictness, retrieval value, and handoff safety gates. |
| Agent/runtime validator | `arcana/inventory/scripts/validate-evidence-card-fixtures.sh` plus pilot fixtures | Shell plus `jq` checks for required fields, enums, selectors, profile rules, owner/status pairs, relation notices, and handoff packet safety. |

## POC Decision Gates

The POC should decide the current open questions with observed data, not preference:

| Gate | Continue If | Refine If |
| --- | --- | --- |
| Source slice | 3-5 bounded sections yield at least 10 distinct cards. | Useful evidence requires whole-repo context. |
| Card size | Median card stays under 120 words and carries one main reusable object. | Cards become mini-documents or pointer-only stubs. |
| Selector quality | Reviewer can inspect each material claim in under 30 seconds. | Selectors are vague, unstable, or require search. |
| Validation strictness | Invalid examples fail for named reasons. | Useful real cards fail for harmless reasons. |
| Retrieval value | One task query returns fewer, better cards and explains exclusions. | Retrieval is noisy or indistinguishable from broad search. |
| Handoff safety | Candidate packet is clearly not promoted. | Authority fields confuse ownership. |

## Blockers And Risks

| ID | Type | Description | Resolution Path |
| --- | --- | --- | --- |
| R-001 | risk | Runtime validator scope may expand before contracts are proven. | Keep validator deferred until readiness review. |
| R-002 | risk | Handoff examples may be mistaken for downstream promotion. | Require non-authority notices. |
| R-003 | risk | Human UI work slows the agent/runtime validator path. | Keep human UI explicitly deferred until shell plus `jq` proves useful. |
| R-004 | risk | Parallel task-session runs mutate shared files accidentally. | Batch only SWUs with satisfied dependencies and disjoint write scopes; sync shared evidence afterward. |

## Handoff

Use `WORK-PACK.md` for current execution state and task-session handoff.
