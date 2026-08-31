#!/usr/bin/env python3
"""Independently validate one staged W2 Design candidate against its W1 bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from project_design_artifact import (  # noqa: E402
    POLICY_PATH,
    PROCESS_PATH,
    PROFILE_PATH,
    canonical_bytes,
    digest_without,
    exact_ref,
    load_json,
    project_design_artifact,
)
from design_stage_contract import OUTPUTS as DESIGN_STAGE_OUTPUTS, validate_stage_receipt  # noqa: E402


IDENTITY = "invoke.validate-design-coherence.v1"
OWNER = "invoke-design-coherence-validator"
VALIDATOR_PATH = "arcanum/spells/invoke/scripts/validate_design_coherence.py"
W1_PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_input_bundle.py"
SIGNAL_MAP = {
    "human_actors": ("actor", "actor_id", ["natural_person", "reads", "decides", "acts", "recovers", "navigates", "assistive_operation", "surfaces"]),
    "rendered_surfaces": ("rendered-surface", "surface_id", ["modality", "semantic_contract_ref", "semantic_change"]),
    "interfaces": ("interface", "interface_id", ["kind", "peer", "direction", "contract_ref"]),
    "stores": ("store", "store_id", ["authority", "data_classes", "writers"]),
    "queues": ("queue", "queue_id", ["producers", "consumers", "ordering"]),
    "writers": ("writer", "writer_id", ["targets", "concurrency"]),
    "normative_rules": ("normative-rule", "rule_id", ["verb", "subject", "object", "enforcement_hint"]),
    "effects": ("effect", "effect_id", ["reversible", "external", "privileged"]),
    "data_and_log_sinks": ("data-log-sink", "sink_id", ["data_classes", "retention_hint"]),
    "deployment_targets": ("deployment", "deployment_id", ["environment", "release_mode"]),
    "compatibility_boundaries": ("compatibility-boundary", "boundary_id", ["old_contract", "new_contract"]),
    "quality_claims": ("quality-claim", "claim_id", ["source_kind", "threshold_or_tradeoff", "required"]),
    "acceptance_and_readiness_claims": ("acceptance-readiness-claim", "claim_id", ["selector", "evidence_state"]),
}


class ContractFailure(ValueError):
    def __init__(self, code: str, message: str, selector: str | None = None, route: str = "repair-design-source"):
        super().__init__(message)
        self.code = code
        self.selector = selector
        self.route = route


def schema_store(schema_dir: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in schema_dir.glob("*.schema.json"):
        try:
            schema = load_json(path)
        except (ValueError, json.JSONDecodeError):
            continue
        if "$id" in schema:
            result[schema["$id"]] = schema
    return result


def schema_errors(document: dict[str, Any], schema: dict[str, Any], store: dict[str, dict[str, Any]]) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store)
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema, resolver=resolver).iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def safe_path(root: Path, label: str) -> Path:
    pure = PurePosixPath(label)
    if pure.is_absolute() or pure.as_posix() != label or "\\" in label or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise ContractFailure("SOURCE_PATH_UNSAFE", f"unsafe repository-relative path: {label}", label)
    current = root.resolve()
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ContractFailure("SOURCE_PATH_UNSAFE", f"symlink path component is forbidden: {label}", label)
    try:
        current.relative_to(root.resolve())
    except ValueError as error:
        raise ContractFailure("SOURCE_PATH_UNSAFE", f"path escapes repository: {label}", label) from error
    return current


def verify_ref(root: Path, ref: dict[str, Any]) -> Path:
    path = safe_path(root, ref["path"])
    if not path.is_file():
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", f"bound file is unavailable: {ref['path']}", ref["path"], "repair-w1-input")
    data = path.read_bytes()
    if len(data) != ref["size"] or hashlib.sha256(data).hexdigest() != ref["sha256"]:
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", f"bound file digest or size drifted: {ref['path']}", ref["path"], "repair-w1-input")
    return path


def ref_tuple(value: dict[str, Any]) -> tuple[str, str, int]:
    return value["path"], value["sha256"], value["size"]


def collect_exact_refs(value: Any) -> set[tuple[str, str, int]]:
    refs: set[tuple[str, str, int]] = set()
    if isinstance(value, dict):
        if {"path", "sha256", "size"} <= value.keys():
            refs.add((value["path"], value["sha256"], value["size"]))
        for child in value.values():
            refs.update(collect_exact_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(collect_exact_refs(child))
    return refs


def check_self_digest(document: dict[str, Any], field: str, code: str, route: str = "repair-design-source") -> None:
    if document.get(field) != digest_without(document, field):
        raise ContractFailure(code, f"self digest mismatch: {field}", field, route)


def pair(kind: str, identifier: str) -> tuple[str, str]:
    return kind, identifier


def expected_application_pairs(closure: dict[str, Any], selection: dict[str, Any]) -> set[tuple[str, str]]:
    conditional = {item["input_id"]: item["outcome"] for item in closure["conditional_input_resolutions"]}
    expected: set[tuple[str, str]] = set()
    for item in closure["input_catalog"]:
        expected.add(pair("input", item["input_id"]))
    expected.update(pair("conditional-resolution", item["input_id"]) for item in closure["conditional_input_resolutions"])
    expected.update(pair("constraint", item["obligation_id"]) for item in closure["constraints"])
    expected.update(pair("invariant", item["obligation_id"]) for item in closure["invariants"])
    expected.update(pair("prior-decision", item["decision_id"]) for item in closure["prior_decisions"])
    expected.update(pair("resolved-conflict", item["conflict_id"]) for item in closure["input_conflicts"] if item["resolution_status"] == "resolved")
    for signals in closure["scope_signals"].values():
        expected.update(pair("scope-signal", item["signal_id"]) for item in signals)
    expected.update(pair("selection-concern", item["concern_id"]) for item in selection["concerns"])
    expected.update(pair("selected-output", item) for item in selection["selected_outputs"])
    expected.update(pair("planned-witness", item["witness_id"]) for item in closure["selection_inputs"]["planned_witness_requirements"])
    expected.add(pair("design-kind", f"design-kind:{closure['design_kind']['kind']}"))
    if closure["design_kind"]["kind"] == "evolution":
        expected.update(pair("evolution-delta", item) for item in closure["design_kind"]["declared_delta_ids"])
    return expected


def diagnostic(code: str, message: str, selector: str | None, index: int) -> dict[str, Any]:
    return {
        "diagnostic_id": f"w2-diagnostic:{index:03d}", "code": code, "message": message,
        "selector": selector, "owner": "design-author", "repair": "Repair the named Design source invariant and rerun W2.",
        "causal_blocker_ids": [],
    }


def validate_semantics(source: dict[str, Any], artifact: dict[str, Any], closure: dict[str, Any], closure_receipt: dict[str, Any], manifest: dict[str, Any], selection: dict[str, Any], profile: dict[str, Any], expected_artifact: dict[str, Any], repository_root: Path | None = None, schema_dir: Path | None = None) -> dict[str, list[dict[str, Any]]]:
    issues: dict[str, list[dict[str, Any]]] = {rule: [] for rule in [
        "rule:w1-entry", "rule:application-denominator", "rule:profile-closure", "rule:registry-integrity",
        "rule:view-projection", "rule:artifact-projection", "rule:contract-preservation", "rule:selection-closure", "rule:glossary-consistency",
        "rule:evolution-delta", "rule:plan-evidence-separation", "rule:authority-ceiling",
    ]}
    counter = 0
    def add(rule: str, code: str, message: str, selector: str | None = None) -> None:
        nonlocal counter
        counter += 1
        issues[rule].append(diagnostic(code, message, selector, counter))

    expected_pairs = expected_application_pairs(closure, selection)
    actual_pairs = [(item["subject_kind"], item["subject_id"]) for item in source["applications"]]
    if len(actual_pairs) != len(set(actual_pairs)):
        add("rule:application-denominator", "DESIGN_APPLICATION_DENOMINATOR_INVALID", "duplicate typed application pair")
    if set(actual_pairs) != expected_pairs:
        add("rule:application-denominator", "DESIGN_APPLICATION_DENOMINATOR_INVALID", f"application pair set mismatch: missing={sorted(expected_pairs-set(actual_pairs))}; extra={sorted(set(actual_pairs)-expected_pairs)}")
    applications = {(item["subject_kind"], item["subject_id"]): item for item in source["applications"]}
    conditional_outcomes = {item["input_id"]: item for item in closure["conditional_input_resolutions"]}
    for catalog_item in closure["input_catalog"]:
        application = applications.get(("input", catalog_item["input_id"]))
        excluded = catalog_item["classification"] == "excluded" or (catalog_item["classification"] == "conditional" and conditional_outcomes.get(catalog_item["input_id"], {}).get("outcome") == "excluded")
        if application is not None and excluded and (application["disposition"] != "not-applicable-with-evidence" or application["fact_ids"]):
            add("rule:application-denominator", "DESIGN_APPLICATION_DENOMINATOR_INVALID", f"excluded catalog input is not explicitly N/A: {catalog_item['input_id']}", catalog_item["input_id"])
        if application is not None and excluded:
            evidence = catalog_item.get("exclusion_evidence_ref") if catalog_item["classification"] == "excluded" else conditional_outcomes[catalog_item["input_id"]]["evidence_ref"]
            expected_evidence = (evidence["path"], evidence["sha256"], evidence["size"])
            if expected_evidence not in {ref_tuple(item) for item in application["evidence_refs"]}:
                add("rule:application-denominator", "DESIGN_APPLICATION_DENOMINATOR_INVALID", f"excluded catalog input lacks exact upstream exclusion evidence: {catalog_item['input_id']}", catalog_item["input_id"])
        if application is not None and not excluded and application["disposition"] == "not-applicable-with-evidence":
            add("rule:application-denominator", "DESIGN_APPLICATION_DENOMINATOR_INVALID", f"applicable catalog input was discarded as N/A: {catalog_item['input_id']}", catalog_item["input_id"])
    for resolution in closure["conditional_input_resolutions"]:
        application = applications.get(("conditional-resolution", resolution["input_id"]))
        if application is not None and resolution["outcome"] == "excluded":
            expected_evidence = (resolution["evidence_ref"]["path"], resolution["evidence_ref"]["sha256"], resolution["evidence_ref"]["size"])
            if application["disposition"] != "not-applicable-with-evidence" or application["fact_ids"] or expected_evidence not in {ref_tuple(item) for item in application["evidence_refs"]}:
                add("rule:application-denominator", "DESIGN_APPLICATION_DENOMINATOR_INVALID", f"conditional exclusion is not exactly preserved: {resolution['input_id']}", resolution["input_id"])

    fact_ids = [item["fact_id"] for item in source["facts"]]
    facts = {item["fact_id"]: item for item in source["facts"]}
    if len(fact_ids) != len(facts):
        add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", "duplicate fact_id")
    for app_pair, app in applications.items():
        for fact_id in app["fact_ids"]:
            if fact_id not in facts:
                add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"application references missing fact {fact_id}", f"{app_pair[0]}:{app_pair[1]}")
    all_view_ids: set[str] = set()
    for view in source["views"].values():
        all_view_ids.update(view["fact_ids"])
    companion_ids = {fact_id for item in source["selected_companions"] for fact_id in item["fact_ids"]}
    for fact in source["facts"]:
        refs = [(item["subject_kind"], item["subject_id"]) for item in fact["requirement_refs"]]
        if len(refs) != len(set(refs)) or any(item not in expected_pairs for item in refs):
            add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"invalid or duplicate requirement refs for {fact['fact_id']}", fact["fact_id"])
        if any(fact["fact_id"] not in applications.get(item, {}).get("fact_ids", []) for item in refs):
            add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"fact/application provenance is not reciprocal for {fact['fact_id']}", fact["fact_id"])
        if fact["fact_id"] not in all_view_ids and fact["fact_id"] not in companion_ids:
            add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"orphan fact {fact['fact_id']}", fact["fact_id"])
        attributes = fact["attributes"]
        edge_expectations: list[tuple[str, str | None]] = []
        if fact["fact_kind"] == "relationship": edge_expectations = [(attributes["from_id"], None), (attributes["to_id"], None)]
        elif fact["fact_kind"] == "component": edge_expectations = ([(attributes["parent_component_id"], "component")] if attributes["parent_component_id"] else []) + [(item, "contract") for item in attributes["contract_ids"]]
        elif fact["fact_kind"] == "workflow-step":
            operator_id = attributes["actor_or_component_id"]
            if operator_id not in facts or facts[operator_id]["fact_kind"] not in {"actor", "component"}:
                add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"workflow operator is not an actor or component: {fact['fact_id']} -> {operator_id}", fact["fact_id"])
            edge_expectations = [(item, "workflow-step") for item in attributes["next_step_ids"]]
        elif fact["fact_kind"] == "state": edge_expectations = [(attributes["subject_id"], None)] + [(item, "state") for item in attributes["allowed_next_state_ids"]]
        elif fact["fact_kind"] == "decision": edge_expectations = [(item["next_id"], None) for item in attributes["outcomes"] if item["next_id"]]
        elif fact["fact_kind"] == "dependency": edge_expectations = [(attributes["consumer_id"], None), (attributes["target_id"], None)]
        for target_id, expected_kind in edge_expectations:
            if target_id not in facts or (expected_kind is not None and facts[target_id]["fact_kind"] != expected_kind):
                add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"dangling or wrong-kind edge {fact['fact_id']} -> {target_id}", fact["fact_id"])
    for application_pair in expected_pairs:
        application_fact_ids = set(applications.get(application_pair, {}).get("fact_ids", []))
        reciprocal_fact_ids = {item["fact_id"] for item in source["facts"] if {tuple((ref["subject_kind"], ref["subject_id"])) for ref in item["requirement_refs"]}.__contains__(application_pair)}
        if application_fact_ids != reciprocal_fact_ids:
            add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"application/fact reciprocity mismatch for {application_pair[0]}:{application_pair[1]}")

    expected_kinds = profile["fact_kinds"]
    if len(expected_kinds) != len(set(expected_kinds)):
        add("rule:profile-closure", "DESIGN_PROFILE_CLOSURE_INVALID", "profile fact kind denominator contains duplicates")
    core = profile["core_requirements"]
    if [item["fact_kind"] for item in core] != expected_kinds:
        add("rule:profile-closure", "DESIGN_PROFILE_CLOSURE_INVALID", "profile core requirement denominator/order differs from fact kinds")
    counts = Counter(item["fact_kind"] for item in source["facts"])
    for item in core:
        if counts[item["fact_kind"]] < item["minimum"]:
            add("rule:profile-closure", "DESIGN_PROFILE_CLOSURE_INVALID", f"minimum {item['fact_kind']} facts not met")
    view_rules = {item["view_id"]: set(item["allowed_fact_kinds"]) for item in profile["view_rules"]}
    if [item["view_id"] for item in profile["view_rules"]] != profile["view_order"]:
        add("rule:profile-closure", "DESIGN_PROFILE_CLOSURE_INVALID", "profile view rule order differs from view denominator")
    for view in source["views"].values():
        if len(view["fact_ids"]) != len(set(view["fact_ids"])):
            add("rule:view-projection", "DESIGN_VIEW_PROJECTION_INVALID", "duplicate view fact IDs", view["view_id"])
        for fact_id in view["fact_ids"]:
            if fact_id not in facts or facts[fact_id]["fact_kind"] not in view_rules.get(view["view_id"], set()):
                add("rule:view-projection", "DESIGN_VIEW_PROJECTION_INVALID", f"illegal view fact {fact_id}", view["view_id"])
        if view["applicability"] == "not-applicable-with-evidence" and any(item["fact_kind"] in view_rules.get(view["view_id"], set()) for item in source["facts"]):
            add("rule:view-projection", "DESIGN_VIEW_PROJECTION_INVALID", "view claims N/A despite available allowed facts", view["view_id"])

    for signal_class, signals in closure["scope_signals"].items():
        fact_kind, identity_key, fields = SIGNAL_MAP[signal_class]
        for signal in signals:
            app = applications.get(("scope-signal", signal["signal_id"]))
            candidates = [] if app is None else [facts[item] for item in app["fact_ids"] if item in facts and facts[item]["fact_kind"] == fact_kind and facts[item]["fact_id"] == signal[identity_key]]
            def equivalent(left: Any, right: Any) -> bool:
                return sorted(left) == sorted(right) if isinstance(left, list) and isinstance(right, list) else left == right
            if len(candidates) != 1 or (candidates and any(not equivalent(candidates[0]["attributes"].get(field), signal[field]) for field in fields)):
                add("rule:registry-integrity", "DESIGN_FACT_REGISTRY_INVALID", f"lossy {signal_class} projection for {signal['signal_id']}", signal["signal_id"])

    if source["target_id"] != closure["target"]["id"] or manifest["target_id"] != source["target_id"]:
        add("rule:w1-entry", "DESIGN_W1_ENTRY_INVALID", "target identity differs across W1 and W2")
    if set(source["selected_outputs"]) != set(selection["selected_outputs"]) or len(source["selected_outputs"]) != len(set(source["selected_outputs"])):
        add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", "selected outputs differ from W1 selection")
    selected_concerns = {item["concern_id"]: item for item in selection["concerns"]}
    if {item["concern_id"] for item in artifact["concern_trace"]} != set(selected_concerns):
        add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", "concern trace denominator mismatch")
    selected_companion_ids = {item for item in selection["selected_outputs"] if item != "architecture"}
    companion_output_ids = [item["output_id"] for item in source["selected_companions"]]
    if len(companion_output_ids) != len(set(companion_output_ids)) or set(companion_output_ids) != selected_companion_ids:
        add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", "selected companion denominator mismatch")
    for concern in selection["concerns"]:
        application = applications.get(("selection-concern", concern["concern_id"]))
        if application is None:
            continue
        if concern["disposition"] == "not-applicable-with-rationale" and (application["disposition"] != "not-applicable-with-evidence" or application["fact_ids"]):
            add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", f"N/A concern drives architecture facts: {concern['concern_id']}", concern["concern_id"])
        if concern["disposition"] == "required" and application["disposition"] == "not-applicable-with-evidence":
            add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", f"required concern is discarded as N/A: {concern['concern_id']}", concern["concern_id"])
    companion_by_output = {item["output_id"]: item for item in source["selected_companions"]}
    for output_id in selection["selected_outputs"]:
        application = applications.get(("selected-output", output_id))
        if application is None:
            continue
        expected_fact_ids = set(facts) if output_id == "architecture" else set(companion_by_output.get(output_id, {}).get("fact_ids", []))
        if set(application["fact_ids"]) != expected_fact_ids:
            add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", f"selected output fact coverage mismatch: {output_id}", output_id)

    witness_ids = [item["witness_id"] for item in source["planned_witnesses"]]
    witness_by_id = {item["witness_id"]: item for item in source["planned_witnesses"]}
    upstream_witness = {item["witness_id"]: item for item in closure["selection_inputs"]["planned_witness_requirements"]}
    if len(witness_ids) != len(set(witness_ids)) or set(witness_by_id) != set(upstream_witness):
        add("rule:plan-evidence-separation", "DESIGN_PLAN_EVIDENCE_OVERCLAIM", "planned witness denominator mismatch")
    for witness_id in set(witness_by_id) & set(upstream_witness):
        if any(witness_by_id[witness_id][key] != upstream_witness[witness_id][key] for key in ["claim_id", "concern_id", "evidence_state"]):
            add("rule:plan-evidence-separation", "DESIGN_PLAN_EVIDENCE_OVERCLAIM", f"planned witness binding drift: {witness_id}", witness_id)

    mappings = source["glossary_application"]["mappings"]
    if len([item["term"] for item in mappings]) != len({item["term"] for item in mappings}):
        add("rule:glossary-consistency", "DESIGN_GLOSSARY_CONFLICT", "duplicate glossary term mapping")
    for item in mappings:
        if any(fact_id not in facts for fact_id in item["fact_ids"]):
            add("rule:glossary-consistency", "DESIGN_GLOSSARY_CONFLICT", f"glossary mapping references missing fact: {item['term']}")
    if source["glossary_application"]["unmapped_terms"]:
        add("rule:glossary-consistency", "DESIGN_GLOSSARY_CONFLICT", "unmapped glossary terms remain")

    kind = closure["design_kind"]["kind"]
    if source["design_kind"]["kind"] != kind or closure_receipt["prior_design_determination"]["kind"] != kind:
        add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", "Design kind differs from W1 determination")
    if kind == "greenfield":
        expected_ref = {k: closure["design_kind"]["no_prior_design_determination_ref"][k] for k in ["path", "sha256", "size"]}
        if source["design_kind"].get("determination_ref") != expected_ref:
            add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", "greenfield determination binding mismatch")
    else:
        predecessor: dict[str, Any] | None = None
        artifact_ref = source["design_kind"].get("predecessor_artifact_ref")
        receipt_ref = source["design_kind"].get("predecessor_stage_receipt_ref")
        closure_artifact_value = closure["design_kind"].get("prior_design_artifact_ref")
        closure_receipt_value = closure["design_kind"].get("prior_design_stage_receipt_ref")
        closure_artifact_ref = ({key: closure_artifact_value[key] for key in ["path", "sha256", "size"]} if isinstance(closure_artifact_value, dict) and all(key in closure_artifact_value for key in ["path", "sha256", "size"]) else None)
        closure_receipt_ref = ({key: closure_receipt_value[key] for key in ["path", "sha256", "size"]} if isinstance(closure_receipt_value, dict) and all(key in closure_receipt_value for key in ["path", "sha256", "size"]) else None)
        if closure_artifact_ref is None or closure_receipt_ref is None:
            add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", "W1 evolution closure lacks exact predecessor artifact and v2 stage receipt refs")
        elif artifact_ref != closure_artifact_ref or receipt_ref != closure_receipt_ref:
            add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", "W1 and W2 predecessor bindings differ")
        elif repository_root is None or schema_dir is None:
            add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", "a real v2 predecessor requires repository-root and installed-schema validation")
        else:
            try:
                prior_receipt_path = verify_ref(repository_root, receipt_ref)
                prior_artifact_path = verify_ref(repository_root, artifact_ref)
                prior_receipt = load_json(prior_receipt_path)
                contract_errors = validate_stage_receipt(prior_receipt, repository_root, schema_dir, prior_receipt_path.parent)
                if contract_errors:
                    raise ContractFailure("EVOLUTION_INVALID", "; ".join(contract_errors), receipt_ref["path"])
                expected_prior_artifact = {
                    "path": (PurePosixPath(receipt_ref["path"]).parent / DESIGN_STAGE_OUTPUTS[0][1]).as_posix(),
                    "sha256": prior_receipt["outputs"][0]["sha256"],
                    "size": prior_receipt["outputs"][0]["size"],
                }
                if artifact_ref != expected_prior_artifact or prior_receipt["target_id"] != source["target_id"]:
                    raise ContractFailure("EVOLUTION_INVALID", "v2 predecessor output or target binding differs", artifact_ref["path"])
                predecessor = load_json(prior_artifact_path)
                store = schema_store(schema_dir)
                errors = schema_errors(predecessor, store["https://arcanum.dev/schemas/invoke/design-artifact/v1"], store)
                if errors or predecessor.get("artifact_digest") != digest_without(predecessor, "artifact_digest"):
                    raise ContractFailure("EVOLUTION_INVALID", "; ".join(errors[:5]) or "predecessor artifact digest mismatch", artifact_ref["path"])
                determination_refs = closure_receipt["prior_design_determination"]["evidence_refs"]
                if receipt_ref not in determination_refs or artifact_ref not in determination_refs:
                    raise ContractFailure("EVOLUTION_INVALID", "W1 determination does not exact-bind both predecessor files", "prior_design_determination")
            except (OSError, ValueError, KeyError, json.JSONDecodeError, ContractFailure) as error:
                add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", f"v2 predecessor validation failed: {error}")
        deltas = source["design_kind"].get("deltas", [])
        if {item["delta_id"] for item in deltas} != set(closure["design_kind"]["declared_delta_ids"]):
            add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", "evolution delta denominator mismatch")
        for item in deltas:
            valid = ((item["change"] == "added" and item["prior_fact_id"] is None and item["current_fact_id"] is not None and item["decision_ref"] is None) or
                     (item["change"] == "removed" and item["prior_fact_id"] is not None and item["current_fact_id"] is None) or
                     (item["change"] == "preserved" and item["prior_fact_id"] is not None and item["current_fact_id"] is not None and item["decision_ref"] is None) or
                     (item["change"] == "modified" and item["prior_fact_id"] is not None and item["current_fact_id"] is not None and item["decision_ref"] is not None))
            if not valid:
                add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", f"illegal evolution delta shape: {item['delta_id']}", item["delta_id"])
            if predecessor is not None:
                prior_ids = {fact["fact_id"] for fact in predecessor["facts"]}
                current_ids = set(facts)
                if item["prior_fact_id"] is not None and item["prior_fact_id"] not in prior_ids:
                    add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", f"delta cites absent predecessor fact: {item['delta_id']}", item["delta_id"])
                if item["current_fact_id"] is not None and item["current_fact_id"] not in current_ids:
                    add("rule:evolution-delta", "DESIGN_EVOLUTION_DELTA_INCOMPLETE", f"delta cites absent current fact: {item['delta_id']}", item["delta_id"])

    for app in source["applications"]:
        if app["disposition"] == "block":
            add("rule:contract-preservation", "DESIGN_CONTRACT_PRESERVATION_INVALID", "blocking source application", app["subject_id"])
        if app["subject_kind"] in {"constraint", "invariant"} and app["disposition"] == "changed-by-exact-decision":
            eligible = [item for item in closure["prior_decisions"] if item["status"] == "eligible-for-supersession" and ref_tuple({key: item["decision_ref"][key] for key in ["path", "sha256", "size"]}) == ref_tuple(app["decision_ref"])]
            if len(eligible) != 1:
                add("rule:contract-preservation", "DESIGN_CONTRACT_PRESERVATION_INVALID", "changed constraint or invariant lacks one eligible exact owner decision", app["subject_id"])
    if any(item["severity"] == "block" for item in source["unresolved_gaps"]):
        add("rule:contract-preservation", "DESIGN_CONTRACT_PRESERVATION_INVALID", "blocking unresolved Design gap")
    for companion in source["selected_companions"]:
        if any(fact_id not in facts for fact_id in companion["fact_ids"]) or any((ref["subject_kind"], ref["subject_id"]) not in expected_pairs for ref in companion["requirement_refs"]):
            add("rule:selection-closure", "DESIGN_SELECTION_CLOSURE_INVALID", f"invalid companion references: {companion['output_id']}")
    for witness in source["planned_witnesses"]:
        if any(fact_id not in facts for fact_id in witness["target_fact_ids"]):
            add("rule:plan-evidence-separation", "DESIGN_PLAN_EVIDENCE_OVERCLAIM", f"witness references missing fact: {witness['witness_id']}")
        application = applications.get(("planned-witness", witness["witness_id"]))
        if application is not None and set(application["fact_ids"]) != set(witness["target_fact_ids"]):
            add("rule:plan-evidence-separation", "DESIGN_PLAN_EVIDENCE_OVERCLAIM", f"witness application coverage mismatch: {witness['witness_id']}")
    if artifact != expected_artifact:
        add("rule:artifact-projection", "DESIGN_ARTIFACT_PROJECTION_MISMATCH", "artifact differs from deterministic source projection")
    return issues


def validate_design_coherence(source_path: Path, artifact_path: Path, artifact_ref: dict[str, Any], root: Path, schema_dir: Path) -> dict[str, Any]:
    store = schema_store(schema_dir)
    source = load_json(source_path)
    artifact = load_json(artifact_path)
    source_ref = exact_ref(source_path, root)
    process_path, profile_path, policy_path = root / PROCESS_PATH, root / PROFILE_PATH, root / POLICY_PATH
    process, profile, policy = load_json(process_path), load_json(profile_path), load_json(policy_path)
    process_ref, profile_ref, policy_ref = exact_ref(process_path, root), exact_ref(profile_path, root), exact_ref(policy_path, root)
    for document, schema_id, field in [(source, "https://arcanum.dev/schemas/invoke/design-source/v1", "source_digest"), (artifact, "https://arcanum.dev/schemas/invoke/design-artifact/v1", "artifact_digest"), (profile, "https://arcanum.dev/schemas/invoke/design-profile/v1", "profile_digest"), (policy, "https://arcanum.dev/schemas/invoke/design-coherence-policy/v1", "policy_digest"), (process, "https://arcanum.dev/schemas/invoke/design-production-process/v1", "process_digest")]:
        errors = schema_errors(document, store[schema_id], store)
        if errors:
            raise ContractFailure("SOURCE_SCHEMA_INVALID", "; ".join(errors[:8]), schema_id, "repair-installed-contract" if document in [profile, policy, process] else "repair-design-source")
        check_self_digest(
            document,
            field,
            "SOURCE_DIGEST_MISMATCH",
            "repair-installed-contract" if document in [profile, policy, process] else "repair-design-source",
        )
    if source["profile_binding"] != {"profile_id": profile["profile_id"], "profile_ref": profile_ref}:
        raise ContractFailure("PROFILE_BINDING_MISMATCH", "source profile binding differs from installed profile", "profile_binding", "repair-installed-contract")

    refs = source["upstream_bindings"]
    w1_path = verify_ref(root, refs["design_input_production_receipt_ref"])
    w1 = load_json(w1_path)
    errors = schema_errors(w1, store["https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1"], store)
    if errors or w1.get("result") != "pass" or w1.get("activation_kind") != "normal" or w1.get("next_route") != "design-authoring":
        raise ContractFailure("W1_RECEIPT_INVALID", "; ".join(errors[:5]) or "W1 receipt is not normal PASS routed to Design", refs["design_input_production_receipt_ref"]["path"], "repair-w1-input")
    check_self_digest(w1, "receipt_digest", "W1_RECEIPT_INVALID")
    if w1["producer"]["sha256"] != exact_ref(root / W1_PRODUCER_PATH, root)["sha256"]:
        raise ContractFailure("W1_RECEIPT_INVALID", "W1 producer digest is not installed producer", W1_PRODUCER_PATH, "repair-w1-input")
    expected_names = ["DESIGN-INPUT-CLOSURE-RECEIPT.json", "DESIGN-SCOPE-MANIFEST.json", "DESIGN-DENOMINATOR-RECEIPT.json", "DESIGN-SELECTION-RESULT.json"]
    if [item["path"] for item in w1["outputs"]] != expected_names:
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", "W1 output inventory differs from exact contract", None, "repair-w1-input")
    binding_keys = ["design_input_closure_receipt_ref", "scope_manifest_ref", "denominator_receipt_ref", "selection_result_ref"]
    w1_parent = PurePosixPath(refs["design_input_production_receipt_ref"]["path"]).parent
    for key, output in zip(binding_keys, w1["outputs"]):
        verify_ref(root, refs[key])
        expected_path = (w1_parent / output["path"]).as_posix()
        if refs[key]["path"] != expected_path or refs[key]["sha256"] != output["sha256"] or refs[key]["size"] != output["size"]:
            raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", f"W1 output binding mismatch: {key}", key, "repair-w1-input")
    verify_ref(root, refs["design_input_closure_ref"])
    if ref_tuple(refs["design_input_closure_ref"]) != ref_tuple(w1["source_ref"]):
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", "W1 source/closure binding mismatch", "design_input_closure_ref", "repair-w1-input")

    closure = load_json(root / refs["design_input_closure_ref"]["path"])
    closure_receipt = load_json(root / refs["design_input_closure_receipt_ref"]["path"])
    manifest = load_json(root / refs["scope_manifest_ref"]["path"])
    denominator = load_json(root / refs["denominator_receipt_ref"]["path"])
    selection = load_json(root / refs["selection_result_ref"]["path"])
    live_documents = [
        (closure, "https://arcanum.dev/schemas/invoke/design-input-closure/v1"),
        (closure_receipt, "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1"),
        (manifest, "https://arcanum.dev/schemas/invoke/design-scope-manifest/1-0-0"),
        (denominator, "https://arcanum.dev/schemas/invoke/design-denominator-receipt/1-0-0"),
        (selection, "https://arcanum.dev/schemas/invoke/design-selection-result/1-0-0"),
    ]
    for document, schema_id in live_documents:
        errors = schema_errors(document, store[schema_id], store)
        if errors:
            raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", f"live W1 payload violates {schema_id}: {'; '.join(errors[:5])}", schema_id, "repair-w1-input")
    for document, field in [(closure, "closure_digest"), (closure_receipt, "receipt_digest"), (manifest, "input_digest"), (denominator, "receipt_digest"), (selection, "result_digest")]:
        check_self_digest(document, field, "W1_OUTPUT_BINDING_MISMATCH")
    if selection.get("verdict") != "pass" or selection.get("evidence_state") != "design-validator-pass" or not selection.get("fixed_point"):
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", "selection result is not fixed-point PASS", "selection_result_ref", "repair-w1-input")
    if w1["input_closure_receipt"] != closure_receipt or closure_receipt.get("activation_kind") != "normal" or closure_receipt.get("verdict") != "pass":
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", "embedded/live closure receipt mismatch or not normal PASS", "design_input_closure_receipt_ref", "repair-w1-input")
    if denominator.get("verdict") != "pass" or denominator.get("manifest_id") != manifest.get("manifest_id") or denominator.get("manifest_input_digest") != manifest.get("input_digest"):
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", "denominator is not PASS for the exact manifest", "denominator_receipt_ref", "repair-w1-input")
    if selection.get("manifest_id") != manifest.get("manifest_id") or selection.get("manifest_input_digest") != manifest.get("input_digest") or selection.get("denominator_receipt_digest") != denominator.get("receipt_digest") or selection.get("pass_1_digest") != selection.get("pass_2_digest"):
        raise ContractFailure("W1_OUTPUT_BINDING_MISMATCH", "selection does not bind the exact fixed-point manifest and denominator", "selection_result_ref", "repair-w1-input")
    expected_rule_digest = hashlib.sha256(canonical_bytes(policy["rule_order"])).hexdigest()
    if policy["rule_set_digest"] != expected_rule_digest or [item["rule_id"] for item in policy["rules"]] != policy["rule_order"]:
        raise ContractFailure("PROFILE_INVALID", "installed policy rule denominator/order/digest is inconsistent", POLICY_PATH, "repair-installed-contract")

    allowed_refs = collect_exact_refs(closure) | collect_exact_refs(closure_receipt) | {ref_tuple(item) for item in refs.values()} | {ref_tuple(profile_ref)}
    source_refs = collect_exact_refs(source)
    if not source_refs <= allowed_refs:
        raise ContractFailure("APPLICATION_INVALID", f"source introduces out-of-bound evidence refs: {sorted(source_refs-allowed_refs)}", None)
    expected_artifact = project_design_artifact(source, source_ref, process_ref, profile_ref, policy_ref, selection)
    issues = validate_semantics(source, artifact, closure, closure_receipt, manifest, selection, profile, expected_artifact, root, schema_dir)
    diagnostics = [item for rule in policy["rule_order"] for item in issues[rule]]
    evidence = [process_ref, profile_ref, policy_ref, refs["design_input_production_receipt_ref"], source_ref, artifact_ref]
    evaluated = []
    for rule_id in policy["rule_order"]:
        rule_issues = issues[rule_id]
        evaluated.append({"rule_id": rule_id, "status": "block" if rule_issues else "pass", "evidence_refs": copy.deepcopy(evidence), "causal_blocker_ids": [item["diagnostic_id"] for item in rule_issues]})
    verdict = "block" if diagnostics else "pass"
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1", "schema_version": "invoke.design-coherence-receipt.v1",
        "receipt_id": f"design-w2-coherence:{artifact['artifact_digest'][:24]}",
        "validator": {"identity": IDENTITY, "owner": OWNER, "path": VALIDATOR_PATH, "sha256": exact_ref(root / VALIDATOR_PATH, root)["sha256"]},
        "bindings": {"process_ref": process_ref, "profile_ref": profile_ref, "coherence_policy_ref": policy_ref, "design_input_production_receipt_ref": copy.deepcopy(refs["design_input_production_receipt_ref"]), "design_input_closure_ref": copy.deepcopy(refs["design_input_closure_ref"]), "design_input_closure_receipt_ref": copy.deepcopy(refs["design_input_closure_receipt_ref"]), "scope_manifest_ref": copy.deepcopy(refs["scope_manifest_ref"]), "denominator_receipt_ref": copy.deepcopy(refs["denominator_receipt_ref"]), "selection_result_ref": copy.deepcopy(refs["selection_result_ref"]), "design_source_ref": source_ref, "design_artifact_ref": artifact_ref},
        "policy_rule_ids": copy.deepcopy(policy["rule_order"]), "policy_rule_set_digest": policy["rule_set_digest"], "evaluated_rules": evaluated,
        "verdict": verdict, "diagnostics": diagnostics, "selection_evidence_state": "design-validator-pass",
        "coherence_state": verdict, "design_stage_state": "pending-bundle-closure" if verdict == "pass" else "ineligible",
        "plan_evidence_state": "plan-evidence-pending", "authority_effect": "none", "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    errors = schema_errors(receipt, store["https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1"], store)
    if errors:
        raise ContractFailure("COHERENCE_BLOCKED", "; ".join(errors[:8]), "coherence-receipt", "repair-installed-contract")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("artifact")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--schema-dir")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    artifact_path = Path(args.artifact)
    receipt = validate_design_coherence(Path(args.source), artifact_path, exact_ref(artifact_path, root), root, Path(args.schema_dir) if args.schema_dir else root / "arcanum/spells/invoke/schemas")
    output = Path(args.output)
    if not output.is_absolute() or output.exists() or output.is_symlink() or not output.parent.is_dir() or output.parent.is_symlink():
        raise SystemExit("output already exists")
    fd, temporary = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(receipt, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, output)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise
    return 0 if receipt["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
