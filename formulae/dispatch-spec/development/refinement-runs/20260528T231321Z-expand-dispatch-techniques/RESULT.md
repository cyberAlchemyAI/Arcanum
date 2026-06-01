# Refine Result: Dispatch Technique Expansion

Status: flag

The refinement produced a usable expansion design, but command-backed stages were captured through the `dry-run` adapter rather than nested model-backed execution. The artifact should be treated as a refined proposal and non-executed plan, not as completed catalog mutation.

## Final Synthesis

Expand `dispatch-spec` techniques with a new runtime-agnostic family:

```text
Runtime Bridge And Evidence Techniques
```

This family is justified by the Arcanum/Tandem research. It gives dispatch documents vocabulary for describing boundary crossings into runtime execution, plan projection, approval, artifact validation, audit evidence, state namespaces, and memory/promotion distinctions.

## Proposed Technique IDs

Runtime boundary:

- `runtime_adapter_boundary`
- `authority_split_gate`
- `protected_action_mapping`

Projection:

- `dispatch_plan_projection`
- `plan_import_preview_gate`
- `capability_projection_pack`
- `agent_team_projection`

Evidence and receipts:

- `runtime_receipt_handoff`
- `evidence_receipt_link`
- `audit_summary_handoff`
- `concrete_path_evidence`

Approval and artifacts:

- `approval_semantics_map`
- `artifact_contract_bridge`

State and memory:

- `state_namespace_boundary`
- `memory_promotion_split`

## Key Guardrail

Runtime bridge techniques must never imply:

- dispatch-spec executes anything,
- Tandem or any runtime owns Arcanum lifecycle promotion,
- runtime approval equals Arcanum semantic approval,
- runtime memory promotion equals Inventory/Ontology promotion,
- foreign audit logs should be copied wholesale into Arcanum observability.

## Recommended Next Routes

1. Task Session: update `TECHNIQUE-CATALOG.md`, `README.md`, and `ARCANUM-DISPATCH-SYNTHESIS.md` with the new technique family.
2. Refine or Invoke: create `TANDEM-DISPATCH-PLAN-CROSSWALK.md`.
3. Task Session: design `arcana/task-session/runtime-adapters/tandem.md`.
