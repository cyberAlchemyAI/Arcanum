---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: glossary
---

# Glossary: Inventory Interface, Linking, And Indexing

| Term | Meaning | Notes |
| --- | --- | --- |
| auto mode | Default `$inventory` behavior when no technical mode is supplied. | Infers target and asks for confirmation. |
| target inference | Process that resolves what the user likely wants inventorized or looked up. | Must record confidence and residue. |
| confirmation proposal | Human-readable mutation preview. | Required before write actions. |
| bounded slice | Small source-backed inventorization unit. | Avoids whole-folder dumps. |
| source anchor | Source path plus optional selector used to seed a slice. | Read-only input. |
| selector | Heading, line span, or stable anchor into a source file. | Used by selector index. |
| selector index | JSON map from source selectors to cards or records. | Machine lookup. |
| link index | JSON list of typed Inventory read-model links. | Not ontology authority. |
| backlink index | Generated reverse lookup from link index. | Do not hand-edit. |
| traceability matrix | JSON rows connecting obligations, sources, artifacts, and validation. | Adapted from DomainSpec discipline. |
| gap/risk queue | JSON list of unresolved residue, blockers, and next owners. | Keeps gaps operational. |
| projection index | JSON registry of read-only projections such as HTML or SQLite. | Projection is not source authority. |
| Markdown record | Human-facing generated explanation or coverage artifact. | Complements JSON. |
| JSON index | Machine-facing source of lookup truth. | Should parse and validate. |
| non-authority notice | Required language when Inventory link/card could be mistaken for downstream promotion. | Protects Ontology/Definitions boundaries. |
