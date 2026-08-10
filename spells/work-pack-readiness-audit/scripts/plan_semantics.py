#!/usr/bin/env python3
"""Canonical semantic-plan normalization shared by audit and selection.

Exact artifact hashes remain provenance evidence.  Plan identity is derived from
the normalized values addressed by declared JSON Pointers plus the closed unit
contracts.  This lets receipt-owned lifecycle fields change without silently
changing an approved plan epoch.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


NORMALIZER_VERSION = "1.0.0"


class PlanSemanticError(ValueError):
    """A fail-closed semantic normalization error."""


def canonical_bytes(value: Any) -> bytes:
    _reject_unsupported(value)
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _reject_unsupported(value: Any, location: str = "$") -> None:
    if isinstance(value, float):
        raise PlanSemanticError(f"floating-point value is forbidden at {location}")
    if value is None or isinstance(value, (str, int, bool)):
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_unsupported(child, f"{location}/{index}")
        return
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise PlanSemanticError(f"non-string object key at {location}")
        for key, child in value.items():
            _reject_unsupported(child, f"{location}/{key}")
        return
    raise PlanSemanticError(
        f"non-JSON value {type(value).__name__} is forbidden at {location}"
    )


def resolve_json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise PlanSemanticError(f"JSON Pointer must start with '/': {pointer}")
    current = document
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            try:
                index = int(token)
                if str(index) != token or index < 0:
                    raise ValueError
                current = current[index]
            except (ValueError, IndexError) as error:
                raise PlanSemanticError(
                    f"unresolved JSON Pointer: {pointer}"
                ) from error
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            raise PlanSemanticError(f"unresolved JSON Pointer: {pointer}")
    _reject_unsupported(current, pointer or "$")
    return current


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PlanSemanticError(f"cannot load semantic source {path}: {error}") from error
    if not isinstance(value, dict):
        raise PlanSemanticError(f"semantic source must be a JSON object: {path}")
    return value


def binding_payload(binding: dict[str, Any] | None, repository_root: Path) -> Any:
    if binding is None:
        return None
    reference = binding.get("artifact_ref")
    if not isinstance(reference, dict) or not isinstance(reference.get("path"), str):
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} lacks an artifact path"
        )
    path = repository_root / reference["path"]
    document = _load_object(path)
    selector = binding.get("selector")
    if not isinstance(selector, str):
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} lacks a selector"
        )
    value = resolve_json_pointer(document, selector)
    return {
        "binding_id": binding["binding_id"],
        "owner_ref": binding["owner_ref"],
        "source_path": reference["path"],
        "selector": selector,
        "selected_value": value,
    }


def opaque_artifact_binding_payload(binding: dict[str, Any]) -> dict[str, Any]:
    """Normalize one non-JSON exact artifact without reading its contents."""

    if binding.get("binding_mode") != "opaque-exact-artifact":
        raise PlanSemanticError(
            "unsupported binding mode: "
            f"{binding.get('binding_mode', '<missing>')}"
        )
    reference = binding.get("artifact_ref")
    if not isinstance(reference, dict):
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} lacks an artifact ref"
        )
    required = {"path", "sha256", "size_bytes"}
    if set(reference) != required:
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} has an invalid exact artifact ref"
        )
    if not isinstance(reference["path"], str):
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} has a non-string artifact path"
        )
    if not isinstance(reference["sha256"], str) or len(reference["sha256"]) != 64:
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} has an invalid artifact digest"
        )
    if not isinstance(reference["size_bytes"], int) or isinstance(
        reference["size_bytes"], bool
    ) or reference["size_bytes"] < 0:
        raise PlanSemanticError(
            f"binding {binding.get('binding_id', '<unknown>')} has an invalid artifact size"
        )
    return {
        "binding_id": binding["binding_id"],
        "owner_ref": binding["owner_ref"],
        "binding_mode": "opaque-exact-artifact",
        "artifact_ref": {
            "path": reference["path"],
            "sha256": reference["sha256"],
            "size_bytes": reference["size_bytes"],
        },
    }


def _normalized_binding_tree(value: Any, repository_root: Path) -> Any:
    if isinstance(value, dict):
        binding_shape = {"binding_id", "owner_ref", "artifact_ref"}
        if binding_shape <= set(value):
            if "binding_mode" in value:
                return opaque_artifact_binding_payload(value)
            if "selector" not in value:
                raise PlanSemanticError(
                    f"binding {value.get('binding_id', '<unknown>')} lacks a selector"
                )
        if {"binding_id", "owner_ref", "artifact_ref", "selector"} <= set(value):
            return binding_payload(value, repository_root)
        return {
            key: _normalized_binding_tree(child, repository_root)
            for key, child in sorted(value.items())
        }
    if isinstance(value, list):
        return [_normalized_binding_tree(child, repository_root) for child in value]
    _reject_unsupported(value)
    return value


def _assert_unique_binding_ids(config: dict[str, Any]) -> None:
    observed: set[str] = set()

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            binding_shape = {"binding_id", "owner_ref", "artifact_ref"}
            if binding_shape <= set(value):
                binding_id = value["binding_id"]
                if binding_id in observed:
                    raise PlanSemanticError(f"duplicate binding id: {binding_id}")
                observed.add(binding_id)
                return
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(config)


def validate_execution_policy(
    policy: dict[str, Any], unit_ids: set[str]
) -> dict[str, Any]:
    """Validate the closed Work-Pack route projection before epoch hashing."""

    routes = policy["allowed_routes"]
    if canonical_digest(routes) != policy["allowed_routes_digest"]:
        raise PlanSemanticError("allowed-routes digest does not match canonical routes")
    route_ids: set[str] = set()
    for route in routes:
        route_id = route["route_id"]
        if route_id in route_ids:
            raise PlanSemanticError(f"duplicate allowed route id: {route_id}")
        route_ids.add(route_id)
        if route["frontier_swu"] not in unit_ids:
            raise PlanSemanticError(
                f"allowed route frontier is unknown: {route['frontier_swu']}"
            )
        for raw in [*route["write_scope"], route["expected_receipt"]]:
            path = PurePosixPath(raw)
            windows = PureWindowsPath(raw)
            if (
                not raw
                or "\\" in raw
                or path.is_absolute()
                or windows.is_absolute()
                or windows.drive
                or any(part in {"", ".", ".."} for part in path.parts)
            ):
                raise PlanSemanticError(f"allowed route path escape: {raw}")
    overlap = set(policy["automatic_decisions"]) & set(policy["stop_decisions"])
    if overlap:
        raise PlanSemanticError(
            f"automatic and stop decisions overlap: {','.join(sorted(overlap))}"
        )
    return policy


def build_plan_semantics(
    config: dict[str, Any], repository_root: Path
) -> dict[str, Any]:
    """Return closed component/unit payloads and deterministic digests."""

    if config.get("admission_timing") != "selected-unit-at-task-session":
        raise PlanSemanticError("plan semantic normalizer requires the opt-in profile")
    _assert_unique_binding_ids(config)
    semantic = config["authority_bindings"]["semantic_bindings"]
    execution = config["execution_bindings"]
    execution_policy = validate_execution_policy(
        config["execution_policy"], {unit["unit_id"] for unit in execution}
    )
    closeout_by_unit = {
        item["unit_id"]: item for item in config["closeout_bindings"]
    }

    components = {
        "objective": binding_payload(config["objective_ref"], repository_root),
        "owner": {
            "semantic": binding_payload(semantic["owner"], repository_root),
            "canonical_authority_refs": [
                binding_payload(binding, repository_root)
                for binding in config["authority_bindings"][
                    "canonical_authority_refs"
                ]
            ],
            "material_producers": [
                {
                    "unit_id": unit["unit_id"],
                    "producer_owner_ref": unit["material_package"][
                        "producer_owner_ref"
                    ],
                    "lifecycle_owner": unit["lifecycle_owner"],
                    "authority_class": unit["authority_class"],
                    "publication_class": unit["publication_class"],
                }
                for unit in execution
            ],
            "approval_owner_ref": config["approval_policy"]["approval_owner_ref"],
        },
        "graph": [
            {
                "task_id": unit["task_id"],
                "swu_id": unit["swu_id"],
                "unit_id": unit["unit_id"],
                "dependencies": unit["dependencies"],
                "canonical_successors": unit["canonical_successors"],
            }
            for unit in execution
        ],
        "material": {
            "semantic": binding_payload(semantic["material"], repository_root),
            "units": [
                {
                    "unit_id": unit["unit_id"],
                    "material_writes": unit["material_writes"],
                    "execution_outputs": unit["execution_outputs"],
                    "allowed_writes": unit["allowed_writes"],
                    "attempt_contract": unit["attempt_contract"],
                    "producer_owner_ref": unit["material_package"][
                        "producer_owner_ref"
                    ],
                }
                for unit in execution
            ],
        },
        "validation": {
            "semantic": binding_payload(semantic["validation"], repository_root),
            "commands": [
                {
                    "unit_id": unit["unit_id"],
                    "command": unit["command"],
                    "validation_contracts": unit["validation_contracts"],
                }
                for unit in execution
            ],
        },
        "receipt": {
            "semantic": binding_payload(semantic["receipt"], repository_root),
            "bindings": _normalized_binding_tree(
                config["receipt_bindings"], repository_root
            ),
        },
        "closeout": {
            "semantic": binding_payload(semantic["closeout"], repository_root),
            "bindings": _normalized_binding_tree(
                config["closeout_bindings"], repository_root
            ),
        },
        "runtime": {
            "requested_task_session_execution_mode": config["runtime_binding"][
                "requested_task_session_execution_mode"
            ]
        },
        "execution_policy": execution_policy,
        "frontier": [unit["unit_id"] for unit in execution],
        "risk_budget": {
            "risk_policy_ref": binding_payload(
                config["approval_policy"]["risk_policy_ref"], repository_root
            ),
            "run_budget": config["approval_policy"]["run_budget"],
            "allowed_audit_verdicts": config["approval_policy"][
                "allowed_audit_verdicts"
            ],
            "allowed_flag_classes": config["approval_policy"][
                "allowed_flag_classes"
            ],
        },
    }
    component_digests = {
        name: canonical_digest(payload) for name, payload in sorted(components.items())
    }
    canonical_semantic_digest = canonical_digest(component_digests)

    unit_payloads: dict[str, Any] = {}
    unit_digests: dict[str, str] = {}
    for unit in execution:
        unit_id = unit["unit_id"]
        unit_routes = [
            route
            for route in execution_policy["allowed_routes"]
            if route["frontier_swu"] == unit_id
        ]
        payload = {
            "normalizer_version": NORMALIZER_VERSION,
            "task_id": unit["task_id"],
            "swu_id": unit["swu_id"],
            "unit_id": unit_id,
            "dependencies": unit["dependencies"],
            "canonical_successors": unit["canonical_successors"],
            "command": unit["command"],
            "validation_contracts": unit["validation_contracts"],
            "attempt_contract": unit["attempt_contract"],
            "material_writes": unit["material_writes"],
            "execution_outputs": unit["execution_outputs"],
            "allowed_writes": unit["allowed_writes"],
            "producer_owner_ref": unit["material_package"]["producer_owner_ref"],
            "lifecycle_owner": unit["lifecycle_owner"],
            "authority_class": unit["authority_class"],
            "publication_class": unit["publication_class"],
            "receipt_contract_digest": component_digests["receipt"],
            "closeout_contract": _normalized_binding_tree(
                closeout_by_unit[unit_id], repository_root
            ),
            "runtime_contract": components["runtime"],
            "owner_contract_digest": component_digests["owner"],
            "risk_budget_digest": component_digests["risk_budget"],
            "allowed_routes_digest": execution_policy["allowed_routes_digest"],
            "execution_policy_digest": component_digests["execution_policy"],
            "unit_routes": unit_routes,
        }
        unit_payloads[unit_id] = payload
        unit_digests[unit_id] = canonical_digest(payload)

    return {
        "normalizer_version": NORMALIZER_VERSION,
        "components": components,
        "semantic_component_digests": component_digests,
        "canonical_semantic_digest": canonical_semantic_digest,
        "unit_contracts": unit_payloads,
        "unit_contract_digests": unit_digests,
        "ready_frontier": [unit["unit_id"] for unit in execution],
    }
