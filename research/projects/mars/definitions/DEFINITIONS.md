# MARS Canonical Definitions

Purpose: normative semantics for MARS governance terms used across planning, execution, analysis, and evidence adjudication.

Interpretation rule:

- Definition statements are normative.
- `Intuition` notes are explanatory and non-normative.

## MARS-DEF-001 Methodology Profile

Definition:
A methodology profile is the experiment-scoped method contract that declares tier, measurement commitments, validity-treatment policy, and reproducibility metadata obligations.

Intuition:
This is the ruleset for how the experiment must be run and judged, not just a description of intent.

## MARS-DEF-002 Source Quality Gate (G2)

Definition:
The source quality gate is the mandatory control that verifies selected sources satisfy accessibility, authority-depth fitness, and immutable version-pin requirements before execution can proceed.

Intuition:
If sources are weak or unpinned, all later conclusions are fragile.

## MARS-DEF-003 Inventory Readiness Gate (G3)

Definition:
The inventory readiness gate is the mandatory control that verifies every required primary source has complete inventory extraction coverage and traceable linkage to experiment requirements.

Intuition:
Do not run an experiment if required knowledge was not extracted and normalized first.

## MARS-DEF-004 Context Bundle

Definition:
A context bundle is the experiment-scoped synthesis artifact that normalizes term mappings, metric definitions, source roles, and known conflicts required for deterministic execution and interpretation.

Intuition:
This is the shared map that keeps everyone using the same meaning during the run.

## MARS-DEF-005 Claim Adjudication

Definition:
Claim adjudication is the structured decision process that maps analyzed experiment evidence to claim-strength status and records explicit support, weakness, or contradiction updates.

Intuition:
It is the formal judgment step where evidence changes claim confidence.

## MARS-DEF-006 Foundation Tier

Definition:
Foundation tier is the minimum valid rigor mode requiring stages S1-S9 and S11, with optional S10, to produce directional evidence under hard-gate enforcement.

Intuition:
This is the cheapest acceptable run that still produces credible directional findings.

## MARS-DEF-007 Full Tier

Definition:
Full tier is the publication-grade rigor mode requiring stages S1-S12 with deep-analysis and synthesis obligations for high-impact claim updates.

Intuition:
This is the complete end-to-end evidence path used when stronger confidence is required.

## MARS-DEF-008 Project Foundations Baseline

Definition:
The project foundations baseline is the pair of project-scoped artifacts `foundations/DOMAIN-CONTEXT.md` and `foundations/METHODOLOGY-AND-THEORY.md` that explain the research setting, methodological posture, theory baseline, and prior-art frame before protocol design begins.

Intuition:
These artifacts answer what is being studied and how it should be studied before any experiment-specific contract is written.

## MARS-DEF-009 Reference Library

Definition:
A reference library is the reusable inventory layer that preserves enough extracted content from authoritative sources to support later protocol design, analysis, and adjudication without re-discovery.

Intuition:
Inventory should work like a library of reusable knowledge, not a cache of tiny snippets.

## MARS-DEF-010 Research Artifact Taxonomy

Definition:
The research artifact taxonomy is the canonical typed vocabulary for modeling research and paper artifacts such as claims, hypotheses, methodology artifacts, references, experiments, run data, analysis results, evidence status, and paper sections.

Intuition:
It is the research-side equivalent of a concept taxonomy: a stable set of node types for the evidence graph.

## MARS-DEF-011 Typed Research Relationships

Definition:
Typed research relationships are the canonical edge verbs used to connect research-artifact nodes, including `frames`, `anchors`, `cites`, `operationalizes`, `tests`, `measures`, `produces`, `analyzes`, `updates`, and `synthesizes`.

Intuition:
These edges make the paper and evidence graph explicit instead of leaving methodology, references, experiments, and synthesis only in prose.

## MARS-DEF-012 Inventory Library Entry

Definition:
An inventory library entry is the per-source extracted-content artifact at `inventory/library/<source-id>.md` that preserves reusable knowledge, provenance notes, raw-content linkage, and experiment relevance for one source.

Intuition:
This is the actual library book, not just the library catalog card.

## MARS-DEF-013 Raw Content Artifact

Definition:
A raw content artifact is the retrieved or user-provided source material stored under `inventory/raw/<source-id>/` and used as the provenance base for inventory extraction.

Intuition:
This is the closest preserved form of what the source actually said when inventory claims are extracted from it.
