# Ontology Runtime Profile

## Identity

- Profile id: {profile-id}
- Profile status: candidate | active-local | retired
- Repository: {repository}
- Owner route: {owner-route}
- Date: {date}

## Source Boundary

| Ref Type | Paths Or Handles | Allowed Use | Blocked Use |
| -------- | ---------------- | ----------- | ----------- |
| Base ontology refs | {base-ontology-refs} | Reusable model shape and non-authority rules. | Local owner decision. |
| Local ontology refs | {local-ontology-refs} | Candidate/local entries and project-specific aliases. | Canonical Arcanum vocabulary. |
| Local owner refs | {local-owner-refs} | Review, promotion, block, or retire decisions. | Silent promotion by proximity. |
| Source spine refs | {source-spine-refs} | Source posture and evidence family rules. | Resolution path unless owner route permits. |
| Implementation refs | {implementation-refs} | System/runtime evidence for bridge checks. | Runtime conformance verdict by itself. |

## Runtime Modes

Allowed runtime modes:

- inline
- agents

Default runtime mode: inline

Agent backend owner: {agent-backend-owner}

Agent backend gate:

- P1 trigger or local equivalent is satisfied.
- Tension or independent-review gate passes when multiple agents are used.
- Human confirmation is explicit before dispatch or execution.
- Dispatch/register/closeout ledger evidence is preserved.
- Agent outputs are delegated evidence, not authority.

## Runtime Outputs

Allowed outputs:

- ontology-map
- validation-report
- confidence-action-report
- premise-review
- drift-report
- candidate-map-projection
- review-index-projection
- delegated-evidence-record

Blocked outputs:

- promotion-verdict
- spec-mutation
- canonical-source-mutation
- runtime-conformance-verdict
- generated-projection-as-authority

## Owner Gates

| Movement | Owner Route | Required Evidence | Blocked Until |
| -------- | ----------- | ----------------- | ------------- |
| Candidate to reviewed candidate | {owner-route} | {evidence} | {gate} |
| Candidate to promotion request | {owner-route} | {evidence} | {gate} |
| Projection of owner-approved state | {owner-route} | {decision-record} | {gate} |

## Residue And Observability

- Residue route: {residue-route}
- Observability route: {observability-route}
- Inventory/read-model route: {inventory-route}

## Profile Validation

| Check | Result | Evidence Or Gap |
| ----- | ------ | --------------- |
| Required refs present | pass | {evidence} |
| Allowed and blocked outputs named | pass | {evidence} |
| Owner gates named | pass | {evidence} |
| Agent backend gated | pass | {evidence} |
| Promotion boundary preserved | pass | {evidence} |
