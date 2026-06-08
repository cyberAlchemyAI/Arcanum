# Multi-Objective Game Theory for Agentic Conversation Decisions Research Project

This project tests whether multi-objective game theory can improve how agentic systems make conversation-level decisions when they must trade off quality, cost, latency, safety, and escalation risk.

It is a greenfield research program under `research/mogt-agentic-conversation` with MARS-compatible gates, experiment bundles, and evidence tracking.

## Public Two-Repository Connection

This project is designed as Repo 2 (`mogt-agentic-conversation`) connected to Repo 1 (`mars`).

- Upstream framework contracts are consumed from the MARS repository.
- This repository owns only MOGT-specific claims, experiments, data, results, and paper artifacts.
- Cross-repository coupling is allowed only through explicit entries in `deps/DEPENDENCIES.yaml` and published MARS exports.

Recommended split from this monorepo:

1. `mars` repo sourced from `implementation/mars`
2. `mogt-agentic-conversation` repo sourced from `research/mogt-agentic-conversation`

## How People Can Help

High-value public contribution lanes:

1. Improve experiment protocols and measurable criteria in `experiments/*/protocol.md`.
2. Expand source quality and inventory provenance coverage.
3. Build benchmark datasets and blinded review rubrics for E1-E4.
4. Review result interpretation and validity-threat documentation once runs are published.

## What This Project Is About

The core question is whether explicit multi-objective and game-theoretic decision policies outperform implicit heuristic arbitration in agentic conversations.

The project focuses on four linked concerns:

- whether explicit objective vectors improve traceability of agent decisions
- whether Pareto-aware selection improves outcome quality under competing goals
- whether negotiation and equilibrium-inspired coordination reduce unresolved disagreement
- whether the added reasoning overhead stays inside an operationally acceptable envelope

The program operationalizes this through project-level foundations baselines, claims, canonical definitions, draft experiment bundles, source governance, a library-grade inventory chain with raw provenance, telemetry for conversation decisions, claim-level evidence updates, and an experimental paper-design contract derived from the research graph.

The project now also maintains an explicit research graph so methodology, references, experiments, and paper sections can be traced as typed MARS relationships rather than only as prose links.

## Current Snapshot (2026-04-27)

- Status: planning
- Version: 0.1.0
- Owner: mars-research-scientist
- Latest run state: project scaffold established, no live runs executed yet

## Completeness Dashboard

### Weighted Completeness

- Structural completeness (40% weight): 100%
- Empirical completeness (40% weight): 0%
- Publication completeness (20% weight): 10%
- Overall weighted completeness: 42%

Scoring note:

- Structural = required project contract and canonical governance artifacts present.
- Empirical = sources, inventory, data capture, integrity checks, analysis outputs, evidence updates.
- Publication = paper-facing synthesis and retrospective artifacts.

### Artifact Lane Status

| Lane                              | Expected Outcome                                                                           | Current State                                                                                                                                                     | Status      |
| --------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Project contract                  | PROJECT, claims, dependencies, registry, telemetry schema                                  | Present                                                                                                                                                           | complete    |
| Governance definitions            | canonical definitions, hypotheses, protocol checklist, experiment index, and draft bundles | Present but still greenfield and unvalidated                                                                                                                      | in progress |
| Execution evidence                | experiment specs, data files, analysis outputs                                             | Draft experiment bundles exist, no data or results yet                                                                                                            | missing     |
| Foundations, source and inventory | project foundations baseline, source selection, library files, and raw provenance coverage | foundations baselines are present; open prior-art coverage now has library-backed entries, while several methodology and theory authorities still await raw input | in progress |
| Claim adjudication                | claim-level evidence status updates                                                        | Evidence status scaffold exists, all claims are still insufficient                                                                                                | in progress |
| Publication                       | paper updates and retrospective outputs                                                    | Paper stub and pilot paper-contract artifacts exist, but no empirical synthesis yet                                                                               | in progress |
| Exports                           | reusable published artifacts for dependents                                                | Export scaffold exists, no published outputs yet                                                                                                                  | missing     |

## What Is Missing Right Now

1. Complete second-wave authority normalization for negotiation-specific theory and the Marler weighted-sum versus survey split.
2. Build the first benchmark conversation corpus and decision-review rubric for E1 and E2.
3. Run a MARS gate walkthrough and first dry execution for the highest-priority experiments.
4. Produce the first append-only JSONL run files and integrity reports under the experiment bundles.
5. Upgrade or reject the initial claims based on measured results rather than design-time reasoning.

## Canonical File Map

- Project manifest: PROJECT.yaml
- Project overview: PROJECT-OVERVIEW.md
- Domain context baseline: foundations/DOMAIN-CONTEXT.md
- Methodology and theory baseline: foundations/METHODOLOGY-AND-THEORY.md
- Canonical definitions source: definitions/DEFINITIONS.md
- Definitions index: definitions/DEFINITIONS-INDEX.md
- Initial definitions notes: definitions/INITIAL-DEFINITIONS.md
- Claims: claims/CLAIMS.md
- Hypotheses: claims/HYPOTHESES.md
- Dependencies: deps/DEPENDENCIES.yaml
- Protocol checklist: protocols/MOGT-PROTOCOL-CHECKLIST.md
- Experiment index: experiments/EXPERIMENTS.md
- Experiment candidates: experiments/EXPERIMENT-CANDIDATES.md
- Module Formulae model: module-formulae/
- Formal/runtime MOGT definition: module-formulae/formal-runtime-definition.md
- Runtime decision receipt contract: module-formulae/runtime-decision-receipt.md
- Artifact index: registry/ARTIFACT-INDEX.md
- Research graph: registry/RESEARCH-GRAPH.md
- Traceability matrix: registry/TRACEABILITY-MATRIX.md
- Paper spec: papers/PAPER-SPEC.md
- Paper stories: papers/PAPER-STORIES.md
- Paper test spec: papers/PAPER-TEST-SPEC.md
- Paper review: papers/PAPER-REVIEW.md
- Source catalog: sources/SOURCE-CATALOG.md
- Reference ledger: sources/REFERENCE-LEDGER.md
- Inventory index: inventory/INVENTORY-INDEX.md
- Inventory schema: inventory/INVENTORY-SCHEMA.md
- Inventory library: inventory/library/\*.md
- Inventory raw provenance: inventory/raw/\*\*
- Evidence matrix: results/MOGT-EVIDENCE-STATUS.md
- Paper stub: papers/mogt-agentic-conversation-paper.md
- Telemetry schema: telemetry/SIGNAL-SCHEMA.md

## Dependency Policy

All upstream dependencies must be declared in deps/DEPENDENCIES.yaml.
Cross-project consumption is allowed only through declared dependency contracts and published exports.
Implicit dependencies on non-MARS frameworks are out of scope for the public MOGT repository.
