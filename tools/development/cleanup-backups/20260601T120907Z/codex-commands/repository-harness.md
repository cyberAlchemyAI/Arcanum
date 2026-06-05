# Arcanum Spell: repository harness

<!-- arcanum:capability-id repository-harness -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command repository-harness -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-repository-harness-<UTC timestamp>`.
- `capability.id`: `repository-harness`
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

Run the installed Arcanum spell `repository-harness` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `repository-harness`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/repository-harness/README.md

````markdown
# Repository Harness

## Identity

- Canonical ID: `repository-harness`
- Aliases: `Repository Codex`
- Scope: library

Repository Harness composes `inventory`, `architecture-pattern-inventory`, and `context-builder` so a repository gains a reusable knowledge substrate, architecture package, and focused task-context retrieval path.

When a repository contains vault-like knowledge governance, Repository Harness can also run an optional ontology branch through `ontology-vault`. This keeps repository harnessing and deeper ontology-vault work available without making ontology governance mandatory for every run.

When that vault-like material spans both domain intent and implementation evidence, the ontology branch can become branch-aware: business ontology for intent, system ontology for realization, and bridge outputs for traceability and drift.

## Trigger Conditions

- A repository lacks a stable knowledge harness for future agents.
- Architecture mapping and task-context retrieval should share reusable evidence.
- The user wants repository setup before implementation work.

## Required Sigils

| Sigil                            | Role In Spell                                                                 | Required Mode                             |
| -------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------- |
| `inventory`                      | Install or validate the compiled knowledge layer.                             | `install`, `ingest`, `validate`, `lookup` |
| `architecture-pattern-inventory` | Map architecture and produce architecture package artifacts.                  | create or update                          |
| `context-builder`                | Prove task-context retrieval can consume inventory and architecture evidence. | dry-run or standard                       |

## Optional Sigils

| Sigil            | Use When                                                                                                                    | Notes                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `ontology-vault` | The repository has vault, ontology, discovery, premise, constitution, session, confidence, or delegated-research materials. | Map and distill ontology knowledge after inventory ingest. |
| `decision-gate`  | Ontology promotion or convention changes require user decisions.                                                            | Use only for blocker trade-offs.                           |

## Prerequisites

- Repository root is known.
- User agrees where local harness files should live.
- Existing docs, architecture notes, or source entrypoints are available for first ingest or mapping.

## Shared State

| State                 | Owner      | Updated By                       | Consumed By                                         |
| --------------------- | ---------- | -------------------------------- | --------------------------------------------------- |
| `.arcanum/inventory/` | repository | `inventory`                      | `context-builder`, `architecture-pattern-inventory` |
| architecture package  | repository | `architecture-pattern-inventory` | `context-builder`, `inventory`                      |
| ontology outputs      | repository | `ontology-vault`                 | `inventory`, `context-builder`                      |
| spell run report      | spell      | all phases                       | user, observability                                 |

## Execution Phases

| Phase | Sigil                            | Input                                          | Output                                                                                                     | Gate                                                                           | Failure Policy                            |
| ----- | -------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------- |
| 1     | `inventory`                      | repository root                                | inventory package                                                                                          | package exists or install plan approved                                        | block if no storage decision              |
| 2     | `inventory`                      | README, docs, architecture notes               | source summaries and entries                                                                               | raw sources remain unmodified                                                  | flag uncovered sources                    |
| 3     | `architecture-pattern-inventory` | repository root and inventory lookup           | architecture package                                                                                       | observed architecture separated from recommendations                           | block on missing repository evidence      |
| 4     | `inventory`                      | architecture package                           | architecture entries                                                                                       | index and log updated                                                          | flag if backfill incomplete               |
| 5     | `ontology-vault`                 | vault-like source folders and inventory lookup | ontology map, optional branch maps, session distillation, premise review, bridge map, or validation report | local labels mapped to generic concepts; branch-aware path justified when used | skip when no vault-like materials exist   |
| 6     | `inventory`                      | ontology outputs                               | ontology entries                                                                                           | index and log updated                                                          | flag if backfill incomplete               |
| 7     | `context-builder`                | sample task or user-selected task              | context pack or dry-run summary                                                                            | selected context maps to obligations                                           | flag if no suitable task exists           |
| 8     | spell report                     | phase outputs                                  | run report                                                                                                 | all blockers named                                                             | report partial if optional phases skipped |

## Observability

Record spell-level telemetry for install decisions, sources ingested, architecture artifacts produced, optional ontology outputs, context lookup quality, gates, and follow-ups when `.arcanum/observability/` exists.

## Output Contract

Return a spell run report with inventory path, architecture package path, optional ontology output path, context-builder result, gates, validation, and recommended next repository harness action.

````
