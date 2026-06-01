# Implementation Layering: Branch-Aware Ontology Schema Validation

Status: exploratory, non-canonical
Date: 2026-05-27

## Objective

Validate the branch-aware ontology schema candidate through tests before generating JSON Schema, revising templates, or changing canonical Ontology Vault behavior.

## Layer Summary

| Layer | Question | Output | Promotion Evidence |
| --- | --- | --- | --- |
| L0 Fixture Shape Proof | Can we express representative valid and invalid ontology entries as fixtures? | Development-only fixture set. | Fixtures cover branch, lifecycle, role, governance outcome, and bridge outcome axes. |
| L1 Deterministic Validator | Can a local validator catch required-field, enum, axis-split, and boundary errors? | Test runner and validation rules. | Passing positive fixtures and failing negative fixtures with useful messages. |
| L2 Cross-System Pressure Test | Does the schema survive Arcanum, CyberAlchemy, DomainSpec, and future-system examples? | Expanded fixtures and validation report. | Each system has at least one valid fixture and one targeted failure case. |
| L3 Promotion Readiness | Is the schema stable enough to become JSON Schema or candidate template material? | Readiness report and next-route decision. | No blocker gaps; remaining gaps are named and routed. |

## L0 Boundary

L0 should create fixtures only. It should not implement a full validator if fixture shape questions remain unresolved.

Required fixture families:

- valid branch examples: `meaning`, `system`, `operational`, `bridge`,
- valid axis examples: `lifecycle_status`, `claim_role`, `governance_outcome`, `bridge_outcome`,
- invalid examples for overloaded `status`, `claim_role: candidate`, missing operational context, missing bridge evidence, and Inventory authority leakage.

## L1 Boundary

L1 should implement the smallest deterministic validator that can check:

- required fields,
- enum membership,
- `branch_context.primary`,
- operational context requirements,
- bridge evidence requirements,
- Inventory non-authority notice,
- confidence split,
- promotion boundary,
- role/lifecycle axis split.

The validator may be a development script or test helper. It is not a canonical Ontology Vault runtime contract.

## L2 Boundary

L2 adds examples from:

- Arcanum Ontology Vault,
- CyberAlchemy ontology lifecycle / PromotionRecord,
- DomainSpec bridge scenario,
- future-system placeholder example.

The goal is classification pressure, not promotion.

## L3 Boundary

Only after L0-L2 pass should the package consider:

- generating JSON Schema,
- drafting candidate templates,
- proposing convention updates,
- opening a decision gate for `meaning` as global branch label.

## Deferrals

- JSON Schema generation is deferred.
- Template mutation is deferred.
- Inventory and structured-action-schema coordination is deferred to separate handoff.
