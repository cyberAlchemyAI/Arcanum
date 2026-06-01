# POC Candidate Selection: Inventory Evidence-Card

## Purpose

Select high-value repository sections for the evidence-card POC.

The goal is not broad coverage. The goal is a source slice dense enough to test:

- whether evidence-cards stay compact;
- whether selectors are reviewable;
- whether retrieval can return a useful EvidenceSet;
- whether handoff candidates preserve authority boundaries;
- whether the model exposes residue instead of hiding it.

## Selection Criteria

| Criterion | Meaning |
| --- | --- |
| Card density | Section can produce multiple reusable cards without whole-repo ingest. |
| Boundary pressure | Section stresses Inventory vs Ontology vs Context Builder ownership. |
| Retrieval value | Section can help answer a concrete task query. |
| Handoff value | Section can feed Ontology Vault or Definitions Governance without promotion. |
| Residue value | Section contains ambiguity, gap, or tension worth preserving. |

## Recommended Pilot Slice

Use these five sections first.

| Rank | Source Section | Lines | Why It Is High Value | Likely Cards | EvidenceSet Role |
| --- | --- | --- | --- | --- | --- |
| 1 | `../cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` — Purpose and Corrected Layering | 16-44 | Cleanly states the raw source -> inventory -> ontology -> context-builder authority split. | source-summary, concept, claim, method | Core set anchor for "inventory-to-ontology pipeline". |
| 2 | `../cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` — Source Corpus through Edge Vocabulary | 104-168 | Dense taxonomy of cohorts, entry types, ontology branches, and edge validation rules. | concept, method, relation-candidate, question | Tests whether card groups need an EvidenceSet to preserve relationships. |
| 3 | `../cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` — Phase 2 through Phase 5 | 194-271 | Gives concrete ingest, typed entry, ontology creation, and context-builder proof gates. | method, claim, question, operational-lesson | Main retrieval set for "prepare context to design Operational Ontology schema". |
| 4 | `../cyberAlchemy/agentic-system-ontology-entry-model.md` — Core Rule and Layer Responsibilities | 15-55 | Sharp boundary between inventory evidence, thick ontology entries, and task context. | concept, claim, contradiction-candidate | Handoff safety test for candidate vs promoted language. |
| 5 | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` — Core Idea, Authority Ladder, Inventory UX Loop | 3-90 | Provides an authority ladder and user-facing retrieval loop with task-shaped context requirements. | concept, method, claim, question | Cross-source EvidenceSet candidate for "authority ladder and retrieval UX". |

## Strong Alternates

Use these if the recommended slice is too homogeneous or if the POC needs more pressure.

| Priority | Source Section | Lines | Use When | Likely Cards |
| --- | --- | --- | --- | --- |
| A | `../cyberAlchemy/agentic-system-knowledge-map.md` — Knowledge Tower | 26-51 | Need a compact authority-ladder source independent of Necronomicon. | concept, claim |
| A | `../cyberAlchemy/agentic-system-knowledge-map.md` — Operational Ontology Gap and Memory Model Seeds | 77-106 | Need more evidence for operational ontology and memory promotion boundaries. | question, concept, claim |
| B | `../cyberAlchemy/agentic-system-architecture.md` — Foundational Principles | 10-33 | Need principles that stress residue, candidate-before-canon, and evidence/commitment split. | concept, claim |
| B | `../cyberAlchemy/agentic-system-architecture.md` — Operational Ontology Model | 302-373 | Need richer node/edge/confidence vocabulary for handoff tests. | concept, relation-candidate, question |
| B | `../cyberAlchemy/agentic-system-ontology-entry-model.md` — Retrieval Rule and Promotion Rule | 264-278 | Need a tight retrieval/handoff comparison source. | method, claim |
| C | `framework/CYBERALCHEMY-METHOD.md` — Governing and Synthesis Primitives | 141-270 | Need meta-method evidence for smallest coherent unit and trace-before-promotion. | method, concept, operational-lesson |
| C | `extraction-research/inventory.md` and `extraction-research/ontology-vault.md` — Reusable Core and Neutral Rewrite Strategy | 1-75 | Need compact neutralized versions of Inventory and Ontology Vault responsibilities. | source-summary, concept, claim |

## Craft Candidates

Craft is high value for the EvidenceSet question because it contains nested contexts, owned artifacts, blockers, enablers, gates, residue, and recomposition. It should not replace the recommended first slice, but it is the best stressor for deciding whether grouped evidence deserves a first-class intermediate artifact.

| Priority | Source Section | Lines | Use When | Likely Cards |
| --- | --- | --- | --- | --- |
| A | `development/craft/CRAFT-RECURSIVE-LEDGER-DEFINE.md` — Objective through MVP Definition | 17-68 | Need a real example where one artifact has to coordinate many contexts and owned artifacts. | source-summary, concept, method, question |
| A | `development/craft/CRAFT-RECURSIVE-LEDGER-DEFINE.md` — Core Model and Candidate Ledger Shape | 106-209 | Need concrete field pressure for EvidenceSet: contexts, artifacts, relationships, gates, blockers, enablers, evidence. | concept, method, claim, relation-candidate |
| A | `development/craft/CRAFT-LEDGER-TYPE-SYSTEM.md` — Base Types through Operational Lanes | 41-122 | Need validation pressure around blockers, gates, enablers, authority gates, recomposition gates, and role lanes. | concept, method, question |
| B | `development/craft/CRAFT-INITIAL-DEFINITION.md` — Executive Definition and Conversation Synthesis | 8-40 | Need conceptual pressure around schema/data translation and residue. | concept, claim |
| B | `development/craft/CRAFT-INITIAL-DEFINITION.md` — SCU, Entropy, and Reflection Tower | 167-262 | Need evidence for smallest coherent unit, residue, and recomposition logic. | concept, method, operational-lesson |
| C | `development/craft/DURABLE-SESSION-CONTEXT.md` — Scope Boundary and Operating Rules | 9-83 | Need authority and promotion guardrails for candidate development material. | claim, method, question |
| C | `development/craft/SESSION-LEDGER.md` — Decision Ledger and Open Gaps | 26-74 | Need live candidate-development gaps that can test evidence-card and EvidenceSet maintenance behavior. | question, claim, operational-lesson |

## Candidate EvidenceSets

These are possible composed artifacts to test after cards exist.

| EvidenceSet Candidate | Source Sections | Purpose | Keep If |
| --- | --- | --- | --- |
| `evidence-set.inventory-to-ontology-boundary` | recommended ranks 1, 4, 5 | Explain the Inventory/Ontology/Context Builder boundary with source-backed cards. | It improves handoff safety and reduces repeated boundary explanation. |
| `evidence-set.operational-ontology-poc` | recommended ranks 2, 3 plus alternates A/B | Prepare context to design Operational Ontology schema. | It returns a compact set of cards with useful inclusions/exclusions. |
| `evidence-set.authority-ladder` | recommended rank 5 plus alternate A Knowledge Tower | Compare authority states across Necronomicon and CyberAlchemy knowledge map. | It reveals agreement/tension without turning into a synthesis essay. |
| `evidence-set.context-solution-card` | recommended rank 3 plus architecture Operational Ontology model | Test whether context-solution/card grouping should be an EvidenceSet or remain retrieval output. | The grouped result is reused by retrieval and handoff assembly. |
| `evidence-set.craft-recursive-ledger` | Craft candidate A sections | Test whether EvidenceSet can represent a composed context around nested artifacts, gates, blockers, enablers, and recomposition. | It explains cross-context relations better than independent cards without becoming a full ledger. |
| `evidence-set.scu-residue-recomposition` | Craft initial definition B sections plus CyberAlchemy Method primitives | Test whether evidence-cards can preserve SCU/residue/recomposition reasoning as reusable method evidence. | It improves card grouping for method validation and does not duplicate Craft's own method artifacts. |

## Rejected For First POC

| Source | Reason |
| --- | --- |
| Whole `../cyberAlchemy/` folder | Violates source-slice gate and would hide card granularity problems. |
| Full `.arcanum/observability/` logs | Too noisy for first POC; useful later for operational lessons. |
| Broad `spells/invoke/development/` fixtures | Rich but too implementation-plan-heavy for initial knowledge-shape validation. |
| Full `development/craft/` folder | High value but too large for the first slice; use selected Craft sections as EvidenceSet stressors. |
| External web research | Not needed for this local concept validation pass. |

## Recommended First Query

Use this task-shaped retrieval query for the pilot:

```text
Prepare context to decide whether Inventory needs an intermediate EvidenceSet artifact between evidence-cards and downstream handoff packets.
```

Expected useful output:

- selected cards explaining the Inventory/Ontology/Context Builder boundary;
- selected cards explaining task-shaped retrieval;
- selected cards explaining authority ladder and promotion rules;
- excluded matches that are too broad, too ontology-owned, or too implementation-specific;
- one candidate EvidenceSet with included and excluded cards.

## Selection Verdict

Start with the recommended five-section pilot slice.

This slice is high value because it exercises all six POC gates from `POC-VALIDATION.md` and creates a real opportunity to test the `EvidenceSet` candidate without over-ingesting the repository.

After the first five-section slice, add the two Craft A sections if the EvidenceSet question remains open. Craft is the best second-pass stressor because it tests whether an EvidenceSet can express grouped relationships among contexts and artifacts without becoming a separate ledger system.
