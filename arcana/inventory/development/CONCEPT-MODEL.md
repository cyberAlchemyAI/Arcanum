# Concept Model: Inventory Evidence-Card

## Invoke Result

- Mode: define/design companion
- Spell: invoke
- Phase status: pass

## Records

### EvidenceCard

One canonical source-backed Inventory record.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | string | yes | Stable ID, formatted as `inventory.card.<stable-slug>`. |
| schema_version | string | yes | Evidence-card schema version, initially `inventory.evidence-card.v0.2`. |
| profile | EvidenceCardProfile | yes | Completeness tier. |
| card_type | CardType | yes | Validation profile for the card. |
| title | string | yes | Human-readable title. |
| summary | string | yes | Source-backed summary or assertion. |
| source_refs | SourceRef[] | yes | Non-empty source references. |
| authority_level | AuthorityLevel | yes | Current authority layer represented by the card. |
| tags | string[] | yes | Stable lowercase tags. |
| selection_reason | string | yes | Why this evidence was selected. |
| captured | Captured | yes | Structured provenance. |
| promotion_status | PromotionStatus | yes | Promotion lifecycle state recorded by Inventory. |
| promotion_owner | PromotionOwner | yes | Owner for promotion decision or status. |
| updated_at | date | yes | Last material update date. |
| handoff_targets | HandoffTarget[] | full only | Downstream consumers for full cards. |
| trace | TraceEntry[] | full only | Field-level decision evidence. |
| governed_ref | string | no | Downstream governed artifact reference. |
| related_cards | string[] | no | Related evidence-card IDs. |
| claim_shape | ClaimShape | no | Structured claim/relation candidate payload. |
| residue | Residue | no | Preserved schema or instance tension. |
| open_questions | string[] | no | Related question card IDs. |

Lifecycle Reference: captured -> candidate/proposed -> promoted/rejected/superseded/blocked, with owner/status rules in `OPERATIONS.md`.

### HandoffPacket

Read model projected from cards for downstream review.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| packet_id | string | yes | Stable packet identifier. |
| target | HandoffTarget | yes | Downstream owner. |
| cards | EvidenceCard[] | yes | Selected source cards or card summaries. |
| non_authority_notice | string | yes | Explicit non-promotion notice. |
| source_refs | SourceRef[] | yes | Consolidated evidence references. |
| open_questions | string[] | no | Review questions for downstream owner. |

## Value Types

### SourceRef

| Field | Type | Constraint |
| --- | --- | --- |
| path | string | Must be retrievable. |
| selector | string | Must identify a reviewable scope. |
| selector_type | SelectorType | Closed vocabulary. |
| start_line | number | Optional; required for precise line-span selectors. |
| end_line | number | Optional; required for precise line-span selectors. |
| fragment_kind | FragmentKind | Optional; used with fragment selectors. |

Equality Rule: two source refs are equal when path, selector, selector_type, and line/fragment fields match.

### Captured

| Field | Type | Constraint |
| --- | --- | --- |
| by | CapturedBy | human, agent, or tool. |
| at | date | ISO date. |
| tool_or_command | string | Optional command/source. |
| source_stage | SourceStage | Closed vocabulary. |

### TraceEntry

| Field | Type | Constraint |
| --- | --- | --- |
| field | string | Field path assigned or reviewed. |
| rule | string | Rule used. |
| source_ref | string | Must refer to a card source ref or source selector. |
| confidence | number | 0 to 1; extraction/rule confidence only. |
| decision | TraceDecision | Closed vocabulary. |

### Residue

| Field | Type | Constraint |
| --- | --- | --- |
| type | ResidueType | schema, instance, both, or none. |
| status | ResidueStatus | open, proposed, deferred, scoped-out, declared, resolved. |
| surfaced_by | string | Optional source of residue. |
| note | string | Required unless type is none. |

## Enumerations

### EvidenceCardProfile

| Value | Description |
| --- | --- |
| full | Complete card with handoff targets and trace entries. |
| minimal | Honest triage card with required source refs, selection reason, captured metadata, and authority fields. |

### CardType

| Value | Description |
| --- | --- |
| source-summary | Bounded source or source-section summary. |
| concept | Reusable concept evidence. |
| method | Ordered method, workflow, or operating rule. |
| claim | One reviewable assertion. |
| question | Unresolved ambiguity and why it matters. |
| context | Persistent reusable context evidence. |
| relation-candidate | Candidate relation for downstream ontology review. |
| contradiction-candidate | Conflicting evidence or claim candidate. |
| operational-lesson | Source-backed workflow or agent-operation lesson. |

### AuthorityLevel

`raw-source`, `session-evidence`, `discovery-baseline`, `inventory-knowledge`, `ontology-candidate`, `downstream-governed-ref`

### PromotionStatus

`captured`, `candidate`, `proposed`, `promoted`, `rejected`, `superseded`, `blocked`

### PromotionOwner

`none`, `inventory`, `ontology-vault`, `definitions-governance`, `context-builder`, `invoke`, `repository-harness`, `other`

### SelectorType

`file`, `heading`, `line-span`, `anchor`, `query`, `fragment`

### HandoffTarget

`ontology-vault`, `definitions-governance`, `context-builder`, `invoke`, `repository-harness`
