# Local Architecture: Boundary Evidence Schema

Status: flag
Owner: refine fallback synthesis
Reason: `invoke design` command surface resolved, but semantic execution used dry-run evidence only.

## Architecture Decision

Add an optional `boundary_evidence` object to `dispatch.schema.json`. Keep it
route-level first. Allow step-level references later only if fixture evidence
shows repeated need.

## Proposed JSON Shape

```json
{
  "boundary_evidence": {
    "boundaries": [
      {
        "boundary_id": "b1",
        "kind": "capability_handoff",
        "from_owner": "invoke",
        "to_owner": "task-session",
        "applies_to_steps": ["s2"],
        "contract": "handoff artifact must name write scope, done criteria, and validation surface",
        "on_violation": "block"
      }
    ],
    "authority": {
      "lifecycle": "dispatch-spec",
      "execution": "task-session",
      "validation": "dispatch-spec",
      "evidence": "signal-observer",
      "memory": "inventory",
      "promotion": "owning capability"
    },
    "receipts": [
      {
        "receipt_id": "r1",
        "producer": "task-session",
        "required_fields": ["run_id", "artifacts", "validation_result", "residue"],
        "stores": ["stages/result.md", ".arcanum/observability/signals/sigil-invocations.jsonl"],
        "on_missing": "flag"
      }
    ],
    "state_namespaces": [
      {
        "namespace": "repo-source",
        "owner": "git/worktree",
        "write_policy": "task-session only after approved plan"
      },
      {
        "namespace": "arcanum-observability",
        "owner": "signal-observer",
        "write_policy": "append-only telemetry"
      }
    ],
    "promotion_splits": [
      {
        "source": "execution evidence",
        "target": "inventory knowledge",
        "rule": "requires owner review before canonical promotion",
        "on_violation": "block"
      }
    ]
  }
}
```

## Field Rules

| Field | Rule |
| --- | --- |
| `boundaries[].kind` | Enum: `capability_handoff`, `artifact_import`, `human_approval`, `evidence_return`, `memory_interaction`, `state_write`, `external_context`. |
| `boundaries[].applies_to_steps` | Optional but must reference known `step_id` values when present. |
| `boundaries[].on_violation` | Enum: `block`, `flag`, `defer`, `ask`, `reroute`. |
| `authority` | Optional object; if present, values are owner strings, not booleans. |
| `receipts[].required_fields` | Non-empty array when a receipt exists. |
| `receipts[].on_missing` | Enum: `block`, `flag`, `defer`, `ask`, `reroute`; default should be `flag`. |
| `state_namespaces[].write_policy` | Required when `state_namespace_boundary` or replacement technique is cited. |
| `promotion_splits[].on_violation` | Should default to `block`. |

## Technique Catalog Migration

Rename the family from `Runtime Bridge And Evidence Techniques` to
`Boundary And Evidence Techniques`.

Suggested id changes:

| Current ID | Replacement |
| --- | --- |
| `runtime_adapter_boundary` | `delegation_boundary` |
| `runtime_receipt_handoff` | `execution_receipt_handoff` |
| `audit_summary_handoff` | `evidence_summary_handoff` |
| `dispatch_plan_projection` | `route_projection_boundary` |
| `agent_team_projection` | `role_projection_boundary` |

Keep:

- `authority_split_gate`
- `approval_semantics_map`
- `artifact_contract_bridge`
- `state_namespace_boundary`
- `memory_promotion_split`
- `concrete_path_evidence`

## Validator Architecture

Add validation in two layers:

1. JSON Schema validates field shape and enums.
2. `validate-dispatch.py` validates cross-references and authority safety.

Initial validator rules:

- block unknown `applies_to_steps`;
- block promotion split violations that claim runtime/execution evidence can
  promote Inventory/Ontology/glossary/sigil/spell;
- flag cited boundary/evidence techniques when `boundary_evidence` is missing;
- flag receipt-producing boundaries without receipt expectations;
- flag state namespace techniques without `state_namespaces`.
