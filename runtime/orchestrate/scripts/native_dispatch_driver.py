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
    if exclusive and path.exists():
        raise DriverBlocked([f"output already exists: {path}"])
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


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
    task_stem = re.sub(r"[^a-z0-9]+", "_", action["role"].lower()).strip("_")
    action_stem = action["action_id"].replace("-", "_")
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
        "task_name": f"{task_stem}_{action_stem}",
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
    action, _ = _admit_persisted_action(action_path, run_plan_path)
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


def prepare_wait(
    run_plan_path: Path, event_stream: Path, request_output: Path
) -> dict[str, Any]:
    run_plan = _load_json_object(run_plan_path, "run plan")
    actions = run_plan.get("actions")
    if not isinstance(actions, list) or not actions:
        raise DriverBlocked(["run plan has no actions to wait for"])
    events = _validated_prefix(event_stream)
    successful_results: dict[str, dict[str, Any]] = {}
    for event in events:
        if event.get("event") == "host_spawn_returned":
            successful_results[str(event["action_id"])] = event

    records: list[dict[str, Any]] = []
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
        pending_agent_ids.append(agent_id)
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
    if len(set(pending_agent_ids)) != len(pending_agent_ids):
        raise DriverBlocked(["native agent bindings must be unique within a wave"])
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

    prepare_wait_parser = subparsers.add_parser("prepare-wait")
    prepare_wait_parser.add_argument("--run-plan", required=True, type=Path)
    prepare_wait_parser.add_argument("--events", required=True, type=Path)
    prepare_wait_parser.add_argument("--output", required=True, type=Path)

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
        elif args.command == "prepare-wait":
            request = prepare_wait(args.run_plan, args.events, args.output)
            summary = {
                "status": "pass",
                "state": "wait_prepared",
                "pending_count": len(request["pending_agent_ids"]),
                "request": str(args.output),
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
