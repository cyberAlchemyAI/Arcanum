#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any


class ModeCapabilityError(ValueError):
    pass


REQUIRED_RULES = {"implementation_status", "dispatch_trace", "distill", "mutation_handoff_allowed"}
ACTIVE_MODES = {"define", "design", "plan", "handoff", "refresh"}


def load_capabilities(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema_version") != "1.0.0":
        raise ModeCapabilityError("capability schema version must be 1.0.0")
    modes = document.get("modes")
    if not isinstance(modes, dict) or set(modes) != {"define", "design", "plan", "handoff", "refresh", "full", "validate"}:
        raise ModeCapabilityError("capability table must enumerate every Invoke mode")
    for mode, rules in modes.items():
        if not isinstance(rules, dict) or not REQUIRED_RULES.issubset(rules):
            raise ModeCapabilityError(f"mode {mode} is missing a capability rule")
        if mode in ACTIVE_MODES:
            evidence = rules.get("evidence")
            if not isinstance(evidence, dict) or not isinstance(evidence.get("required"), list):
                raise ModeCapabilityError(f"active mode {mode} is missing evidence obligations")
            if not isinstance(evidence.get("distill_skip_requires_rationale"), bool):
                raise ModeCapabilityError(f"active mode {mode} is missing Distill skip policy")
    return document


def resolve_mode_capability(mode: str, capabilities: dict[str, Any]) -> dict[str, Any]:
    rules = capabilities["modes"].get(mode)
    if rules is None:
        raise ModeCapabilityError(f"unknown Invoke mode: {mode}")

    if rules["implementation_status"] == "deferred":
        return {
            "mode": mode,
            "status": "unsupported",
            "implementation_status": "deferred",
            "lifecycle_processed": False,
            "dispatch_trace": "not_evaluated",
            "distill": "not_evaluated",
            "mutation_handoff_allowed": False,
            "diagnostics": [f"Invoke mode {mode} is deferred and stops before lifecycle processing"],
        }

    return {
        "mode": mode,
        "status": "supported",
        "implementation_status": "active",
        "lifecycle_processed": False,
        "dispatch_trace": rules["dispatch_trace"],
        "distill": rules["distill"],
        "mutation_handoff_allowed": False,
        "diagnostics": [],
    }


def _present(value: Any) -> bool:
    return value is not None and value is not False and value != "" and value != [] and value != {}


def evaluate_active_mode_evidence(
    mode: str, payload: dict[str, Any], capabilities: dict[str, Any]
) -> dict[str, Any]:
    if mode not in ACTIVE_MODES:
        raise ModeCapabilityError(f"active evidence is not applicable to mode: {mode}")

    rules = capabilities["modes"][mode]
    evidence = payload.get("evidence")
    diagnostics: list[str] = []
    if not isinstance(evidence, dict):
        diagnostics.append("active mode evidence object is missing")
        evidence = {}

    missing = [field for field in rules["evidence"]["required"] if not _present(evidence.get(field))]
    diagnostics.extend(f"missing required evidence: {field}" for field in missing)

    distill_status = payload.get("distill_status")
    if rules["distill"] == "required" and distill_status != "pass":
        diagnostics.append("required Distill evidence must have status pass")
    if rules["distill"] == "conditional":
        if distill_status not in {"pass", "not_required"}:
            diagnostics.append("conditional Distill evidence must be pass or not_required")
        if distill_status == "not_required" and rules["evidence"]["distill_skip_requires_rationale"]:
            if not _present(payload.get("distill_skip_rationale")):
                diagnostics.append("conditional Distill skip requires rationale")

    validator = payload.get("validator_result")
    validator_pass = (
        isinstance(validator, dict)
        and validator.get("status") == "pass"
        and validator.get("mutation_handoff_allowed") is True
    )
    if not isinstance(validator, dict):
        diagnostics.append("validator result is required")
    elif not validator_pass:
        diagnostics.append("validator result does not authorize handoff")

    status = "pass" if not diagnostics else "block"
    return {
        "mode": mode,
        "status": status,
        "implementation_status": "active",
        "lifecycle_processed": False,
        "dispatch_trace": "evaluated" if _present(evidence.get("dispatch_trace")) else "missing",
        "distill": distill_status or "missing",
        "mutation_handoff_allowed": status == "pass" and validator_pass,
        "missing_evidence": missing,
        "diagnostics": diagnostics,
    }
