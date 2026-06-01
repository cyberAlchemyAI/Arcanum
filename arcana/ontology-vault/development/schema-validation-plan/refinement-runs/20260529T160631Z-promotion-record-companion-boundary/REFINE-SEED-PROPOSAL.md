# Refine Seed Proposal: PromotionRecord Companion Boundary And Model Gap Sweep

Status: seed
Preset: standard
Research: no-research
Date: 2026-05-29

## Target

`arcana/ontology-vault/development/schema-validation-plan/`

## Operator Intent

Refine PromotionRecord companion boundaries before the first development-only JSON Schema candidate. Also inspect adjacent model gaps so the next schema step does not immediately discover another missing discriminator or companion model.

## Current Baseline

The fixture-driven candidate validation surface is passing:

- `record_kind` is present in the schema candidate.
- `record_kind` is represented in valid fixtures.
- invalid fixtures cover `record_kind: candidate`.
- validator rule `V12` enforces record-kind enum membership and PromotionRecord boundary checks.

## Core Refinement Question

Should `promotion_record` remain as one `record_kind` inside the main ontology-entry schema for the first JSON Schema candidate, or should it become a companion schema/template boundary before JSON Schema generation?

## Adjacent Gap Questions

- Does `evidence_input` need a companion schema before the first JSON Schema candidate?
- Does `bridge_validation` need a companion schema before the first JSON Schema candidate?
- Are `entry_type`, `record_kind`, `claim_role`, `lifecycle_status`, `governance_outcome`, and `bridge_outcome` now sufficiently separated?
- Is `PromotionRecord` a schema shape, a workflow artifact, a governance receipt, or all three at different layers?
- What should stay in the common ontology entry schema versus move into record-kind-specific companion schemas?
- Which gaps should block JSON Schema generation, and which should remain explicitly deferred?

## Write Scope

Allowed:

- create this refinement run folder;
- create run manifest, evidence index, dispatch route, runtime handoff, stage artifacts, and result;
- update no canonical schema in this refinement unless a later task-session is approved.

Out of scope:

- mutating Inventory;
- mutating structured-action-schema;
- mutating canonical Ontology Vault templates;
- generating JSON Schema;
- changing fixtures or validator;
- promoting branch labels, record kinds, or schema fields.

## Done Criteria

- The run names the recommended PromotionRecord boundary.
- The run names other model gaps likely to matter before JSON Schema generation.
- The run distinguishes blockers from deferrable companion-model work.
- The run recommends the next route without executing it.

## Validation Surface

```bash
python3 -m json.tool arcana/ontology-vault/development/schema-validation-plan/refinement-runs/20260529T160631Z-promotion-record-companion-boundary/REFINE-DISPATCH.json
python3 -m json.tool arcana/ontology-vault/development/schema-validation-plan/refinement-runs/20260529T160631Z-promotion-record-companion-boundary/evidence-index.json
python3 - <<'PY'
import jsonschema, yaml, json
from pathlib import Path
schema = json.loads(Path('formulae/dispatch-spec/dispatch.schema.json').read_text())
doc = json.loads(Path('arcana/ontology-vault/development/schema-validation-plan/refinement-runs/20260529T160631Z-promotion-record-companion-boundary/REFINE-DISPATCH.json').read_text())
jsonschema.validate(doc, schema)
PY
```

## Research Decision

No external research. The issue is internal model ownership and schema boundary design. Local evidence is sufficient for this refinement.
