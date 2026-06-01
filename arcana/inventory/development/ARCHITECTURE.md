---
module: inventory-evidence-card
version: current
status: draft
updatedAt: 2026-05-26
docType: architecture-bundle
---

# Architecture Bundle: Inventory Evidence-Card

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `../../../spells/invoke/design.md`
- Outputs: `ARCHITECTURE.md`, `TEMPLATE-MANIFEST.md`, `GLOSSARY-CONSISTENCY.md`, `DESIGN-TRANSPORT.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: Module Formulae architecture profile plus Inventory evidence-card templates
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: n/a for design mode; executable work-pack provided by plan mode
- Decisions: one canonical `evidence-card`; optional shapes are profiles; downstream packets are projections
- Unresolved gaps: executable validator and command integration deferred
- Next route: plan/task-session

## Design Intent

Inventory gains an evidence-card layer that captures source-backed reusable knowledge as one canonical unit. The architecture preserves raw-source authority, keeps ontology and definition governance downstream, and gives Context Builder/Invoke task-shaped retrieval instead of full wiki dumps.

## Inputs

- `SPEC.md`
- `GLOSSARY.md`
- `CONCEPT-MODEL.md`
- source evidence summarized in `work-pack/shared/SOURCE-CONTRACTS.md`

## 1. Context View

```mermaid
graph TD
    Raw[Raw repository sources] --> Inventory[Inventory evidence-card layer]
    Inventory --> Indexes[Generated indexes]
    Inventory --> Retrieval[Task-shaped retrieval]
    Retrieval --> ContextBuilder[Context Builder]
    Retrieval --> Invoke[Invoke]
    Retrieval --> Harness[Repository Harness]
    Inventory --> Handoffs[Candidate handoff packets]
    Handoffs --> Ontology[Ontology Vault]
    Handoffs --> Definitions[Definitions Governance]
```

Rules:

- Raw sources remain authority.
- Inventory owns cards, selectors, indexes, lint findings, and handoff projections.
- Ontology Vault owns governed meaning, relations, confidence, branches, and promotion.
- Definitions Governance owns canonical definitions and glossary synchronization.

## 2. High-Level Structure View

```mermaid
graph TD
    Select[Source selection] --> Capture[Card capture]
    Capture --> SharedValidation[Shared schema validation]
    SharedValidation --> ProfileValidation[card_type profile validation]
    ProfileValidation --> Store[Card store]
    Store --> IndexBuild[Index build]
    IndexBuild --> Retrieval[Retrieval composer]
    Retrieval --> Packet[Handoff packet builder]
    ProfileValidation --> Lint[Lint and residue]
```

## 3. Low-Level Components View

| Component | Purpose | Contract |
| --- | --- | --- |
| Evidence-card schema | Shared record shape. | `CONCEPT-MODEL.md`, `templates/evidence-card-schema.md` |
| Authoring template | Human/agent fillable card. | `templates/evidence-card.md` |
| Validation profiles | Required and type-specific checks. | `templates/evidence-card-lint.md` |
| Index families | Lookup by id, source, tag, type, authority, promotion, handoff, cohort, related, residue, trace. | `templates/evidence-card-index.md` |
| Retrieval composer | Compact task-shaped output. | `FLOWS-POLICIES.md` |
| Handoff builders | Downstream candidate packets. | `INTERFACES.md` |

## 4. Workflow Process View

```mermaid
graph TD
    W1[Select bounded source scope] --> W2[Extract reusable evidence]
    W2 --> W3[Draft evidence-card]
    W3 --> W4[Validate schema and vocabularies]
    W4 --> W5[Validate profile and authority rules]
    W5 --> W6{Valid?}
    W6 -->|yes| W7[Persist card and update indexes]
    W6 -->|no| W8[Record lint finding or residue]
    W7 --> W9[Compose retrieval or handoff]
```

## 5. Decision Flow View

```mermaid
graph TD
    D1[Selected evidence] --> D2{Source-first bounded section?}
    D2 -->|yes| D3[source-summary]
    D2 -->|no| D4{Reusable concept?}
    D4 -->|yes| D5[concept]
    D4 -->|no| D6{Repeatable method?}
    D6 -->|yes| D7[method]
    D6 -->|no| D8{Reviewable assertion?}
    D8 -->|yes| D9{Relation-shaped handoff needed?}
    D9 -->|yes| D10[relation-candidate]
    D9 -->|no| D11[claim]
    D8 -->|no| D12{Unresolved ambiguity?}
    D12 -->|yes| D13[question]
    D12 -->|no| D14[residue or reject]
```

## 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Evidence-card template | Inventory development | Inventory maintainers | Source-backed fillable card. |
| Lookup output | Inventory | Context Builder, Invoke | Selected cards, selectors, authority levels, gaps, excluded matches. |
| Ontology packet | Inventory | Ontology Vault | Candidate claim/relation/contradiction/lesson cards with non-authority notice. |
| Definitions packet | Inventory | Definitions Governance | Candidate term evidence without canonical status. |
| Pilot fixtures | Inventory development | Future validators | Bounded JSON examples for card, index, retrieval, and handoff checks. |

## Design Decisions

| ID | Decision | Rationale |
| --- | --- | --- |
| D1 | Keep one canonical `evidence-card` schema. | Avoids taxonomy sprawl and preserves Distill output. |
| D2 | Use `card_type` profiles. | Allows specific validation without separate storage families. |
| D3 | Add `profile`, `captured`, `trace`, and `residue`. | Supports migration, provenance, auditability, and honest gaps. |
| D4 | Treat handoff packets as read models. | Prevents Inventory from claiming downstream authority. |
| D5 | Pilot with shaped CyberAlchemy sources only. | Validates shape without whole-repo ingest. |

## Open Risks

| Risk ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R1 | Evidence-card becomes too generic. | medium | Enforce required fields, profiles, and lint rules. |
| R2 | Promotion metadata creates authority confusion. | high | Validate owner/status pairs and require non-authority notices. |
| R3 | Minimal profile becomes a dumping ground. | medium | Require source refs, selection reason, captured metadata, and residue for missing detail. |
| R4 | Trace confidence is mistaken for ontology confidence. | high | State extraction/rule confidence only in schema and docs. |
