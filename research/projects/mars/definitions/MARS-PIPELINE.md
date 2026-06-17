# MARS Research Pipeline v1 (13 Stages)

This document defines the canonical pipeline for the MARS research program.

Primary objective: system validity with explicit governance gates and traceable evidence.

## Pipeline Stages

| Stage | Name                                    | Owner             | Inputs                                                             | Outputs                                                                                                                                          | Tier              |
| ----- | --------------------------------------- | ----------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| S0    | Project Foundations Baseline            | Scientist         | Research objective, project overview, seeded authority directions  | `foundations/DOMAIN-CONTEXT.md`, `foundations/METHODOLOGY-AND-THEORY.md`, source catalog, reference ledger, and library-grade inventory coverage | Foundation + Full |
| S1    | Methodology Profile Selection           | Scientist         | Research objective, constraints                                    | Method profile artifact (`experiments/<experiment-key>/methodology.md`)                                                                          | Foundation + Full |
| S2    | Claim Framing and Questions             | Scientist         | Paper scope, prior evidence, definitions index                     | Claims, research questions, and definition anchors                                                                                               | Foundation + Full |
| S3    | Protocol Design and Validation          | Protocol Designer | Claims, experiment intent, methodology profile, existing templates | Protocol file, measurable criteria, schema                                                                                                       | Foundation + Full |
| S4    | Source Discovery and Scoring            | Sourcer           | Protocol requirements, reference ledger                            | Source candidates, ranked selection, and reference-ledger updates                                                                                | Foundation + Full |
| S5    | Source Quality Gate                     | Sourcer           | Candidate sources                                                  | Pass/fail decision with version pins                                                                                                             | Foundation + Full |
| S6    | Inventory Extraction and Readiness Gate | Inventorist       | Selected sources, prior inventory, context requirements            | Inventory readiness report and context bundle readiness                                                                                          | Foundation + Full |
| S7    | Experiment Execution and Data Capture   | Scientist         | Protocol, source and inventory ready                               | Raw JSONL run file(s)                                                                                                                            | Foundation + Full |
| S8    | Data Integrity Audit                    | Analyst           | Raw JSONL and schema                                               | Integrity report, gate decision                                                                                                                  | Foundation + Full |
| S9    | Core Statistical Evaluation             | Analyst           | Clean data, success criteria                                       | Descriptive + criteria pass/fail table                                                                                                           | Foundation + Full |
| S10   | Deep Analysis Pack                      | Analyst           | Clean data, related results                                        | Subgroups, sensitivity, triangulation, threats                                                                                                   | Full              |
| S11   | Claim Adjudication and Evidence Update  | Evidence Auditor  | Analysis outputs, claim map                                        | Claim evidence status and experiment priority updates                                                                                            | Foundation + Full |
| S12   | Paper Integration and Retrospective     | Scientist         | Evidence status and findings                                       | Paper updates, retrospective actions                                                                                                             | Full              |

## Tiered Rigor Policy

### Foundation tier

Use for early or low-cost experiments where primary goal is directional validity.

Required stages:

- S0 through S9
- S11

Optional stage:

- S10

### Full tier

Use for high-impact experiments and publication-critical claims.

Required stages:

- S0 through S12

## Hard Governance Gates

Execution is blocked when any hard gate fails.

| Gate | Condition                                                                                                                                                                 | Enforced at |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| G0   | Project foundations baseline exists with domain-context and methodology/theory artifacts backed by source catalog, reference ledger, and library-grade inventory coverage | S0          |
| G1   | Methodology-linked protocol with definition/context anchors approved and measurable                                                                                       | S3          |
| G2   | Source and authoritative reference selection include accessibility, depth, and version pin                                                                                | S5          |
| G3   | Inventory readiness confirmed for required entry types                                                                                                                    | S6          |
| G4   | Data integrity pass (schema and metadata)                                                                                                                                 | S8          |

## Project Foundations Contract

Project-level research foundations must exist before experiment protocol design begins:

- `foundations/DOMAIN-CONTEXT.md`
- `foundations/METHODOLOGY-AND-THEORY.md`
- `sources/SOURCE-CATALOG.md`
- `sources/REFERENCE-LEDGER.md`
- `inventory/INVENTORY-INDEX.md`

## Experiment Bundle Contract

All experiment-scoped artifacts must live inside one bundle directory:

- `experiments/<experiment-key>/methodology.md`
- `experiments/<experiment-key>/protocol.md`
- `experiments/<experiment-key>/sources.md`
- `experiments/<experiment-key>/context.md`
- `experiments/<experiment-key>/data/*.jsonl`
- `experiments/<experiment-key>/results/*.md`

Legacy flat experiment files are migration-only and must not receive new writes.

## Required Artifacts by Stage

| Stage  | Required Artifact                                                                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S0     | `foundations/DOMAIN-CONTEXT.md`, `foundations/METHODOLOGY-AND-THEORY.md`, `sources/SOURCE-CATALOG.md`, `sources/REFERENCE-LEDGER.md`, and library-grade inventory entries |
| S1     | `experiments/<experiment-key>/methodology.md`                                                                                                                             |
| S2     | `research/projects/mars/definitions/DEFINITIONS-INDEX.md`                                                                                                                    |
| S3     | `experiments/<experiment-key>/protocol.md`                                                                                                                                |
| S4-S5  | `experiments/<experiment-key>/sources.md` and `sources/REFERENCE-LEDGER.md`                                                                                               |
| S6     | `experiments/<experiment-key>/context.md` plus `inventory/INVENTORY-INDEX.md` and source-linked inventory entries                                                         |
| S7     | `experiments/<experiment-key>/data/run-YYYY-MM-DD[-suffix].jsonl`                                                                                                         |
| S8-S10 | `experiments/<experiment-key>/results/<run-id>-results.md`                                                                                                                |
| S11    | `results/MARS-EVIDENCE-STATUS.md`                                                                                                                                         |
| S12    | `papers/*.md` section update + retrospective note                                                                                                                         |

Protocol gate template:

- `protocols/MARS-PROTOCOL-CHECKLIST.md`

Methodology contract:

- `research/projects/mars/definitions/METHODOLOGY-PROFILE-CONTRACT.md`

Knowledge stack contract:

- `research/projects/mars/definitions/RESEARCH-KNOWLEDGE-STACK-CONTRACT.md`

Experiment bundle policy:

- `research/projects/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`

## Default Handoff Chain

1. Sourcer -> source selection and quality gate.
2. Inventorist -> reference library and inventory readiness gate.
3. Scientist -> experiment execution and data capture.
4. Analyst -> integrity plus analysis outputs.
5. Evidence Auditor -> claim status update and next-run priorities.
6. Scientist -> paper integration and retrospective closure.
