---
module: inventory-whole-arcanum
version: 0.1.0
status: complete
updatedAt: 2026-06-01
docType: work-pack
---

# WORK-PACK: Whole Arcanum Inventory

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | complete |
| complexity | high |
| outputMode | split |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| activeLayerWindow | complete |
| nextExecutableSWU | none |
| nextRoute | real-task POC |

## Objective

Create a staged, validated, agent-fast inventory for Arcanum source knowledge so
future agents can query reusable context through shell plus `jq` surfaces before
opening large source files.

## Success Conditions

1. Source inclusion and exclusion are explicit before card creation.
2. Evidence cards cover high-value implementation knowledge, not every line.
3. Candidate EvidenceSets support real implementation questions with selected
   and excluded evidence.
4. Validation catches malformed cards, unresolved references, and governance
   boundary mistakes.
5. The inventory remains queryable by agents without a human UI.

## Delivery Slices

| Slice | Outcome | Layer | Validation |
| --- | --- | --- | --- |
| S-WAI-001 | Source manifest and exclusion policy. | L0 | manifest review, Artifact Constitution validator |
| S-WAI-002 | Inventory self-slice cards and query examples. | L1 | completed |
| S-WAI-003 | Governance/lifecycle pilot cards and candidate sets. | L1 | completed |
| S-WAI-004 | Expanded capability-family cards and indexes. | L2 | completed |
| S-WAI-005 | Operational refresh and readiness checks. | L3 | completed |

## Task Board

| Task | Goal | Layer | Status |
| --- | --- | --- | --- |
| [TASK-WAI-001](work-pack/tasks/TASK-WAI-001-source-manifest.md) | Create source manifest and exclusion policy. | L0 | completed |
| [TASK-WAI-002](work-pack/tasks/TASK-WAI-002-inventory-self-slice.md) | Inventory the Inventory package as the first proof slice. | L1 | completed |
| [TASK-WAI-003](work-pack/tasks/TASK-WAI-003-governance-lifecycle-slices.md) | Build governance and lifecycle pilot slices. | L1 | completed |
| [TASK-WAI-004](work-pack/tasks/TASK-WAI-004-expanded-capability-waves.md) | Expand to remaining capability families. | L2 | completed |
| [TASK-WAI-005](work-pack/tasks/TASK-WAI-005-operational-readiness.md) | Harden refresh, validation, and readiness reporting. | L3 | completed |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write Scope | Validation |
| --- | --- | --- | --- | --- | --- |
| SWU-WAI-001 | TASK-WAI-001 | Draft source manifest and source-family classification. | none | `arcana/inventory/development/whole-arcanum/source-manifest.*` | `rg` and constitution validator |
| SWU-WAI-002 | TASK-WAI-001 | Add exclusion and durable-evidence promotion policy. | SWU-WAI-001 | `arcana/inventory/development/whole-arcanum/SOURCE-POLICY.md` | generated/local path review |
| SWU-WAI-003 | TASK-WAI-002 | Create slice-aware validation contract and Inventory self-slice cards. | TASK-WAI-001 | `arcana/inventory/development/whole-arcanum/cards/inventory/`, validator wrapper/contract path | completed |
| SWU-WAI-004 | TASK-WAI-002 | Create self-slice EvidenceSet and query example. | SWU-WAI-003 | `arcana/inventory/development/whole-arcanum/evidence-sets/` | completed |
| SWU-WAI-005 | TASK-WAI-003 | Create constitution/schema governance cards. | TASK-WAI-001 | `cards/governance/` | completed |
| SWU-WAI-006 | TASK-WAI-003 | Create invoke/refine/task-session lifecycle cards. | TASK-WAI-001 | `cards/lifecycle/` | completed |
| SWU-WAI-007 | TASK-WAI-003 | Create cross-pilot EvidenceSet for "can we implement next SWU?" queries. | SWU-WAI-005, SWU-WAI-006 | `evidence-sets/` | completed |
| SWU-WAI-008 | TASK-WAI-004 | Expand `arcana/` capability families by wave. | W1 | `cards/arcana/` | completed |
| SWU-WAI-009 | TASK-WAI-004 | Expand `spells/`, `transmutations/`, and `formulae/`. | W1 | `cards/composition/` | completed |
| SWU-WAI-010 | TASK-WAI-004 | Expand `framework/`, `registry/`, `tools/`, and native runtime surfaces. | W1 | `cards/runtime/` | completed |
| SWU-WAI-011 | TASK-WAI-005 | Add refresh and lint command contract for whole inventory. | W2 | validator/docs paths under whole-arcanum pack | completed |
| SWU-WAI-012 | TASK-WAI-005 | Write readiness report and next promotion gate. | SWU-WAI-011 | `READINESS.md` and task-session result | completed |

## Blockers And Gates

| Gate | Status | Decision Needed |
| --- | --- | --- |
| Source boundary before ingestion | pass | `source-manifest.json` and `SOURCE-POLICY.md` exist and passed validation. |
| Durable evidence inclusion | pass | `SOURCE-POLICY.md` requires adjacent promotion evidence before inclusion. |
| EvidenceSet promotion | deferred | Candidate-only until repeated task-session reuse proves value. |
| Human UI | deferred | Keep agent-fast shell plus `jq` surface. |
| Generated/runtime paths | strict | Excluded by default under Artifact Constitution. |
| W1 validation shape | pass | Option B selected: slice-aware validator contract. |
| Implementation completion gate | pass | No blocker-level decisions remain before continuing W1; assumptions recorded in `decisions/IMPLEMENTATION-COMPLETION-GATE.md`. |

## Next Step

Run the real-task POC:

```text
Use arcana/inventory/development/whole-arcanum/READINESS.md and OPERATIONAL-COMMANDS.md before a real Arcanum implementation task.
```

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-01 | Completed SWU-WAI-012 and TASK-WAI-005; readiness report records validation results, promotion gate, deferred decisions, and real-task POC route. | Codex |
| 2026-06-03 | Refreshed SWU-WAI-010 runtime scope to exclude legacy `.codex/commands` as live proof and use native/generated skill packages plus canonical source contracts for cross-repository testing. | Codex |
| 2026-06-01 | Completed SWU-WAI-011; whole-inventory validation script and operational command contract pass command review. | Codex |
| 2026-06-01 | Completed SWU-WAI-010; runtime support cards, index, retrieval fixture, and coverage report pass slice validation, opening L3 operational readiness. | Codex |
| 2026-06-01 | Completed SWU-WAI-009; composition family cards, index, retrieval fixture, and coverage report pass slice validation. | Codex |
| 2026-06-01 | Completed SWU-WAI-008; arcana capability-family cards, index, retrieval fixture, and coverage report pass slice validation. | Codex |
| 2026-06-01 | Completed TASK-WAI-003; governance and lifecycle card slices plus cross-pilot candidate EvidenceSet pass, opening L2 expansion. | Codex |
| 2026-05-29 | Completed TASK-WAI-002; slice-aware validator, Inventory self-slice cards, retrieval fixture, and candidate EvidenceSet pass. | Codex |
| 2026-05-31 | Refine plus decision-gate pass found no blocker-level decisions before continuing W1; recorded assumptions for governance/lifecycle card minimums. | Codex |
| 2026-05-29 | Refreshed W1 validation gate with selected option B: slice-aware validator contract. | Codex |
| 2026-05-29 | Completed TASK-WAI-001; W0 source manifest and source policy are in place, opening L1 proof-slice work. | Codex |
