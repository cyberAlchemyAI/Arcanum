#!/usr/bin/env python3
"""Fail-closed native-dispatch evidence and wave-advance driver.

The driver never calls a host-native operation. It makes the request for a
host call available only after the matching pre-call event is durably appended,
records post-call results, separates non-causal residue, and exposes dependent
actions only after exact receipt admission and a causal gate append.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import native_dispatch_coordinator as coordinator  # noqa: E402
import validate_run_evidence as evidence  # noqa: E402


RUN_EVENT_SCHEMA_VERSION = "arcanum.native-dispatch-runner.run-event.v0.1"
RESIDUE_SCHEMA_VERSION = "arcanum.native-dispatch-runner.run-residue.v0.1"
RECEIPT_ADMISSION_SCHEMA_VERSION = (
    "arcanum.native-dispatch-runner.receipt-admission.v0.1"
)
RESIDUE_REQUIRED_FIELDS = {
    "recorded_at",
    "kind",
    "dispatch_id",
    "run_id",
    "wave_id",
    "action_id",
    "agent_id",
    "summary",
    "source_refs",
}
RESIDUE_KINDS = {
    "feedback",
    "governance",
    "commentary",
    "evidence_closure",
    "reduction_note",
    "other",
}


class DriverBlocked(RuntimeError):
    """Raised before a host request or dependent action can be exposed."""

    def __init__(self, blockers: list[str]) -> None:
        normalized = sorted(set(str(item) for item in blockers if str(item)))
        super().__init__("; ".join(normalized))
        self.blockers = normalized


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DriverBlocked([f"cannot load {label}: {exc}"]) from exc
    if not isinstance(value, dict):
        raise DriverBlocked([f"{label} root must be an object"])
    return value


def _write_json(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _json_payload(value)
    if exclusive:
        try:
            with path.open("x", encoding="utf-8") as handle:
                handle.write(payload)
        except FileExistsError as exc:
            raise DriverBlocked([f"output already exists: {path}"]) from exc
        return
    path.write_text(payload, encoding="utf-8")


def _json_payload(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _load_jsonl_handle(handle: Any, source: Path) -> list[dict[str, Any]]:
    handle.seek(0)
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(handle.read().splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise DriverBlocked(
                [f"{source}:{line_number}: invalid JSON: {exc}"]
            ) from exc
        if not isinstance(value, dict):
            raise DriverBlocked(
                [f"{source}:{line_number}: record must be an object"]
            )
        records.append(value)
    return records


def _causal_blockers(receipt: dict[str, Any]) -> list[str]:
    return [
        f"{error['code']}@{error['sequence']}: {error['message']}"
        for error in receipt.get("errors", [])
    ]


def append_causal_records(
    stream: Path, records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Append one validated causal batch under an exclusive stream lock."""

    if not records:
        raise DriverBlocked(["causal append requires at least one record"])
    stream.parent.mkdir(parents=True, exist_ok=True)
    with stream.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            existing = _load_jsonl_handle(handle, stream)
            prepared: list[dict[str, Any]] = []
            for ordinal, record in enumerate(records, start=1):
                if not isinstance(record, dict):
                    raise DriverBlocked(
                        [f"causal record[{ordinal}] must be an object"]
                    )
                owned = sorted({"schema_version", "sequence"} & set(record))
                if owned:
                    raise DriverBlocked(
                        [
                            "causal writer owns metadata fields: "
                            + ", ".join(owned)
                        ]
                    )
                prepared.append(
                    {
                        "schema_version": RUN_EVENT_SCHEMA_VERSION,
                        "sequence": len(existing) + ordinal,
                        **record,
                    }
                )

            prospective = existing + prepared
            receipt = evidence.validate_events(
                prospective, str(stream), require_complete=False
            )
            if not receipt["valid"]:
                raise DriverBlocked(_causal_blockers(receipt))

            handle.seek(0, os.SEEK_END)
            for event in prepared:
                handle.write(
                    json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
                )
            handle.flush()
            os.fsync(handle.fileno())
            return prepared
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _residue_shape_blockers(record: dict[str, Any], index: int) -> list[str]:
    prefix = f"residue[{index}]"
    required = RESIDUE_REQUIRED_FIELDS | {"schema_version", "sequence"}
    blockers = [
        f"{prefix}: missing required field '{field}'"
        for field in sorted(required - set(record))
    ]
    blockers.extend(
        f"{prefix}: unexpected field '{field}'"
        for field in sorted(set(record) - required)
    )
    if record.get("schema_version") != RESIDUE_SCHEMA_VERSION:
        blockers.append(f"{prefix}: unsupported schema_version")
    if (
        not isinstance(record.get("sequence"), int)
        or isinstance(record.get("sequence"), bool)
        or record["sequence"] < 1
    ):
        blockers.append(f"{prefix}: sequence must be a positive integer")
    for field in ("recorded_at", "dispatch_id", "run_id", "summary"):
        if not isinstance(record.get(field), str) or not record[field]:
            blockers.append(f"{prefix}: {field} must be a non-empty string")
    if record.get("kind") not in RESIDUE_KINDS:
        blockers.append(f"{prefix}: unsupported kind '{record.get('kind')}'")
    for field in ("wave_id", "action_id", "agent_id"):
        if record.get(field) is not None and (
            not isinstance(record[field], str) or not record[field]
        ):
            blockers.append(f"{prefix}: {field} must be null or a non-empty string")
    source_refs = record.get("source_refs")
    if not isinstance(source_refs, list) or any(
        not isinstance(item, str) or not item for item in source_refs
    ):
        blockers.append(f"{prefix}: source_refs must be an array of strings")
    return blockers


def append_residue_record(stream: Path, record: dict[str, Any]) -> dict[str, Any]:
    """Append one non-causal record to a separately owned residue stream."""

    owned = sorted({"schema_version", "sequence"} & set(record))
    if owned:
        raise DriverBlocked(
            ["residue writer owns metadata fields: " + ", ".join(owned)]
        )
    stream.parent.mkdir(parents=True, exist_ok=True)
    with stream.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            existing = _load_jsonl_handle(handle, stream)
            blockers: list[str] = []
            dispatch_id: str | None = None
            run_id: str | None = None
            for index, existing_record in enumerate(existing):
                blockers.extend(_residue_shape_blockers(existing_record, index))
                if existing_record.get("sequence") != index + 1:
                    blockers.append(
                        f"residue[{index}]: expected sequence {index + 1}"
                    )
                if dispatch_id is None:
                    dispatch_id = existing_record.get("dispatch_id")
                    run_id = existing_record.get("run_id")
                elif (
                    existing_record.get("dispatch_id") != dispatch_id
                    or existing_record.get("run_id") != run_id
                ):
                    blockers.append(f"residue[{index}]: run identity mismatch")

            prepared = {
                "schema_version": RESIDUE_SCHEMA_VERSION,
                "sequence": len(existing) + 1,
                **record,
            }
            blockers.extend(_residue_shape_blockers(prepared, len(existing)))
            if existing and (
                prepared.get("dispatch_id") != dispatch_id
                or prepared.get("run_id") != run_id
            ):
                blockers.append("residue append run identity mismatch")
            if blockers:
                raise DriverBlocked(blockers)

            handle.seek(0, os.SEEK_END)
            handle.write(
                json.dumps(prepared, sort_keys=True, separators=(",", ":")) + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
            return prepared
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _admit_persisted_action(
    action_path: Path, run_plan_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    action = _load_json_object(action_path, "persisted action")
    run_plan = _load_json_object(run_plan_path, "run plan")
    actions = run_plan.get("actions")
    action_id = action.get("action_id")
    if not isinstance(actions, list) or not isinstance(action_id, str):
        raise DriverBlocked(["run plan or persisted action has no usable actions"])
    matches = [candidate for candidate in actions if candidate.get("action_id") == action_id]
    if len(matches) != 1 or matches[0] != action:
        raise DriverBlocked(
            ["persisted action does not exactly match one current run-plan action"]
        )
    expected_artifact = f"actions/{action_id}.json"
    if expected_artifact not in (run_plan.get("action_artifacts") or []):
        raise DriverBlocked([f"run plan does not bind {expected_artifact}"])
    return action, run_plan


def _compact(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def _spawn_request(action: dict[str, Any]) -> dict[str, Any]:
    action_stem = action["action_id"].replace("-", "_")
    run_scope = hashlib.sha256(
        f"{action['dispatch_id']}\0{action['run_id']}".encode("utf-8")
    ).hexdigest()
    lines = [
        "Execute one bounded host-native action.",
        f"Action: {action['action_id']}",
        f"Role: {action['role']}",
        f"Capability: {action['capability_ref']}",
        f"Target: {action['target']}",
        f"Mode: {action['mode']}",
        f"Mutation policy: {action['mutation_policy']}",
        f"Write scope: {_compact(action['write_scope'])}",
        f"Forbidden write scopes: {_compact(action['forbidden_write_scopes'])}",
        f"Input refs: {_compact(action['input_refs'])}",
        f"Output refs: {_compact(action['output_refs'])}",
        "Return one bounded receipt for the persisted action. Do not widen scope.",
    ]
    return {
        "action_id": action["action_id"],
        "operation": "collaboration.spawn_agent",
        "task_name": f"orchestrate_{run_scope}_{action_stem}",
        "fork_turns": "none",
        "message": "\n".join(lines),
    }


def prepare_spawn(
    action_path: Path,
    run_plan_path: Path,
    event_stream: Path,
    request_output: Path,
    depends_on_gate_id: str | None,
) -> dict[str, Any]:
    action, run_plan = _admit_persisted_action(action_path, run_plan_path)
    events = _validated_prefix(event_stream) if event_stream.exists() else []
    selected_wave = run_plan.get("selected_wave")
    dependencies = (
        selected_wave.get("depends_on_waves", [])
        if isinstance(selected_wave, dict)
        else []
    )
    if dependencies:
        if not isinstance(depends_on_gate_id, str) or not depends_on_gate_id:
            raise DriverBlocked(
                ["dependent-wave spawn requires a non-empty passed gate identifier"]
            )
        matching_gates = [
            event
            for event in events
            if event.get("event") == "gate_decided"
            and event.get("gate_id") == depends_on_gate_id
            and event.get("decision") == "gate_pass"
            and event.get("wave_id") in dependencies
        ]
        if len(matching_gates) != 1:
            raise DriverBlocked(
                ["dependent-wave spawn gate does not match one passed dependency gate"]
            )
    if any(
        event.get("event") == "host_spawn_failed"
        and event.get("dispatch_id") == action["dispatch_id"]
        and event.get("run_id") == action["run_id"]
        and event.get("wave_id") == action["wave_id"]
        for event in events
    ):
        raise DriverBlocked(
            ["selected wave has a host_spawn_failed event; no later spawn is permitted"]
        )
    append_causal_records(
        event_stream,
        [
            {
                "event": "action_attempted",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": None,
                "operation": "collaboration.spawn_agent",
                "depends_on_gate_id": depends_on_gate_id,
            }
        ],
    )
    request = _spawn_request(action)
    _write_json(request_output, request, exclusive=True)
    return request


def record_spawn(
    action_path: Path,
    run_plan_path: Path,
    event_stream: Path,
    agent_id: str | None,
) -> dict[str, Any]:
    action, _ = _admit_persisted_action(action_path, run_plan_path)
    if agent_id is not None and not agent_id:
        raise DriverBlocked(["agent_id must be non-empty when spawn succeeds"])
    kind = "host_spawn_returned" if agent_id is not None else "host_spawn_failed"
    return append_causal_records(
        event_stream,
        [
            {
                "event": kind,
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": agent_id,
                "operation": "collaboration.spawn_agent",
            }
        ],
    )[0]


def _validated_prefix(path: Path) -> list[dict[str, Any]]:
    try:
        events = evidence.load_events(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise DriverBlocked([f"cannot load causal event stream: {exc}"]) from exc
    receipt = evidence.validate_events(events, str(path), require_complete=False)
    if not receipt["valid"]:
        raise DriverBlocked(_causal_blockers(receipt))
    return events


def _load_exact_action_directory(
    actions_dir: Path, action_set: dict[str, Any]
) -> list[dict[str, Any]]:
    """Admit only canonical action files that exactly equal the action set."""

    actions = action_set.get("actions")
    if not isinstance(actions, list) or not actions:
        raise DriverBlocked(["next action set has no actions"])
    expected_by_name: dict[str, dict[str, Any]] = {}
    for action in actions:
        if not isinstance(action, dict):
            raise DriverBlocked(["next action set contains a non-object action"])
        action_id = action.get("action_id")
        if not isinstance(action_id, str) or not action_id:
            raise DriverBlocked(["next action set contains an invalid action_id"])
        filename = f"{action_id}.json"
        if filename in expected_by_name:
            raise DriverBlocked([f"duplicate next action identifier: {action_id}"])
        expected_by_name[filename] = action

    if not actions_dir.is_dir():
        raise DriverBlocked([f"action directory does not exist: {actions_dir}"])
    actual_entries = {path.name: path for path in actions_dir.iterdir()}
    unexpected = sorted(set(actual_entries) - set(expected_by_name))
    missing = sorted(set(expected_by_name) - set(actual_entries))
    blockers = [f"unexpected action entry '{name}'" for name in unexpected]
    blockers.extend(f"missing action entry '{name}'" for name in missing)
    for name in sorted(set(actual_entries) & set(expected_by_name)):
        path = actual_entries[name]
        if not path.is_file() or path.is_symlink():
            blockers.append(f"action entry is not a regular file: {name}")
            continue
        try:
            actual_bytes = path.read_bytes()
        except OSError as exc:
            blockers.append(f"cannot read persisted action {name}: {exc}")
            continue
        expected_bytes = _json_payload(expected_by_name[name]).encode("utf-8")
        if actual_bytes != expected_bytes:
            blockers.append(
                f"persisted action bytes do not exactly match next action set: {name}"
            )
    if blockers:
        raise DriverBlocked(blockers)
    return [expected_by_name[f"{action['action_id']}.json"] for action in actions]


def _validate_next_wave_event_prefix(
    events: list[dict[str, Any]],
    gate_decision: dict[str, Any],
    run_plan: dict[str, Any],
) -> None:
    if not events:
        raise DriverBlocked(["next-wave planning requires a causal event prefix"])
    if any(event.get("event") == "run_blocked" for event in events):
        raise DriverBlocked(["terminally blocked runs cannot emit a next-wave plan"])
    action_ids = {str(action["action_id"]) for action in run_plan["actions"]}
    replayed = sorted(
        {
            str(event.get("action_id"))
            for event in events
            if event.get("event") == "action_attempted"
            and event.get("action_id") in action_ids
        }
    )
    if replayed:
        raise DriverBlocked(
            ["next-wave actions already have attempt evidence: " + ", ".join(replayed)]
        )

    last = events[-1]
    expected = {
        "event": "gate_decided",
        "dispatch_id": gate_decision["dispatch_id"],
        "run_id": gate_decision["run_id"],
        "wave_id": gate_decision["wave_id"],
        "action_id": None,
        "agent_id": None,
        "operation": "orchestrate.reduce",
        "gate_id": gate_decision["gate_id"],
        "decision": gate_decision["decision"],
        "required_action_ids": gate_decision["required_action_ids"],
        "admitted_receipt_action_ids": gate_decision[
            "admitted_receipt_action_ids"
        ],
    }
    mismatches = sorted(
        field for field, expected_value in expected.items() if last.get(field) != expected_value
    )
    if mismatches:
        raise DriverBlocked(
            ["last causal event does not match the source gate decision: " + ", ".join(mismatches)]
        )


def prepare_next_wave_plan(
    dispatch_path: Path,
    prior_run_plan_path: Path,
    gate_decision_path: Path,
    action_set_path: Path,
    next_state_path: Path,
    event_stream: Path,
    actions_dir: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Exclusively emit a dependent plan without writing a causal event."""

    if output_path.exists():
        raise DriverBlocked([f"output already exists: {output_path}"])
    dispatch = _load_json_object(dispatch_path, "dispatch")
    prior_run_plan = _load_json_object(prior_run_plan_path, "prior run plan")
    gate_decision = _load_json_object(gate_decision_path, "gate decision")
    action_set = _load_json_object(action_set_path, "next action set")
    next_state = _load_json_object(next_state_path, "next state")
    persisted_actions = _load_exact_action_directory(actions_dir, action_set)

    try:
        with event_stream.open("r", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                events = _load_jsonl_handle(handle, event_stream)
                validation = evidence.validate_events(
                    events, str(event_stream), require_complete=True
                )
                if not validation["valid"]:
                    raise DriverBlocked(_causal_blockers(validation))
                try:
                    run_plan = coordinator.build_next_wave_plan(
                        dispatch,
                        prior_run_plan,
                        gate_decision,
                        action_set,
                        next_state,
                        persisted_actions,
                    )
                except coordinator.CompileBlocked as exc:
                    raise DriverBlocked(exc.blockers) from exc
                _validate_next_wave_event_prefix(events, gate_decision, run_plan)
                _write_json(output_path, run_plan, exclusive=True)
                return run_plan
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError as exc:
        raise DriverBlocked([f"cannot load causal event stream: {exc}"]) from exc


def prepare_wait(
    run_plan_path: Path, event_stream: Path, request_output: Path
) -> dict[str, Any]:
    if request_output.exists():
        raise DriverBlocked([f"output already exists: {request_output}"])
    run_plan = _load_json_object(run_plan_path, "run plan")
    actions = run_plan.get("actions")
    if not isinstance(actions, list) or not actions:
        raise DriverBlocked(["run plan has no actions to wait for"])
    events = _validated_prefix(event_stream)
    successful_results: dict[str, dict[str, Any]] = {}
    registrations: dict[str, dict[str, Any]] = {}
    terminal_action_ids: set[str] = set()
    for event in events:
        if event.get("event") == "host_spawn_returned":
            successful_results[str(event["action_id"])] = event
        elif event.get("event") == "agent_wait_registered":
            registrations[str(event["action_id"])] = event
        elif event.get("event") in {
            "agent_terminal",
            "wait_timed_out",
            "agent_interrupted",
        }:
            terminal_action_ids.add(str(event["action_id"]))

    records: list[dict[str, Any]] = []
    bound_agent_ids: list[str] = []
    pending_agent_ids: list[str] = []
    for action in actions:
        action_id = str(action.get("action_id", ""))
        host_result = successful_results.get(action_id)
        if host_result is None:
            raise DriverBlocked(
                [f"action '{action_id}' has no successful host result"]
            )
        if host_result.get("wave_id") != action.get("wave_id"):
            raise DriverBlocked([f"action '{action_id}' host result wave mismatch"])
        agent_id = str(host_result.get("agent_id", ""))
        if not agent_id:
            raise DriverBlocked([f"action '{action_id}' has no native agent binding"])
        bound_agent_ids.append(agent_id)
        registration = registrations.get(action_id)
        if registration is None:
            records.append(
                {
                    "event": "agent_wait_registered",
                    "dispatch_id": action["dispatch_id"],
                    "run_id": action["run_id"],
                    "wave_id": action["wave_id"],
                    "action_id": action_id,
                    "agent_id": agent_id,
                    "operation": "logical-register",
                }
            )
        elif (
            registration.get("agent_id") != agent_id
            or registration.get("wave_id") != action.get("wave_id")
        ):
            raise DriverBlocked([f"action '{action_id}' wait registration mismatch"])
        if action_id not in terminal_action_ids:
            pending_agent_ids.append(agent_id)
    if len(set(bound_agent_ids)) != len(bound_agent_ids):
        raise DriverBlocked(["native agent bindings must be unique within a wave"])
    if not pending_agent_ids:
        raise DriverBlocked(["selected wave has no unresolved native agents"])
    selected_wave = run_plan.get("selected_wave") or {}
    records.append(
        {
            "event": "wait_attempted",
            "dispatch_id": run_plan["dispatch_id"],
            "run_id": run_plan["run_id"],
            "wave_id": selected_wave.get("wave_id"),
            "action_id": None,
            "agent_id": None,
            "operation": "collaboration.wait_agent",
        }
    )
    append_causal_records(event_stream, records)
    request = {
        "operation": "collaboration.wait_agent",
        "wave_id": selected_wave.get("wave_id"),
        "pending_agent_ids": pending_agent_ids,
        "targeting": "mailbox-wide",
    }
    _write_json(request_output, request, exclusive=True)
    return request


def _partial_wave_context(
    run_plan_path: Path, event_stream: Path
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Return current-wave success/failure bindings for a failed spawn prefix.

    A failed spawn does not become an action receipt.  This helper is only for
    cleaning up the already-created sibling agents before a terminal blocked
    closeout.
    """

    run_plan = _load_json_object(run_plan_path, "run plan")
    actions = run_plan.get("actions")
    selected_wave = run_plan.get("selected_wave")
    if not isinstance(actions, list) or not actions or not isinstance(selected_wave, dict):
        raise DriverBlocked(["run plan must contain one selected wave and actions"])
    wave_id = selected_wave.get("wave_id")
    if not isinstance(wave_id, str) or not wave_id:
        raise DriverBlocked(["selected wave must have a non-empty wave_id"])
    events = _validated_prefix(event_stream)
    host_results = {
        str(event["action_id"]): event
        for event in events
        if event.get("event") in {"host_spawn_returned", "host_spawn_failed"}
    }
    successful: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    unattempted: list[str] = []
    for action in actions:
        action_id = action.get("action_id")
        if not isinstance(action_id, str) or not action_id:
            raise DriverBlocked(["run plan action identifiers must be non-empty strings"])
        if action.get("wave_id") != wave_id:
            raise DriverBlocked([f"action '{action_id}' is outside the selected wave"])
        result = host_results.get(action_id)
        if result is None:
            unattempted.append(action_id)
            continue
        if result.get("wave_id") != wave_id:
            raise DriverBlocked([f"action '{action_id}' host result wave mismatch"])
        if result.get("event") == "host_spawn_returned":
            agent_id = result.get("agent_id")
            if not isinstance(agent_id, str) or not agent_id:
                raise DriverBlocked([f"action '{action_id}' has no native agent binding"])
            successful.append({"action": action, "event": result})
        else:
            failed.append({"action": action, "event": result})
    if not failed:
        raise DriverBlocked(["partial-wave recovery requires at least one host_spawn_failed action"])
    return run_plan, successful, failed, events, unattempted


def _validated_residue(path: Path, dispatch_id: str, run_id: str) -> list[dict[str, Any]]:
    if not path.is_file():
        raise DriverBlocked([f"residue stream does not exist: {path}"])
    try:
        with path.open("r", encoding="utf-8") as handle:
            records = _load_jsonl_handle(handle, path)
    except OSError as exc:
        raise DriverBlocked([f"cannot load residue stream: {exc}"]) from exc
    blockers: list[str] = []
    for index, record in enumerate(records):
        blockers.extend(_residue_shape_blockers(record, index))
        if record.get("sequence") != index + 1:
            blockers.append(f"residue[{index}]: expected sequence {index + 1}")
        if record.get("dispatch_id") != dispatch_id or record.get("run_id") != run_id:
            blockers.append(f"residue[{index}]: run identity mismatch")
    if blockers:
        raise DriverBlocked(blockers)
    return records


def _partial_success_binding(
    action_path: Path, run_plan_path: Path, event_stream: Path, agent_id: str
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    action, run_plan = _admit_persisted_action(action_path, run_plan_path)
    _, successful, _, events, _ = _partial_wave_context(run_plan_path, event_stream)
    binding = next(
        (item for item in successful if item["action"].get("action_id") == action.get("action_id")),
        None,
    )
    if binding is None:
        raise DriverBlocked([f"action '{action['action_id']}' is not a successfully spawned partial-wave sibling"])
    if binding["event"].get("agent_id") != agent_id:
        raise DriverBlocked([f"action '{action['action_id']}' agent binding mismatch"])
    registrations = [
        event
        for event in events
        if event.get("event") == "agent_wait_registered"
        and event.get("action_id") == action["action_id"]
    ]
    waits = [
        event
        for event in events
        if event.get("event") == "wait_attempted"
        and event.get("wave_id") == action["wave_id"]
    ]
    if len(registrations) != 1 or not any(
        wait["sequence"] > registrations[0]["sequence"] for wait in waits
    ):
        raise DriverBlocked([f"action '{action['action_id']}' has no prepared partial-wave wait"])
    return action, run_plan, events


def prepare_partial_recovery(
    run_plan_path: Path, event_stream: Path, request_output: Path
) -> dict[str, Any]:
    """Prepare a mailbox wait for only siblings that actually spawned."""

    run_plan, successful, _, events, _ = _partial_wave_context(run_plan_path, event_stream)
    if not successful:
        raise DriverBlocked(["partial-wave recovery has no successfully spawned sibling to wait for"])
    selected_wave = run_plan["selected_wave"]
    wave_id = selected_wave["wave_id"]
    if any(
        event.get("wave_id") == wave_id
        and event.get("event") in {"agent_wait_registered", "wait_attempted"}
        for event in events
    ):
        raise DriverBlocked(["partial-wave recovery wait has already been prepared"])
    pending_agent_ids = [str(item["event"]["agent_id"]) for item in successful]
    if len(set(pending_agent_ids)) != len(pending_agent_ids):
        raise DriverBlocked(["native agent bindings must be unique within a wave"])
    records = [
        {
            "event": "agent_wait_registered",
            "dispatch_id": item["action"]["dispatch_id"],
            "run_id": item["action"]["run_id"],
            "wave_id": item["action"]["wave_id"],
            "action_id": item["action"]["action_id"],
            "agent_id": item["event"]["agent_id"],
            "operation": "logical-register",
        }
        for item in successful
    ]
    records.append(
        {
            "event": "wait_attempted",
            "dispatch_id": run_plan["dispatch_id"],
            "run_id": run_plan["run_id"],
            "wave_id": wave_id,
            "action_id": None,
            "agent_id": None,
            "operation": "collaboration.wait_agent",
        }
    )
    append_causal_records(event_stream, records)
    request = {
        "operation": "collaboration.wait_agent",
        "wave_id": wave_id,
        "pending_agent_ids": pending_agent_ids,
        "targeting": "mailbox-wide",
        "recovery_kind": "partial_wave",
    }
    _write_json(request_output, request, exclusive=True)
    return request


def record_partial_terminal(
    action_path: Path, run_plan_path: Path, event_stream: Path, agent_id: str
) -> list[dict[str, Any]]:
    """Record a completed known sibling after the prepared recovery wait."""

    action, _, events = _partial_success_binding(
        action_path, run_plan_path, event_stream, agent_id
    )
    if any(
        event.get("action_id") == action["action_id"]
        and event.get("event")
        in {"agent_terminal", "agent_closed", "wait_timed_out", "agent_interrupted"}
        for event in events
    ):
        raise DriverBlocked([f"action '{action['action_id']}' already has terminal cleanup evidence"])
    return append_causal_records(
        event_stream,
        [
            {
                "event": "agent_terminal",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": agent_id,
                "operation": "collaboration.list_agents",
            },
            {
                "event": "agent_closed",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": agent_id,
                "operation": "logical-close",
            },
        ],
    )


def prepare_partial_interrupt(
    action_path: Path,
    run_plan_path: Path,
    event_stream: Path,
    agent_id: str,
    request_output: Path,
) -> dict[str, Any]:
    """Record timeout before exposing the one allowed recovery interrupt."""

    action, _, events = _partial_success_binding(
        action_path, run_plan_path, event_stream, agent_id
    )
    if any(
        event.get("action_id") == action["action_id"]
        and event.get("event")
        in {"agent_terminal", "agent_closed", "wait_timed_out", "agent_interrupted"}
        for event in events
    ):
        raise DriverBlocked([f"action '{action['action_id']}' already has terminal cleanup evidence"])
    append_causal_records(
        event_stream,
        [
            {
                "event": "wait_timed_out",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": agent_id,
                "operation": "collaboration.wait_agent",
            }
        ],
    )
    request = {
        "operation": "collaboration.interrupt_agent",
        "action_id": action["action_id"],
        "agent_id": agent_id,
        "recovery_kind": "partial_wave",
    }
    _write_json(request_output, request, exclusive=True)
    return request


def record_partial_interrupt(
    action_path: Path, run_plan_path: Path, event_stream: Path, agent_id: str
) -> dict[str, Any]:
    """Record the outcome of the exact interrupt request prepared above."""

    action, _, events = _partial_success_binding(
        action_path, run_plan_path, event_stream, agent_id
    )
    timeout = [
        event
        for event in events
        if event.get("event") == "wait_timed_out"
        and event.get("action_id") == action["action_id"]
    ]
    if len(timeout) != 1:
        raise DriverBlocked([f"action '{action['action_id']}' has no prepared interrupt timeout"])
    if any(
        event.get("event") == "agent_interrupted"
        and event.get("action_id") == action["action_id"]
        for event in events
    ):
        raise DriverBlocked([f"action '{action['action_id']}' interrupt is already recorded"])
    return append_causal_records(
        event_stream,
        [
            {
                "event": "agent_interrupted",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": agent_id,
                "operation": "collaboration.interrupt_agent",
            }
        ],
    )[0]


def close_partial_wave(
    run_plan_path: Path,
    state_path: Path,
    event_stream: Path,
    residue_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Close a failed spawn wave after every known sibling has been cleaned."""

    run_plan, successful, failed, events, unattempted = _partial_wave_context(
        run_plan_path, event_stream
    )
    if any(event.get("event") == "run_blocked" for event in events):
        raise DriverBlocked(["partial wave already has a blocked closeout"])
    residue = _validated_residue(
        residue_path, run_plan["dispatch_id"], run_plan["run_id"]
    )
    cleaned_action_ids: list[str] = []
    for item in successful:
        action_id = item["action"]["action_id"]
        has_closed = any(
            event.get("event") == "agent_closed" and event.get("action_id") == action_id
            for event in events
        )
        has_interrupted = any(
            event.get("event") == "agent_interrupted" and event.get("action_id") == action_id
            for event in events
        )
        if not has_closed and not has_interrupted:
            raise DriverBlocked([f"action '{action_id}' has not completed partial-wave cleanup"])
        if not any(
            record.get("kind") == "evidence_closure"
            and record.get("action_id") == action_id
            and record.get("agent_id") == item["event"]["agent_id"]
            for record in residue
        ):
            raise DriverBlocked([f"action '{action_id}' has no matching cleanup residue"])
        cleaned_action_ids.append(action_id)
    failed_action_ids = [item["action"]["action_id"] for item in failed]
    closing_record = {
        "event": "run_blocked",
        "dispatch_id": run_plan["dispatch_id"],
        "run_id": run_plan["run_id"],
        "wave_id": run_plan["selected_wave"]["wave_id"],
        "action_id": failed_action_ids[0],
        "agent_id": None,
        "operation": "logical-close",
        "failed_action_ids": failed_action_ids,
        "cleaned_action_ids": cleaned_action_ids,
        "blocker_code": "partial_wave_spawn_failure",
    }
    prospective = events + [
        {
            "schema_version": RUN_EVENT_SCHEMA_VERSION,
            "sequence": len(events) + 1,
            **closing_record,
        }
    ]
    validation = evidence.validate_events(
        prospective, str(event_stream), require_complete=True
    )
    if not validation["valid"]:
        raise DriverBlocked(_causal_blockers(validation))
    state = _load_json_object(state_path, "run state")
    if state.get("dispatch_id") != run_plan["dispatch_id"] or state.get("run_id") != run_plan["run_id"]:
        raise DriverBlocked(["run state identity does not match run plan"])
    if output_path.exists():
        raise DriverBlocked([f"output already exists: {output_path}"])
    append_causal_records(event_stream, [closing_record])
    closeout = {
        "schema_version": "arcanum.native-dispatch-runner.partial-wave-closeout.v0.1",
        "status": "block",
        "state": "blocked",
        "dispatch_id": run_plan["dispatch_id"],
        "run_id": run_plan["run_id"],
        "wave_id": run_plan["selected_wave"]["wave_id"],
        "failed_action_ids": failed_action_ids,
        "cleaned_action_ids": cleaned_action_ids,
        "unattempted_action_ids": unattempted,
        "dependent_action_ids": [],
        "blockers": [f"partial_wave_spawn_failure:{action_id}" for action_id in failed_action_ids],
        "event_validation_status": validation["status"],
    }
    _write_json(output_path, closeout, exclusive=True)
    return closeout


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def admit_receipt_directory(
    run_plan: dict[str, Any], receipts_dir: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    actions = run_plan.get("actions")
    selected_wave = run_plan.get("selected_wave")
    if not isinstance(actions, list) or not actions or not isinstance(selected_wave, dict):
        raise DriverBlocked(["run plan must contain one selected wave and actions"])
    expected_by_id = {str(action.get("action_id")): action for action in actions}
    if "" in expected_by_id or len(expected_by_id) != len(actions):
        raise DriverBlocked(["run plan action identifiers must be non-empty and unique"])
    expected_files = {f"{action_id}.json" for action_id in expected_by_id}
    blockers: list[str] = []
    actual_files: dict[str, Path] = {}
    if not receipts_dir.is_dir():
        blockers.append(f"receipt directory does not exist: {receipts_dir}")
    else:
        for path in sorted(receipts_dir.iterdir()):
            if not path.is_file() or path.name not in expected_files:
                blockers.append(f"unexpected receipt entry '{path.name}'")
                continue
            actual_files[path.name] = path
    for expected_file in sorted(expected_files - set(actual_files)):
        blockers.append(f"missing receipt entry '{expected_file}'")

    admitted: list[dict[str, Any]] = []
    file_rows: list[dict[str, Any]] = []
    identity_fields = (
        "dispatch_id",
        "run_id",
        "wave_id",
        "step_id",
        "role",
        "capability_ref",
    )
    for action_id, action in expected_by_id.items():
        path = actual_files.get(f"{action_id}.json")
        if path is None:
            continue
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            blockers.append(f"{path.name}: invalid receipt JSON: {exc}")
            continue
        shape_blockers = coordinator._receipt_shape_blockers(receipt, len(file_rows))
        blockers.extend(f"{path.name}: {item}" for item in shape_blockers)
        if shape_blockers or not isinstance(receipt, dict):
            continue
        if receipt.get("action_id") != action_id:
            blockers.append(
                f"{path.name}: receipt action_id '{receipt.get('action_id')}' does not match '{action_id}'"
            )
            continue
        identity_mismatches = [
            field for field in identity_fields if receipt.get(field) != action.get(field)
        ]
        if identity_mismatches:
            blockers.append(
                f"{path.name}: receipt identity mismatch: "
                + ", ".join(identity_mismatches)
            )
            continue
        admitted.append(receipt)
        file_rows.append(
            {
                "action_id": action_id,
                "path": str(path),
                "sha256": _sha256(path),
                "receipt_status": receipt["status"],
            }
        )

    status = "pass" if not blockers and len(admitted) == len(actions) else "block"
    admission = {
        "schema_version": RECEIPT_ADMISSION_SCHEMA_VERSION,
        "dispatch_id": run_plan.get("dispatch_id"),
        "run_id": run_plan.get("run_id"),
        "wave_id": selected_wave.get("wave_id"),
        "status": status,
        "expected_action_ids": list(expected_by_id),
        "admitted_receipt_action_ids": [item["action_id"] for item in admitted],
        "receipt_files": file_rows,
        "blockers": sorted(set(blockers)),
    }
    return admitted, admission


def advance_wave(
    dispatch_path: Path,
    state_path: Path,
    run_plan_path: Path,
    receipts_dir: Path,
    event_stream: Path,
    output_dir: Path,
) -> dict[str, Any]:
    coordinator._prepare_output_directory(output_dir)
    dispatch = _load_json_object(dispatch_path, "dispatch")
    state = _load_json_object(state_path, "state")
    run_plan = _load_json_object(run_plan_path, "run plan")
    receipts, admission = admit_receipt_directory(run_plan, receipts_dir)
    _write_json(output_dir / "receipt-admission.json", admission)
    if admission["status"] != "pass":
        raise DriverBlocked(admission["blockers"])

    next_state, gate, action_set = coordinator.reduce_wave_receipts(
        dispatch, state, run_plan, receipts
    )
    join_events = [
        {
            "event": "receipt_joined",
            "dispatch_id": receipt["dispatch_id"],
            "run_id": receipt["run_id"],
            "wave_id": receipt["wave_id"],
            "action_id": receipt["action_id"],
            "agent_id": receipt["agent_id"],
            "operation": "orchestrate.join",
            "receipt_status": receipt["status"],
        }
        for receipt in receipts
    ]
    gate_id = gate.get("gate_id")
    if gate_id is not None:
        join_events.append(
            {
                "event": "gate_decided",
                "dispatch_id": gate["dispatch_id"],
                "run_id": gate["run_id"],
                "wave_id": gate["wave_id"],
                "action_id": None,
                "agent_id": None,
                "operation": "orchestrate.reduce",
                "gate_id": gate_id,
                "decision": gate["decision"],
                "required_action_ids": gate["required_action_ids"],
                "admitted_receipt_action_ids": gate[
                    "admitted_receipt_action_ids"
                ],
            }
        )
    append_causal_records(event_stream, join_events)

    validation = evidence.validate_events(
        evidence.load_events(event_stream), str(event_stream)
    )
    _write_json(output_dir / "event-validation.json", validation)
    if not validation["valid"]:
        raise DriverBlocked(_causal_blockers(validation))

    _write_json(output_dir / "state.json", next_state)
    _write_json(output_dir / "gate-decision.json", gate)
    _write_json(output_dir / "next-actions.json", action_set)
    for action in action_set["actions"]:
        _write_json(output_dir / "actions" / f"{action['action_id']}.json", action)
    return {
        "status": "pass",
        "state": next_state,
        "gate_decision": gate,
        "action_set": action_set,
        "receipt_admission": admission,
        "event_validation": validation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare, record, and advance native dispatch evidence."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    append_parser = subparsers.add_parser("append-event")
    append_parser.add_argument("--events", required=True, type=Path)
    append_parser.add_argument("--record", required=True, type=Path)

    prepare_spawn_parser = subparsers.add_parser("prepare-spawn")
    prepare_spawn_parser.add_argument("--action", required=True, type=Path)
    prepare_spawn_parser.add_argument("--run-plan", required=True, type=Path)
    prepare_spawn_parser.add_argument("--events", required=True, type=Path)
    prepare_spawn_parser.add_argument("--output", required=True, type=Path)
    prepare_spawn_parser.add_argument("--depends-on-gate-id")

    record_spawn_parser = subparsers.add_parser("record-spawn")
    record_spawn_parser.add_argument("--action", required=True, type=Path)
    record_spawn_parser.add_argument("--run-plan", required=True, type=Path)
    record_spawn_parser.add_argument("--events", required=True, type=Path)
    spawn_result = record_spawn_parser.add_mutually_exclusive_group(required=True)
    spawn_result.add_argument("--agent-id")
    spawn_result.add_argument("--failed", action="store_true")

    next_plan_parser = subparsers.add_parser("prepare-next-wave-plan")
    next_plan_parser.add_argument("dispatch", type=Path)
    next_plan_parser.add_argument("--prior-run-plan", required=True, type=Path)
    next_plan_parser.add_argument("--gate-decision", required=True, type=Path)
    next_plan_parser.add_argument("--next-actions", required=True, type=Path)
    next_plan_parser.add_argument("--next-state", required=True, type=Path)
    next_plan_parser.add_argument("--events", required=True, type=Path)
    next_plan_parser.add_argument("--actions-dir", required=True, type=Path)
    next_plan_parser.add_argument("--output", required=True, type=Path)

    prepare_wait_parser = subparsers.add_parser("prepare-wait")
    prepare_wait_parser.add_argument("--run-plan", required=True, type=Path)
    prepare_wait_parser.add_argument("--events", required=True, type=Path)
    prepare_wait_parser.add_argument("--output", required=True, type=Path)

    partial_recovery_parser = subparsers.add_parser("prepare-partial-recovery")
    partial_recovery_parser.add_argument("--run-plan", required=True, type=Path)
    partial_recovery_parser.add_argument("--events", required=True, type=Path)
    partial_recovery_parser.add_argument("--output", required=True, type=Path)

    partial_terminal_parser = subparsers.add_parser("record-partial-terminal")
    partial_terminal_parser.add_argument("--action", required=True, type=Path)
    partial_terminal_parser.add_argument("--run-plan", required=True, type=Path)
    partial_terminal_parser.add_argument("--events", required=True, type=Path)
    partial_terminal_parser.add_argument("--agent-id", required=True)

    partial_interrupt_prepare_parser = subparsers.add_parser(
        "prepare-partial-interrupt"
    )
    partial_interrupt_prepare_parser.add_argument("--action", required=True, type=Path)
    partial_interrupt_prepare_parser.add_argument("--run-plan", required=True, type=Path)
    partial_interrupt_prepare_parser.add_argument("--events", required=True, type=Path)
    partial_interrupt_prepare_parser.add_argument("--agent-id", required=True)
    partial_interrupt_prepare_parser.add_argument("--output", required=True, type=Path)

    partial_interrupt_record_parser = subparsers.add_parser(
        "record-partial-interrupt"
    )
    partial_interrupt_record_parser.add_argument("--action", required=True, type=Path)
    partial_interrupt_record_parser.add_argument("--run-plan", required=True, type=Path)
    partial_interrupt_record_parser.add_argument("--events", required=True, type=Path)
    partial_interrupt_record_parser.add_argument("--agent-id", required=True)

    partial_close_parser = subparsers.add_parser("close-partial-wave")
    partial_close_parser.add_argument("--run-plan", required=True, type=Path)
    partial_close_parser.add_argument("--state", required=True, type=Path)
    partial_close_parser.add_argument("--events", required=True, type=Path)
    partial_close_parser.add_argument("--residue", required=True, type=Path)
    partial_close_parser.add_argument("--output", required=True, type=Path)

    residue_parser = subparsers.add_parser("append-residue")
    residue_parser.add_argument("--residue", required=True, type=Path)
    residue_parser.add_argument("--record", required=True, type=Path)

    advance_parser = subparsers.add_parser("advance-wave")
    advance_parser.add_argument("dispatch", type=Path)
    advance_parser.add_argument("--state", required=True, type=Path)
    advance_parser.add_argument("--run-plan", required=True, type=Path)
    advance_parser.add_argument("--receipts-dir", required=True, type=Path)
    advance_parser.add_argument("--events", required=True, type=Path)
    advance_parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    try:
        if args.command == "append-event":
            record = _load_json_object(args.record, "causal record")
            appended = append_causal_records(args.events, [record])
            summary = {
                "status": "pass",
                "event": appended[0]["event"],
                "sequence": appended[0]["sequence"],
                "stream": str(args.events),
            }
        elif args.command == "prepare-spawn":
            request = prepare_spawn(
                args.action,
                args.run_plan,
                args.events,
                args.output,
                args.depends_on_gate_id,
            )
            summary = {
                "status": "pass",
                "state": "spawn_prepared",
                "action_id": request["action_id"],
                "request": str(args.output),
            }
        elif args.command == "record-spawn":
            event = record_spawn(
                args.action,
                args.run_plan,
                args.events,
                None if args.failed else args.agent_id,
            )
            summary = {
                "status": "pass",
                "state": event["event"],
                "action_id": event["action_id"],
                "agent_id": event["agent_id"],
            }
        elif args.command == "prepare-next-wave-plan":
            run_plan = prepare_next_wave_plan(
                args.dispatch,
                args.prior_run_plan,
                args.gate_decision,
                args.next_actions,
                args.next_state,
                args.events,
                args.actions_dir,
                args.output,
            )
            summary = {
                "status": "pass",
                "state": "wave_ready",
                "wave_id": run_plan["selected_wave"]["wave_id"],
                "action_count": len(run_plan["actions"]),
                "output": str(args.output),
            }
        elif args.command == "prepare-wait":
            request = prepare_wait(args.run_plan, args.events, args.output)
            summary = {
                "status": "pass",
                "state": "wait_prepared",
                "pending_count": len(request["pending_agent_ids"]),
                "request": str(args.output),
            }
        elif args.command == "prepare-partial-recovery":
            request = prepare_partial_recovery(
                args.run_plan, args.events, args.output
            )
            summary = {
                "status": "pass",
                "state": "partial_recovery_wait_prepared",
                "pending_count": len(request["pending_agent_ids"]),
                "request": str(args.output),
            }
        elif args.command == "record-partial-terminal":
            records = record_partial_terminal(
                args.action, args.run_plan, args.events, args.agent_id
            )
            summary = {
                "status": "pass",
                "state": "partial_sibling_closed",
                "action_id": records[0]["action_id"],
                "agent_id": records[0]["agent_id"],
            }
        elif args.command == "prepare-partial-interrupt":
            request = prepare_partial_interrupt(
                args.action,
                args.run_plan,
                args.events,
                args.agent_id,
                args.output,
            )
            summary = {
                "status": "pass",
                "state": "partial_sibling_interrupt_prepared",
                "action_id": request["action_id"],
                "agent_id": request["agent_id"],
                "request": str(args.output),
            }
        elif args.command == "record-partial-interrupt":
            event = record_partial_interrupt(
                args.action, args.run_plan, args.events, args.agent_id
            )
            summary = {
                "status": "pass",
                "state": "partial_sibling_interrupted",
                "action_id": event["action_id"],
                "agent_id": event["agent_id"],
            }
        elif args.command == "close-partial-wave":
            closeout = close_partial_wave(
                args.run_plan,
                args.state,
                args.events,
                args.residue,
                args.output,
            )
            summary = {
                "status": closeout["status"],
                "state": closeout["state"],
                "failed_action_ids": closeout["failed_action_ids"],
                "output": str(args.output),
            }
        elif args.command == "append-residue":
            record = _load_json_object(args.record, "residue record")
            appended = append_residue_record(args.residue, record)
            summary = {
                "status": "pass",
                "kind": appended["kind"],
                "sequence": appended["sequence"],
                "stream": str(args.residue),
            }
        else:
            result = advance_wave(
                args.dispatch,
                args.state,
                args.run_plan,
                args.receipts_dir,
                args.events,
                args.output_dir,
            )
            summary = {
                "status": result["status"],
                "state": result["state"]["state"],
                "decision": result["gate_decision"]["decision"],
                "next_action_count": len(result["action_set"]["actions"]),
                "receipt_admission": str(
                    args.output_dir / "receipt-admission.json"
                ),
                "event_validation": str(
                    args.output_dir / "event-validation.json"
                ),
            }
    except DriverBlocked as exc:
        print(
            json.dumps(
                {"status": "block", "blockers": exc.blockers},
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
