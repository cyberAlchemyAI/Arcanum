# Refine Result: Record Kind Schema Gap

Status: pass
Preset: compact
Research: no-research

## Recommendation

Add `record_kind` to the branch-aware ontology schema candidate before JSON Schema generation.

Use it as a minimal top-level record-family discriminator:

```yaml
record_kind: ontology_entry | promotion_record | evidence_input | bridge_validation
```

Recommended default:

```yaml
record_kind: ontology_entry
```

## Why

The validation suite proves that the four schema axes are useful:

- `lifecycle_status`
- `claim_role`
- `governance_outcome`
- `bridge_outcome`

But the CyberAlchemy PromotionRecord pressure fixture exposed a different distinction. `PromotionRecord` is not merely a lifecycle status, claim role, governance outcome, or bridge outcome. It is a different kind of record: a governed change/promotion object about one primary claim.

Without `record_kind`, the schema can only represent PromotionRecord by overloading `entry_type`, `claim_role`, or `branch_context.local_role`. That recreates the same ambiguity the schema-axis split just repaired.

## Rejected Alternatives

| Alternative | Verdict | Reason |
| --- | --- | --- |
| Keep `record_kind` fixture-local | rejected | It preserves the immediate tests but leaves JSON Schema generation likely to freeze a known gap. |
| Split companion schemas now | deferred | Likely correct later, but too much structure before examples prove which companion records need their own schema. |
| Use `entry_type` only | rejected | `entry_type` names the domain/class label; it should not carry schema family semantics. |
| Use `claim_role` only | rejected | `PromotionRecord` is not just what the claim is doing; it changes the record's governance shape. |

## Minimal Schema Delta

Add `record_kind` near `entry_type` in the minimal shape:

```yaml
entry_type: string
record_kind: ontology_entry | promotion_record | evidence_input | bridge_validation
lifecycle_status: raw | catalogedEvidence | reviewableSignal | promotionRecordDraft | candidate | premise | reviewed | promoted | contradicted | retired | rejected | deferred
```

Add `record_kind` to required fields.

Add a validation rule:

```text
V12: Record Kind

record_kind must be one of ontology_entry, promotion_record, evidence_input, bridge_validation.

Promotion records:
- should carry one primary claim,
- should cite source/evidence pointers,
- should preserve evidence and commitment confidence,
- should name review owner, gate, contradiction path, and rollback/retirement path,
- should not replace ontology entries.
```

## JSON Schema Boundary

JSON Schema generation remains blocked until:

1. `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` includes `record_kind`,
2. `tests/validate_branch_schema.py` validates `record_kind`,
3. fixture defaults are updated so every valid entry declares a `record_kind`,
4. the validation suite passes again.

## Next Route

Recommended next route:

```text
task-session: patch candidate schema and validator for record_kind
```

Suggested first SWU:

```text
Add record_kind to schema candidate, fixtures, and validator; rerun fixture validation.
```

Do not generate JSON Schema yet.
