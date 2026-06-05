# Branch-Aware Ontology Schema Validation Report

Status: pass
Date: 2026-06-01
Scope: published candidate bundle validation surface plus PromotionRecord record-kind refresh

## Verdict

The schema validation pass is usable and passes deterministic fixture validation.

The earlier `record_kind` flag has been resolved for the candidate validation surface. `record_kind` is now documented in the schema candidate, present in fixtures, and enforced by validator rule `V12`.

This remains non-canonical as a full schema/template package. Passing validation means the candidate shape is coherent enough to publish as a governed candidate bundle; it does not promote Ontology Vault templates, Inventory fields, structured-action-schema fields, or external-system adoption obligations.

The PromotionRecord refresh promotes only the `promotion_record` record-kind semantics as canonical ontology governance. Companion templates, separate schemas, and external adoption remain gated.

## Commands

```bash
jq empty arcana/ontology-vault/development/schema-validation-plan/fixtures/valid/*.json arcana/ontology-vault/development/schema-validation-plan/fixtures/invalid/*.json
python3 arcana/ontology-vault/development/schema-validation-plan/tests/validate_branch_schema.py
python3 arcana/ontology-vault/development/schema-validation-plan/tests/validate_branch_json_schema.py
tools/validate-artifact-constitution.sh
```

## Fixture Coverage

| Fixture family | Count | Status |
| --- | ---: | --- |
| Valid branch/axis fixtures | 11 | pass |
| Invalid targeted fixtures | 8 | pass |
| CyberAlchemy pressure fixture | 1 | pass |
| DomainSpec pressure fixture | 1 | pass |
| Future-system placeholder fixture | 1 | pass |

## Rule Coverage

| Rule | Coverage |
| --- | --- |
| Required top-level fields | validator |
| Enum membership | validator |
| V1 branch value | validator |
| V2 local alias | validator |
| V3 operational context | invalid fixture + validator |
| V4 bridge evidence | invalid fixture + validator |
| V5 Inventory non-authority | invalid fixture + validator |
| V8 confidence split | invalid fixture + validator |
| V9 promotion boundary | positive fixture + validator |
| V11 role/lifecycle axis split | positive and invalid fixtures + validator |
| V12 record kind | positive and invalid fixtures + validator |
| V13 record kind profiles | positive and invalid fixtures + validator |
| Development JSON Schema | positive and invalid fixtures + JSON Schema validator |

## Passing Decisions

- JSON fixtures are sufficient for the first deterministic validation pass.
- `lifecycle_status`, `claim_role`, `governance_outcome`, and `bridge_outcome` work as separate axes.
- `claim_role: candidate` is correctly invalid.
- `record_kind` works as a separate record-family discriminator.
- `record_kind: candidate` is correctly invalid.
- CyberAlchemy PromotionRecord can be represented as `record_kind: promotion_record` without overloading lifecycle, role, governance outcome, or bridge outcome axes.
- `evidence_input` now has direct valid and invalid fixture coverage.
- Record-kind profiles are explicit enough for development validation.
- The first development-only JSON Schema candidate validates the fixture corpus.
- Inventory can appear as evidence only when non-authority is explicit.
- DomainSpec and future-system placeholders can be represented without mutating external systems.
- GoldenQuill provides a canonical applied reference showing that local domain candidates can project into PromotionRecord-compatible owner decisions.

## Schema Gaps

| Gap | Evidence | Severity | Recommended route |
| --- | --- | --- | --- |
| PromotionRecord may need a companion schema or template. | CAOL pressure fixture, record-kind refinement result, and GoldenQuill applied reference | non-blocking authoring gap | keep record-kind canonical; defer companion template/schema until fixtures prove separate ownership is useful |
| Full DomainSpec validation still requires a DomainSpec-owned package. | DomainSpec fixture uses `local_role: evidence-gap` | non-blocking | separate DomainSpec handoff |

## Fixture Gaps

| Gap | Reason |
| --- | --- |
| No real future-system source fixture yet. | Placeholder intentionally avoids pretending evidence exists. |
| No canonical template validation. | Templates must not mutate before a template-specific gate. |

## Boundary Check

No mutation was made to:

- Inventory,
- structured-action-schema,
- canonical Ontology Vault templates,
- canonical branch conventions,
- DomainSpec files,
- CyberAlchemy source ontology.

## Published Candidate Bundle

The validated surface is now indexed at:

```text
GOVERNED-CANDIDATE-BUNDLE.md
```

Publication status:

```text
published candidate
```

This status permits future ontology development sessions to cite the bundle as current candidate evidence. It does not make the JSON Schema final canonical truth or make record-kind profiles mandatory authoring templates.

PromotionRecord boundary:

```text
record_kind: promotion_record is canonical as the Ontology Vault governance decision shape.
```

This does not make the JSON Schema candidate final canonical truth and does not make record-kind profiles mandatory authoring templates.

## Next Route

Recommended next route:

```text
task-session: create GoldenQuill L0 PromotionRecord compatibility fixtures
```

Alternative next route:

```text
decision-gate OVS-GATE-003: decide DomainSpec handoff route
```

Do not mutate canonical templates, Inventory, structured-action-schema, DomainSpec, or CyberAlchemy during the next route.
