#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any


class ModeCapabilityError(ValueError):
    pass


REQUIRED_RULES = {"implementation_status", "dispatch_trace", "distill", "mutation_handoff_allowed"}
ACTIVE_MODES = {"define", "design", "plan", "handoff", "refresh"}
REFRESH_PHASE_STATUSES = {"pass", "flag", "block", "no-op"}
REFRESH_HANDOFF_STATUSES = {"ready", "gated", "deferred", "blocked", "not-needed"}
REFRESH_BLOCKER_SCOPES = {
    "refresh-authoring",
    "apply-authorization",
    "target-lifecycle",
    "audit",
}


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


def _validate_refresh_evidence(evidence: dict[str, Any]) -> list[str]:
    diagnostics: list[str] = []
    mutation_mode = evidence.get("mutation_mode")
    phase_status = evidence.get("phase_status")
    handoff_status = evidence.get("handoff_status")
    blocker_scopes = evidence.get("blocker_scopes")

    if mutation_mode not in {"proposal-only", "apply-approved"}:
        diagnostics.append("refresh mutation mode must be proposal-only or apply-approved")
    if phase_status not in REFRESH_PHASE_STATUSES:
        diagnostics.append("refresh phase status is invalid")
    if handoff_status not in REFRESH_HANDOFF_STATUSES:
        diagnostics.append("refresh handoff status is invalid")

    if not isinstance(blocker_scopes, dict) or set(blocker_scopes) != REFRESH_BLOCKER_SCOPES:
        diagnostics.append("refresh blocker scopes must enumerate every lifecycle scope")
        blocker_scopes = {}
    elif any(
        not isinstance(count, int) or isinstance(count, bool) or count < 0
        for count in blocker_scopes.values()
    ):
        diagnostics.append("refresh blocker scope counts must be non-negative integers")

    result = evidence.get("result")
    if isinstance(result, dict) and result.get("phase_status") != phase_status:
        diagnostics.append("refresh authored phase status must match result phase status")

    authoring_blockers = blocker_scopes.get("refresh-authoring", 0)
    apply_blockers = blocker_scopes.get("apply-authorization", 0)

    if mutation_mode == "proposal-only":
        if phase_status in {"pass", "no-op"} and authoring_blockers:
            diagnostics.append("complete proposal-only phase cannot retain refresh-authoring blockers")
        if phase_status == "flag" and not authoring_blockers:
            diagnostics.append(
                "proposal-only flag requires a refresh-authoring blocker; downstream or apply blockers only gate handoff"
            )
        if phase_status == "block" and not authoring_blockers:
            diagnostics.append("proposal-only block requires a refresh-authoring activation blocker")
        if phase_status == "pass" and handoff_status not in {"ready", "gated", "deferred"}:
            diagnostics.append("complete proposal-only phase must have ready, gated, or deferred handoff")
        if phase_status in {"flag", "block"} and handoff_status not in {"blocked", "deferred"}:
            diagnostics.append("incomplete proposal-only phase must have blocked or deferred handoff")
        if phase_status == "no-op" and handoff_status != "not-needed":
            diagnostics.append("no-op refresh must have not-needed handoff")
        if phase_status == "pass" and apply_blockers and handoff_status != "gated":
            diagnostics.append("pending apply authorization requires gated handoff, not a lower phase status")

    if mutation_mode == "apply-approved":
        if not _present(evidence.get("apply_approval")):
            diagnostics.append("apply-approved refresh requires explicit apply approval evidence")
        if phase_status == "pass" and handoff_status != "ready":
            diagnostics.append("passing apply-approved refresh must have ready handoff")
        if phase_status == "pass" and (authoring_blockers or apply_blockers):
            diagnostics.append("passing apply-approved refresh cannot retain authoring or apply blockers")
        if phase_status in {"flag", "block"} and handoff_status not in {"blocked", "deferred"}:
            diagnostics.append("non-passing apply-approved refresh must have blocked or deferred handoff")
        if phase_status == "no-op" and handoff_status != "not-needed":
            diagnostics.append("no-op refresh must have not-needed handoff")

    return diagnostics


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
    if mode == "refresh":
        diagnostics.extend(_validate_refresh_evidence(evidence))

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
    validator_pass = isinstance(validator, dict) and validator.get("status") == "pass"
    validator_authorizes_mutation = (
        isinstance(validator, dict) and validator.get("mutation_handoff_allowed") is True
    )
    if not isinstance(validator, dict):
        diagnostics.append("validator result is required")
    elif not validator_pass:
        diagnostics.append("validator result must pass")
    elif mode == "refresh" and evidence.get("mutation_mode") == "proposal-only":
        if validator_authorizes_mutation:
            diagnostics.append("proposal-only validator result must not authorize mutation handoff")
    elif not validator_authorizes_mutation:
        diagnostics.append("validator result does not authorize mutation handoff")

    status = "pass" if not diagnostics else "block"
    refresh_mutation_ready = (
        mode != "refresh"
        or (
            evidence.get("mutation_mode") == "apply-approved"
            and evidence.get("phase_status") == "pass"
            and evidence.get("handoff_status") == "ready"
            and _present(evidence.get("apply_approval"))
        )
    )
    return {
        "mode": mode,
        "status": status,
        "implementation_status": "active",
        "lifecycle_processed": False,
        "dispatch_trace": "evaluated" if _present(evidence.get("dispatch_trace")) else "missing",
        "distill": distill_status or "missing",
        "mutation_handoff_allowed": (
            status == "pass"
            and validator_pass
            and validator_authorizes_mutation
            and refresh_mutation_ready
        ),
        "missing_evidence": missing,
        "diagnostics": diagnostics,
    }
