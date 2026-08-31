#!/usr/bin/env python3
"""Author the complete W2 source request from the exact W1 V6 denominator."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
from typing import Any


TARGET = "invoke:plan-successor:definition-target"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root).as_posix(),
        "sha256": __import__("hashlib").sha256(data).hexdigest(),
        "size": len(data),
    }


def remove_pointer(document: dict[str, Any], pointer: str) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    current: Any = document
    for part in parts[:-1]:
        current = current[part]
    current.pop(parts[-1])


def strip_exact_refs(value: Any, pointer: str = "") -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    if isinstance(value, dict):
        if {"path", "sha256", "size"}.issubset(value):
            bindings.append({"pointer": pointer, "path": value["path"]})
            value.pop("sha256")
            value.pop("size")
        for key, child in list(value.items()):
            escaped = key.replace("~", "~0").replace("/", "~1")
            bindings.extend(strip_exact_refs(child, f"{pointer}/{escaped}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            bindings.extend(strip_exact_refs(child, f"{pointer}/{index}"))
    return bindings


def requirement(kind: str, identifier: str) -> dict[str, str]:
    return {"subject_kind": kind, "subject_id": identifier}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--closure", required=True, type=Path)
    parser.add_argument("--w1-dir", required=True, type=Path)
    parser.add_argument("--no-prior", required=True, type=Path)
    parser.add_argument("--definitions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        raise ValueError("--output must be absent")

    closure_path = args.closure.resolve()
    w1 = args.w1_dir.resolve()
    closure = load(closure_path)
    selection = load(w1 / "DESIGN-SELECTION-RESULT.json")
    definitions = load(args.definitions.resolve())
    if closure["target"]["id"] != TARGET:
        raise ValueError("W1 target mismatch")
    receipt = load(w1 / "DESIGN-INPUT-PRODUCTION-RECEIPT.json")
    if receipt.get("result") != "pass" or receipt.get("next_route") != "design-authoring":
        raise ValueError("W1 production receipt is not an exact Design-authoring PASS")

    invoke = repo / "arcanum/spells/invoke"
    validator = load_module(
        "plan_successor_w2_validator", invoke / "scripts/validate_design_coherence.py"
    )
    profile_path = invoke / "development/whole-invoke-repair-plan/design-process/DESIGN-PROFILE.json"
    profile = load(profile_path)
    closure_ref = exact(closure_path, repo)
    decision_ref = exact(
        repo / "arcanum/development/invoke-plan-successor-design/PLAN-SUCCESSOR-DESIGN-OWNER-DECISION-V6.json",
        repo,
    )

    core_specs: list[dict[str, Any]] = [
        {"fact_id": "system:plan-successor", "fact_kind": "system", "name": "Plan successor authoring system", "owner": "invoke-plan-owner", "attributes": {"responsibility": "Turn one admitted Design into one canonical Plan source, deterministic views, and independently admitted Plan bundle without granting execution authority."}},
        {"fact_id": "component:plan-source-validator", "fact_kind": "component", "name": "Plan source validator", "owner": "invoke-plan-owner", "attributes": {"level": "high-level", "parent_component_id": None, "responsibility": "Validate the canonical Plan source and its graph invariants before any view is generated.", "contract_ids": ["contract:plan-source-v2"]}},
        {"fact_id": "component:plan-graph-compiler", "fact_kind": "component", "name": "Plan graph compiler", "owner": "invoke-plan-owner", "attributes": {"level": "high-level", "parent_component_id": None, "responsibility": "Compile the exact Plan source into one normalized graph shared by every projection.", "contract_ids": ["contract:plan-source-v2"]}},
        {"fact_id": "component:plan-view-projector", "fact_kind": "component", "name": "Plan view projector", "owner": "plan-work-pack-owner", "attributes": {"level": "low-level", "parent_component_id": "component:plan-graph-compiler", "responsibility": "Render only Work Pack, task, wave, layering, and optional Execution Pack human navigation from the normalized graph; this component emits no consumer contract.", "contract_ids": ["contract:work-pack-navigation"]}},
        {"fact_id": "component:execution-contract-projector", "fact_kind": "component", "name": "Execution contract projector", "owner": "implementation-readiness-owner", "attributes": {"level": "low-level", "parent_component_id": "component:plan-graph-compiler", "responsibility": "Exclusively project WPRA, Implementation Readiness, Task Session, Context Builder, Dispatch, Goal, and observer handoff contracts from the normalized graph according to the exact consumer applicability matrix.", "contract_ids": ["contract:conditional-consumer-applicability", "contract:native-context-version"]}},
        {"fact_id": "component:plan-bundle-producer", "fact_kind": "component", "name": "Plan bundle producer", "owner": "invoke-plan-owner", "attributes": {"level": "high-level", "parent_component_id": None, "responsibility": "Publish one complete Plan candidate bundle through an absent staging directory and atomic replacement.", "contract_ids": ["contract:plan-bundle-admission"]}},
        {"fact_id": "component:plan-bundle-admission-validator", "fact_kind": "component", "name": "Plan bundle admission validator", "owner": "invoke-plan-admission-owner", "attributes": {"level": "high-level", "parent_component_id": None, "responsibility": "Independently recompile, byte-compare, and rehearse every applicable machine-backed consumer without product effects.", "contract_ids": ["contract:plan-bundle-admission", "contract:conditional-consumer-applicability"]}},
        {"fact_id": "component:plan-evidence-resolver", "fact_kind": "component", "name": "Plan evidence resolver", "owner": "invoke-plan-owner", "attributes": {"level": "low-level", "parent_component_id": "component:plan-bundle-admission-validator", "responsibility": "Act as a conditional post-admission boundary adapter that reads external lifecycle receipts and keeps authored, admitted, readiness, acceptance, execution, and terminal outcomes on separate axes; it is not a mandatory authoring stage.", "contract_ids": ["contract:plan-bundle-admission"]}},
        {"fact_id": "component:plan-migration-validator", "fact_kind": "component", "name": "Plan migration validator", "owner": "migration-owner", "attributes": {"level": "low-level", "parent_component_id": "component:plan-source-validator", "responsibility": "Act as a conditional compatibility adapter when historical Work-Pack-as-source material is supplied; it validates that material without admitting it for a new Plan PASS and is not a mandatory authoring stage.", "contract_ids": ["contract:plan-source-v2"]}},
        {"fact_id": "contract:plan-source-v2", "fact_kind": "contract", "name": "Canonical Plan source contract", "owner": "invoke-plan-owner", "attributes": {"contract_kind": "canonical-machine-source", "statement": "One JSON source owns objectives, slices, layers, waves, tasks, SWUs, implementation details, validation obligations, gates, blockers, gaps, eligible execution entries, and closeout obligations.", "versioning": "Successor v2; historical v1 material remains validate-only.", "failure_boundary": "Reject invalid or ambiguous graphs before generating views.", "preservation": "new"}},
        {"fact_id": "contract:plan-bundle-admission", "fact_kind": "contract", "name": "Plan bundle admission contract", "owner": "invoke-plan-admission-owner", "attributes": {"contract_kind": "independent-replay-admission", "statement": "Admission replays the exact source, compares every output byte, and validates every applicable consumer without granting readiness or execution.", "versioning": "New successor contract; historical receipts are validate-only.", "failure_boundary": "Any stale binding, byte mismatch, missing consumer proof, or unknown value blocks admission.", "preservation": "new"}},
        {"fact_id": "contract:work-pack-navigation", "fact_kind": "contract", "name": "Generated Work Pack navigation contract", "owner": "ux-plan-owner", "attributes": {"contract_kind": "human-navigation-view", "statement": "A plan coordinator can locate objectives, slices, waves, tasks, gates, blockers, gaps, and the next eligible action without treating the view as semantic authority.", "versioning": "Generated from the exact Plan source; manual edits are drift.", "failure_boundary": "Unreadable, incomplete, or source-divergent navigation blocks bundle admission.", "preservation": "changed"}},
        {"fact_id": "contract:conditional-consumer-applicability", "fact_kind": "contract", "name": "Conditional consumer applicability contract", "owner": "interface-owner", "attributes": {"contract_kind": "consumer-closure", "statement": "Every possible consumer has a machine-checkable applicability predicate; applicable consumers require exact no-effect rehearsal and inapplicable consumers require negative evidence.", "versioning": "New successor contract.", "failure_boundary": "Missing predicates, skipped consumers, or prose-only closure claims block admission.", "preservation": "new"}},
        {"fact_id": "contract:native-context-version", "fact_kind": "contract", "name": "Native-context version selection contract", "owner": "context-builder-owner", "attributes": {"contract_kind": "version-selection", "statement": "Use 1.2.0 when no transient outputs are declared and 1.3.0 when the transient-output set is nonempty.", "versioning": "Deterministically selects one currently supported contract.", "failure_boundary": "A version inconsistent with the exact transient-output set blocks the projection.", "preservation": "changed"}},
        {"fact_id": "contract:consumer-applicability-matrix", "fact_kind": "contract", "name": "Per-consumer applicability matrix", "owner": "interface-owner", "attributes": {"contract_kind": "typed-applicability-matrix", "statement": "Each possible consumer has explicit predicate inputs, true and false results, required negative evidence, produced projection, no-effect validator or rehearsal, and failure route.", "versioning": "New successor contract bound to the Plan source schema.", "failure_boundary": "An absent, ambiguous, or unevaluable consumer row blocks bundle admission.", "preservation": "new"}},
        {"fact_id": "decision:wpra-applicability", "fact_kind": "decision", "name": "WPRA applicability", "owner": "work-pack-readiness-audit-owner", "attributes": {"question": "Is the Plan mutation-capable?", "decision": "Read source field mutation_capable. True produces audit config v2, semantic manifest, and selection handoff and rehearses audit_work_pack.py; false requires exact mutation_capable=false evidence and produces no WPRA projection; missing or failed evidence blocks admission.", "rationale": "WPRA is required only for Plans that can reach mutation.", "outcomes": [{"condition": "mutation_capable=true", "result": "Project and rehearse WPRA inputs.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "mutation_capable=false", "result": "Record negative applicability evidence and omit WPRA projection.", "next_id": "workflow:admit-plan-bundle"}]}},
        {"fact_id": "decision:implementation-readiness-applicability", "fact_kind": "decision", "name": "Implementation Readiness applicability", "owner": "implementation-readiness-owner", "attributes": {"question": "Can this Plan nominate an implementation unit?", "decision": "Read mutation_capable and execution_entries. A mutation-capable Plan with an eligible entry produces arcanum.work-pack-execution-entry/v1 and runs validate_work_pack_execution_entry.py; otherwise exact empty-entry or mutation-false evidence is required; unknown or failed validation blocks admission.", "rationale": "Artifact admission must not manufacture implementation readiness.", "outcomes": [{"condition": "mutation_capable=true and execution_entries is nonempty", "result": "Project and validate the readiness entry.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "mutation_capable=false or execution_entries is empty", "result": "Record negative evidence and omit the readiness projection.", "next_id": "workflow:admit-plan-bundle"}]}},
        {"fact_id": "decision:task-session-applicability", "fact_kind": "decision", "name": "Task Session applicability", "owner": "task-session-owner", "attributes": {"question": "Does an execution entry route to Task Session?", "decision": "Read every execution_entry.route. Any task-session route produces an eligible-unit contract only and rehearses Task Session admission validation without selecting or launching work; otherwise all routes must prove they are not task-session; missing or failed evidence blocks admission.", "rationale": "Plan authorship may expose eligibility but cannot grant live Task Session admission.", "outcomes": [{"condition": "any route=task-session", "result": "Project the eligible-unit contract and validate it without effects.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "all routes differ from task-session", "result": "Record route-negative evidence and omit the Task Session projection.", "next_id": "workflow:admit-plan-bundle"}]}},
        {"fact_id": "decision:context-builder-applicability", "fact_kind": "decision", "name": "Context Builder applicability", "owner": "context-builder-owner", "attributes": {"question": "Is any unit delegated or executable from bounded context?", "decision": "Read unit.delegated and unit.bounded_context_execution. True produces a strict native-context projection and runs compile_native_context_projection.py with version derived from transients; false requires every unit flag false; mismatch or failed validation blocks admission.", "rationale": "Context packs are required only where a bounded execution or delegation boundary exists.", "outcomes": [{"condition": "any unit delegated=true or bounded_context_execution=true", "result": "Project and validate strict native context.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "all unit flags are false", "result": "Record unit-level negative evidence and omit the context projection.", "next_id": "workflow:admit-plan-bundle"}]}},
        {"fact_id": "decision:dispatch-applicability", "fact_kind": "decision", "name": "Dispatch applicability", "owner": "dispatch-spec-owner", "attributes": {"question": "Does the Plan require a full dispatch graph?", "decision": "Always emit a technique trace. Read route.multi_owner, delegated, protected_scope, and reusable_graph. Any true value produces a schema-valid dispatch and runs validate-dispatch.py in no-effect rehearsal; all false values retain trace-only negative evidence; unknown or failed validation blocks admission.", "rationale": "Simple single-owner work does not need a full dispatch graph, but delegation technique evidence is never omitted.", "outcomes": [{"condition": "any dispatch trigger is true", "result": "Project and rehearse the full dispatch graph.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "all dispatch triggers are false", "result": "Keep technique trace and record negative evidence for the full graph.", "next_id": "workflow:admit-plan-bundle"}]}},
        {"fact_id": "decision:goal-applicability", "fact_kind": "decision", "name": "Goal applicability", "owner": "goal-owner", "attributes": {"question": "Does the Plan expose a Goal-compatible route?", "decision": "Read routes[].capability. A goal route produces frontier, route, expected receipt, stop, and fallback policy and runs Goal validation without ledger mutation; no goal route requires exact route-negative evidence; unknown or failed validation blocks admission.", "rationale": "Goal projection is route-specific and cannot be inferred from generic tasks.", "outcomes": [{"condition": "any capability=goal", "result": "Project and validate the Goal route without mutation.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "no capability=goal", "result": "Record route-negative evidence and omit the Goal projection.", "next_id": "workflow:admit-plan-bundle"}]}},
        {"fact_id": "decision:observer-applicability", "fact_kind": "decision", "name": "Signal Observer applicability", "owner": "signal-observer-owner", "attributes": {"question": "Is observability configured and is a machine observer contract admitted?", "decision": "Read observability.configured and observer_contract_admitted. Both true are required before producing and no-append validating an observer envelope. Configured without an admitted contract blocks observer closure and defers observability-configured execution; configured=false records negative evidence and emits no projection.", "rationale": "Observer prose alone cannot become machine admission evidence.", "outcomes": [{"condition": "configured=true and observer_contract_admitted=true", "result": "Project and validate the no-append observer envelope.", "next_id": "workflow:project-consumer-contracts"}, {"condition": "configured=false", "result": "Record configuration-negative evidence and omit the observer projection.", "next_id": "workflow:admit-plan-bundle"}, {"condition": "configured=true and observer_contract_admitted=false", "result": "Preserve the observer gap and block an observer-closure claim.", "next_id": "risk:false-observer-closure"}]}},
        {"fact_id": "workflow:validate-plan-source", "fact_kind": "workflow-step", "name": "Validate Plan source", "owner": "invoke-plan-owner", "attributes": {"actor_or_component_id": "component:plan-source-validator", "action": "Validate the source schema, identities, relationships, graph totals, and predecessor bindings.", "next_step_ids": ["workflow:compile-plan-graph"]}},
        {"fact_id": "workflow:compile-plan-graph", "fact_kind": "workflow-step", "name": "Compile Plan graph", "owner": "invoke-plan-owner", "attributes": {"actor_or_component_id": "component:plan-graph-compiler", "action": "Compile one normalized graph from the validated source.", "next_step_ids": ["workflow:project-plan-views"]}},
        {"fact_id": "workflow:project-plan-views", "fact_kind": "workflow-step", "name": "Project Plan human views", "owner": "plan-work-pack-owner", "attributes": {"actor_or_component_id": "component:plan-view-projector", "action": "Generate only Work Pack, task, wave, layering, and optional Execution Pack navigation from the normalized graph.", "next_step_ids": ["workflow:project-consumer-contracts"]}},
        {"fact_id": "workflow:project-consumer-contracts", "fact_kind": "workflow-step", "name": "Project applicable consumer contracts", "owner": "interface-owner", "attributes": {"actor_or_component_id": "component:execution-contract-projector", "action": "Evaluate every row in the consumer applicability matrix, produce each true-branch projection, and record exact negative evidence for each false branch.", "next_step_ids": ["workflow:admit-plan-bundle"]}},
        {"fact_id": "workflow:admit-plan-bundle", "fact_kind": "workflow-step", "name": "Admit Plan bundle", "owner": "invoke-plan-admission-owner", "attributes": {"actor_or_component_id": "component:plan-bundle-admission-validator", "action": "Recompile, byte-compare, and run no-effect consumer rehearsals before recording admission.", "next_step_ids": []}},
        {"fact_id": "state:plan-source-draft", "fact_kind": "state", "name": "Plan source draft", "owner": "invoke-plan-owner", "attributes": {"subject_id": "system:plan-successor", "allowed_next_state_ids": ["state:plan-source-valid", "state:plan-blocked"]}},
        {"fact_id": "state:plan-source-valid", "fact_kind": "state", "name": "Plan source valid", "owner": "invoke-plan-owner", "attributes": {"subject_id": "system:plan-successor", "allowed_next_state_ids": ["state:plan-bundle-compiled", "state:plan-blocked"]}},
        {"fact_id": "state:plan-bundle-compiled", "fact_kind": "state", "name": "Plan bundle compiled", "owner": "invoke-plan-owner", "attributes": {"subject_id": "system:plan-successor", "allowed_next_state_ids": ["state:plan-bundle-admitted", "state:plan-blocked"]}},
        {"fact_id": "state:plan-bundle-admitted", "fact_kind": "state", "name": "Plan bundle admitted", "owner": "invoke-plan-admission-owner", "attributes": {"subject_id": "system:plan-successor", "allowed_next_state_ids": ["state:plan-artifact-authored", "state:plan-blocked"]}},
        {"fact_id": "state:plan-artifact-authored", "fact_kind": "state", "name": "Plan artifact authored", "owner": "invoke-plan-owner", "attributes": {"subject_id": "system:plan-successor", "allowed_next_state_ids": []}},
        {"fact_id": "state:plan-blocked", "fact_kind": "state", "name": "Plan blocked", "owner": "invoke-plan-owner", "attributes": {"subject_id": "system:plan-successor", "allowed_next_state_ids": ["state:plan-source-draft"]}},
        {"fact_id": "decision:single-plan-source", "fact_kind": "decision", "name": "Single Plan source authority", "owner": "authority-owner", "attributes": {"question": "Which artifact owns Plan meaning?", "decision": "One canonical JSON Plan source owns meaning; Markdown and execution documents are generated views.", "rationale": "A single machine source prevents contradictory edits and supports deterministic replay.", "outcomes": [{"condition": "The source is valid.", "result": "Compile the normalized graph.", "next_id": "workflow:compile-plan-graph"}]}},
        {"fact_id": "decision:external-lifecycle-state", "fact_kind": "decision", "name": "External lifecycle evidence", "owner": "authority-owner", "attributes": {"question": "May the Plan source record achieved lifecycle outcomes?", "decision": "No. Admission, readiness, selection, acceptance, execution, terminal, and continuity outcomes remain external receipts.", "rationale": "Authored intent cannot manufacture evidence about later work.", "outcomes": [{"condition": "A lifecycle outcome is needed.", "result": "Read the responsible external receipt.", "next_id": "component:plan-evidence-resolver"}]}},
        {"fact_id": "decision:observer-gap", "fact_kind": "decision", "name": "Signal Observer machine-gap treatment", "owner": "signal-observer-owner", "attributes": {"question": "Does Signal Observer prose establish consumer closure?", "decision": "No. Preserve a conditional gap until a schema, deterministic projector or validator, and no-append fixture exist.", "rationale": "README and skill prose cannot be machine-admitted evidence.", "outcomes": [{"condition": "Observability is configured without machine contracts.", "result": "Flag the gap and block an observer-closure claim.", "next_id": "risk:false-observer-closure"}]}},
        {"fact_id": "dependency:wpra-readiness", "fact_kind": "dependency", "name": "Plan to readiness dependency", "owner": "interface-owner", "attributes": {"consumer_id": "component:execution-contract-projector", "target_id": "contract:conditional-consumer-applicability", "dependency_kind": "mutation-capable Plan readiness", "failure_policy": "Block admission when required WPRA or Implementation Readiness projections fail."}},
        {"fact_id": "dependency:task-context-route", "fact_kind": "dependency", "name": "Task and context route dependency", "owner": "interface-owner", "attributes": {"consumer_id": "component:execution-contract-projector", "target_id": "contract:native-context-version", "dependency_kind": "selected execution-entry projection", "failure_policy": "Require Task Session and strict Context Builder projections only when their route predicates are true."}},
        {"fact_id": "risk:derived-view-authority", "fact_kind": "risk", "name": "Derived view becomes a second source", "owner": "authority-owner", "attributes": {"risk": "A generated Markdown or execution view is edited as if it owned Plan meaning.", "mitigation": "Bind every view to the source digest and reject byte drift during admission."}},
        {"fact_id": "risk:false-observer-closure", "fact_kind": "risk", "name": "Prose mistaken for observer closure", "owner": "signal-observer-owner", "attributes": {"risk": "Signal Observer is counted as admitted without a machine contract or no-append rehearsal.", "mitigation": "Keep the integration flagged and prohibit a closure claim until machine evidence exists."}},
        {"fact_id": "risk:historical-plan-activation", "fact_kind": "risk", "name": "Historical Plan format establishes new PASS", "owner": "migration-owner", "attributes": {"risk": "A v1 Work-Pack-as-source artifact is treated as current successor evidence.", "mitigation": "Validate historical formats read-only and require the successor source and admission for every new PASS."}},
    ]

    facts = [{**item, "requirement_refs": []} for item in core_specs]
    signal_fact_ids: dict[tuple[str, str], str] = {}
    signal_output: dict[str, str] = {}
    output_by_signal_class = {
        "human_actors": "ux-plan",
        "rendered_surfaces": "ux-plan",
        "interfaces": "architecture:integration-versioning",
        "stores": "architecture:persistence-concurrency",
        "queues": "architecture:persistence-concurrency",
        "writers": "architecture:persistence-concurrency",
        "data_and_log_sinks": "architecture:persistence-concurrency",
        "deployment_targets": "architecture:migration-rollout",
        "compatibility_boundaries": "architecture:migration-rollout",
        "quality_claims": "architecture:quality",
        "acceptance_and_readiness_claims": "validation-contracts",
    }
    for signal_class, values in closure["scope_signals"].items():
        fact_kind, identity_key, fields = validator.SIGNAL_MAP[signal_class]
        for signal in values:
            fact_id = signal[identity_key]
            signal_fact_ids[("scope-signal", signal["signal_id"])] = fact_id
            selected_output = output_by_signal_class.get(signal_class)
            if signal_class == "normative_rules":
                rule_id = signal["rule_id"]
                if rule_id == "rule:single-plan-source":
                    selected_output = "architecture:authority-trust"
                elif rule_id == "rule:terminal-plan-handoff":
                    selected_output = "architecture:state-event"
                else:
                    selected_output = "validation-contracts"
            elif signal_class == "effects":
                selected_output = (
                    "architecture:failure-compensation"
                    if signal["effect_id"] == "effect:implementation-execution"
                    else "validation-contracts"
                )
            if selected_output is None:
                raise ValueError(f"no selected-output mapping for signal class {signal_class}")
            signal_output[fact_id] = selected_output
            facts.append(
                {
                    "fact_id": fact_id,
                    "fact_kind": fact_kind,
                    "name": f"W1 {signal_class.replace('_', ' ')}: {fact_id}",
                    "owner": "invoke-plan-owner",
                    "requirement_refs": [],
                    "attributes": {field: copy.deepcopy(signal[field]) for field in fields},
                }
            )

    core_ids = [item["fact_id"] for item in facts if item["fact_id"] not in signal_output]
    common_ids = [
        "system:plan-successor",
        "component:plan-source-validator",
        "component:plan-graph-compiler",
        "contract:plan-source-v2",
    ]
    output_fact_ids: dict[str, list[str]] = {
        "architecture:authority-trust": ["contract:plan-source-v2", "decision:single-plan-source", "decision:external-lifecycle-state", "risk:derived-view-authority"],
        "architecture:state-event": [item for item in core_ids if item.startswith(("workflow:", "state:"))],
        "architecture:persistence-concurrency": ["component:plan-bundle-producer", "component:plan-bundle-admission-validator", "contract:plan-bundle-admission"],
        "architecture:failure-compensation": ["workflow:admit-plan-bundle", "state:plan-blocked", "risk:false-observer-closure", "risk:historical-plan-activation"],
        "architecture:quality": ["component:plan-source-validator", "component:plan-bundle-admission-validator", "contract:plan-bundle-admission", "risk:derived-view-authority"],
        "architecture:integration-versioning": ["component:execution-contract-projector", "contract:conditional-consumer-applicability", "contract:consumer-applicability-matrix", "contract:native-context-version", "decision:observer-gap", "decision:wpra-applicability", "decision:implementation-readiness-applicability", "decision:task-session-applicability", "decision:context-builder-applicability", "decision:dispatch-applicability", "decision:goal-applicability", "decision:observer-applicability", "dependency:wpra-readiness", "dependency:task-context-route", "risk:false-observer-closure", "workflow:project-consumer-contracts"],
        "architecture:migration-rollout": ["component:plan-migration-validator", "contract:plan-source-v2", "risk:historical-plan-activation"],
        "ux-plan": ["component:plan-view-projector", "contract:work-pack-navigation"],
        "validation-contracts": ["component:plan-source-validator", "component:plan-bundle-admission-validator", "component:plan-evidence-resolver", "contract:plan-bundle-admission", "contract:conditional-consumer-applicability", "contract:consumer-applicability-matrix", "contract:native-context-version"],
    }
    for fact_id, output_id in signal_output.items():
        output_fact_ids[output_id].append(fact_id)
    output_fact_ids = {key: sorted(set(values)) for key, values in output_fact_ids.items()}

    pairs = sorted(validator.expected_application_pairs(closure, selection))
    concern_by_id = {item["concern_id"]: item for item in selection["concerns"]}
    input_by_id = {item["input_id"]: item for item in closure["input_catalog"]}
    witness_by_id = {
        item["witness_id"]: item
        for item in closure["selection_inputs"]["planned_witness_requirements"]
    }
    witness_targets = {
        "witness:deterministic-replay": ["component:plan-graph-compiler", "component:plan-view-projector", "component:plan-bundle-producer"],
        "witness:consumer-rehearsal": output_fact_ids["architecture:integration-versioning"],
        "witness:migration-compatibility": output_fact_ids["architecture:migration-rollout"],
        "witness:distill-v1": ["contract:plan-bundle-admission", "component:plan-bundle-admission-validator"],
        "witness:work-pack-navigation": output_fact_ids["ux-plan"],
        "witness:native-context-version": ["contract:native-context-version", "component:execution-contract-projector"],
    }
    applications: list[dict[str, Any]] = []
    for subject_kind, subject_id in pairs:
        fact_ids: list[str]
        disposition = "satisfied"
        evidence_refs: list[dict[str, Any]] = []
        rationale = "The Plan successor fact registry preserves this exact W1 obligation."
        if subject_kind == "selection-concern":
            concern = concern_by_id[subject_id]
            if concern["disposition"] == "not-applicable-with-rationale":
                disposition = "not-applicable-with-evidence"
                fact_ids = []
                evidence_refs = [closure_ref]
                rationale = concern["rationale"]
            else:
                fact_ids = output_fact_ids[concern["output_id"]]
                rationale = concern["rationale"]
        elif subject_kind == "selected-output":
            fact_ids = (
                sorted(item["fact_id"] for item in facts)
                if subject_id == "architecture"
                else output_fact_ids[subject_id]
            )
            rationale = "This selected output owns the listed concrete Plan successor facts."
        elif subject_kind == "scope-signal":
            fact_ids = [signal_fact_ids[(subject_kind, subject_id)]]
            rationale = "This fact is the lossless typed projection of the exact W1 signal."
        elif subject_kind == "planned-witness":
            fact_ids = witness_targets[subject_id]
            rationale = "This planned witness targets the facts needed to test its W1 claim."
        elif subject_kind == "input":
            path = input_by_id[subject_id]["source_ref"]["path"]
            if "signal-observer" in path:
                fact_ids = ["decision:observer-gap", "risk:false-observer-closure", "contract:conditional-consumer-applicability"]
            elif "context-builder" in path or "native-context" in path:
                fact_ids = ["component:execution-contract-projector", "contract:native-context-version", "dependency:task-context-route"]
            elif any(token in path for token in ("task-session", "implementation-readiness", "work-pack-readiness-audit", "dispatch-spec", "root-goal")):
                fact_ids = ["component:execution-contract-projector", "contract:conditional-consumer-applicability", "dependency:wpra-readiness"]
            elif "templates/work-pack.md" in path:
                fact_ids = ["component:plan-view-projector", "contract:work-pack-navigation"]
            elif "DEFINITIONS.json" in path:
                fact_ids = ["contract:plan-source-v2", "decision:single-plan-source"]
            else:
                fact_ids = common_ids
        else:
            text = subject_id.lower()
            if "observer" in text:
                fact_ids = ["decision:observer-gap", "risk:false-observer-closure"]
            elif "native-context" in text:
                fact_ids = ["contract:native-context-version", "component:execution-contract-projector"]
            elif "consumer" in text or "integration" in text:
                fact_ids = ["contract:conditional-consumer-applicability", "component:execution-contract-projector"]
            elif "migration" in text or "work-pack" in text:
                fact_ids = ["component:plan-migration-validator", "contract:work-pack-navigation", "risk:historical-plan-activation"]
            else:
                fact_ids = common_ids
        applications.append(
            {
                "subject_kind": subject_kind,
                "subject_id": subject_id,
                "disposition": disposition,
                "fact_ids": sorted(set(fact_ids)),
                "evidence_refs": evidence_refs,
                "decision_ref": None,
                "rationale": rationale,
            }
        )

    refs_by_fact: dict[str, list[dict[str, str]]] = {item["fact_id"]: [] for item in facts}
    for application in applications:
        pair = requirement(application["subject_kind"], application["subject_id"])
        for fact_id in application["fact_ids"]:
            refs_by_fact[fact_id].append(pair)
    for fact in facts:
        refs = refs_by_fact[fact["fact_id"]]
        if not refs:
            raise ValueError(f"fact has no W1 requirement: {fact['fact_id']}")
        fact["requirement_refs"] = sorted(refs, key=lambda item: (item["subject_kind"], item["subject_id"]))

    projected_views: dict[str, Any] = {}
    view_keys = [
        "context",
        "high_level_structure",
        "low_level_components",
        "workflow_process",
        "decision_flow",
        "dependency_interface",
    ]
    for key, rule in zip(view_keys, profile["view_rules"]):
        ids = sorted(
            item["fact_id"]
            for item in facts
            if item["fact_kind"] in rule["allowed_fact_kinds"]
        )
        projected_views[key] = {
            "view_id": rule["view_id"],
            "applicability": "applicable",
            "fact_ids": ids,
            "na_evidence_refs": [],
        }

    selected_outputs = sorted(selection["selected_outputs"])
    companions = [
        {
            "output_id": output_id,
            "fact_ids": output_fact_ids[output_id],
            "requirement_refs": [requirement("selected-output", output_id)],
        }
        for output_id in selected_outputs
        if output_id != "architecture"
    ]
    term_map = {
        "Invoke Plan": ["system:plan-successor"],
        "Plan authoring source": ["contract:plan-source-v2"],
        "Work Pack": ["contract:work-pack-navigation", "component:plan-view-projector"],
        "Delivery slice": ["contract:plan-source-v2", "component:plan-graph-compiler"],
        "Implementation layer": ["contract:plan-source-v2", "component:plan-graph-compiler"],
        "Plan wave": ["contract:plan-source-v2", "workflow:project-plan-views"],
        "Plan task": ["contract:plan-source-v2", "workflow:project-plan-views"],
        "Smallest Working Unit": ["contract:plan-source-v2", "component:execution-contract-projector"],
        "Implementation detail contract": ["contract:plan-source-v2"],
        "Validation obligation": ["contract:plan-bundle-admission", "component:plan-bundle-admission-validator"],
        "Plan gate": ["workflow:admit-plan-bundle", "state:plan-blocked"],
        "Plan blocker": ["state:plan-blocked", "risk:false-observer-closure"],
        "Plan gap": ["decision:observer-gap", "risk:false-observer-closure"],
        "Execution entry": ["component:execution-contract-projector", "contract:conditional-consumer-applicability"],
        "Execution Pack": ["component:plan-view-projector", "component:execution-contract-projector"],
        "Plan candidate bundle": ["component:plan-bundle-producer", "contract:plan-bundle-admission"],
        "Plan bundle admission": ["component:plan-bundle-admission-validator", "contract:plan-bundle-admission"],
        "Plan evidence state": ["component:plan-evidence-resolver", "decision:external-lifecycle-state"],
    }
    definition_terms = [item["term"] for item in definitions["definitions"]]
    missing_terms = sorted(set(definition_terms) - set(term_map))
    if missing_terms:
        raise ValueError(f"unmapped admitted definition terms: {missing_terms}")

    witness_text = {
        "witness:deterministic-replay": ("Compile the same exact Plan source twice.", "Both runs produce the same ordered files and bytes."),
        "witness:consumer-rehearsal": ("Run every applicable machine-backed consumer in no-effect mode and verify negative evidence for every inapplicable consumer.", "All applicable rehearsals pass and no consumer is silently skipped."),
        "witness:migration-compatibility": ("Validate historical v1 Plan material and attempt to use it for a new PASS.", "Historical material validates read-only but cannot establish successor admission."),
        "witness:distill-v1": ("Run Distill with the four exact v1 contracts against the W2 candidate.", "Distill identifies one coherent unit or returns an explicit gap without substituting v2 evidence."),
        "witness:work-pack-navigation": ("Render WORK-PACK.md from the source and inspect objective, slice, wave, task, gate, blocker, gap, and next-action navigation.", "A plan coordinator can find every required item and the view contains no independent authored meaning."),
        "witness:native-context-version": ("Project one contract without transient outputs and one with a nonempty transient set.", "The first uses 1.2.0, the second uses 1.3.0, and mismatches are rejected."),
    }
    planned_witnesses = []
    application_by_pair = {
        (item["subject_kind"], item["subject_id"]): item for item in applications
    }
    for witness_id, witness in sorted(witness_by_id.items()):
        input_text, expected_text = witness_text[witness_id]
        planned_witnesses.append(
            {
                "witness_id": witness_id,
                "claim_id": witness["claim_id"],
                "concern_id": witness["concern_id"],
                "polarity": "positive",
                "target_fact_ids": application_by_pair[("planned-witness", witness_id)]["fact_ids"],
                "input_or_violation": input_text,
                "expected_result": expected_text,
                "execution_owner": "plan-work-pack-owner",
                "execution_phase": "validation",
                "evidence_state": "planned-contract",
            }
        )

    full_source = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-source/v2",
        "schema_version": "invoke.design-source.v2",
        "source_id": "design-source:derived",
        "target_id": TARGET,
        "activation_kind": "normal",
        "profile_binding": {
            "profile_id": "invoke.generic-design-baseline.v1",
            "profile_ref": exact(profile_path, repo),
        },
        "upstream_bindings": {
            "design_input_production_receipt_ref": exact(w1 / "DESIGN-INPUT-PRODUCTION-RECEIPT.json", repo),
            "design_input_closure_ref": closure_ref,
            "design_input_closure_receipt_ref": exact(w1 / "DESIGN-INPUT-CLOSURE-RECEIPT.json", repo),
            "scope_manifest_ref": exact(w1 / "DESIGN-SCOPE-MANIFEST.json", repo),
            "denominator_receipt_ref": exact(w1 / "DESIGN-DENOMINATOR-RECEIPT.json", repo),
            "selection_result_ref": exact(w1 / "DESIGN-SELECTION-RESULT.json", repo),
        },
        "design_kind": {
            "kind": "greenfield",
            "determination_ref": exact(args.no_prior.resolve(), repo),
        },
        "applications": applications,
        "facts": sorted(facts, key=lambda item: item["fact_id"]),
        "views": projected_views,
        "selected_outputs": selected_outputs,
        "selected_companions": companions,
        "glossary_application": {
            "source_glossary_ref": exact(args.definitions.resolve(), repo),
            "mappings": [
                {"term": term, "fact_ids": sorted(term_map[term])}
                for term in definition_terms
            ],
            "unmapped_terms": [],
        },
        "planned_witnesses": planned_witnesses,
        "unresolved_gaps": [
            {
                "gap_id": "gap:signal-observer-machine-contract",
                "severity": "flag",
                "owner": "signal-observer-owner",
                "repair_route": "Add and admit a Signal Observer schema, deterministic projector or validator, and no-append fixture before claiming observer consumer closure.",
                "effect": "Plan bundle admission may proceed only without an observer-closure claim; observability-configured execution remains deferred.",
            }
        ],
        "layering": {
            "kind": "seed",
            "decision": "The mandatory authoring vertical is Plan source validation, normalized graph compilation, separate human-view and consumer-contract projection, bundle production, and independent admission. PlanEvidenceResolver and PlanMigrationValidator are conditional boundary adapters outside that stage sequence; readiness and execution remain later external evidence chains.",
            "minimum_unit": "One exact Plan source through one normalized graph, separately owned human and consumer projections, byte-identical bundle replay, and no-effect rehearsal or negative evidence for every consumer applicability row.",
        },
        "template_selection": {
            "selected_profile_id": "invoke.generic-design-baseline.v1",
            "evidence_ref": closure_ref,
        },
        "dispatch_trace": {
            "techniques": [
                "exact-binding",
                "schema-first-source",
                "deterministic-projection",
                "conditional-consumer-closure",
                "independent-replay-admission",
            ],
            "evidence_ref": exact(repo / "arcanum/development/invoke-plan-successor-design/DISTILL-BALANCER-BLOCK-V6.json", repo),
        },
        "distill_contract": {
            "classification": "required",
            "validator_owner": "distill",
            "coherent_unit_candidate": "One Plan artifact-authoring vertical from canonical source through independent admission, excluding readiness and execution outcomes.",
            "split_pressure_question": "Would splitting the source, normalized graph, views, consumer projections, or admission break deterministic meaning or allow one projection to bypass exact source binding?",
            "expected_receipt": "DISTILL-RECEIPT.json",
        },
        "transport_policy": {
            "append_existing_only": True,
            "upstream_mutation": False,
            "targets": [],
        },
        "next_route": "design-bundle-production",
        "authority_effect": "none",
        "source_digest": "0" * 64,
    }

    authored = json.loads(json.dumps(full_source, ensure_ascii=False))
    for pointer in (
        "/$schema",
        "/schema_version",
        "/source_id",
        "/activation_kind",
        "/profile_binding/profile_id",
        "/template_selection/selected_profile_id",
        "/transport_policy/append_existing_only",
        "/transport_policy/upstream_mutation",
        "/transport_policy/targets",
        "/next_route",
        "/authority_effect",
        "/source_digest",
    ):
        remove_pointer(authored, pointer)
    evidence_paths = strip_exact_refs(authored)
    request = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-source-v2-authoring-request/v1",
        "schema_version": "invoke.cli-authoring-request.v1",
        "mode": "design",
        "stage": "source",
        "document": authored,
        "evidence_paths": evidence_paths,
    }
    output.write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": output.as_posix(),
                "application_count": len(applications),
                "fact_count": len(facts),
                "witness_count": len(planned_witnesses),
                "evidence_binding_count": len(evidence_paths),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
