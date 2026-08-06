#!/usr/bin/env python3
"""Admit one durable fresh Task Session after a joined prerequisite owner hop."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


SPELL_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = Path(__file__).resolve().parents[3]
REQUEST_SCHEMA = SPELL_ROOT / "schemas" / "fresh-session-resume-request.schema.json"
RECEIPT_SCHEMA = SPELL_ROOT / "schemas" / "fresh-session-resume-receipt.schema.json"
FAST_GUARD_PATH = (
    ARCANUM_ROOT
    / "arcana"
    / "task-session"
    / "scripts"
    / "fast_execution_entry_guard.py"
)
ROUTER_PATH = (
    ARCANUM_ROOT
    / "arcana"
    / "continuation-router"
    / "scripts"
    / "work_pack_route.py"
)


def _load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load canonical owner module: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


FAST_GUARD = _load_module("wpeg_task_session_fast_guard", FAST_GUARD_PATH)
ROUTER = _load_module("wpeg_continuation_router", ROUTER_PATH)


class FreshSessionResumeError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _schema_errors(
    document: Any, schema_path: Path, label: str
) -> list[str]:
    return [
        f"{label} at "
        f"{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(_load_schema(schema_path)).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def _validate_request(request: dict[str, Any]) -> None:
    errors = _schema_errors(request, REQUEST_SCHEMA, "fresh-session request")
    if errors:
        raise FreshSessionResumeError("FRESH_SESSION_REQUEST_INVALID", errors[0])


def validate_fresh_session_receipt(
    receipt: dict[str, Any], request: dict[str, Any] | None = None
) -> dict[str, Any]:
    errors = _schema_errors(receipt, RECEIPT_SCHEMA, "fresh-session receipt")
    if errors:
        raise FreshSessionResumeError("FRESH_SESSION_RECEIPT_INVALID", errors[0])
    if request is not None:
        expected = {
            "chain_id": request.get("chain_id"),
            "loop_id": request.get("loop_id"),
            "loop_state_digest": request.get("loop_state_digest"),
            "work_pack_id": request.get("work_pack_id"),
            "work_pack_semantic_digest": request.get("work_pack_semantic_digest"),
            "selected_unit": request.get("selected_unit"),
            "captured_frontier": request.get("captured_frontier", []),
        }
        for field, value in expected.items():
            if receipt[field] != value:
                raise FreshSessionResumeError(
                    "FRESH_SESSION_RECEIPT_MISMATCH", field
                )
    return copy.deepcopy(receipt)


def _safe_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _safe_digest(value: Any) -> str | None:
    if (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    ):
        return value
    return None


def _safe_frontier(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result


def _safe_budget(request: dict[str, Any]) -> dict[str, int]:
    source = request.get("session_budget")
    if not isinstance(source, dict):
        source = {}

    def number(name: str) -> int:
        value = source.get(name)
        return value if isinstance(value, int) and value >= 0 else 0

    used = number("task_sessions_started")
    return {
        "captured": number("captured_max_task_sessions"),
        "current": number("current_max_task_sessions"),
        "used_before": used,
        "used_after": used,
    }


def _receipt_id(request: dict[str, Any], decision: str, code: str) -> str:
    seed = {
        "chain_id": request.get("chain_id"),
        "loop_id": request.get("loop_id"),
        "loop_state_digest": request.get("loop_state_digest"),
        "selected_unit": request.get("selected_unit"),
        "decision": decision,
        "code": code,
    }
    return f"fsr-{canonical_digest(seed)[:24]}"


def _owner_projection(
    owner_receipt: dict[str, Any] | None,
    owner_reference: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if owner_receipt is None or owner_reference is None:
        return None
    return {
        "receipt_id": owner_receipt["receipt_id"],
        "receipt_ref": copy.deepcopy(owner_reference),
        "binding_id": owner_receipt["binding_id"],
        "binding_digest": owner_receipt["binding_digest"],
        "route_fingerprint": owner_receipt["route_fingerprint"],
    }


def _receipt(
    request: dict[str, Any],
    *,
    decision: str,
    code: str,
    detail: str | None,
    owner_receipt: dict[str, Any] | None = None,
    owner_reference: dict[str, Any] | None = None,
    resumed_fingerprints: list[str] | None = None,
    fresh_session: dict[str, Any] | None = None,
    receipt_slot: dict[str, Any] | None = None,
    ledger_event_ref: dict[str, Any] | None = None,
) -> dict[str, Any]:
    budget = _safe_budget(request)
    if decision == "start-fresh-session":
        budget["used_after"] = budget["used_before"] + 1
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": _receipt_id(request, decision, code),
        "chain_id": _safe_string(request.get("chain_id")),
        "loop_id": _safe_string(request.get("loop_id")),
        "loop_state_digest": _safe_digest(request.get("loop_state_digest")),
        "work_pack_id": _safe_string(request.get("work_pack_id")),
        "work_pack_semantic_digest": _safe_digest(
            request.get("work_pack_semantic_digest")
        ),
        "selected_unit": _safe_string(request.get("selected_unit")),
        "decision": decision,
        "code": code,
        "detail": detail,
        "captured_frontier": _safe_frontier(request.get("captured_frontier")),
        "session_budget": budget,
        "original_task_session_id": _safe_string(
            request.get("original_task_session", {}).get("session_id")
            if isinstance(request.get("original_task_session"), dict)
            else None
        ),
        "joined_owner_receipt_count": 1 if owner_receipt is not None else 0,
        "owner_join": _owner_projection(owner_receipt, owner_reference),
        "resumed_route_fingerprints": copy.deepcopy(
            resumed_fingerprints
            if resumed_fingerprints is not None
            else [
                value
                for value in request.get("resumed_route_fingerprints", [])
                if _safe_digest(value) is not None
            ]
        ),
        "fresh_task_session_start_count": (
            1 if decision == "start-fresh-session" else 0
        ),
        "fresh_task_session": copy.deepcopy(fresh_session),
        "task_session_receipt_slot": copy.deepcopy(receipt_slot),
        "evidence_write_count": 1 if ledger_event_ref is not None else 0,
        "ledger_event_ref": copy.deepcopy(ledger_event_ref),
        "authorization_prompt_count": 0,
        "recursive_resume": False,
        "mutation_count": 0,
        "protected_effect_count": 0,
        "authority_effect": "none",
    }
    validate_fresh_session_receipt(receipt)
    return receipt


def _resolve_inside(root: Path, raw_path: str, *, must_exist: bool) -> Path:
    if (
        not raw_path
        or "\x00" in raw_path
        or "$" in raw_path
        or "*" in raw_path
        or "?" in raw_path
        or "\\" in raw_path
    ):
        raise FreshSessionResumeError("UNSAFE_PATH", raw_path)
    path = PurePosixPath(raw_path)
    if path.is_absolute() or PureWindowsPath(raw_path).is_absolute() or ".." in path.parts:
        raise FreshSessionResumeError("PATH_ESCAPE", raw_path)
    root = root.resolve()
    try:
        candidate = (root / str(path)).resolve(strict=must_exist)
    except FileNotFoundError as error:
        raise FreshSessionResumeError("JOIN_RECEIPT_MISSING", raw_path) from error
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise FreshSessionResumeError("PATH_ESCAPE", raw_path) from error
    return candidate


def _verify_exact_json(
    root: Path, reference: dict[str, Any], expected: dict[str, Any]
) -> None:
    path = _resolve_inside(root, reference["path"], must_exist=True)
    if not path.is_file():
        raise FreshSessionResumeError("JOIN_RECEIPT_MISSING", reference["path"])
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise FreshSessionResumeError("JOIN_RECEIPT_STALE", reference["path"])
    if len(content) != reference["size_bytes"]:
        raise FreshSessionResumeError("JOIN_RECEIPT_STALE", reference["path"])
    try:
        observed = json.loads(content)
    except json.JSONDecodeError as error:
        raise FreshSessionResumeError("JOIN_RECEIPT_INVALID", str(error)) from error
    if observed != expected:
        raise FreshSessionResumeError(
            "JOIN_RECEIPT_MISMATCH", reference["path"]
        )


def _validate_unique_task_receipts(receipts: list[dict[str, Any]]) -> None:
    for field in ("unit_id", "session_id", "receipt_id"):
        values = [receipt[field] for receipt in receipts]
        if len(values) != len(set(values)):
            raise FreshSessionResumeError(
                "TASK_SESSION_RECEIPT_REPLAY", field
            )


def _prepare(
    request: dict[str, Any], repository_root: Path
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[str],
    dict[str, Any],
    dict[str, Any],
]:
    _validate_request(request)
    root = repository_root.resolve()
    if request["selected_unit"] not in request["captured_frontier"]:
        raise FreshSessionResumeError(
            "SELECTED_UNIT_OUTSIDE_FRONTIER", request["selected_unit"]
        )

    budget = request["session_budget"]
    captured_budget = budget["captured_max_task_sessions"]
    if budget["current_max_task_sessions"] != captured_budget:
        raise FreshSessionResumeError(
            "SESSION_BUDGET_DRIFT", "current budget differs from captured budget"
        )
    if captured_budget > len(request["captured_frontier"]):
        raise FreshSessionResumeError(
            "SESSION_BUDGET_EXPANDED", "budget exceeds captured frontier"
        )
    if budget["task_sessions_started"] >= captured_budget:
        raise FreshSessionResumeError(
            "SESSION_BUDGET_EXHAUSTED", str(captured_budget)
        )
    if budget["task_sessions_started"] < len(request["task_session_receipts"]):
        raise FreshSessionResumeError(
            "SESSION_BUDGET_CONTRADICTORY", "fewer starts than terminal receipts"
        )

    original_pair = request["original_guard"]
    current_pair = request["reclassification"]
    try:
        original_receipt = FAST_GUARD.validate_fast_entry_receipt(
            original_pair["receipt"], original_pair["request"]
        )
        current_receipt = FAST_GUARD.validate_fast_entry_receipt(
            current_pair["receipt"], current_pair["request"]
        )
    except Exception as error:
        raise FreshSessionResumeError("FAST_GUARD_EVIDENCE_INVALID", str(error)) from error

    if original_receipt["decision"] != "route-owner":
        raise FreshSessionResumeError(
            "ORIGINAL_ENTRY_NOT_OWNER_PREREQUISITE", original_receipt["decision"]
        )
    if original_receipt["authorization_prompt_required"] is not False:
        raise FreshSessionResumeError(
            "OWNER_ROUTE_PROMPT_CONTRADICTION", original_receipt["receipt_id"]
        )

    original_request = original_pair["request"]
    current_request = current_pair["request"]
    policy = original_request["execution_policy"]
    if current_request["execution_policy"] != policy:
        raise FreshSessionResumeError(
            "WORK_PACK_POLICY_DRIFT", request["work_pack_id"]
        )
    exact_values = {
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "captured_frontier": policy["frontier"],
        "selected_unit": original_request["selected_unit"]["swu_id"],
    }
    for field, expected in exact_values.items():
        if request[field] != expected:
            raise FreshSessionResumeError("RESUME_IDENTITY_MISMATCH", field)
    if current_request["selected_unit"] != original_request["selected_unit"]:
        raise FreshSessionResumeError(
            "SELECTED_UNIT_DRIFT", request["selected_unit"]
        )

    route_pair = request["route_admission"]
    evaluated_admission = ROUTER.evaluate_work_pack_route(route_pair["request"])
    if route_pair["receipt"] != evaluated_admission:
        raise FreshSessionResumeError(
            "ROUTE_ADMISSION_RECEIPT_MISMATCH", original_receipt["receipt_id"]
        )
    if evaluated_admission["verdict"] != "pass":
        raise FreshSessionResumeError(
            "ROUTE_ADMISSION_BLOCKED", evaluated_admission["code"]
        )
    route = original_receipt["owner_packet"]
    if route_pair["request"]["execution_policy"] != policy:
        raise FreshSessionResumeError("ROUTE_ADMISSION_POLICY_MISMATCH", route["route_id"])
    if route_pair["request"]["execution_entry"] != original_request["execution_entry"]:
        raise FreshSessionResumeError("ROUTE_ADMISSION_ENTRY_MISMATCH", route["route_id"])
    if route_pair["request"]["execution_binding"] != original_request["execution_binding"]:
        raise FreshSessionResumeError("ROUTE_ADMISSION_BINDING_MISMATCH", route["route_id"])
    if evaluated_admission["matched_route"] != route:
        raise FreshSessionResumeError("ROUTE_ADMISSION_TARGET_MISMATCH", route["route_id"])

    owner_join = request["owner_join"]
    owner_receipt = owner_join["receipt"]
    _verify_exact_json(root, owner_join["receipt_ref"], owner_receipt)
    if owner_join["receipt_ref"]["path"] != route["expected_receipt"]:
        raise FreshSessionResumeError(
            "OWNER_RECEIPT_PATH_MISMATCH", owner_join["receipt_ref"]["path"]
        )
    owner_pairs = {
        "work_pack_id": request["work_pack_id"],
        "selected_unit": request["selected_unit"],
        "binding_id": original_receipt["binding_id"],
        "binding_digest": original_receipt["binding_digest"],
        "route_fingerprint": original_receipt["route_fingerprint"],
        "route": route,
    }
    for field, expected in owner_pairs.items():
        if owner_receipt[field] != expected:
            raise FreshSessionResumeError("OWNER_RECEIPT_MISMATCH", field)
    if owner_receipt["result"] != "pass":
        raise FreshSessionResumeError(
            "OWNER_PREREQUISITE_BLOCKED", owner_receipt["receipt_id"]
        )
    if evaluated_admission["route_fingerprint"] != owner_receipt["route_fingerprint"]:
        raise FreshSessionResumeError(
            "OWNER_ROUTER_FINGERPRINT_MISMATCH", owner_receipt["receipt_id"]
        )

    resumed = copy.deepcopy(request["resumed_route_fingerprints"])
    owner_fingerprint = owner_receipt["route_fingerprint"]
    if owner_fingerprint in resumed:
        raise FreshSessionResumeError(
            "OWNER_ROUTE_FINGERPRINT_REPEATED", owner_fingerprint
        )

    if current_receipt["decision"] == "route-owner":
        code = (
            "UNCHANGED_PREREQUISITE_FINGERPRINT"
            if current_receipt["route_fingerprint"] == owner_fingerprint
            else "PREREQUISITE_NOT_CLEARED"
        )
        raise FreshSessionResumeError(code, current_receipt["route_fingerprint"])
    if current_receipt["decision"] != "proceed":
        raise FreshSessionResumeError(
            "RECLASSIFIED_ENTRY_BLOCKED", current_receipt["code"]
        )
    task_route = current_request["execution_binding"]["current_route"]
    if task_route["capability"] != "task-session" or task_route["mode"] != "execute":
        raise FreshSessionResumeError(
            "FRESH_SESSION_ROUTE_INVALID", f"{task_route['capability']}:{task_route['mode']}"
        )

    original_session = request["original_task_session"]
    if original_session["session_id"] not in request["visited_task_session_ids"]:
        raise FreshSessionResumeError(
            "ORIGINAL_SESSION_HISTORY_MISSING", original_session["session_id"]
        )
    if original_session["cursor"] not in request["visited_session_cursors"]:
        raise FreshSessionResumeError(
            "ORIGINAL_CURSOR_HISTORY_MISSING", original_session["cursor"]
        )

    _validate_unique_task_receipts(request["task_session_receipts"])
    if any(
        receipt["unit_id"] == request["selected_unit"]
        for receipt in request["task_session_receipts"]
    ):
        raise FreshSessionResumeError(
            "TASK_SESSION_RECEIPT_SLOT_ALREADY_USED", request["selected_unit"]
        )

    session_seed = {
        "chain_id": request["chain_id"],
        "loop_id": request["loop_id"],
        "loop_state_digest": request["loop_state_digest"],
        "selected_unit": request["selected_unit"],
        "original_task_session_id": original_session["session_id"],
        "owner_receipt_id": owner_receipt["receipt_id"],
        "owner_route_fingerprint": owner_fingerprint,
        "task_binding_id": current_receipt["binding_id"],
        "task_route_fingerprint": current_receipt["route_fingerprint"],
    }
    fresh_session = {
        "session_id": f"task-session-{canonical_digest(session_seed)[:24]}",
        "cursor": f"cursor-{canonical_digest({'fresh': session_seed})[:24]}",
        "selector": request["selected_unit"],
        "action": "task-session:execute",
        "binding_id": current_receipt["binding_id"],
        "binding_digest": current_receipt["binding_digest"],
        "route_fingerprint": current_receipt["route_fingerprint"],
        "expected_receipt": task_route["expected_receipt"],
    }
    if fresh_session["session_id"] == original_session["session_id"]:
        raise FreshSessionResumeError(
            "RECURSIVE_TASK_SESSION_RESUME", fresh_session["session_id"]
        )
    if fresh_session["session_id"] in request["visited_task_session_ids"]:
        raise FreshSessionResumeError(
            "TASK_SESSION_ID_REPEATED", fresh_session["session_id"]
        )
    if fresh_session["cursor"] in request["visited_session_cursors"]:
        raise FreshSessionResumeError(
            "TASK_SESSION_CURSOR_REPEATED", fresh_session["cursor"]
        )

    resumed.append(owner_fingerprint)
    receipt_slot = {
        "unit_id": request["selected_unit"],
        "expected_receipt": task_route["expected_receipt"],
        "maximum_receipts": 1,
    }
    return owner_receipt, owner_join["receipt_ref"], resumed, fresh_session, receipt_slot


def _exclusive_write(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, payload)
    finally:
        os.close(descriptor)


def _exact_ref(root: Path, path: Path, content: bytes) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def admit_fresh_task_session(
    request: dict[str, Any], repository_root: Path
) -> dict[str, Any]:
    """Validate, persist, and return exactly one fresh Task Session admission."""

    owner_receipt: dict[str, Any] | None = None
    owner_reference: dict[str, Any] | None = None
    try:
        (
            owner_receipt,
            owner_reference,
            resumed,
            fresh_session,
            receipt_slot,
        ) = _prepare(request, repository_root)
        root = repository_root.resolve()
        state_root = _resolve_inside(
            root, request["resume_state_directory"], must_exist=False
        )
        admissions = state_root / "fresh-session-admissions"
        admissions.mkdir(parents=True, exist_ok=True)
        event_path = admissions / f"{fresh_session['session_id']}.json"
        start_receipt_id = _receipt_id(
            request, "start-fresh-session", "FRESH_TASK_SESSION_READY"
        )
        event = {
            "schema_version": "1.0.0",
            "event_type": "fresh-task-session-admitted",
            "event_id": f"fsa-{canonical_digest({'session': fresh_session['session_id']})[:24]}",
            "receipt_id": start_receipt_id,
            "request_digest": canonical_digest(request),
            "chain_id": request["chain_id"],
            "loop_id": request["loop_id"],
            "loop_state_digest": request["loop_state_digest"],
            "work_pack_id": request["work_pack_id"],
            "selected_unit": request["selected_unit"],
            "original_task_session_id": request["original_task_session"]["session_id"],
            "owner_receipt_id": owner_receipt["receipt_id"],
            "owner_route_fingerprint": owner_receipt["route_fingerprint"],
            "fresh_task_session": copy.deepcopy(fresh_session),
            "authority_effect": "none",
        }
        content = json.dumps(event, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        try:
            _exclusive_write(event_path, content)
        except FileExistsError as error:
            raise FreshSessionResumeError(
                "FRESH_SESSION_REPLAY", fresh_session["session_id"]
            ) from error
        ledger_reference = _exact_ref(root, event_path, content)
        return _receipt(
            request,
            decision="start-fresh-session",
            code="FRESH_TASK_SESSION_READY",
            detail=None,
            owner_receipt=owner_receipt,
            owner_reference=owner_reference,
            resumed_fingerprints=resumed,
            fresh_session=fresh_session,
            receipt_slot=receipt_slot,
            ledger_event_ref=ledger_reference,
        )
    except FreshSessionResumeError as error:
        return _receipt(
            request,
            decision="block",
            code=error.code,
            detail=error.detail,
            owner_receipt=owner_receipt,
            owner_reference=owner_reference,
        )

