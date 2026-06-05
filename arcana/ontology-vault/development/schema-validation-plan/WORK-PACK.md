# Work-Pack: Test-First Branch-Aware Ontology Schema Validation

Status: validated; published candidate bundle; PromotionRecord canonical record-kind
Mode: non-executed
Complexity: medium
Owner: Ontology Vault development

## Objective

Create the first validation tests for `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` so schema behavior is proven with fixtures before schema promotion, JSON Schema generation, or template mutation.

## Delivery Boundary

In scope:

- development-only fixture directory,
- deterministic validator or test helper,
- tests for positive and negative fixtures,
- validation report,
- gaps routed back to schema candidate.

Out of scope:

- mutating Inventory,
- mutating structured-action-schema,
- mutating canonical Ontology Vault templates,
- generating governed JSON Schema,
- promoting branch labels or schema fields.

## Source Contracts

- `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`
- `../invoke-runs/20260527T011500Z-schema-axis-design.md`
- `../general-ontology-lifecycle/refinement-runs/20260527T010000Z-role-lifecycle-redundancy/RESULT.md`
- `../cyberalchemy-ontology-lifecycle/ONTOLOGY-VAULT-BRIEF.md`
- `../cyberalchemy-ontology-lifecycle/WORK-PACK.md`

## Validation Strategy

Use local deterministic checks first:

```bash
jq empty <json artifacts>
tools/validate-artifact-constitution.sh
```

The future test command should be added by the implementation SWU. Candidate command shape:

```bash
python3 arcana/ontology-vault/development/schema-validation-plan/tests/validate_branch_schema.py
```

If Python dependencies become necessary, prefer standard-library YAML-adjacent parsing only when fixture format allows it. If YAML parsing is required, record the dependency decision before adding it.

## Task Board

| Task | Layer | Status | SWUs |
| --- | --- | --- | --- |
| OVS-TEST-001 Fixture Set | L0 | complete | OVS-SWU-001, OVS-SWU-002 |
| OVS-TEST-002 Deterministic Validator | L1 | complete | OVS-SWU-003, OVS-SWU-004 |
| OVS-TEST-003 Cross-System Fixtures | L2 | flag | OVS-SWU-005, OVS-SWU-006 |
| OVS-TEST-004 Validation Report | L3 | complete-with-flag | OVS-SWU-007 |

## Smallest Working Unit Manifest

| SWU | Parent task | Goal | Verification |
| --- | --- | --- | --- |
| OVS-SWU-001 | OVS-TEST-001 | Create positive fixtures for branch and axis coverage. | Fixture review confirms required valid cases exist. |
| OVS-SWU-002 | OVS-TEST-001 | Create negative fixtures for invalid schema states. | Fixture review confirms targeted failures exist. |
| OVS-SWU-003 | OVS-TEST-002 | Implement required-field and enum validation. | Validator fails missing/invalid required fields. |
| OVS-SWU-004 | OVS-TEST-002 | Implement cross-field rules. | Validator catches operational, bridge, confidence, promotion, and axis-split violations. |
| OVS-SWU-005 | OVS-TEST-003 | Add CyberAlchemy PromotionRecord pressure fixture. | CyberAlchemy fixture validates or produces named schema gap. |
| OVS-SWU-006 | OVS-TEST-003 | Add DomainSpec and future-system fixtures. | Non-Arcanum examples validate or produce named schema gaps. |
| OVS-SWU-007 | OVS-TEST-004 | Produce validation report and schema gap ledger. | Report states pass/flag/block and next route. |

## Task Details

### OVS-TEST-001 Fixture Set

Purpose: prove the schema can be represented before implementing a validator.

Implementation detail:

- create a development-only fixture root, likely `arcana/ontology-vault/development/schema-validation-plan/fixtures/`;
- use one fixture file per case;
- separate `valid/` and `invalid/` fixtures;
- include comments or sidecar expected-result metadata if YAML comments would complicate parsing;
- keep fixtures small enough to inspect manually.

Smallest Working Units:

- `OVS-SWU-001`
  - Dependencies: schema candidate axis design.
  - Write scope: fixture files only.
  - Done criteria: valid fixtures cover branch values and selected axes.
  - Acceptance evidence: fixture list plus manual review summary.
  - Execution owner: local-fallback.
  - Handoff note: start with the example entries already in the schema candidate.
- `OVS-SWU-002`
  - Dependencies: `OVS-SWU-001`.
  - Write scope: invalid fixture files only.
  - Done criteria: invalid fixtures cover overloaded `status`, `claim_role: candidate`, missing operational context, missing bridge evidence, missing non-authority notice, collapsed confidence.
  - Acceptance evidence: fixture list plus expected failure reason per fixture.
  - Execution owner: local-fallback.
  - Handoff note: each invalid fixture should target one rule.

### OVS-TEST-002 Deterministic Validator

Purpose: create the first local test runner for candidate schema behavior.

Implementation detail:

- parse fixtures with a conservative structured parser;
- fail fast on malformed fixture shape;
- report fixture id, rule id, expected outcome, actual outcome, and message;
- avoid turning the validator into canonical runtime API;
- keep rule IDs aligned with schema validation rules `V1` through `V11`.

Smallest Working Units:

- `OVS-SWU-003`
  - Dependencies: `OVS-SWU-001`, `OVS-SWU-002`.
  - Write scope: validator/test script and minimal documentation.
  - Done criteria: required-field and enum checks pass/fail as expected.
  - Acceptance evidence: command output showing expected fixture outcomes.
  - Execution owner: local-fallback.
  - Handoff note: use `python3`, not `python`, unless the environment proves otherwise.
- `OVS-SWU-004`
  - Dependencies: `OVS-SWU-003`.
  - Write scope: validator/test script and test fixtures if needed.
  - Done criteria: cross-field rules V3-V11 are covered by positive and negative cases.
  - Acceptance evidence: command output plus rule coverage list.
  - Execution owner: local-fallback.
  - Handoff note: prioritize role/lifecycle axis split and Inventory non-authority rules.

### OVS-TEST-003 Cross-System Fixtures

Purpose: pressure-test the schema beyond Arcanum examples.

Implementation detail:

- use CyberAlchemy PromotionRecord material as the first external pressure fixture;
- add a DomainSpec bridge scenario from existing handoff material;
- add one future-system placeholder with explicit limits;
- failures should become schema gaps, not forced data edits.

Smallest Working Units:

- `OVS-SWU-005`
  - Dependencies: `OVS-SWU-004`.
  - Write scope: CyberAlchemy fixture and validation note.
  - Done criteria: PromotionRecord fixture validates or names missing schema fields.
  - Acceptance evidence: validation output and gap note.
  - Execution owner: local-fallback.
  - Handoff note: use `../cyberalchemy-ontology-lifecycle/ONTOLOGY-VAULT-BRIEF.md`.
- `OVS-SWU-006`
  - Dependencies: `OVS-SWU-005`.
  - Write scope: DomainSpec/future-system fixtures and validation note.
  - Done criteria: non-Arcanum examples validate or expose classification gaps.
  - Acceptance evidence: validation output and gap note.
  - Execution owner: local-fallback.
  - Handoff note: preserve boundaries; do not mutate DomainSpec or structured-action-schema.

### OVS-TEST-004 Validation Report

Purpose: decide whether the schema is ready for JSON Schema or more refinement.

Implementation detail:

- summarize fixture coverage,
- list passing rules,
- list failing rules and whether they are schema gaps or fixture gaps,
- recommend one next route.

Smallest Working Units:

- `OVS-SWU-007`
  - Dependencies: `OVS-SWU-001` through `OVS-SWU-006`.
  - Write scope: validation report only.
  - Done criteria: report has pass/flag/block verdict and explicit next route.
  - Acceptance evidence: report path and validation command output.
  - Execution owner: local-fallback.
  - Handoff note: do not recommend canonical mutation unless L0-L2 are clean.

## Gates

| Gate | Pass condition | Blocks |
| --- | --- | --- |
| Fixture shape gate | Valid and invalid fixtures are inspectable and scoped. | Validator implementation if fixtures cannot represent the schema. |
| Deterministic rule gate | Required-field, enum, and cross-field rules produce expected outcomes. | Cross-system pressure test if rule checks are unreliable. |
| Boundary gate | Inventory and structured-action-schema remain non-authoritative. | Any promotion or template work. |
| Readiness gate | Report distinguishes schema gaps from fixture gaps. | JSON Schema generation and template candidate work. |

## Execution Evidence

| SWU | Result | Evidence |
| --- | --- | --- |
| OVS-SWU-001 | pass | `task-sessions/20260529T000000Z-ovs-swu-001/RESULT.md` |
| OVS-SWU-002 | pass | `task-sessions/20260529T001000Z-ovs-swu-002/RESULT.md` |
| OVS-SWU-003 | pass | `task-sessions/20260529T002000Z-ovs-swu-003/RESULT.md` |
| OVS-SWU-004 | pass | `task-sessions/20260529T003000Z-ovs-swu-004/RESULT.md` |
| OVS-SWU-005 | flag | `task-sessions/20260529T004000Z-ovs-swu-005/RESULT.md` |
| OVS-SWU-006 | pass | `task-sessions/20260529T005000Z-ovs-swu-006/RESULT.md` |
| OVS-SWU-007 | complete-with-flag | `VALIDATION-REPORT.md` |
| OVS-RK-001 | pass | `task-sessions/20260529T124348Z-ovs-rk-001/RESULT.md` |
| OVS-PROFILE-001 | pass | `task-sessions/20260529T162952Z-ovs-profile/RESULT.md` |
| OVS-PROFILE-002 | pass | `task-sessions/20260529T162952Z-ovs-profile/RESULT.md` |
| OVS-PROFILE-003 | pass | `task-sessions/20260529T162952Z-ovs-profile/RESULT.md` |
| OVS-PROFILE-004 | pass | `task-sessions/20260529T162952Z-ovs-profile/RESULT.md` |
| OVS-JSON-001 | pass | `task-sessions/20260529T164000Z-ovs-json/RESULT.md` |
| OVS-JSON-002 | pass | `task-sessions/20260529T164000Z-ovs-json/RESULT.md` |
| OVS-JSON-003 | pass | `task-sessions/20260529T164000Z-ovs-json/RESULT.md` |

## Current Blockers

No active blocker remains for publishing the current validation surface as a governed candidate bundle.

The previous blockers are resolved for development validation:

- `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` includes `record_kind`;
- valid fixtures declare `record_kind`;
- invalid fixtures include `record_kind: candidate` coverage;
- validator rule `V12` enforces enum membership and PromotionRecord boundary checks;
- schema candidate includes V13 record-kind profile rules;
- valid and invalid fixtures cover `evidence_input`;
- validator rule `V13` enforces profile checks for `ontology_entry`, `promotion_record`, `bridge_validation`, and `evidence_input`;
- the first development-only JSON Schema candidate validates the fixture corpus;
- deterministic fixture validation passes.
- OVS-GATE-001 selected `promote-governed-candidate-bundle`, allowing the bundle to be indexed as a published candidate.
- OVS-GATE-002 selected `promotion-record-canonical-record-kind`, making `promotion_record` canonical as an Ontology Vault governance decision shape while keeping templates and separate schemas gated.

## Current Gaps

- PromotionRecord companion schema/template split is deferred; the record-kind is canonical, but authoring templates and separate schemas still need narrower evidence and gates.
- Full DomainSpec validation still requires a DomainSpec-owned package; current DomainSpec coverage is a boundary-preserving pressure fixture.
- The future-system fixture is intentionally placeholder-level until a real future-system source exists.
- `dispatch-spec` command-surface resolution is unavailable in the refine run; direct schema validation works, but command-backed refine remains flagged.
- Canonical template/convention promotion remains blocked pending later, narrower gates.
- GoldenQuill L0 fixtures are now the best next evidence source for applied PromotionRecord compatibility.

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

## Next SWUs

| SWU | Goal | Verification |
| --- | --- | --- |
| OVS-PUBLISH-001 | Publish governed candidate-bundle index. | `GOVERNED-CANDIDATE-BUNDLE.md` exists and points to schema, fixtures, validators, validation report, and OVS-GATE-001. |
| OVS-GATE-001 | Decide promotion boundary for development-only schema, JSON Schema, and profiles. | Complete: selected `promote-governed-candidate-bundle`. |
| OVS-GATE-002 | Decide PromotionRecord canonical record-kind and companion template/schema boundary. | Complete: selected `promotion-record-canonical-record-kind`; template/schema work remains deferred. |
| OVS-GATE-003 | Decide DomainSpec handoff route. | DomainSpec-owned package remains separate from general ontology mechanics. |
| OVS-GQ-001 | Add GoldenQuill L0 PromotionRecord compatibility fixtures. | GoldenQuill local candidates project to PromotionRecord-compatible owner decisions without production mutation. |
