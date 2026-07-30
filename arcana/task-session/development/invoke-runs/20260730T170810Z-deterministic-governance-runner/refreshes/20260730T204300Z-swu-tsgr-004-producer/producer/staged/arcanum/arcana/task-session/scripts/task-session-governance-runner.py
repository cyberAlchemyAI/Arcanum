#!/usr/bin/env python3
"""Deterministic, one-SWU Task Session governance runner.

SWU-TSGR-003 owns only ``prepare`` and read-only ``status``.  Later phases are
intentionally absent.  Prepare joins already-produced owner receipts, validates
their exact byte identities, and emits a digest-chained execution ticket without
launching an executor.
"""

from __future__ import annotations

import argparse
import hashlib
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
)
SELECTED_SWU = re.compile(
    r"^\|\s*`(?P<swu>SWU-[A-Z0-9-]+)`\s*\|.*\|\s*selected\s*\|\s*$",
    re.MULTILINE,
)


class RunnerBlock(ValueError):
    """A fail-closed runner outcome."""


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
    if current["phase"] in ("ticketed", "execution-received"):
        ticket_path = run_dir / "execution-ticket.json"
        if not ticket_path.is_file():
            raise RunnerBlock("ticketed checkpoint is missing execution ticket")
        ticket = load_object(ticket_path, "execution ticket")
        validate_schema(
            ticket,
            load_object(schema_dir() / "execution-ticket.schema.json", "ticket schema"),
            "execution ticket",
        )
    if current["phase"] == "ticketed":
        next_action = "executor-join"
    elif current["phase"] == "execution-received":
        next_action = "reconcile-not-implemented"
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
    if run_dir.exists():
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
    work_pack_path, work_pack_bytes = read_exact_bytes(
        repo_root, request["work_pack_ref"], "work pack"
    )
    swu_path, swu_bytes = read_exact_bytes(repo_root, request["swu_ref"], "SWU contract")
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
    baselines = baseline_inventory(
        repo_root, request["execution_contract"]["allowed_writes"]
    )

    executor_contract = executor_contract_from_config(
        repo_root, request, run_dir, executor_config
    )

    resolved = phase_receipt(
        request=request,
        phase="resolved",
        index=1,
        predecessor_phase="request",
        predecessor_ref=request_ref,
        input_refs=[request_ref, request["work_pack_ref"], request["swu_ref"]],
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
    return status_document(repo_root, run_dir)


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
        elif args.command == "executor-join":
            receipt_path = (
                resolve_repo_path(repo_root, args.receipt, "joined executor receipt")
                if args.receipt
                else None
            )
            result = executor_join(repo_root, run_dir, receipt_path)
        else:
            result = status_document(repo_root, run_dir)
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
