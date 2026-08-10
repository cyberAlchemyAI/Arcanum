#!/usr/bin/env python3
"""Control one approved finite frontier without executing Task Session itself."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


SPELL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_SCHEMA = SPELL_ROOT / "schemas" / "chain-config.schema.json"
TRANSITION_SCHEMA = SPELL_ROOT / "schemas" / "chain-transition.schema.json"
NO_OP_SCHEMA = SPELL_ROOT / "schemas" / "closeout-no-op-proof.schema.json"
RISK_ORDER = {
    "read-only": 0,
    "bounded-write": 1,
    "browser": 2,
    "network": 3,
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, dict):
        raise ValueError(f"JSON object required: {path}")
    return document


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def schema_errors(document: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    return [
        f"{label} invalid at "
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def resolve_inside(root: Path, raw_path: str, must_exist: bool) -> Path:
    if (
        not raw_path
        or "\x00" in raw_path
        or "$" in raw_path
        or "*" in raw_path
        or "?" in raw_path
        or "\\" in raw_path
    ):
        raise ValueError(f"unsafe path: {raw_path}")
    path = PurePosixPath(raw_path)
    if path.is_absolute() or PureWindowsPath(raw_path).is_absolute() or ".." in path.parts:
        raise ValueError(f"path escapes repository: {raw_path}")
    root = root.resolve()
    try:
        candidate = (root / str(path)).resolve(strict=must_exist)
    except FileNotFoundError as error:
        raise ValueError(f"missing path: {raw_path}") from error
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"symlink or path escape: {raw_path}") from error
    return candidate


def verify_exact_ref(root: Path, reference: dict[str, Any]) -> Path:
    path = resolve_inside(root, reference["path"], must_exist=True)
    if not path.is_file():
        raise ValueError(f"exact artifact is not a file: {reference['path']}")
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise ValueError(f"digest mismatch: {reference['path']}")
    if len(content) != reference["size_bytes"]:
        raise ValueError(f"size mismatch: {reference['path']}")
    return path


def block(code: str, claim: str, *, next_route: str | None = None) -> dict[str, Any]:
    return {
        "status": "BLOCK",
        "terminal_code": code,
        "claim": claim,
        "next_task_session_selector": None,
        "next_route": next_route,
        "authority_effect": "none",
    }


def normalize_plan_semantic_manifest(
    manifest: dict[str, Any],
    config: dict[str, Any],
    audit_report: dict[str, Any] | None,
) -> dict[str, Any]:
    """Adapt a WPRA v2 manifest without weakening its frozen bindings."""
    if "epoch_binding" in manifest:
        return manifest

    required = {
        "manifest_id",
        "plan_epoch_id",
        "canonical_semantic_digest",
        "source_snapshot_digest",
        "ready_frontier",
        "completion_continuity",
        "allowed_routes",
        "allowed_routes_digest",
    }
    missing = sorted(name for name in required if name not in manifest)
    if missing:
        raise ValueError(f"WPRA v2 manifest missing: {', '.join(missing)}")
    if audit_report is None:
        raise ValueError("WPRA v2 manifest requires an exact audit report reference")

    approved = config["approved_epoch"]
    report_snapshot = audit_report.get("source_snapshot")
    report_checks = {
        "verdict": config["audit_verdict"],
        "flags": config["audit_flags"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": approved["canonical_semantic_digest"],
    }
    mismatches = [
        name for name, expected in report_checks.items()
        if audit_report.get(name) != expected
    ]
    if (
        not isinstance(report_snapshot, dict)
        or report_snapshot.get("digest") != approved["source_snapshot_digest"]
    ):
        mismatches.append("source_snapshot_digest")
    if audit_report.get("manifest") != manifest:
        mismatches.append("manifest")
    if mismatches:
        raise ValueError(
            "WPRA v2 audit report differs from approved epoch: "
            + ", ".join(mismatches)
        )
    if manifest["manifest_id"] != f"psm-{approved['audit_projection_digest'][:24]}":
        raise ValueError("WPRA v2 manifest id does not bind the audit projection")

    frontier = manifest["ready_frontier"]
    if (
        not isinstance(frontier, list)
        or not frontier
        or any(not isinstance(unit, str) or not unit for unit in frontier)
        or len(frontier) != len(set(frontier))
    ):
        raise ValueError("WPRA v2 ready frontier is not a unique non-empty sequence")
    continuity = manifest["completion_continuity"]
    if not isinstance(continuity, dict) or (
        continuity.get("plan_epoch_id") != manifest["plan_epoch_id"]
        or continuity.get("work_pack_semantic_digest")
        != manifest["canonical_semantic_digest"]
        or continuity.get("next_unit") != frontier[0]
        or continuity.get("authority_effect") != "none"
    ):
        raise ValueError("WPRA v2 continuity binding is invalid")
    if digest(manifest["allowed_routes"]) != manifest["allowed_routes_digest"]:
        raise ValueError("WPRA v2 allowed routes digest mismatch")

    task_routes: dict[str, dict[str, Any]] = {}
    closeout_routes: dict[str, dict[str, Any]] = {}
    for route in manifest["allowed_routes"]:
        if not isinstance(route, dict):
            raise ValueError("WPRA v2 allowed route is not an object")
        unit_id = route.get("frontier_swu")
        if unit_id not in frontier:
            raise ValueError("WPRA v2 allowed route is outside the ready frontier")
        if route.get("effect_class") != "repository-local-reversible":
            raise ValueError("WPRA v2 allowed route has an unsafe effect class")
        if route.get("capability") == "task-session":
            if (
                route.get("mode") != "execute"
                or route.get("target") != unit_id
                or unit_id in task_routes
            ):
                raise ValueError("WPRA v2 Task Session route is ambiguous or invalid")
            task_routes[unit_id] = route
        elif route.get("capability") == "invoke":
            if (
                route.get("mode") != "refresh-apply-approved"
                or route.get("target") != f"{unit_id}-closeout"
                or unit_id in closeout_routes
            ):
                raise ValueError("WPRA v2 closeout route is ambiguous or invalid")
            closeout_routes[unit_id] = route
        else:
            raise ValueError("WPRA v2 allowed route has an unsupported capability")
    if set(task_routes) != set(frontier) or set(closeout_routes) != set(frontier):
        raise ValueError("WPRA v2 routes do not cover the ready frontier exactly")

    normalized = dict(manifest)
    normalized["epoch_binding"] = {
        "epoch_id": manifest["plan_epoch_id"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": manifest["canonical_semantic_digest"],
        "source_snapshot_digest": manifest["source_snapshot_digest"],
    }
    normalized["canonical_plan_graph"] = {"finite_frontier": frontier}
    normalized["execution_bindings"] = [
        {
            "unit_id": unit_id,
            # WPRA v2 permits only repository-local reversible Task Session routes.
            "command": {"risk_class": "bounded-write"},
        }
        for unit_id in frontier
    ]
    # V2 binds Invoke's expected receipt path but not a static exact contract
    # digest. PASS closeouts remain supported; NO_OP continues to block unless a
    # future v2 manifest adds an exact closeout-contract binding.
    normalized["closeout_bindings"] = []
    return normalized


def preflight(
    config: dict[str, Any], repository_root: Path
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        manifest_path = verify_exact_ref(repository_root, config["manifest_ref"])
        verify_exact_ref(
            repository_root,
            config["approved_epoch"]["decision_gate_approval_receipt_ref"],
        )
        manifest = load_json(manifest_path)
        audit_report = None
        if "audit_report_ref" in config:
            audit_report = load_json(
                verify_exact_ref(repository_root, config["audit_report_ref"])
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return None, block("FROZEN_INPUT_MISMATCH", str(error))
    try:
        manifest = normalize_plan_semantic_manifest(manifest, config, audit_report)
    except ValueError as error:
        return None, block("MANIFEST_SHAPE_INVALID", str(error))

    if (
        manifest.get("authority_effect") != "none"
        or manifest.get("mutation_ready") is not False
        or manifest.get("selected_unit") is not None
    ):
        return None, block(
            "MANIFEST_AUTHORITY_INVALID",
            "manifest must remain no-authority, non-mutation-ready, and unselected",
        )
    if config["audit_verdict"] not in {"pass", "flag"}:
        return None, block("AUDIT_VERDICT_NOT_ALLOWED", "audit verdict is not consumable")
    if any(flag != "observability-residue" for flag in config["audit_flags"]):
        return None, block("FLAG_CLASS_NOT_ALLOWED", "audit flag class is not allowed")
    if config["audit_verdict"] == "flag" and not config["audit_flags"]:
        return None, block("FLAG_CLASS_MISSING", "flag verdict has no named flag class")

    approved = config["approved_epoch"]
    epoch = manifest.get("epoch_binding", {})
    comparisons = {
        "epoch_id": approved["epoch_id"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": approved["canonical_semantic_digest"],
        "source_snapshot_digest": approved["source_snapshot_digest"],
    }
    mismatches = [
        name for name, expected in comparisons.items() if epoch.get(name) != expected
    ]
    if mismatches:
        return None, block(
            "EPOCH_BINDING_MISMATCH",
            f"approved epoch differs from manifest: {', '.join(mismatches)}",
        )
    if approved["approval_status"] != "approved":
        return None, block("EPOCH_APPROVAL_MISSING", "epoch approval is absent")

    manifest_frontier = (
        manifest.get("canonical_plan_graph", {}).get("finite_frontier")
    )
    if manifest_frontier != config["finite_frontier"]:
        return None, block(
            "FRONTIER_MISMATCH",
            "configured frontier differs from the audited manifest frontier",
        )
    budget = config["run_budget"]["max_task_session_requests"]
    if budget > len(config["finite_frontier"]):
        return None, block(
            "BUDGET_INVALID",
            "request budget exceeds the finite audited frontier",
        )
    ceiling = RISK_ORDER[config["risk_ceiling"]]
    for unit in manifest.get("execution_bindings", []):
        risk = unit.get("command", {}).get("risk_class")
        if risk not in RISK_ORDER or RISK_ORDER[risk] > ceiling:
            return None, block(
                "RISK_CEILING_EXCEEDED",
                f"unit {unit.get('unit_id')} exceeds the approved risk ceiling",
            )
    return manifest, {
        "status": "PASS",
        "terminal_code": "CHAIN_PREFLIGHT_READY",
        "claim": "approved finite epoch is consumable",
        "next_task_session_selector": config["finite_frontier"][0],
        "next_route": "task-session",
        "authority_effect": "none",
    }


def initial_state(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "chain_id": config["chain_id"],
        "epoch_id": config["approved_epoch"]["epoch_id"],
        "manifest_digest": config["approved_epoch"]["audit_projection_digest"],
        "frontier": config["finite_frontier"],
        "visited": [],
        "cursors": [],
        "request_count": 0,
        "last_transition_digest": None,
        "last_selector": None,
        "status": "ACTIVE",
        "next_selector": config["finite_frontier"][0],
        "stop_code": None,
        "authority_effect": "none",
    }


def admit_next_request(
    config: dict[str, Any], manifest: dict[str, Any], state: dict[str, Any]
) -> dict[str, Any]:
    if state["status"] == "COMPLETE":
        return {
            "status": "COMPLETE",
            "terminal_code": "CHAIN_COMPLETE",
            "claim": "every approved-frontier unit has a joined closeout",
            "next_task_session_selector": None,
            "next_route": None,
            "authority_effect": "none",
        }
    if state["status"] == "BLOCK":
        return block("CHAIN_ALREADY_BLOCKED", "chain is already terminal")
    if state["epoch_id"] != config["approved_epoch"]["epoch_id"]:
        return block("EPOCH_BINDING_MISMATCH", "state epoch differs from approval")
    if state["frontier"] != config["finite_frontier"]:
        return block("FRONTIER_DRIFT", "persisted frontier differs from approval")
    if state["request_count"] >= config["run_budget"]["max_task_session_requests"]:
        return block("BUDGET_EXHAUSTED", "approved request budget is exhausted")
    selector = state["next_selector"]
    if selector is None or selector in state["visited"]:
        return block("SELECTOR_INVALID", "no novel approved selector is available")
    bound = next(
        (
            unit
            for unit in manifest["execution_bindings"]
            if unit["unit_id"] == selector
        ),
        None,
    )
    if bound is None:
        return block("SELECTOR_OUTSIDE_MANIFEST", "selector is absent from manifest")
    if RISK_ORDER[bound["command"]["risk_class"]] > RISK_ORDER[config["risk_ceiling"]]:
        return block("RISK_CEILING_EXCEEDED", "selector exceeds approved risk")
    return {
        "status": "READY",
        "terminal_code": "NEXT_SELECTOR_READY",
        "claim": "exactly one approved Task Session request is legal",
        "next_task_session_selector": selector,
        "request_ordinal": state["request_count"] + 1,
        "next_route": "task-session",
        "authority_effect": "none",
    }


def _exact_inventory(items: list[dict[str, str]]) -> list[tuple[str, str]]:
    return sorted((item["path"], item["sha256"]) for item in items)


def validate_no_op(
    proof: Any,
    *,
    selector: str,
    expected_successor: str | None,
    manifest: dict[str, Any],
    verification_receipt: dict[str, Any] | None,
) -> list[str]:
    errors = schema_errors(proof, NO_OP_SCHEMA, "NO_OP proof")
    if errors:
        return errors
    assert isinstance(proof, dict)
    if proof["unit_id"] != selector:
        errors.append("NO_OP proof unit does not match selector")
    if _exact_inventory(proof["before_inventory"]) != _exact_inventory(
        proof["after_inventory"]
    ):
        errors.append("NO_OP before and after inventories differ")
    closeout = next(
        (
            item
            for item in manifest["closeout_bindings"]
            if item["unit_id"] == selector
        ),
        None,
    )
    expected_contract = (
        closeout.get("owner_receipt_contract_ref", {}).get("artifact_ref")
        if closeout
        else None
    )
    if proof["closeout_contract_ref"] != expected_contract:
        errors.append("NO_OP proof is not bound to the approved closeout contract")
    router = proof["continuation_router_verification"]
    if router["canonical_successor"] != expected_successor:
        errors.append("NO_OP proof successor differs from the finite frontier")
    if verification_receipt is None or router["receipt_ref"] != verification_receipt:
        errors.append("NO_OP proof does not join the supplied router verification")
    return errors


def evaluate_transition(
    config: dict[str, Any],
    manifest: dict[str, Any],
    transition: dict[str, Any],
    state: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    next_state = json.loads(json.dumps(state))
    input_errors = schema_errors(transition, TRANSITION_SCHEMA, "transition")
    if input_errors:
        next_state.update(status="BLOCK", next_selector=None, stop_code="TRANSITION_INVALID")
        return block("TRANSITION_INVALID", "; ".join(input_errors)), next_state

    admission = admit_next_request(config, manifest, state)
    if admission["status"] != "READY":
        next_state.update(
            status="BLOCK",
            next_selector=None,
            stop_code=admission["terminal_code"],
        )
        return admission, next_state

    expected_selector = admission["next_task_session_selector"]
    expected_ordinal = admission["request_ordinal"]
    transition_payload = dict(transition)
    supplied_digest = transition_payload.pop("transition_digest")
    transition_digest = digest(transition_payload)
    next_state["request_count"] += 1
    next_state["last_transition_digest"] = transition_digest
    next_state["last_selector"] = transition["selector"]

    if supplied_digest is not None and supplied_digest != transition_digest:
        next_state.update(
            status="BLOCK",
            next_selector=None,
            stop_code="TRANSITION_DIGEST_MISMATCH",
        )
        return block(
            "TRANSITION_DIGEST_MISMATCH",
            "supplied transition digest is not canonical",
        ), next_state

    checks = (
        (
            transition["chain_id"] != config["chain_id"],
            "CHAIN_ID_MISMATCH",
            "transition chain id differs from configuration",
        ),
        (
            transition["epoch_id"] != state["epoch_id"],
            "EPOCH_BINDING_MISMATCH",
            "transition epoch differs from persisted state",
        ),
        (
            transition["previous_transition_digest"]
            != state["last_transition_digest"],
            "TRANSITION_LINK_MISMATCH",
            "transition does not hash-link to the current chain head",
        ),
        (
            transition["request_ordinal"] != expected_ordinal,
            "REQUEST_ORDINAL_MISMATCH",
            "transition request ordinal is not the next durable ordinal",
        ),
        (
            transition["selector"] != expected_selector,
            "SELECTOR_OUT_OF_ORDER",
            "transition selector is not the unique expected selector",
        ),
        (
            transition["cursor"] in state["cursors"],
            "CURSOR_REPEATED",
            "continuity cursor was already consumed",
        ),
        (
            transition["observed_frontier_digest"]
            != digest(config["finite_frontier"]),
            "FRONTIER_DRIFT",
            "transition observed a different finite frontier",
        ),
    )
    for failed, code, claim in checks:
        if failed:
            next_state.update(status="BLOCK", next_selector=None, stop_code=code)
            return block(code, claim), next_state

    bound = next(
        unit
        for unit in manifest["execution_bindings"]
        if unit["unit_id"] == expected_selector
    )
    if (
        transition["risk_class"] != bound["command"]["risk_class"]
        or RISK_ORDER[transition["risk_class"]] > RISK_ORDER[config["risk_ceiling"]]
    ):
        next_state.update(
            status="BLOCK",
            next_selector=None,
            stop_code="RISK_CEILING_EXCEEDED",
        )
        return block(
            "RISK_CEILING_EXCEEDED",
            "transition risk differs from or exceeds the approved binding",
        ), next_state

    next_state["cursors"].append(transition["cursor"])

    if transition["task_session_result"] == "FLAG":
        flags = transition["task_session_flags"]
        if not flags or any(
            flag not in config["allowed_task_session_flags"] for flag in flags
        ):
            next_state.update(
                status="BLOCK", next_selector=None, stop_code="FLAG_CLASS_NOT_ALLOWED"
            )
            return block(
                "FLAG_CLASS_NOT_ALLOWED",
                "Task Session flag is absent or outside the approval allowlist",
            ), next_state
    elif transition["task_session_flags"]:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="FLAG_STATUS_MISMATCH"
        )
        return block(
            "FLAG_STATUS_MISMATCH",
            "Task Session flags are present without a FLAG result",
        ), next_state

    if transition["task_session_result"] == "BLOCK":
        compensation = config["compensation"]
        next_state.update(status="BLOCK", next_selector=None)
        if compensation["mode"] == "owner-routed":
            next_state["stop_code"] = "COMPENSATION_OWNER_ROUTE_REQUIRED"
            return block(
                "COMPENSATION_OWNER_ROUTE_REQUIRED",
                "chain stopped before compensation; the named owner must decide",
                next_route=compensation["owner_ref"],
            ), next_state
        next_state["stop_code"] = "TASK_SESSION_BLOCK"
        return block("TASK_SESSION_BLOCK", "Task Session returned BLOCK"), next_state

    closeout = transition["closeout"]
    current_index = len(state["visited"])
    expected_successor = (
        config["finite_frontier"][current_index + 1]
        if current_index + 1 < len(config["finite_frontier"])
        else None
    )
    if closeout["result"] == "PASS":
        if (
            closeout["owner_receipt_ref"] is None
            or closeout["continuation_router_verification_receipt_ref"] is None
            or closeout["no_op_proof"] is not None
        ):
            next_state.update(
                status="BLOCK", next_selector=None, stop_code="OWNER_JOIN_MISSING"
            )
            return block(
                "OWNER_JOIN_MISSING",
                "PASS closeout requires owner and router receipts only",
            ), next_state
    elif closeout["result"] == "NO_OP":
        errors = validate_no_op(
            closeout["no_op_proof"],
            selector=expected_selector,
            expected_successor=expected_successor,
            manifest=manifest,
            verification_receipt=closeout[
                "continuation_router_verification_receipt_ref"
            ],
        )
        if errors or closeout["owner_receipt_ref"] is not None:
            next_state.update(
                status="BLOCK", next_selector=None, stop_code="NO_OP_PROOF_INVALID"
            )
            return block("NO_OP_PROOF_INVALID", "; ".join(errors) or "owner receipt conflicts with NO_OP"), next_state
    else:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="CLOSEOUT_BLOCK"
        )
        return block("CLOSEOUT_BLOCK", "closeout returned BLOCK"), next_state

    successor = transition["successor"]
    if successor["scope_digest"] != config["approved_epoch"]["audit_projection_digest"]:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="SUCCESSOR_SCOPE_MISMATCH"
        )
        return block(
            "SUCCESSOR_SCOPE_MISMATCH",
            "successor scope differs from the approved projection",
        ), next_state
    expected_count = 0 if expected_successor is None else 1
    if successor["candidate_count"] != expected_count:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="SUCCESSOR_NON_UNIQUE"
        )
        return block(
            "SUCCESSOR_NON_UNIQUE",
            "successor candidate count is not exact",
        ), next_state
    if (
        successor["unit_id"] != expected_successor
        or successor["declared"] is not True
        or successor["dependency_ready"] is not True
    ):
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="SUCCESSOR_INVALID"
        )
        return block(
            "SUCCESSOR_INVALID",
            "successor is missing, out of order, undeclared, or not dependency-ready",
        ), next_state

    next_state["visited"].append(expected_selector)
    next_state["next_selector"] = expected_successor
    if expected_successor is None:
        next_state.update(status="COMPLETE", stop_code="CHAIN_COMPLETE")
        status = "COMPLETE"
        code = "CHAIN_COMPLETE"
        next_route = None
    else:
        next_state.update(status="ACTIVE", stop_code=None)
        status = "PASS"
        code = "NEXT_SELECTOR_READY"
        next_route = "task-session"
    return {
        "status": status,
        "terminal_code": code,
        "claim": "transition joined and finite frontier advanced",
        "transition_digest": transition_digest,
        "next_task_session_selector": expected_successor,
        "next_route": next_route,
        "authority_effect": "none",
    }, next_state


def exclusive_write_json(path: Path, document: dict[str, Any]) -> None:
    payload = json.dumps(document, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, payload)
    finally:
        os.close(descriptor)


def open_chain_state(
    config: dict[str, Any], repository_root: Path
) -> tuple[Path, dict[str, Any]]:
    state_dir = resolve_inside(
        repository_root, config["state_directory"], must_exist=False
    )
    state_dir.mkdir(parents=True, exist_ok=True)
    transitions_dir = state_dir / "transitions"
    transitions_dir.mkdir(exist_ok=True)
    chain_path = state_dir / "chain.json"
    config_projection = {
        "chain_id": config["chain_id"],
        "scope_id": config["scope_id"],
        "epoch_id": config["approved_epoch"]["epoch_id"],
        "manifest_digest": config["approved_epoch"]["audit_projection_digest"],
        "frontier": config["finite_frontier"],
        "budget": config["run_budget"],
        "risk_ceiling": config["risk_ceiling"],
    }
    chain_record = {
        "schema_version": "1.0.0",
        "config_digest": digest(config_projection),
        "projection": config_projection,
    }
    if not chain_path.exists():
        try:
            exclusive_write_json(chain_path, chain_record)
        except FileExistsError:
            pass
    if load_json(chain_path) != chain_record:
        raise ValueError("existing chain record differs from approved configuration")

    records = sorted(transitions_dir.glob("*.json"))
    if not records:
        return transitions_dir, initial_state(config)
    expected_ordinals = [f"{index:06d}.json" for index in range(1, len(records) + 1)]
    if [path.name for path in records] != expected_ordinals:
        raise ValueError("transition ledger has a gap or unexpected filename")
    previous_digest = None
    state = initial_state(config)
    for path in records:
        record = load_json(path)
        if record.get("previous_transition_digest") != previous_digest:
            raise ValueError("transition ledger hash link is broken")
        previous_digest = record.get("transition_digest")
        state = record["state_after"]
    if state["last_transition_digest"] != previous_digest:
        raise ValueError("transition ledger head differs from state")
    return transitions_dir, state


def persist_transition(
    transitions_dir: Path,
    transition: dict[str, Any],
    receipt: dict[str, Any],
    state: dict[str, Any],
) -> Path:
    ordinal = state["request_count"]
    path = transitions_dir / f"{ordinal:06d}.json"
    record = {
        "schema_version": "1.0.0",
        "transition_id": transition["transition_id"],
        "transition_digest": state["last_transition_digest"],
        "previous_transition_digest": transition["previous_transition_digest"],
        "receipt": receipt,
        "state_after": state,
    }
    exclusive_write_json(path, record)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--transition", type=Path)
    return parser.parse_args()


def discover_repository_root(config_path: Path) -> Path:
    current = config_path.resolve().parent
    while current.parent != current and not (current / ".git").exists():
        current = current.parent
    if not (current / ".git").exists():
        raise ValueError("repository root could not be discovered")
    return current


def main() -> int:
    args = parse_args()
    config = load_json(args.config)
    errors = schema_errors(config, CONFIG_SCHEMA, "chain config")
    if errors:
        raise SystemExit("\n".join(errors))
    repository_root = discover_repository_root(args.config)
    manifest, preflight_receipt = preflight(config, repository_root)
    if manifest is None:
        print(json.dumps(preflight_receipt, sort_keys=True))
        return 2
    try:
        transitions_dir, state = open_chain_state(config, repository_root)
    except ValueError as error:
        print(json.dumps(block("CHAIN_STATE_INVALID", str(error)), sort_keys=True))
        return 2
    if args.transition is None:
        receipt = admit_next_request(config, manifest, state)
        print(json.dumps(receipt, sort_keys=True))
        return 0 if receipt["status"] in {"READY", "COMPLETE"} else 2
    transition = load_json(args.transition)
    receipt, next_state = evaluate_transition(config, manifest, transition, state)
    if next_state["request_count"] == state["request_count"]:
        print(json.dumps(receipt, sort_keys=True))
        return 2
    try:
        ledger_path = persist_transition(
            transitions_dir, transition, receipt, next_state
        )
    except FileExistsError:
        receipt = block(
            "TRANSITION_COLLISION",
            "exclusive-create refused an existing transition ordinal",
        )
        print(json.dumps(receipt, sort_keys=True))
        return 2
    receipt["ledger_path"] = str(ledger_path.relative_to(repository_root))
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["status"] in {"PASS", "COMPLETE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
