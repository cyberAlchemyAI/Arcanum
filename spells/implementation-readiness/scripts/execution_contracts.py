#!/usr/bin/env python3
"""Deterministic contracts for Work-Pack-bound internal execution routes."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = SPELL_ROOT / "schemas"
POLICY_SCHEMA = SCHEMA_ROOT / "execution-policy.schema.json"
ENTRY_SCHEMA = SCHEMA_ROOT / "execution-entry-projection.schema.json"
BINDING_SCHEMA = SCHEMA_ROOT / "execution-intent-binding.schema.json"

PROTECTED_EFFECTS = {
    "destructive-or-irreversible",
    "external-network-or-message",
    "authority-or-promotion",
    "publication-or-deployment",
}


class ExecutionContractError(ValueError):
    """One stable fail-closed execution-contract diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def canonical_bytes(value: Any) -> bytes:
    _reject_noncanonical(value)
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _reject_noncanonical(value: Any, location: str = "$") -> None:
    if isinstance(value, float):
        raise ExecutionContractError(
            "NONCANONICAL_VALUE", f"floating-point value at {location}"
        )
    if value is None or isinstance(value, (str, int, bool)):
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_noncanonical(child, f"{location}/{index}")
        return
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ExecutionContractError(
                "NONCANONICAL_VALUE", f"non-string object key at {location}"
            )
        for key, child in value.items():
            _reject_noncanonical(child, f"{location}/{key}")
        return
    raise ExecutionContractError(
        "NONCANONICAL_VALUE", f"unsupported value at {location}"
    )


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ExecutionContractError("DOCUMENT_NOT_OBJECT", str(path))
    return value


def load_schema(path: Path) -> dict[str, Any]:
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    return schema


def _validate_schema(document: dict[str, Any], schema_path: Path, label: str) -> None:
    validator = Draft202012Validator(
        load_schema(schema_path), format_checker=FormatChecker()
    )
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or label
        raise ExecutionContractError(
            "SCHEMA_INVALID", f"{label} at {location}: {error.message}"
        )


def normalize_relative_path(value: str, label: str) -> str:
    if not value or "\\" in value:
        raise ExecutionContractError("PATH_UNSAFE", f"{label}: {value!r}")
    windows = PureWindowsPath(value)
    path = PurePosixPath(value)
    if path.is_absolute() or windows.is_absolute() or windows.drive:
        raise ExecutionContractError("PATH_UNSAFE", f"{label}: {value!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ExecutionContractError("PATH_UNSAFE", f"{label}: {value!r}")
    return path.as_posix()


def allowed_routes_digest(routes: list[dict[str, Any]]) -> str:
    return canonical_digest(routes)


def validate_completion_continuity(
    continuity: dict[str, Any],
    frontier: list[str],
    work_pack_semantic_digest: str,
) -> dict[str, Any]:
    payload = {
        key: value for key, value in continuity.items() if key != "continuity_digest"
    }
    if canonical_digest(payload) != continuity["continuity_digest"]:
        raise ExecutionContractError(
            "CONTINUITY_DIGEST_STALE", continuity["source_audit_id"]
        )
    if continuity["work_pack_semantic_digest"] != work_pack_semantic_digest:
        raise ExecutionContractError(
            "CONTINUITY_SEMANTIC_STALE", continuity["source_audit_id"]
        )
    completed = continuity["completed_prefix"]
    completed_units = [item["unit_id"] for item in completed]
    if completed_units != frontier[: len(completed_units)]:
        raise ExecutionContractError(
            "CONTINUITY_NON_PREFIX_COMPLETION", continuity["source_audit_id"]
        )
    receipt_identities = [
        (
            item["completion_artifact_ref"]["path"],
            item["completion_artifact_ref"]["sha256"],
            item["completion_artifact_ref"]["size_bytes"],
        )
        for item in completed
    ]
    if len(set(receipt_identities)) != len(receipt_identities):
        raise ExecutionContractError(
            "CONTINUITY_RECEIPT_REPLAY", continuity["source_audit_id"]
        )
    expected_next = (
        frontier[len(completed_units)]
        if len(completed_units) < len(frontier)
        else None
    )
    if continuity["next_unit"] != expected_next:
        raise ExecutionContractError(
            "CONTINUITY_CURSOR_CONTRADICTION", continuity["source_audit_id"]
        )
    return copy.deepcopy(continuity)


def validate_execution_policy(policy: dict[str, Any]) -> dict[str, Any]:
    _validate_schema(policy, POLICY_SCHEMA, "execution policy")
    frontier = policy["frontier"]
    if "completion_continuity" in policy:
        validate_completion_continuity(
            policy["completion_continuity"],
            frontier,
            policy["work_pack_semantic_digest"],
        )
    elif (
        policy["schema_version"] != "1.0.0"
        or len(frontier) != 1
    ):
        raise ExecutionContractError(
            "CONTINUITY_PROJECTION_MISSING", policy["work_pack_id"]
        )
    route_ids: set[str] = set()
    for route in policy["allowed_routes"]:
        route_id = route["route_id"]
        if route_id in route_ids:
            raise ExecutionContractError("ROUTE_ID_DUPLICATE", route_id)
        route_ids.add(route_id)
        if route["frontier_swu"] not in frontier:
            raise ExecutionContractError(
                "ROUTE_FRONTIER_UNKNOWN",
                f"{route_id}: {route['frontier_swu']}",
            )
        if route["effect_class"] in PROTECTED_EFFECTS:
            raise ExecutionContractError(
                "PROTECTED_ROUTE_EFFECT",
                f"{route_id}: {route['effect_class']}",
            )
        for index, path in enumerate(route["write_scope"]):
            normalize_relative_path(path, f"{route_id}.write_scope[{index}]")
        normalize_relative_path(route["expected_receipt"], f"{route_id}.expected_receipt")
    actual_digest = allowed_routes_digest(policy["allowed_routes"])
    if actual_digest != policy["allowed_routes_digest"]:
        raise ExecutionContractError(
            "ALLOWED_ROUTES_DIGEST_STALE",
            f"expected {actual_digest}, got {policy['allowed_routes_digest']}",
        )
    overlap = set(policy["automatic_decisions"]) & set(policy["stop_decisions"])
    if overlap:
        raise ExecutionContractError(
            "DECISION_CLASS_OVERLAP", ",".join(sorted(overlap))
        )
    if any(not command.strip() for command in policy["validation_commands"]):
        raise ExecutionContractError("VALIDATION_MISSING", "blank command")
    return copy.deepcopy(policy)


def route_map(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {route["route_id"]: route for route in policy["allowed_routes"]}


def _owner_for_route(route: dict[str, Any]) -> dict[str, str]:
    return {
        "capability": route["capability"],
        "mode": route["mode"],
        "target": route["target"],
    }


def validate_execution_entry(
    entry: dict[str, Any], policy: dict[str, Any]
) -> dict[str, Any]:
    validate_execution_policy(policy)
    _validate_schema(entry, ENTRY_SCHEMA, "execution entry")
    if entry["work_pack_id"] != policy["work_pack_id"]:
        raise ExecutionContractError("WORK_PACK_ID_MISMATCH", entry["work_pack_id"])
    if entry["work_pack_semantic_digest"] != policy["work_pack_semantic_digest"]:
        raise ExecutionContractError("WORK_PACK_SEMANTIC_STALE", entry["work_pack_id"])
    if entry["allowed_routes_digest"] != policy["allowed_routes_digest"]:
        raise ExecutionContractError("ALLOWED_ROUTES_DIGEST_STALE", entry["work_pack_id"])
    selected = entry["selected_unit"]
    if selected is not None and selected not in policy["frontier"]:
        raise ExecutionContractError("SELECTED_UNIT_OUTSIDE_FRONTIER", selected)

    state = entry["entry_state"]
    route_id = entry["route_id"]
    owner = entry["next_owner"]
    blocker = entry["blocker_code"]
    routes = route_map(policy)
    if state == "selection-ready":
        expected = {
            "capability": "implementation-readiness",
            "mode": "execute",
            "target": policy["work_pack_id"],
        }
        if selected is not None or route_id is not None or blocker is not None or owner != expected:
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION", "selection-ready projection"
            )
    elif state == "owner-prerequisite":
        if route_id not in routes or blocker is not None:
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION", "owner-prerequisite route"
            )
        route = routes[route_id]
        if selected is not None and route["frontier_swu"] != selected:
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION", "route frontier differs from selected unit"
            )
        if owner != _owner_for_route(route):
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION", "owner differs from route"
            )
    elif state in {"context-ready", "task-ready"}:
        if selected is None or route_id not in routes or blocker is not None:
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION", f"{state} route"
            )
        route = routes[route_id]
        if route["frontier_swu"] != selected:
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION", f"{state} route frontier differs"
            )
        if route["capability"] != "task-session" or owner != _owner_for_route(route):
            raise ExecutionContractError(
                "ENTRY_ROUTE_CONTRADICTION",
                f"{state} must name Task Session route",
            )
    elif state == "blocked":
        if blocker is None or route_id is not None:
            raise ExecutionContractError("ENTRY_ROUTE_CONTRADICTION", "blocked projection")
    return copy.deepcopy(entry)


def _write_scope_union(policy: dict[str, Any]) -> list[str]:
    return sorted(
        {
            normalize_relative_path(path, "write_scope_union")
            for route in policy["allowed_routes"]
            for path in route["write_scope"]
        }
    )


def _completion_continuity_digest(policy: dict[str, Any]) -> str:
    continuity = policy.get("completion_continuity")
    if continuity is not None:
        return continuity["continuity_digest"]
    return canonical_digest(
        {
            "legacy_explicit_single_unit_policy": policy["work_pack_id"],
            "frontier": policy["frontier"],
            "authority_effect": "none",
        }
    )


def build_execution_intent_binding(
    policy: dict[str, Any],
    entry: dict[str, Any],
    *,
    source_invocation_id: str,
    created_at: str,
    execution_mode: str,
) -> dict[str, Any]:
    validate_execution_entry(entry, policy)
    current_route = (
        copy.deepcopy(route_map(policy)[entry["route_id"]])
        if entry["route_id"] is not None
        else None
    )
    route_fingerprint = canonical_digest(
        current_route
        if current_route is not None
        else {
            "entry_state": entry["entry_state"],
            "selected_unit": entry["selected_unit"],
            "allowed_routes_digest": policy["allowed_routes_digest"],
        }
    )
    seed = {
        "schema_version": "1.1.0",
        "source_invocation_id": source_invocation_id,
        "created_at": created_at,
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "captured_frontier": copy.deepcopy(policy["frontier"]),
        "completion_continuity_digest": _completion_continuity_digest(policy),
        "selected_unit": entry["selected_unit"],
        "execution_mode": execution_mode,
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "current_route": current_route,
        "write_scope_union": _write_scope_union(policy),
        "validation_commands": copy.deepcopy(policy["validation_commands"]),
        "automatic_decisions": copy.deepcopy(policy["automatic_decisions"]),
        "stop_decisions": copy.deepcopy(policy["stop_decisions"]),
        "route_fingerprint": route_fingerprint,
        "authority_effect": "bounded-execution-only",
    }
    binding_id = f"wpeb-{canonical_digest(seed)[:24]}"
    binding = {**seed, "binding_id": binding_id}
    binding["binding_digest"] = canonical_digest(binding)
    validate_execution_binding(binding, policy, entry)
    return binding


def validate_execution_binding(
    binding: dict[str, Any],
    policy: dict[str, Any],
    entry: dict[str, Any],
) -> dict[str, Any]:
    validate_execution_entry(entry, policy)
    _validate_schema(binding, BINDING_SCHEMA, "execution intent binding")
    if binding["work_pack_id"] != policy["work_pack_id"]:
        raise ExecutionContractError("WORK_PACK_ID_MISMATCH", binding["work_pack_id"])
    if binding["work_pack_semantic_digest"] != policy["work_pack_semantic_digest"]:
        raise ExecutionContractError("WORK_PACK_SEMANTIC_STALE", binding["work_pack_id"])
    if binding["captured_frontier"] != policy["frontier"]:
        raise ExecutionContractError("FRONTIER_STALE", binding["work_pack_id"])
    if (
        binding["completion_continuity_digest"]
        != _completion_continuity_digest(policy)
    ):
        raise ExecutionContractError(
            "CONTINUITY_POLICY_STATE_MISMATCH", binding["work_pack_id"]
        )
    if binding["selected_unit"] != entry["selected_unit"]:
        raise ExecutionContractError("SELECTED_UNIT_STALE", binding["work_pack_id"])
    if binding["allowed_routes_digest"] != policy["allowed_routes_digest"]:
        raise ExecutionContractError("ALLOWED_ROUTES_DIGEST_STALE", binding["work_pack_id"])
    expected_route = (
        route_map(policy)[entry["route_id"]] if entry["route_id"] is not None else None
    )
    if binding["current_route"] != expected_route:
        raise ExecutionContractError("ROUTE_BINDING_STALE", binding["work_pack_id"])
    if binding["write_scope_union"] != _write_scope_union(policy):
        raise ExecutionContractError("WRITE_SCOPE_EXPANDED", binding["work_pack_id"])
    expected_fingerprint = canonical_digest(
        expected_route
        if expected_route is not None
        else {
            "entry_state": entry["entry_state"],
            "selected_unit": entry["selected_unit"],
            "allowed_routes_digest": policy["allowed_routes_digest"],
        }
    )
    if binding["route_fingerprint"] != expected_fingerprint:
        raise ExecutionContractError("ROUTE_FINGERPRINT_STALE", binding["work_pack_id"])
    digest_payload = {key: value for key, value in binding.items() if key != "binding_digest"}
    if binding["binding_digest"] != canonical_digest(digest_payload):
        raise ExecutionContractError("BINDING_DIGEST_STALE", binding["work_pack_id"])
    return copy.deepcopy(binding)


def match_bound_route(
    binding: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    route = binding.get("current_route")
    if route is None:
        raise ExecutionContractError("ROUTE_UNDECLARED", "binding has no current route")
    for key in ("route_id", "frontier_swu", "capability", "mode"):
        if candidate.get(key) != route[key]:
            raise ExecutionContractError("ROUTE_UNDECLARED", key)
    if candidate.get("target") != route["target"]:
        raise ExecutionContractError("ROUTE_TARGET_MISMATCH", route["route_id"])
    if candidate.get("write_scope") != route["write_scope"]:
        raise ExecutionContractError("ROUTE_WRITE_SCOPE_EXPANDED", route["route_id"])
    if candidate.get("effect_class") != route["effect_class"]:
        raise ExecutionContractError("ROUTE_EFFECT_MISMATCH", route["route_id"])
    if candidate.get("required_inputs") != route["required_inputs"]:
        raise ExecutionContractError("ROUTE_INPUT_MISMATCH", route["route_id"])
    if candidate.get("expected_receipt") != route["expected_receipt"]:
        raise ExecutionContractError("ROUTE_RECEIPT_MISMATCH", route["route_id"])
    return {
        "match": "matched",
        "authorization_source": "work-pack-binding",
        "authorization_prompt_required": False,
        "route_fingerprint": binding["route_fingerprint"],
    }
