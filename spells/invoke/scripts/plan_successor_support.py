#!/usr/bin/env python3
"""Shared deterministic support for Invoke Plan v2 production and admission."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

CONSUMERS = ["wpra", "implementation-readiness", "task-session", "context-builder", "dispatch-spec", "goal", "signal-observer"]


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON value is forbidden: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def semantic_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return sha_bytes(semantic_bytes(value))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def file_ref(path: Path, label: str | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": label or path.as_posix(), "sha256": sha_bytes(data), "size": len(data)}


def validate_schema(value: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    return [f"{label} at /{'/'.join(map(str, error.absolute_path))}: {error.message}" for error in sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: (list(item.absolute_path), item.message))]


def validate_ref(ref: dict[str, Any], repo_root: Path, label: str) -> tuple[Path | None, list[str]]:
    path = (repo_root / ref.get("path", "")).resolve()
    errors: list[str] = []
    try:
        path.relative_to(repo_root.resolve())
    except ValueError:
        return None, [f"{label} escapes repository root"]
    if not path.is_file() or path.is_symlink():
        return None, [f"{label} is not a regular file: {path}"]
    data = path.read_bytes()
    if sha_bytes(data) != ref.get("sha256"):
        errors.append(f"{label} digest mismatch")
    if len(data) != ref.get("size"):
        errors.append(f"{label} size mismatch")
    return path, errors


def semantic_errors(source: dict[str, Any], repo_root: Path) -> list[str]:
    errors: list[str] = []
    collections = ["objectives", "slices", "layers", "waves", "tasks", "swus", "implementation_details", "validation_obligations", "gates", "blockers", "gaps", "execution_entries", "closeout_obligations"]
    indexes: dict[str, dict[str, dict[str, Any]]] = {}
    all_ids: set[str] = set()
    for name in collections:
        rows = source[name]
        ids = [row["id"] for row in rows]
        if len(ids) != len(set(ids)):
            errors.append(f"{name} ids must be unique")
        overlap = all_ids.intersection(ids)
        if overlap:
            errors.append(f"ids must be globally unique: {', '.join(sorted(overlap))}")
        all_ids.update(ids)
        indexes[name] = {row["id"]: row for row in rows}

    def refs(rows: list[str], target: str, context: str) -> None:
        for item in rows:
            if item not in indexes[target]:
                errors.append(f"{context} references missing {target} id {item}")

    for row in source["slices"]:
        refs(row["objective_ids"], "objectives", row["id"])
    for row in source["waves"]:
        refs(row["slice_ids"], "slices", row["id"]); refs(row["depends_on"], "waves", row["id"]); refs(row["task_ids"], "tasks", row["id"]); refs([row["layer_id"]], "layers", row["id"]); refs([row["gate_id"]], "gates", row["id"])
    for row in source["tasks"]:
        refs([row["wave_id"]], "waves", row["id"]); refs([row["slice_id"]], "slices", row["id"]); refs(row["swu_ids"], "swus", row["id"]); refs(row["validation_ids"], "validation_obligations", row["id"])
        if not row["swu_ids"] or not row["validation_ids"]:
            errors.append(f"task {row['id']} requires at least one SWU and validation")
    for row in source["swus"]:
        refs([row["task_id"]], "tasks", row["id"]); refs(row["validation_ids"], "validation_obligations", row["id"])
    for row in source["implementation_details"]:
        refs([row["task_id"]], "tasks", row["id"])
    for row in source["gates"]:
        refs([row["after_wave"]], "waves", row["id"]); refs(row["required_validation_ids"], "validation_obligations", row["id"])
    for row in source["execution_entries"]:
        if row["unit_id"] not in indexes["tasks"] and row["unit_id"] not in indexes["swus"]:
            errors.append(f"execution entry {row['id']} references missing unit {row['unit_id']}")
    if source["mutation_capable"] and not source["execution_entries"]:
        errors.append("mutation-capable plans require at least one execution entry")
    execution_units = [row["unit_id"] for row in source["execution_entries"]]
    if len(execution_units) != len(set(execution_units)):
        errors.append("each execution unit may have only one execution entry")
    observability = source["consumer_inputs"]["observability"]
    if not observability["configured"] and observability["observer_contract_admitted"]:
        errors.append("observer_contract_admitted cannot be true when observability configured is false")
    if set(row["after_wave"] for row in source["gates"]) != set(indexes["waves"]):
        errors.append("every wave must have exactly one gate")
    for wave in source["waves"]:
        if any(indexes["tasks"].get(task_id, {}).get("wave_id") != wave["id"] for task_id in wave["task_ids"]):
            errors.append(f"wave {wave['id']} task membership is not reciprocal")
        gate = indexes["gates"].get(wave["gate_id"])
        if gate and gate["after_wave"] != wave["id"]:
            errors.append(f"wave {wave['id']} gate binding is inconsistent")
    visiting: set[str] = set(); visited: set[str] = set()
    def visit(wave_id: str) -> None:
        if wave_id in visiting:
            errors.append(f"wave dependency cycle includes {wave_id}"); return
        if wave_id in visited: return
        visiting.add(wave_id)
        for dependency in indexes["waves"].get(wave_id, {}).get("depends_on", []): visit(dependency)
        visiting.remove(wave_id); visited.add(wave_id)
    for wave_id in indexes["waves"]: visit(wave_id)
    for key, label in (("stage_receipt", "Design stage receipt"), ("admission_receipt", "Design admission receipt")):
        path, ref_errors = validate_ref(source["design_binding"][key], repo_root, label); errors.extend(ref_errors)
        if path and not ref_errors:
            try:
                receipt = load_json(path)
                if receipt.get("result") != "pass" or receipt.get("authority_effect") != "none": errors.append(f"{label} is not a no-authority PASS")
                if key == "stage_receipt" and receipt.get("schema_version") != "invoke.design-stage-receipt.v3": errors.append("Design stage receipt must be v3")
                if key == "admission_receipt" and receipt.get("schema_version") != "invoke.design-bundle-admission-receipt.v2": errors.append("Design admission receipt must be v2")
            except (OSError, ValueError, json.JSONDecodeError) as error: errors.append(f"cannot read {label}: {error}")
    return errors


def graph_from_source(source: dict[str, Any]) -> dict[str, Any]:
    kinds = {"objectives": "objective", "slices": "slice", "layers": "layer", "waves": "wave", "tasks": "task", "swus": "swu", "implementation_details": "implementation-detail", "validation_obligations": "validation", "gates": "gate", "blockers": "blocker", "gaps": "gap", "execution_entries": "execution-entry", "closeout_obligations": "closeout"}
    nodes = [{"id": row["id"], "kind": kinds[name], "data": row} for name in kinds for row in source[name]]
    edges: list[dict[str, str]] = []
    def edge(start: str, relation: str, ends: list[str]) -> None:
        edges.extend({"from": start, "relation": relation, "to": end} for end in ends)
    for row in source["slices"]: edge(row["id"], "serves", row["objective_ids"])
    for row in source["waves"]: edge(row["id"], "implements", row["slice_ids"]); edge(row["id"], "depends-on", row["depends_on"]); edge(row["id"], "contains", row["task_ids"]); edge(row["id"], "uses-layer", [row["layer_id"]]); edge(row["id"], "closes-with", [row["gate_id"]])
    for row in source["tasks"]: edge(row["id"], "contains", row["swu_ids"]); edge(row["id"], "validated-by", row["validation_ids"])
    for row in source["swus"]: edge(row["id"], "validated-by", row["validation_ids"])
    next_actions = sorted(row["id"] for row in source["tasks"] if row["status"] == "ready")
    return {"$schema": "https://arcanum.dev/schemas/invoke/plan-graph/v1", "schema_version": "invoke.plan-graph.v1", "source_id": source["source_id"], "nodes": sorted(nodes, key=lambda row: (row["kind"], row["id"])), "edges": sorted(edges, key=lambda row: (row["from"], row["relation"], row["to"])), "next_actions": next_actions, "authority_effect": "none"}


def consumer_states(source: dict[str, Any]) -> list[tuple[str, str, dict[str, Any], str]]:
    entries = source["execution_entries"]; inputs = source["consumer_inputs"]
    dispatch = inputs["dispatch"]; observability = inputs["observability"]
    observer_state = "applicable" if observability["configured"] and observability["observer_contract_admitted"] else ("blocked" if observability["configured"] else "not_applicable")
    return [
        ("wpra", "applicable" if source["mutation_capable"] else "not_applicable", {"mutation_capable": source["mutation_capable"]}, "mutation-capable plans require readiness audit input"),
        ("implementation-readiness", "applicable" if source["mutation_capable"] and entries else "not_applicable", {"mutation_capable": source["mutation_capable"], "execution_entry_count": len(entries)}, "mutation-capable plan has eligible execution entries"),
        ("task-session", "applicable" if any(row["route"] == "task-session" for row in entries) else "not_applicable", {"task_session_entries": sum(row["route"] == "task-session" for row in entries)}, "an execution entry selects task-session"),
        ("context-builder", "applicable" if any(row["delegated"] or row["bounded_context_execution"] for row in entries) else "not_applicable", {"delegated_units": sum(row["delegated"] for row in entries), "bounded_context_units": sum(row["bounded_context_execution"] for row in entries)}, "a unit is delegated or executes from bounded context"),
        ("dispatch-spec", "applicable" if any(dispatch.values()) else "not_applicable", dispatch, "a full dispatch trigger is true"),
        ("goal", "applicable" if any(row["route"] == "goal" for row in entries) else "not_applicable", {"goal_entries": sum(row["route"] == "goal" for row in entries)}, "an execution route selects Goal"),
        ("signal-observer", observer_state, observability, "observability is configured and its machine contract is admitted"),
    ]


def render_views(source: dict[str, Any], graph: dict[str, Any], root: Path) -> None:
    objectives = "\n".join(f"- **{row['id']}** — {row['statement']}" for row in source["objectives"])
    waves = "\n".join(f"- **{row['id']}** — tasks: {', '.join(row['task_ids'])}; gate: `{row['gate_id']}`" for row in source["waves"])
    blockers = "\n".join(f"- **{row['id']}** ({row['status']}) — {row['summary']}" for row in source["blockers"]) or "- None"
    gaps = "\n".join(f"- **{row['id']}** ({row['status']}) — {row['summary']}" for row in source["gaps"]) or "- None"
    next_actions = "\n".join(f"- `{item}`" for item in graph["next_actions"]) or "- No task is currently ready."
    (root / "WORK-PACK.md").write_text(f"# Work Pack: {source['target_id']}\n\nGenerated from `{source['source_id']}`. Edit `PLAN-SOURCE.json`, not this view.\n\n## Summary\n\n{source['summary']}\n\n## Objectives\n\n{objectives}\n\n## Waves\n\n{waves}\n\n## Blockers\n\n{blockers}\n\n## Gaps\n\n{gaps}\n\n## Next actions\n\n{next_actions}\n", encoding="utf-8")
    (root / "IMPLEMENTATION-LAYERING.md").write_text("# Implementation Layers\n\nGenerated from `PLAN-SOURCE.json`.\n\n" + "\n".join(f"## {row['id']}: {row['name']}\n\nExit evidence: " + "; ".join(row["exit_evidence"]) + "\n" for row in source["layers"]), encoding="utf-8")
    (root / "VALIDATION-STRATEGY.md").write_text("# Validation Strategy\n\n" + "\n".join(f"- **{row['id']}** — `{row['command']}` → {row['expected_result']}" for row in source["validation_obligations"]) + "\n", encoding="utf-8")
    (root / "GAP-LEDGER.md").write_text("# Gaps\n\n" + gaps + "\n", encoding="utf-8")
    for row in source["tasks"]:
        (root / "tasks").mkdir(exist_ok=True); (root / "tasks" / f"{row['id']}.md").write_text(f"# {row['id']}: {row['title']}\n\nOwner: {row['owner']}\n\nWave: `{row['wave_id']}`\n\nNext action: {row['next_action']}\n\nSWUs: {', '.join(row['swu_ids'])}\n\nValidations: {', '.join(row['validation_ids'])}\n", encoding="utf-8")
    for row in source["waves"]:
        (root / "waves").mkdir(exist_ok=True); (root / "waves" / f"{row['id']}.md").write_text(f"# Wave {row['id']}\n\nTasks: {', '.join(row['task_ids'])}\n\nDepends on: {', '.join(row['depends_on']) or 'none'}\n\nGate: `{row['gate_id']}`\n", encoding="utf-8")
    if source["execution_entries"]:
        (root / "EXECUTION-PACK.md").write_text("# Execution Pack\n\nGenerated navigation only. This document grants no execution authority.\n\n" + "\n".join(f"- `{row['id']}` routes `{row['unit_id']}` through `{row['route']}` and expects `{row['expected_receipt_ref']}`." for row in source["execution_entries"]) + "\n", encoding="utf-8")


def capability_path(repo_root: Path, candidates: list[str]) -> Path | None:
    return next((repo_root / item for item in candidates if (repo_root / item).is_file()), None)


def validator_identity(path: Path, repo_root: Path, identity: str) -> dict[str, Any]:
    reference = file_ref(path, path.relative_to(repo_root).as_posix())
    return {"identity": identity, **reference}


def execution_route_projection(source: dict[str, Any]) -> dict[str, Any]:
    swus = {row["id"]: row for row in source["swus"]}; tasks = {row["id"]: row for row in source["tasks"]}
    routes = []
    for entry in source["execution_entries"]:
        unit = swus.get(entry["unit_id"]); task = tasks.get(entry["unit_id"])
        writes = unit["write_scope"] if unit else [item for swu_id in task["swu_ids"] for item in swus[swu_id]["write_scope"]]
        routes.append({"route_id": entry["id"], "frontier_swu": entry["unit_id"], "capability": entry["route"], "mode": "execute", "target": entry["unit_id"], "write_scope": sorted(set(writes)), "effect_class": "repository-local-reversible", "required_inputs": ["PLAN-SOURCE.json"], "expected_receipt": entry["expected_receipt_ref"]})
    return {"schema_version": "arcanum.work-pack-execution-entry/v1", "work_pack_id": source["source_id"], "admission_timing": "selected-unit-at-task-session", "frontier": [row["unit_id"] for row in source["execution_entries"]], "execution_policy": {"route_policy": "automatic-in-scope", "allowed_routes": routes, "allowed_routes_digest": digest(routes), "digest_algorithm": "sha256 of RFC8785-compatible canonical JSON for allowed_routes", "automatic_decisions": ["internal-tool-selection", "capability-owner-routing"], "stop_decisions": ["product-or-semantic-choice", "scope-expansion", "failed-acceptance-critical-validation"], "scope_source": "exact-work-pack-and-captured-frontier", "validation_policy": "owner-gates-remain-mandatory"}, "execution_entry": {"state": "selection-ready", "selected_unit": None, "route_id": None, "next_owner": "implementation-readiness:execute"}, "pre_execution_owner_prerequisite": None, "continuation_rule": "A later explicit execution request obtains fresh selection and admission evidence.", "authority_effect": "none"}


def task_session_closure(source: dict[str, Any]) -> dict[str, Any]:
    swus = {row["id"]: row for row in source["swus"]}; tasks = {row["id"]: row for row in source["tasks"]}; validations = {row["id"]: row for row in source["validation_obligations"]}
    units = []
    applicable_entries = [row for row in source["execution_entries"] if row["route"] == "task-session" or row["delegated"] or row["bounded_context_execution"]]
    for entry in applicable_entries:
        swu = swus.get(entry["unit_id"])
        if swu is None:
            task = tasks[entry["unit_id"]]; swu = swus[task["swu_ids"][0]]
        task = tasks[swu["task_id"]]; commands = [validations[item] for item in swu["validation_ids"]]
        transients = entry["transient_outputs"]; owner_path = entry["expected_receipt_ref"] + ".owner.json"
        partition = {"schema_version": "task-session.fast-entry-route-scope-partition.v1", "executor_write_scopes": swu["write_scope"], "lifecycle_owner_scopes": [{"path": owner_path, "owner_capability": task["owner"], "write_class": "lifecycle-closeout"}], "terminal_receipt_scope": entry["expected_receipt_ref"], "exact_union_scope": sorted(set(swu["write_scope"] + [owner_path, entry["expected_receipt_ref"]]))}
        contract = {"writeProfile": "material-bound", "materialWrites": swu["write_scope"], "executionOutputs": transients, "allowedWrites": swu["write_scope"], "validationCommands": [row["command"] for row in commands], "lifecycleOwner": task["owner"], "authorityClass": "public", "publicationClass": "public"}
        version = "1.3.0" if transients else "1.2.0"
        if transients: contract["transientOutputs"] = transients
        units.append({"unit_id": entry["unit_id"], "task_id": task["id"], "native_context_projection": {"task_id": task["id"], "swu_id": entry["unit_id"], "strict_coverage": True, "admission_schema_version": version, "execution_contract": contract}, "route_scope_partition": partition, "material_writes": swu["write_scope"], "executor_outputs": transients, "validation_contracts": [{"argv": shlex.split(row["command"])} for row in commands], "lifecycle_owner": task["owner"], "authority_class": "public", "publication_class": "public", "route_write_scope": partition["exact_union_scope"], "material_delta_classes": ["repository-source"], "lifecycle_closeout_delta_classes": ["lifecycle-evidence"], "owner_receipt_schema_identity": "invoke.plan-owner-receipt.v1"})
    exact = {"path": "PLAN-SOURCE.json", "sha256": "0" * 64, "size_bytes": 0}
    return {"execution_entry_closure": {"schema_version": "execution-entry-closure.v1", "consumer_rehearsal": {"stages": ["wpra", "implementation-readiness", "context-builder", "mutation-admission", "governance-prepare", "closeout-preflight", "heterogeneous-owner-closeout", "terminal", "continuity"], "required_runs": 2, "effect": "deterministic-no-effect", "fixture_only_substitution": "forbidden", "exact_finalized_unit": units[0]["unit_id"]}, "material_delta_classes": ["repository-source"], "lifecycle_closeout_delta_classes": ["lifecycle-evidence"], "semantic_acceptance_binding": {"required": True, "eligibility_receipt": exact, "owner_acceptance_receipt": None}}, "units": units}


def _wpra_binding(binding_id: str, selector: str, evidence_ref: dict[str, Any], owner: str = "invoke-plan-owner") -> dict[str, Any]:
    return {"binding_id": binding_id, "owner_ref": owner, "artifact_ref": evidence_ref, "selector": selector}


def _wpra_status(name: str, value: str, evidence_ref: dict[str, Any]) -> dict[str, Any]:
    return {"value": value, "owner_ref": f"{name}-owner", "receipt_ref": _wpra_binding(f"{name}-receipt", f"/statuses/{name}", evidence_ref)}


def build_wpra_rehearsal(source: dict[str, Any], directory: Path, repo_root: Path) -> tuple[Path | None, list[str]]:
    """Build a bundle-local, no-effect WPRA v2 input from exact Plan fields."""
    rehearsal = directory / "rehearsal-root"
    rehearsal.mkdir(parents=True, exist_ok=True)
    (rehearsal / ".git").mkdir()
    (rehearsal / "receipts").mkdir()
    entries = source["execution_entries"]
    tasks = {row["id"]: row for row in source["tasks"]}
    swus = {row["id"]: row for row in source["swus"]}
    validations = {row["id"]: row for row in source["validation_obligations"]}
    evidence = {
        "objective": {"source_id": source["source_id"], "objectives": source["objectives"]},
        "owner": "invoke-plan-owner",
        "material": {"plan_source_digest": digest(source), "declared_write_scopes": sorted({path for row in source["swus"] for path in row["write_scope"]})},
        "validation": {"obligations": source["validation_obligations"]},
        "receipt": {"semantic": "terminal-and-closeout"},
        "closeout": {"delta": "exact", "owner": "invoke-plan-owner"},
        "package": {"kind": "invoke-plan-v2"},
        "producerReceipt": {"status": "projected"},
        "schema": {"type": "object"}, "outputSchema": {"type": "object"},
        "inventory": sorted({path for row in source["swus"] for path in row["write_scope"]}),
        "terminalSchema": {"type": "object"}, "validator": {"id": "invoke-plan-owner"},
        "admission": {"status": "candidate"}, "approval": {"status": "unapproved"},
        "risk": {"maximum": "bounded-write"}, "decision": {"selection": "pending"},
        "equivalence": {"version": "1"}, "continuation": entries[0]["unit_id"],
        "precloseoutSchema": {"type": "object"},
        "ownerSchema": {"type": "object", "properties": {"schema_version": {"const": "invoke.plan-owner-receipt.v1"}}},
        "terminalSchemaV1": {"type": "object"}, "continuitySchema": {"type": "object"}, "routerSchema": {"type": "object"},
        "statuses": {"artifact-authored": "authored", "registry-released": "unreleased", "mutation-runtime": "candidate", "audit-verdict": "pending", "plan": "authored", "audit": "pending", "approval": "unapproved", "chain": "not-started"},
    }
    evidence_path = rehearsal / "EVIDENCE.json"
    write_json(evidence_path, evidence)
    evidence_file_ref = file_ref(evidence_path, "EVIDENCE.json")
    evidence_ref = {"path": evidence_file_ref["path"], "sha256": evidence_file_ref["sha256"], "size_bytes": evidence_file_ref["size"]}
    binding = lambda name, selector: _wpra_binding(name, selector, evidence_ref)

    entry_by_unit = {row["unit_id"]: row for row in entries}
    task_for_entry: dict[str, dict[str, Any]] = {}
    wave_for_entry: dict[str, str] = {}
    for entry in entries:
        unit = swus.get(entry["unit_id"])
        task = tasks[unit["task_id"]] if unit else tasks[entry["unit_id"]]
        task_for_entry[entry["id"]] = task
        wave_for_entry[entry["id"]] = task["wave_id"]
    wave_dependencies = {row["id"]: set(row["depends_on"]) for row in source["waves"]}
    execution_bindings: list[dict[str, Any]] = []
    closeout_bindings: list[dict[str, Any]] = []
    closeout_contracts: list[dict[str, Any]] = []
    expected_material_digests: dict[str, str] = {}
    errors: list[str] = []
    for entry in entries:
        suffix = sha_bytes(entry["id"].encode("utf-8"))[:12]
        unit = swus.get(entry["unit_id"])
        task = task_for_entry[entry["id"]]
        unit_swus = [unit] if unit else [swus[item] for item in task["swu_ids"]]
        write_scope = sorted({path for row in unit_swus for path in row["write_scope"]})
        validation_ids = sorted({item for row in unit_swus for item in row["validation_ids"]})
        target_dispositions: list[dict[str, Any]] = []
        output_contracts: list[dict[str, Any]] = []
        for relative in write_scope:
            rel = Path(relative)
            if rel.is_absolute() or ".." in rel.parts:
                errors.append(f"WPRA write scope must be a confined repository-relative path: {relative}")
                continue
            live = repo_root / rel
            mirror = rehearsal / rel
            if live.is_dir():
                errors.append(f"WPRA requires exact file write scopes, not a directory: {relative}")
                continue
            mirror.parent.mkdir(parents=True, exist_ok=True)
            disposition = "update" if live.is_file() and not live.is_symlink() else "create"
            if disposition == "update":
                mirror.write_bytes(live.read_bytes())
            target_dispositions.append({"path": relative, "disposition": disposition, "producer_id": task["owner"], "parent_path": rel.parent.as_posix(), "collision_policy": "replace-declared" if disposition == "update" else "fail-if-exists", "baseline_obligation": "required-at-admission" if disposition == "update" else "none"})
            output_contracts.append({"expected_path": relative, "disposition": disposition, "producer_id": task["owner"], "schema_ref": binding(f"output-schema-{suffix}-{len(output_contracts)}", "/outputSchema"), "semantic_predicate": None, "failure_behavior": "block-before-successor", "validation_phase": "post-produce"})
        receipt_path = f"receipts/{suffix}.json"
        target_dispositions.append({"path": receipt_path, "disposition": "create", "producer_id": task["owner"], "parent_path": "receipts", "collision_policy": "fail-if-exists", "baseline_obligation": "none"})
        output_contracts.append({"expected_path": receipt_path, "disposition": "create", "producer_id": task["owner"], "schema_ref": binding(f"receipt-schema-{suffix}", "/outputSchema"), "semantic_predicate": None, "failure_behavior": "block-before-successor", "validation_phase": "post-produce"})
        dependencies = sorted(other["unit_id"] for other in entries if wave_for_entry[other["id"]] in wave_dependencies[wave_for_entry[entry["id"]]])
        successors = sorted(other["unit_id"] for other in entries if wave_for_entry[entry["id"]] in wave_dependencies[wave_for_entry[other["id"]]]) or ["__complete__"]
        validation_contracts = [{"command_id": f"validate-{suffix}-{index}", "phase": "post-produce", "argv": shlex.split(validations[item]["command"]), "cwd": ".", "timeout_seconds": 30, "max_output_bytes": 4096} for index, item in enumerate(validation_ids)]
        package_digest = digest({"unit_id": entry["unit_id"], "write_scope": write_scope, "validation_ids": validation_ids})
        expected_material_digests[entry["unit_id"]] = package_digest
        execution_bindings.append({
            "unit_id": entry["unit_id"], "dependencies": dependencies, "canonical_successors": successors, "producer_id": task["owner"],
            "task_id": task["id"], "swu_id": unit["id"] if unit else task["swu_ids"][0], "lifecycle_owner": task["owner"], "authority_class": "public", "publication_class": "public",
            "attempt_contract": {"id_policy": "one-unique-attempt-per-selected-unit", "collision_policy": "fail-before-mutation", "success_teardown": "close-after-terminal-receipt", "failure_teardown": "preserve-failure-evidence-and-stop"},
            "command": {"argv": ["false"], "cwd": ".", "risk_class": "bounded-write"},
            "target_dispositions": target_dispositions, "validation_contracts": validation_contracts, "output_contracts": output_contracts,
            "material_writes": write_scope, "execution_outputs": [receipt_path], "allowed_writes": write_scope + [receipt_path],
            "material_package": {"package_ref": binding(f"package-{suffix}", "/package"), "producer_owner_ref": task["owner"], "producer_receipt_ref": binding(f"producer-receipt-{suffix}", "/producerReceipt"), "schema_ref": binding(f"package-schema-{suffix}", "/schema"), "declared_sha256": package_digest, "target_inventory_ref": binding(f"target-inventory-{suffix}", "/inventory")},
            "byte_baselines": [{"path": row["path"], "sha256": sha_bytes((rehearsal / row["path"]).read_bytes())} for row in target_dispositions if row["disposition"] == "update"],
        })
        closeout_bindings.append({"unit_id": entry["unit_id"], "allowed_delta_policy_ref": binding(f"allowed-delta-{suffix}", "/closeout/delta"), "owner_receipt_contract_ref": binding(f"closeout-owner-{suffix}", "/closeout"), "compensation": {"mode": "none", "rationale": "The Plan compiler performs a no-effect readiness rehearsal."}})
        closeout_contracts.append({"unit_id": entry["unit_id"], "receipt_profile": "precloseout-execution-v1", "precloseout_execution_schema_ref": binding(f"precloseout-schema-{suffix}", "/precloseoutSchema"), "expected_owner_receipt_schema_ref": binding(f"owner-schema-{suffix}", "/ownerSchema"), "declared_owner_receipt_schema_identity": "invoke.plan-owner-receipt.v1", "final_terminal_schema_ref": binding(f"terminal-schema-v1-{suffix}", "/terminalSchemaV1"), "continuity_schema_ref": binding(f"continuity-schema-{suffix}", "/continuitySchema"), "continuation_router_schema_ref": binding(f"router-schema-{suffix}", "/routerSchema")})
    if errors:
        return None, errors
    first_unit = entries[0]["unit_id"]
    allowed_routes = execution_route_projection(source)["execution_policy"]["allowed_routes"]
    config = {
        "schema_version": "2.0.0", "admission_timing": "selected-unit-at-task-session", "audit_id": f"invoke-plan-v2-{digest(source)[:16]}", "repository_root": ".", "evidence_ceiling": "frozen-input-contractual-readiness", "classifier_version": "wpra-projection-v1",
        "execution_policy": {"work_pack_id": source["source_id"], "route_policy": "automatic-in-scope", "allowed_routes": allowed_routes, "allowed_routes_digest": digest(allowed_routes), "automatic_decisions": ["internal-tool-selection", "capability-owner-routing"], "stop_decisions": ["product-or-semantic-choice", "scope-expansion", "failed-acceptance-critical-validation"], "scope_source": "exact-work-pack-and-captured-frontier", "validation_policy": "owner-gates-remain-mandatory"},
        "objective_ref": binding("objective", "/objective"), "closure_receipt_refs": [binding("design-stage", "/statuses/artifact-authored"), binding("design-admission", "/statuses/mutation-runtime")],
        "authority_bindings": {"canonical_authority_refs": [binding("canonical-objective", "/objective")], "semantic_bindings": {name: binding(f"semantic-{name}", f"/{name}") for name in ["owner", "material", "validation", "receipt", "closeout"]}},
        "execution_bindings": execution_bindings,
        "receipt_bindings": {"terminal_schema_ref": binding("terminal-schema", "/terminalSchema"), "semantic_validator_ref": binding("terminal-validator", "/validator"), "expected_receipt_refs": [binding("expected-terminal", "/statuses/mutation-runtime")]},
        "closeout_bindings": closeout_bindings, "task_session_closeout_contracts": closeout_contracts,
        "runtime_binding": {"requested_task_session_execution_mode": "routed-mutation", "task_session_admission_receipt_ref": None},
        "status_receipt_refs": {"artifact_authored_status": _wpra_status("artifact-authored", "authored", evidence_ref), "registry_released_status": _wpra_status("registry-released", "unreleased", evidence_ref), "mutation_runtime_ready_status": _wpra_status("mutation-runtime", "candidate", evidence_ref), "audit_verdict": _wpra_status("audit-verdict", "pending", evidence_ref)},
        "lifecycle_status_refs": {"plan_artifact_status": _wpra_status("plan", "authored", evidence_ref), "audit_status": _wpra_status("audit", "pending", evidence_ref), "approval_status": _wpra_status("approval", "unapproved", evidence_ref), "chain_status": _wpra_status("chain", "not-started", evidence_ref)},
        "approval_policy": {"approval_owner_ref": "decision-gate", "decision_gate_receipt_ref": binding("decision-gate", "/decision"), "run_budget": {"max_task_session_requests": 1}, "risk_policy_ref": binding("risk-policy", "/risk"), "allowed_audit_verdicts": ["pass", "flag"], "allowed_flag_classes": ["observability-residue"]},
        "continuity_projection": {"cursor": first_unit, "completed_unit_receipt_refs": [], "joined_closeout_receipt_refs": [], "projected_next_successor": {"unit_id": first_unit, "canonical_successor_ref": binding("canonical-successor", "/continuation"), "projection_owner_ref": "work-pack-readiness-audit", "equivalence_validator_ref": binding("equivalence-validator", "/equivalence"), "continuation_router_verification_receipt_ref": binding("continuation-verification", "/continuation"), "authority_effect": "none"}},
        "expected_material_digests": expected_material_digests,
    }
    config_path = rehearsal / "AUDIT-CONFIG.json"
    write_json(config_path, config)
    return config_path, []


def run_wpra_rehearsal(source: dict[str, Any], directory: Path, repo_root: Path) -> tuple[list[str], list[str], Path | None]:
    config_path, errors = build_wpra_rehearsal(source, directory, repo_root)
    if errors or config_path is None:
        return [], errors, None
    runner = capability_path(repo_root, ["arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py", ".agents/skills/work-pack-readiness-audit/scripts/audit_work_pack.py", ".claude/skills/work-pack-readiness-audit/scripts/audit_work_pack.py"])
    if runner is None:
        return [], ["wpra no-effect validator is not installed"], None
    paths = [path for path in sorted(config_path.parent.rglob("*")) if path.is_file()]
    output_dirs = [directory / "run-1", directory / "run-2"]
    for output_dir in output_dirs:
        completed = subprocess.run([sys.executable, str(runner), "--config", str(config_path), "--output-dir", str(output_dir)], text=True, capture_output=True, check=False)
        if completed.returncode:
            return [path.relative_to(directory.parent.parent).as_posix() for path in paths if path.is_file()], [f"wpra no-effect validator failed: {(completed.stderr or completed.stdout).strip()}"], runner
        report = load_json(output_dir / "work-pack-readiness-report-v2.json")
        if report.get("verdict") != "pass" or report.get("configured_commands_executed") is not False or report.get("authority_effect") != "none":
            return [], ["wpra rehearsal did not produce a no-effect PASS"], runner
        paths.extend(path for path in sorted(output_dir.rglob("*")) if path.is_file())
    first = [(path.relative_to(output_dirs[0]), path.read_bytes()) for path in sorted(output_dirs[0].rglob("*")) if path.is_file()]
    second = [(path.relative_to(output_dirs[1]), path.read_bytes()) for path in sorted(output_dirs[1].rglob("*")) if path.is_file()]
    if first != second:
        return [], ["wpra two-run outputs are not byte-identical"], runner
    return [path.relative_to(directory.parent.parent).as_posix() for path in paths if path.is_file()], [], runner


def project_consumers(source: dict[str, Any], root: Path, repo_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    results: list[dict[str, Any]] = []; blockers: list[str] = []; entries = source["execution_entries"]
    closure = task_session_closure(source) if entries else None
    applicability_validator = validator_identity(Path(__file__).resolve(), repo_root, "invoke.plan-consumer-applicability.v1")
    for name, state, inputs, reason in consumer_states(source):
        directory = root / "consumers" / name; directory.mkdir(parents=True, exist_ok=True); paths: list[str] = []
        if name == "dispatch-spec":
            trace = directory / "TECHNIQUE-TRACE.json"; write_json(trace, {"source_id": source["source_id"], "techniques": ["sequence", "scu_swu_reduction", "validation_loop", "owner_boundary_check", "execution_receipt_handoff"], "authority_effect": "none"}); paths.append(trace.relative_to(root).as_posix())
        if state == "blocked":
            blocker = f"{name} applicability blocked: configured observer contract is not admitted"; blockers.append(blocker)
            path = directory / "BLOCKER.json"; write_json(path, {"consumer": name, "predicate_inputs": inputs, "blocker": blocker, "authority_effect": "none"}); paths.append(path.relative_to(root).as_posix())
            results.append({"consumer": name, "state": "blocked", "predicate_inputs": inputs, "reason": blocker, "projection_paths": paths, "validator": applicability_validator, "result": "block", "failure_route": f"repair-{name}-contract"}); continue
        if state == "not_applicable":
            path = directory / "NEGATIVE-EVIDENCE.json"; write_json(path, {"consumer": name, "state": state, "predicate_inputs": inputs, "reason": f"Not applicable: {reason} predicate evaluated false.", "authority_effect": "none"}); paths.append(path.relative_to(root).as_posix())
            results.append({"consumer": name, "state": state, "predicate_inputs": inputs, "reason": f"{reason} predicate evaluated false", "projection_paths": paths, "validator": applicability_validator, "result": "negative_evidence", "failure_route": f"repair-{name}-predicate"}); continue
        blocker_start = len(blockers)
        command: list[str] | None = None; runner: Path | None = None; validator = f"invoke.validate-plan-{name}-projection.v1"
        if name == "wpra":
            wpra_paths, wpra_errors, runner = run_wpra_rehearsal(source, directory, repo_root)
            paths.extend(wpra_paths); blockers.extend(wpra_errors)
            projection = {"schema_version": "invoke.plan-wpra-projection.v1", "work_pack_id": source["source_id"], "frontier": [row["unit_id"] for row in entries], "validation_ids": [row["id"] for row in source["validation_obligations"]], "configured_commands_executed": False, "required_runs": 2, "audit_config": "consumers/wpra/rehearsal-root/AUDIT-CONFIG.json", "authority_effect": "none"}
        elif name == "implementation-readiness":
            projection = execution_route_projection(source); validator = "implementation-readiness.validate-work-pack-execution-entry.v1"
        elif name in {"task-session", "context-builder"}:
            assert closure is not None; closure_path = directory / "EXECUTION-ENTRY-CLOSURE.json"; write_json(closure_path, closure); paths.append(closure_path.relative_to(root).as_posix())
            if name == "task-session":
                projection = closure; validator = "task-session.execution-entry-projection-validation.v1"
            else:
                projection = {"schema_version": "invoke.plan-context-builder-projections.v1", "units": [row["native_context_projection"] for row in closure["units"]]}; validator = "context-builder.compile-native-context-projection.v1"
        elif name == "dispatch-spec":
            goal_runtime = capability_path(repo_root, ["arcanum/spells/goal/runtime/goal_loop.py", ".agents/skills/goal/runtime/goal_loop.py", ".claude/skills/goal/runtime/goal_loop.py"])
            if goal_runtime is None: projection = {}; blockers.append("dispatch-spec projection requires the Goal route builder")
            else:
                spec = importlib.util.spec_from_file_location("plan_goal_route_builder", goal_runtime); module = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module)
                projection = module.build_dispatch_route({"goal": source["summary"], "nodes": [{"node_id": row["id"], "summary": row["title"], "owner": row["owner"], "status": row["status"], "risk_tier": "T1"} for row in source["tasks"]]})
            validator = "dispatch-spec.validate-dispatch"
        elif name == "goal":
            selected = next(row for row in entries if row["route"] == "goal"); projection = {"schema_version": "goal.plan-route-contract.v1", "frontier": [selected["unit_id"]], "owner": "goal", "expected_receipt": selected["expected_receipt_ref"], "gate": source["gates"][0]["id"], "stop": "block before mutation when validation fails", "fallback": "return to plan owner", "authority_effect": "none"}; validator = "goal.validate-plan-route.v1"
        else:
            projection = {"timestamp": "1970-01-01T00:00:00Z", "run_id": f"plan-projection-{digest(source)[:16]}", "capability": {"id": "invoke", "kind": "spell", "mode": "plan"}, "request": {"summary": source["summary"]}, "execution": {"status": "projected", "outputs": [], "files_changed": [], "validation": ["Plan envelope validated without append"]}, "observer": {"quality_bar_status": "not_checked", "anti_pattern_hits": [], "workflow_gaps": [], "reflection_trigger": "none", "recommendation": "none"}}; validator = "observability.validate-invocation-envelope.v1"
        path = directory / "PROJECTION.json"; write_json(path, projection); paths.append(path.relative_to(root).as_posix())
        output = directory / "VALIDATION-RESULT.json"
        if name == "implementation-readiness":
            runner = capability_path(repo_root, ["arcanum/spells/implementation-readiness/scripts/validate_work_pack_execution_entry.py", ".agents/skills/implementation-readiness/scripts/validate_work_pack_execution_entry.py", ".claude/skills/implementation-readiness/scripts/validate_work_pack_execution_entry.py"]); command = ["python3", str(runner), "--projection", str(path), "--output", str(output)] if runner else None
        elif name == "task-session":
            runner = capability_path(repo_root, ["arcanum/arcana/task-session/scripts/execution_entry_projection.py", ".agents/skills/task-session/scripts/execution_entry_projection.py", ".claude/skills/task-session/scripts/execution_entry_projection.py"]); command = ["python3", str(runner), str(path), "--output", str(output)] if runner else None
        elif name == "context-builder":
            runner = capability_path(repo_root, ["arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py", ".agents/skills/context-builder/scripts/compile_native_context_projection.py", ".claude/skills/context-builder/scripts/compile_native_context_projection.py"])
            if runner:
                context_errors = []
                for index, unit_row in enumerate(closure["units"]):
                    unit_output = directory / f"VALIDATION-RESULT-{index + 1}.json"
                    completed = subprocess.run(["python3", str(runner), "--source", str(directory / "EXECUTION-ENTRY-CLOSURE.json"), "--unit-id", unit_row["unit_id"], "--output", str(unit_output)], cwd=repo_root, text=True, capture_output=True, check=False)
                    if completed.returncode:
                        context_errors.append((completed.stderr or completed.stdout).strip())
                    else:
                        paths.append(unit_output.relative_to(root).as_posix())
                if context_errors:
                    blockers.append(f"context-builder no-effect validator failed: {'; '.join(context_errors)}")
                command = []
        elif name == "dispatch-spec":
            runner = capability_path(repo_root, ["arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py", ".agents/skills/dispatch-spec/scripts/validate-dispatch.py", ".claude/skills/dispatch-spec/scripts/validate-dispatch.py"]); command = ["python3", str(runner), str(path)] if runner else None
        elif name == "goal":
            runner = capability_path(repo_root, ["arcanum/spells/goal/runtime/validate_plan_route.py", ".agents/skills/goal/runtime/validate_plan_route.py", ".claude/skills/goal/runtime/validate_plan_route.py"]); command = ["python3", str(runner), "--input", str(path)] if runner else None
        elif name == "signal-observer":
            runner = capability_path(repo_root, ["arcanum/arcana/signal-observer/scripts/validate-invocation-envelope.py", ".agents/skills/signal-observer/scripts/validate-invocation-envelope.py", ".claude/skills/signal-observer/scripts/validate-invocation-envelope.py"]); command = ["python3", str(runner), "--envelope", str(path)] if runner else None
        if name != "wpra" and command is None: blockers.append(f"{name} no-effect validator is not installed")
        elif command:
            completed = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
            if completed.returncode: blockers.append(f"{name} no-effect validator failed: {(completed.stderr or completed.stdout).strip()}")
            elif output.is_file(): paths.append(output.relative_to(root).as_posix())
        result = "block" if len(blockers) > blocker_start else "pass"
        bound_validator = validator_identity(runner, repo_root, validator) if runner else applicability_validator
        results.append({"consumer": name, "state": state, "predicate_inputs": inputs, "reason": reason, "projection_paths": paths, "validator": bound_validator, "result": result, "failure_route": f"repair-{name}-projection"})
    return results, blockers


def inventory(root: Path, *, exclude_stage: bool = False) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink(): raise ValueError(f"symlink forbidden in bundle: {path}")
        if path.is_file() and not (exclude_stage and path.name == "PLAN-STAGE-RECEIPT.json"):
            rows.append(file_ref(path, path.relative_to(root).as_posix()))
    return rows


def compile_bundle(source_path: Path, output_dir: Path, repo_root: Path, schema_dir: Path) -> list[str]:
    errors: list[str] = []
    try: source = load_json(source_path)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error: return [f"source invalid: {error}"]
    errors.extend(validate_schema(source, schema_dir / "plan-source-v2.schema.json", "Plan source")); errors.extend(semantic_errors(source, repo_root))
    if errors: return errors
    if output_dir.exists() or output_dir.is_symlink(): return [f"output directory must be absent: {output_dir}"]
    staging = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_dir.parent))
    try:
        write_json(staging / "PLAN-SOURCE.json", source)
        graph = graph_from_source(source); write_json(staging / "PLAN-GRAPH.json", graph)
        write_json(staging / "SWU-MANIFEST.json", {"schema_version": "invoke.plan-swu-manifest.v1", "source_id": source["source_id"], "swus": source["swus"], "authority_effect": "none"})
        render_views(source, graph, staging)
        consumer_results, consumer_blockers = project_consumers(source, staging, repo_root); errors.extend(consumer_blockers)
        applicability = {"$schema": "https://arcanum.dev/schemas/invoke/plan-consumer-applicability/v1", "schema_version": "invoke.plan-consumer-applicability.v1", "source_id": source["source_id"], "consumers": consumer_results, "authority_effect": "none"}
        errors.extend(validate_schema(applicability, schema_dir / "plan-consumer-applicability-v1.schema.json", "Consumer applicability")); write_json(staging / "CONSUMER-APPLICABILITY.json", applicability)
        errors.extend(validate_schema(graph, schema_dir / "plan-graph-v1.schema.json", "Plan graph"))
        if errors: return errors
        producer_path = Path(__file__).resolve().parent / "compile_plan_bundle_v2.py"
        source_ref = file_ref(staging / "PLAN-SOURCE.json", "PLAN-SOURCE.json")
        receipt = {"$schema": "https://arcanum.dev/schemas/invoke/plan-stage-receipt/v2", "schema_version": "invoke.plan-stage-receipt.v2", "receipt_id": f"plan-stage-v2:{source_ref['sha256'][:24]}", "source_ref": source_ref, "design_binding": source["design_binding"], "producer": {"identity": "invoke.compile-plan-bundle.v2", "path": producer_path.relative_to(repo_root).as_posix(), "sha256": sha_bytes(producer_path.read_bytes())}, "outputs": inventory(staging, exclude_stage=True), "consumer_results": consumer_results, "result": "pass", "authority_effect": "none"}
        receipt["receipt_digest"] = digest(receipt); errors.extend(validate_schema(receipt, schema_dir / "plan-stage-receipt-v2.schema.json", "Plan stage receipt")); write_json(staging / "PLAN-STAGE-RECEIPT.json", receipt)
        if errors: return errors
        os.rename(staging, output_dir)
    finally:
        if staging.exists(): shutil.rmtree(staging)
    return []
