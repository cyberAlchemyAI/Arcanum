#!/usr/bin/env python3
"""Exercise finalized execution-entry values across real consumers, with no effects."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
INVOKE_ROOT = Path(__file__).resolve().parents[1]
RECEIPT_SCHEMA = INVOKE_ROOT / "schemas/execution-entry-consumer-rehearsal-v1.schema.json"
STAGE_CONSUMERS = {
    "wpra": ("work-pack-readiness-audit.v2", ["arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py"]),
    "implementation-readiness": ("implementation-readiness.execution-contracts.v1", ["arcanum/spells/implementation-readiness/scripts/execution_contracts.py"]),
    "context-builder": ("context-builder.native-machine-view.v1", ["arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py"]),
    "mutation-admission": ("task-session.mutation-admission.v1", ["arcanum/arcana/task-session/scripts/verify-mutation-readiness.py"]),
    "governance-prepare": ("task-session.live-execution-entry-preparation.v1", ["arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"]),
    "accepted-stream-driver-request": ("invoke.accepted-stream-driver-bridge.v1", ["arcanum/spells/invoke/scripts/accepted_stream_driver_bridge.py"]),
    "accepted-stream-driver": ("task-session-until-blocker.accepted-stream-driver.v1", ["arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py"]),
    "accepted-stream-driver-join": ("invoke.accepted-stream-driver-join.v1", ["arcanum/spells/invoke/schemas/accepted-stream-driver-join-v1.schema.json"]),
    "child-precloseout": ("task-session.closeout-preflight.v2", ["arcanum/arcana/task-session/scripts/evaluate-governance.py"]),
    "child-final-terminal": ("task-session.final-terminal.v2", ["arcanum/arcana/task-session/scripts/accepted_stream_terminalization.py"]),
    "child-continuity": ("task-session.continuity.v2", ["arcanum/arcana/task-session/continuity.schema.json"]),
    "successor-pair": ("task-session-until-blocker.successor-pair.v1", ["arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py"]),
    "reducer-transition": ("task-session-until-blocker.reducer-transition.v1", ["arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py"]),
    "stream-completion": ("task-session-until-blocker.stream-completion.v1", ["arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py"]),
}


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def exact_ref(path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": path.resolve().relative_to(REPOSITORY_ROOT.resolve()).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def load_module(relative: str, name: str) -> Any:
    path = REPOSITORY_ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ValueError(f"cannot load consumer: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def stage(
    stage_id: str,
    value: Any,
    consumer_refs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if stage_id == "invoke-owner-closeout":
        identity = "invoke.owner-closeout-schema-frontier.v2"
        if not consumer_refs:
            raise ValueError("heterogeneous owner closeout refs missing")
        refs = consumer_refs
    else:
        identity, relative_paths = STAGE_CONSUMERS[stage_id]
        refs = [exact_ref(REPOSITORY_ROOT / relative) for relative in relative_paths]
    return {
        "stage_id": stage_id,
        "consumer_identity": identity,
        "consumer_refs": refs,
        "result": "pass",
        "projection_digest": canonical_digest(value),
    }


def resolve_binding(binding: dict[str, Any]) -> Any:
    source = load_object(REPOSITORY_ROOT / binding["artifact_ref"]["path"])
    pointer = binding["selector"]
    if pointer == "":
        return source
    current: Any = source
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def resolve_owner_closeout_frontier(
    units: list[dict[str, Any]],
    config: dict[str, Any],
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    """Resolve every declared owner schema without imposing owner heterogeneity."""
    unit_by_id = {item["unit_id"]: item for item in units}
    if not unit_by_id or len(unit_by_id) != len(units):
        raise ValueError("typed owner closeout unit frontier is empty or duplicated")
    contracts = config.get("task_session_closeout_contracts")
    if not isinstance(contracts, list) or not contracts:
        raise ValueError("typed owner closeout contract frontier is missing")
    closeouts = {
        item.get("unit_id"): item
        for item in contracts
        if isinstance(item, dict) and isinstance(item.get("unit_id"), str)
    }
    if len(closeouts) != len(contracts) or set(closeouts) != set(unit_by_id):
        raise ValueError("typed owner closeout frontier is incomplete or mismatched")

    identities: dict[str, str] = {}
    owner_schema_refs: list[dict[str, Any]] = []
    for closed_unit, unit in unit_by_id.items():
        binding = closeouts[closed_unit].get("expected_owner_receipt_schema_ref")
        if not isinstance(binding, dict) or not isinstance(binding.get("artifact_ref"), dict):
            raise ValueError(f"owner closeout schema binding missing: {closed_unit}")
        owner_schema_refs.append(binding["artifact_ref"])
        owner_schema = resolve_binding(binding)
        Draft202012Validator.check_schema(owner_schema)
        identity = owner_schema.get("properties", {}).get("schema_version", {}).get("const")
        if identity != unit.get("owner_receipt_schema_identity"):
            raise ValueError(f"owner closeout schema identity mismatch: {closed_unit}")
        identities[closed_unit] = identity
    if set(identities) != set(unit_by_id):
        raise ValueError("typed owner closeout frontier is incomplete")

    unique_owner_schema_refs = {
        canonical_digest(reference): reference for reference in owner_schema_refs
    }
    return identities, sorted(
        unique_owner_schema_refs.values(), key=lambda item: item["path"]
    )


def resolve_task_session_execution_routes(
    policy: dict[str, Any],
    unit_ids: set[str],
) -> dict[str, dict[str, Any]]:
    """Select one Task Session execution route per unit without collapsing owner routes."""
    routes_by_unit: dict[str, list[dict[str, Any]]] = {
        unit_id: [] for unit_id in unit_ids
    }
    for route in policy.get("allowed_routes", []):
        if not isinstance(route, dict):
            raise ValueError("Implementation Readiness route is not an object")
        if route.get("capability") != "task-session" or route.get("mode") != "execute":
            continue
        unit_id = route.get("frontier_swu")
        if unit_id not in routes_by_unit:
            raise ValueError(
                "Task Session execution route is outside the finalized frontier"
            )
        routes_by_unit[unit_id].append(route)
    invalid = sorted(
        unit_id for unit_id, routes in routes_by_unit.items() if len(routes) != 1
    )
    if invalid:
        raise ValueError(
            "Implementation Readiness must provide exactly one Task Session "
            "execution route for each finalized unit: " + ", ".join(invalid)
        )
    return {unit_id: routes[0] for unit_id, routes in routes_by_unit.items()}


def rehearse(
    source: dict[str, Any],
    config: dict[str, Any],
    unit_id: str,
    source_ref: dict[str, Any],
    config_ref: dict[str, Any],
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    task_projection = load_module(
        "arcanum/arcana/task-session/scripts/execution_entry_projection.py",
        "invoke_task_execution_entry_projection",
    )
    closure = task_projection.validate_document(source)
    if closure["closure_result"] != "pass":
        raise ValueError("Task Session execution-entry closure failed")

    wpra = load_module(
        "arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py",
        "invoke_execution_entry_wpra",
    )
    config_errors = wpra.schema_errors(config, wpra.load_json(wpra.CONFIG_SCHEMA_V2), "v2 config")
    if config_errors:
        raise ValueError(config_errors[0])
    wpra_result = wpra.audit_v2(config, REPOSITORY_ROOT)
    if wpra_result["verdict"] != "pass" or wpra_result["configured_commands_executed"]:
        raise ValueError("WPRA did not produce a no-command closure projection")
    results.append(stage("wpra", wpra_result["manifest"]))

    readiness = load_module(
        "arcanum/spells/implementation-readiness/scripts/execution_contracts.py",
        "invoke_execution_entry_readiness",
    )
    wpra_policy = config["execution_policy"]
    manifest = wpra_result["manifest"]
    continuity = {
        "source_audit_id": config["audit_id"],
        "source_projection_digest": wpra_result["audit_projection_digest"],
        "work_pack_semantic_digest": manifest["canonical_semantic_digest"],
        "plan_epoch_id": manifest["plan_epoch_id"],
        "completed_prefix": [],
        "next_unit": manifest["ready_frontier"][0],
        "authority_effect": "none",
    }
    continuity["continuity_digest"] = readiness.canonical_digest(continuity)
    policy_input = {
        "schema_version": "1.1.0",
        "work_pack_id": wpra_policy["work_pack_id"],
        "work_pack_semantic_digest": manifest["canonical_semantic_digest"],
        "frontier": [item["unit_id"] for item in source["units"]],
        "completion_continuity": continuity,
        "allowed_routes": wpra_policy["allowed_routes"],
        "allowed_routes_digest": wpra_policy["allowed_routes_digest"],
        "automatic_decisions": wpra_policy["automatic_decisions"],
        "stop_decisions": wpra_policy["stop_decisions"],
        "validation_commands": sorted({
            " ".join(command["argv"])
            for unit in source["units"]
            for command in unit["validation_contracts"]
        }),
        "scope_source": wpra_policy["scope_source"],
        "validation_policy": wpra_policy["validation_policy"],
        "authority_effect": "none",
    }
    policy = readiness.validate_execution_policy(policy_input)
    unit_by_id = {item["unit_id"]: item for item in source["units"]}
    route_by_unit = resolve_task_session_execution_routes(policy, set(unit_by_id))
    for closed_unit, unit in unit_by_id.items():
        if route_by_unit[closed_unit]["write_scope"] != unit["route_write_scope"]:
            raise ValueError(f"Implementation Readiness route partition drift: {closed_unit}")
    results.append(stage("implementation-readiness", policy))

    context_builder = load_module(
        "arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py",
        "invoke_execution_entry_context_builder",
    )
    context = context_builder.compile_projection(source, unit_id)
    results.append(stage("context-builder", context))

    unit = unit_by_id[unit_id]
    contract = context["execution_contract"]
    admission = load_module(
        "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
        "invoke_execution_entry_mutation_admission",
    )
    request = {
        "schemaVersion": context["admission_schema_version"],
        "validationCommands": contract["validationCommands"],
        "lifecycleOwner": contract["lifecycleOwner"],
        "authorityClass": contract["authorityClass"],
        "publicationClass": contract["publicationClass"],
    }
    failures = admission.context_contract_failures(
        contract, request, contract["writeProfile"], set(contract["materialWrites"]),
        set(contract["executionOutputs"]), set(contract.get("transientOutputs", [])),
        set(contract["allowedWrites"]),
    )
    if failures:
        raise ValueError("mutation admission projection failed: " + "; ".join(failures))
    results.append(stage("mutation-admission", context))

    governance = load_module(
        "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
        "invoke_execution_entry_governance",
    )
    route = route_by_unit[unit_id]
    partition = governance.fast_entry_route_scope_partition(
        REPOSITORY_ROOT,
        {"route_scope_partition": unit["route_scope_partition"]},
        route,
        {"execution_contract": {"allowed_writes": contract["allowedWrites"], "transient_outputs": []}, "closeout_contract": {"terminal_receipt_path": unit["route_scope_partition"]["terminal_receipt_scope"]}},
    )
    results.append(stage("governance-prepare", partition))

    bridge = load_module("arcanum/spells/invoke/scripts/accepted_stream_driver_bridge.py", "invoke_accepted_stream_driver_bridge")
    accepted_contract = load_module("arcanum/spells/invoke/scripts/accepted_stream_contract.py", "invoke_accepted_stream_contract")
    driver = load_module("arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py", "invoke_accepted_stream_driver")
    authority = {name: [] for name in ("material", "control", "terminal", "lifecycle", "transient", "failure", "claim", "stream")}
    requested_effect = {"kind": "bounded-write", "external_effect": "none"}
    epoch = f"rehearsal-{manifest['plan_epoch_id']}"
    graph_digest = canonical_digest({"source": source_ref, "config": config_ref})
    frozen_frontier = [{"ordinal": item.get("ordinal", ordinal), "swu_id": item["unit_id"]} for ordinal, item in enumerate(source["units"])]
    stream = accepted_contract.stream_id(graph_digest, requested_effect, authority, frozen_frontier, epoch)
    for item in frozen_frontier:
        item["child_id"] = accepted_contract.child_id(stream, item["ordinal"], item["swu_id"])
    units = [{"unit_id": item["swu_id"], "ordinal": item["ordinal"], "status": "pass", "result_digest": canonical_digest({"source_unit": unit_id, "ordinal": item["ordinal"], "partition": partition})} for item in frozen_frontier]
    finalized_projection = {"schema_version": "invoke.accepted-stream-finalized-projection.v1", "graph_digest": graph_digest, "accepted_stream_id": stream, "requested_effect": requested_effect, "authority": authority, "epoch": epoch, "frontier_digest": canonical_digest(frozen_frontier), "acceptance_request_digest": "0" * 64, "units": units}
    live_baseline = {"schema_version": "invoke.accepted-stream-live-baseline.v1", "accepted_stream_id": stream, "epoch": epoch, "frontier_digest": finalized_projection["frontier_digest"], "baseline_digest": canonical_digest({"source": source_ref, "partition": partition}), "status": "pass"}
    driver_request = bridge.compile_request(REPOSITORY_ROOT, finalized_projection, None, live_baseline, frozen_frontier, no_effect=True)
    results.append(stage("accepted-stream-driver-request", driver_request))
    driver_receipt = driver.run(driver_request)
    if driver_receipt.get("status") != "complete" or len(driver_receipt.get("ordered_units", [])) != len(frozen_frontier):
        raise ValueError("accepted-stream driver did not complete the frozen frontier")
    results.append(stage("accepted-stream-driver", driver_receipt))
    joined_driver = bridge.join_receipt(REPOSITORY_ROOT, finalized_projection, live_baseline, driver_request, [driver_receipt])
    if joined_driver["joined_receipt_count"] != 1:
        raise ValueError("accepted-stream driver receipt was not joined exactly once")
    results.append(stage("accepted-stream-driver-join", joined_driver))

    evaluator = load_module(
        "arcanum/arcana/task-session/scripts/evaluate-governance.py",
        "invoke_execution_entry_precloseout",
    )
    decision_policy = load_object(REPOSITORY_ROOT / "arcanum/arcana/task-session/decision-validation-policy.json")
    preflight_input = {
        "sync_expected": True,
        "terminal_source_receipt_contract": "bound",
        "declared_target_inventory": unit["route_write_scope"],
        "baseline_state": "captured",
        "allowed_delta_classes": unit["lifecycle_closeout_delta_classes"],
        "validation_commands": contract["validationCommands"],
        "expected_owner_receipt": unit["owner_receipt_schema_identity"],
        "successor_selection": {"requested": False},
    }
    if evaluator.evaluate_closeout_preflight(decision_policy, preflight_input) != "PROCEED":
        raise ValueError("closeout preflight rejected lifecycle delta classes")
    results.append(stage("child-precloseout", preflight_input))

    identities, owner_schema_refs = resolve_owner_closeout_frontier(
        source["units"], config
    )
    results.append(
        stage(
            # Historical stage token: exhaustive typed owner-closeout coverage;
            # it does not require two distinct owner or schema identities.
            "invoke-owner-closeout",
            identities,
            owner_schema_refs,
        )
    )

    terminal_schema = load_object(REPOSITORY_ROOT / "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json")
    Draft202012Validator.check_schema(terminal_schema)
    terminal_binding = {"task_id": unit["task_id"], "swu_id": unit_id, "terminal_scope": unit["route_scope_partition"]["terminal_receipt_scope"], "owner_result_schema": unit["owner_receipt_schema_identity"]}
    terminal_binding["predecessor_join_digest"] = joined_driver["join_digest"]
    results.append(stage("child-final-terminal", terminal_binding))

    continuity_schema = load_object(REPOSITORY_ROOT / "arcanum/arcana/task-session/continuity.schema.json")
    continuity = {"schema_version": "task-session.continuity.v1", "session_id": "no-effect-rehearsal", "updated_at": "2000-01-01T00:00:00Z", "scope_root": ".", "work_pack": source["work_pack_id"], "source_swu": unit_id, "source_result": "BLOCK", "source_receipt": unit["route_scope_partition"]["terminal_receipt_scope"], "closeout_owner_receipt": None, "next_swu": None, "next_route": None, "blocker_fingerprint": "REQUEST_EMISSION_ELIGIBILITY_BINDING_MISSING"}
    continuity_errors = list(Draft202012Validator(continuity_schema).iter_errors(continuity))
    if continuity_errors:
        raise ValueError("continuity projection schema failed: " + continuity_errors[0].message)
    continuity["driver_join_digest"] = joined_driver["join_digest"]
    results.append(stage("child-continuity", continuity))
    successor_pair = {"stream_id": stream, "completed_unit": frozen_frontier[-1]["swu_id"], "next_unit": None, "driver_join_digest": joined_driver["join_digest"]}
    results.append(stage("successor-pair", successor_pair))
    reducer_transition = {"stream_id": stream, "joined_receipt_digest": joined_driver["receipt_digest"], "completed_count": len(frozen_frontier), "successor_pair_digest": canonical_digest(successor_pair)}
    results.append(stage("reducer-transition", reducer_transition))
    completion = {"stream_id": stream, "status": "complete", "completed_count": len(frozen_frontier), "retry_count": 0, "transition_digest": canonical_digest(reducer_transition)}
    results.append(stage("stream-completion", completion))

    receipt = {
        "schema_version": "invoke.execution-entry-consumer-rehearsal.v1",
        "source_ref": source_ref, "wpra_config_ref": config_ref,
        "unit_id": unit_id, "stages": results, "closure_result": "pass",
        "request_eligibility_result": closure["request_eligibility_result"],
        "request_eligibility_blockers": closure["request_eligibility_blockers"],
        "owner_acceptance_status": closure["owner_acceptance_status"],
        "selection_admission_authority": "absent",
        "joined_driver_digest": joined_driver["join_digest"],
        "effects": {"repository_writes": 0, "external_effects": False, "selection": False, "admission_token": False, "execution": False},
        "authority_effect": "none",
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    errors = list(Draft202012Validator(load_object(RECEIPT_SCHEMA)).iter_errors(receipt))
    if errors:
        raise ValueError("rehearsal receipt invalid: " + errors[0].message)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--wpra-config", required=True)
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    source_path = Path(args.source)
    config_path = Path(args.wpra_config)
    receipt = rehearse(
        load_object(source_path), load_object(config_path), args.unit_id,
        exact_ref(source_path), exact_ref(config_path),
    )
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output: Path(args.output).write_text(rendered, encoding="utf-8")
    else: print(rendered, end="")
    return 0


if __name__ == "__main__": raise SystemExit(main())
