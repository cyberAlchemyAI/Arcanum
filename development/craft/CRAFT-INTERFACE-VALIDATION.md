# Craft Interface Validation

Status: pass
Date: 2026-06-08
Task: `CRAFT-INTERFACE-001`

## Purpose

Validate the local Craft interface contract, schema extension, example ledger,
and live-test recipe against the work-pack and hard gates.

## Evidence Reviewed

- `development/craft/CRAFT-INTERFACE.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERFACE-EXAMPLE.yml`
- `development/craft/CRAFT-LIVE-TEST-RECIPE.md`
- `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`
- `docs/decisions/craft-interface-development-risk-gates.md`

## Method Coverage

| Method | Evidence | Result |
| --- | --- | --- |
| `start_project` | Contract lists inputs, writes, returns, invariants. | pass |
| `state` | Contract lists read-only return state. | pass |
| `describe` | Contract preserves versioned descriptions. | pass |
| `add_blocker` | Contract blocks raw direct resolution. | pass |
| `refine_blocker` | Contract separates refinement from closure. | pass |
| `add_enabler` | Contract records enabler row and relation. | pass |
| `next` | Contract requires one active next move. | pass |
| `open_decision` | Contract opens blocking decisions. | pass |
| `decide` | Contract requires rationale and evidence. | pass |
| `add_gap` | Contract requires severity, treatment, owner, status. | pass |
| `add_definition` | Contract keeps definitions local candidates. | pass |
| `open_child_context` | Contract requires parent and recomposition target. | pass |
| `link` | Contract creates typed relations. | pass |
| `validate` | Contract returns pass, flag, or block. | pass |
| `recompose` | Contract requires parent-fit evidence. | pass |
| `export_ledger` | Contract preserves YAML source of truth. | pass |

## Schema Review

| Requirement | Evidence | Result |
| --- | --- | --- |
| Definitions row family exists. | `definitions` row family in schema. | pass |
| Gaps row family exists. | `gaps` row family in schema. | pass |
| Descriptions preserve context description history. | `descriptions` row family in schema. | pass |
| YAML owns state. | `source_of_truth_policy.target_project_source`. | pass |
| Markdown is view only. | `source_of_truth_policy.human_view`. | pass |

## Example Review

| Requirement | Evidence | Result |
| --- | --- | --- |
| Root context starts project. | `CTX-CRAFT-TEST`. | pass |
| Child context is recursive. | `CTX-CRAFT-BLOCKER` parent is root. | pass |
| Blocker exists and is refined/resolved with evidence. | `BLK-STORAGE-SOURCE-001`. | pass |
| Enabler exists. | `ENA-RECOMPOSE-001`. | pass |
| Decision exists. | `DEC-STORAGE-SOURCE-001`. | pass |
| Gap exists. | `GAP-VALIDATOR-001`. | pass |
| Definition exists and is candidate. | `DEF-LOCAL-LEDGER-001`. | pass |
| Next move exists. | Both context rows include `next_move`. | pass |
| Recomposition exists. | `recomposition` row and `REL-RECOMPOSE-001`. | pass |

## Hard Gate Review

| Gate | Result |
| --- | --- |
| No command surfaces, runtime adapters, registries, sigils, spells, or canonical glossary state changed. | pass |
| `.craft/ledger.yml` remains source of truth. | pass |
| No receipt closes context without recomposition evidence. | pass |
| Dispatch pass is route-shape evidence only. | pass |
| Raw blocker cannot resolve directly. | pass |
| Definitions are not promoted without owner route. | pass |

## Validation Result

`pass`

The interface contract and fixtures satisfy `CRAFT-INTERFACE-001`. Runtime
helper shape, executable receipt validation, generated indexes, scoring, and
promotion remain deferred.
