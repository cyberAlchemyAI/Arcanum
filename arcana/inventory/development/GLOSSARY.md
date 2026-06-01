---
module: inventory-evidence-card
version: current
status: draft
updatedAt: 2026-05-26
docType: glossary-ontology
---

# Glossary And Ontology: Inventory Evidence-Card

## Invoke Result

- Mode: define companion
- Spell: invoke
- Phase status: pass
- Link policy: candidate terms only; no Definitions Governance promotion

## Plain Language Terms

| Term | Meaning In This Module | Related Concepts |
| --- | --- | --- |
| Evidence-card | A source-backed Inventory record used for reusable lookup and downstream handoff. | EvidenceCard |
| Selector | A retrievable pointer to a source file, heading, line span, anchor, query, or fragment. | SourceRef |
| Trace | A field-level note explaining how a card value was assigned. | TraceEntry |
| Residue | A preserved schema or instance tension that should not be hidden. | Residue |
| Handoff packet | A read model sent to another owner for review. | HandoffPacket |

## Formal Terms

| Term | Category | Definition | Source Or Rationale | Linked Authority Concepts | Link Status | No Match Reason | Usage References | Status | Created At | Updated At |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| evidence-card | system | One canonical source-backed Inventory record for retrieval, linting, and downstream handoff. | Distilled Inventory design | inventory.EvidenceCard | linked |  | `CONCEPT-MODEL.md`, `ARCHITECTURE.md` | candidate | 2026-05-26 | 2026-05-26 |
| schema_version | system | Version marker for the evidence-card contract used by a card. | Repaired design migration need | inventory.EvidenceCard.schema_version | linked |  | `CONCEPT-MODEL.md` | candidate | 2026-05-26 | 2026-05-26 |
| profile | system | Completeness tier for a card, either `full` or `minimal`. | Minimal profile honesty rule | inventory.EvidenceCardProfile | linked |  | `CONCEPT-MODEL.md` | candidate | 2026-05-26 | 2026-05-26 |
| source_refs | system | Non-empty evidence references for a card. | Inventory authority rule | inventory.SourceRef | linked |  | `CONCEPT-MODEL.md`, `OPERATIONS.md` | candidate | 2026-05-26 | 2026-05-26 |
| authority_level | shared | The authority layer represented by a card, not a promotion grant. | Inventory/Ontology boundary | inventory.AuthorityLevel | linked |  | `CONCEPT-MODEL.md`, `FLOWS-POLICIES.md` | candidate | 2026-05-26 | 2026-05-26 |
| promotion_owner | shared | The owner responsible for promotion state decisions or downstream status. | Owner/status validation | inventory.PromotionOwner | linked |  | `CONCEPT-MODEL.md` | candidate | 2026-05-26 | 2026-05-26 |
| governed_ref | shared | Link to a downstream governed artifact when one exists. | Downstream boundary | inventory.EvidenceCard.governed_ref | linked |  | `INTERFACES.md` | candidate | 2026-05-26 | 2026-05-26 |
| non_authority_notice | system | Notice that Inventory has not promoted a candidate claim or relation. | Handoff safety rule | inventory.ClaimShape.non_authority_notice | linked |  | `INTERFACES.md` | candidate | 2026-05-26 | 2026-05-26 |

## Maintenance Rules

- Candidate terms stay candidate until Definitions Governance reviews them.
- Ontology confidence and commitment confidence are out of scope for Inventory cards.
- Trace confidence is extraction or rule confidence only.
