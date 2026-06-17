# MARS Definitions Index

Purpose: canonical terminology used across planning, execution, analysis, and evidence adjudication.

## Definitions

| Definition ID | Term                         | Canonical Meaning                                                                              | Scope                       | Linked Claims             |
| ------------- | ---------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------- | ------------------------- |
| MARS-DEF-001  | Methodology profile          | experiment-specific method contract declaring tier and analysis commitments                    | protocol governance         | MARS-C2                   |
| MARS-DEF-002  | Source quality gate          | G2 check for accessibility, depth, and pin quality of selected sources                         | sourcing                    | MARS-C2, MARS-C3          |
| MARS-DEF-003  | Inventory readiness gate     | G3 check that primary sources are inventoried and traceable                                    | inventory governance        | MARS-C1, MARS-C2          |
| MARS-DEF-004  | Context bundle               | experiment-scoped synthesis of definitions, references, metrics, and conflicts                 | execution readiness         | MARS-C1, MARS-C3          |
| MARS-DEF-005  | Claim adjudication           | structured update of evidence strength and claim status from analyzed runs                     | evidence governance         | MARS-C1..MARS-C4          |
| MARS-DEF-006  | Foundation tier              | minimum valid analysis path for directional evidence                                           | methodology                 | MARS-C2                   |
| MARS-DEF-007  | Full tier                    | publication-grade analysis path with deep validity treatment                                   | methodology                 | MARS-C2, MARS-C4          |
| MARS-DEF-008  | Project foundations baseline | project-scoped domain-context and methodology/theory artifacts required before protocol design | project baseline governance | MARS-C1, MARS-C2          |
| MARS-DEF-009  | Reference library            | reusable inventory layer preserving extracted authority content for later reuse                | knowledge-stack governance  | MARS-C1, MARS-C2, MARS-C4 |
| MARS-DEF-010  | Research artifact taxonomy   | canonical node vocabulary for research and paper artifacts                                     | knowledge graph governance  | MARS-C1, MARS-C4          |
| MARS-DEF-011  | Typed research relationships | canonical edge vocabulary connecting research and paper artifacts                              | knowledge graph governance  | MARS-C1, MARS-C4          |
| MARS-DEF-012  | Inventory library entry      | per-source extracted-content artifact with reusable knowledge and provenance linkage           | inventory governance        | MARS-C1, MARS-C2, MARS-C4 |
| MARS-DEF-013  | Raw content artifact         | retrieved or user-provided source material used as provenance base for inventory extraction    | inventory governance        | MARS-C1, MARS-C2, MARS-C4 |

## Usage Rules

1. New protocol terms must be added here before they are used as gate-critical requirements.
2. If a term meaning changes, update this file first, then update affected protocols.
