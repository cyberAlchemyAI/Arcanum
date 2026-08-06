#!/usr/bin/env python3
"""Deterministic, one-SWU Task Session governance runner.

The runner prepares a digest-chained ticket, joins one structured executor,
reconciles its staged evidence, and applies an explicitly journaled transaction.
Whole-run terminal closeout, owner hooks, continuation, and observation behavior
remain intentionally absent.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


PHASES = (
    "resolved",
    "governed",
    "admitted",
    "ticketed",
    "execution-received",
    "reconciled",
)
SELECTED_SWU = re.compile(
    r"^\|\s*`(?P<swu>SWU-[A-Z0-9-]+)`\s*\|.*\|\s*selected\s*\|\s*$",
    re.MULTILINE,
)


class RunnerBlock(ValueError):
    """A fail-closed runner outcome."""


class RunnerInterrupted(RuntimeError):
    """A synthetic transaction interruption used by the validation harness."""

    def __init__(self, boundary: str, writes_performed: int):
        super().__init__(f"synthetic interruption after {boundary}")
        self.boundary = boundary
        self.writes_performed = writes_performed


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def rendered_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RunnerBlock(f"cannot load {label}: {error}") from error
    if not isinstance(value, dict):
        raise RunnerBlock(f"{label} must be a JSON object")
    return value


def validate_schema(value: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise RunnerBlock(f"{label} schema invalid: {details}")


def normalized_relative(raw: str, label: str) -> str:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
        or ".." in path.parts
        or str(path) in ("", ".")
    ):
        raise RunnerBlock(f"{label} path escapes repository root: {raw}")
    return str(path)


def resolve_repo_path(repo_root: Path, raw: str, label: str) -> Path:
    normalized = normalized_relative(raw, label)
    root = repo_root.resolve()
    candidate = (root / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise RunnerBlock(f"{label} path escapes repository root: {raw}") from error
    return candidate


def relative_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as error:
        raise RunnerBlock(f"path is outside repository root: {path}") from error


def exact_ref(repo_root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": relative_path(repo_root, path),
        "sha256": sha256(data),
        "size_bytes": len(data),
    }


def read_exact_ref(
    repo_root: Path, reference: dict[str, Any], label: str
) -> tuple[Path, dict[str, Any]]:
    path = resolve_repo_path(repo_root, str(reference.get("path", "")), label)
    if not path.is_file():
        raise RunnerBlock(f"missing {label}: {reference.get('path')}")
    data = path.read_bytes()
    if sha256(data) != reference.get("sha256"):
        raise RunnerBlock(f"stale {label} digest: {reference.get('path')}")
    if len(data) != reference.get("size_bytes"):
        raise RunnerBlock(f"stale {label} size: {reference.get('path')}")
    return path, load_object(path, label)


def read_exact_bytes(
    repo_root: Path, reference: dict[str, Any], label: str
) -> tuple[Path, bytes]:
    path = resolve_repo_path(repo_root, str(reference.get("path", "")), label)
    if not path.is_file():
        raise RunnerBlock(f"missing {label}: {reference.get('path')}")
    data = path.read_bytes()
    if sha256(data) != reference.get("sha256"):
        raise RunnerBlock(f"stale {label} digest: {reference.get('path')}")
    if len(data) != reference.get("size_bytes"):
        raise RunnerBlock(f"stale {label} size: {reference.get('path')}")
    return path, data


def schema_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "schemas"


def selected_swu(work_pack_bytes: bytes) -> str:
    text = work_pack_bytes.decode("utf-8", errors="strict")
    selected = SELECTED_SWU.findall(text)
    if len(selected) != 1:
        raise RunnerBlock(
            f"work pack must contain exactly one selected SWU, observed {len(selected)}"
        )
    return selected[0]


def classify_controls(
    controls: list[tuple[dict[str, Any], dict[str, Any]]],
    task_id: str,
    swu_id: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any] | None,
]:
    evaluations: list[dict[str, Any]] = []
    admissions: list[dict[str, Any]] = []
    preflights: list[dict[str, Any]] = []
    executor_configs: list[dict[str, Any]] = []
    for reference, document in controls:
        if document.get("schema_version") == (
            "task-session.governance-evaluation-receipt.v1"
        ):
            evaluations.append(reference)
            if document.get("outcome") not in ("PROCEED", "PASS"):
                raise RunnerBlock("governance evaluator did not pass")
        if document.get("schemaVersion") == "1.2.0" and (
            "admissionVerdict" in document
        ):
            admissions.append(reference)
            if not (
                document.get("admissionVerdict") == "admit"
                and document.get("mutationReady") is True
                and document.get("taskId") == task_id
                and document.get("swuId") == swu_id
            ):
                raise RunnerBlock("mutation admission receipt did not admit this SWU")
        if document.get("schema_version") == "task-session.closeout-preflight.v1":
            preflights.append(reference)
            if not (
                document.get("result") == "PROCEED"
                and document.get("task_id") == task_id
                and document.get("swu_id") == swu_id
            ):
                raise RunnerBlock("closeout preflight did not proceed for this SWU")
        if document.get("schema_version") == "task-session.executor-launch-config.v1":
            executor_configs.append(document)
    if len(evaluations) != 1:
        raise RunnerBlock("exactly one governance evaluation receipt is required")
    if len(admissions) != 1:
        raise RunnerBlock("exactly one mutation admission receipt is required")
    if len(preflights) != 1:
        raise RunnerBlock("exactly one closeout preflight receipt is required")
    if len(executor_configs) > 1:
        raise RunnerBlock("at most one executor launch configuration is permitted")
    return (
        evaluations[0],
        admissions[0],
        preflights[0],
        executor_configs[0] if executor_configs else None,
    )


def executor_contract_from_config(
    repo_root: Path,
    request: dict[str, Any],
    run_dir: Path,
    config: dict[str, Any] | None,
) -> dict[str, Any]:
    if config is None:
        return {
            "owner_identity": {
                "capability": "implementation-executor",
                "subject": "unconfigured-until-swu-tsgr-004",
            },
            "argv": ["task-session-executor-not-configured"],
            "cwd": ".",
            "environment_names": [],
            "timeout_seconds": request["execution_contract"]["timeout_seconds"],
            "max_output_bytes": request["execution_contract"]["max_output_bytes"],
            "expected_receipt_path": (
                relative_path(repo_root, run_dir / "terminal-executor-receipt.json")
            ),
            "expected_receipt_schema_ref": exact_ref(
                repo_root, schema_dir() / "executor-receipt.schema.json"
            ),
        }
    expected = {
        "schema_version",
        "owner_identity",
        "argv",
        "cwd",
        "environment_names",
        "timeout_seconds",
        "max_output_bytes",
        "expected_receipt_path",
        "expected_receipt_schema_ref",
    }
    if set(config) != expected:
        raise RunnerBlock("executor launch configuration is not closed")
    if not (
        isinstance(config["argv"], list)
        and config["argv"]
        and all(isinstance(item, str) and item for item in config["argv"])
    ):
        raise RunnerBlock("executor argv must be a non-empty structured vector")
    executable = Path(config["argv"][0]).name.casefold()
    shell_switches = {"-c", "/c", "-command"}
    if executable in {
        "sh",
        "bash",
        "dash",
        "zsh",
        "fish",
        "cmd",
        "cmd.exe",
        "powershell",
        "powershell.exe",
        "pwsh",
    } and any(item.casefold() in shell_switches for item in config["argv"][1:]):
        raise RunnerBlock("executor argv may not invoke a shell command string")
    if config["cwd"] != ".":
        resolve_repo_path(repo_root, config["cwd"], "executor cwd")
    expected_path = resolve_repo_path(
        repo_root, config["expected_receipt_path"], "expected executor receipt"
    )
    if expected_path != (run_dir / "terminal-executor-receipt.json").resolve():
        raise RunnerBlock("executor receipt path must be the run-scoped terminal path")
    read_exact_bytes(
        repo_root,
        config["expected_receipt_schema_ref"],
        "executor receipt schema",
    )
    return {key: config[key] for key in expected if key != "schema_version"}


def baseline_inventory(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for raw in sorted(paths):
        path = resolve_repo_path(repo_root, raw, "allowed write")
        if path.is_file():
            data = path.read_bytes()
            inventory.append(
                {
                    "path": normalized_relative(raw, "allowed write"),
                    "state": "present",
                    "sha256": sha256(data),
                    "size_bytes": len(data),
                }
            )
        elif path.exists():
            raise RunnerBlock(f"allowed write is not a regular file: {raw}")
        else:
            inventory.append(
                {
                    "path": normalized_relative(raw, "allowed write"),
                    "state": "absent",
                    "sha256": None,
                    "size_bytes": None,
                }
            )
    return inventory


def execution_writes_fit_route_scope(
    route_scopes: list[str], execution_writes: list[str]
) -> bool:
    """Require an exact file delta that uses, and never escapes, route scope."""

    if not route_scopes or not execution_writes:
        return False
    scopes = [
        PurePosixPath(normalized_relative(item, "route write scope"))
        for item in route_scopes
    ]
    writes = [
        PurePosixPath(normalized_relative(item, "execution write"))
        for item in execution_writes
    ]

    def contains(scope: PurePosixPath, target: PurePosixPath) -> bool:
        return target == scope or scope in target.parents

    return all(any(contains(scope, target) for scope in scopes) for target in writes) and all(
        any(contains(scope, target) for target in writes) for scope in scopes
    )


def fast_execution_entry_contract(
    repo_root: Path,
    request: dict[str, Any],
) -> dict[str, Any] | None:
    if request.get("entry_profile") != "work-pack-fast-entry":
        return None
    profile = request["fast_execution_entry"]
    _, guard_request = read_exact_ref(
        repo_root, profile["request_ref"], "work-pack fast-entry request"
    )
    _, receipt = read_exact_ref(
        repo_root, profile["receipt_ref"], "work-pack fast-entry receipt"
    )
    module_path = Path(__file__).resolve().parent / "fast_execution_entry_guard.py"
    specification = importlib.util.spec_from_file_location(
        "task_session_fast_execution_entry_guard", module_path
    )
    if specification is None or specification.loader is None:
        raise RunnerBlock("cannot load Work Pack fast-entry validator")
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
        module.validate_fast_entry_receipt(receipt, guard_request)
    except (OSError, RuntimeError, ValueError) as error:
        raise RunnerBlock(f"Work Pack fast-entry validation failed: {error}") from error

    binding = guard_request["execution_binding"]
    route = binding["current_route"]
    selected = guard_request["selected_unit"]
    expected = (
        receipt.get("decision") == "proceed"
        and receipt.get("code") == "TASK_READY"
        and receipt.get("permitted_next_action") == "enter-context-builder"
        and receipt.get("entry_state") == "task-ready"
        and receipt.get("authorization_source") == "work-pack-binding"
        and receipt.get("authorization_prompt_required") is False
        and receipt.get("mutation_count") == 0
        and receipt.get("phase_trace", {}).get("owner_hops_dispatched") == 0
        and receipt.get("authority_effect") == "none"
        and guard_request["execution_policy"]["work_pack_id"]
        == request["work_pack_ref"]["path"]
        and selected["work_pack_id"] == request["work_pack_ref"]["path"]
        and selected["swu_id"] == request["swu_id"]
        and guard_request["execution_entry"]["selected_unit"] == request["swu_id"]
        and binding["selected_unit"] == request["swu_id"]
        and isinstance(route, dict)
        and route["frontier_swu"] == request["swu_id"]
        and route["capability"] == "task-session"
        and route["mode"] == "execute"
        and execution_writes_fit_route_scope(
            route["write_scope"], request["execution_contract"]["allowed_writes"]
        )
        and route["expected_receipt"]
        == request["closeout_contract"]["terminal_receipt_path"]
    )
    if not expected:
        raise RunnerBlock(
            "fast-entry request and receipt do not bind this governance route"
        )
    return {
        "request_ref": profile["request_ref"],
        "receipt_ref": profile["receipt_ref"],
        "binding_id": binding["binding_id"],
        "binding_digest": binding["binding_digest"],
        "route_fingerprint": binding["route_fingerprint"],
        "work_pack_semantic_digest": binding["work_pack_semantic_digest"],
    }


def plan_admission_contract(
    repo_root: Path,
    request: dict[str, Any],
    admission_ref: dict[str, Any],
    fast_entry: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if request.get("admission_profile") != "plan-once-selected-unit":
        return None
    plan = request["plan_admission"]
    if plan["attempt_id"] != request["run_id"]:
        raise RunnerBlock("plan admission attempt must equal the governance run id")
    if plan["mutation_admission_receipt_ref"] != admission_ref:
        raise RunnerBlock("plan admission receipt identity differs from admitted control")
    if admission_ref not in request["control_refs"]:
        raise RunnerBlock("mutation admission receipt is absent from control refs")
    if plan["selection_receipt_ref"] not in request["control_refs"]:
        raise RunnerBlock("selection receipt is absent from control refs")

    _, admission = read_exact_ref(
        repo_root, admission_ref, "plan mutation admission receipt"
    )
    _, selection = read_exact_ref(
        repo_root, plan["selection_receipt_ref"], "plan selection receipt"
    )
    expected = (
        admission.get("schemaVersion") == "1.2.0"
        and admission.get("admissionProfile") == "plan-once-selected-unit"
        and admission.get("admissionVerdict") == "admit"
        and admission.get("mutationReady") is True
        and admission.get("singleUse") is True
        and admission.get("taskId") == request["task_id"]
        and admission.get("swuId") == request["swu_id"]
        and admission.get("planEpochId") == plan["plan_epoch_id"]
        and admission.get("unitContractDigest") == plan["unit_contract_digest"]
        and admission.get("attemptId") == plan["attempt_id"]
        and admission.get("admissionToken") == plan["admission_token"]
        and admission.get("targetBaselineDigest")
        == plan["target_baseline_digest"]
        and admission.get("validationContractDigest")
        == plan["validation_contract_digest"]
        and admission.get("reasons") == []
    )
    if not expected:
        raise RunnerBlock("plan mutation admission does not bind this run")
    if not (
        selection.get("schemaVersion") == "1.0.0"
        and selection.get("selectionVerdict") == "select"
        and selection.get("terminalCode") == "SELECTION_READY"
        and selection.get("taskId") == request["task_id"]
        and selection.get("swuId") == request["swu_id"]
        and selection.get("planEpochId") == plan["plan_epoch_id"]
        and selection.get("unitContractDigest") == plan["unit_contract_digest"]
        and selection.get("mutationReady") is False
        and selection.get("authorityEffect") == "none"
    ):
        raise RunnerBlock("selection receipt does not bind this run")
    if fast_entry is not None:
        validate_schema(
            admission,
            load_object(
                schema_dir() / "mutation-admission-receipt.schema.json",
                "mutation admission receipt schema",
            ),
            "plan mutation admission receipt",
        )
        material_writes = sorted(admission.get("materialWrites", []))
        execution_outputs = sorted(admission.get("executionOutputs", []))
        allowed_writes = sorted(admission.get("allowedWrites", []))
        requested_writes = sorted(request["execution_contract"]["allowed_writes"])
        terminal_output = request["closeout_contract"]["terminal_receipt_path"]
        if material_writes != requested_writes:
            raise RunnerBlock(
                "fast-entry execution writes differ from plan material admission"
            )
        if execution_outputs != [terminal_output]:
            raise RunnerBlock(
                "fast-entry terminal output differs from plan execution admission"
            )
        if allowed_writes != sorted(material_writes + execution_outputs):
            raise RunnerBlock("fast-entry plan admission write closure is inconsistent")
        if admission.get("selectionReceiptDigest") != plan[
            "selection_receipt_ref"
        ]["sha256"]:
            raise RunnerBlock("plan admission selection receipt identity is stale")
        if not (
            selection.get("selectionIntentSource") == "execution-intent-binding"
            and selection.get("canonicalSemanticDigest")
            == fast_entry["work_pack_semantic_digest"]
        ):
            raise RunnerBlock(
                "fast-entry selection is not bound to the execution intent"
            )
    if sha256(canonical_bytes(request["execution_contract"]["validation_commands"])) != plan[
        "validation_contract_digest"
    ]:
        raise RunnerBlock("governance validation contract differs from plan admission")

    receipt_parent = PurePosixPath(admission_ref["path"]).parent
    ledger_relative = PurePosixPath(".admission-consumption") / (
        f"{admission_ref['sha256']}.json"
    )
    expected_ledger = (
        ledger_relative
        if str(receipt_parent) == "."
        else receipt_parent / ledger_relative
    ).as_posix()
    if plan["consumption_ledger_path"] != expected_ledger:
        raise RunnerBlock("admission consumption ledger path is not deterministic")

    raw_baselines = admission.get("targetBaselines")
    if not isinstance(raw_baselines, list) or not raw_baselines:
        raise RunnerBlock("plan admission receipt lacks target baselines")
    baselines = [
        {
            "path": item["path"],
            "state": item["state"],
            "sha256": item["sha256"],
            "size_bytes": item["sizeBytes"],
        }
        for item in raw_baselines
    ]
    if sha256(canonical_bytes(raw_baselines)) != plan["target_baseline_digest"]:
        raise RunnerBlock("plan target baseline digest is inconsistent")
    if fast_entry is not None and sorted(item["path"] for item in raw_baselines) != sorted(
        request["execution_contract"]["allowed_writes"]
    ):
        raise RunnerBlock("fast-entry plan baselines do not cover exact execution writes")
    return {**plan, "target_baselines": baselines}


def verify_plan_live_baselines(repo_root: Path, ticket: dict[str, Any]) -> None:
    if ticket.get("admission_profile") != "plan-once-selected-unit":
        return
    for baseline in ticket["plan_admission"]["target_baselines"]:
        target = resolve_repo_path(repo_root, baseline["path"], "plan target baseline")
        if baseline["state"] == "absent":
            if target.exists():
                raise RunnerBlock(
                    f"plan target baseline changed from absent: {baseline['path']}"
                )
            continue
        if not target.is_file():
            raise RunnerBlock(
                f"plan target baseline changed from present: {baseline['path']}"
            )
        content = target.read_bytes()
        if not (
            sha256(content) == baseline["sha256"]
            and len(content) == baseline["size_bytes"]
        ):
            raise RunnerBlock(f"plan target baseline drift: {baseline['path']}")


def consume_plan_admission(
    repo_root: Path, run_dir: Path, ticket: dict[str, Any]
) -> dict[str, Any] | None:
    if ticket.get("admission_profile") != "plan-once-selected-unit":
        return None
    plan = ticket["plan_admission"]
    ledger_path = resolve_repo_path(
        repo_root, plan["consumption_ledger_path"], "admission consumption ledger"
    )
    payload = {
        "schema_version": "task-session.admission-consumption.v1",
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "attempt_id": plan["attempt_id"],
        "admission_token": plan["admission_token"],
        "ticket_ref": exact_ref(repo_root, run_dir / "execution-ticket.json"),
        "mutation_admission_receipt_ref": plan[
            "mutation_admission_receipt_ref"
        ],
    }
    data = rendered_bytes(payload)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(
            ledger_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
    except FileExistsError:
        existing = load_object(ledger_path, "admission consumption ledger")
        if existing != payload:
            raise RunnerBlock("single-use admission receipt was already consumed")
    else:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    return exact_ref(repo_root, ledger_path)


def phase_receipt(
    *,
    request: dict[str, Any],
    phase: str,
    index: int,
    predecessor_phase: str,
    predecessor_ref: dict[str, Any],
    input_refs: list[dict[str, Any]],
    output_refs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "task-session.governance-phase-receipt.v1",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "phase": phase,
        "phase_index": index,
        "predecessor": {
            "phase": predecessor_phase,
            "receipt_ref": predecessor_ref,
        },
        "input_refs": input_refs,
        "result": "pass",
        "output_refs": output_refs,
        "owner_identity": request["owner_identity"],
        "idempotency_key": f"{request['idempotency_key']}:{phase}",
        "diagnostics": [],
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def json_pointer_value(document: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise RunnerBlock("satisfaction predicate must use an absolute JSON pointer")
    value = document
    try:
        for raw_part in pointer[1:].split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise RunnerBlock("owner receipt does not satisfy the declared JSON pointer") from error
    return value


def continuation_route_schema() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "continuation-router"
        / "schemas"
        / "continuation-route.schema.json"
    )


def verify_pre_execution_live_baselines(
    repo_root: Path, prerequisite: dict[str, Any]
) -> None:
    for baseline in prerequisite["target_inventory"]:
        target = resolve_repo_path(
            repo_root, baseline["path"], "pre-execution target baseline"
        )
        if baseline["state"] == "absent":
            if target.exists():
                raise RunnerBlock(
                    f"pre-execution target baseline changed from absent: {baseline['path']}"
                )
            continue
        if not target.is_file():
            raise RunnerBlock(
                f"pre-execution target baseline changed from present: {baseline['path']}"
            )
        data = target.read_bytes()
        if not (
            sha256(data) == baseline["sha256"]
            and len(data) == baseline["size_bytes"]
        ):
            raise RunnerBlock(
                f"pre-execution target baseline drift: {baseline['path']}"
            )


def validate_pre_execution_chain(
    repo_root: Path,
    request_path: Path,
    request: dict[str, Any],
) -> dict[str, Any]:
    if request.get("entry_profile") != "pre-execution-prerequisite":
        raise RunnerBlock("request does not select the pre-execution prerequisite profile")
    prerequisite = request["pre_execution_prerequisite"]
    if prerequisite["attempt_id"] != request["run_id"]:
        raise RunnerBlock("pre-execution attempt must equal the governance run id")

    _, classification = read_exact_ref(
        repo_root,
        prerequisite["classification_receipt_ref"],
        "pre-execution classification receipt",
    )
    validate_schema(
        classification,
        load_object(
            schema_dir() / "pre-execution-prerequisite-receipt.schema.json",
            "pre-execution classification receipt schema",
        ),
        "pre-execution classification receipt",
    )
    if not (
        classification["classification"] == "unmet"
        and classification["permitted_next_action"] == "route-one-owner-hop"
        and classification["authorization"]["status"] == "matched"
        and classification["task_id"] == request["task_id"]
        and classification["swu_id"] == request["swu_id"]
        and classification["attempt_id"] == request["run_id"]
        and classification["prerequisite_fingerprint"]
        == prerequisite["prerequisite_fingerprint"]
        and classification["phase_trace"]["context_builder_entered"] is False
        and classification["phase_trace"]["mutation_admission_entered"] is False
        and classification["phase_trace"]["implementation_inspected"] is False
        and classification["phase_trace"]["target_mutation_entered"] is False
        and classification["phase_trace"]["owner_hops_dispatched"] == 0
    ):
        raise RunnerBlock("classification receipt does not admit one prerequisite owner hop")

    _, route = read_exact_ref(
        repo_root,
        prerequisite["continuation_route_receipt_ref"],
        "pre-execution continuation route receipt",
    )
    validate_schema(
        route,
        load_object(continuation_route_schema(), "continuation route schema"),
        "pre-execution continuation route receipt",
    )
    context = route["source"]["pre_execution_context"]
    binding = route["authorization"]["binding"]
    handle = route["control_handle"]
    target_digest = sha256(canonical_bytes(prerequisite["target_inventory"]))
    validation_digest = sha256(
        canonical_bytes(request["execution_contract"]["validation_commands"])
    )
    predicate_digest = sha256(
        canonical_bytes(prerequisite["satisfaction_predicate"])
    )
    current_key = (
        f"{prerequisite['attempt_id']}:"
        f"{prerequisite['prerequisite_fingerprint']}"
    )
    expected_common = {
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "attempt_id": request["run_id"],
        "prerequisite_fingerprint": prerequisite["prerequisite_fingerprint"],
        "target_inventory_digest": target_digest,
        "validation_contract_digest": validation_digest,
        "satisfaction_predicate_digest": predicate_digest,
        "resume_point": prerequisite["resume_point"],
        "max_owner_hops": prerequisite["max_owner_hops"],
        "allowed_effect": prerequisite["allowed_effect"],
    }
    if not (
        route["schema_version"] == "arcanum.continuation_route.v2"
        and route["source"]["phase"] == "pre-execution-prerequisite"
        and route["source"]["capability"] == "task-session"
        and route["source"]["mode"] == "execute"
        and route["source"]["result"] == "unmet"
        and context["classification_receipt_ref"]
        == prerequisite["classification_receipt_ref"]
        and context["declared_owner_route"] == prerequisite["route"]
        and current_key not in context["consumed_attempt_fingerprints"]
        and route["authorization"]["requested"] is True
        and route["authorization"]["exact_route"] == prerequisite["route"]
        and binding["evidence_ref"]
        == classification["authorization"]["evidence_ref"]
        and route["selection"]["status"] == "selected"
        and route["selection"]["candidate_rank"] == 1
        and len(route["candidates"]) == 1
        and route["candidates"][0]["authorization_status"] == "matched"
        and route["dispatch"]["status"] == "completed"
        and route["dispatch"]["dispatch_count"] == 1
        and route["dispatch"]["join_count"] == 1
        and route["dispatch"]["join_validation"] == "pass"
        and route["dispatch"]["helper_closeout"] == "pass"
        and route["dispatch"]["router_mutations"] == []
        and route["dispatch"]["owner_receipt_ref"]
        == prerequisite["owner_receipt_ref"]
        and route["owner_boundary"] == "pass"
        and route["returned_next_route"] is None
        and handle["return_to"] == "task-session"
        and handle["mode"] == "resume-same-attempt"
        and handle["route"] == prerequisite["route"]
        and handle["owner_receipt_ref"] == prerequisite["owner_receipt_ref"]
    ):
        raise RunnerBlock("continuation route is not a joined one-hop prerequisite result")
    for field, expected in expected_common.items():
        if context.get(field) != expected:
            raise RunnerBlock(f"pre-execution route context mismatch: {field}")
        if binding.get(field) != expected:
            raise RunnerBlock(f"pre-execution authorization mismatch: {field}")
        if handle.get(field) != expected:
            raise RunnerBlock(f"pre-execution control handle mismatch: {field}")
    if binding.get("route") != prerequisite["route"]:
        raise RunnerBlock("pre-execution authorization route mismatch")

    owner_path, owner_receipt = read_exact_ref(
        repo_root,
        prerequisite["owner_receipt_ref"],
        "pre-execution owner receipt",
    )
    _, owner_schema_bytes = read_exact_bytes(
        repo_root,
        prerequisite["owner_receipt_schema_ref"],
        "pre-execution owner receipt schema",
    )
    try:
        owner_schema = json.loads(owner_schema_bytes)
    except json.JSONDecodeError as error:
        raise RunnerBlock("pre-execution owner receipt schema is invalid JSON") from error
    validate_schema(owner_receipt, owner_schema, "pre-execution owner receipt")
    expected_paths = sorted(item["path"] for item in prerequisite["target_inventory"])
    if not (
        owner_receipt.get("packageId") == prerequisite["expected_package_id"]
        and owner_receipt.get("packageDigest")
        == prerequisite["expected_package_digest"]
        and sorted(owner_receipt.get("validatedPaths", [])) == expected_paths
        and owner_receipt.get("validationCommands")
        == prerequisite["expected_owner_validation_commands"]
        and owner_receipt.get("patchVerdict") == "pass"
        and owner_receipt.get("mutationHandoff") == "ready"
        and owner_receipt.get("dependencyResult") == "pass"
        and owner_receipt.get("ownerBoundaryResult") == "pass"
        and owner_receipt.get("publicationBoundaryResult") == "pass"
        and owner_receipt.get("reasons") == []
    ):
        raise RunnerBlock("owner receipt package, scope, validation, or readiness mismatch")
    predicate = prerequisite["satisfaction_predicate"]
    if json_pointer_value(owner_receipt, predicate["receipt_pointer"]) not in predicate[
        "accepted_values"
    ]:
        raise RunnerBlock("owner receipt does not satisfy the prerequisite predicate")
    if owner_path.stat().st_size != prerequisite["owner_receipt_ref"]["size_bytes"]:
        raise RunnerBlock("owner receipt size changed during prerequisite validation")

    verify_pre_execution_live_baselines(repo_root, prerequisite)
    return {
        "request_ref": exact_ref(repo_root, request_path),
        "classification_receipt_ref": prerequisite["classification_receipt_ref"],
        "continuation_route_receipt_ref": prerequisite[
            "continuation_route_receipt_ref"
        ],
        "owner_receipt_ref": prerequisite["owner_receipt_ref"],
        "attempt_id": prerequisite["attempt_id"],
        "prerequisite_fingerprint": prerequisite["prerequisite_fingerprint"],
        "route": prerequisite["route"],
        "target_inventory_digest": target_digest,
        "validation_contract_digest": validation_digest,
        "satisfaction_predicate_digest": predicate_digest,
        "resume_point": prerequisite["resume_point"],
        "max_owner_hops": prerequisite["max_owner_hops"],
        "allowed_effect": prerequisite["allowed_effect"],
    }


def pre_execution_paths(
    repo_root: Path, run_dir: Path, prerequisite: dict[str, Any]
) -> tuple[Path, Path]:
    ledger = resolve_repo_path(
        repo_root,
        prerequisite["consumption_ledger_path"],
        "pre-execution consumption ledger",
    )
    receipt = resolve_repo_path(
        repo_root,
        prerequisite["resume_receipt_path"],
        "pre-execution resume receipt",
    )
    if ledger != (run_dir / "pre-execution-consumption.json").resolve():
        raise RunnerBlock("pre-execution consumption ledger path is not deterministic")
    if receipt != (run_dir / "pre-execution-resume-receipt.json").resolve():
        raise RunnerBlock("pre-execution resume receipt path is not deterministic")
    return ledger, receipt


def validate_pre_execution_resume(
    repo_root: Path,
    request_path: Path,
    request: dict[str, Any],
    run_dir: Path,
    chain: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prerequisite = request["pre_execution_prerequisite"]
    ledger_path, receipt_path = pre_execution_paths(repo_root, run_dir, prerequisite)
    if not receipt_path.is_file() or not ledger_path.is_file():
        raise RunnerBlock("pre-execution resume evidence is incomplete")
    chain = chain or validate_pre_execution_chain(repo_root, request_path, request)
    ledger = load_object(ledger_path, "pre-execution consumption ledger")
    ledger_ref = exact_ref(repo_root, ledger_path)
    receipt = load_object(receipt_path, "pre-execution resume receipt")
    expected_ledger = {
        "schema_version": "task-session.pre-execution-consumption.v1",
        **chain,
        "resume_receipt_path": relative_path(repo_root, receipt_path),
        "state": "consumed",
    }
    if ledger != expected_ledger:
        raise RunnerBlock("pre-execution consumption ledger identity mismatch")
    expected_receipt = {
        "schema_version": "task-session.pre-execution-resume-receipt.v1",
        "result": "pass",
        **chain,
        "consumption_ledger_ref": ledger_ref,
        "resume_count": 1,
        "selector_resolution_reentered": False,
        "context_builder_entry_budget": 1,
        "next_action": "context-builder",
    }
    if receipt != expected_receipt:
        raise RunnerBlock("pre-execution resume receipt identity mismatch")
    verify_pre_execution_live_baselines(repo_root, prerequisite)
    return receipt


def prerequisite_resume(
    repo_root: Path, request_path: Path, run_dir: Path
) -> dict[str, Any]:
    request = load_object(request_path, "governance run request")
    validate_schema(
        request,
        load_object(schema_dir() / "governance-run-request.schema.json", "request schema"),
        "governance run request",
    )
    chain = validate_pre_execution_chain(repo_root, request_path, request)
    prerequisite = request["pre_execution_prerequisite"]
    ledger_path, receipt_path = pre_execution_paths(repo_root, run_dir, prerequisite)
    if receipt_path.exists():
        receipt = validate_pre_execution_resume(
            repo_root, request_path, request, run_dir, chain
        )
        return {
            "schema_version": "task-session.governance-runner-status.v1",
            "result": "already-resumed",
            "run_id": request["run_id"],
            "task_id": request["task_id"],
            "swu_id": request["swu_id"],
            "resume_point": receipt["resume_point"],
            "resume_count": 1,
            "idempotent_replay": True,
            "context_builder_entry_budget": 0,
            "next_action": None,
            "writes_performed": 0,
        }
    if ledger_path.exists():
        raise RunnerBlock("pre-execution attempt/fingerprint is already or partially consumed")

    ledger = {
        "schema_version": "task-session.pre-execution-consumption.v1",
        **chain,
        "resume_receipt_path": relative_path(repo_root, receipt_path),
        "state": "consumed",
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(ledger_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise RunnerBlock(
            "pre-execution attempt/fingerprint was consumed concurrently"
        ) from error
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(rendered_bytes(ledger))
        handle.flush()
        os.fsync(handle.fileno())

    # Recheck after exclusive consumption and before authorizing Context Builder.
    verify_pre_execution_live_baselines(repo_root, prerequisite)
    receipt = {
        "schema_version": "task-session.pre-execution-resume-receipt.v1",
        "result": "pass",
        **chain,
        "consumption_ledger_ref": exact_ref(repo_root, ledger_path),
        "resume_count": 1,
        "selector_resolution_reentered": False,
        "context_builder_entry_budget": 1,
        "next_action": "context-builder",
    }
    atomic_write(receipt_path, rendered_bytes(receipt))
    return {
        "schema_version": "task-session.governance-runner-status.v1",
        "result": "pass",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "resume_point": prerequisite["resume_point"],
        "resume_count": 1,
        "idempotent_replay": False,
        "next_action": "context-builder",
        "writes_performed": 2,
    }


def checkpoint_paths(run_dir: Path) -> list[Path]:
    checkpoints = run_dir / "checkpoints"
    return [
        checkpoints / f"{index:02d}-{phase}.json"
        for index, phase in enumerate(PHASES, start=1)
    ]


def status_document(repo_root: Path, run_dir: Path) -> dict[str, Any]:
    if not run_dir.is_dir():
        raise RunnerBlock("run directory is missing")
    paths = checkpoint_paths(run_dir)
    observed = sorted((run_dir / "checkpoints").glob("*.json"))
    if observed != paths[: len(observed)] or not observed:
        raise RunnerBlock("checkpoint sequence is missing, unknown, or non-monotonic")

    previous_ref: dict[str, Any] | None = None
    current: dict[str, Any] | None = None
    for index, path in enumerate(observed, start=1):
        current = load_object(path, f"checkpoint {index}")
        validate_schema(
            current,
            load_object(
                schema_dir() / "governance-phase-receipt.schema.json",
                "phase receipt schema",
            ),
            f"checkpoint {index}",
        )
        if current["phase"] != PHASES[index - 1] or current["phase_index"] != index:
            raise RunnerBlock("checkpoint phase order is non-monotonic")
        if previous_ref is not None:
            if current["predecessor"]["receipt_ref"] != previous_ref:
                raise RunnerBlock("checkpoint predecessor digest chain is invalid")
        previous_ref = exact_ref(repo_root, path)

    assert current is not None
    if current["phase"] in ("ticketed", "execution-received", "reconciled"):
        ticket_path = run_dir / "execution-ticket.json"
        if not ticket_path.is_file():
            raise RunnerBlock("ticketed checkpoint is missing execution ticket")
        ticket = load_object(ticket_path, "execution ticket")
        validate_schema(
            ticket,
            load_object(schema_dir() / "execution-ticket.schema.json", "ticket schema"),
            "execution ticket",
        )
    if current["phase"] == "reconciled":
        reconciliation_path = run_dir / "reconciliation.json"
        if not reconciliation_path.is_file():
            raise RunnerBlock("reconciled checkpoint is missing reconciliation evidence")
        if current["output_refs"] != [exact_ref(repo_root, reconciliation_path)]:
            raise RunnerBlock("reconciled checkpoint output identity is stale")
    if current["phase"] == "ticketed":
        next_action = "executor-join"
    elif current["phase"] == "execution-received":
        next_action = "reconcile"
    elif current["phase"] == "reconciled":
        next_action = "commit-resume-not-implemented"
    else:
        next_action = f"resume-{PHASES[len(observed)]}"
    return {
        "schema_version": "task-session.governance-runner-status.v1",
        "result": "pass",
        "run_id": current["run_id"],
        "task_id": current["task_id"],
        "swu_id": current["swu_id"],
        "current_phase": current["phase"],
        "phase_index": current["phase_index"],
        "checkpoint_ref": exact_ref(repo_root, observed[-1]),
        "next_action": next_action,
        "writes_performed": 0,
    }


def prepare(repo_root: Path, request_path: Path, run_dir: Path) -> dict[str, Any]:
    if run_dir.exists() and any((run_dir / "checkpoints").glob("*.json")):
        status = status_document(repo_root, run_dir)
        request = load_object(request_path, "governance run request")
        ticket = load_object(run_dir / "execution-ticket.json", "execution ticket")
        if not (
            status["run_id"] == request.get("run_id")
            and status["swu_id"] == request.get("swu_id")
            and ticket.get("idempotency_key") == request.get("idempotency_key")
            and ticket.get("request_ref") == exact_ref(repo_root, request_path)
        ):
            raise RunnerBlock("existing run conflicts with request identity")
        status["idempotent_replay"] = True
        return status

    request = load_object(request_path, "governance run request")
    validate_schema(
        request,
        load_object(schema_dir() / "governance-run-request.schema.json", "request schema"),
        "governance run request",
    )
    request_ref = exact_ref(repo_root, request_path)
    pre_execution_resume = None
    fast_entry = fast_execution_entry_contract(repo_root, request)
    if request.get("entry_profile") == "pre-execution-prerequisite":
        pre_execution_resume = validate_pre_execution_resume(
            repo_root, request_path, request, run_dir
        )
        # Exact refs are re-read for drift only. The selected task/SWU identity
        # was already bound before atomic consumption; selector resolution is
        # intentionally not re-entered on this same-attempt resume.
        read_exact_bytes(repo_root, request["work_pack_ref"], "work pack")
        _, swu_bytes = read_exact_bytes(
            repo_root, request["swu_ref"], "SWU contract"
        )
        if request["swu_id"].encode("utf-8") not in swu_bytes:
            raise RunnerBlock("resumed SWU contract does not name requested SWU")
    elif fast_entry is not None:
        # The exact TASK_READY receipt replaces only the legacy prose selector.
        # Work Pack/SWU identity, governance controls, plan admission, baselines,
        # and atomic single-use consumption remain mandatory.
        read_exact_bytes(repo_root, request["work_pack_ref"], "work pack")
        _, swu_bytes = read_exact_bytes(
            repo_root, request["swu_ref"], "SWU contract"
        )
        if request["swu_id"].encode("utf-8") not in swu_bytes:
            raise RunnerBlock("fast-entry SWU contract does not name requested SWU")
    else:
        _, work_pack_bytes = read_exact_bytes(
            repo_root, request["work_pack_ref"], "work pack"
        )
        _, swu_bytes = read_exact_bytes(
            repo_root, request["swu_ref"], "SWU contract"
        )
        if request["swu_id"] != selected_swu(work_pack_bytes):
            raise RunnerBlock("requested SWU is not the unique selected work-pack SWU")
        if request["swu_id"].encode("utf-8") not in swu_bytes:
            raise RunnerBlock("SWU contract does not name requested SWU")

    controls: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for reference in request["control_refs"]:
        _, document = read_exact_ref(repo_root, reference, "control artifact")
        controls.append((reference, document))
    evaluation_ref, admission_ref, preflight_ref, executor_config = classify_controls(
        controls, request["task_id"], request["swu_id"]
    )
    plan_contract = plan_admission_contract(
        repo_root, request, admission_ref, fast_entry
    )
    baselines = baseline_inventory(
        repo_root, request["execution_contract"]["allowed_writes"]
    )

    executor_contract = executor_contract_from_config(
        repo_root, request, run_dir, executor_config
    )

    resolved_inputs = [request_ref, request["work_pack_ref"], request["swu_ref"]]
    if pre_execution_resume is not None:
        resolved_inputs.append(
            exact_ref(
                repo_root,
                resolve_repo_path(
                    repo_root,
                    request["pre_execution_prerequisite"]["resume_receipt_path"],
                    "pre-execution resume receipt",
                ),
            )
        )
    if fast_entry is not None:
        resolved_inputs.extend(
            [fast_entry["request_ref"], fast_entry["receipt_ref"]]
        )
    resolved = phase_receipt(
        request=request,
        phase="resolved",
        index=1,
        predecessor_phase="request",
        predecessor_ref=request_ref,
        input_refs=resolved_inputs,
        output_refs=[request["work_pack_ref"], request["swu_ref"]],
    )
    resolved_bytes = rendered_bytes(resolved)
    resolved_path = checkpoint_paths(run_dir)[0]
    resolved_ref = {
        "path": relative_path(repo_root, resolved_path),
        "sha256": sha256(resolved_bytes),
        "size_bytes": len(resolved_bytes),
    }

    governed = phase_receipt(
        request=request,
        phase="governed",
        index=2,
        predecessor_phase="resolved",
        predecessor_ref=resolved_ref,
        input_refs=[resolved_ref, evaluation_ref],
        output_refs=[evaluation_ref],
    )
    governed_bytes = rendered_bytes(governed)
    governed_path = checkpoint_paths(run_dir)[1]
    governed_ref = {
        "path": relative_path(repo_root, governed_path),
        "sha256": sha256(governed_bytes),
        "size_bytes": len(governed_bytes),
    }

    admitted = phase_receipt(
        request=request,
        phase="admitted",
        index=3,
        predecessor_phase="governed",
        predecessor_ref=governed_ref,
        input_refs=[governed_ref, admission_ref, preflight_ref],
        output_refs=[admission_ref, preflight_ref],
    )
    admitted_bytes = rendered_bytes(admitted)
    admitted_path = checkpoint_paths(run_dir)[2]
    admitted_ref = {
        "path": relative_path(repo_root, admitted_path),
        "sha256": sha256(admitted_bytes),
        "size_bytes": len(admitted_bytes),
    }

    ticket = {
        "schema_version": "task-session.execution-ticket.v1",
        "ticket_id": f"ticket:{request['run_id']}:{request['swu_id']}",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "request_ref": request_ref,
        "predecessor_ref": {"phase": "admitted", "receipt_ref": admitted_ref},
        "control_refs": request["control_refs"],
        "baseline_inventory": baselines,
        "allowed_writes": request["execution_contract"]["allowed_writes"],
        "declared_outputs": request["execution_contract"]["declared_outputs"],
        "validation_contracts": request["execution_contract"]["validation_commands"],
        "executor_contract": executor_contract,
        "owner_identity": request["owner_identity"],
        "idempotency_key": request["idempotency_key"],
        "closeout_contract": request["closeout_contract"],
    }
    if plan_contract is not None:
        ticket["admission_profile"] = "plan-once-selected-unit"
        ticket["plan_admission"] = plan_contract
    if fast_entry is not None:
        ticket["entry_profile"] = "work-pack-fast-entry"
        ticket["fast_execution_entry"] = fast_entry
    validate_schema(
        ticket,
        load_object(schema_dir() / "execution-ticket.schema.json", "ticket schema"),
        "execution ticket",
    )
    ticket_bytes = rendered_bytes(ticket)
    ticket_path = run_dir / "execution-ticket.json"
    ticket_ref = {
        "path": relative_path(repo_root, ticket_path),
        "sha256": sha256(ticket_bytes),
        "size_bytes": len(ticket_bytes),
    }

    ticketed = phase_receipt(
        request=request,
        phase="ticketed",
        index=4,
        predecessor_phase="admitted",
        predecessor_ref=admitted_ref,
        input_refs=[admitted_ref, ticket_ref],
        output_refs=[ticket_ref],
    )
    validate_schema(
        ticketed,
        load_object(
            schema_dir() / "governance-phase-receipt.schema.json",
            "phase receipt schema",
        ),
        "ticketed phase receipt",
    )
    ticketed_bytes = rendered_bytes(ticketed)

    # Every gate above completes before the first persistent run-state write.
    for path, data in (
        (resolved_path, resolved_bytes),
        (governed_path, governed_bytes),
        (admitted_path, admitted_bytes),
        (ticket_path, ticket_bytes),
        (checkpoint_paths(run_dir)[3], ticketed_bytes),
    ):
        atomic_write(path, data)
    result = status_document(repo_root, run_dir)
    if pre_execution_resume is not None:
        result["entry_profile"] = "pre-execution-prerequisite"
        result["resume_point"] = "task-session:context-build"
        result["resume_count"] = 1
        result["selector_resolution_reentered"] = False
        result["context_builder_entry_count"] = 1
    if fast_entry is not None:
        result["entry_profile"] = "work-pack-fast-entry"
        result["fast_entry_receipt_ref"] = fast_entry["receipt_ref"]
        result["selector_resolution_reentered"] = False
        result["context_builder_entry_count"] = 1
    return result


def execution_failure(
    ticket: dict[str, Any],
    reason: str,
    *,
    exit_code: int | None,
    stdout: bytes,
    stderr: bytes,
) -> dict[str, Any]:
    limit = ticket["executor_contract"]["max_output_bytes"]
    return {
        "schema_version": "task-session.governance-runner-execution.v1",
        "result": "execution-failed",
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "exit_code": exit_code,
        "diagnostics": [reason],
        "capture": {
            "max_output_bytes": limit,
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "stdout_truncated": len(stdout) > limit,
            "stderr_truncated": len(stderr) > limit,
        },
        "writes_performed": 0,
    }


def validate_executor_receipt(
    repo_root: Path,
    run_dir: Path,
    ticket: dict[str, Any],
    receipt_path: Path,
) -> dict[str, Any]:
    contract = ticket["executor_contract"]
    expected_path = resolve_repo_path(
        repo_root, contract["expected_receipt_path"], "expected executor receipt"
    )
    if receipt_path.resolve() != expected_path:
        raise RunnerBlock("joined executor receipt path differs from ticket")
    receipt = load_object(receipt_path, "executor receipt")
    _, schema_bytes = read_exact_bytes(
        repo_root,
        contract["expected_receipt_schema_ref"],
        "executor receipt schema",
    )
    schema = json.loads(schema_bytes)
    validate_schema(receipt, schema, "executor receipt")
    ticket_ref = exact_ref(repo_root, run_dir / "execution-ticket.json")
    for field in ("run_id", "task_id", "swu_id", "idempotency_key"):
        if receipt[field] != ticket[field]:
            raise RunnerBlock(f"executor receipt {field} identity mismatch")
    if receipt["ticket_ref"] != ticket_ref:
        raise RunnerBlock("executor receipt ticket identity mismatch")
    if receipt["owner_identity"] != contract["owner_identity"]:
        raise RunnerBlock("executor receipt owner identity mismatch")
    if receipt["terminal_sequence"]["receipt_path"] != contract[
        "expected_receipt_path"
    ]:
        raise RunnerBlock("executor terminal sequence path mismatch")

    receipt_mtime = receipt_path.stat().st_mtime_ns
    for raw in receipt["touched_files"]:
        target = resolve_repo_path(repo_root, raw, "executor touched file")
        if target.exists() and target.stat().st_mtime_ns > receipt_mtime:
            raise RunnerBlock("executor receipt was not the final executor write")
    for reference in receipt["outputs"]:
        output, _ = read_exact_bytes(repo_root, reference, "executor output")
        if output.stat().st_mtime_ns > receipt_mtime:
            raise RunnerBlock("executor receipt was not the final executor write")
    return receipt


def executor_join(
    repo_root: Path,
    run_dir: Path,
    joined_receipt: Path | None,
) -> dict[str, Any]:
    current = status_document(repo_root, run_dir)
    if current["current_phase"] == "execution-received":
        current["idempotent_replay"] = True
        return current
    if current["current_phase"] != "ticketed":
        raise RunnerBlock("executor join requires a ticketed checkpoint")

    ticket_path = run_dir / "execution-ticket.json"
    ticket = load_object(ticket_path, "execution ticket")
    contract = ticket["executor_contract"]
    expected_receipt = resolve_repo_path(
        repo_root, contract["expected_receipt_path"], "expected executor receipt"
    )
    if joined_receipt is not None and joined_receipt.resolve() != expected_receipt:
        raise RunnerBlock("explicit joined receipt differs from ticket path")

    if ticket.get("admission_profile") == "plan-once-selected-unit":
        verify_plan_live_baselines(repo_root, ticket)
        ledger_path = resolve_repo_path(
            repo_root,
            ticket["plan_admission"]["consumption_ledger_path"],
            "admission consumption ledger",
        )
        if (joined_receipt is not None or expected_receipt.is_file()) and not ledger_path.is_file():
            raise RunnerBlock(
                "pre-joined executor output bypassed single-use admission consumption"
            )
        consume_plan_admission(repo_root, run_dir, ticket)

    stdout = b""
    stderr = b""
    if joined_receipt is None and not expected_receipt.is_file():
        cwd = (
            repo_root
            if contract["cwd"] == "."
            else resolve_repo_path(repo_root, contract["cwd"], "executor cwd")
        )
        environment = {
            name: os.environ[name]
            for name in contract["environment_names"]
            if name in os.environ
        }
        try:
            completed = subprocess.run(
                contract["argv"],
                cwd=cwd,
                env=environment,
                shell=False,
                capture_output=True,
                timeout=contract["timeout_seconds"],
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            return execution_failure(
                ticket,
                "executor timeout",
                exit_code=None,
                stdout=error.stdout or b"",
                stderr=error.stderr or b"",
            )
        except OSError as error:
            return execution_failure(
                ticket,
                f"executor launch failed: {error}",
                exit_code=None,
                stdout=b"",
                stderr=b"",
            )
        stdout = completed.stdout
        stderr = completed.stderr
        if completed.returncode != 0:
            return execution_failure(
                ticket,
                "executor returned a nonzero exit status",
                exit_code=completed.returncode,
                stdout=stdout,
                stderr=stderr,
            )

    receipt = validate_executor_receipt(
        repo_root, run_dir, ticket, expected_receipt
    )
    if receipt["result"] != "pass":
        return execution_failure(
            ticket,
            f"executor receipt result is {receipt['result']}",
            exit_code=None,
            stdout=stdout,
            stderr=stderr,
        )
    if (
        len(stdout) > contract["max_output_bytes"]
        or len(stderr) > contract["max_output_bytes"]
    ):
        return execution_failure(
            ticket,
            "executor output exceeded bounded capture",
            exit_code=0,
            stdout=stdout,
            stderr=stderr,
        )

    ticketed_path = checkpoint_paths(run_dir)[3]
    ticketed_ref = exact_ref(repo_root, ticketed_path)
    receipt_ref = exact_ref(repo_root, expected_receipt)
    phase = phase_receipt(
        request={
            "run_id": ticket["run_id"],
            "task_id": ticket["task_id"],
            "swu_id": ticket["swu_id"],
            "owner_identity": ticket["owner_identity"],
            "idempotency_key": ticket["idempotency_key"],
        },
        phase="execution-received",
        index=5,
        predecessor_phase="ticketed",
        predecessor_ref=ticketed_ref,
        input_refs=[ticketed_ref, exact_ref(repo_root, ticket_path), receipt_ref],
        output_refs=[receipt_ref],
    )
    validate_schema(
        phase,
        load_object(
            schema_dir() / "governance-phase-receipt.schema.json",
            "phase receipt schema",
        ),
        "execution-received phase receipt",
    )
    atomic_write(checkpoint_paths(run_dir)[4], rendered_bytes(phase))
    result = status_document(repo_root, run_dir)
    result["writes_performed"] = 1
    return result


def require_closed_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    if set(value) != expected:
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        raise RunnerBlock(f"{label} is not closed: missing={missing} extra={extra}")


def validate_output_only_admission(
    repo_root: Path,
    reference: dict[str, Any],
    ticket: dict[str, Any],
) -> None:
    _, admission = read_exact_ref(
        repo_root, reference, "output-only mutation admission receipt"
    )
    expected_outputs = sorted(ticket["declared_outputs"])
    if not (
        admission.get("schemaVersion") == "1.2.0"
        and admission.get("executionMode") in ("routed-mutation", "reusable-mutation")
        and admission.get("writeProfile") == "execution-output-only"
        and admission.get("admissionVerdict") == "admit"
        and admission.get("mutationReady") is True
        and admission.get("taskId") == ticket["task_id"]
        and admission.get("swuId") == ticket["swu_id"]
        and admission.get("materialWrites") == []
        and sorted(admission.get("executionOutputs", [])) == expected_outputs
        and sorted(admission.get("allowedWrites", [])) == expected_outputs
        and admission.get("reasons") == []
    ):
        raise RunnerBlock(
            "explicit output-only re-admission does not admit the declared outputs"
        )


def validate_critical_results(
    ticket: dict[str, Any], executor_receipt: dict[str, Any]
) -> None:
    expected = {
        item["command_id"]: item for item in ticket["validation_contracts"]
    }
    if len(expected) != len(ticket["validation_contracts"]):
        raise RunnerBlock("validation contract contains duplicate command ids")
    received = {
        item["command_id"]: item for item in executor_receipt["validation_results"]
    }
    if len(received) != len(executor_receipt["validation_results"]):
        raise RunnerBlock("executor validation results contain duplicate command ids")
    if set(received) != set(expected):
        raise RunnerBlock("executor validation result inventory is missing or undeclared")
    for command_id, contract in expected.items():
        result = received[command_id]
        for key in ("argv", "cwd", "timeout_seconds", "max_output_bytes"):
            if result[key] != contract[key]:
                raise RunnerBlock(
                    f"critical validation {command_id} contract identity mismatch"
                )
        if result["exit_code"] != 0 or result["result"] != "pass":
            raise RunnerBlock(f"critical validation {command_id} did not pass")


def classify_candidate(
    repo_root: Path,
    target_path: str,
    output_ref: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    staged_path, staged_bytes = read_exact_bytes(
        repo_root, output_ref, f"staged output for {target_path}"
    )
    live_path = resolve_repo_path(repo_root, target_path, "reconciliation target")
    if live_path.is_file():
        live_bytes = live_path.read_bytes()
        live_identity = {
            "state": "present",
            "sha256": sha256(live_bytes),
            "size_bytes": len(live_bytes),
        }
    elif live_path.exists():
        raise RunnerBlock(f"reconciliation target is not a regular file: {target_path}")
    else:
        live_identity = {"state": "absent", "sha256": None, "size_bytes": None}

    staged_identity = {
        "sha256": sha256(staged_bytes),
        "size_bytes": len(staged_bytes),
    }
    if (
        live_identity["state"] == "present"
        and live_identity["sha256"] == staged_identity["sha256"]
        and live_identity["size_bytes"] == staged_identity["size_bytes"]
    ):
        classification = "already-present-exact-output"
    elif (
        live_identity["state"] == baseline["state"]
        and live_identity["sha256"] == baseline["sha256"]
        and live_identity["size_bytes"] == baseline["size_bytes"]
    ):
        classification = "apply"
    else:
        classification = "conflict"
    return {
        "target_path": target_path,
        "output_ref": output_ref,
        "baseline": {
            "state": baseline["state"],
            "sha256": baseline["sha256"],
            "size_bytes": baseline["size_bytes"],
        },
        "live": live_identity,
        "classification": classification,
    }


def reconcile(
    repo_root: Path,
    run_dir: Path,
    output_only_admission_path: Path,
) -> dict[str, Any]:
    current = status_document(repo_root, run_dir)
    if current["current_phase"] == "reconciled":
        evidence = load_object(run_dir / "reconciliation.json", "reconciliation evidence")
        if evidence.get("output_only_admission_ref") != exact_ref(
            repo_root, output_only_admission_path
        ):
            raise RunnerBlock(
                "existing reconciliation conflicts with output-only admission"
            )
        current["idempotent_replay"] = True
        return current
    if current["current_phase"] != "execution-received":
        raise RunnerBlock("reconcile requires an execution-received checkpoint")

    ticket_path = run_dir / "execution-ticket.json"
    ticket = load_object(ticket_path, "execution ticket")
    ticket_ref = exact_ref(repo_root, ticket_path)

    expected_receipt_path = resolve_repo_path(
        repo_root,
        ticket["executor_contract"]["expected_receipt_path"],
        "expected executor receipt",
    )
    executor_receipt = validate_executor_receipt(
        repo_root, run_dir, ticket, expected_receipt_path
    )
    executor_receipt_ref = exact_ref(repo_root, expected_receipt_path)
    execution_received = load_object(
        checkpoint_paths(run_dir)[4], "execution-received checkpoint"
    )
    if execution_received["output_refs"] != [executor_receipt_ref]:
        raise RunnerBlock("execution-received checkpoint output identity is stale")
    if executor_receipt["result"] != "pass":
        raise RunnerBlock("executor receipt is not a passing reconciliation input")

    admission_ref = exact_ref(repo_root, output_only_admission_path)
    validate_output_only_admission(
        repo_root, admission_ref, ticket
    )
    validate_critical_results(ticket, executor_receipt)

    allowed_targets = ticket["allowed_writes"]
    declared_outputs = ticket["declared_outputs"]
    received_touches = executor_receipt["touched_files"]
    received_outputs = executor_receipt["outputs"]
    if received_touches != declared_outputs:
        raise RunnerBlock("executor touched inventory is missing, reordered, or undeclared")
    if [item["path"] for item in received_outputs] != declared_outputs:
        raise RunnerBlock("executor output inventory is missing, reordered, or undeclared")
    if len(allowed_targets) != len(received_outputs):
        raise RunnerBlock("executor target/output mapping cardinality mismatch")

    baseline_by_target = {
        item["path"]: item for item in ticket["baseline_inventory"]
    }
    if set(baseline_by_target) != set(allowed_targets):
        raise RunnerBlock("ticket baseline inventory does not cover every target")

    classifications = [
        classify_candidate(
            repo_root,
            target,
            output_ref,
            baseline_by_target[target],
        )
        for target, output_ref in zip(
            allowed_targets, received_outputs, strict=True
        )
    ]
    conflicts = [
        item["target_path"]
        for item in classifications
        if item["classification"] == "conflict"
    ]
    if conflicts:
        raise RunnerBlock(
            "reconciliation target conflict: " + ", ".join(conflicts)
        )

    evidence = {
        "schema_version": "task-session.reconciliation-evidence.v1",
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "ticket_ref": ticket_ref,
        "executor_receipt_ref": executor_receipt_ref,
        "output_only_admission_ref": admission_ref,
        "mapping_policy": "positional-target-to-output-v1",
        "classifications": classifications,
        "critical_validation_ids": sorted(
            item["command_id"] for item in ticket["validation_contracts"]
        ),
        "live_apply_performed": False,
        "result": "pass",
    }
    evidence_bytes = rendered_bytes(evidence)
    evidence_path = run_dir / "reconciliation.json"
    evidence_ref = {
        "path": relative_path(repo_root, evidence_path),
        "sha256": sha256(evidence_bytes),
        "size_bytes": len(evidence_bytes),
    }
    execution_received_path = checkpoint_paths(run_dir)[4]
    execution_received_ref = exact_ref(repo_root, execution_received_path)
    phase = phase_receipt(
        request={
            "run_id": ticket["run_id"],
            "task_id": ticket["task_id"],
            "swu_id": ticket["swu_id"],
            "owner_identity": ticket["owner_identity"],
            "idempotency_key": ticket["idempotency_key"],
        },
        phase="reconciled",
        index=6,
        predecessor_phase="execution-received",
        predecessor_ref=execution_received_ref,
        input_refs=[
            execution_received_ref,
            ticket_ref,
            executor_receipt_ref,
            admission_ref,
        ],
        output_refs=[evidence_ref],
    )
    validate_schema(
        phase,
        load_object(
            schema_dir() / "governance-phase-receipt.schema.json",
            "phase receipt schema",
        ),
        "reconciled phase receipt",
    )
    atomic_write(evidence_path, evidence_bytes)
    atomic_write(checkpoint_paths(run_dir)[5], rendered_bytes(phase))
    result = status_document(repo_root, run_dir)
    result["writes_performed"] = 2
    result["classifications"] = {
        item["target_path"]: item["classification"] for item in classifications
    }
    result["live_apply_performed"] = False
    return result


def file_state(path: Path) -> dict[str, Any]:
    if path.is_file():
        data = path.read_bytes()
        return {
            "state": "present",
            "sha256": sha256(data),
            "size_bytes": len(data),
        }
    if path.exists():
        raise RunnerBlock(f"transaction target is not a regular file: {path}")
    return {"state": "absent", "sha256": None, "size_bytes": None}


def state_matches(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return all(left.get(key) == right.get(key) for key in (
        "state", "sha256", "size_bytes"
    ))


def transaction_plan(
    repo_root: Path,
    run_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    status = status_document(repo_root, run_dir)
    if status["current_phase"] != "reconciled":
        raise RunnerBlock("commit-resume requires a reconciled checkpoint")
    ticket_path = run_dir / "execution-ticket.json"
    reconciliation_path = run_dir / "reconciliation.json"
    ticket = load_object(ticket_path, "execution ticket")
    reconciliation = load_object(reconciliation_path, "reconciliation evidence")
    ticket_ref = exact_ref(repo_root, ticket_path)
    reconciliation_ref = exact_ref(repo_root, reconciliation_path)
    require_closed_keys(
        reconciliation,
        {
            "schema_version",
            "run_id",
            "task_id",
            "swu_id",
            "ticket_ref",
            "executor_receipt_ref",
            "output_only_admission_ref",
            "mapping_policy",
            "classifications",
            "critical_validation_ids",
            "live_apply_performed",
            "result",
        },
        "reconciliation evidence",
    )
    if not (
        reconciliation["schema_version"]
        == "task-session.reconciliation-evidence.v1"
        and reconciliation["ticket_ref"] == ticket_ref
        and reconciliation["mapping_policy"] == "positional-target-to-output-v1"
        and reconciliation["live_apply_performed"] is False
        and reconciliation["result"] == "pass"
    ):
        raise RunnerBlock("reconciliation evidence is not an admissible commit input")
    for key in ("run_id", "task_id", "swu_id"):
        if reconciliation[key] != ticket[key]:
            raise RunnerBlock(f"reconciliation {key} identity mismatch")
    if len(reconciliation["classifications"]) != len(ticket["allowed_writes"]):
        raise RunnerBlock("reconciliation classification cardinality mismatch")

    targets: list[dict[str, Any]] = []
    for index, (target_path, classification) in enumerate(
        zip(
            ticket["allowed_writes"],
            reconciliation["classifications"],
            strict=True,
        )
    ):
        require_closed_keys(
            classification,
            {"target_path", "output_ref", "baseline", "live", "classification"},
            f"reconciliation classification {index}",
        )
        if classification["target_path"] != target_path:
            raise RunnerBlock("reconciliation target order differs from ticket")
        if classification["classification"] not in (
            "apply",
            "already-present-exact-output",
        ):
            raise RunnerBlock("reconciliation contains a non-committable classification")
        _, output_bytes = read_exact_bytes(
            repo_root,
            classification["output_ref"],
            f"transaction output for {target_path}",
        )
        output_state = {
            "state": "present",
            "sha256": sha256(output_bytes),
            "size_bytes": len(output_bytes),
        }
        targets.append(
            {
                "index": index,
                "target_path": target_path,
                "output_ref": classification["output_ref"],
                "output_state": output_state,
                "baseline": classification["baseline"],
                "classification": classification["classification"],
            }
        )
    identity = {
        "ticket_ref": ticket_ref,
        "reconciliation_ref": reconciliation_ref,
        "idempotency_key": ticket["idempotency_key"],
        "targets": targets,
    }
    identity["transaction_id"] = "transaction:" + sha256(canonical_bytes(identity))
    return ticket, reconciliation, identity, targets


def initial_journal(
    ticket: dict[str, Any],
    identity: dict[str, Any],
    targets: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "task-session.commit-journal.v1",
        "transaction_id": identity["transaction_id"],
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "idempotency_key": ticket["idempotency_key"],
        "ticket_ref": identity["ticket_ref"],
        "reconciliation_ref": identity["reconciliation_ref"],
        "state": "applying",
        "next_index": 0,
        "targets": [
            {
                "index": item["index"],
                "target_path": item["target_path"],
                "output_ref": item["output_ref"],
                "baseline": item["baseline"],
                "classification": item["classification"],
                "outcome": "pending",
            }
            for item in targets
        ],
    }


def validate_journal(
    journal: dict[str, Any],
    expected: dict[str, Any],
    ticket: dict[str, Any],
    targets: list[dict[str, Any]],
) -> None:
    require_closed_keys(
        journal,
        {
            "schema_version",
            "transaction_id",
            "run_id",
            "task_id",
            "swu_id",
            "idempotency_key",
            "ticket_ref",
            "reconciliation_ref",
            "state",
            "next_index",
            "targets",
        },
        "commit journal",
    )
    if journal["schema_version"] != "task-session.commit-journal.v1":
        raise RunnerBlock("commit journal schema version mismatch")
    for key in (
        "transaction_id",
        "ticket_ref",
        "reconciliation_ref",
        "idempotency_key",
    ):
        if journal[key] != expected[key]:
            raise RunnerBlock(f"commit journal {key} mismatch")
    for key in ("run_id", "task_id", "swu_id"):
        if journal[key] != ticket[key]:
            raise RunnerBlock(f"commit journal {key} mismatch")
    if journal["state"] not in ("applying", "committed"):
        raise RunnerBlock("commit journal state is invalid")
    if not isinstance(journal["next_index"], int) or not (
        0 <= journal["next_index"] <= len(targets)
    ):
        raise RunnerBlock("commit journal next index is invalid")
    if len(journal["targets"]) != len(targets):
        raise RunnerBlock("commit journal target cardinality mismatch")
    for observed, item in zip(journal["targets"], targets, strict=True):
        require_closed_keys(
            observed,
            {
                "index",
                "target_path",
                "output_ref",
                "baseline",
                "classification",
                "outcome",
            },
            "commit journal target",
        )
        for key in (
            "index",
            "target_path",
            "output_ref",
            "baseline",
            "classification",
        ):
            if observed[key] != item[key]:
                raise RunnerBlock(f"commit journal target {key} mismatch")
        if observed["outcome"] not in (
            "pending",
            "applied",
            "already-present-exact-output",
        ):
            raise RunnerBlock("commit journal target outcome is invalid")
        completed = observed["index"] < journal["next_index"]
        if completed == (observed["outcome"] == "pending"):
            raise RunnerBlock("commit journal progress is non-monotonic")
    if journal["state"] == "committed" and journal["next_index"] != len(targets):
        raise RunnerBlock("committed journal does not cover every target")


def commit_receipt_document(
    repo_root: Path,
    run_dir: Path,
    ticket: dict[str, Any],
    identity: dict[str, Any],
    journal: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "task-session.commit-receipt.v1",
        "receipt_id": f"commit-receipt:{identity['transaction_id']}",
        "transaction_id": identity["transaction_id"],
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "idempotency_key": ticket["idempotency_key"],
        "ticket_ref": identity["ticket_ref"],
        "reconciliation_ref": identity["reconciliation_ref"],
        "journal_ref": exact_ref(repo_root, run_dir / "commit-journal.json"),
        "target_results": [
            {
                "target_path": item["target_path"],
                "output_ref": item["output_ref"],
                "classification": item["classification"],
                "outcome": item["outcome"],
            }
            for item in journal["targets"]
        ],
        "result": "pass",
        "final_transaction_write": True,
        "authority_ceiling": "transaction-committed-not-whole-run-terminal",
        "residue": [
            (
                "Canonical whole-run terminal receipt requires later closeout and "
                "observation phases; this commit receipt does not claim them."
            )
        ],
    }


def validate_commit_receipt(
    repo_root: Path,
    run_dir: Path,
    receipt: dict[str, Any],
    ticket: dict[str, Any],
    identity: dict[str, Any],
    targets: list[dict[str, Any]],
) -> None:
    require_closed_keys(
        receipt,
        {
            "schema_version",
            "receipt_id",
            "transaction_id",
            "run_id",
            "task_id",
            "swu_id",
            "idempotency_key",
            "ticket_ref",
            "reconciliation_ref",
            "journal_ref",
            "target_results",
            "result",
            "final_transaction_write",
            "authority_ceiling",
            "residue",
        },
        "commit receipt",
    )
    if not (
        receipt["schema_version"] == "task-session.commit-receipt.v1"
        and receipt["transaction_id"] == identity["transaction_id"]
        and receipt["idempotency_key"] == ticket["idempotency_key"]
        and receipt["ticket_ref"] == identity["ticket_ref"]
        and receipt["reconciliation_ref"] == identity["reconciliation_ref"]
        and receipt["result"] == "pass"
        and receipt["final_transaction_write"] is True
        and receipt["authority_ceiling"]
        == "transaction-committed-not-whole-run-terminal"
    ):
        raise RunnerBlock("commit receipt identity or terminal claim mismatch")
    for key in ("run_id", "task_id", "swu_id"):
        if receipt[key] != ticket[key]:
            raise RunnerBlock(f"commit receipt {key} mismatch")
    journal_path = run_dir / "commit-journal.json"
    if receipt["journal_ref"] != exact_ref(repo_root, journal_path):
        raise RunnerBlock("commit receipt journal identity is stale")
    journal = load_object(journal_path, "commit journal")
    validate_journal(journal, identity, ticket, targets)
    if journal["state"] != "committed":
        raise RunnerBlock("commit receipt refers to an incomplete journal")
    expected_receipt = commit_receipt_document(
        repo_root, run_dir, ticket, identity, journal
    )
    if receipt != expected_receipt:
        raise RunnerBlock("commit receipt content mismatch")
    receipt_path = run_dir / "commit-receipt.json"
    receipt_mtime = receipt_path.stat().st_mtime_ns
    if journal_path.stat().st_mtime_ns > receipt_mtime:
        raise RunnerBlock("commit receipt was not the final transaction write")
    for item in targets:
        target = resolve_repo_path(
            repo_root, item["target_path"], "committed target"
        )
        if not state_matches(file_state(target), item["output_state"]):
            raise RunnerBlock("committed target no longer matches staged output")
        if target.stat().st_mtime_ns > receipt_mtime:
            raise RunnerBlock("commit receipt was not the final transaction write")


def maybe_interrupt(
    requested: str | None,
    observed: str,
    writes_performed: int,
) -> None:
    if requested == observed:
        raise RunnerInterrupted(observed, writes_performed)


def commit_resume(
    repo_root: Path,
    run_dir: Path,
    interrupt_after: str | None,
) -> dict[str, Any]:
    ticket, _, identity, targets = transaction_plan(repo_root, run_dir)
    journal_path = run_dir / "commit-journal.json"
    receipt_path = run_dir / "commit-receipt.json"
    if receipt_path.exists():
        receipt = load_object(receipt_path, "commit receipt")
        validate_commit_receipt(
            repo_root, run_dir, receipt, ticket, identity, targets
        )
        return {
            "schema_version": "task-session.governance-runner-status.v1",
            "result": "pass",
            "run_id": ticket["run_id"],
            "task_id": ticket["task_id"],
            "swu_id": ticket["swu_id"],
            "current_phase": "reconciled",
            "phase_index": 6,
            "transaction_state": "committed",
            "commit_receipt_ref": exact_ref(repo_root, receipt_path),
            "next_action": "owner-hooks-not-implemented",
            "idempotent_replay": True,
            "writes_performed": 0,
        }

    writes_performed = 0
    if journal_path.exists():
        journal = load_object(journal_path, "commit journal")
        validate_journal(journal, identity, ticket, targets)
    else:
        journal = initial_journal(ticket, identity, targets)
        atomic_write(journal_path, rendered_bytes(journal))
        writes_performed += 1
        maybe_interrupt(interrupt_after, "journal-created", writes_performed)

    if journal["state"] == "committed":
        for item in targets:
            target = resolve_repo_path(
                repo_root, item["target_path"], "committed target"
            )
            if not state_matches(file_state(target), item["output_state"]):
                raise RunnerBlock("finalized transaction target state drifted")
    else:
        # Scan the complete transaction before advancing its journal.  This makes
        # an impossible mixed state a write-free block even when a prior crash
        # left a recoverable applied prefix.
        for index, item in enumerate(targets):
            target = resolve_repo_path(
                repo_root, item["target_path"], "transaction target"
            )
            observed = file_state(target)
            if index < journal["next_index"]:
                admissible = state_matches(observed, item["output_state"])
            else:
                admissible = state_matches(observed, item["output_state"]) or (
                    item["classification"] == "apply"
                    and state_matches(observed, item["baseline"])
                )
            if not admissible:
                raise RunnerBlock(
                    f"transaction target state conflict: {item['target_path']}"
                )
        for index, item in enumerate(targets):
            target = resolve_repo_path(
                repo_root, item["target_path"], "transaction target"
            )
            observed = file_state(target)
            if index < journal["next_index"]:
                if not state_matches(observed, item["output_state"]):
                    raise RunnerBlock("completed transaction target state drifted")
                continue
            if state_matches(observed, item["output_state"]):
                outcome = (
                    "already-present-exact-output"
                    if item["classification"] == "already-present-exact-output"
                    else "applied"
                )
            elif (
                item["classification"] == "apply"
                and state_matches(observed, item["baseline"])
            ):
                _, output_bytes = read_exact_bytes(
                    repo_root,
                    item["output_ref"],
                    f"transaction output for {item['target_path']}",
                )
                atomic_write(target, output_bytes)
                writes_performed += 1
                maybe_interrupt(
                    interrupt_after, f"target-{index + 1}", writes_performed
                )
                outcome = "applied"
            else:
                raise RunnerBlock(
                    f"transaction target state conflict: {item['target_path']}"
                )
            journal["targets"][index]["outcome"] = outcome
            journal["next_index"] = index + 1
            atomic_write(journal_path, rendered_bytes(journal))
            writes_performed += 1

        journal["state"] = "committed"
        atomic_write(journal_path, rendered_bytes(journal))
        writes_performed += 1
        maybe_interrupt(interrupt_after, "journal-finalized", writes_performed)

    receipt = commit_receipt_document(
        repo_root, run_dir, ticket, identity, journal
    )
    atomic_write(receipt_path, rendered_bytes(receipt))
    writes_performed += 1
    maybe_interrupt(interrupt_after, "commit-receipt", writes_performed)
    validate_commit_receipt(
        repo_root, run_dir, receipt, ticket, identity, targets
    )
    return {
        "schema_version": "task-session.governance-runner-status.v1",
        "result": "pass",
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "current_phase": "reconciled",
        "phase_index": 6,
        "transaction_state": "committed",
        "commit_receipt_ref": exact_ref(repo_root, receipt_path),
        "next_action": "owner-hooks-not-implemented",
        "writes_performed": writes_performed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--repo-root", required=True)
    prepare_parser.add_argument("--request", required=True)
    prepare_parser.add_argument("--run-dir", required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--repo-root", required=True)
    status_parser.add_argument("--run-dir", required=True)
    executor_parser = subparsers.add_parser("executor-join")
    executor_parser.add_argument("--repo-root", required=True)
    executor_parser.add_argument("--run-dir", required=True)
    executor_parser.add_argument("--receipt")
    reconcile_parser = subparsers.add_parser("reconcile")
    reconcile_parser.add_argument("--repo-root", required=True)
    reconcile_parser.add_argument("--run-dir", required=True)
    reconcile_parser.add_argument("--output-only-admission", required=True)
    commit_parser = subparsers.add_parser("commit-resume")
    commit_parser.add_argument("--repo-root", required=True)
    commit_parser.add_argument("--run-dir", required=True)
    commit_parser.add_argument("--interrupt-after")
    prerequisite_parser = subparsers.add_parser("prerequisite-resume")
    prerequisite_parser.add_argument("--repo-root", required=True)
    prerequisite_parser.add_argument("--request", required=True)
    prerequisite_parser.add_argument("--run-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = Path(args.repo_root).resolve()
        if not repo_root.is_dir():
            raise RunnerBlock("repository root is missing")
        run_dir = resolve_repo_path(repo_root, args.run_dir, "run directory")
        if args.command == "prepare":
            request_path = resolve_repo_path(repo_root, args.request, "request")
            result = prepare(repo_root, request_path, run_dir)
        elif args.command == "prerequisite-resume":
            request_path = resolve_repo_path(repo_root, args.request, "request")
            result = prerequisite_resume(repo_root, request_path, run_dir)
        elif args.command == "executor-join":
            receipt_path = (
                resolve_repo_path(repo_root, args.receipt, "joined executor receipt")
                if args.receipt
                else None
            )
            result = executor_join(repo_root, run_dir, receipt_path)
        elif args.command == "reconcile":
            output_only_admission_path = resolve_repo_path(
                repo_root,
                args.output_only_admission,
                "output-only mutation admission receipt",
            )
            result = reconcile(
                repo_root, run_dir, output_only_admission_path
            )
        elif args.command == "commit-resume":
            result = commit_resume(repo_root, run_dir, args.interrupt_after)
        else:
            result = status_document(repo_root, run_dir)
    except RunnerInterrupted as error:
        print(
            json.dumps(
                {
                    "schema_version": "task-session.governance-runner-status.v1",
                    "result": "interrupted",
                    "diagnostics": [str(error)],
                    "interruption_boundary": error.boundary,
                    "writes_performed": error.writes_performed,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 4
    except (RunnerBlock, OSError, UnicodeError) as error:
        print(
            json.dumps(
                {
                    "schema_version": "task-session.governance-runner-status.v1",
                    "result": "block",
                    "diagnostics": [str(error)],
                    "writes_performed": 0,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 3 if result.get("result") == "execution-failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
