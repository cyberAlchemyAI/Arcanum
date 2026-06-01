# Actions And Read Views: Inventory Evidence-Card

## Invoke Result

- Mode: design companion
- Spell: invoke
- Phase status: pass

## Action: CaptureEvidenceCard

Type: Action (state-changing)

Initiator: agent, human, or tool

Trigger: shaped source selection identifies reusable source-backed knowledge.

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| source_refs | SourceRef[] | yes | Source selectors. |
| card_type | CardType | yes | Intended profile. |
| summary | string | yes | Source-backed summary or assertion. |
| selection_reason | string | yes | Task, cohort, obligation, or lookup reason. |

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| EC-R1 | Source refs are mandatory. | `len(source_refs) > 0` |
| EC-R2 | Unknown controlled vocabulary values are invalid. | `value in enum` |
| EC-R3 | Minimal cards still require traceable source refs, authority level, selection reason, captured metadata, and updated date. | `profile == minimal -> required_core_fields` |
| EC-R4 | Trace confidence is not ontology or commitment confidence. | `trace.confidence describes extraction_or_rule_confidence` |

### State Update

Record: EvidenceCard

Transition: none -> captured

### Success Guarantees

- Card is traceable to source selectors.
- Card does not claim downstream promotion.

## Action: ValidateEvidenceCard

Type: Action (review or future validator)

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| VAL-R1 | Required fields exist for every profile. | `required_fields subset card.keys` |
| VAL-R2 | Full profile includes `handoff_targets` and `trace`. | `profile == full -> handoff_targets && trace` |
| VAL-R3 | Owner/status pair is legal. | `promotion_status == captured -> owner can be none`; terminal states require owner not none. |
| VAL-R4 | Relation candidates include structured claim shape and non-authority notice. | `card_type == relation-candidate -> claim_shape.required_fields` |
| VAL-R5 | Governed refs are used only for real downstream artifacts. | `governed_ref != inferred_from_text_similarity` |

### Failure Outcomes

| Condition | Result |
| --- | --- |
| Missing source refs | validation error |
| Unknown enum | validation error or schema residue |
| Terminal promotion with owner none | validation error |
| Candidate relation without non-authority notice | validation error |
| Minimal profile used to hide missing traceability | validation error |

## Read View: EvidenceCardLookup

Consumer: context-builder, invoke, repository-harness, humans.

### Query Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| query | string | no | Text query. |
| tags | string[] | no | Tag filters. |
| card_type | CardType[] | no | Type filters. |
| source_path | string | no | Source path filter. |
| handoff_target | HandoffTarget | no | Downstream target filter. |

### Output

| Field | Type | Description |
| --- | --- | --- |
| selected_cards | EvidenceCard[] | Cards selected for task fit. |
| excluded_matches | object[] | Near matches with exclusion reasons. |
| unresolved_questions | string[] | Question cards or gaps. |
| trace_notes | string[] | Notes about extraction/rule decisions. |

## Read View: EvidenceCardLintReport

Consumer: inventory maintainers and future runtime validators.

Output includes validation findings, residue, stale selectors, authority-boundary risks, and recommended next owner.
