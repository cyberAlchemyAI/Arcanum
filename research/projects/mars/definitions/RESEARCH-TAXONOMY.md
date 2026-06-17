# MARS Research Artifact Taxonomy

Purpose: define a reusable taxonomy for modeling research and paper artifacts as a typed graph rather than as isolated documents.

This taxonomy is not limited to publication papers. It covers the research knowledge graph that sits behind papers: methodology, references, definitions, foundations, experiments, run data, analysis, evidence, and paper sections.

## Why This Exists

MARS already has strong governance around methodology, references, inventory, experiments, and evidence updates. What it has lacked is an explicit typed ontology connecting those artifacts.

This taxonomy gives a stable vocabulary for answering questions like:

- which methodology artifact governs this protocol?
- which references justify this experiment or paper section?
- which experiment tests which claim?
- which results update which evidence status?
- which paper sections synthesize which parts of the evidence graph?

## Meta-Concept Families

### Inquiry Concepts

| Meta-Concept      | Purpose                                                     | Typical Artifact           |
| ----------------- | ----------------------------------------------------------- | -------------------------- |
| Research Question | the question the program or experiment is trying to answer  | project overview, protocol |
| Claim             | the statement whose support status can change with evidence | `claims/CLAIMS.md`         |
| Hypothesis        | falsifiable expectation that informs experimental design    | `claims/HYPOTHESES.md`     |
| Metric            | measurable construct used to judge outcomes                 | definitions, protocols     |

### Authority Concepts

| Meta-Concept         | Purpose                                                                                | Typical Artifact                                                        |
| -------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Definition           | canonical meaning for a term, construct, or measurement                                | `definitions/DEFINITIONS.md`                                            |
| Methodology Artifact | project- or experiment-scoped method contract                                          | `foundations/METHODOLOGY-AND-THEORY.md`, `experiments/*/methodology.md` |
| Domain Context       | project-scoped explanation of setting, comparators, prior-art frame, and failure modes | `foundations/DOMAIN-CONTEXT.md`                                         |
| Reference            | authoritative cited source with a stable pin                                           | `sources/REFERENCE-LEDGER.md`                                           |
| Source Entry         | discovered and scored source candidate or selected source                              | `sources/SOURCE-CATALOG.md`                                             |
| Inventory Entry      | library-grade extracted knowledge from a source                                        | `inventory/*.md`                                                        |

### Execution Concepts

| Meta-Concept     | Purpose                                                          | Typical Artifact                          |
| ---------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| Experiment       | named evidence-producing investigation                           | `experiments/EXPERIMENTS.md`, bundle root |
| Protocol         | measurable execution contract for one experiment                 | `experiments/*/protocol.md`               |
| Context Bundle   | experiment-scoped synthesis used during execution                | `experiments/*/context.md`                |
| Run Data         | append-only raw data from execution                              | `experiments/*/data/*.jsonl`              |
| Analysis Result  | interpreted outputs from integrity, statistics, or deep analysis | `experiments/*/results/*.md`              |
| Evidence Status  | claim-level support state after adjudication                     | `results/*-EVIDENCE-STATUS.md`            |
| Telemetry Signal | append-only structured operational or governance observation     | `telemetry/*.jsonl`                       |

### Publication Concepts

| Meta-Concept       | Purpose                                                                     | Typical Artifact                     |
| ------------------ | --------------------------------------------------------------------------- | ------------------------------------ |
| Paper Section      | narrative synthesis block in a publication artifact                         | `papers/*.md` section                |
| Retrospective Note | project- or experiment-level reflection on what changed and what to do next | `papers/*.md`, retrospective outputs |
| Export             | reusable published artifact consumed by another project                     | `exports/**`                         |

## Modeling Guidance

1. A paper is not one undifferentiated node. It is best modeled as multiple `Paper Section` nodes that synthesize claims, experiments, results, and references.
2. Methodology should be modeled as an authority concept, not as a paper-only prose note.
3. References and inventory are different concepts:
   - `Reference` captures citation authority and pin metadata.
   - `Inventory Entry` captures reusable extracted content.
4. `Experiment`, `Protocol`, `Run Data`, and `Analysis Result` are different execution states and should not be collapsed.
5. A project foundations baseline is represented through `Domain Context` plus `Methodology Artifact` rather than by overloading the paper stub.

## Minimal Paper Graph For MARS

The smallest useful paper-oriented graph in MARS usually includes:

- Claim
- Methodology Artifact
- Reference
- Experiment
- Analysis Result
- Evidence Status
- Paper Section

That minimum graph is enough to represent:

- what the paper is arguing
- how the argument is being tested
- which sources justify the approach
- what evidence was produced
- how the paper text should trace back to underlying evidence

## Example Mapping (MOGT)

| Artifact                                                   | Meta-Concept               |
| ---------------------------------------------------------- | -------------------------- |
| `foundations/DOMAIN-CONTEXT.md`                            | Domain Context             |
| `foundations/METHODOLOGY-AND-THEORY.md`                    | Methodology Artifact       |
| `claims/CLAIMS.md` rows                                    | Claim                      |
| `claims/HYPOTHESES.md` rows                                | Hypothesis                 |
| `sources/REFERENCE-LEDGER.md` rows                         | Reference                  |
| `inventory/methodology-authorities.md`                     | Inventory Entry collection |
| `experiments/E1-*/protocol.md`                             | Protocol                   |
| `experiments/E1-*/data/*.jsonl`                            | Run Data                   |
| `experiments/E1-*/results/*.md`                            | Analysis Result            |
| `results/MOGT-EVIDENCE-STATUS.md` rows                     | Evidence Status            |
| `papers/mogt-agentic-conversation-paper.md` section blocks | Paper Section              |

## Scope Rule

Use this taxonomy for research and paper artifacts. Do not overload it with software-domain entities that belong in DomainSpec's business and UI taxonomy.
