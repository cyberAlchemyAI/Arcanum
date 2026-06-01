# Stage 6: Invoke Redefine / Design

Status: pass.

## Proposed Technique Family

### Runtime Bridge And Evidence Techniques

These techniques help a dispatch document describe runtime crossings without claiming runtime authority.

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `runtime_adapter_boundary` | Mark a step that delegates bounded execution to a runtime adapter. | Adapter id, input contract, ownership boundary, and blocked fallback are named. |
| `dispatch_plan_projection` | Translate dispatch route metadata into an external plan or preview format. | Projection status is marked `preview`, `metadata-only`, or `requires-translation`; no direct schema equivalence is assumed. |
| `runtime_receipt_handoff` | Require runtime execution to return structured receipts. | Receipt fields include run/session ids, artifacts, validation result, approval records, and audit references where available. |
| `approval_semantics_map` | Map Arcanum decision/human gates to runtime approvals or questions. | The dispatch distinguishes lifecycle approval from runtime authorization. |
| `artifact_contract_bridge` | Bind Arcanum output contracts to runtime artifact validation. | Runtime artifact checks are recorded without claiming promotion readiness. |
| `evidence_receipt_link` | Link external runtime evidence into Arcanum observability or task evidence. | Store stable references and summaries, not full foreign runtime state. |
| `state_namespace_boundary` | Keep repository-local Arcanum state separate from runtime/workspace state. | State roots and owners are named; cross-system writes use explicit handoff artifacts. |
| `memory_promotion_split` | Separate runtime memory visibility changes from Arcanum knowledge promotion. | Runtime memory promotion cannot become Inventory/Ontology promotion without owner review. |
| `protected_action_mapping` | Identify steps that may require runtime policy, tenant, or approval controls. | Protected action class, policy owner, and fail behavior are named before execution. |
| `concrete_path_evidence` | Require runtime or evidence claims to cite concrete paths or handles. | Globs/placeholders are flagged unless they are intentionally unresolved route candidates. |
| `plan_import_preview_gate` | Preview an external workflow/plan import before making it runnable. | Import compatibility is checked before execution or automation arming. |
| `audit_summary_handoff` | Summarize runtime audit/tool ledger records for Arcanum consumption. | Summary links back to runtime-owned receipts and does not replace audit logs. |
| `agent_team_projection` | Project Arcanum role-bound subagents into runtime agent-team/task primitives. | Parent sigil authority, role boundaries, and join policy are preserved. |
| `capability_projection_pack` | Export selected sigil/spell metadata into an external catalog format. | Projection records source version, canonical owner, and non-authority status. |
| `authority_split_gate` | Explicitly decide which system owns lifecycle, runtime, evidence, and promotion authority. | Any unresolved authority owner blocks execution or promotion. |

## Placement

Add this family after `POLE-Inspired Standards Techniques` or before the use rule. It should be clearly runtime-agnostic, even though Tandem research motivated it.

## Related Documentation Updates

- `README.md`: mention runtime bridge/evidence techniques alongside Arcanum and POLE-inspired techniques.
- `ARCANUM-DISPATCH-SYNTHESIS.md`: add a short subsection explaining route-to-runtime boundary techniques.
- Optional later: add examples to a fixture after a validator exists.
