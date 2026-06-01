# Evidence-Card Lint Contract

## Required Checks

| Check | Finding |
| --- | --- |
| Missing required field | error |
| Empty `source_refs` | error |
| Unknown controlled vocabulary value | error or schema residue |
| `profile: full` without `handoff_targets` or `trace` | error |
| `profile: minimal` without traceable source refs | error |
| Terminal promotion status with `promotion_owner: none` | error |
| Relation candidate without `claim_shape.non_authority_notice` | error |
| Trace confidence described as ontology or commitment confidence | error |
| Query selector that cannot be reproduced | warning or residue |

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
