# Interfaces: Inventory Evidence-Card

## External Interface: Inventory Templates (Markdown/JSON)

### Template Outputs

| Output | Target Production Path | Purpose |
| --- | --- | --- |
| `templates/evidence-card-schema.md` | `arcana/inventory/templates/evidence-card-schema.md` | Human-readable schema contract. |
| `templates/evidence-card.md` | `arcana/inventory/templates/evidence-card.md` | Authoring template. |
| `templates/evidence-card-lint.md` | `arcana/inventory/templates/evidence-card-lint.md` | Static lint and validation contract. |
| `templates/evidence-card-index.md` | `arcana/inventory/templates/index.md` patch source | Index and retrieval output contract. |

## Internal Interface: Lookup Output

Consumers: Context Builder, Invoke, Repository Harness.

| Field | Maps To | Description |
| --- | --- | --- |
| query | retrieval request | Purpose and filters. |
| selected_cards | EvidenceCardLookup output | Cards selected for task fit. |
| excluded_matches | EvidenceCardLookup output | Near matches rejected with reasons. |
| unresolved_questions | EvidenceCardLookup output | Gaps and open questions. |
| trace_notes | TraceEntry summaries | Assignment or extraction caveats. |

## External Interface: Ontology Handoff Packet

Consumer: Ontology Vault.

| Field | Type | Maps To |
| --- | --- | --- |
| packet_id | string | HandoffPacket.packet_id |
| target | `ontology-vault` | HandoffPacket.target |
| non_authority_notice | string | Required boundary statement |
| candidate_cards | EvidenceCard[] | claim, relation-candidate, contradiction-candidate, operational-lesson |
| source_refs | SourceRef[] | Evidence references |
| requested_review | string[] | Ontology review prompts |

## External Interface: Definitions Handoff Packet

Consumer: Definitions Governance.

| Field | Type | Maps To |
| --- | --- | --- |
| packet_id | string | HandoffPacket.packet_id |
| target | `definitions-governance` | HandoffPacket.target |
| candidate_terms | object[] | Concept and claim evidence |
| non_authority_notice | string | Required boundary statement |
| source_refs | SourceRef[] | Evidence references |

## Data Mapping Notes

- Keep enum values identical between schema, lint contract, fixtures, and docs.
- Handoff packet IDs must not be confused with downstream governed IDs.
- `governed_ref` is populated only after downstream review creates a real artifact.
