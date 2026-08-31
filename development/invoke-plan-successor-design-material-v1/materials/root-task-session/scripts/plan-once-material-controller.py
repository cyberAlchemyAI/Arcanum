#!/usr/bin/env python3
"""Fixture-only proof of the split precloseout receipt protocol.

This intentionally does not launch an executor, invoke Invoke Refresh, mutate
canonical targets, or execute a successor. It validates fixture artifacts in
their causal order and exclusive-creates only a fixture-local consumption
ledger and deterministic controller state receipt.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from jsonschema import Draft202012Validator
from pathlib import Path, PurePosixPath
from typing import Any


PROFILE = "precloseout-execution-v1"
MARKER = ".task-session-precloseout-fixture"
MARKER_BYTES = b"task-session-precloseout-fixture-v1\n"


class ControllerBlock(RuntimeError):
    """A fail-closed fixture contract violation."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def invoke_receipt_projection_digest(receipt: dict[str, Any]) -> str:
    """Match the staged Invoke owner's non-self-referential digest contract."""
    projection = copy.deepcopy(receipt)
    projection.pop("receipt_digest", None)
    encoded = json.dumps(
        projection,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ControllerBlock(f"{label} must be a lowercase sha256")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ControllerBlock(f"{label} must be a non-empty string")
    return value


def fixture_root(path: Path) -> Path:
    root = path.resolve()
    temporary = Path(tempfile.gettempdir()).resolve()
    if root == temporary or temporary not in root.parents:
        raise ControllerBlock("fixture root must be a marked child of the system temporary directory")
    marker = root / MARKER
    if not marker.is_file() or marker.read_bytes() != MARKER_BYTES:
        raise ControllerBlock("fixture root marker is missing or invalid")
    return root


def safe_path(root: Path, relative: str, label: str) -> Path:
    raw = require_string(relative, label).replace("\\", "/")
    posix = PurePosixPath(raw)
    if posix.is_absolute() or ".." in posix.parts or not posix.parts:
        raise ControllerBlock(f"{label} escapes fixture root")
    candidate = (root / Path(*posix.parts)).resolve()
    if candidate != root and root not in candidate.parents:
        raise ControllerBlock(f"{label} escapes fixture root")
    return candidate


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ControllerBlock(f"{label} cannot be loaded: {error}") from error
    if not isinstance(value, dict):
        raise ControllerBlock(f"{label} must be a JSON object")
    return value


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    try:
        relative = path.resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise ControllerBlock("artifact ref escapes fixture root") from error
    payload = path.read_bytes()
    return {"path": relative, "sha256": sha256_bytes(payload), "size_bytes": len(payload)}


def read_exact(root: Path, reference: Any, label: str) -> tuple[Path, dict[str, Any]]:
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256", "size_bytes"}:
        raise ControllerBlock(f"{label} must be a closed exact artifact ref")
    path = safe_path(root, reference["path"], f"{label}.path")
    if not path.is_file():
        raise ControllerBlock(f"{label} is missing")
    actual = exact_ref(root, path)
    if actual != reference:
        raise ControllerBlock(f"{label} exact identity drift")
    return path, load_json(path, label)


def require_closed(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ControllerBlock(f"{label} has an invalid closed shape")
    return value


def protocol_path(root: Path, run_dir: str) -> Path:
    run = safe_path(root, run_dir, "run-dir")
    if run == root:
        raise ControllerBlock("run-dir must be a strict fixture-root child")
    return run


def load_protocol(root: Path, run: Path) -> tuple[Path, dict[str, Any]]:
    protocol_file = run / "protocol.json"
    protocol = load_json(protocol_file, "protocol")
    require_closed(
        protocol,
        {
            "schema_version",
            "receipt_profile",
            "run_id",
            "task_id",
            "swu_id",
            "attempt_id",
            "idempotency_key",
            "admission_token",
            "admission_receipt_ref",
            "ticket_ref",
            "executor_receipt_path",
            "precloseout_receipt_path",
            "invoke_receipt_path",
            "terminal_receipt_path",
            "validation_contract_digest",
            "successor_policy",
        },
        "protocol",
    )
    if protocol["schema_version"] != "task-session.plan-once-material-controller-fixture.v1":
        raise ControllerBlock("protocol schema version is invalid")
    if protocol["receipt_profile"] != PROFILE:
        raise ControllerBlock("protocol receipt profile is invalid")
    for field in ("run_id", "task_id", "swu_id", "attempt_id", "idempotency_key"):
        require_string(protocol[field], f"protocol.{field}")
    require_sha256(protocol["admission_token"], "protocol.admission_token")
    require_sha256(protocol["validation_contract_digest"], "protocol.validation_contract_digest")
    if protocol["successor_policy"] != "emit-cursor-never-execute-successor":
        raise ControllerBlock("protocol successor policy is invalid")
    for field in (
        "executor_receipt_path",
        "precloseout_receipt_path",
        "invoke_receipt_path",
        "terminal_receipt_path",
    ):
        safe_path(root, protocol[field], f"protocol.{field}")
    return protocol_file, protocol


def ledger_path(root: Path, run: Path, admission_ref: dict[str, Any]) -> Path:
    name = f"{admission_ref['sha256']}.json"
    return safe_path(
        root,
        (run.relative_to(root) / ".admission-consumption" / name).as_posix(),
        "derived admission ledger",
    )


def consume_admission(
    root: Path, run: Path, protocol_file: Path, protocol: dict[str, Any]
) -> tuple[Path, dict[str, Any], str]:
    admission_ref = protocol["admission_receipt_ref"]
    _, admission = read_exact(root, admission_ref, "mutation admission receipt")
    if admission.get("admissionToken") != protocol["admission_token"]:
        raise ControllerBlock("protocol admission token differs from admission receipt")
    if admission.get("attemptId") != protocol["attempt_id"]:
        raise ControllerBlock("protocol attempt differs from admission receipt")
    ledger = ledger_path(root, run, admission_ref)
    payload = {
        "schema_version": "task-session.admission-consumption.v1",
        "run_id": protocol["run_id"],
        "task_id": protocol["task_id"],
        "swu_id": protocol["swu_id"],
        "attempt_id": protocol["attempt_id"],
        "admission_token": protocol["admission_token"],
        "ticket_ref": protocol["ticket_ref"],
        "mutation_admission_receipt_ref": admission_ref,
        "protocol_ref": exact_ref(root, protocol_file),
    }
    rendered = canonical_bytes(payload)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(str(ledger), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if ledger.read_bytes() != rendered:
            raise ControllerBlock("single-use admission is already consumed by a different contract")
        status = "already-consumed-same-contract"
    else:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        status = "consumed-now"
    return ledger, payload, status


def require_identity(document: dict[str, Any], protocol: dict[str, Any], label: str) -> None:
    for field in ("run_id", "task_id", "swu_id"):
        if document.get(field) != protocol[field]:
            raise ControllerBlock(f"{label} {field} identity drift")


def validate_precloseout(
    root: Path,
    run: Path,
    protocol: dict[str, Any],
    ledger: Path,
) -> tuple[Path, dict[str, Any]]:
    receipt_path = safe_path(root, protocol["precloseout_receipt_path"], "precloseout receipt")
    receipt = load_json(receipt_path, "precloseout receipt")
    require_identity(receipt, protocol, "precloseout receipt")
    if receipt.get("schema_version") != "task-session.precloseout-execution-receipt.v1":
        raise ControllerBlock("precloseout receipt schema version is invalid")
    if receipt.get("claim_state") != "execution-validated-closeout-pending":
        raise ControllerBlock("precloseout receipt claim ceiling is invalid")
    if "closeout_join" in receipt:
        raise ControllerBlock("precloseout receipt must not contain closeout_join")
    _, executor = read_exact(
        root,
        receipt.get("executor_receipt_ref"),
        "precloseout executor receipt",
    )
    executor_path = safe_path(root, protocol["executor_receipt_path"], "protocol executor receipt")
    if exact_ref(root, executor_path) != receipt["executor_receipt_ref"]:
        raise ControllerBlock("precloseout executor receipt differs from protocol")
    require_identity(executor, protocol, "executor receipt")
    _, ticket = read_exact(root, receipt.get("ticket_ref"), "precloseout ticket")
    if receipt["ticket_ref"] != protocol["ticket_ref"]:
        raise ControllerBlock("precloseout ticket differs from protocol")
    require_identity(ticket, protocol, "ticket")
    read_exact(root, receipt.get("request_ref"), "precloseout request")
    consumed = require_closed(
        receipt.get("consumed_admission"),
        {"receipt_ref", "admission_token", "attempt_id", "consumption_ledger_ref"},
        "precloseout consumed admission",
    )
    if consumed["receipt_ref"] != protocol["admission_receipt_ref"]:
        raise ControllerBlock("precloseout admission receipt drift")
    if consumed["admission_token"] != protocol["admission_token"]:
        raise ControllerBlock("precloseout admission token drift")
    if consumed["attempt_id"] != protocol["attempt_id"]:
        raise ControllerBlock("precloseout admission attempt drift")
    if consumed["consumption_ledger_ref"] != exact_ref(root, ledger):
        raise ControllerBlock("precloseout consumption ledger identity drift")
    for field in (
        "material_commit_ref",
        "reconciliation_ref",
        "validation_receipt_ref",
        "target_inventory_ref",
        "target_result_inventory_ref",
    ):
        read_exact(root, receipt.get(field), f"precloseout {field}")
    if receipt.get("validation_contract_digest") != protocol["validation_contract_digest"]:
        raise ControllerBlock("precloseout validation contract drift")
    outputs = receipt.get("output_refs")
    if not isinstance(outputs, list) or not outputs:
        raise ControllerBlock("precloseout output inventory is missing")
    for index, reference in enumerate(outputs):
        read_exact(root, reference, f"precloseout output {index}")
    closeout = require_closed(
        receipt.get("closeout_contract"),
        {
            "route",
            "owner_capability",
            "source_receipt_path",
            "source_schema_ref",
            "target_inventory_ref",
            "expected_owner_receipt_path",
            "expected_owner_receipt_schema_ref",
            "final_terminal_receipt_path",
            "final_terminal_schema_ref",
            "allowed_delta_classes",
            "continuation_policy",
        },
        "precloseout Invoke contract",
    )
    if closeout["route"] != "invoke:refresh:apply-approved" or closeout["owner_capability"] != "invoke":
        raise ControllerBlock("precloseout Invoke route/owner drift")
    if closeout["source_receipt_path"] != receipt_path.relative_to(root).as_posix():
        raise ControllerBlock("precloseout source path is not self path")
    read_exact(root, closeout["source_schema_ref"], "precloseout schema")
    read_exact(root, closeout["target_inventory_ref"], "precloseout closeout inventory")
    read_exact(root, closeout["expected_owner_receipt_schema_ref"], "Invoke receipt schema")
    read_exact(root, closeout["final_terminal_schema_ref"], "terminal receipt schema")
    if closeout["expected_owner_receipt_path"] != protocol["invoke_receipt_path"]:
        raise ControllerBlock("precloseout Invoke receipt path differs from protocol")
    if closeout["final_terminal_receipt_path"] != protocol["terminal_receipt_path"]:
        raise ControllerBlock("precloseout terminal path differs from protocol")
    if closeout["continuation_policy"] != "emit-cursor-never-execute-successor":
        raise ControllerBlock("precloseout continuation policy drift")
    return receipt_path, receipt


def validate_invoke(
    root: Path,
    protocol: dict[str, Any],
    precloseout_path: Path,
    precloseout: dict[str, Any],
) -> tuple[Path, dict[str, Any]]:
    path = safe_path(root, protocol["invoke_receipt_path"], "Invoke receipt")
    receipt = load_json(path, "Invoke receipt")
    _, schema = read_exact(
        root,
        precloseout["closeout_contract"]["expected_owner_receipt_schema_ref"],
        "Invoke receipt schema",
    )
    schema_errors = [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(receipt),
            key=lambda item: list(item.absolute_path),
        )
    ]
    if schema_errors:
        raise ControllerBlock(
            "Invoke receipt fails its exact owner schema: " + "; ".join(schema_errors)
        )
    digest_description = schema.get("properties", {}).get("receipt_digest", {}).get(
        "description", ""
    )
    if "canonical JSON projection" not in digest_description:
        raise ControllerBlock("Invoke receipt schema lacks a canonical digest contract")
    if receipt["receipt_digest"] != invoke_receipt_projection_digest(receipt):
        raise ControllerBlock("Invoke receipt digest does not match canonical projection")
    expected_identity = {
        "task_id": protocol["task_id"],
        "run_id": protocol["run_id"],
        "swu_id": protocol["swu_id"],
        "attempt_id": protocol["attempt_id"],
        "idempotency_key": protocol["idempotency_key"],
    }
    if receipt["task_identity"] != expected_identity:
        raise ControllerBlock("Invoke receipt task identity drift")
    source = receipt["precloseout_source"]
    if source["receipt_ref"] != exact_ref(root, precloseout_path):
        raise ControllerBlock("Invoke receipt source is not the typed precloseout receipt")
    if source["schema_ref"] != precloseout["closeout_contract"]["source_schema_ref"]:
        raise ControllerBlock("Invoke receipt source schema drift")
    if source["task_identity"] != expected_identity:
        raise ControllerBlock("Invoke receipt embedded source identity drift")
    if receipt["closeout_output"]["path"] != protocol["invoke_receipt_path"]:
        raise ControllerBlock("Invoke receipt closeout output path differs from protocol")
    if receipt["final_owner_write"]["output_ref"] != receipt["closeout_output"]:
        raise ControllerBlock("Invoke receipt final owner write differs from closeout output")
    validation_ids: list[str] = []
    validation_kinds: set[str] = set()
    for index, entry in enumerate(receipt["validation_inventory"]):
        validation_ids.append(entry["validation_id"])
        validation_kinds.add(entry["kind"])
        read_exact(root, entry["evidence_ref"], f"Invoke validation evidence {index}")
    if len(validation_ids) != len(set(validation_ids)):
        raise ControllerBlock("Invoke validation inventory duplicates validation_id")
    required_kinds = {
        "source-precloseout",
        "material-reconciliation",
        "target-validation",
    }
    if not required_kinds.issubset(validation_kinds):
        raise ControllerBlock("Invoke validation inventory lacks required evidence kind")
    return path, receipt


def validate_terminal(
    root: Path,
    protocol: dict[str, Any],
    precloseout_path: Path,
    precloseout: dict[str, Any],
    invoke_path: Path,
) -> dict[str, Any]:
    path = safe_path(root, protocol["terminal_receipt_path"], "terminal receipt")
    terminal = load_json(path, "terminal receipt")
    require_identity(terminal, protocol, "terminal receipt")
    if terminal.get("receipt_profile") != PROFILE:
        raise ControllerBlock("terminal receipt profile is invalid")
    if terminal.get("precloseout_execution_receipt_ref") != exact_ref(root, precloseout_path):
        raise ControllerBlock("terminal receipt precloseout identity drift")
    if terminal.get("precloseout_execution_schema_ref") != precloseout["closeout_contract"]["source_schema_ref"]:
        raise ControllerBlock("terminal receipt precloseout schema drift")
    join = require_closed(
        terminal.get("closeout_join"),
        {"required_owner_capabilities", "joined_owner_receipts", "continuation"},
        "terminal closeout join",
    )
    if join["required_owner_capabilities"] != ["invoke"]:
        raise ControllerBlock("terminal receipt must require exactly Invoke")
    receipts = join["joined_owner_receipts"]
    if not isinstance(receipts, list) or len(receipts) != 1:
        raise ControllerBlock("terminal receipt must join exactly one Invoke receipt")
    owner = require_closed(receipts[0], {"owner_capability", "receipt_ref", "result"}, "joined Invoke receipt")
    if owner["owner_capability"] != "invoke" or owner["receipt_ref"] != exact_ref(root, invoke_path):
        raise ControllerBlock("terminal joined Invoke receipt identity drift")
    continuation = require_closed(
        join["continuation"], {"policy", "cursor_ref", "successor_executed"}, "terminal continuation"
    )
    if continuation["policy"] != "emit-cursor-never-execute-successor" or continuation["successor_executed"] is not False:
        raise ControllerBlock("terminal continuation attempts successor execution")
    return terminal


def write_state(root: Path, run: Path, value: dict[str, Any]) -> Path:
    target = safe_path(root, (run.relative_to(root) / "controller-state.json").as_posix(), "controller state")
    rendered = canonical_bytes(value)
    temporary = target.with_suffix(".tmp")
    temporary.write_bytes(rendered)
    os.replace(temporary, target)
    return target


def resume(fixture_root_path: Path, run_dir: str) -> dict[str, Any]:
    root = fixture_root(fixture_root_path)
    run = protocol_path(root, run_dir)
    protocol_file, protocol = load_protocol(root, run)
    ledger, _, consumption_status = consume_admission(root, run, protocol_file, protocol)
    state: dict[str, Any] = {
        "schema_version": "task-session.plan-once-material-controller-state.v1",
        "receipt_profile": PROFILE,
        "run_id": protocol["run_id"],
        "task_id": protocol["task_id"],
        "swu_id": protocol["swu_id"],
        "consumption_ledger_ref": exact_ref(root, ledger),
        "consumption": consumption_status,
        "successor_executed": False,
        "next_action": "await-precloseout-receipt",
    }
    precloseout_path = safe_path(root, protocol["precloseout_receipt_path"], "precloseout receipt")
    if not precloseout_path.is_file():
        write_state(root, run, state)
        return state
    precloseout_path, precloseout = validate_precloseout(root, run, protocol, ledger)
    state["next_action"] = "await-invoke-closeout"
    invoke_path = safe_path(root, protocol["invoke_receipt_path"], "Invoke receipt")
    if not invoke_path.is_file():
        write_state(root, run, state)
        return state
    invoke_path, _ = validate_invoke(root, protocol, precloseout_path, precloseout)
    state["next_action"] = "await-final-terminal"
    terminal_path = safe_path(root, protocol["terminal_receipt_path"], "terminal receipt")
    if not terminal_path.is_file():
        write_state(root, run, state)
        return state
    validate_terminal(root, protocol, precloseout_path, precloseout, invoke_path)
    state["next_action"] = "terminal-validated-selection-eligible"
    write_state(root, run, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    resume_parser = subparsers.add_parser("resume")
    resume_parser.add_argument("--fixture-root", required=True)
    resume_parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    try:
        result = resume(Path(args.fixture_root), args.run_dir)
    except ControllerBlock as error:
        print(json.dumps({"result": "block", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps({"result": "pass", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
