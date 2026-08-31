# Dispatch Technique Catalog

Status: draft companion catalog for `dispatch.schema.yml`.

This catalog names reusable dispatch techniques that can be cited from a dispatch document with `techniques` at the dispatch or step level. It is not an execution engine and does not grant promotion authority. It gives route proposers a shared vocabulary for explaining why a route is shaped a certain way.

## Source Notes

Local Arcanum techniques are drawn from [ARCANUM-DISPATCH-SYNTHESIS.md](ARCANUM-DISPATCH-SYNTHESIS.md).

POLE-inspired techniques are adapted from the public NPCC / Police Digital Services "Minimum POLE Data Standards Dictionary", version 1.1 final, dated 2023-07-30. The useful transferable idea is a standards catalog discipline: entity classes, minimum components, component descriptors, validation rules, owner/steward/version metadata, data quality dimensions, and general validation notes. These techniques are domain-neutral here; they do not import policing semantics into Arcanum.

Boundary and evidence techniques are drawn from dispatch composition pressure inside Arcanum routes. They describe cross-capability handoffs, external evidence claims, state boundaries, approval semantics, and promotion safety without making `dispatch-spec` an execution engine.

## Arcanum Dispatch Techniques

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `sequence` | One step feeds the next. | Every non-first step consumes a prior frame, handle, decision, ledger, artifact, or external context. |
| `zig_zag` | Alternate generation with critique, or exploration with exploitation. | Stop conditions must prevent endless alternation. |
| `dialectic` | Preserve competing roles or principles until synthesis. | Roles and convergence criteria are required. |
| `tournament` | Compare multiple candidate routes, designs, or abstractions. | Elimination criteria, join policy, and rejected alternatives are recorded. |
| `scu_swu_reduction` | Find the smallest coherent or workable unit before planning. | The selected unit has a recomposition target. |
| `x_ray` | Explain hidden structure in an artifact, workflow, or architecture. | Output is a handle or artifact that later steps can consume. |
| `toy_game` | Test a design in a small controlled scenario. | Expected evidence artifact and failure interpretation are named. |
| `validation_loop` | Run fixture, example, or live validation before promotion. | Validation evidence and repair route are explicit. |
| `memory_loop` | Recover route history and preserve residue without silent promotion. | Inventory, Necronomicon, or owner-specific promotion guardrails are named. |
| `sentence_grammar` | Translate an operator sentence into structured slots. | Raw intent is preserved beside structured fields. |
| `route_menu` | Offer bounded route choices before selecting steps. | Menu items are bounded and selection is recorded or blocked. |
| `frame_handoff` | Pass safe summaries between steps. | Consumer and frame reference are named. |
| `handle_handoff` | Pass controlled artifact references between steps. | Raw artifacts are referenced by handle, not copied into unrelated owners. |
| `residue_ledger` | Preserve unresolved gaps, contradictions, and rejected candidates. | Residue has an owner or next route. |
| `spell_candidate` | Mark a repeated sequence as a possible Spellcraft target. | Dispatch validation precedes reusable spell authoring. |
| `pareto_gate` | Choose among options using non-dominated trade-offs. | Criteria and decision owner are recorded. |
| `recomposition_proof` | Prove a small unit still fits the larger target. | Recomposition target and failure route are named. |
| `owner_boundary_check` | Ensure steps do not claim another capability's authority. | Promotion guardrails block false ownership. |
| `observability_grouping` | Bind sibling steps under one `dispatch_id`. | Trace events include dispatch and step identifiers. |

## POLE-Inspired Standards Techniques

| Technique ID | Transferable Idea | Dispatch Use |
| --- | --- | --- |
| `entity_classing` | Class records into stable entity families. | Class steps as route, authoring, validation, execution, memory, or synthesis work. |
| `minimum_component_catalog` | Define the minimum components needed for a useful record. | Require only the fields needed to validate a route at the current layer. |
| `component_descriptor` | Describe each component by purpose and context. | Step inputs, outputs, gates, and evidence artifacts carry purpose notes when ambiguity exists. |
| `unique_standard_component` | Reuse the same component definition wherever it appears. | Shared concepts such as frame, handle, gate, and trace event keep one meaning. |
| `local_standard_component` | Apply local validation rules to a generic component. | Generic steps can add mode-specific rules without redefining the base step contract. |
| `entity_component_reference` | Allow one entity to include another entity as a component. | Dispatch steps may reference artifacts, packs, ledgers, or child dispatches by handle. |
| `component_reuse` | Components can repeat across entities without semantic drift. | A frame or ledger can appear in multiple steps while preserving its source. |
| `validation_rule_catalog` | Separate structural components from rules that validate them. | Schema structure and Formulae validation rules stay distinct. |
| `mandatory_component` | Mark components that must exist. | Required fields are explicit in schema and output contracts. |
| `conditional_component` | Make requirements depend on context. | Parallel steps require join policy; tournaments require convergence criteria; validation steps require evidence. |
| `one_or_more_option_set` | Require at least one option from a valid set. | Route menus and alternative lanes must name viable choices before selection. |
| `owner_steward_metadata` | Record owner and maintainer separately. | Dispatches name capability owner and validation steward where useful. |
| `version_status_metadata` | Track version, status, and approval state. | Dispatch artifacts can distinguish draft, live, deprecated, pass, flag, and block states. |
| `approval_checkpoint` | Record when a standard or route is approved. | Human approval and decision gates become explicit gates, not implicit agreement. |
| `attribute_descriptor` | Give attributes names, descriptions, ranges, and validation. | Technique refs, step fields, and gates can include purpose and validation notes. |
| `min_max_constraint` | Bound valid lengths or counts. | Route menus, stage loops, and research passes stay within declared budgets. |
| `default_value_rule` | Use defaults only when no explicit value is supplied. | Presets and research modes are defaulted visibly. |
| `value_range_rule` | Limit values to a known range. | Pattern, mode, gate, and status enums are bounded where governance needs stability. |
| `data_quality_accuracy` | Data should be accurate enough for its purpose. | Dispatch evidence must reflect the actual owner artifact, not a convenient paraphrase. |
| `data_quality_integrity` | Relationships and use must comply with requirements. | Inputs, outputs, gates, and promotion guardrails must not contradict owner boundaries. |
| `data_quality_timeliness` | Capture data near the event and make it available when needed. | Stage evidence and trace events are recorded during the run, not reconstructed later. |
| `data_quality_completeness` | Data should be sufficient for meaningful inference. | Missing required components produce `flag` or `block`, not silent assumptions. |
| `data_quality_conformity` | Use stable definitions and consistent collection processes. | Dispatch documents conform to schema and catalog vocabulary. |
| `data_quality_deduplication` | Avoid duplicate records that create drift. | Dispatches reference existing handles and parent dispatches rather than copying artifacts. |
| `general_validation_notes` | Preserve common quality notes outside individual records. | Cross-cutting validation notes live in Dispatch Spec rather than in each capability. |
| `format_conformity_check` | Validate expected formats. | Dates, ids, artifact paths, statuses, and enums must be machine-checkable where possible. |
| `orphan_record_check` | Records should be linked to meaningful context. | A step without an input, output, consumer, or parent dispatch is invalid or flagged. |
| `protected_context_flag` | Mark sensitive or protected context explicitly. | External or sensitive context is labelled and cannot silently become canonical memory. |
| `system_agnostic_standard` | Define standards independent of implementation systems. | Dispatch Spec validates route shape without assuming a specific executor. |
| `local_nuance_coordination` | Local differences should be coordinated against shared standards. | Capability-specific modes can extend dispatch only with source and validation notes. |
| `assessment_failure_reference` | Failed records should point to the reason and affected record. | Blocked dispatches name the failed step, gate, or field with a repair route. |

## Boundary And Evidence Techniques

These techniques describe boundary crossings between an Arcanum dispatch route and another capability, artifact, approval surface, state namespace, or evidence system. A dispatch that cites them still does not execute work or grant promotion authority.

### Boundary

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `delegation_boundary` | Mark a step that delegates bounded work to another capability, role, or executor. | Delegation target, input contract, ownership boundary, and blocked fallback are named. |
| `authority_split_gate` | Decide which owner holds lifecycle, execution, validation, evidence, memory, and promotion authority. | Any unresolved authority owner blocks execution or promotion. |
| `protected_action_mapping` | Identify steps that may require policy, tenant, human, or approval controls. | Protected action class, policy owner, and fail behavior are named before execution. |

### Projection

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `route_projection_boundary` | Translate dispatch route metadata into an external plan, preview, or handoff format. | Projection status is marked `preview`, `metadata-only`, or `requires-translation`; no direct schema equivalence is assumed. |
| `plan_import_preview_gate` | Preview an external workflow/plan import before making it runnable. | Import compatibility is checked before execution or automation arming. |
| `capability_projection_pack` | Export selected sigil/spell metadata into an external catalog format. | Projection records source version, canonical owner, and non-authority status. |
| `role_projection_boundary` | Project Arcanum role-bound subagents into another planning or task primitive. | Parent sigil authority, role boundaries, and join policy are preserved. |

### Evidence And Receipts

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `execution_receipt_handoff` | Require delegated execution or bounded work to return structured receipts. | Receipt fields include run/session ids, artifacts, validation result, approval records, and audit references where available. |
| `evidence_receipt_link` | Link external or downstream evidence into Arcanum observability or task evidence. | Store stable references and summaries, not full foreign state. |
| `evidence_summary_handoff` | Summarize audit, tool, or evidence ledger records for Arcanum consumption. | Summary links back to owner-held receipts and does not replace audit logs. |
| `concrete_path_evidence` | Require evidence claims to cite concrete paths or handles. | Globs/placeholders are flagged unless they are intentionally unresolved route candidates. |

### Approval And Artifacts

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `approval_semantics_map` | Map Arcanum decision/human gates to approval records or questions. | The dispatch distinguishes lifecycle approval from execution authorization. |
| `artifact_contract_bridge` | Bind Arcanum output contracts to artifact validation. | Artifact checks are recorded without claiming promotion readiness. |

### State And Memory

| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `state_namespace_boundary` | Keep repository-local source, generated evidence, observability, and workspace state separate. | State roots and owners are named; cross-boundary writes use explicit handoff artifacts. |
| `memory_promotion_split` | Separate memory visibility changes from Arcanum knowledge promotion. | Memory visibility cannot become Inventory/Ontology promotion without owner review. |

## Use Rule

Dispatch documents should cite only the techniques that actually affect the route. A route that lists techniques without using them in steps, gates, or validation notes should be `flag`.
Boundary and evidence techniques should name the relevant owner or boundary; claiming that execution approval implies Arcanum promotion should be `block`.
