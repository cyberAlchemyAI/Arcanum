# Research Knowledge Stack Contract

Purpose: standardize how definitions, references, context, and resources become executable research assets.

Scope: all new and modified experiments in this project.

## Knowledge Stack Model

| Layer          | Artifact                                                                  | Purpose                                                                                                    |
| -------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Foundations    | `foundations/DOMAIN-CONTEXT.md` + `foundations/METHODOLOGY-AND-THEORY.md` | project-level synthesis of the research setting, prior-art frame, methodology posture, and theory baseline |
| Definitions    | `definitions/DEFINITIONS-INDEX.md`                                        | stable meaning for claim, metric, and protocol terms                                                       |
| References     | `sources/REFERENCE-LEDGER.md`                                             | authoritative citations with source IDs and pin metadata                                                   |
| Inventory      | `inventory/INVENTORY-INDEX.md` + `inventory/library/<source-id>.md`       | reusable extracted knowledge layer with per-source content coverage                                        |
| Raw Provenance | `inventory/raw/<source-id>/...`                                           | raw content backing layer for extracted inventory claims                                                   |
| Context        | `experiments/<experiment-key>/context.md`                                 | experiment-scoped synthesis across definitions and references                                              |
| Resources      | `experiments/<experiment-key>/sources.md` + inventory linkage             | executable source set and reusable reference library for data capture and analysis                         |

## Contract Rules

| Rule ID | Rule                                                                                                                                                                          | Enforcement                                                                                |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| RK0     | Before protocol design, the project must maintain both foundations artifacts backed by sourced and inventoried authorities.                                                   | Startpoint and G0 block when the foundations baseline is missing or placeholder-only.      |
| RK1     | Claims and protocols must use terms declared in the definitions index.                                                                                                        | G1 blocks on undefined critical terms.                                                     |
| RK2     | Any reference used as decision authority must appear in the reference ledger with pin metadata or explicit waiver.                                                            | G2 blocks on unpinned authoritative references.                                            |
| RK3     | Every experiment must include a context bundle at `experiments/<experiment-key>/context.md`.                                                                                  | Execution blocked before S7 when context bundle is missing.                                |
| RK4     | Context bundle must map claim IDs, key definitions, primary references, and open conflicts.                                                                                   | G1 or S6 returns NEEDS-REVISION on missing mappings.                                       |
| RK5     | Primary references must be source-cataloged and inventory-linked before execution.                                                                                            | G3 blocks when primary references lack inventory coverage.                                 |
| RK6     | Conflicts between references must be logged explicitly in context bundle.                                                                                                     | Analysis stage flags conclusion validity risk if conflicts are hidden.                     |
| RK7     | Inventory for primary authorities must be library-grade: enough extracted content to support later protocol design without re-discovery.                                      | S0 or S6 returns NEEDS-REVISION when inventory is snippet-only.                            |
| RK8     | Library-grade inventory must expose a provenance chain from reference ledger to per-source library file and, when possible, to raw content artifacts.                         | S0 or S6 returns NEEDS-REVISION when inventory claims cannot be traced to source material. |
| RK9     | When source content cannot be lawfully or technically retrieved from the web, the workflow must request user-provided raw files and inventory against those files explicitly. | Source readiness remains partial until raw input is provided or an explicit waiver exists. |

## Required Fields By Artifact

### Domain context baseline

- research setting
- unit of analysis
- regimes or comparators in scope
- prior-art context map
- failure modes and non-goals

### Methodology and theory baseline

- methodology posture
- authority map
- theory synthesis
- experiment design implications
- reference library obligations

### Definitions index

- definition_id
- term
- scope
- canonical meaning
- linked claims

### Reference ledger

- reference_id
- citation
- source_id (if cataloged)
- pin metadata (DOI/ISBN/commit/hash/archive)
- authority level (primary/supporting/fallback)
- usage scope (paper/protocol/analysis)

### Inventory index

- source_id
- entry_type
- library file path
- raw content status
- raw content path or missing-input note
- experiment relevance

### Inventory library entry

- source_id
- reference_id (when available)
- acquisition mode (`web-retrieved` or `user-provided-raw`)
- raw content paths
- extracted knowledge blocks
- anchor notes or unresolved-anchor notes

### Raw provenance artifact

- provenance note
- source acquisition details
- raw file list
- pin/version note when available

### Context bundle

- experiment scope and claim target
- source role matrix
- terminology normalization map
- metric definition map
- conflict log
- open risks and follow-up actions

## Gate Coupling

| Gate | Additional Knowledge-Stack Obligation                                                                  |
| ---- | ------------------------------------------------------------------------------------------------------ |
| G0   | project-level foundations baseline exists and is backed by sourced and library-inventoried authorities |
| G1   | protocol includes definition anchors + context bundle path                                             |
| G2   | authoritative references are pinned and ledgered                                                       |
| G3   | primary references/resources have library-file linkage and provenance status                           |
| G4   | run metadata references context bundle version when applicable                                         |

## Related Artifacts

- `research/projects/mars/definitions/MARS-PIPELINE.md`
- `research/projects/mars/definitions/INVENTORY-LIBRARY-CONTRACT.md`
- `research/projects/mars/definitions/RESEARCH-TAXONOMY.md`
- `research/projects/mars/definitions/RESEARCH-RELATIONSHIPS.md`
- `protocols/MARS-PROTOCOL-CHECKLIST.md`
- `research/projects/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- `implementation/mars/templates/definitions-index-template.md`
- `implementation/mars/templates/domain-context-template.md`
- `implementation/mars/templates/methodology-theory-baseline-template.md`
- `implementation/mars/templates/reference-ledger-template.md`
- `implementation/mars/templates/context-bundle-template.md`
