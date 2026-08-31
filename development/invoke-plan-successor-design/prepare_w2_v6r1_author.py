#!/usr/bin/env python3
"""Create the W2 V6R1 author that repairs the Distill Balancer blockers."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"expected one source fragment, found {count}: {old[:120]}")
    return text.replace(old, new)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    text = args.source.read_text(encoding="utf-8")

    replacements = [
        (
            '"responsibility": "Render Work Pack, task, wave, layering, and optional Execution Pack navigation from the normalized graph."',
            '"responsibility": "Render only Work Pack, task, wave, layering, and optional Execution Pack human navigation from the normalized graph; this component emits no consumer contract."',
        ),
        (
            '"responsibility": "Project only applicable WPRA, readiness, Task Session, Context Builder, Dispatch, Goal, and observer handoff contracts."',
            '"responsibility": "Exclusively project WPRA, Implementation Readiness, Task Session, Context Builder, Dispatch, Goal, and observer handoff contracts from the normalized graph according to the exact consumer applicability matrix."',
        ),
        (
            '"responsibility": "Keep authored, admitted, readiness, acceptance, execution, and terminal outcomes on separate evidence axes."',
            '"responsibility": "Act as a conditional post-admission boundary adapter that reads external lifecycle receipts and keeps authored, admitted, readiness, acceptance, execution, and terminal outcomes on separate axes; it is not a mandatory authoring stage."',
        ),
        (
            '"responsibility": "Validate historical Work-Pack-as-source material without admitting it for a new Plan PASS."',
            '"responsibility": "Act as a conditional compatibility adapter when historical Work-Pack-as-source material is supplied; it validates that material without admitting it for a new Plan PASS and is not a mandatory authoring stage."',
        ),
        (
            '{"fact_id": "contract:native-context-version", "fact_kind": "contract", "name": "Native-context version selection contract", "owner": "context-builder-owner", "attributes": {"contract_kind": "version-selection", "statement": "Use 1.2.0 when no transient outputs are declared and 1.3.0 when the transient-output set is nonempty.", "versioning": "Deterministically selects one currently supported contract.", "failure_boundary": "A version inconsistent with the exact transient-output set blocks the projection.", "preservation": "changed"}},',
            '{"fact_id": "contract:native-context-version", "fact_kind": "contract", "name": "Native-context version selection contract", "owner": "context-builder-owner", "attributes": {"contract_kind": "version-selection", "statement": "Use 1.2.0 when no transient outputs are declared and 1.3.0 when the transient-output set is nonempty.", "versioning": "Deterministically selects one currently supported contract.", "failure_boundary": "A version inconsistent with the exact transient-output set blocks the projection.", "preservation": "changed"}},\n'
            '        {"fact_id": "contract:consumer-applicability-matrix", "fact_kind": "contract", "name": "Per-consumer applicability matrix", "owner": "interface-owner", "attributes": {"contract_kind": "typed-applicability-matrix", "statement": "Each possible consumer has explicit predicate inputs, true and false results, required negative evidence, produced projection, no-effect validator or rehearsal, and failure route.", "versioning": "New successor contract bound to the Plan source schema.", "failure_boundary": "An absent, ambiguous, or unevaluable consumer row blocks bundle admission.", "preservation": "new"}},\n'
            '        {"fact_id": "decision:wpra-applicability", "fact_kind": "decision", "name": "WPRA applicability", "owner": "work-pack-readiness-audit-owner", "attributes": {"question": "Is the Plan mutation-capable?", "decision": "Read source field mutation_capable. True produces audit config v2, semantic manifest, and selection handoff and rehearses audit_work_pack.py; false requires exact mutation_capable=false evidence and produces no WPRA projection; missing or failed evidence blocks admission.", "rationale": "WPRA is required only for Plans that can reach mutation.", "outcomes": [{"condition": "mutation_capable=true", "result": "Project and rehearse WPRA inputs.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "mutation_capable=false", "result": "Record negative applicability evidence and omit WPRA projection.", "next_id": "workflow:admit-plan-bundle"}]}},\n'
            '        {"fact_id": "decision:implementation-readiness-applicability", "fact_kind": "decision", "name": "Implementation Readiness applicability", "owner": "implementation-readiness-owner", "attributes": {"question": "Can this Plan nominate an implementation unit?", "decision": "Read mutation_capable and execution_entries. A mutation-capable Plan with an eligible entry produces arcanum.work-pack-execution-entry/v1 and runs validate_work_pack_execution_entry.py; otherwise exact empty-entry or mutation-false evidence is required; unknown or failed validation blocks admission.", "rationale": "Artifact admission must not manufacture implementation readiness.", "outcomes": [{"condition": "mutation_capable=true and execution_entries is nonempty", "result": "Project and validate the readiness entry.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "mutation_capable=false or execution_entries is empty", "result": "Record negative evidence and omit the readiness projection.", "next_id": "workflow:admit-plan-bundle"}]}},\n'
            '        {"fact_id": "decision:task-session-applicability", "fact_kind": "decision", "name": "Task Session applicability", "owner": "task-session-owner", "attributes": {"question": "Does an execution entry route to Task Session?", "decision": "Read every execution_entry.route. Any task-session route produces an eligible-unit contract only and rehearses Task Session admission validation without selecting or launching work; otherwise all routes must prove they are not task-session; missing or failed evidence blocks admission.", "rationale": "Plan authorship may expose eligibility but cannot grant live Task Session admission.", "outcomes": [{"condition": "any route=task-session", "result": "Project the eligible-unit contract and validate it without effects.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "all routes differ from task-session", "result": "Record route-negative evidence and omit the Task Session projection.", "next_id": "workflow:admit-plan-bundle"}]}},\n'
            '        {"fact_id": "decision:context-builder-applicability", "fact_kind": "decision", "name": "Context Builder applicability", "owner": "context-builder-owner", "attributes": {"question": "Is any unit delegated or executable from bounded context?", "decision": "Read unit.delegated and unit.bounded_context_execution. True produces a strict native-context projection and runs compile_native_context_projection.py with version derived from transients; false requires every unit flag false; mismatch or failed validation blocks admission.", "rationale": "Context packs are required only where a bounded execution or delegation boundary exists.", "outcomes": [{"condition": "any unit delegated=true or bounded_context_execution=true", "result": "Project and validate strict native context.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "all unit flags are false", "result": "Record unit-level negative evidence and omit the context projection.", "next_id": "workflow:admit-plan-bundle"}]}},\n'
            '        {"fact_id": "decision:dispatch-applicability", "fact_kind": "decision", "name": "Dispatch applicability", "owner": "dispatch-spec-owner", "attributes": {"question": "Does the Plan require a full dispatch graph?", "decision": "Always emit a technique trace. Read route.multi_owner, delegated, protected_scope, and reusable_graph. Any true value produces a schema-valid dispatch and runs validate-dispatch.py in no-effect rehearsal; all false values retain trace-only negative evidence; unknown or failed validation blocks admission.", "rationale": "Simple single-owner work does not need a full dispatch graph, but delegation technique evidence is never omitted.", "outcomes": [{"condition": "any dispatch trigger is true", "result": "Project and rehearse the full dispatch graph.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "all dispatch triggers are false", "result": "Keep technique trace and record negative evidence for the full graph.", "next_id": "workflow:admit-plan-bundle"}]}},\n'
            '        {"fact_id": "decision:goal-applicability", "fact_kind": "decision", "name": "Goal applicability", "owner": "goal-owner", "attributes": {"question": "Does the Plan expose a Goal-compatible route?", "decision": "Read routes[].capability. A goal route produces frontier, route, expected receipt, stop, and fallback policy and runs Goal validation without ledger mutation; no goal route requires exact route-negative evidence; unknown or failed validation blocks admission.", "rationale": "Goal projection is route-specific and cannot be inferred from generic tasks.", "outcomes": [{"condition": "any capability=goal", "result": "Project and validate the Goal route without mutation.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "no capability=goal", "result": "Record route-negative evidence and omit the Goal projection.", "next_id": "workflow:admit-plan-bundle"}]}},\n'
            '        {"fact_id": "decision:observer-applicability", "fact_kind": "decision", "name": "Signal Observer applicability", "owner": "signal-observer-owner", "attributes": {"question": "Is observability configured and is a machine observer contract admitted?", "decision": "Read observability.configured and observer_contract_admitted. Both true are required before producing and no-append validating an observer envelope. Configured without an admitted contract blocks observer closure and defers observability-configured execution; configured=false records negative evidence and emits no projection.", "rationale": "Observer prose alone cannot become machine admission evidence.", "outcomes": [{"condition": "configured=true and observer_contract_admitted=true", "result": "Project and validate the no-append observer envelope.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "configured=false", "result": "Record configuration-negative evidence and omit the observer projection.", "next_id": "workflow:admit-plan-bundle"}, {"condition": "configured=true and observer_contract_admitted=false", "result": "Preserve the observer gap and block an observer-closure claim.", "next_id": "risk:false-observer-closure"}]}},',
        ),
        (
            '{"fact_id": "workflow:project-plan-views", "fact_kind": "workflow-step", "name": "Project Plan views and consumer contracts", "owner": "plan-work-pack-owner", "attributes": {"actor_or_component_id": "component:plan-view-projector", "action": "Generate navigation views and applicable consumer projections from the same graph.", "next_step_ids": ["workflow:admit-plan-bundle"]}},',
            '{"fact_id": "workflow:project-plan-views", "fact_kind": "workflow-step", "name": "Project Plan human views", "owner": "plan-work-pack-owner", "attributes": {"actor_or_component_id": "component:plan-view-projector", "action": "Generate only Work Pack, task, wave, layering, and optional Execution Pack navigation from the normalized graph.", "next_step_ids": ["workflow:project-consumer-contracts"]}},\n'
            '        {"fact_id": "workflow:project-consumer-contracts", "fact_kind": "workflow-step", "name": "Project applicable consumer contracts", "owner": "interface-owner", "attributes": {"actor_or_component_id": "component:execution-contract-projector", "action": "Evaluate every row in the consumer applicability matrix, produce each true-branch projection, and record exact negative evidence for each false branch.", "next_step_ids": ["workflow:admit-plan-bundle"]}},',
        ),
        (
            '"architecture:integration-versioning": ["component:execution-contract-projector", "contract:conditional-consumer-applicability", "contract:native-context-version", "decision:observer-gap", "dependency:wpra-readiness", "dependency:task-context-route", "risk:false-observer-closure"],',
            '"architecture:integration-versioning": ["component:execution-contract-projector", "contract:conditional-consumer-applicability", "contract:consumer-applicability-matrix", "contract:native-context-version", "decision:observer-gap", "decision:wpra-applicability", "decision:implementation-readiness-applicability", "decision:task-session-applicability", "decision:context-builder-applicability", "decision:dispatch-applicability", "decision:goal-applicability", "decision:observer-applicability", "dependency:wpra-readiness", "dependency:task-context-route", "risk:false-observer-closure", "workflow:project-consumer-contracts"],',
        ),
        (
            '"validation-contracts": ["component:plan-source-validator", "component:plan-bundle-admission-validator", "component:plan-evidence-resolver", "contract:plan-bundle-admission", "contract:conditional-consumer-applicability", "contract:native-context-version"],',
            '"validation-contracts": ["component:plan-source-validator", "component:plan-bundle-admission-validator", "component:plan-evidence-resolver", "contract:plan-bundle-admission", "contract:conditional-consumer-applicability", "contract:consumer-applicability-matrix", "contract:native-context-version"],',
        ),
        (
            '"decision": "Keep the Plan source, normalized graph, deterministic views, conditional consumer projections, and independent admission as one coherent artifact-authoring vertical; keep readiness and execution in later external evidence chains.",\n            "minimum_unit": "One exact Plan source through byte-identical bundle replay and no-effect rehearsal of every applicable machine-backed consumer."',
            '"decision": "The mandatory authoring vertical is Plan source validation, normalized graph compilation, separate human-view and consumer-contract projection, bundle production, and independent admission. PlanEvidenceResolver and PlanMigrationValidator are conditional boundary adapters outside that stage sequence; readiness and execution remain later external evidence chains.",\n            "minimum_unit": "One exact Plan source through one normalized graph, separately owned human and consumer projections, byte-identical bundle replay, and no-effect rehearsal or negative evidence for every consumer applicability row."',
        ),
        (
            '"evidence_ref": decision_ref,',
            '"evidence_ref": exact(repo / "arcanum/development/invoke-plan-successor-design/DISTILL-BALANCER-BLOCK-V6.json", repo),',
        ),
    ]
    for old, new in replacements:
        text = replace_once(text, old, new)
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
