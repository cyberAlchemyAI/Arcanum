# Refine Seed Proposal: Record Kind Schema Gap

Status: exploratory, non-canonical
Run id: `20260529T104000Z-record-kind-decision`
Preset: compact
Research: no-research

## Target

`arcana/ontology-vault/development/schema-validation-plan/VALIDATION-REPORT.md`

Primary decision gap:

Should `record_kind` enter `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` before JSON Schema generation?

## Source Context

- `VALIDATION-REPORT.md` reports a `flag`: the CyberAlchemy PromotionRecord pressure fixture uses `record_kind: promotion_record`, but the minimal schema does not govern `record_kind`.
- `fixtures/valid/cyberalchemy-caol-promotion-record.json` is the pressure evidence.
- `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` already separates `lifecycle_status`, `claim_role`, `governance_outcome`, and `bridge_outcome`.
- CAOL material suggests PromotionRecord should record governed change to one claim and should not replace ontology entries.

## Candidate Options

| Option | Meaning | Risk |
| --- | --- | --- |
| Add `record_kind` now | Minimal schema gains a top-level record-family discriminator. | Could over-generalize before examples beyond PromotionRecord exist. |
| Keep `record_kind` fixture-local | PromotionRecord fixture remains pressure evidence only. | JSON Schema generation may freeze a schema that cannot express companion records. |
| Split companion schemas now | Create separate entry, promotion-record, evidence-input, bridge-validation schemas. | Too much structure before validation evidence. |

## Write Scope

This refinement may write only inside this refinement run folder.

It does not mutate:

- `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`,
- schema fixtures,
- Inventory,
- structured-action-schema,
- canonical Ontology Vault templates.

## Done Criteria

- Produce a clear recommendation for `record_kind`.
- Preserve exploratory/non-canonical posture.
- Name the schema mutation, if any, as a next route rather than performing it.
- Keep JSON Schema generation blocked or unblocked explicitly.

## Research Decision

`no-research`: local validation evidence and CAOL package evidence are sufficient.
