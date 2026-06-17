# MARS Research Project

MARS is the research-orchestration project that defines and validates a gated, reproducible lifecycle for experiment design, execution, evidence adjudication, and paper integration.

This project is self-contained under `research/projects/mars` and follows canonical-only paths (no compatibility aliases).

## What This Project Is About

MARS exists to answer one core question:

Can we run research programs with deterministic governance gates, explicit dependency contracts, and traceable evidence updates so claim quality improves over time?

## Canonical Asset Model

- Canonical reusable MARS definitions and templates live under `research/projects/mars/definitions` and `implementation/mars/templates`.
- `research/projects/mars` is the project projection and evidence workspace where runs, data, adjudications, and claim updates are executed.
- When canonical definitions/templates change, refresh projection copies with `./tools/sync_mars_canonical_assets.sh`.

The project operationalizes this through:

- 13-stage pipeline orchestration (`research/projects/mars/definitions/MARS-PIPELINE.md`)
- hard governance gates G1-G4
- claim-level evidence tracking (`results/MARS-EVIDENCE-STATUS.md`)
- explicit dependency contracts (`deps/DEPENDENCIES.yaml`)
- a research-artifact ontology for modeling methodology, references, experiments, results, and paper sections as a typed graph

## Research Artifact Ontology

MARS can model papers and research programs as explicit graphs, not just as disconnected markdown files.

Canonical ontology artifacts:

- `research/projects/mars/definitions/RESEARCH-TAXONOMY.md`
- `research/projects/mars/definitions/RESEARCH-RELATIONSHIPS.md`

This makes it possible to model relations such as:

- methodology `anchors` protocol
- paper section `cites` reference
- experiment `tests` claim
- experiment `measures` metric
- experiment `produces` run data and analysis
- analysis `updates` evidence status
- paper section `synthesizes` claims, results, and references

This ontology is for research and paper artifacts. It is not a replacement for DomainSpec's software-domain taxonomy.

## Inventory Library Chain

MARS now treats library-grade inventory as a visible provenance chain, not just as a summary layer.

Canonical assets:

- `research/projects/mars/definitions/INVENTORY-LIBRARY-CONTRACT.md`
- `implementation/mars/templates/inventory-schema-template.md`
- `implementation/mars/templates/inventory-library-entry-template.md`
- `implementation/mars/templates/raw-content-note-template.md`

Required chain:

1. `sources/SOURCE-CATALOG.md`
2. `sources/REFERENCE-LEDGER.md`
3. `inventory/INVENTORY-INDEX.md`
4. `inventory/library/<source-id>.md`
5. `inventory/raw/<source-id>/...`

If source material cannot be retrieved lawfully or technically from the web, the workflow should request user-provided raw files and inventory against those files explicitly.

## Experimental Paper Design Pilot

MARS now carries an experimental paper-design workflow that applies a DomainSpec-style contract to paper work without yet turning it into a hard pipeline gate.

Pilot assets:

- reusable derivation rules: `research/projects/mars/definitions/PAPER-DERIVATION-RULES.md`
- reusable templates: `implementation/mars/templates/paper-spec-template.md`, `implementation/mars/templates/paper-stories-template.md`, `implementation/mars/templates/paper-test-spec-template.md`, `implementation/mars/templates/paper-review-template.md`
- framework proposal: `research/projects/mars/runbooks/PAPER-DESIGN-WORKFLOW-PILOT-2026-04-28.md`

Current intent:

- use project research graphs as the input authority
- derive lightweight paper-contract artifacts before full narrative writing
- capture lessons from live pilots before making paper design a formal MARS gate or command

## Research Startpoint

MARS now includes a dedicated startpoint for greenfield project initialization and brownfield baseline audits.

Primary command:

```
@mars-research-interviewer mars-research-start [greenfield|brownfield|auto] [topic-or-project]
```

What this adds:

- Research-scope discovery before protocol design
- Project foundations baseline before protocol design
- Greenfield project initialization into a repository-valid MARS project baseline
- Brownfield evidence inspection (claims, protocols, results, data) before questioning
- Registry integration and dependency-graph registration for new projects
- Structural validation before protocol design or execution handoff

Startpoint artifact baseline:

- `README.md`
- `PROJECT.yaml`
- `foundations/DOMAIN-CONTEXT.md`
- `foundations/METHODOLOGY-AND-THEORY.md`
- `PROJECT-OVERVIEW.md`
- `definitions/DEFINITIONS.md`
- `definitions/DEFINITIONS-INDEX.md`
- `definitions/INITIAL-DEFINITIONS.md`
- `claims/CLAIMS.md`
- `claims/HYPOTHESES.md`
- `experiments/EXPERIMENTS.md`
- `experiments/EXPERIMENT-CANDIDATES.md`

Validation after init or normalization:

- `./tools/update_project_experiments_index.sh <project-key>`
- `./tools/check_research_structure.sh`

Direct discovery mode remains available when you only want scoping artifacts without startpoint gating:

```
@mars-research-interviewer mars-research-interview [greenfield|brownfield|auto] [topic-or-project]
```

Discovery-only output artifact set:

- `PROJECT-OVERVIEW.md`
- `definitions/INITIAL-DEFINITIONS.md`
- `claims/HYPOTHESES.md`
- `experiments/EXPERIMENT-CANDIDATES.md`

Template sources:

- `implementation/mars/templates/project-overview-template.md`
- `implementation/mars/templates/initial-definitions-template.md`
- `implementation/mars/templates/hypotheses-template.md`
- `implementation/mars/templates/experiment-candidates-template.md`

Asset paths:

- Agent: `.github/agents/mars-research-interviewer.agent.md`
- Skill: `.github/skills/mars-research-start/SKILL.md`
- Skill: `.github/skills/mars-research-foundations/SKILL.md`
- Skill: `.github/skills/mars-research-interview/SKILL.md`

## Research Foundations Baseline

MARS now treats project-level research foundations as a required step before protocol design.

Primary command:

```bash
@mars-research-scientist mars-research-foundations <project-key>
```

This step should produce and maintain:

- `foundations/DOMAIN-CONTEXT.md`
- `foundations/METHODOLOGY-AND-THEORY.md`
- `sources/SOURCE-CATALOG.md`
- `sources/REFERENCE-LEDGER.md`
- `inventory/INVENTORY-INDEX.md`, `inventory/INVENTORY-SCHEMA.md`, per-source library files, and raw provenance coverage

Intent:

- explain the research setting before experiment bundles define narrower contexts
- explain the methodology and theory baseline before protocols define thresholds and metrics
- force sourcing and inventorization early enough that later protocol authors can consult a reusable reference library instead of rediscovering the same authorities

Protocol design should be treated as blocked until this baseline exists and is backed by sourced and inventoried authorities.

## Telemetry and Reflection

MARS now has a structured signal-emission model for capturing workflow blind spots, contract drift, evidence blockers, and improvement proposals.

Primary command:

```bash
@mars-research-scientist mars-research-emit-signals <project-key> [--experiment <experiment-key>] [--mode startpoint|discovery|planning|execution|analysis|adjudication|retrospective]
```

Signal families are defined in:

- `telemetry/SIGNAL-SCHEMA.md`

The current signal model is designed to catch exactly the kind of issue we saw in greenfield research-project creation:

- `workflow-gap` for missing structured workflows or startpoints
- `contract-gap` for missing required artifacts or registry integration
- `evidence-gap` for blocked analysis, adjudication, or claim propagation
- `decision-friction` for repeated clarifications and unresolved options
- `overhead`, `proposal`, and `pattern` for reflective framework improvement

Signal log:

- `telemetry/signals.jsonl`

Planned reflective use:

- recurring `workflow-gap` -> create or harden MARS commands
- recurring `contract-gap` -> strengthen startpoint and templates
- recurring `evidence-gap` -> refine analysis and adjudication workflows

## Current Snapshot (2026-04-21)

- Status: active, bootstrap stage
- Version: 0.1.0
- Owner: mars-research-scientist
- Latest run state: tabletop dry run completed, live execution not yet completed

## Completeness Dashboard

### Weighted Completeness

- Structural completeness (40% weight): 100%
- Empirical completeness (40% weight): 20%
- Publication completeness (20% weight): 0%
- Overall weighted completeness: 48%

Scoring note:

- Structural = required project contract and canonical governance artifacts present.
- Empirical = live sourcing, inventory, data capture, integrity audit, and evidence updates.
- Publication = paper-facing synthesis and retrospective artifacts.

### Artifact Lane Status

| Lane                   | Expected Outcome                                              | Current State                                                                  | Status      |
| ---------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------- |
| Project contract       | PROJECT, claims, dependencies, registry, telemetry schema     | Present                                                                        | complete    |
| Governance definitions | pipeline + gate policies + protocol checklist                 | Present                                                                        | complete    |
| Execution evidence     | experiment specs, live data files, integrity/analysis outputs | Dry run exists; no live JSONL data yet                                         | in progress |
| Source and inventory   | source selection artifacts and inventory coverage             | methodology authority baseline is seeded; experiment-specific coverage pending | in progress |
| Claim adjudication     | claim evidence updates from completed analyses                | Evidence file exists, mostly insufficient/partial support                      | in progress |
| Publication            | paper updates and retrospective outputs                       | `papers/` empty                                                                | missing     |
| Exports                | reusable methods/claim exports for downstream consumers       | Present                                                                        | complete    |

## Gate Readiness

From the latest dry run (`experiments/MARS-DRY-RUN-E1-foundation/protocol.md`):

| Gate                   | Current Decision | Meaning                                 |
| ---------------------- | ---------------- | --------------------------------------- |
| G1 Protocol measurable | pass             | Protocol quality baseline is acceptable |
| G2 Source quality      | pass             | Sources are identifiable and pinnable   |
| G3 Inventory readiness | pending          | Inventory artifacts are not complete    |
| G4 Data integrity      | pending          | No live run data generated yet          |

## What Is Missing Right Now

1. Expand `sources/` beyond methodology authorities with experiment-specific source selections.
2. Expand `inventory/` beyond baseline authority entries with experiment readiness reports.
3. Execute at least one live foundation run and write JSONL outputs under `experiments/<experiment-key>/data/`.
4. Produce integrity and analysis outputs tied to that live run.
5. Update claim evidence statuses from live-run analysis, not just inherited upstream evidence.
6. Create first paper-facing synthesis artifact under `papers/`.

## Claim Coverage Summary

Current evidence baseline (`results/MARS-EVIDENCE-STATUS.md`):

- MARS-C1: weak, insufficient evidence
- MARS-C2: moderate, partially supported
- MARS-C3: insufficient evidence
- MARS-C4: insufficient evidence

Interpretation:

- MARS currently has governance scaffolding and initial traceability.
- It still lacks enough empirical runs to support strong claim adjudication.

## Canonical File Map

- Project manifest: `PROJECT.yaml`
- Canonical definitions root: `research/projects/mars/definitions/`
- Canonical templates root: `implementation/mars/templates/`
- Canonical definitions source: `research/projects/mars/definitions/DEFINITIONS.md`
- Pipeline definition (canonical): `research/projects/mars/definitions/MARS-PIPELINE.md`
- Methodology contract (canonical): `research/projects/mars/definitions/METHODOLOGY-PROFILE-CONTRACT.md`
- Knowledge stack contract (canonical): `research/projects/mars/definitions/RESEARCH-KNOWLEDGE-STACK-CONTRACT.md`
- Inventory library contract (canonical): `research/projects/mars/definitions/INVENTORY-LIBRARY-CONTRACT.md`
- Research taxonomy (canonical): `research/projects/mars/definitions/RESEARCH-TAXONOMY.md`
- Research relationships (canonical): `research/projects/mars/definitions/RESEARCH-RELATIONSHIPS.md`
- Paper derivation rules (experimental): `research/projects/mars/definitions/PAPER-DERIVATION-RULES.md`
- Definitions index (canonical): `research/projects/mars/definitions/DEFINITIONS-INDEX.md`
- Experiment bundle contract (canonical): `research/projects/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- Definitions projection copy: `research/projects/mars/definitions/`
- Templates projection copy: `research/projects/mars/templates/`
- Protocol checklist: `protocols/MARS-PROTOCOL-CHECKLIST.md`
- Source catalog: `sources/SOURCE-CATALOG.md`
- Reference ledger: `sources/REFERENCE-LEDGER.md`
- Inventory index: `inventory/INVENTORY-INDEX.md`
- Inventory schema: `inventory/INVENTORY-SCHEMA.md`
- Inventory library: `inventory/library/*.md`
- Inventory raw provenance: `inventory/raw/**`
- Experiment methodology: `experiments/*/methodology.md`
- Experiment context bundle: `experiments/*/context.md`
- Claims: `claims/CLAIMS.md`
- Dependencies: `deps/DEPENDENCIES.yaml`
- Artifact index: `registry/ARTIFACT-INDEX.md`
- Traceability matrix: `registry/TRACEABILITY-MATRIX.md`
- Telemetry schema: `telemetry/SIGNAL-SCHEMA.md`
- Telemetry log: `telemetry/signals.jsonl`
- Evidence status: `results/MARS-EVIDENCE-STATUS.md`
- Paper workflow pilot proposal: `runbooks/PAPER-DESIGN-WORKFLOW-PILOT-2026-04-28.md`

## Experiment Bundle Policy

Each experiment must keep protocol, source selection, run data, and results under its own bundle directory:

- `experiments/<experiment-key>/methodology.md`
- `experiments/<experiment-key>/protocol.md`
- `experiments/<experiment-key>/sources.md`
- `experiments/<experiment-key>/context.md`
- `experiments/<experiment-key>/data/*.jsonl`
- `experiments/<experiment-key>/results/*.md`

Governance contract:

- `research/projects/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`

Migration plan for current flat artifacts:

- `runbooks/EXPERIMENT-BUNDLE-MIGRATION-PLAN.md`

## Dependency Policy

All upstream dependencies must be declared in `deps/DEPENDENCIES.yaml`.
Cross-project consumption is allowed only through declared dependency contracts and published exports.

Canonical/projection maintenance command:

```bash
./tools/sync_mars_canonical_assets.sh
```
