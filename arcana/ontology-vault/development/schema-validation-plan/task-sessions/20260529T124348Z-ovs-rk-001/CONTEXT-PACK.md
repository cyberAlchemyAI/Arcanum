# Context Pack: OVS-RK-001 Record Kind Patch

Status: pass
Mode: lean
Task: `OVS-RK-001`
Date: 2026-05-29

## Task Contract

Patch `record_kind` into the branch-aware ontology schema candidate, fixtures, and deterministic validator.

Done criteria:

- candidate schema names `record_kind` near `entry_type`;
- `record_kind` allowed values are documented;
- `record_kind` is required;
- valid fixtures declare `record_kind`;
- invalid fixtures cover unsupported `record_kind`;
- validator enforces `record_kind`;
- validation suite passes.

## Controlling Sources

- `../../WORK-PACK.md`
- `../../VALIDATION-REPORT.md`
- `../../refinement-runs/20260529T104000Z-record-kind-decision/RESULT.md`
- `../../../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`
- `../../tests/validate_branch_schema.py`
- `../../fixtures/valid/index.json`
- `../../fixtures/invalid/index.json`

## Constraints

- Keep result exploratory and non-canonical.
- Do not mutate Inventory.
- Do not mutate structured-action-schema.
- Do not mutate canonical Ontology Vault templates.
- Do not generate JSON Schema in this task.
- Keep validator development-only.

## Decision Summary

Use `record_kind` as a top-level record-family discriminator:

```text
ontology_entry | promotion_record | evidence_input | bridge_validation
```

Use `ontology_entry` as the default for ordinary ontology-shaped entries. Use `promotion_record` for CyberAlchemy PromotionRecord pressure coverage. Use `bridge_validation` for records whose primary function is branch alignment, contradiction, or evidence-gap validation.

## Validation Surface

```bash
jq empty arcana/ontology-vault/development/schema-validation-plan/fixtures/valid/*.json arcana/ontology-vault/development/schema-validation-plan/fixtures/invalid/*.json arcana/ontology-vault/development/schema-validation-plan/refresh-report.json
python3 arcana/ontology-vault/development/schema-validation-plan/tests/validate_branch_schema.py
tools/validate-artifact-constitution.sh
```
