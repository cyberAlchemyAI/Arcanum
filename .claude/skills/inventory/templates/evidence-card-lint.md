# Evidence-Card Lint Contract

This contract defines the static checks required before evidence-cards can be used for POC retrieval, EvidenceSet evaluation, or downstream handoff examples.

## Required Checks

| Check | Severity | Expected finding |
| --- | --- | --- |
| Missing required field | error | The card omits a field required by `profile`. |
| Empty `source_refs` | error | Every card requires at least one source ref. |
| Unknown controlled vocabulary value | error | Unknown enum value; propose schema residue instead of silently accepting it. |
| `profile: full` without `handoff_targets` or `trace` | error | Full cards must preserve handoff intent and field-level trace. |
| `profile: minimal` without traceable source refs | error | Minimal cards are still source-backed and reviewable. |
| Terminal promotion status with `promotion_owner: none` | error | Terminal promotion state requires an explicit owner. |
| Relation candidate without `claim_shape.non_authority_notice` | error | Relation candidates must not imply downstream ontology authority. |
| Relation candidate without evidence refs or target resolution | error | Relation candidates require evidence refs and a target resolution. |
| Trace confidence described as ontology or commitment confidence | error | Trace confidence is extraction/rule confidence only. |
| Query selector that cannot be reproduced | warning or residue | Query selectors need reproducible text or declared residue. |

## Invalid Examples

### Owner/status mismatch

```yaml
promotion_status: promoted
promotion_owner: none
```

Expected finding: terminal promotion state requires an explicit owner.

### Missing selector

```yaml
source_refs: []
```

Expected finding: every card requires at least one source ref.

### Unknown enum

```yaml
card_type: ontology-node
```

Expected finding: unknown card type; propose schema residue instead.

### Relation candidate without notice

```yaml
card_type: relation-candidate
claim_shape:
  subject_ref: agentic.memory
  predicate_label: promotes_to
  object_ref: agentic.operational_ontology
```

Expected finding: relation candidates require evidence refs, target resolution, and non-authority notice.

### Minimal profile hiding missing evidence

```yaml
profile: minimal
selection_reason: ""
source_refs: []
```

Expected finding: minimal cards are still traceable and reasoned.

## POC Use

- Invalid examples should be kept as fixture seeds for validation strictness.
- A useful real card failing for a harmless reason should become schema residue rather than an immediate rejection.
- Lint findings must distinguish hard errors from warnings that can be carried as residue.
