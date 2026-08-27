#!/usr/bin/env python3
"""Compile the first executable wave of a validated Arcanum dispatch.

This module is deliberately deterministic. It validates and compiles actions; it
does not call any host-native agent operation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


AUTHORIZED_STATES = {"approved", "not_needed"}
STATE_SCHEMA_VERSION = "arcanum.native-dispatch-runner.state.v0.1"
RUN_PLAN_SCHEMA_VERSION = "arcanum.native-dispatch-runner.run-plan.v0.1"
ACTION_SCHEMA_VERSION = "arcanum.native-dispatch-runner.action.v0.1"
RECEIPT_SCHEMA_VERSION = "arcanum.native-dispatch-runner.receipt.v0.1"
GATE_DECISION_SCHEMA_VERSION = "arcanum.native-dispatch-runner.gate-decision.v0.1"
ACTION_SET_SCHEMA_VERSION = "arcanum.native-dispatch-runner.action-set.v0.1"
MAX_ACTION_NUMBER = 9999
BRIEFING_CONTRACT_VERSION = "arcanum.confirmed-role-briefing.v0.1"
STRATEGY_REGISTRATION_SCHEMA_VERSION = "arcanum.subagent-strategy-registration.v0.2"
STRATEGY_LEDGER = Path(".arcanum/observability/subagents-strategy/subagents-dispatch.yaml")
STRATEGY_TEMP_ROOT = Path(".arcanum/runtime/subagents-strategy")
SHEET_SCHEMA_VERSION = "0.6.1"
EXECUTION_PROJECTION_FIELDS = (
    "binding_mode",
    "execution_owner",
    "roles",
    "execution_waves",
    "parallelism",
    "join_policy",
    "authorization",
    "receipt_requirements",
)

RECEIPT_REQUIRED_FIELDS = {
    "schema_version",
    "action_id",
    "dispatch_id",
    "run_id",
    "wave_id",
    "step_id",
    "role",
    "capability_ref",
    "agent_id",
    "status",
    "artifacts",
    "validation",
    "blockers",
    "started_at",
    "finished_at",
}


class CompileBlocked(RuntimeError):
    """Raised when compilation must stop without emitting executable actions."""

    def __init__(self, blockers: list[str]) -> None:
        super().__init__("; ".join(blockers))
        self.blockers = blockers


def _project_root_for_dispatch(
    dispatch_path: Path, project_root: Path | None = None
) -> Path:
    if project_root is not None:
        root = project_root.resolve()
        if not root.is_dir():
            raise CompileBlocked([f"project root is not a directory: {root}"])
        return root

    configured = os.environ.get("ARCANUM_PROJECT_DIR")
    if configured:
        root = Path(configured).resolve()
        if not root.is_dir():
            raise CompileBlocked([f"ARCANUM_PROJECT_DIR is not a directory: {root}"])
        return root

    resolved_dispatch = dispatch_path.resolve()
    for candidate in (resolved_dispatch.parent, *resolved_dispatch.parents):
        if (candidate / STRATEGY_LEDGER).is_file():
            return candidate
    for candidate in (resolved_dispatch.parent, *resolved_dispatch.parents):
        if (candidate / ".git").exists():
            return candidate
    raise CompileBlocked(["cannot resolve project root for subagent strategy registration"])


def _decode_ledger_scalar(raw: str, line_number: int) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CompileBlocked(
            [f"strategy ledger line {line_number} has an invalid scalar: {exc.msg}"]
        ) from exc


def _strategy_ledger_rows(ledger_path: Path) -> list[dict[str, Any]]:
    try:
        text = ledger_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CompileBlocked([f"cannot read strategy ledger {ledger_path}: {exc}"]) from exc

    rows: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        start = re.fullmatch(r"  - (dispatch_id|close_of): (.+)", line)
        if start:
            if current is not None:
                rows.append(current)
            current = {
                start.group(1): _decode_ledger_scalar(start.group(2), line_number)
            }
            continue
        field = re.fullmatch(r"    ([a-z][a-z0-9_]*): (.+)", line)
        if field and current is not None:
            current[field.group(1)] = _decode_ledger_scalar(
                field.group(2), line_number
            )
    if current is not None:
        rows.append(current)
    return rows


def strategy_execution_projection(dispatch: dict[str, Any]) -> dict[str, Any]:
    """Return the complete executable strategy subset committed at confirmation."""

    strategy = dispatch.get("subagent_strategy")
    if not isinstance(strategy, dict):
        raise CompileBlocked(["dispatch must declare a subagent_strategy"])
    return {field: copy.deepcopy(strategy.get(field)) for field in EXECUTION_PROJECTION_FIELDS}


def strategy_execution_projection_sha256(dispatch: dict[str, Any]) -> str:
    return _canonical_payload_sha256(strategy_execution_projection(dispatch))


def _registered_topology(row: dict[str, Any]) -> list[dict[str, Any]]:
    groups = row.get("groups")
    connections = row.get("connections", [])
    if not isinstance(groups, list) or not all(isinstance(group, dict) for group in groups):
        raise CompileBlocked(["registered strategy topology has no valid groups"])
    if not isinstance(connections, list):
        raise CompileBlocked(["registered strategy topology has invalid connections"])
    blocking = {"sequential", "zig-zag"}
    topology = []
    for group in groups:
        group_id = group.get("group_id")
        agents = group.get("agents")
        if not isinstance(group_id, str) or not isinstance(agents, list):
            raise CompileBlocked(["registered strategy topology has an invalid group"])
        dependencies = []
        for connection in connections:
            if not isinstance(connection, dict):
                raise CompileBlocked(["registered strategy topology has an invalid connection"])
            if connection.get("to") == group_id and connection.get("type") in blocking:
                source = connection.get("from")
                if not isinstance(source, str):
                    raise CompileBlocked(["registered strategy topology has an invalid dependency"])
                dependencies.append(source)
        topology.append({"wave_id": group_id, "agent_count": len(agents), "depends_on_waves": sorted(dependencies)})
    return topology


def _runtime_topology(dispatch: dict[str, Any]) -> list[dict[str, Any]]:
    strategy = dispatch.get("subagent_strategy", {})
    roles = strategy.get("roles", [])
    waves = strategy.get("execution_waves", [])
    role_counts = {
        role.get("role_id"): role.get("agent_count")
        for role in roles
        if isinstance(role, dict)
    }
    topology = []
    for wave in waves:
        if not isinstance(wave, dict):
            raise CompileBlocked(["runtime strategy topology has an invalid execution wave"])
        wave_roles = wave.get("role_ids", [])
        if not isinstance(wave_roles, list) or any(
            not isinstance(role_counts.get(role_id), int) or role_counts[role_id] < 1
            for role_id in wave_roles
        ):
            raise CompileBlocked(["runtime strategy topology has invalid role cardinality"])
        topology.append(
            {
                "wave_id": wave.get("wave_id"),
                "agent_count": sum(role_counts[role_id] for role_id in wave_roles),
                "depends_on_waves": sorted(wave.get("depends_on_waves", []) or []),
            }
        )
    return topology


def verify_strategy_registration(
    dispatch: dict[str, Any],
    dispatch_path: Path,
    project_root: Path | None = None,
    *,
    require_close: bool = False,
) -> dict[str, Any]:
    """Verify the exact-sheet ledger row and temporary-file lifecycle."""

    dispatch_id = dispatch.get("dispatch_id")
    strategy = dispatch.get("subagent_strategy")
    if not isinstance(dispatch_id, str) or not dispatch_id:
        raise CompileBlocked(["dispatch_id is required for strategy registration"])
    if not isinstance(strategy, dict):
        raise CompileBlocked(["dispatch must declare a subagent_strategy"])
    registration = strategy.get("registration")
    if not isinstance(registration, dict):
        raise CompileBlocked(["approved subagent execution has no strategy registration"])
    if registration.get("schema_version") != STRATEGY_REGISTRATION_SCHEMA_VERSION:
        raise CompileBlocked(["strategy registration schema_version mismatch"])
    if registration.get("ledger") != STRATEGY_LEDGER.as_posix():
        raise CompileBlocked(["strategy registration ledger path is not canonical"])
    if registration.get("sheet_schema_version") != SHEET_SCHEMA_VERSION:
        raise CompileBlocked(["strategy registration sheet_schema_version mismatch"])
    sheet_sha = registration.get("sheet_sha256")
    if not isinstance(sheet_sha, str) or re.fullmatch(r"[0-9a-f]{64}", sheet_sha) is None:
        raise CompileBlocked(["strategy registration sheet_sha256 is invalid"])
    projection_sha = registration.get("execution_projection_sha256")
    if not isinstance(projection_sha, str) or re.fullmatch(r"[0-9a-f]{64}", projection_sha) is None:
        raise CompileBlocked(["strategy registration execution_projection_sha256 is invalid"])
    computed_projection_sha = strategy_execution_projection_sha256(dispatch)
    if projection_sha != computed_projection_sha:
        raise CompileBlocked(["strategy registration execution projection digest mismatch"])

    root = _project_root_for_dispatch(dispatch_path, project_root)
    sheet_raw = str(registration.get("temporary_sheet", ""))
    close_raw = str(registration.get("temporary_close", ""))
    sheet_rel = Path(sheet_raw)
    close_rel = Path(close_raw)
    for label, raw, relative, suffix in (
        ("temporary_sheet", sheet_raw, sheet_rel, ".tmp.json"),
        ("temporary_close", close_raw, close_rel, ".close.tmp.json"),
    ):
        if "\\" in raw or not raw.startswith(STRATEGY_TEMP_ROOT.as_posix() + "/"):
            raise CompileBlocked(
                [f"strategy registration {label} must use a portable project-relative path"]
            )
        try:
            resolved = (root / relative).resolve()
            resolved.relative_to((root / STRATEGY_TEMP_ROOT).resolve())
        except (OSError, ValueError) as exc:
            raise CompileBlocked([f"strategy registration {label} escapes its runtime root"]) from exc
        if not relative.as_posix().endswith(suffix):
            raise CompileBlocked([f"strategy registration {label} has the wrong suffix"])

    if (root / sheet_rel).exists():
        raise CompileBlocked(["confirmed strategy sheet was not consumed before preflight"])

    ledger_path = root / STRATEGY_LEDGER
    if not ledger_path.is_file():
        raise CompileBlocked([f"strategy ledger does not exist: {ledger_path}"])
    rows = _strategy_ledger_rows(ledger_path)
    dispatch_rows = [row for row in rows if row.get("dispatch_id") == dispatch_id]
    if len(dispatch_rows) != 1:
        raise CompileBlocked(
            [f"strategy ledger must contain exactly one dispatch row for {dispatch_id}"]
        )
    row = dispatch_rows[0]
    if row.get("schema_version") != SHEET_SCHEMA_VERSION:
        raise CompileBlocked(["registered strategy sheet schema_version mismatch"])
    if row.get("sheet_sha256") != sheet_sha:
        raise CompileBlocked(["registered strategy sheet digest mismatch"])
    if row.get("execution_projection_sha256") != projection_sha:
        raise CompileBlocked(["registered strategy execution projection digest mismatch"])
    registered_topology = _registered_topology(row)
    runtime_topology = _runtime_topology(dispatch)
    if registered_topology != runtime_topology:
        raise CompileBlocked(["registered strategy topology does not match executable runtime waves"])

    close_rows = [row for row in rows if row.get("close_of") == dispatch_id]
    if require_close:
        if (root / close_rel).exists():
            raise CompileBlocked(["strategy close record was not consumed"])
        if len(close_rows) != 1:
            raise CompileBlocked(
                [f"strategy ledger must contain exactly one close row for {dispatch_id}"]
            )
        if rows.index(close_rows[0]) <= rows.index(dispatch_rows[0]):
            raise CompileBlocked(["strategy close row must follow its dispatch row"])
        close_row = close_rows[0]
        if close_row.get("exit_reason") != "resolved":
            raise CompileBlocked(["strategy close row is not resolved"])
        if re.fullmatch(r"[0-9a-f]{64}", str(close_row.get("close_sha256", ""))) is None:
            raise CompileBlocked(["strategy close row has no content digest"])
        agents_spawned = close_row.get("agents_spawned")
        expected_agents = sum(item["agent_count"] for item in registered_topology)
        if not isinstance(agents_spawned, dict) or agents_spawned.get("total") != expected_agents:
            raise CompileBlocked(["strategy close agent total does not match the registered topology"])
        tree = agents_spawned.get("tree", {})
        if (
            not isinstance(tree, dict)
            or any(not isinstance(value, int) or value < 0 for value in tree.values())
            or sum(tree.values()) != agents_spawned.get("total")
        ):
            raise CompileBlocked(["strategy close agent tree does not sum to its total"])
        if agents_spawned.get("loops_used", -1) > row.get("max_loops", -1):
            raise CompileBlocked(["strategy close loops_used exceeds registered max_loops"])

    return {
        "status": "pass",
        "dispatch_id": dispatch_id,
        "sheet_sha256": sheet_sha,
        "execution_projection_sha256": projection_sha,
        "topology": runtime_topology,
        "ledger": str(ledger_path),
        "dispatch_registered": True,
        "close_registered": len(close_rows) == 1,
        "temporary_sheet_consumed": not (root / sheet_rel).exists(),
        "temporary_close_consumed": not (root / close_rel).exists(),
    }


def _canonical_payload_sha256(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _validated_briefing_binding(
    role: dict[str, Any], role_id: str
) -> dict[str, Any]:
    binding = role.get("briefing_binding")
    if not isinstance(binding, dict):
        raise CompileBlocked([f"role has no briefing_binding: {role_id}"])
    if binding.get("contract_version") != BRIEFING_CONTRACT_VERSION:
        raise CompileBlocked([f"role has unsupported briefing contract: {role_id}"])
    briefing = binding.get("briefing")
    source = binding.get("source_binding")
    if not isinstance(briefing, dict) or not isinstance(source, dict):
        raise CompileBlocked([f"role briefing binding is incomplete: {role_id}"])
    briefing_sha = _canonical_payload_sha256(briefing)
    if binding.get("briefing_sha256") != briefing_sha:
        raise CompileBlocked([f"role briefing digest mismatch: {role_id}"])
    if source.get("selected_payload_sha256") != briefing_sha:
        raise CompileBlocked([f"role selected payload digest mismatch: {role_id}"])
    read_policy = briefing.get("read_policy")
    write_policy = briefing.get("write_policy")
    if not isinstance(read_policy, dict) or not isinstance(write_policy, dict):
        raise CompileBlocked([f"role briefing policy is incomplete: {role_id}"])
    if read_policy.get("input_refs") != list(role.get("input_refs", []) or []):
        raise CompileBlocked([f"role briefing read policy mismatch: {role_id}"])
    expected_write_policy = {
        "mutation_policy": role.get("mutation_policy"),
        "write_scope": list(role.get("write_scope", []) or []),
        "forbidden_write_scopes": list(role.get("forbidden_write_scopes", []) or []),
    }
    if write_policy != expected_write_policy:
        raise CompileBlocked([f"role briefing write policy mismatch: {role_id}"])
    status = briefing.get("status_semantics")
    receipt = briefing.get("receipt_shape")
    if not isinstance(status, dict) or not isinstance(receipt, dict):
        raise CompileBlocked([f"role briefing status or receipt shape is incomplete: {role_id}"])
    required_fields = receipt.get("required_fields", [])
    if (
        status.get("task_status_field") == status.get("domain_gate_status_field")
        or status.get("task_status_field") not in required_fields
        or status.get("domain_gate_status_field") not in required_fields
        or receipt.get("completion_requires_all_fields") is not True
    ):
        raise CompileBlocked([f"role briefing status/receipt contract mismatch: {role_id}"])
    return copy.deepcopy(binding)


def _format_action_id(action_number: int) -> str:
    if action_number < 1 or action_number > MAX_ACTION_NUMBER:
        raise CompileBlocked(
            [f"run action allocation exceeds supported range: {action_number}"]
        )
    return f"spawn-{action_number:04d}"


def _action_count_for_waves(
    dispatch: dict[str, Any], wave_ids: list[str]
) -> int:
    """Count statically declared action instances for an ordered wave history."""

    strategy = dispatch.get("subagent_strategy")
    if not isinstance(strategy, dict):
        raise CompileBlocked(["dispatch must declare a subagent_strategy"])
    roles = strategy.get("roles")
    waves = strategy.get("execution_waves")
    if not isinstance(roles, list) or not isinstance(waves, list):
        raise CompileBlocked(["capability-bound strategy requires roles and execution_waves"])

    role_by_id: dict[str, dict[str, Any]] = {}
    for role in roles:
        if not isinstance(role, dict) or not role.get("role_id"):
            continue
        role_id = str(role["role_id"])
        if role_id in role_by_id:
            raise CompileBlocked([f"duplicate strategy role identifier: {role_id}"])
        role_by_id[role_id] = role

    wave_by_id: dict[str, dict[str, Any]] = {}
    for wave in waves:
        if not isinstance(wave, dict) or not wave.get("wave_id"):
            continue
        wave_id = str(wave["wave_id"])
        if wave_id in wave_by_id:
            raise CompileBlocked([f"duplicate execution wave identifier: {wave_id}"])
        wave_by_id[wave_id] = wave

    total = 0
    seen_wave_ids: set[str] = set()
    for wave_id in wave_ids:
        if wave_id in seen_wave_ids:
            raise CompileBlocked([f"duplicate completed wave identifier: {wave_id}"])
        seen_wave_ids.add(wave_id)
        wave = wave_by_id.get(wave_id)
        if wave is None:
            raise CompileBlocked([f"unknown completed wave identifier: {wave_id}"])
        for role_id_value in wave.get("role_ids", []) or []:
            role_id = str(role_id_value)
            role = role_by_id.get(role_id)
            if role is None:
                raise CompileBlocked(
                    [f"completed wave '{wave_id}' references unknown role: {role_id}"]
                )
            agent_count = role.get("agent_count")
            if (
                not isinstance(agent_count, int)
                or isinstance(agent_count, bool)
                or agent_count < 1
            ):
                raise CompileBlocked([f"role has invalid agent_count: {role_id}"])
            total += agent_count
            if total > MAX_ACTION_NUMBER:
                raise CompileBlocked(
                    [f"run action allocation exceeds supported range: {total}"]
                )
    return total


def _validated_run_action_count(
    dispatch: dict[str, Any],
    state: dict[str, Any],
    actions: list[dict[str, Any]],
    current_wave_id: str,
) -> int:
    """Validate the current frontier and return its run-global allocated count."""

    eligible_action_ids = state.get("eligible_action_ids")
    if not isinstance(eligible_action_ids, list) or any(
        not isinstance(action_id, str) for action_id in eligible_action_ids
    ):
        raise CompileBlocked(["state eligible_action_ids must be an array of strings"])

    action_ids = [action.get("action_id") for action in actions]
    if any(not isinstance(action_id, str) for action_id in action_ids):
        raise CompileBlocked(["run-plan actions must have string action_id values"])
    if eligible_action_ids != action_ids:
        raise CompileBlocked(["state/run-plan eligible action mismatch"])
    if len(set(action_ids)) != len(action_ids):
        raise CompileBlocked(["run-plan action identifiers must be unique"])

    previous_completed = [str(item) for item in state.get("completed_wave_ids", []) or []]
    previous_action_count = _action_count_for_waves(dispatch, previous_completed)
    allocated_action_count = _action_count_for_waves(
        dispatch, previous_completed + [current_wave_id]
    )
    expected_action_ids = [
        _format_action_id(action_number)
        for action_number in range(previous_action_count + 1, allocated_action_count + 1)
    ]
    if action_ids != expected_action_ids:
        raise CompileBlocked(["run-plan action identifiers do not match run-global allocation"])
    return allocated_action_count


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CompileBlocked([f"cannot load dispatch JSON: {exc}"]) from exc
    if not isinstance(value, dict):
        raise CompileBlocked(["dispatch JSON root must be an object"])
    return value


def discover_validator() -> Path:
    """Find the canonical validator from a canonical or generated package path."""

    relative_candidates = (
        Path("formulae/dispatch-spec/scripts/validate-dispatch.py"),
        Path("dispatch-spec/scripts/validate-dispatch.py"),
    )
    for parent in Path(__file__).resolve().parents:
        for relative in relative_candidates:
            candidate = parent / relative
            if candidate.is_file():
                return candidate
    raise CompileBlocked(["canonical Dispatch Spec validator was not found"])


def validate_dispatch(dispatch_path: Path, validator_path: Path | None = None) -> dict[str, Any]:
    validator = validator_path or discover_validator()
    completed = subprocess.run(
        [sys.executable, str(validator), str(dispatch_path), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        receipt = json.loads(completed.stdout)
    except json.JSONDecodeError:
        detail = completed.stderr.strip() or completed.stdout.strip() or "validator emitted no JSON"
        return {
            "validation": "block",
            "blocks": [f"validator invocation failed: {detail}"],
            "flags": [],
        }
    if not isinstance(receipt, dict):
        return {
            "validation": "block",
            "blocks": ["validator receipt root must be an object"],
            "flags": [],
        }
    if completed.returncode != 0 and receipt.get("validation") != "block":
        receipt = {
            "validation": "block",
            "blocks": [f"validator exited with status {completed.returncode}"],
            "flags": list(receipt.get("flags", [])),
        }
    return receipt


def _prepare_output_directory(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise CompileBlocked([f"output directory must be empty: {output_dir}"])
    output_dir.mkdir(parents=True, exist_ok=True)


def _blocked_state(
    dispatch_id: str,
    run_id: str,
    state: str,
    authorization: str,
    blockers: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "state": state,
        "validation_status": "pass",
        "authorization_status": authorization,
        "selected_wave_id": None,
        "eligible_action_ids": [],
        "completed_wave_ids": [],
        "blockers": blockers,
    }


def compile_first_wave(dispatch: dict[str, Any], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return deterministic state and run plan for the first eligible wave."""

    dispatch_id = str(dispatch.get("dispatch_id", ""))
    strategy = dispatch.get("subagent_strategy")
    if not isinstance(strategy, dict) or strategy.get("binding_mode") != "capability-bound":
        raise CompileBlocked(["dispatch must declare a capability-bound subagent_strategy"])

    authorization = str(strategy.get("authorization", ""))
    if authorization not in AUTHORIZED_STATES:
        raise CompileBlocked([f"execution authorization is not satisfied: {authorization or '<missing>'}"])

    roles = strategy.get("roles")
    waves = strategy.get("execution_waves")
    if not isinstance(roles, list) or not isinstance(waves, list) or not waves:
        raise CompileBlocked(["capability-bound strategy requires roles and execution_waves"])

    role_by_id = {
        str(role.get("role_id")): role
        for role in roles
        if isinstance(role, dict) and role.get("role_id")
    }
    selected_wave: dict[str, Any] | None = None
    for candidate in waves:
        if isinstance(candidate, dict) and not (candidate.get("depends_on_waves") or []):
            selected_wave = candidate
            break
    if selected_wave is None:
        raise CompileBlocked(["no dependency-free initial execution wave exists"])

    wave_id = str(selected_wave.get("wave_id", ""))
    actions: list[dict[str, Any]] = []
    for role_id_value in selected_wave.get("role_ids", []) or []:
        role_id = str(role_id_value)
        role = role_by_id.get(role_id)
        if role is None:
            raise CompileBlocked([f"selected wave references unknown role: {role_id}"])
        if role.get("depends_on_roles"):
            raise CompileBlocked([f"initial-wave role has unmet role dependencies: {role_id}"])

        applies_to_steps = [str(item) for item in role.get("applies_to_steps", []) or []]
        if not applies_to_steps:
            raise CompileBlocked([f"role has no applied step: {role_id}"])
        agent_count = role.get("agent_count")
        if not isinstance(agent_count, int) or isinstance(agent_count, bool) or agent_count < 1:
            raise CompileBlocked([f"role has invalid agent_count: {role_id}"])

        for agent_ordinal in range(agent_count):
            briefing_binding = _validated_briefing_binding(role, role_id)
            action_number = len(actions) + 1
            action = {
                "schema_version": ACTION_SCHEMA_VERSION,
                "action_id": _format_action_id(action_number),
                "action": "spawn",
                "dispatch_id": dispatch_id,
                "run_id": run_id,
                "wave_id": wave_id,
                "step_id": applies_to_steps[0],
                "applies_to_steps": applies_to_steps,
                "role": role_id,
                "agent_ordinal": agent_ordinal,
                "agent_count": agent_count,
                "capability_ref": str(role.get("capability_ref")),
                "target": str(role.get("capability_target")),
                "mode": str(role.get("capability_mode")),
                "mutation_policy": str(role.get("mutation_policy")),
                "write_scope": list(role.get("write_scope", []) or []),
                "forbidden_write_scopes": list(role.get("forbidden_write_scopes", []) or []),
                "briefing_binding": briefing_binding,
                "input_refs": list(role.get("input_refs", []) or []),
                "output_refs": list(role.get("output_refs", []) or []),
            }
            actions.append(action)

    if not actions:
        raise CompileBlocked([f"selected wave has no executable role instances: {wave_id}"])

    action_ids = [action["action_id"] for action in actions]
    state = {
        "schema_version": STATE_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "state": "wave_ready",
        "validation_status": "pass",
        "authorization_status": authorization,
        "selected_wave_id": wave_id,
        "eligible_action_ids": action_ids,
        "completed_wave_ids": [],
        "blockers": [],
    }
    wave_plan = {
        "wave_id": wave_id,
        "role_ids": [str(item) for item in selected_wave.get("role_ids", []) or []],
        "parallel": bool(selected_wave.get("parallel", False)),
        "join_policy": str(selected_wave.get("join_policy", "all")),
        "depends_on_waves": list(selected_wave.get("depends_on_waves", []) or []),
        "gate_after": selected_wave.get("gate_after"),
        "on_incomplete": str(selected_wave.get("on_incomplete", "block")),
    }
    run_plan = {
        "schema_version": RUN_PLAN_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "state": "wave_ready",
        "validation_status": "pass",
        "selected_wave": wave_plan,
        "action_artifacts": [f"actions/{action_id}.json" for action_id in action_ids],
        "actions": actions,
    }
    return state, run_plan


def compile_to_directory(
    dispatch_path: Path,
    run_id: str,
    output_dir: Path,
    validator_path: Path | None = None,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Validate, compile, and persist one first-wave run plan."""

    if not run_id.strip():
        raise CompileBlocked(["run_id must be non-empty"])
    _prepare_output_directory(output_dir)
    validation = validate_dispatch(dispatch_path, validator_path)
    _write_json(output_dir / "validation.json", validation)
    if validation.get("validation") != "pass":
        blockers = list(validation.get("blocks", []) or [])
        flags = list(validation.get("flags", []) or [])
        raise CompileBlocked(blockers + [f"validator flag: {flag}" for flag in flags] or ["dispatch did not validate"])

    dispatch = _load_json(dispatch_path)
    try:
        registration = verify_strategy_registration(
            dispatch, dispatch_path, project_root
        )
    except CompileBlocked as exc:
        strategy = dispatch.get("subagent_strategy") if isinstance(dispatch.get("subagent_strategy"), dict) else {}
        authorization = str(strategy.get("authorization", ""))
        _write_json(
            output_dir / "state.json",
            _blocked_state(
                str(dispatch.get("dispatch_id", "")),
                run_id,
                "blocked",
                authorization,
                exc.blockers,
            ),
        )
        raise
    _write_json(output_dir / "strategy-registration.json", registration)
    try:
        state, run_plan = compile_first_wave(dispatch, run_id)
    except CompileBlocked as exc:
        strategy = dispatch.get("subagent_strategy") if isinstance(dispatch.get("subagent_strategy"), dict) else {}
        authorization = str(strategy.get("authorization", ""))
        state_name = "authorization_pending" if authorization not in AUTHORIZED_STATES else "blocked"
        _write_json(
            output_dir / "state.json",
            _blocked_state(str(dispatch.get("dispatch_id", "")), run_id, state_name, authorization, exc.blockers),
        )
        raise

    _write_json(output_dir / "state.json", state)
    _write_json(output_dir / "run-plan.json", run_plan)
    for action in run_plan["actions"]:
        _write_json(output_dir / "actions" / f"{action['action_id']}.json", action)
    return {"status": "pass", "state": state, "run_plan": run_plan}


def _compile_named_wave_actions(
    dispatch: dict[str, Any],
    run_id: str,
    wave_id: str,
    start_action_number: int,
) -> list[dict[str, Any]]:
    strategy = dispatch.get("subagent_strategy")
    if not isinstance(strategy, dict) or strategy.get("binding_mode") != "capability-bound":
        raise CompileBlocked(["dispatch must declare a capability-bound subagent_strategy"])
    authorization = str(strategy.get("authorization", ""))
    if authorization not in AUTHORIZED_STATES:
        raise CompileBlocked([f"execution authorization is not satisfied: {authorization or '<missing>'}"])

    roles = strategy.get("roles", []) or []
    waves = strategy.get("execution_waves", []) or []
    role_by_id = {
        str(role.get("role_id")): role
        for role in roles
        if isinstance(role, dict) and role.get("role_id")
    }
    wave = next(
        (
            candidate
            for candidate in waves
            if isinstance(candidate, dict) and str(candidate.get("wave_id")) == wave_id
        ),
        None,
    )
    if wave is None:
        raise CompileBlocked([f"unknown execution wave: {wave_id}"])

    actions: list[dict[str, Any]] = []
    for role_id_value in wave.get("role_ids", []) or []:
        role_id = str(role_id_value)
        role = role_by_id.get(role_id)
        if role is None:
            raise CompileBlocked([f"selected wave references unknown role: {role_id}"])
        applies_to_steps = [str(item) for item in role.get("applies_to_steps", []) or []]
        if not applies_to_steps:
            raise CompileBlocked([f"role has no applied step: {role_id}"])
        agent_count = role.get("agent_count")
        if not isinstance(agent_count, int) or isinstance(agent_count, bool) or agent_count < 1:
            raise CompileBlocked([f"role has invalid agent_count: {role_id}"])

        for agent_ordinal in range(agent_count):
            briefing_binding = _validated_briefing_binding(role, role_id)
            action_number = start_action_number + len(actions)
            actions.append(
                {
                    "schema_version": ACTION_SCHEMA_VERSION,
                    "action_id": _format_action_id(action_number),
                    "action": "spawn",
                    "dispatch_id": str(dispatch.get("dispatch_id", "")),
                    "run_id": run_id,
                    "wave_id": wave_id,
                    "step_id": applies_to_steps[0],
                    "applies_to_steps": applies_to_steps,
                    "role": role_id,
                    "agent_ordinal": agent_ordinal,
                    "agent_count": agent_count,
                    "capability_ref": str(role.get("capability_ref")),
                    "target": str(role.get("capability_target")),
                    "mode": str(role.get("capability_mode")),
                    "mutation_policy": str(role.get("mutation_policy")),
                    "write_scope": list(role.get("write_scope", []) or []),
                    "forbidden_write_scopes": list(role.get("forbidden_write_scopes", []) or []),
                    "briefing_binding": briefing_binding,
                    "input_refs": list(role.get("input_refs", []) or []),
                    "output_refs": list(role.get("output_refs", []) or []),
                }
            )
    if not actions:
        raise CompileBlocked([f"selected wave has no executable role instances: {wave_id}"])
    return actions


def _normalized_wave_plan(wave: Any) -> dict[str, Any]:
    """Return the closed run-plan projection of one declared route wave."""

    if not isinstance(wave, dict):
        raise CompileBlocked(["execution wave must be an object"])
    wave_id = wave.get("wave_id")
    role_ids = wave.get("role_ids")
    dependencies = wave.get("depends_on_waves", []) or []
    if not isinstance(wave_id, str) or not wave_id:
        raise CompileBlocked(["execution wave must have a non-empty wave_id"])
    if (
        not isinstance(role_ids, list)
        or not role_ids
        or any(not isinstance(item, str) or not item for item in role_ids)
    ):
        raise CompileBlocked([f"execution wave '{wave_id}' has invalid role_ids"])
    if (
        not isinstance(dependencies, list)
        or any(not isinstance(item, str) or not item for item in dependencies)
        or len(set(dependencies)) != len(dependencies)
    ):
        raise CompileBlocked(
            [f"execution wave '{wave_id}' has invalid depends_on_waves"]
        )
    gate_after = wave.get("gate_after")
    if gate_after is not None and (
        not isinstance(gate_after, str) or not gate_after
    ):
        raise CompileBlocked([f"execution wave '{wave_id}' has invalid gate_after"])
    if not isinstance(wave.get("parallel", False), bool):
        raise CompileBlocked([f"execution wave '{wave_id}' has invalid parallel"])
    for field, default in (("join_policy", "all"), ("on_incomplete", "block")):
        value = wave.get(field, default)
        if not isinstance(value, str) or not value:
            raise CompileBlocked([f"execution wave '{wave_id}' has invalid {field}"])
    return {
        "wave_id": wave_id,
        "role_ids": list(role_ids),
        "parallel": wave.get("parallel", False),
        "join_policy": wave.get("join_policy", "all"),
        "depends_on_waves": list(dependencies),
        "gate_after": gate_after,
        "on_incomplete": wave.get("on_incomplete", "block"),
    }


def build_next_wave_plan(
    dispatch: dict[str, Any],
    prior_run_plan: dict[str, Any],
    gate_decision: dict[str, Any],
    action_set: dict[str, Any],
    next_state: dict[str, Any],
    persisted_actions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Purely derive one dependent-wave plan from an admitted gate frontier."""

    dispatch_id = dispatch.get("dispatch_id")
    run_id = prior_run_plan.get("run_id")
    if not isinstance(dispatch_id, str) or not dispatch_id:
        raise CompileBlocked(["dispatch must have a non-empty dispatch_id"])
    if not isinstance(run_id, str) or not run_id:
        raise CompileBlocked(["prior run plan must have a non-empty run_id"])

    versioned_inputs = (
        ("prior run plan", prior_run_plan, RUN_PLAN_SCHEMA_VERSION),
        ("gate decision", gate_decision, GATE_DECISION_SCHEMA_VERSION),
        ("next action set", action_set, ACTION_SET_SCHEMA_VERSION),
        ("next state", next_state, STATE_SCHEMA_VERSION),
    )
    for label, value, expected_version in versioned_inputs:
        if not isinstance(value, dict):
            raise CompileBlocked([f"{label} must be an object"])
        if value.get("schema_version") != expected_version:
            raise CompileBlocked([f"{label} has an unsupported schema_version"])
        if value.get("dispatch_id") != dispatch_id:
            raise CompileBlocked([f"{label} dispatch identity mismatch"])
        if value.get("run_id") != run_id:
            raise CompileBlocked([f"{label} run identity mismatch"])

    strategy = dispatch.get("subagent_strategy")
    if not isinstance(strategy, dict) or strategy.get("binding_mode") != "capability-bound":
        raise CompileBlocked(["dispatch must declare a capability-bound subagent_strategy"])
    authorization = strategy.get("authorization")
    if authorization not in AUTHORIZED_STATES:
        raise CompileBlocked(
            [f"execution authorization is not satisfied: {authorization or '<missing>'}"]
        )
    waves = strategy.get("execution_waves")
    if not isinstance(waves, list) or not waves:
        raise CompileBlocked(["capability-bound strategy requires execution_waves"])
    wave_by_id: dict[str, dict[str, Any]] = {}
    for wave in waves:
        normalized = _normalized_wave_plan(wave)
        wave_id = normalized["wave_id"]
        if wave_id in wave_by_id:
            raise CompileBlocked([f"duplicate execution wave identifier: {wave_id}"])
        wave_by_id[wave_id] = wave

    selected_wave = prior_run_plan.get("selected_wave")
    prior_actions = prior_run_plan.get("actions")
    if not isinstance(selected_wave, dict) or not isinstance(prior_actions, list) or not prior_actions:
        raise CompileBlocked(["prior run plan must contain one selected wave and actions"])
    if any(not isinstance(action, dict) for action in prior_actions):
        raise CompileBlocked(["prior run plan contains a non-object action"])
    source_wave_id = selected_wave.get("wave_id")
    if not isinstance(source_wave_id, str) or source_wave_id not in wave_by_id:
        raise CompileBlocked(["prior run plan references an unknown source wave"])
    if selected_wave != _normalized_wave_plan(wave_by_id[source_wave_id]):
        raise CompileBlocked(["prior run plan source wave does not match the dispatch route"])
    prior_action_ids = [action.get("action_id") for action in prior_actions]
    if any(not isinstance(item, str) or not item for item in prior_action_ids):
        raise CompileBlocked(["prior run plan has invalid action identifiers"])
    if len(set(prior_action_ids)) != len(prior_action_ids):
        raise CompileBlocked(["prior run plan action identifiers must be unique"])
    if prior_run_plan.get("state") != "wave_ready" or prior_run_plan.get("validation_status") != "pass":
        raise CompileBlocked(["prior run plan is not validator-ready"])
    if prior_run_plan.get("action_artifacts") != [
        f"actions/{action_id}.json" for action_id in prior_action_ids
    ]:
        raise CompileBlocked(["prior run plan action artifacts do not exactly bind its actions"])

    gate_id = gate_decision.get("gate_id")
    if not isinstance(gate_id, str) or not gate_id:
        raise CompileBlocked(["dependent-wave planning requires a non-empty source gate"])
    if (
        gate_decision.get("wave_id") != source_wave_id
        or action_set.get("source_wave_id") != source_wave_id
        or selected_wave.get("gate_after") != gate_id
        or action_set.get("source_gate_id") != gate_id
    ):
        raise CompileBlocked(["prior plan/source gate linkage mismatch"])
    if gate_decision.get("decision") != "gate_pass" or gate_decision.get("blockers"):
        raise CompileBlocked(["source gate decision is not an unblocked gate_pass"])
    if action_set.get("decision") != "gate_pass":
        raise CompileBlocked(["next action set is not opened by gate_pass"])
    if gate_decision.get("required_action_ids") != prior_action_ids:
        raise CompileBlocked(["source gate required actions do not match the prior run plan"])
    if gate_decision.get("admitted_receipt_action_ids") != prior_action_ids:
        raise CompileBlocked(["source gate did not admit the exact prior action set"])

    completed_wave_ids = next_state.get("completed_wave_ids")
    if (
        not isinstance(completed_wave_ids, list)
        or not completed_wave_ids
        or any(not isinstance(item, str) or not item for item in completed_wave_ids)
        or len(set(completed_wave_ids)) != len(completed_wave_ids)
    ):
        raise CompileBlocked(["next state has invalid completed_wave_ids"])
    if completed_wave_ids[-1] != source_wave_id:
        raise CompileBlocked(["next state does not append the source wave to completed history"])
    previous_completed = completed_wave_ids[:-1]
    source_dependencies = selected_wave.get("depends_on_waves", [])
    if not set(source_dependencies) <= set(previous_completed):
        raise CompileBlocked(["source wave dependencies are not completed"])

    next_wave_id = gate_decision.get("next_wave_id")
    action_set_actions = action_set.get("actions")
    if (
        not isinstance(next_wave_id, str)
        or not next_wave_id
        or action_set.get("next_wave_id") != next_wave_id
        or next_state.get("selected_wave_id") != next_wave_id
    ):
        raise CompileBlocked(["gate/action-set/state next-wave linkage mismatch"])
    if next_wave_id in completed_wave_ids or next_wave_id not in wave_by_id:
        raise CompileBlocked(["next wave is already completed or unknown"])
    if next_state.get("state") != "gate_pass" or next_state.get("validation_status") != "pass":
        raise CompileBlocked(["next state is not a validator-clean gate_pass frontier"])
    if next_state.get("authorization_status") != authorization or next_state.get("blockers"):
        raise CompileBlocked(["next state authorization or blockers do not permit planning"])
    next_wave = wave_by_id[next_wave_id]
    normalized_next_wave = _normalized_wave_plan(next_wave)
    if not set(normalized_next_wave["depends_on_waves"]) <= set(completed_wave_ids):
        raise CompileBlocked(["next wave dependencies are not completed"])
    eligible_wave = _next_eligible_wave(dispatch, completed_wave_ids)
    if not isinstance(eligible_wave, dict) or eligible_wave.get("wave_id") != next_wave_id:
        raise CompileBlocked(["next wave is not the route's next eligible wave"])

    if not isinstance(action_set_actions, list) or not action_set_actions:
        raise CompileBlocked(["next action set must contain actions"])
    if any(not isinstance(action, dict) for action in action_set_actions):
        raise CompileBlocked(["next action set contains a non-object action"])
    next_action_ids = [action.get("action_id") for action in action_set_actions]
    if any(not isinstance(item, str) or not item for item in next_action_ids):
        raise CompileBlocked(["next action set has invalid action identifiers"])
    if len(set(next_action_ids)) != len(next_action_ids):
        raise CompileBlocked(["next action set action identifiers must be unique"])
    if (
        gate_decision.get("next_action_ids") != next_action_ids
        or next_state.get("eligible_action_ids") != next_action_ids
    ):
        raise CompileBlocked(["gate/action-set/state next-action linkage mismatch"])
    if persisted_actions != action_set_actions:
        raise CompileBlocked(["persisted actions do not exactly match the next action set"])

    source_state = {
        "eligible_action_ids": prior_action_ids,
        "completed_wave_ids": previous_completed,
    }
    source_allocated_count = _validated_run_action_count(
        dispatch, source_state, prior_actions, source_wave_id
    )
    expected_source_actions = _compile_named_wave_actions(
        dispatch,
        run_id,
        source_wave_id,
        start_action_number=_action_count_for_waves(dispatch, previous_completed) + 1,
    )
    if prior_actions != expected_source_actions:
        raise CompileBlocked(["prior run-plan actions do not match route allocation"])
    expected_next_actions = _compile_named_wave_actions(
        dispatch,
        run_id,
        next_wave_id,
        start_action_number=source_allocated_count + 1,
    )
    if action_set_actions != expected_next_actions:
        raise CompileBlocked(["next actions do not match route allocation"])
    _validated_run_action_count(
        dispatch, next_state, action_set_actions, next_wave_id
    )

    return {
        "schema_version": RUN_PLAN_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "state": "wave_ready",
        "validation_status": "pass",
        "selected_wave": normalized_next_wave,
        "action_artifacts": [
            f"actions/{action_id}.json" for action_id in next_action_ids
        ],
        "actions": action_set_actions,
    }


def _receipt_shape_blockers(receipt: Any, index: int) -> list[str]:
    prefix = f"receipt[{index}]"
    if not isinstance(receipt, dict):
        return [f"{prefix}: receipt must be an object"]
    missing = sorted(RECEIPT_REQUIRED_FIELDS - set(receipt))
    blockers = [f"{prefix}: missing required field '{field}'" for field in missing]
    unexpected = sorted(set(receipt) - RECEIPT_REQUIRED_FIELDS)
    blockers.extend(
        f"{prefix}: unexpected field '{field}'" for field in unexpected
    )
    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        blockers.append(f"{prefix}: unsupported schema_version")
    for field in (
        "action_id",
        "dispatch_id",
        "run_id",
        "wave_id",
        "step_id",
        "role",
        "capability_ref",
        "agent_id",
        "started_at",
        "finished_at",
    ):
        if field in receipt and (not isinstance(receipt[field], str) or not receipt[field]):
            blockers.append(f"{prefix}: field '{field}' must be a non-empty string")
    if "status" in receipt and receipt.get("status") not in {"pass", "fail", "block", "timed_out"}:
        blockers.append(f"{prefix}: invalid status '{receipt.get('status')}'")
    if "validation" in receipt and receipt.get("validation") not in {"pass", "fail", "block"}:
        blockers.append(f"{prefix}: invalid validation '{receipt.get('validation')}'")
    for field in ("artifacts", "blockers"):
        if field in receipt and (
            not isinstance(receipt[field], list)
            or any(not isinstance(item, str) for item in receipt[field])
        ):
            blockers.append(f"{prefix}: field '{field}' must be an array of strings")
    return blockers


def _admit_receipts(
    expected_actions: list[dict[str, Any]], receipts: list[Any]
) -> tuple[list[dict[str, Any]], list[str]]:
    expected_by_id = {str(action["action_id"]): action for action in expected_actions}
    receipt_by_id: dict[str, dict[str, Any]] = {}
    blockers: list[str] = []

    for index, receipt in enumerate(receipts):
        shape_blockers = _receipt_shape_blockers(receipt, index)
        blockers.extend(shape_blockers)
        if shape_blockers:
            continue
        if not isinstance(receipt, dict) or not isinstance(receipt.get("action_id"), str):
            continue
        action_id = receipt["action_id"]
        if action_id in receipt_by_id:
            blockers.append(f"duplicate receipt for action '{action_id}'")
            continue
        if action_id not in expected_by_id:
            blockers.append(f"unexpected receipt for action '{action_id}'")
            continue
        receipt_by_id[action_id] = receipt

    admitted: list[dict[str, Any]] = []
    identity_fields = (
        "dispatch_id",
        "run_id",
        "wave_id",
        "step_id",
        "role",
        "capability_ref",
    )
    for action in expected_actions:
        action_id = str(action["action_id"])
        receipt = receipt_by_id.get(action_id)
        if receipt is None:
            blockers.append(f"missing receipt for action '{action_id}'")
            continue
        identity_blocked = False
        for field in identity_fields:
            if receipt.get(field) != action.get(field):
                blockers.append(
                    f"action '{action_id}': receipt {field} '{receipt.get(field)}' does not match '{action.get(field)}'"
                )
                identity_blocked = True
        if identity_blocked:
            continue
        admitted.append(receipt)
        if receipt.get("status") != "pass":
            blockers.append(f"action '{action_id}': non-pass status '{receipt.get('status')}'")
        if receipt.get("validation") != "pass":
            blockers.append(f"action '{action_id}': non-pass validation '{receipt.get('validation')}'")
        if receipt.get("blockers"):
            blockers.append(f"action '{action_id}': receipt declares blockers")

    return admitted, sorted(set(blockers))


def _next_eligible_wave(
    dispatch: dict[str, Any], completed_wave_ids: list[str]
) -> dict[str, Any] | None:
    strategy = dispatch.get("subagent_strategy")
    if not isinstance(strategy, dict):
        return None
    completed = set(completed_wave_ids)
    for wave in strategy.get("execution_waves", []) or []:
        if not isinstance(wave, dict):
            continue
        wave_id = str(wave.get("wave_id", ""))
        if wave_id in completed:
            continue
        dependencies = {str(item) for item in wave.get("depends_on_waves", []) or []}
        if dependencies <= completed:
            return wave
    return None


def reduce_wave_receipts(
    dispatch: dict[str, Any],
    state: dict[str, Any],
    run_plan: dict[str, Any],
    receipts: list[Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Reduce one wave's receipts into a gate decision and next action set."""

    dispatch_id = str(dispatch.get("dispatch_id", ""))
    run_id = str(state.get("run_id", ""))
    if state.get("dispatch_id") != dispatch_id or run_plan.get("dispatch_id") != dispatch_id:
        raise CompileBlocked(["state/run-plan dispatch identity mismatch"])
    if run_plan.get("run_id") != run_id:
        raise CompileBlocked(["state/run-plan run identity mismatch"])
    selected_wave = run_plan.get("selected_wave")
    actions = run_plan.get("actions")
    if not isinstance(selected_wave, dict) or not isinstance(actions, list) or not actions:
        raise CompileBlocked(["run plan must contain one selected wave and executable actions"])
    current_wave_id = str(selected_wave.get("wave_id", ""))
    if state.get("selected_wave_id") != current_wave_id:
        raise CompileBlocked(["state/run-plan selected wave mismatch"])
    allocated_action_count = _validated_run_action_count(
        dispatch, state, actions, current_wave_id
    )

    admitted, blockers = _admit_receipts(actions, receipts)
    strategy = dispatch.get("subagent_strategy") if isinstance(dispatch.get("subagent_strategy"), dict) else {}
    authorization = str(strategy.get("authorization", ""))
    previous_completed = [str(item) for item in state.get("completed_wave_ids", []) or []]
    gate_id = selected_wave.get("gate_after")

    next_actions: list[dict[str, Any]] = []
    next_wave_id: str | None = None
    if not blockers:
        completed_wave_ids = previous_completed + [current_wave_id]
        next_wave = _next_eligible_wave(dispatch, completed_wave_ids)
        if next_wave is not None:
            next_wave_id = str(next_wave.get("wave_id", ""))
            next_actions = _compile_named_wave_actions(
                dispatch,
                run_id,
                next_wave_id,
                start_action_number=allocated_action_count + 1,
            )
        decision = "gate_pass"
        next_state_name = "gate_pass" if next_wave_id else "complete"
        completed_for_state = completed_wave_ids
        selected_for_state = next_wave_id
    else:
        decision = "gate_block"
        next_state_name = "gate_block"
        completed_for_state = previous_completed
        selected_for_state = current_wave_id

    next_action_ids = [str(action["action_id"]) for action in next_actions]
    next_state = {
        "schema_version": STATE_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "state": next_state_name,
        "validation_status": "pass",
        "authorization_status": authorization,
        "selected_wave_id": selected_for_state,
        "eligible_action_ids": next_action_ids,
        "completed_wave_ids": completed_for_state,
        "blockers": blockers,
    }
    gate_decision = {
        "schema_version": GATE_DECISION_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "wave_id": current_wave_id,
        "gate_id": gate_id,
        "decision": decision,
        "required_action_ids": [str(action["action_id"]) for action in actions],
        "admitted_receipt_action_ids": [
            str(receipt["action_id"])
            for receipt in admitted
            if isinstance(receipt, dict) and receipt.get("action_id")
        ],
        "next_wave_id": next_wave_id,
        "next_action_ids": next_action_ids,
        "blockers": blockers,
    }
    action_set = {
        "schema_version": ACTION_SET_SCHEMA_VERSION,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "source_wave_id": current_wave_id,
        "source_gate_id": gate_id,
        "decision": decision,
        "next_wave_id": next_wave_id,
        "actions": next_actions,
    }
    return next_state, gate_decision, action_set


def _load_receipts_directory(receipts_dir: Path) -> list[Any]:
    if not receipts_dir.is_dir():
        return []
    receipts: list[Any] = []
    for receipt_path in sorted(receipts_dir.glob("*.json")):
        try:
            receipts.append(json.loads(receipt_path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as exc:
            receipts.append({"parse_error": f"{receipt_path.name}: {exc}"})
    return receipts


def reduce_to_directory(
    dispatch_path: Path,
    state_path: Path,
    run_plan_path: Path,
    receipts_dir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    _prepare_output_directory(output_dir)
    dispatch = _load_json(dispatch_path)
    state = _load_json(state_path)
    run_plan = _load_json(run_plan_path)
    receipts = _load_receipts_directory(receipts_dir)
    next_state, gate_decision, action_set = reduce_wave_receipts(dispatch, state, run_plan, receipts)
    _write_json(output_dir / "state.json", next_state)
    _write_json(output_dir / "gate-decision.json", gate_decision)
    _write_json(output_dir / "next-actions.json", action_set)
    for action in action_set["actions"]:
        _write_json(output_dir / "actions" / f"{action['action_id']}.json", action)
    return {
        "status": "pass",
        "state": next_state,
        "gate_decision": gate_decision,
        "action_set": action_set,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the first eligible native dispatch wave.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    compile_parser = subparsers.add_parser("compile", help="Validate and compile first-wave actions")
    compile_parser.add_argument("dispatch", type=Path)
    compile_parser.add_argument("--run-id", required=True)
    compile_parser.add_argument("--output-dir", required=True, type=Path)
    compile_parser.add_argument("--validator", type=Path)
    compile_parser.add_argument("--project-root", type=Path)
    verify_parser = subparsers.add_parser(
        "verify-registration", help="Verify exact-sheet registration before spawn"
    )
    verify_parser.add_argument("dispatch", type=Path)
    verify_parser.add_argument("--project-root", type=Path)
    close_parser = subparsers.add_parser(
        "verify-close", help="Verify the paired strategy close row after agent closeout"
    )
    close_parser.add_argument("dispatch", type=Path)
    close_parser.add_argument("--project-root", type=Path)
    digest_parser = subparsers.add_parser(
        "projection-digest", help="Compute the canonical executable strategy projection digest"
    )
    digest_parser.add_argument("dispatch", type=Path)
    reduce_parser = subparsers.add_parser("reduce", help="Reduce bound wave receipts into one gate decision")
    reduce_parser.add_argument("dispatch", type=Path)
    reduce_parser.add_argument("--state", required=True, type=Path)
    reduce_parser.add_argument("--run-plan", required=True, type=Path)
    reduce_parser.add_argument("--receipts-dir", required=True, type=Path)
    reduce_parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    try:
        if args.command == "compile":
            result = compile_to_directory(
                args.dispatch,
                args.run_id,
                args.output_dir,
                args.validator,
                args.project_root,
            )
        elif args.command == "projection-digest":
            dispatch = _load_json(args.dispatch)
            result = {
                "status": "pass",
                "execution_projection_sha256": strategy_execution_projection_sha256(dispatch),
                "projection": strategy_execution_projection(dispatch),
            }
        elif args.command == "reduce":
            result = reduce_to_directory(
                args.dispatch,
                args.state,
                args.run_plan,
                args.receipts_dir,
                args.output_dir,
            )
        else:
            dispatch = _load_json(args.dispatch)
            result = verify_strategy_registration(
                dispatch,
                args.dispatch,
                args.project_root,
                require_close=args.command == "verify-close",
            )
    except CompileBlocked as exc:
        print(json.dumps({"status": "block", "blockers": exc.blockers}, indent=2, sort_keys=True))
        return 2
    if args.command in {"verify-registration", "verify-close", "projection-digest"}:
        summary = result
    elif args.command == "compile":
        summary = {
            "status": result["status"],
            "state": result["state"]["state"],
            "run_plan": str(args.output_dir / "run-plan.json"),
            "action_count": len(result["run_plan"]["actions"]),
        }
    else:
        summary = {
            "status": result["status"],
            "state": result["state"]["state"],
            "decision": result["gate_decision"]["decision"],
            "next_action_count": len(result["action_set"]["actions"]),
            "gate_decision": str(args.output_dir / "gate-decision.json"),
        }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
