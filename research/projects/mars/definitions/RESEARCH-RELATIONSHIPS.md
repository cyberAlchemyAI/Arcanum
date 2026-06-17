# MARS Research Artifact Relationships

Purpose: define typed edges between research-artifact concepts so papers and evidence programs can be modeled as an explicit graph.

This relationship set is meant to work with `RESEARCH-TAXONOMY.md`.

## Core Edge Set

| Edge              | Meaning                                                                   |
| ----------------- | ------------------------------------------------------------------------- |
| `frames`          | gives the question, setting, or comparative frame for another artifact    |
| `defines`         | provides canonical meaning for a term or metric used elsewhere            |
| `anchors`         | formally constrains or governs another artifact                           |
| `cites`           | references an authority source for justification or synthesis             |
| `inventory-of`    | preserves extracted reusable content from a source                        |
| `operationalizes` | turns a higher-level idea into a measurable or executable artifact        |
| `tests`           | evaluates a claim or hypothesis through an experiment                     |
| `measures`        | declares the metric or measurable outcome for an experiment or protocol   |
| `produces`        | creates a downstream artifact, typically run data or analysis result      |
| `analyzes`        | interprets or processes raw run data                                      |
| `updates`         | changes claim evidence or status state                                    |
| `synthesizes`     | integrates evidence and authorities into paper or retrospective narrative |
| `exports`         | publishes a reusable artifact for downstream consumption                  |

## Typed Signatures

| Edge              | Allowed Source Types                                                           | Allowed Target Types                                           |
| ----------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| `frames`          | Domain Context, Methodology Artifact, Research Question                        | Claim, Hypothesis, Experiment, Protocol, Paper Section         |
| `defines`         | Definition                                                                     | Metric, Claim, Hypothesis, Protocol, Paper Section             |
| `anchors`         | Methodology Artifact, Definition, Reference                                    | Protocol, Context Bundle, Paper Section                        |
| `cites`           | Methodology Artifact, Domain Context, Protocol, Analysis Result, Paper Section | Reference                                                      |
| `inventory-of`    | Inventory Entry                                                                | Reference, Source Entry                                        |
| `operationalizes` | Claim, Hypothesis, Methodology Artifact, Domain Context                        | Experiment, Protocol, Metric                                   |
| `tests`           | Experiment                                                                     | Claim, Hypothesis                                              |
| `measures`        | Protocol, Experiment                                                           | Metric                                                         |
| `produces`        | Experiment, Protocol, Analysis Result                                          | Run Data, Analysis Result, Telemetry Signal                    |
| `analyzes`        | Analysis Result                                                                | Run Data                                                       |
| `updates`         | Analysis Result, Telemetry Signal                                              | Evidence Status, Claim                                         |
| `synthesizes`     | Paper Section, Retrospective Note                                              | Claim, Experiment, Analysis Result, Evidence Status, Reference |
| `exports`         | Evidence Status, Analysis Result, Methodology Artifact                         | Export                                                         |

## Practical Interpretation

### Paper Modeling

A paper section is typically connected through:

- `synthesizes` -> Claim
- `synthesizes` -> Analysis Result
- `cites` -> Reference
- `anchors` -> Methodology Artifact or Definition

This means a paper section can be traced backward to both the authorities that justify its wording and the evidence that supports it.

### Experiment Modeling

An experiment is typically connected through:

- `tests` -> Claim or Hypothesis
- `measures` -> Metric
- `produces` -> Run Data
- `produces` -> Analysis Result

This makes the evidence path explicit instead of implicit.

### Source-Library Modeling

A library-grade inventory should look like:

- Source Entry `cites` or points to the discovered source record
- Reference provides the authoritative pinned version
- Inventory Entry `inventory-of` the Reference or Source Entry
- Methodology Artifact / Domain Context / Protocol `cites` the Reference

This preserves the distinction between discovery, authority, and extracted reusable content.

## Example Graph (MOGT)

1. `foundations/DOMAIN-CONTEXT.md` `frames` E1, E2, E3, E4.
2. `foundations/METHODOLOGY-AND-THEORY.md` `anchors` E1 protocol and E2 protocol.
3. `PAPER-WOHLIN-2012` is `cites`-linked from the methodology baseline and from experiment protocols.
4. E2 `tests` MOGT-C2 and `measures` MOGT-M1 plus dominated-selection outcomes.
5. E2 `produces` run data and analysis result artifacts.
6. The paper section on arbitration quality `synthesizes` MOGT-C2, E2 results, and its cited references.

## Usage Rules

1. Use `cites` only for authority reference links, not for general causal or evidence flow.
2. Use `anchors` when an artifact is governed or constrained by another artifact.
3. Use `operationalizes` when an abstract research object becomes an executable or measurable object.
4. Use `produces` and `analyzes` to keep raw data and interpreted outputs separate.
5. Use `synthesizes` only for narrative artifacts such as paper sections or retrospectives.
6. If a relation is needed repeatedly but not covered here, add it explicitly rather than overloading an existing edge.
