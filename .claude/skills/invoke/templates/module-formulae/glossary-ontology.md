---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: glossary-ontology
---

# Glossary And Ontology: {Module Name}

This glossary is the terminology authority for all generated artifacts.

Scope note: write plain-language terms first, then formal terms with source references.

## Plain Language Terms

Use this section for words that readers need before formal concept rows make sense.

| Term | Meaning In This Module | Related Concepts |
| --- | --- | --- |
| {PlainTerm} | {plain-language meaning and why it matters} | {concept names} |

## Formal Terms

| Term | Category | Definition | Source Or Rationale | Linked Authority Concepts | Link Status | No Match Reason | Usage References | Status | Created At | Updated At |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {TermName} | business | {one clear sentence} | {source summary} | {concept ids or names} | linked | {optional} | {spec/design/execution sections} | candidate | {iso-date} | {iso-date} |
| {TermName} | system | {one clear sentence} | {source summary} | {concept ids or names} | partial | {optional} | {spec/design/execution sections} | canonical | {iso-date} | {iso-date} |

Allowed category values: business, system, shared.

Allowed link status values: linked, partial, no-match.

## Deterministic Linking Order

1. Try to match an already-authorized concept first.
2. If a match exists, reuse that concept language.
3. If no match exists, create a candidate term and record the no-match reason.

## External Terms

| Term | Source Scope | Definition In This Module | Source Reference |
| --- | --- | --- | --- |
| {ExternalTerm} | {external module or standard} | {how this module uses the term} | {path or uri} |

## Maintenance Rules

- Treat this document as the single terminology source for generated artifacts.
- Keep every formal term linked to a source or rationale.
- Keep category and link status values deterministic.
- Update usage references whenever contract sections change.
- Do not define new behavior here; define behavior in source contracts and sync this glossary.
