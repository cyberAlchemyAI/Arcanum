# Validation Note: OVS-SWU-005

Status: flag

## Result

The CyberAlchemy PromotionRecord pressure fixture can be represented by the current branch-aware schema candidate as:

- `entry_type: PromotionRecord`
- `record_kind: promotion_record`
- `branch_context.primary: bridge`
- `claim_role: policy`
- `bridge_outcome: partial`

## Schema Gap

`record_kind` is useful for distinguishing:

- ontology entry,
- promotion record,
- evidence input,
- bridge validation.

The schema candidate mentions this pressure in prose, but `record_kind` is not yet a governed field in the minimal shape. The fixture therefore passes as a permissive candidate entry, but the result is `flag` for schema design follow-up.

## Boundary

The fixture was written under `schema-validation-plan/fixtures/valid/` instead of the CAOL package's recommended fixture path because the CAOL package README lists package mutation as out of scope.
