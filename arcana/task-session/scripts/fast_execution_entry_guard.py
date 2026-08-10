#!/usr/bin/env python3
"""Classify a Work-Pack-bound Task Session entry before Context Builder."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
REQUEST_SCHEMA = SCHEMA_ROOT / "fast-execution-entry-request.schema.json"
RECEIPT_SCHEMA = SCHEMA_ROOT / "fast-execution-entry-receipt.schema.json"


def _execution_contracts_path() -> Path:
    candidates = (
        # Generated Codex/Claude skill packages are siblings under skills/.
        PACKAGE_ROOT.parent
        / "implementation-readiness"
        / "scripts"
        / "execution_contracts.py",
        # The canonical public source keeps spells beside arcana/.
        PACKAGE_ROOT.parents[1]
        / "spells"
        / "implementation-readiness"
        / "scripts"
        / "execution_contracts.py",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    rendered = ", ".join(str(candidate) for candidate in candidates)
    raise RuntimeError(f"cannot locate implementation-readiness contracts: {rendered}")


EXECUTION_CONTRACTS = _execution_contracts_path()
_SPEC = importlib.util.spec_from_file_location(
    "implementation_readiness_execution_contracts", EXECUTION_CONTRACTS
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"cannot load execution contracts: {EXECUTION_CONTRACTS}")
_CONTRACTS = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_CONTRACTS)
ExecutionContractError = _CONTRACTS.ExecutionContractError
canonical_digest = _CONTRACTS.canonical_digest
validate_execution_binding = _CONTRACTS.validate_execution_binding


class FastGuardError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


class FastGuardTrace:
    """Observed logical reads and phase entries for the pre-context boundary."""

    def __init__(self) -> None:
        self.inputs_read: list[str] = []
        self.phases_entered: list[str] = []

    def enter(self, phase: str) -> None:
        self.phases_entered.append(phase)

    def read(self, name: str, value: Any) -> Any:
        self.inputs_read.append(name)
        return value


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
        raise FastGuardError(
            "FAST_GUARD_SCHEMA_INVALID", f"{label} at {location}: {error.message}"
        )


def _phase_trace(trace: FastGuardTrace) -> dict[str, Any]:
    return {
        "entry_guard_entered": "entry-guard" in trace.phases_entered,
        "context_builder_entered": False,
        "deep_material_check_entered": False,
        "mutation_admission_entered": False,
        "target_mutation_entered": False,
        "owner_hops_dispatched": 0,
    }


def _receipt(
    request: dict[str, Any],
    trace: FastGuardTrace,
    *,
    decision: str,
    code: str,
    owner_packet: dict[str, Any] | None,
    blocker_detail: str | None,
) -> dict[str, Any]:
    policy = request.get("execution_policy")
    entry = request.get("execution_entry")
    binding = request.get("execution_binding")
    selected = request.get("selected_unit")
    seed = {
        "work_pack_id": policy.get("work_pack_id") if isinstance(policy, dict) else None,
        "selected_unit": selected.get("swu_id") if isinstance(selected, dict) else None,
        "binding_id": binding.get("binding_id") if isinstance(binding, dict) else None,
        "decision": decision,
        "code": code,
    }
    stable_code = code if re.fullmatch(r"[A-Z0-9_]+", code) else "EXECUTION_ENTRY_BLOCKED"
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": f"feg-{canonical_digest(seed)[:24]}",
        "decision": decision,
        "code": stable_code,
        "work_pack_id": policy.get("work_pack_id") if isinstance(policy, dict) else None,
        "work_pack_semantic_digest": (
            policy.get("work_pack_semantic_digest") if isinstance(policy, dict) else None
        ),
        "selected_unit": selected.get("swu_id") if isinstance(selected, dict) else None,
        "entry_state": entry.get("entry_state") if isinstance(entry, dict) else None,
        "binding_id": binding.get("binding_id") if isinstance(binding, dict) else None,
        "binding_digest": binding.get("binding_digest") if isinstance(binding, dict) else None,
        "route_fingerprint": (
            binding.get("route_fingerprint") if isinstance(binding, dict) else None
        ),
        "owner_packet": copy.deepcopy(owner_packet),
        "authorization_source": (
            "work-pack-binding" if decision in {"proceed", "route-owner"} else "none"
        ),
        "authorization_prompt_required": False,
        "permitted_next_action": {
            "proceed": "enter-context-builder",
            "route-owner": "return-owner-packet",
            "block": "stop",
        }[decision],
        "logical_inputs_read": copy.deepcopy(trace.inputs_read),
        "read_count": len(trace.inputs_read),
        "phase_count": len(trace.phases_entered),
        "phase_trace": _phase_trace(trace),
        "mutation_count": 0,
        "blocker_detail": blocker_detail,
        "authority_effect": "none",
    }
    _validate(receipt, RECEIPT_SCHEMA, "fast-entry receipt")
    return receipt


def classify_fast_entry(request: dict[str, Any]) -> dict[str, Any]:
    trace = FastGuardTrace()
    trace.enter("entry-guard")
    policy = trace.read("work-pack", request.get("execution_policy"))
    selected = trace.read("selected-unit", request.get("selected_unit"))
    binding = trace.read("execution-binding", request.get("execution_binding"))
    entry = trace.read("execution-entry-projection", request.get("execution_entry"))
    try:
        _validate(request, REQUEST_SCHEMA, "fast-entry request")
        validate_execution_binding(binding, policy, entry)

        if selected["work_pack_id"] != policy["work_pack_id"]:
            raise FastGuardError("WORK_PACK_ID_MISMATCH", selected["work_pack_id"])
        if selected["swu_id"] not in policy["frontier"]:
            raise FastGuardError("SELECTED_UNIT_OUTSIDE_FRONTIER", selected["swu_id"])
        if entry["entry_state"] in {
            "context-ready",
            "task-ready",
            "owner-prerequisite",
        }:
            if entry["selected_unit"] != selected["swu_id"]:
                raise FastGuardError("SELECTED_UNIT_STALE", selected["swu_id"])
            route = binding["current_route"]
            if route is None or route["frontier_swu"] != selected["swu_id"]:
                raise FastGuardError("ROUTE_FRONTIER_MISMATCH", selected["swu_id"])

        if entry["entry_state"] == "context-ready":
            return _receipt(
                request,
                trace,
                decision="proceed",
                code="CONTEXT_READY",
                owner_packet=None,
                blocker_detail=None,
            )
        if entry["entry_state"] == "task-ready":
            return _receipt(
                request,
                trace,
                decision="proceed",
                code="TASK_READY",
                owner_packet=None,
                blocker_detail=None,
            )
        if entry["entry_state"] == "owner-prerequisite":
            return _receipt(
                request,
                trace,
                decision="route-owner",
                code="OWNER_PREREQUISITE",
                owner_packet=binding["current_route"],
                blocker_detail=None,
            )
        if entry["entry_state"] == "selection-ready":
            raise FastGuardError(
                "SELECTION_NOT_MATERIALIZED",
                "Implementation Readiness must select the unit before Task Session",
            )
        blocker = entry["blocker_code"] or "EXECUTION_ENTRY_BLOCKED"
        raise FastGuardError(blocker, f"execution entry is blocked: {blocker}")
    except (ExecutionContractError, FastGuardError) as error:
        return _receipt(
            request,
            trace,
            decision="block",
            code=error.code,
            owner_packet=None,
            blocker_detail=error.message,
        )


def validate_fast_entry_receipt(
    receipt: dict[str, Any], request: dict[str, Any] | None = None
) -> dict[str, Any]:
    _validate(receipt, RECEIPT_SCHEMA, "fast-entry receipt")
    if request is not None:
        _validate(request, REQUEST_SCHEMA, "fast-entry request")
        policy = request["execution_policy"]
        entry = request["execution_entry"]
        binding = request["execution_binding"]
        selected = request["selected_unit"]
        validate_execution_binding(binding, policy, entry)
        exact_pairs = (
            ("work_pack_id", policy["work_pack_id"]),
            ("work_pack_semantic_digest", policy["work_pack_semantic_digest"]),
            ("selected_unit", selected["swu_id"]),
            ("entry_state", entry["entry_state"]),
            ("binding_id", binding["binding_id"]),
            ("binding_digest", binding["binding_digest"]),
            ("route_fingerprint", binding["route_fingerprint"]),
        )
        for field, expected in exact_pairs:
            if receipt[field] != expected:
                raise FastGuardError("FAST_GUARD_RECEIPT_MISMATCH", field)
        expected_packet = (
            binding["current_route"] if receipt["decision"] == "route-owner" else None
        )
        if receipt["owner_packet"] != expected_packet:
            raise FastGuardError("FAST_GUARD_OWNER_PACKET_MISMATCH", "owner_packet")
    return copy.deepcopy(receipt)
