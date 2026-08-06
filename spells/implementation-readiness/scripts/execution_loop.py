#!/usr/bin/env python3
"""Deterministic outer-loop reducer for Work-Pack-bound execution."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from execution_contracts import (
    ExecutionContractError,
    build_execution_intent_binding,
    canonical_digest,
    route_map,
    validate_execution_binding,
    validate_execution_entry,
    validate_execution_policy,
)
from implementation_readiness_runtime_paths import capability_root


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = SPELL_ROOT / "schemas"
STATE_SCHEMA = SCHEMA_ROOT / "outer-loop-state.schema.json"
ACTION_SCHEMA = SCHEMA_ROOT / "outer-loop-action.schema.json"
EVENT_SCHEMA = SCHEMA_ROOT / "outer-loop-event.schema.json"
ROUTER_SCRIPTS = capability_root("continuation-router", "arcana") / "scripts"
if str(ROUTER_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ROUTER_SCRIPTS))

from work_pack_route import evaluate_work_pack_route  # noqa: E402


class OuterLoopError(ValueError):
    """One stable fail-closed outer-loop diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _validate_schema(document: dict[str, Any], path: Path, label: str) -> None:
    validator = Draft202012Validator(
        _load_schema(path), format_checker=FormatChecker()
    )
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or label
        raise OuterLoopError(
            "OUTER_LOOP_SCHEMA_INVALID", f"{label} at {location}: {error.message}"
        )


def _build_binding(state: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    return build_execution_intent_binding(
        policy,
        state["current_entry"],
        source_invocation_id=state["source_invocation_id"],
        created_at=state["created_at"],
        execution_mode=state["execution_mode"],
    )


def _historical_units(state: dict[str, Any]) -> list[str]:
    return [
        item["unit_id"]
        for item in state["completion_continuity"]["completed_prefix"]
    ]


def _frontier_cursor(state: dict[str, Any]) -> int:
    return len(_historical_units(state)) + len(state["visited_units"])


def _validate_state(state: dict[str, Any], policy: dict[str, Any]) -> None:
    _validate_schema(state, STATE_SCHEMA, "outer-loop state")
    validate_execution_policy(policy)
    if state["work_pack_id"] != policy["work_pack_id"]:
        raise OuterLoopError("WORK_PACK_ID_MISMATCH", state["work_pack_id"])
    if state["work_pack_semantic_digest"] != policy["work_pack_semantic_digest"]:
        raise OuterLoopError("WORK_PACK_SEMANTIC_STALE", state["work_pack_id"])
    if state["allowed_routes_digest"] != policy["allowed_routes_digest"]:
        raise OuterLoopError("ALLOWED_ROUTES_DIGEST_STALE", state["work_pack_id"])
    if state["captured_frontier"] != policy["frontier"]:
        raise OuterLoopError("FRONTIER_STALE", state["work_pack_id"])
    if state["completion_continuity"] != policy["completion_continuity"]:
        raise OuterLoopError(
            "CONTINUITY_POLICY_STATE_MISMATCH", state["work_pack_id"]
        )
    historical = _historical_units(state)
    if historical != policy["frontier"][: len(historical)]:
        raise OuterLoopError(
            "CONTINUITY_NON_PREFIX_COMPLETION", state["work_pack_id"]
        )
    visited_start = len(historical)
    visited_end = visited_start + len(state["visited_units"])
    if state["visited_units"] != policy["frontier"][visited_start:visited_end]:
        raise OuterLoopError("FRONTIER_ORDER_MISMATCH", state["work_pack_id"])
    expected_next = (
        policy["frontier"][_frontier_cursor(state)]
        if _frontier_cursor(state) < len(policy["frontier"])
        else None
    )
    if (
        not state["visited_units"]
        and state["completion_continuity"]["next_unit"] != expected_next
    ):
        raise OuterLoopError(
            "CONTINUITY_CURSOR_CONTRADICTION", state["work_pack_id"]
        )
    if state["steps_used"] > state["step_budget"]:
        raise OuterLoopError("STEP_BUDGET_EXCEEDED", state["work_pack_id"])
    if len({item["receipt_id"] for item in state["owner_receipts"]}) != len(
        state["owner_receipts"]
    ):
        raise OuterLoopError("OWNER_RECEIPT_REPLAY", state["work_pack_id"])
    for receipt in state["owner_receipts"]:
        if receipt["result"] == "pass" and receipt["blocker_code"] is not None:
            raise OuterLoopError("OWNER_RECEIPT_CONTRADICTION", receipt["receipt_id"])
        if (
            receipt["result"] == "retry"
            and receipt["blocker_code"] != "REPAIRABLE_OWNER_CONDITION"
        ):
            raise OuterLoopError("RETRY_CONDITION_INVALID", receipt["receipt_id"])
    for fingerprint, count in state["route_retry_counts"].items():
        if count != 1 or not any(
            item["result"] == "retry"
            and item["route_fingerprint"] == fingerprint
            for item in state["owner_receipts"]
        ):
            raise OuterLoopError("RETRY_HISTORY_INVALID", fingerprint)
        if fingerprint not in state["consumed_route_fingerprints"]:
            raise OuterLoopError("RETRY_HISTORY_RELEASED", fingerprint)
    pending_retry = state["pending_retry"]
    if pending_retry is not None:
        pending_fingerprint = pending_retry["route_fingerprint"]
        pending_receipt = next(
            (
                item
                for item in state["owner_receipts"]
                if item["receipt_id"] == pending_retry["owner_receipt_id"]
            ),
            None,
        )
        current_route = state["current_binding"]["current_route"]
        if (
            state["phase"] != "ready"
            or state["current_entry"]["entry_state"] != "owner-prerequisite"
            or state["current_binding"]["route_fingerprint"] != pending_fingerprint
            or state["route_retry_counts"].get(pending_fingerprint) != 1
            or pending_fingerprint not in state["consumed_route_fingerprints"]
            or pending_retry["blocker_code"] != "REPAIRABLE_OWNER_CONDITION"
            or pending_receipt is None
            or pending_receipt["result"] != "retry"
            or pending_receipt["blocker_code"] != pending_retry["blocker_code"]
            or pending_receipt["route_fingerprint"] != pending_fingerprint
            or pending_receipt["capability"] != current_route["capability"]
            or pending_receipt["mode"] != current_route["mode"]
        ):
            raise OuterLoopError("PENDING_RETRY_INVALID", pending_fingerprint)
    if len({item["receipt_id"] for item in state["task_session_receipts"]}) != len(
        state["task_session_receipts"]
    ):
        raise OuterLoopError("TASK_RECEIPT_REPLAY", state["work_pack_id"])
    if len({item["session_id"] for item in state["task_session_receipts"]}) != len(
        state["task_session_receipts"]
    ):
        raise OuterLoopError("TASK_SESSION_REUSED", state["work_pack_id"])
    validate_execution_binding(
        state["current_binding"], policy, state["current_entry"]
    )
    if state["current_binding"]["binding_id"] not in state["binding_ids"]:
        raise OuterLoopError("BINDING_HISTORY_INCOMPLETE", state["work_pack_id"])
    if state["phase"].startswith("awaiting-"):
        if state["pending_action_id"] is None:
            raise OuterLoopError("PENDING_ACTION_MISSING", state["phase"])
    elif state["pending_action_id"] is not None:
        raise OuterLoopError("PENDING_ACTION_STALE", state["phase"])
    if state["phase"] == "awaiting-task-session":
        if state["pending_task_session_id"] is None:
            raise OuterLoopError("PENDING_TASK_SESSION_MISSING", state["phase"])
    elif state["pending_task_session_id"] is not None:
        raise OuterLoopError("PENDING_TASK_SESSION_STALE", state["phase"])
    if state["phase"] in {"complete", "blocked"} and state["stop_reason"] is None:
        raise OuterLoopError("TERMINAL_REASON_MISSING", state["phase"])
    if state["phase"] not in {"complete", "blocked"} and state["stop_reason"] is not None:
        raise OuterLoopError("TERMINAL_REASON_EARLY", state["phase"])
    selected = state["current_entry"]["selected_unit"]
    if (
        selected is not None
        and state["phase"] not in {"complete", "blocked"}
        and state["current_entry"]["entry_state"] != "blocked"
        and selected != _expected_frontier_unit(state)
    ):
        raise OuterLoopError(
            "CONTINUITY_CURSOR_CONTRADICTION",
            f"expected {_expected_frontier_unit(state)}, got {selected}",
        )


def initialize_outer_loop(
    policy: dict[str, Any],
    entry: dict[str, Any],
    *,
    source_invocation_id: str,
    created_at: str,
    execution_mode: str,
    step_budget: int,
) -> dict[str, Any]:
    validate_execution_entry(entry, policy)
    if "completion_continuity" not in policy:
        raise OuterLoopError("CONTINUITY_PROJECTION_MISSING", policy["work_pack_id"])
    if step_budget < 1:
        raise OuterLoopError("STEP_BUDGET_INVALID", str(step_budget))
    binding = build_execution_intent_binding(
        policy,
        entry,
        source_invocation_id=source_invocation_id,
        created_at=created_at,
        execution_mode=execution_mode,
    )
    loop_seed = {
        "source_invocation_id": source_invocation_id,
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "captured_frontier": policy["frontier"],
        "completion_continuity_digest": policy["completion_continuity"][
            "continuity_digest"
        ],
        "execution_mode": execution_mode,
    }
    state = {
        "schema_version": "1.2.0",
        "loop_id": f"wpol-{canonical_digest(loop_seed)[:24]}",
        "source_invocation_id": source_invocation_id,
        "created_at": created_at,
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "execution_mode": execution_mode,
        "captured_frontier": copy.deepcopy(policy["frontier"]),
        "completion_continuity": copy.deepcopy(policy["completion_continuity"]),
        "phase": "ready",
        "current_entry": copy.deepcopy(entry),
        "current_binding": binding,
        "binding_ids": [binding["binding_id"]],
        "pending_action_id": None,
        "pending_task_session_id": None,
        "step_budget": step_budget,
        "steps_used": 0,
        "visited_units": [],
        "consumed_route_fingerprints": [],
        "route_retry_counts": {},
        "pending_retry": None,
        "owner_receipts": [],
        "task_session_receipts": [],
        "automatic_decisions": [],
        "authorization_prompt_count": 0,
        "pending_stop_decision": None,
        "stop_reason": None,
        "authority_effect": "none",
    }
    _validate_state(state, policy)
    return state


def _action(
    state: dict[str, Any],
    *,
    action_type: str,
    phase_before: str,
    selected_unit: str | None,
    owner_route: dict[str, Any] | None = None,
    admission: dict[str, Any] | None = None,
    task_session_id: str | None = None,
    authorization_source: str = "none",
    automatic_decision: str | None = None,
    stop_reason: str | None = None,
) -> dict[str, Any]:
    seed = {
        "loop_id": state["loop_id"],
        "steps_used": state["steps_used"],
        "action_type": action_type,
        "phase_before": phase_before,
        "phase_after": state["phase"],
        "selected_unit": selected_unit,
        "binding_id": state["current_binding"]["binding_id"],
        "stop_reason": stop_reason,
    }
    action = {
        "schema_version": "1.0.0",
        "action_id": f"wpoa-{canonical_digest(seed)[:24]}",
        "action_type": action_type,
        "phase_before": phase_before,
        "phase_after": state["phase"],
        "selected_unit": selected_unit,
        "owner_route": copy.deepcopy(owner_route),
        "route_admission": copy.deepcopy(admission),
        "task_session_id": task_session_id,
        "authorization_source": authorization_source,
        "authorization_prompt_required": False,
        "automatic_decision": automatic_decision,
        "stop_reason": stop_reason,
        "authority_effect": "none",
    }
    _validate_schema(action, ACTION_SCHEMA, "outer-loop action")
    return action


def _record_automatic(
    state: dict[str, Any], decision_class: str, action_type: str, selected_unit: str | None
) -> None:
    state["automatic_decisions"].append(
        {
            "sequence": len(state["automatic_decisions"]) + 1,
            "decision_class": decision_class,
            "action_type": action_type,
            "selected_unit": selected_unit,
        }
    )


def _block_action(
    state: dict[str, Any], reason: str, phase_before: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    state["phase"] = "blocked"
    state["stop_reason"] = reason
    state["pending_stop_decision"] = None
    state["pending_action_id"] = None
    state["pending_task_session_id"] = None
    state["pending_retry"] = None
    action = _action(
        state,
        action_type="stop",
        phase_before=phase_before,
        selected_unit=state["current_entry"]["selected_unit"],
        stop_reason=reason,
    )
    return state, action


def decide_next_action(
    state: dict[str, Any],
    policy: dict[str, Any],
    *,
    available_inputs: list[str],
    installed_owner_routes: list[dict[str, str]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = copy.deepcopy(state)
    _validate_state(state, policy)
    phase_before = state["phase"]
    if phase_before == "complete":
        return state, _action(
            state,
            action_type="complete",
            phase_before=phase_before,
            selected_unit=None,
            stop_reason=state["stop_reason"],
        )
    if phase_before == "blocked":
        return state, _action(
            state,
            action_type="stop",
            phase_before=phase_before,
            selected_unit=state["current_entry"]["selected_unit"],
            stop_reason=state["stop_reason"],
        )
    if phase_before != "ready":
        return _block_action(state, "JOIN_REQUIRED", phase_before)
    if state["pending_stop_decision"] is not None:
        decision = state["pending_stop_decision"]
        if decision not in policy["stop_decisions"]:
            return _block_action(state, "STOP_DECISION_UNDECLARED", phase_before)
        return _block_action(state, decision, phase_before)
    if state["steps_used"] >= state["step_budget"]:
        return _block_action(state, "STEP_BUDGET_EXHAUSTED", phase_before)

    entry = state["current_entry"]
    entry_state = entry["entry_state"]
    if entry_state == "blocked":
        return _block_action(state, entry["blocker_code"], phase_before)
    if entry_state == "selection-ready":
        expected_index = _frontier_cursor(state)
        if expected_index >= len(state["captured_frontier"]):
            state["phase"] = "complete"
            state["stop_reason"] = "FRONTIER_COMPLETE"
            return state, _action(
                state,
                action_type="complete",
                phase_before=phase_before,
                selected_unit=None,
                stop_reason="FRONTIER_COMPLETE",
            )
        selected_unit = state["captured_frontier"][expected_index]
        state["phase"] = "awaiting-selection"
        _record_automatic(
            state, "internal-tool-selection", "select-unit", selected_unit
        )
        action = _action(
            state,
            action_type="select-unit",
            phase_before=phase_before,
            selected_unit=selected_unit,
            authorization_source="not-required",
            automatic_decision="internal-tool-selection",
        )
        state["pending_action_id"] = action["action_id"]
        return state, action

    route = route_map(policy).get(entry["route_id"])
    if route is None:
        return _block_action(state, "ROUTE_UNDECLARED", phase_before)
    retrying = state["pending_retry"] is not None
    current_fingerprint = state["current_binding"]["route_fingerprint"]
    consumed_for_admission = copy.deepcopy(state["consumed_route_fingerprints"])
    if retrying:
        consumed_for_admission = [
            fingerprint
            for fingerprint in consumed_for_admission
            if fingerprint != current_fingerprint
        ]
    request = {
        "schema_version": "1.0.0",
        "execution_policy": copy.deepcopy(policy),
        "execution_entry": copy.deepcopy(entry),
        "execution_binding": copy.deepcopy(state["current_binding"]),
        "candidate_routes": [copy.deepcopy(route)],
        "installed_owner_routes": copy.deepcopy(installed_owner_routes),
        "available_inputs": copy.deepcopy(available_inputs),
        "consumed_route_fingerprints": consumed_for_admission,
        "authorization_flag": None,
        "authority_effect": "none",
    }
    admission = evaluate_work_pack_route(request)
    if admission["verdict"] != "pass":
        return _block_action(state, admission["code"], phase_before)

    state["steps_used"] += 1
    if not retrying:
        state["consumed_route_fingerprints"].append(current_fingerprint)
    selected_unit = entry["selected_unit"] or route["frontier_swu"]
    if entry_state == "owner-prerequisite":
        state["phase"] = "awaiting-owner"
        decision_class = (
            "declared-retry" if retrying else "capability-owner-routing"
        )
        _record_automatic(
            state, decision_class, "route-owner", selected_unit
        )
        action = _action(
            state,
            action_type="route-owner",
            phase_before=phase_before,
            selected_unit=selected_unit,
            owner_route=route,
            admission=admission,
            authorization_source="work-pack-binding",
            automatic_decision=decision_class,
        )
        state["pending_action_id"] = action["action_id"]
        state["pending_retry"] = None
        return state, action
    if entry_state == "task-ready":
        session_seed = {
            "loop_id": state["loop_id"],
            "selected_unit": selected_unit,
            "task_session_count": len(state["task_session_receipts"]),
            "route_fingerprint": state["current_binding"]["route_fingerprint"],
        }
        session_id = f"task-session-{canonical_digest(session_seed)[:20]}"
        if any(
            receipt["session_id"] == session_id
            for receipt in state["task_session_receipts"]
        ):
            return _block_action(state, "TASK_SESSION_REUSED", phase_before)
        state["phase"] = "awaiting-task-session"
        _record_automatic(
            state,
            "fresh-task-session-resumption",
            "start-task-session",
            selected_unit,
        )
        action = _action(
            state,
            action_type="start-task-session",
            phase_before=phase_before,
            selected_unit=selected_unit,
            owner_route=route,
            admission=admission,
            task_session_id=session_id,
            authorization_source="work-pack-binding",
            automatic_decision="fresh-task-session-resumption",
        )
        state["pending_action_id"] = action["action_id"]
        state["pending_task_session_id"] = session_id
        return state, action
    return _block_action(state, "ENTRY_STATE_UNKNOWN", phase_before)


def _replace_entry(
    state: dict[str, Any], policy: dict[str, Any], entry: dict[str, Any]
) -> None:
    validate_execution_entry(entry, policy)
    state["current_entry"] = copy.deepcopy(entry)
    binding = _build_binding(state, policy)
    state["current_binding"] = binding
    if binding["binding_id"] not in state["binding_ids"]:
        state["binding_ids"].append(binding["binding_id"])


def _expected_frontier_unit(state: dict[str, Any]) -> str | None:
    index = _frontier_cursor(state)
    if index >= len(state["captured_frontier"]):
        return None
    return state["captured_frontier"][index]


def _assert_next_entry_unit(state: dict[str, Any], entry: dict[str, Any]) -> None:
    expected = _expected_frontier_unit(state)
    selected = entry["selected_unit"]
    if entry["entry_state"] == "selection-ready":
        if selected is not None:
            raise OuterLoopError("FRONTIER_ABSORPTION_BLOCKED", str(selected))
    elif selected != expected:
        raise OuterLoopError(
            "FRONTIER_ABSORPTION_BLOCKED", f"expected {expected}, got {selected}"
        )


def join_event(
    state: dict[str, Any], policy: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any]:
    state = copy.deepcopy(state)
    _validate_state(state, policy)
    _validate_schema(event, EVENT_SCHEMA, "outer-loop event")
    expected_event = {
        "awaiting-selection": "selection-materialized",
        "awaiting-owner": "owner-joined",
        "awaiting-task-session": "task-session-joined",
    }.get(state["phase"])
    if event["event_type"] != expected_event:
        raise OuterLoopError(
            "EVENT_PHASE_MISMATCH", f"{state['phase']}:{event['event_type']}"
        )
    if event["action_id"] != state["pending_action_id"]:
        raise OuterLoopError(
            "ACTION_CORRELATION_MISMATCH",
            f"expected {state['pending_action_id']}, got {event['action_id']}",
        )
    if event["stop_decision"] is not None and event["stop_decision"] not in policy["stop_decisions"]:
        raise OuterLoopError("STOP_DECISION_UNDECLARED", event["stop_decision"])

    current_fingerprint = state["current_binding"]["route_fingerprint"]
    expected_unit = _expected_frontier_unit(state)
    if state["phase"] == "awaiting-selection":
        if event["selected_unit"] != expected_unit:
            raise OuterLoopError(
                "FRONTIER_ABSORPTION_BLOCKED",
                f"expected {expected_unit}, got {event['selected_unit']}",
            )
        if event["receipt_id"] is not None or event["session_id"] is not None:
            raise OuterLoopError("SELECTION_OWNER_IMPERSONATION", state["loop_id"])
    else:
        if event["route_fingerprint"] != current_fingerprint:
            raise OuterLoopError("ROUTE_FINGERPRINT_STALE", state["loop_id"])
        if event["receipt_id"] is None:
            raise OuterLoopError("JOIN_RECEIPT_MISSING", state["loop_id"])

    if event["result"] == "retry":
        if state["phase"] != "awaiting-owner":
            raise OuterLoopError("RETRY_PHASE_INVALID", state["phase"])
        if event["selected_unit"] != state["current_entry"]["selected_unit"]:
            raise OuterLoopError("OWNER_UNIT_MISMATCH", str(event["selected_unit"]))
        if event["blocker_code"] != "REPAIRABLE_OWNER_CONDITION":
            raise OuterLoopError("RETRY_CONDITION_INVALID", state["loop_id"])
        if event["stop_decision"] is not None:
            raise OuterLoopError("RETRY_STOP_CONTRADICTION", event["stop_decision"])
        if event["next_entry"] != state["current_entry"]:
            raise OuterLoopError("RETRY_ROUTE_CHANGED", state["loop_id"])
        route = state["current_binding"]["current_route"]
        state["owner_receipts"].append(
            {
                "receipt_id": event["receipt_id"],
                "result": "retry",
                "capability": route["capability"],
                "mode": route["mode"],
                "route_fingerprint": current_fingerprint,
                "blocker_code": event["blocker_code"],
            }
        )
        state["pending_action_id"] = None
        if "declared-retry" not in policy["automatic_decisions"]:
            state["phase"] = "blocked"
            state["stop_reason"] = "RETRY_UNDECLARED"
            _validate_state(state, policy)
            return state
        if state["route_retry_counts"].get(current_fingerprint, 0) >= 1:
            state["phase"] = "blocked"
            state["stop_reason"] = "DECLARED_RETRY_EXHAUSTED"
            _validate_state(state, policy)
            return state
        if current_fingerprint not in state["consumed_route_fingerprints"]:
            raise OuterLoopError("RETRY_ROUTE_NOT_CONSUMED", current_fingerprint)
        state["route_retry_counts"][current_fingerprint] = 1
        state["pending_retry"] = {
            "route_fingerprint": current_fingerprint,
            "blocker_code": event["blocker_code"],
            "owner_receipt_id": event["receipt_id"],
        }
        state["phase"] = "ready"
        _validate_state(state, policy)
        return state

    if event["result"] == "block":
        if state["phase"] == "awaiting-owner":
            route = state["current_binding"]["current_route"]
            state["owner_receipts"].append(
                {
                    "receipt_id": event["receipt_id"],
                    "result": "block",
                    "capability": route["capability"],
                    "mode": route["mode"],
                    "route_fingerprint": current_fingerprint,
                    "blocker_code": event["blocker_code"],
                }
            )
        elif state["phase"] == "awaiting-task-session":
            if event["session_id"] is None:
                raise OuterLoopError("TASK_SESSION_ID_MISSING", state["loop_id"])
            if event["session_id"] != state["pending_task_session_id"]:
                raise OuterLoopError("TASK_SESSION_CORRELATION_MISMATCH", event["session_id"])
            state["task_session_receipts"].append(
                {
                    "receipt_id": event["receipt_id"],
                    "session_id": event["session_id"],
                    "selected_unit": event["selected_unit"],
                    "result": "block",
                    "route_fingerprint": current_fingerprint,
                }
            )
        state["phase"] = "blocked"
        state["pending_action_id"] = None
        state["pending_task_session_id"] = None
        state["stop_reason"] = (
            event["stop_decision"] or event["blocker_code"] or "OWNER_BLOCKED"
        )
        _validate_state(state, policy)
        return state

    if event["blocker_code"] is not None or event["stop_decision"] is not None:
        raise OuterLoopError("PASS_EVENT_CONTRADICTION", event["event_type"])
    if event["next_entry"] is None:
        if (
            state["phase"] != "awaiting-task-session"
            or (
                state["execution_mode"] != "one-unit"
                and _frontier_cursor(state) + 1 != len(state["captured_frontier"])
            )
        ):
            raise OuterLoopError("NEXT_ENTRY_MISSING", event["event_type"])

    if state["phase"] == "awaiting-selection":
        _assert_next_entry_unit(state, event["next_entry"])
        _replace_entry(state, policy, event["next_entry"])
        state["pending_action_id"] = None
        state["phase"] = "ready"
    elif state["phase"] == "awaiting-owner":
        route = state["current_binding"]["current_route"]
        state["owner_receipts"].append(
            {
                "receipt_id": event["receipt_id"],
                "result": "pass",
                "capability": route["capability"],
                "mode": route["mode"],
                "route_fingerprint": current_fingerprint,
                "blocker_code": None,
            }
        )
        _assert_next_entry_unit(state, event["next_entry"])
        _replace_entry(state, policy, event["next_entry"])
        state["pending_action_id"] = None
        state["phase"] = "ready"
    else:
        if event["session_id"] is None:
            raise OuterLoopError("TASK_SESSION_ID_MISSING", state["loop_id"])
        if event["session_id"] != state["pending_task_session_id"]:
            raise OuterLoopError("TASK_SESSION_CORRELATION_MISMATCH", event["session_id"])
        if event["selected_unit"] != state["current_entry"]["selected_unit"]:
            raise OuterLoopError("TASK_SESSION_UNIT_MISMATCH", str(event["selected_unit"]))
        if any(
            receipt["session_id"] == event["session_id"]
            for receipt in state["task_session_receipts"]
        ):
            raise OuterLoopError("TASK_SESSION_REUSED", event["session_id"])
        state["task_session_receipts"].append(
            {
                "receipt_id": event["receipt_id"],
                "session_id": event["session_id"],
                "selected_unit": event["selected_unit"],
                "result": "pass",
                "route_fingerprint": current_fingerprint,
            }
        )
        state["visited_units"].append(event["selected_unit"])
        state["pending_action_id"] = None
        state["pending_task_session_id"] = None
        if (
            state["execution_mode"] == "one-unit"
            or _frontier_cursor(state) == len(state["captured_frontier"])
        ):
            state["phase"] = "complete"
            state["stop_reason"] = "FRONTIER_COMPLETE"
        else:
            _assert_next_entry_unit(state, event["next_entry"])
            _replace_entry(state, policy, event["next_entry"])
            state["phase"] = "ready"
    _validate_state(state, policy)
    return state


def set_stop_decision(
    state: dict[str, Any], policy: dict[str, Any], decision: str
) -> dict[str, Any]:
    state = copy.deepcopy(state)
    _validate_state(state, policy)
    if state["phase"] != "ready":
        raise OuterLoopError("STOP_DECISION_PHASE_INVALID", state["phase"])
    if decision not in policy["stop_decisions"]:
        raise OuterLoopError("STOP_DECISION_UNDECLARED", decision)
    state["pending_stop_decision"] = decision
    _validate_state(state, policy)
    return state


def validate_outer_loop_state(
    state: dict[str, Any], policy: dict[str, Any]
) -> dict[str, Any]:
    _validate_state(state, policy)
    return copy.deepcopy(state)
