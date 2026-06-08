---
name: ontology-harness
description: "Ontology Harness composes `inventory`, `ontology-vault`, and `context-builder` so a repository can turn vault-like knowledge material into a reusable ontology governance layer."
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: spells/ontology-harness/README.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
---

# Ontology Harness

## Identity

- Canonical ID: `ontology-harness`
- Primary alias: `Ontology Harness`
- Aliases: `Necronomicon Vault`, `Ontology Codex`
- Scope: library

## Purpose

Ontology Harness composes `inventory`, `ontology-vault`, and `context-builder` so a repository can turn vault-like knowledge material into a reusable ontology governance layer.

It is designed for repositories with sessions, discoveries, premises, conventions, confidence rules, or delegated research artifacts that need traceable distillation and promotion gates.

When a repository has both business/domain material and system/runtime material, Ontology Harness can run a branch-aware path that maps business ontology, maps system ontology, and validates the bridge between intent and implementation.

For long-running repository work, use `necronomicon` as the durable operational harness. The session spell keeps memory, selected capability routing, fallback discovery, and capability updates while delegating ontology mapping and bridge validation back to this spell.

## Trigger Conditions

- A repository has a `vault/`, `ontology/`, `discovery/`, `premise/`, `axiom/`, `constitution/`, `sessions/`, or equivalent knowledge-governance area.
- Session records need distillation into durable claims, decisions, contradictions, and open questions.
- Premises or working bets need confidence review.
- Ontology roles, statuses, edge rules, tags, or schema conventions need mapping or update planning.
- Delegated research and synthesis findings need traceability checks.
- Business intent needs explicit links to implementation, tests, telemetry, constraints, or drift findings.

## Required Sigils

| Sigil             | Role In Spell                                                                                | Required Mode                                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `inventory`       | Install or reuse the compiled knowledge layer and ingest vault sources.                      | `install`, `ingest`, `lookup`, `validate`                                                          |
| `ontology-vault`  | Map, distill, review, promote, propose convention changes, and validate ontology governance. | `map`, `distill-sessions`, `premise-review`, `promote-confidence`, `convention-update`, `validate` |
| `context-builder` | Prove future tasks can retrieve ontology evidence compactly.                                 | dry-run or standard                                                                                |

## Optional Sigils

| Sigil                            | Use When                                                                              | Notes                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `decision-gate`                  | Promotion or convention changes require human trade-off decisions.                    | Use before mutating rules.                                         |
| `feature-glossary`               | Local ontology terms need concise plain-language explanation.                         | Keep glossary explanatory, not authoritative.                      |
| `architecture-pattern-inventory` | System ontology or bridge validation depends on architecture or repository structure. | Recommended for branch-aware mapping with implementation evidence. |

## Prerequisites

- Repository root is known.
- User agrees where local ontology outputs should live.
- Existing vault-like source folders or session records are available, or the user wants an initial ontology map.

## Shared State

| State                       | Owner      | Updated By                                         | Consumed By                          |
| --------------------------- | ---------- | -------------------------------------------------- | ------------------------------------ |
| `.arcanum/inventory/`       | repository | `inventory`                                        | `ontology-vault`, `context-builder`  |
| ontology map                | spell      | `ontology-vault`                                   | `inventory`, `context-builder`, user |
| session distillation report | spell      | `ontology-vault`                                   | `inventory`, `decision-gate`, user   |
| premise review ledger       | spell      | `ontology-vault`                                   | `decision-gate`, user                |
| confidence promotion report | spell      | `ontology-vault`                                   | user, observability                  |
| convention change plan      | spell      | `ontology-vault`                                   | `decision-gate`, user                |
| business ontology map       | spell      | `ontology-vault`                                   | `inventory`, `context-builder`, user |
| system ontology map         | spell      | `ontology-vault`, `architecture-pattern-inventory` | `inventory`, `context-builder`, user |
| business-system bridge map  | spell      | `ontology-vault`                                   | `inventory`, `context-builder`, user |
| spell run report            | spell      | all phases                                         | user, observability                  |

## Execution Phases

| Phase | Sigil                            | Input                                                                | Output                                                     | Gate                                              | Failure Policy                               |
| ----- | -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- | -------------------------------------------- |
| 1     | `inventory`                      | repository root and source folders                                   | inventory package                                          | package exists or install plan approved           | block if no storage decision                 |
| 2     | `inventory`                      | vault, ontology, discovery, premise, convention, and session sources | source summaries and entries                               | raw sources remain unmodified                     | flag uncovered sources                       |
| 3     | `ontology-vault`                 | inventory lookup and source folders                                  | ontology map                                               | local labels mapped to generic concepts           | flag unmapped labels                         |
| 4     | `ontology-vault`                 | business and system sources                                          | branch classification and optional branch maps             | branch-aware path is justified or skipped         | skip when single ontology map is enough      |
| 5     | `architecture-pattern-inventory` | repository root and system sources                                   | architecture evidence for system ontology                  | observed structure separated from recommendations | skip when no system branch exists            |
| 6     | `ontology-vault`                 | business map, system map, architecture evidence                      | business-system bridge map and traceability matrix         | bridge claims cite both branches                  | flag unbridged claims, block false alignment |
| 7     | `ontology-vault`                 | sessions and delegated evidence                                      | session distillation and synthesis traceability report     | sessions remain evidence records, not authority   | block if findings lack source evidence       |
| 8     | `ontology-vault`                 | premises, confidence rules, and evidence                             | premise review and confidence promotion report             | promotions cite sufficient evidence               | block unsafe promotion                       |
| 9     | `decision-gate`                  | blocker promotions, bridge claims, or convention changes             | decision record                                            | user resolves consequential trade-offs            | skip if no blockers                          |
| 10    | `ontology-vault`                 | approved decisions                                                   | convention change plan, drift report, or validation report | migration impact named                            | report partial if changes deferred           |
| 11    | `inventory`                      | ontology outputs and bridge outputs                                  | updated inventory entries                                  | index and log updated                             | flag if backfill incomplete                  |
| 12    | `context-builder`                | sample ontology or cross-branch task                                 | context pack or dry-run summary                            | selected context maps to obligations              | flag if no suitable task exists              |
| 13    | spell report                     | phase outputs                                                        | run report                                                 | all blockers named                                | report partial if optional phases skipped    |

## Local Customization

- Spell root: `.arcanum/spells/`
- Default output root: `.arcanum/ontology/`
- Local paths: repository-specific vault, ontology, docs, notes, wiki, or session folders.
- Branch paths: optional repository-specific business, system, and bridge folders or tags.
- Gate strictness: standard by default, strict for promotion or convention mutation.
- Interaction mode: interactive for promotions, guided-auto for mapping and distillation, dry-run when requested.

## Observability

Record spell-level telemetry when `.arcanum/observability/` exists:

- spell name,
- alias used,
- source folders scanned,
- sessions distilled,
- delegated research records found,
- synthesis findings validated,
- premises reviewed,
- promotions recommended,
- convention changes proposed,
- gates passed or blocked,
- handoff artifacts created,
- branch-aware path used,
- business documents mapped,
- system documents mapped,
- bridge edges validated,
- drift findings found,
- traceability gaps found,
- validation result,
- follow-up actions.

## Output Contract

Return:

```markdown
## Spell Result

- Spell: Ontology Harness
- Canonical ID: ontology-harness
- Alias used: <alias or none>
- Repository: <path>
- Phases completed: <count>
- Sigils invoked: inventory, ontology-vault, context-builder, <optional>
- Gates: pass | block | flag
- Outputs: <paths, including branch maps or bridge artifacts when used>
- Validation: <checks>
- Follow-up: <items or none>
```
