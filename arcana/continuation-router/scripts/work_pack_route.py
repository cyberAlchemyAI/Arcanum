#!/usr/bin/env python3
"""Fail-closed admission for one Work-Pack-bound Continuation Router hop."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
REQUEST_SCHEMA = SCHEMA_ROOT / "work-pack-route-request.schema.json"
ADMISSION_SCHEMA = SCHEMA_ROOT / "work-pack-route-admission.schema.json"
EXECUTION_CONTRACTS = ARCANUM_ROOT / "spells" / "implementation-readiness" / "scripts"
if str(EXECUTION_CONTRACTS) not in sys.path:
    sys.path.insert(0, str(EXECUTION_CONTRACTS))

from execution_contracts import (  # noqa: E402
    ExecutionContractError,
    match_bound_route,
    validate_execution_binding,
)


def _load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _validate(document: dict[str, Any], schema_path: Path, label: str) -> None:
    errors = sorted(
        Draft202012Validator(_load_schema(schema_path)).iter_errors(document),
        key=lambda error: list(error.path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or label
        raise ExecutionContractError(
            "SCHEMA_INVALID", f"{label} at {location}: {error.message}"
        )


def _block_receipt(
    code: str,
    detail: str,
    request: dict[str, Any],
) -> dict[str, Any]:
    binding = request.get("execution_binding")
    candidate_count = len(request.get("candidate_routes", []))
    receipt = {
        "schema_version": "1.0.0",
        "verdict": "block",
        "code": code,
        "authorization_source": "none",
        "authorization_prompt_required": False,
        "dispatch_allowed": False,
        "candidate_count": min(candidate_count, 3),
        "binding_id": binding.get("binding_id") if isinstance(binding, dict) else None,
        "binding_digest": binding.get("binding_digest") if isinstance(binding, dict) else None,
        "matched_route": None,
        "route_fingerprint": (
            binding.get("route_fingerprint") if isinstance(binding, dict) else None
        ),
        "blocking_detail": detail,
        "authority_effect": "none",
    }
    _validate(receipt, ADMISSION_SCHEMA, "admission receipt")
    return receipt


def evaluate_work_pack_route(request: dict[str, Any]) -> dict[str, Any]:
    """Return one validated admission receipt; contract failures become blocks."""

    try:
        _validate(request, REQUEST_SCHEMA, "route request")
        policy = request["execution_policy"]
        entry = request["execution_entry"]
        binding = request["execution_binding"]
        validate_execution_binding(binding, policy, entry)

        candidates = request["candidate_routes"]
        if len(candidates) != 1:
            raise ExecutionContractError(
                "OWNER_ROUTE_AMBIGUOUS", f"expected one candidate, got {len(candidates)}"
            )
        candidate = candidates[0]

        installed = {
            (route["capability"], route["mode"])
            for route in request["installed_owner_routes"]
        }
        owner_route = (candidate["capability"], candidate["mode"])
        if owner_route not in installed:
            raise ExecutionContractError(
                "OWNER_ROUTE_UNKNOWN", ":".join(owner_route)
            )

        try:
            match = match_bound_route(binding, candidate)
        except ExecutionContractError as error:
            if error.code == "ROUTE_UNDECLARED" and error.message == "frontier_swu":
                raise ExecutionContractError(
                    "ROUTE_FRONTIER_MISMATCH", candidate["frontier_swu"]
                ) from error
            if error.code == "ROUTE_UNDECLARED" and error.message in {
                "capability",
                "mode",
            }:
                raise ExecutionContractError(
                    "ROUTE_OWNER_MISMATCH",
                    f"{candidate['capability']}:{candidate['mode']}",
                ) from error
            raise

        available = set(request["available_inputs"])
        missing = [
            required
            for required in candidate["required_inputs"]
            if required not in available
        ]
        if missing:
            raise ExecutionContractError(
                "ROUTE_INPUT_MISSING", ",".join(missing)
            )
        if binding["route_fingerprint"] in request["consumed_route_fingerprints"]:
            raise ExecutionContractError(
                "ROUTE_FINGERPRINT_REPEATED", binding["route_fingerprint"]
            )

        receipt = {
            "schema_version": "1.0.0",
            "verdict": "pass",
            "code": "ROUTE_ADMITTED",
            "authorization_source": match["authorization_source"],
            "authorization_prompt_required": match["authorization_prompt_required"],
            "dispatch_allowed": True,
            "candidate_count": 1,
            "binding_id": binding["binding_id"],
            "binding_digest": binding["binding_digest"],
            "matched_route": copy.deepcopy(candidate),
            "route_fingerprint": match["route_fingerprint"],
            "blocking_detail": None,
            "authority_effect": "none",
        }
        _validate(receipt, ADMISSION_SCHEMA, "admission receipt")
        return receipt
    except ExecutionContractError as error:
        return _block_receipt(error.code, error.message, request)


def validate_admission_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    _validate(receipt, ADMISSION_SCHEMA, "admission receipt")
    return copy.deepcopy(receipt)
