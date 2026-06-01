# Stage 8: Distill Repair

Status: pass.

## Repair

Group the new techniques into five subfamilies to avoid catalog sprawl:

1. Runtime Boundary
   - `runtime_adapter_boundary`
   - `authority_split_gate`
   - `protected_action_mapping`

2. Projection
   - `dispatch_plan_projection`
   - `plan_import_preview_gate`
   - `capability_projection_pack`
   - `agent_team_projection`

3. Evidence And Receipts
   - `runtime_receipt_handoff`
   - `evidence_receipt_link`
   - `audit_summary_handoff`
   - `concrete_path_evidence`

4. Approval And Artifacts
   - `approval_semantics_map`
   - `artifact_contract_bridge`

5. State And Memory
   - `state_namespace_boundary`
   - `memory_promotion_split`

## Validation Rule

A dispatch document should be `flag` when it cites a runtime bridge technique but does not name the external runtime or adapter boundary. It should be `block` when it claims external runtime approval implies Arcanum promotion.
