# Glossary Candidates: Inventory Evidence-Card

## Purpose

Record candidate terms surfaced by the evidence-card POC. These are not canonical definitions until Definitions Governance accepts or rewrites them.

## Candidate Terms

| Term | Candidate Definition | Evidence | Status | Promotion Owner |
| --- | --- | --- | --- | --- |
| evidence-card | A source-backed Inventory record with `schema_version`, `source_refs`, captured metadata, authority state, optional `trace`, optional `residue`, and promotion metadata such as `promotion_owner`. | `arcana/inventory/templates/evidence-card-schema.md` | candidate | definitions-governance |
| SourceRef | A selector-level pointer to reviewable evidence, including path, selector, selector type, and optional line or fragment fields. | `arcana/inventory/templates/evidence-card-schema.md` | candidate | definitions-governance |
| trace | Field-level extraction or assignment evidence that explains how an evidence-card value was copied, inferred, assigned, rejected, or deferred. | `arcana/inventory/templates/evidence-card-schema.md` | candidate | definitions-governance |
| residue | Preserved schema or instance ambiguity that should remain visible instead of being hidden by a forced card shape. | `arcana/inventory/templates/evidence-card-schema.md` | candidate | definitions-governance |
| promotion_owner | The owner responsible for terminal promotion decisions such as promoted, rejected, superseded, or blocked. | `arcana/inventory/templates/evidence-card-schema.md` | candidate | definitions-governance |
| governed_ref | A downstream governed artifact reference populated only after the responsible owner creates or accepts the governed artifact. | `arcana/inventory/templates/evidence-card-schema.md` | candidate | definitions-governance |
| EvidenceSet | A possible task-scoped composition of evidence-cards with inclusion reasons, excluded matches, index terms, synthesis note, residue, and handoff target. | `arcana/inventory/development/POC-VALIDATION.md`; `arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json` | candidate | inventory |
| task-shaped retrieval | Retrieval that returns selected cards, source selectors, excluded matches, trace notes, gaps, and next-route context for a concrete task. | `arcana/inventory/templates/index.md`; `arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json` | candidate | definitions-governance |
| non-authority handoff | A downstream packet that presents candidate evidence with source refs and explicit language that Inventory has not promoted ontology relations or canonical definitions. | `arcana/inventory/development/pilot/evidence-card/pilot-handoff-ontology.json`; `arcana/inventory/development/pilot/evidence-card/pilot-handoff-definitions.json` | candidate | definitions-governance |

## Candidate Governance Notes

- `EvidenceSet` remains an Inventory candidate until repeated retrieval or handoff reuse proves it should become a first-class artifact.
- `governed_ref` must stay empty until a downstream owner creates an accepted governed artifact.
- `promotion_owner` should not be used to imply promotion when `promotion_status` is only captured, candidate, or proposed.
- Definitions Governance owns canonical wording for shared terms; Ontology Vault owns governed meanings and relations.
