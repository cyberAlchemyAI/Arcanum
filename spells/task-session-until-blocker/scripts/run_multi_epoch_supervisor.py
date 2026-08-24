#!/usr/bin/env python3
"""Supervise fresh one-request epochs without launching lifecycle capabilities."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


SPELL_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = SPELL_ROOT / "scripts" / "run_chain.py"
CONFIG_SCHEMA = SPELL_ROOT / "schemas" / "multi-epoch-supervisor-config.schema.json"
ACCEPTANCE_SCHEMA = (
    SPELL_ROOT / "schemas" / "finite-stream-execution-acceptance.schema.json"
)


def _task_session_root() -> Path:
    candidates = (
        SPELL_ROOT.parent / "task-session",
        SPELL_ROOT.parents[1] / "arcana" / "task-session",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise RuntimeError(
        "cannot locate Task Session dependency: "
        + ", ".join(str(candidate) for candidate in candidates)
    )


FAST_ENTRY_PATH = _task_session_root() / "scripts" / "fast_execution_entry_guard.py"
SPEC = importlib.util.spec_from_file_location("task_session_chain", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {RUNNER_PATH}")
CHAIN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHAIN)
FAST_SPEC = importlib.util.spec_from_file_location(
    "task_session_fast_entry", FAST_ENTRY_PATH
)
if FAST_SPEC is None or FAST_SPEC.loader is None:
    raise RuntimeError(f"cannot load {FAST_ENTRY_PATH}")
FAST_ENTRY = importlib.util.module_from_spec(FAST_SPEC)
FAST_SPEC.loader.exec_module(FAST_ENTRY)


def supervisor_block(code: str, claim: str) -> dict[str, Any]:
    return {
        "status": "BLOCK",
        "terminal_code": code,
        "claim": claim,
        "next_task_session_selector": None,
        "next_fresh_epoch_unit": None,
        "next_route": None,
        "authority_effect": "none",
    }


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("epoch config escapes the repository root") from error
    content = resolved.read_bytes()
    return {
        "path": relative.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def verify_supervisor_inputs(config: dict[str, Any], root: Path) -> None:
    CHAIN.verify_exact_ref(root, config["work_pack_ref"])
    for reference in config["owner_input_refs"]:
        CHAIN.verify_exact_ref(root, reference)
    if config["max_epochs"] > len(config["captured_frontier"]):
        raise ValueError("maximum epochs exceeds the captured frontier")
    if config["epoch_policy"]["mode"] == "accepted-finite-stream":
        if config["max_epochs"] != len(config["captured_frontier"]):
            raise ValueError("accepted stream budget must equal the captured frontier")
        if (
            config["epoch_policy"]["max_task_session_requests"]
            != len(config["captured_frontier"])
        ):
            raise ValueError("accepted stream request budget must equal the frontier")
        accepted_stream_documents(config, root)


def _load_bound_document(
    root: Path, reference: dict[str, Any], label: str
) -> dict[str, Any]:
    try:
        return CHAIN.load_exact_document(root, reference)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} is invalid: {error}") from error


def accepted_stream_documents(
    config: dict[str, Any], root: Path
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    """Validate the one-time stream acceptance and real fast-entry receipt."""

    envelope = config["accepted_stream"]
    chain_config = _load_bound_document(
        root, envelope["chain_config_ref"], "accepted chain config"
    )
    chain_errors = CHAIN.schema_errors(
        chain_config, CHAIN.CONFIG_SCHEMA, "accepted chain config"
    )
    if chain_errors:
        raise ValueError("; ".join(chain_errors))
    manifest, preflight_receipt = CHAIN.preflight(chain_config, root)
    if manifest is None:
        raise ValueError(
            "accepted chain preflight "
            f"{preflight_receipt['terminal_code']}: {preflight_receipt['claim']}"
        )

    acceptance = _load_bound_document(
        root, envelope["execution_acceptance_ref"], "stream acceptance"
    )
    acceptance_errors = CHAIN.schema_errors(
        acceptance, ACCEPTANCE_SCHEMA, "stream acceptance"
    )
    if acceptance_errors:
        raise ValueError("; ".join(acceptance_errors))
    fast_request = _load_bound_document(
        root, envelope["initial_fast_entry_request_ref"], "fast-entry request"
    )
    fast_receipt = _load_bound_document(
        root, envelope["initial_fast_entry_receipt_ref"], "fast-entry receipt"
    )
    FAST_ENTRY.validate_fast_entry_receipt(fast_receipt, fast_request)

    exact_pairs = {
        "supervisor id": (acceptance["supervisor_id"], config["supervisor_id"]),
        "scope": (acceptance["scope_id"], config["scope_id"]),
        "work-pack id": (
            acceptance["work_pack_id"],
            fast_request["execution_policy"]["work_pack_id"],
        ),
        "semantic digest": (
            acceptance["work_pack_semantic_digest"],
            chain_config["approved_epoch"]["canonical_semantic_digest"],
        ),
        "fast-entry semantic digest": (
            fast_request["execution_policy"]["work_pack_semantic_digest"],
            acceptance["work_pack_semantic_digest"],
        ),
        "allowed-routes digest": (
            acceptance["allowed_routes_digest"],
            fast_request["execution_policy"]["allowed_routes_digest"],
        ),
        "frontier": (
            acceptance["captured_frontier"],
            config["captured_frontier"],
        ),
        "chain config ref": (
            acceptance["chain_config_ref"],
            envelope["chain_config_ref"],
        ),
        "fast-entry request ref": (
            acceptance["fast_entry_request_ref"],
            envelope["initial_fast_entry_request_ref"],
        ),
        "fast-entry receipt ref": (
            acceptance["fast_entry_receipt_ref"],
            envelope["initial_fast_entry_receipt_ref"],
        ),
        "request budget": (
            acceptance["max_task_session_requests"],
            config["epoch_policy"]["max_task_session_requests"],
        ),
        "risk ceiling": (acceptance["risk_ceiling"], config["risk_ceiling"]),
        "chain frontier": (
            chain_config["finite_frontier"],
            config["captured_frontier"],
        ),
        "chain budget": (
            chain_config["run_budget"]["max_task_session_requests"],
            config["epoch_policy"]["max_task_session_requests"],
        ),
        "policy frontier": (
            fast_request["execution_policy"]["frontier"],
            config["captured_frontier"],
        ),
        "selected unit": (
            fast_request["selected_unit"]["swu_id"],
            config["captured_frontier"][0],
        ),
        "source invocation": (
            fast_request["execution_binding"]["source_invocation_id"],
            acceptance["source_invocation_id"],
        ),
        "execution mode": (
            fast_request["execution_binding"]["execution_mode"],
            acceptance["execution_mode"],
        ),
        "automatic decisions": (
            fast_request["execution_binding"]["automatic_decisions"],
            acceptance["automatic_decisions"],
        ),
        "stop decisions": (
            fast_request["execution_binding"]["stop_decisions"],
            acceptance["stop_decisions"],
        ),
    }
    mismatches = [
        label for label, (actual, expected) in exact_pairs.items() if actual != expected
    ]
    if mismatches:
        raise ValueError("accepted stream differs: " + ", ".join(mismatches))
    if fast_receipt["decision"] != "proceed" or fast_receipt["code"] != "TASK_READY":
        raise ValueError("initial accepted fast-entry receipt is not TASK_READY")
    if manifest["canonical_plan_graph"]["finite_frontier"] != config[
        "captured_frontier"
    ]:
        raise ValueError("accepted manifest frontier differs from the supervisor")
    route_units = [
        route["frontier_swu"]
        for route in fast_request["execution_policy"]["allowed_routes"]
        if route["capability"] == "task-session"
        and route["mode"] in {"execute", "execute-one-swu"}
    ]
    if route_units != config["captured_frontier"]:
        raise ValueError("accepted policy lacks one ordered Task Session route per unit")
    return chain_config, manifest, acceptance, fast_request, fast_receipt


def load_epoch(
    path: Path, root: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    reference = exact_ref(root, path)
    epoch_config = CHAIN.load_json(CHAIN.verify_exact_ref(root, reference))
    errors = CHAIN.schema_errors(epoch_config, CHAIN.CONFIG_SCHEMA, "epoch config")
    if errors:
        raise ValueError("; ".join(errors))
    manifest, receipt = CHAIN.preflight(epoch_config, root)
    if manifest is None:
        raise ValueError(
            f"inner epoch preflight {receipt['terminal_code']}: {receipt['claim']}"
        )
    return reference, epoch_config, manifest


def validate_epoch_window(
    supervisor: dict[str, Any],
    epoch_config: dict[str, Any],
    manifest: dict[str, Any],
    completed_records: list[dict[str, Any]],
) -> None:
    ordinal = len(completed_records) + 1
    if ordinal > supervisor["max_epochs"]:
        raise ValueError("supervisor epoch budget is exhausted")
    frontier = supervisor["captured_frontier"]
    expected_unit = frontier[ordinal - 1]
    window = epoch_config.get("admission_window")
    if not isinstance(window, dict):
        raise ValueError("epoch config lacks a fresh-current-unit admission window")
    checks = {
        "supervisor id": (window.get("supervisor_id"), supervisor["supervisor_id"]),
        "epoch ordinal": (window.get("epoch_ordinal"), ordinal),
        "selected unit": (window.get("selected_unit"), expected_unit),
        "scope": (epoch_config.get("scope_id"), supervisor["scope_id"]),
        "epoch frontier": (epoch_config.get("finite_frontier"), [expected_unit]),
        "request budget": (
            epoch_config.get("run_budget", {}).get("max_task_session_requests"),
            1,
        ),
        "supervisor frontier digest": (
            window.get("supervisor_frontier_digest"),
            CHAIN.digest(frontier),
        ),
    }
    mismatches = [
        label for label, (actual, expected) in checks.items() if actual != expected
    ]
    if mismatches:
        raise ValueError("epoch window differs: " + ", ".join(mismatches))
    ready_frontier = manifest.get("fresh_epoch_ready_frontier")
    if ready_frontier is None:
        ready_frontier = manifest.get("canonical_plan_graph", {}).get(
            "finite_frontier"
        )
    expected_ready_frontier = frontier[ordinal - 1 :]
    if ready_frontier != expected_ready_frontier:
        raise ValueError("fresh ready frontier is not the captured remaining suffix")
    if window.get("observed_ready_frontier_digest") != CHAIN.digest(ready_frontier):
        raise ValueError("fresh ready-frontier digest differs")
    if CHAIN.RISK_ORDER[epoch_config["risk_ceiling"]] > CHAIN.RISK_ORDER[
        supervisor["risk_ceiling"]
    ]:
        raise ValueError("epoch risk ceiling exceeds the supervisor ceiling")
    if epoch_config["allowed_task_session_flags"] != supervisor[
        "allowed_task_session_flags"
    ]:
        raise ValueError("epoch flag allowlist differs from the supervisor")
    prior_epoch_ids = {item["epoch_id"] for item in completed_records}
    prior_manifest_digests = {
        item["manifest_ref"]["sha256"] for item in completed_records
    }
    prior_approval_digests = {
        item["epoch_approval_ref"]["sha256"] for item in completed_records
    }
    if epoch_config["approved_epoch"]["epoch_id"] in prior_epoch_ids:
        raise ValueError("fresh epoch reuses an earlier epoch id")
    if epoch_config["manifest_ref"]["sha256"] in prior_manifest_digests:
        raise ValueError("fresh epoch reuses an earlier manifest")
    approval_ref = epoch_config["approved_epoch"][
        "decision_gate_approval_receipt_ref"
    ]
    if approval_ref["sha256"] in prior_approval_digests:
        raise ValueError("fresh epoch reuses an earlier approval")


def inspect_inner_state(
    epoch_config: dict[str, Any], manifest: dict[str, Any], root: Path
) -> tuple[Path, dict[str, Any], list[Path]]:
    transitions_dir, state = CHAIN.open_chain_state(epoch_config, manifest, root)
    records = sorted(transitions_dir.glob("*.json"))
    if len(records) > 1 or state["request_count"] > 1:
        raise ValueError("a fresh epoch consumed more than one Task Session request")
    return transitions_dir, state, records


def completion_record(
    supervisor: dict[str, Any],
    epoch_ref: dict[str, Any],
    epoch_config: dict[str, Any],
    manifest: dict[str, Any],
    transition_path: Path,
    root: Path,
    previous_digest: str | None,
) -> dict[str, Any]:
    transition_record = CHAIN.load_json(transition_path)
    ordinal = epoch_config["admission_window"]["epoch_ordinal"]
    next_unit = (
        supervisor["captured_frontier"][ordinal]
        if ordinal < len(supervisor["captured_frontier"])
        else None
    )
    payload = {
        "schema_version": "task-session-until-blocker.supervisor-epoch-record/v1",
        "supervisor_id": supervisor["supervisor_id"],
        "epoch_ordinal": ordinal,
        "previous_epoch_digest": previous_digest,
        "epoch_id": epoch_config["approved_epoch"]["epoch_id"],
        "selected_unit": epoch_config["admission_window"]["selected_unit"],
        "epoch_config_ref": epoch_ref,
        "manifest_ref": epoch_config["manifest_ref"],
        "epoch_approval_ref": epoch_config["approved_epoch"][
            "decision_gate_approval_receipt_ref"
        ],
        "inner_transition_record_ref": exact_ref(root, transition_path),
        "transition_digest": transition_record["transition_digest"],
        "cursor": transition_record["transition"]["cursor"],
        "ready_frontier_digest": epoch_config["admission_window"][
            "observed_ready_frontier_digest"
        ],
        "next_fresh_epoch_unit": next_unit,
        "authority_effect": "none",
    }
    payload["epoch_digest"] = CHAIN.digest(payload)
    return payload


def replay_records(
    supervisor: dict[str, Any], root: Path, records_dir: Path
) -> list[dict[str, Any]]:
    paths = sorted(records_dir.glob("*.json"))
    expected_names = [f"{index:06d}.json" for index in range(1, len(paths) + 1)]
    if [path.name for path in paths] != expected_names:
        raise ValueError("supervisor epoch ledger has a gap")
    records: list[dict[str, Any]] = []
    previous_digest: str | None = None
    for ordinal, path in enumerate(paths, 1):
        observed = CHAIN.load_json(path)
        if observed.get("epoch_ordinal") != ordinal:
            raise ValueError("supervisor epoch ordinal differs from the ledger")
        if observed.get("previous_epoch_digest") != previous_digest:
            raise ValueError("supervisor epoch hash link is broken")
        epoch_path = CHAIN.verify_exact_ref(root, observed["epoch_config_ref"])
        epoch_ref, epoch_config, manifest = load_epoch(epoch_path, root)
        validate_epoch_window(supervisor, epoch_config, manifest, records)
        _, state, transition_paths = inspect_inner_state(
            epoch_config, manifest, root
        )
        if (
            state["status"] != "COMPLETE"
            or state["request_count"] != 1
            or state["visited"] != [observed["selected_unit"]]
            or len(transition_paths) != 1
        ):
            raise ValueError("recorded epoch is not a closed one-request epoch")
        expected = completion_record(
            supervisor,
            epoch_ref,
            epoch_config,
            manifest,
            transition_paths[0],
            root,
            previous_digest,
        )
        if observed != expected:
            raise ValueError("supervisor epoch record differs from replay")
        records.append(observed)
        previous_digest = observed["epoch_digest"]
    return records


def open_supervisor(
    config: dict[str, Any], root: Path
) -> tuple[Path, list[dict[str, Any]]]:
    state_dir = CHAIN.resolve_inside(
        root, config["state_directory"], must_exist=False
    )
    state_dir.mkdir(parents=True, exist_ok=True)
    records_dir = state_dir / "epochs"
    records_dir.mkdir(exist_ok=True)
    supervisor_path = state_dir / "supervisor.json"
    record = {
        "schema_version": "task-session-until-blocker.supervisor-state/v1",
        "config_digest": CHAIN.digest(config),
        "projection": {
            "supervisor_id": config["supervisor_id"],
            "scope_id": config["scope_id"],
            "work_pack_ref": config["work_pack_ref"],
            "owner_input_refs": config["owner_input_refs"],
            "captured_frontier": config["captured_frontier"],
            "max_epochs": config["max_epochs"],
            "risk_ceiling": config["risk_ceiling"],
        },
        "authority_effect": "none",
    }
    if not supervisor_path.exists():
        try:
            CHAIN.exclusive_write_json(supervisor_path, record)
        except FileExistsError:
            pass
    if CHAIN.load_json(supervisor_path) != record:
        raise ValueError("existing supervisor state differs from configuration")
    return records_dir, replay_records(config, root, records_dir)


def next_epoch_receipt(
    supervisor: dict[str, Any], records: list[dict[str, Any]]
) -> dict[str, Any]:
    if len(records) == len(supervisor["captured_frontier"]):
        return {
            "status": "COMPLETE",
            "terminal_code": "SUPERVISOR_COMPLETE",
            "claim": "every captured unit has one closed fresh epoch",
            "next_task_session_selector": None,
            "next_fresh_epoch_unit": None,
            "next_route": None,
            "completed_epochs": len(records),
            "authority_effect": "none",
        }
    if len(records) >= supervisor["max_epochs"]:
        return supervisor_block(
            "SUPERVISOR_BUDGET_EXHAUSTED",
            "the approved supervisor epoch budget ended before the captured frontier",
        )
    return {
        "status": "READY",
        "terminal_code": "NEXT_EPOCH_INPUT_REQUIRED",
        "claim": "a fresh readiness, selection, and approval epoch is required",
        "next_task_session_selector": None,
        "next_fresh_epoch_unit": supervisor["captured_frontier"][len(records)],
        "next_route": "work-pack-readiness-audit",
        "completed_epochs": len(records),
        "authority_effect": "none",
    }


def _accepted_fast_entry_result(
    config: dict[str, Any],
    root: Path,
    *,
    expected_unit: str,
    visited: list[str],
    request_ref: dict[str, Any],
    receipt_ref: dict[str, Any],
) -> dict[str, Any]:
    _, _, acceptance, initial_request, _ = accepted_stream_documents(config, root)
    request = _load_bound_document(root, request_ref, "current fast-entry request")
    receipt = _load_bound_document(root, receipt_ref, "current fast-entry receipt")
    FAST_ENTRY.validate_fast_entry_receipt(receipt, request)
    policy = request["execution_policy"]
    binding = request["execution_binding"]
    continuity = policy["completion_continuity"]
    completed_units = [item["unit_id"] for item in continuity["completed_prefix"]]
    checks = {
        "selected unit": (request["selected_unit"]["swu_id"], expected_unit),
        "entry unit": (request["execution_entry"]["selected_unit"], expected_unit),
        "binding unit": (binding["selected_unit"], expected_unit),
        "frontier": (policy["frontier"], config["captured_frontier"]),
        "completed prefix": (completed_units, visited),
        "continuity next unit": (continuity["next_unit"], expected_unit),
        "source invocation": (
            binding["source_invocation_id"],
            acceptance["source_invocation_id"],
        ),
        "execution mode": (binding["execution_mode"], "finite-frontier"),
        "work-pack id": (
            policy["work_pack_id"],
            initial_request["execution_policy"]["work_pack_id"],
        ),
        "semantic digest": (
            policy["work_pack_semantic_digest"],
            initial_request["execution_policy"]["work_pack_semantic_digest"],
        ),
        "allowed-routes digest": (
            policy["allowed_routes_digest"],
            initial_request["execution_policy"]["allowed_routes_digest"],
        ),
        "automatic decisions": (
            binding["automatic_decisions"],
            acceptance["automatic_decisions"],
        ),
        "stop decisions": (binding["stop_decisions"], acceptance["stop_decisions"]),
    }
    mismatches = [
        label for label, (actual, expected) in checks.items() if actual != expected
    ]
    if mismatches:
        return supervisor_block(
            "FAST_ENTRY_STREAM_BINDING_MISMATCH",
            "current fast-entry differs: " + ", ".join(mismatches),
        )
    if receipt["decision"] == "route-owner":
        result = supervisor_block(
            "OWNER_PREREQUISITE",
            "the next frozen unit requires its separately owned prerequisite",
        )
        result.update(
            next_fresh_epoch_unit=expected_unit,
            next_route=receipt["owner_packet"],
            completed_epochs=len(visited),
            fast_entry_request_ref=request_ref,
            fast_entry_receipt_ref=receipt_ref,
        )
        return result
    if receipt["decision"] != "proceed" or receipt["code"] != "TASK_READY":
        return supervisor_block(
            receipt["code"], receipt.get("blocker_detail") or "fast-entry blocked"
        )
    return {
        "status": "READY",
        "terminal_code": "TASK_READY",
        "claim": "one fresh Task Session is admitted inside the accepted stream",
        "next_task_session_selector": expected_unit,
        "next_fresh_epoch_unit": None,
        "next_route": "task-session",
        "completed_epochs": len(visited),
        "fast_entry_request_ref": request_ref,
        "fast_entry_receipt_ref": receipt_ref,
        "authorization_prompt_required": False,
        "authority_effect": "none",
    }


def supervise_accepted_stream(
    config: dict[str, Any],
    root: Path,
    *,
    transition_path: Path | None,
    fast_entry_request_path: Path | None,
    fast_entry_receipt_path: Path | None,
) -> dict[str, Any]:
    """Advance one accepted finite stream through one command surface."""

    chain_config, manifest, _, _, _ = accepted_stream_documents(config, root)
    transitions_dir, state = CHAIN.open_chain_state(chain_config, manifest, root)
    if transition_path is not None:
        transition_ref = exact_ref(root, transition_path)
        transition = _load_bound_document(root, transition_ref, "chain transition")
        prior_count = state["request_count"]
        receipt, next_state = CHAIN.evaluate_transition(
            chain_config, manifest, transition, state, root
        )
        if next_state["request_count"] == prior_count + 1:
            CHAIN.persist_transition(
                transitions_dir, transition, receipt, next_state
            )
        state = next_state
        if receipt["status"] == "BLOCK":
            receipt.update(completed_epochs=len(state["visited"]))
            return receipt
    elif state["request_count"] > 0:
        # A replay-safe status call is allowed after prior transitions.
        pass

    admission = CHAIN.admit_next_request(chain_config, manifest, state)
    if admission["status"] == "COMPLETE":
        return {
            "status": "COMPLETE",
            "terminal_code": "SUPERVISOR_COMPLETE",
            "claim": "every accepted-stream unit has a separate joined Task Session and closeout",
            "next_task_session_selector": None,
            "next_fresh_epoch_unit": None,
            "next_route": None,
            "completed_epochs": len(state["visited"]),
            "authority_effect": "none",
        }
    if admission["status"] != "READY":
        admission.update(completed_epochs=len(state["visited"]))
        return admission

    expected_unit = admission["next_task_session_selector"]
    if not state["visited"]:
        request_ref = config["accepted_stream"]["initial_fast_entry_request_ref"]
        receipt_ref = config["accepted_stream"]["initial_fast_entry_receipt_ref"]
    else:
        if (fast_entry_request_path is None) != (fast_entry_receipt_path is None):
            return supervisor_block(
                "FAST_ENTRY_PAIR_INCOMPLETE",
                "both current fast-entry request and receipt are required",
            )
        if fast_entry_request_path is None:
            result = {
                "status": "READY",
                "terminal_code": "FAST_ENTRY_INPUT_REQUIRED",
                "claim": "the next unit needs a fresh deterministic fast-entry projection",
                "next_task_session_selector": None,
                "next_fresh_epoch_unit": expected_unit,
                "next_route": "implementation-readiness:project-fast-entry",
                "completed_epochs": len(state["visited"]),
                "authorization_prompt_required": False,
                "authority_effect": "none",
            }
            return result
        request_ref = exact_ref(root, fast_entry_request_path)
        receipt_ref = exact_ref(root, fast_entry_receipt_path)
    return _accepted_fast_entry_result(
        config,
        root,
        expected_unit=expected_unit,
        visited=state["visited"],
        request_ref=request_ref,
        receipt_ref=receipt_ref,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--epoch-config", type=Path)
    parser.add_argument("--transition", type=Path)
    parser.add_argument("--fast-entry-request", type=Path)
    parser.add_argument("--fast-entry-receipt", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        supervisor = CHAIN.load_json(args.config)
        errors = CHAIN.schema_errors(
            supervisor, CONFIG_SCHEMA, "supervisor config"
        )
        if errors:
            raise ValueError("; ".join(errors))
        root = CHAIN.discover_repository_root(args.config)
        verify_supervisor_inputs(supervisor, root)
        if supervisor["epoch_policy"]["mode"] == "accepted-finite-stream":
            if args.epoch_config is not None:
                raise ValueError("accepted stream does not consume per-unit epoch configs")
            receipt = supervise_accepted_stream(
                supervisor,
                root,
                transition_path=args.transition,
                fast_entry_request_path=args.fast_entry_request,
                fast_entry_receipt_path=args.fast_entry_receipt,
            )
            print(json.dumps(receipt, sort_keys=True))
            return 0 if receipt["status"] in {"READY", "COMPLETE"} else 2
        if any(
            value is not None
            for value in (
                args.transition,
                args.fast_entry_request,
                args.fast_entry_receipt,
            )
        ):
            raise ValueError("fresh-current-unit mode does not consume stream inputs")
        records_dir, records = open_supervisor(supervisor, root)
        if args.epoch_config is None:
            receipt = next_epoch_receipt(supervisor, records)
            print(json.dumps(receipt, sort_keys=True))
            return 0
        supplied_ref = exact_ref(root, args.epoch_config)
        if records and supplied_ref == records[-1]["epoch_config_ref"]:
            receipt = next_epoch_receipt(supervisor, records)
            print(json.dumps(receipt, sort_keys=True))
            return 0
        epoch_ref, epoch_config, manifest = load_epoch(args.epoch_config, root)
        validate_epoch_window(supervisor, epoch_config, manifest, records)
        _, state, transition_paths = inspect_inner_state(
            epoch_config, manifest, root
        )
        if state["status"] == "BLOCK":
            raise ValueError(f"inner epoch blocked: {state.get('stop_code')}")
        if state["request_count"] == 0:
            admission = CHAIN.admit_next_request(epoch_config, manifest, state)
            admission.update(
                supervisor_id=supervisor["supervisor_id"],
                epoch_ordinal=len(records) + 1,
                epoch_config_ref=epoch_ref,
            )
            print(json.dumps(admission, sort_keys=True))
            return 0 if admission["status"] == "READY" else 2
        if (
            state["status"] != "COMPLETE"
            or state["request_count"] != 1
            or state["visited"] != [epoch_config["admission_window"]["selected_unit"]]
            or len(transition_paths) != 1
        ):
            raise ValueError("inner epoch is neither ready nor closed exactly once")
        previous_digest = records[-1]["epoch_digest"] if records else None
        record = completion_record(
            supervisor,
            epoch_ref,
            epoch_config,
            manifest,
            transition_paths[0],
            root,
            previous_digest,
        )
        record_path = records_dir / f"{len(records) + 1:06d}.json"
        CHAIN.exclusive_write_json(record_path, record)
        records.append(record)
        receipt = next_epoch_receipt(supervisor, records)
        receipt.update(
            closed_epoch_ordinal=record["epoch_ordinal"],
            closed_unit=record["selected_unit"],
            epoch_record_ref=exact_ref(root, record_path),
        )
        print(json.dumps(receipt, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps(supervisor_block("SUPERVISOR_INVALID", str(error)), sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
