#!/usr/bin/env python3
"""Compile Work Pack Readiness evidence into outer-loop execution contracts."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from execution_contracts import (
    allowed_routes_digest,
    canonical_digest,
    validate_execution_binding,
    validate_execution_entry,
    validate_execution_policy,
)
from execution_loop import decide_next_action, initialize_outer_loop
from implementation_readiness_runtime_paths import capability_root


SPELL_ROOT = Path(__file__).resolve().parents[1]
READINESS_AUDIT_ROOT = capability_root("work-pack-readiness-audit", "spells")
TASK_SESSION_ROOT = capability_root("task-session", "arcana")
AUDIT_CONFIG_SCHEMA = READINESS_AUDIT_ROOT / "schemas" / "audit-config-v2.schema.json"
AUDIT_REPORT_SCHEMA = READINESS_AUDIT_ROOT / "schemas" / "audit-report-v2.schema.json"
SELECTION_RECEIPT_SCHEMA = (
    READINESS_AUDIT_ROOT / "schemas" / "selection-receipt.schema.json"
)
MUTATION_ADMISSION_SCHEMA = (
    TASK_SESSION_ROOT / "schemas" / "mutation-admission-receipt.schema.json"
)
FRESH_SESSION_RUNTIME_PATH = capability_root(
    "task-session-until-blocker", "spells"
) / "scripts" / "fresh_session_resume.py"


def _load_owner_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load owner runtime: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


FRESH_SESSION = _load_owner_module(
    "implementation_readiness_fresh_session_owner", FRESH_SESSION_RUNTIME_PATH
)


class ReadinessExecutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _validate(document: Any, schema_path: Path, label: str) -> None:
    errors = sorted(
        Draft202012Validator(_load_schema(schema_path)).iter_errors(document),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(map(str, error.absolute_path)) or "<root>"
        raise ReadinessExecutionError(
            "READINESS_EVIDENCE_INVALID",
            f"{label} at {location}: {error.message}",
        )


def _validation_commands(config: dict[str, Any]) -> list[str]:
    commands: list[str] = []
    for unit in config["execution_bindings"]:
        for contract in unit.get("validation_contracts", []):
            rendered = json.dumps(
                {
                    "command_id": contract["command_id"],
                    "argv": contract["argv"],
                    "cwd": contract["cwd"],
                    "timeout_seconds": contract["timeout_seconds"],
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            if rendered not in commands:
                commands.append(rendered)
    if not commands:
        raise ReadinessExecutionError(
            "VALIDATION_COMMANDS_MISSING", config["audit_id"]
        )
    return commands


def _repairable_semantic_drift(report: dict[str, Any]) -> bool:
    return (
        report["verdict"] == "block"
        and report["execution_entry"]["entry_state"] == "owner-prerequisite"
        and {item["code"] for item in report["blockers"]}
        == {"EPOCH_INVALIDATED_SEMANTIC_CHANGE"}
    )


def compile_completion_continuity(
    audit_config: dict[str, Any],
    audit_report: dict[str, Any],
    *,
    semantic_digest: str,
    frontier: list[str],
) -> dict[str, Any]:
    manifest = audit_report.get("manifest")
    if manifest is not None:
        continuity = copy.deepcopy(manifest.get("completion_continuity"))
        if continuity is None:
            raise ReadinessExecutionError(
                "CONTINUITY_PROJECTION_MISSING", audit_report["audit_id"]
            )
        exact_pairs = {
            "source_audit_id": audit_report["audit_id"],
            "work_pack_semantic_digest": semantic_digest,
            "plan_epoch_id": manifest["plan_epoch_id"],
        }
        for field, expected in exact_pairs.items():
            if continuity.get(field) != expected:
                raise ReadinessExecutionError(
                    "CONTINUITY_SEMANTIC_STALE", field
                )
        source_projection = {
            "cursor": audit_config["continuity_projection"]["cursor"],
            "completed_unit_receipt_refs": audit_config["continuity_projection"][
                "completed_unit_receipt_refs"
            ],
            "joined_closeout_receipt_refs": audit_config["continuity_projection"][
                "joined_closeout_receipt_refs"
            ],
            "projected_next_successor": audit_config["continuity_projection"][
                "projected_next_successor"
            ],
            "source_snapshot_digest": manifest["source_snapshot_digest"],
        }
        if continuity.get("source_projection_digest") != canonical_digest(
            source_projection
        ):
            raise ReadinessExecutionError(
                "CONTINUITY_DIGEST_STALE", "source_projection_digest"
            )
        completed = continuity.get("completed_prefix", [])
        completed_units = [item.get("unit_id") for item in completed]
        if completed_units != frontier[: len(completed_units)]:
            raise ReadinessExecutionError(
                "CONTINUITY_NON_PREFIX_COMPLETION", audit_report["audit_id"]
            )
        unit_digests = manifest["unit_contract_digests"]
        for item in completed:
            if item.get("unit_contract_digest") != unit_digests.get(item.get("unit_id")):
                raise ReadinessExecutionError(
                    "CONTINUITY_UNIT_CONTRACT_STALE", str(item.get("unit_id"))
                )
        expected_next = (
            frontier[len(completed)] if len(completed) < len(frontier) else None
        )
        if continuity.get("next_unit") != expected_next:
            raise ReadinessExecutionError(
                "CONTINUITY_CURSOR_CONTRADICTION", audit_report["audit_id"]
            )
        payload = {
            key: value
            for key, value in continuity.items()
            if key != "continuity_digest"
        }
        if continuity.get("continuity_digest") != canonical_digest(payload):
            raise ReadinessExecutionError(
                "CONTINUITY_DIGEST_STALE", audit_report["audit_id"]
            )
        return continuity

    if not _repairable_semantic_drift(audit_report):
        raise ReadinessExecutionError(
            "CONTINUITY_PROJECTION_MISSING", audit_report["audit_id"]
        )
    source = audit_config.get("continuity_projection")
    if (
        not isinstance(source, dict)
        or source.get("completed_unit_receipt_refs") != []
        or source.get("joined_closeout_receipt_refs") != []
        or not frontier
        or source.get("cursor") != frontier[0]
        or source.get("projected_next_successor", {}).get("unit_id") != frontier[0]
    ):
        raise ReadinessExecutionError(
            "CONTINUITY_PROJECTION_MISSING",
            "semantic repair may synthesize only an explicit all-pending projection",
        )
    plan_epoch_id = f"epoch-{canonical_digest({'audit_id': audit_report['audit_id'], 'semantic_digest': semantic_digest, 'continuity': source})[:24]}"
    payload = {
        "source_audit_id": audit_report["audit_id"],
        "source_projection_digest": canonical_digest(source),
        "work_pack_semantic_digest": semantic_digest,
        "plan_epoch_id": plan_epoch_id,
        "completed_prefix": [],
        "next_unit": frontier[0],
        "authority_effect": "none",
    }
    return {**payload, "continuity_digest": canonical_digest(payload)}


def compile_execution_policy(
    audit_config: dict[str, Any], audit_report: dict[str, Any]
) -> dict[str, Any]:
    """Compile the exact no-authority execution policy consumed by the loop."""

    _validate(audit_config, AUDIT_CONFIG_SCHEMA, "audit config")
    _validate(audit_report, AUDIT_REPORT_SCHEMA, "audit report")
    if audit_config.get("admission_timing") != "selected-unit-at-task-session":
        raise ReadinessExecutionError(
            "READINESS_PROFILE_UNSUPPORTED", str(audit_config.get("admission_timing"))
        )
    if audit_report["audit_id"] != audit_config["audit_id"]:
        raise ReadinessExecutionError("AUDIT_ID_MISMATCH", audit_report["audit_id"])
    if audit_report["verdict"] not in {"pass", "flag"} and not _repairable_semantic_drift(
        audit_report
    ):
        raise ReadinessExecutionError(
            "READINESS_NOT_EXECUTABLE", audit_report["terminal_code"]
        )

    configured = audit_config["execution_policy"]
    routes = copy.deepcopy(configured["allowed_routes"])
    if configured["allowed_routes_digest"] != allowed_routes_digest(routes):
        raise ReadinessExecutionError(
            "ALLOWED_ROUTES_DIGEST_STALE", audit_config["audit_id"]
        )
    if audit_report["manifest"] is not None:
        manifest = audit_report["manifest"]
        if manifest["work_pack_id"] != configured["work_pack_id"]:
            raise ReadinessExecutionError(
                "WORK_PACK_ID_MISMATCH", manifest["work_pack_id"]
            )
        if manifest["allowed_routes"] != routes:
            raise ReadinessExecutionError(
                "ALLOWED_ROUTES_PROJECTION_MISMATCH", audit_config["audit_id"]
            )
        if manifest["allowed_routes_digest"] != configured["allowed_routes_digest"]:
            raise ReadinessExecutionError(
                "ALLOWED_ROUTES_DIGEST_STALE", audit_config["audit_id"]
            )

    if _repairable_semantic_drift(audit_report):
        semantic_digest = audit_config.get("expected_semantic_digest")
        if semantic_digest is None:
            raise ReadinessExecutionError(
                "EXPECTED_SEMANTIC_IDENTITY_MISSING", audit_config["audit_id"]
            )
    else:
        semantic_digest = audit_report["canonical_semantic_digest"]
    frontier = [item["unit_id"] for item in audit_config["execution_bindings"]]
    completion_continuity = compile_completion_continuity(
        audit_config,
        audit_report,
        semantic_digest=semantic_digest,
        frontier=frontier,
    )
    policy = {
        "schema_version": "1.1.0",
        "work_pack_id": configured["work_pack_id"],
        "work_pack_semantic_digest": semantic_digest,
        "frontier": frontier,
        "completion_continuity": completion_continuity,
        "allowed_routes": routes,
        "allowed_routes_digest": configured["allowed_routes_digest"],
        "automatic_decisions": copy.deepcopy(configured["automatic_decisions"]),
        "stop_decisions": copy.deepcopy(configured["stop_decisions"]),
        "validation_commands": _validation_commands(audit_config),
        "scope_source": configured["scope_source"],
        "validation_policy": configured["validation_policy"],
        "authority_effect": "none",
    }
    validate_execution_policy(policy)
    return policy


def compile_readiness_entry(
    policy: dict[str, Any], audit_report: dict[str, Any]
) -> dict[str, Any]:
    """Bind the owner projection to the exact Work Pack execution identity."""

    partial = audit_report["execution_entry"]
    if partial["entry_state"] == "blocked":
        raise ReadinessExecutionError(
            "READINESS_ENTRY_BLOCKED", str(partial["blocker_code"])
        )
    if (
        audit_report["verdict"] in {"pass", "flag"}
        and audit_report["canonical_semantic_digest"]
        != policy["work_pack_semantic_digest"]
    ):
        raise ReadinessExecutionError(
            "READINESS_SEMANTIC_STALE", audit_report["audit_id"]
        )
    entry = {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": partial["entry_state"],
        "selected_unit": partial["selected_unit"],
        "route_id": partial["route_id"],
        "next_owner": copy.deepcopy(partial["next_owner"]),
        "blocker_code": partial["blocker_code"],
        "authority_effect": "none",
    }
    validate_execution_entry(entry, policy)
    return entry


def initialize_from_readiness(
    audit_config: dict[str, Any],
    audit_report: dict[str, Any],
    *,
    source_invocation_id: str,
    created_at: str,
    execution_mode: str,
    step_budget: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Initialize one loop directly from validated readiness evidence."""

    policy = compile_execution_policy(audit_config, audit_report)
    entry = compile_readiness_entry(policy, audit_report)
    state = initialize_outer_loop(
        policy,
        entry,
        source_invocation_id=source_invocation_id,
        created_at=created_at,
        execution_mode=execution_mode,
        step_budget=step_budget,
    )
    return policy, state


def selection_intent_projection(
    execution_binding: dict[str, Any],
) -> dict[str, Any]:
    return {
        "bindingId": execution_binding["binding_id"],
        "sourceInvocationId": execution_binding["source_invocation_id"],
        "workPackId": execution_binding["work_pack_id"],
        "bindingDigest": execution_binding["binding_digest"],
        "authorityEffect": "bounded-execution-only",
    }


def compile_plan_once_context_entry(
    policy: dict[str, Any],
    audit_config: dict[str, Any],
    audit_report: dict[str, Any],
    selection_receipt: dict[str, Any],
    execution_binding: dict[str, Any],
) -> dict[str, Any]:
    """Emit a selected-unit Context Builder entry with no mutation authority."""

    validate_execution_policy(policy)
    _validate(audit_config, AUDIT_CONFIG_SCHEMA, "audit config")
    _validate(audit_report, AUDIT_REPORT_SCHEMA, "audit report")
    _validate(selection_receipt, SELECTION_RECEIPT_SCHEMA, "selection receipt")
    validate_execution_binding(
        execution_binding,
        policy,
        compile_readiness_entry(policy, audit_report),
    )
    report_continuity = audit_report["manifest"].get("completion_continuity")
    policy_continuity = policy["completion_continuity"]
    if report_continuity is None:
        raise ReadinessExecutionError(
            "CONTINUITY_PROJECTION_MISSING", audit_report["audit_id"]
        )
    if report_continuity != policy_continuity:
        raise ReadinessExecutionError(
            "CONTINUITY_POLICY_STATE_MISMATCH", audit_report["audit_id"]
        )
    if audit_report["verdict"] not in {"pass", "flag"}:
        raise ReadinessExecutionError(
            "PLAN_ONCE_AUDIT_NOT_READY", audit_report["terminal_code"]
        )
    manifest = audit_report["manifest"]
    if manifest is None:
        raise ReadinessExecutionError("PLAN_MANIFEST_MISSING", audit_report["audit_id"])
    if selection_receipt["selectionVerdict"] != "select":
        raise ReadinessExecutionError(
            "SELECTION_NOT_READY", selection_receipt["terminalCode"]
        )
    intent = selection_intent_projection(execution_binding)
    if selection_receipt["selectionIntentSource"] != "execution-intent-binding":
        raise ReadinessExecutionError(
            "SECOND_CONFIRMATION_NOT_CONSUMABLE",
            selection_receipt["selectionIntentSource"],
        )
    if selection_receipt["selectionIntentDigest"] != canonical_digest(intent):
        raise ReadinessExecutionError(
            "SELECTION_INTENT_BINDING_MISMATCH", execution_binding["binding_id"]
        )
    if selection_receipt["canonicalSemanticDigest"] != policy["work_pack_semantic_digest"]:
        raise ReadinessExecutionError(
            "SELECTION_SEMANTIC_STALE", selection_receipt["taskId"]
        )
    if selection_receipt["planEpochId"] != manifest["plan_epoch_id"]:
        raise ReadinessExecutionError(
            "SELECTION_EPOCH_STALE", selection_receipt["taskId"]
        )

    matches = [
        item
        for item in audit_config["execution_bindings"]
        if item.get("task_id") == selection_receipt["taskId"]
        and item.get("swu_id") == selection_receipt["swuId"]
    ]
    if len(matches) != 1:
        raise ReadinessExecutionError(
            "SELECTED_UNIT_NOT_UNIQUE", str(selection_receipt["swuId"])
        )
    unit = matches[0]
    unit_id = unit["unit_id"]
    if selection_receipt["unitContractDigest"] != manifest["unit_contract_digests"].get(
        unit_id
    ):
        raise ReadinessExecutionError("UNIT_CONTRACT_STALE", unit_id)

    routes = [
        route
        for route in policy["allowed_routes"]
        if route["frontier_swu"] == unit_id
        and route["capability"] == "task-session"
        and route["mode"] == "execute"
    ]
    if len(routes) != 1:
        raise ReadinessExecutionError(
            "TASK_SESSION_ROUTE_NOT_UNIQUE", f"{unit_id}:{len(routes)}"
        )
    route = routes[0]
    entry = {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "context-ready",
        "selected_unit": unit_id,
        "route_id": route["route_id"],
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }
    validate_execution_entry(entry, policy)
    return entry


def compile_plan_once_task_entry(
    policy: dict[str, Any],
    audit_config: dict[str, Any],
    audit_report: dict[str, Any],
    selection_receipt: dict[str, Any],
    mutation_admission_receipt: dict[str, Any],
    execution_binding: dict[str, Any],
) -> dict[str, Any]:
    """Emit task-ready only after exact selection and mutation admission pass."""

    validate_execution_policy(policy)
    _validate(audit_config, AUDIT_CONFIG_SCHEMA, "audit config")
    _validate(audit_report, AUDIT_REPORT_SCHEMA, "audit report")
    _validate(selection_receipt, SELECTION_RECEIPT_SCHEMA, "selection receipt")
    _validate(
        mutation_admission_receipt,
        MUTATION_ADMISSION_SCHEMA,
        "mutation admission receipt",
    )
    validate_execution_binding(
        execution_binding,
        policy,
        compile_readiness_entry(policy, audit_report),
    )
    report_continuity = audit_report["manifest"].get("completion_continuity")
    policy_continuity = policy["completion_continuity"]
    if report_continuity is None:
        raise ReadinessExecutionError(
            "CONTINUITY_PROJECTION_MISSING", audit_report["audit_id"]
        )
    if report_continuity != policy_continuity:
        raise ReadinessExecutionError(
            "CONTINUITY_POLICY_STATE_MISMATCH", audit_report["audit_id"]
        )
    if audit_report["verdict"] not in {"pass", "flag"}:
        raise ReadinessExecutionError(
            "PLAN_ONCE_AUDIT_NOT_READY", audit_report["terminal_code"]
        )
    manifest = audit_report["manifest"]
    if manifest is None:
        raise ReadinessExecutionError("PLAN_MANIFEST_MISSING", audit_report["audit_id"])
    if selection_receipt["selectionVerdict"] != "select":
        raise ReadinessExecutionError(
            "SELECTION_NOT_READY", selection_receipt["terminalCode"]
        )
    intent = selection_intent_projection(execution_binding)
    if selection_receipt["selectionIntentSource"] != "execution-intent-binding":
        raise ReadinessExecutionError(
            "SECOND_CONFIRMATION_NOT_CONSUMABLE",
            selection_receipt["selectionIntentSource"],
        )
    if selection_receipt["selectionIntentDigest"] != canonical_digest(intent):
        raise ReadinessExecutionError(
            "SELECTION_INTENT_BINDING_MISMATCH", execution_binding["binding_id"]
        )
    if selection_receipt["canonicalSemanticDigest"] != policy["work_pack_semantic_digest"]:
        raise ReadinessExecutionError(
            "SELECTION_SEMANTIC_STALE", selection_receipt["taskId"]
        )
    if selection_receipt["planEpochId"] != manifest["plan_epoch_id"]:
        raise ReadinessExecutionError(
            "SELECTION_EPOCH_STALE", selection_receipt["taskId"]
        )

    matches = [
        item
        for item in audit_config["execution_bindings"]
        if item.get("task_id") == selection_receipt["taskId"]
        and item.get("swu_id") == selection_receipt["swuId"]
    ]
    if len(matches) != 1:
        raise ReadinessExecutionError(
            "SELECTED_UNIT_NOT_UNIQUE", str(selection_receipt["swuId"])
        )
    unit = matches[0]
    unit_id = unit["unit_id"]
    if selection_receipt["unitContractDigest"] != manifest["unit_contract_digests"].get(
        unit_id
    ):
        raise ReadinessExecutionError("UNIT_CONTRACT_STALE", unit_id)

    admission = mutation_admission_receipt
    admission_pairs = {
        "admissionProfile": "plan-once-selected-unit",
        "admissionVerdict": "admit",
        "mutationReady": True,
        "taskId": selection_receipt["taskId"],
        "swuId": selection_receipt["swuId"],
        "planEpochId": selection_receipt["planEpochId"],
        "unitContractDigest": selection_receipt["unitContractDigest"],
        "singleUse": True,
        "liveValidationRequired": True,
    }
    for field, expected in admission_pairs.items():
        if admission.get(field) != expected:
            raise ReadinessExecutionError("MUTATION_ADMISSION_MISMATCH", field)

    routes = [
        route
        for route in policy["allowed_routes"]
        if route["frontier_swu"] == unit_id
        and route["capability"] == "task-session"
        and route["mode"] == "execute"
    ]
    if len(routes) != 1:
        raise ReadinessExecutionError(
            "TASK_SESSION_ROUTE_NOT_UNIQUE", f"{unit_id}:{len(routes)}"
        )
    route = routes[0]
    entry = {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "task-ready",
        "selected_unit": unit_id,
        "route_id": route["route_id"],
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }
    validate_execution_entry(entry, policy)
    return entry


def fresh_resume_loop_state_digest(state: dict[str, Any]) -> str:
    """Digest the exact outer-loop projection controlled by fresh resumption."""

    return canonical_digest(
        {
            "loop_id": state["loop_id"],
            "work_pack_id": state["work_pack_id"],
            "work_pack_semantic_digest": state["work_pack_semantic_digest"],
            "captured_frontier": state["captured_frontier"],
            "completion_continuity_digest": state["completion_continuity"][
                "continuity_digest"
            ],
            "selected_unit": state["current_entry"]["selected_unit"],
            "binding_id": state["current_binding"]["binding_id"],
            "binding_digest": state["current_binding"]["binding_digest"],
            "steps_used": state["steps_used"],
            "step_budget": state["step_budget"],
            "owner_receipt_ids": [
                item["receipt_id"] for item in state["owner_receipts"]
            ],
            "task_session_receipt_ids": [
                item["receipt_id"] for item in state["task_session_receipts"]
            ],
        }
    )


def expected_fresh_resume_session_budget(state: dict[str, Any]) -> dict[str, int]:
    """Return the immutable fresh-session budget for the remaining frontier."""

    completed_count = len(state["completion_continuity"]["completed_prefix"])
    remaining_count = len(state["captured_frontier"]) - completed_count
    captured_session_budget = (
        1 if state["execution_mode"] == "one-unit" else remaining_count
    )
    return {
        "captured_max_task_sessions": captured_session_budget,
        "current_max_task_sessions": captured_session_budget,
        "task_sessions_started": len(state["task_session_receipts"]),
    }


def decide_task_session_with_fresh_resume(
    state: dict[str, Any],
    policy: dict[str, Any],
    resume_request: dict[str, Any],
    repository_root: Path,
    *,
    available_inputs: list[str],
    installed_owner_routes: list[dict[str, str]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Bind one outer-loop task action to the durable fresh-session owner."""

    if state["phase"] != "ready" or state["current_entry"]["entry_state"] != "task-ready":
        raise ReadinessExecutionError(
            "FRESH_RESUME_PHASE_INVALID", state["phase"]
        )
    if not state["owner_receipts"]:
        raise ReadinessExecutionError(
            "FRESH_RESUME_OWNER_JOIN_MISSING", state["loop_id"]
        )
    expected_state_digest = fresh_resume_loop_state_digest(state)
    exact_pairs = {
        "loop_id": state["loop_id"],
        "loop_state_digest": expected_state_digest,
        "work_pack_id": state["work_pack_id"],
        "work_pack_semantic_digest": state["work_pack_semantic_digest"],
        "captured_frontier": state["captured_frontier"],
        "selected_unit": state["current_entry"]["selected_unit"],
    }
    for field, expected in exact_pairs.items():
        if resume_request.get(field) != expected:
            raise ReadinessExecutionError("FRESH_RESUME_STATE_MISMATCH", field)

    latest_owner = state["owner_receipts"][-1]
    joined_owner = resume_request.get("owner_join", {}).get("receipt", {})
    owner_pairs = {
        "receipt_id": latest_owner["receipt_id"],
        "result": "pass",
        "route_fingerprint": latest_owner["route_fingerprint"],
    }
    for field, expected in owner_pairs.items():
        if joined_owner.get(field) != expected:
            raise ReadinessExecutionError("FRESH_RESUME_OWNER_JOIN_MISMATCH", field)
    joined_route = joined_owner.get("route", {})
    for field in ("capability", "mode"):
        if joined_route.get(field) != latest_owner[field]:
            raise ReadinessExecutionError("FRESH_RESUME_OWNER_JOIN_MISMATCH", field)

    session_budget = resume_request.get("session_budget", {})
    budget_pairs = expected_fresh_resume_session_budget(state)
    for field, expected in budget_pairs.items():
        if session_budget.get(field) != expected:
            raise ReadinessExecutionError("FRESH_RESUME_BUDGET_MISMATCH", field)
    expected_task_receipts = [
        {
            "unit_id": item["selected_unit"],
            "session_id": item["session_id"],
            "receipt_id": item["receipt_id"],
        }
        for item in state["task_session_receipts"]
    ]
    if resume_request.get("task_session_receipts") != expected_task_receipts:
        raise ReadinessExecutionError(
            "FRESH_RESUME_TASK_HISTORY_MISMATCH", state["loop_id"]
        )
    reclassified = resume_request.get("reclassification", {})
    reclassified_request = reclassified.get("request", {})
    if reclassified_request.get("execution_binding") != state["current_binding"]:
        raise ReadinessExecutionError(
            "FRESH_RESUME_BINDING_MISMATCH", state["loop_id"]
        )

    candidate_state, action = decide_next_action(
        state,
        policy,
        available_inputs=available_inputs,
        installed_owner_routes=installed_owner_routes,
    )
    if action["action_type"] != "start-task-session":
        raise ReadinessExecutionError(
            "FRESH_RESUME_TASK_ROUTE_BLOCKED",
            action.get("stop_reason") or action["action_type"],
        )
    admission = FRESH_SESSION.admit_fresh_task_session(
        resume_request, repository_root
    )
    if admission["decision"] != "start-fresh-session":
        raise ReadinessExecutionError(
            "FRESH_SESSION_ADMISSION_BLOCKED",
            f"{admission['code']}:{admission['detail']}",
        )
    fresh = admission["fresh_task_session"]
    current_binding = state["current_binding"]
    correlations = {
        "selector": state["current_entry"]["selected_unit"],
        "binding_id": current_binding["binding_id"],
        "binding_digest": current_binding["binding_digest"],
        "route_fingerprint": current_binding["route_fingerprint"],
        "expected_receipt": current_binding["current_route"]["expected_receipt"],
    }
    for field, expected in correlations.items():
        if fresh[field] != expected:
            raise ReadinessExecutionError("FRESH_SESSION_CORRELATION_MISMATCH", field)
    action["task_session_id"] = fresh["session_id"]
    candidate_state["pending_task_session_id"] = fresh["session_id"]
    return candidate_state, action, admission
