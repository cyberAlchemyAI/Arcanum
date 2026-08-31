#!/usr/bin/env python3
"""Validate a Task Session pre-execution block without claiming owner closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


INVOKE_ROOT = Path(__file__).resolve().parent.parent
TASK_ROOT = Path(__file__).resolve().parents[2] / "arcana/task-session"


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.resolve().relative_to(root.resolve()).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def resolve(root: Path, raw: str) -> Path:
    path = (root / raw).resolve(); path.relative_to(root.resolve()); return path


def validate(value: dict[str, Any], schema: Path, label: str) -> None:
    errors = sorted(Draft202012Validator(load(schema)).iter_errors(value), key=lambda item: list(item.absolute_path))
    if errors:
        raise ValueError(f"{label} schema invalid: {errors[0].message}")


def validate_canonical_receipt_digest(value: dict[str, Any], label: str) -> None:
    projection = dict(value)
    declared = projection.pop("receipt_digest", None)
    if declared != canonical_digest(projection):
        raise ValueError(f"{label} receipt digest is not canonical")


def atomic_create(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError:
        if path.read_bytes()!=data: raise ValueError(f"owner block receipt conflicts: {path}")
        return
    with os.fdopen(fd,"wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())


def handle(root: Path, request_path: Path, terminal_path: Path) -> dict[str, Any]:
    request = load(request_path)
    profile = request.get("failure_terminalization")
    if not isinstance(profile, dict): raise ValueError("failure terminalization profile missing")
    terminal = load(terminal_path)
    terminal_schema=resolve(root,profile["failure_terminal_schema_ref"]["path"])
    owner_schema=resolve(root,profile["invoke_owner_schema_ref"]["path"])
    if exact_ref(root,terminal_schema)!=profile["failure_terminal_schema_ref"] or exact_ref(root,owner_schema)!=profile["invoke_owner_schema_ref"]: raise ValueError("failure terminalization schema identity drift")
    validate(terminal, terminal_schema, "Task Session failure receipt")
    validate_canonical_receipt_digest(terminal, "Task Session failure")
    if terminal["request_ref"] != exact_ref(root, request_path): raise ValueError("failure receipt request identity is stale")
    for key in ("work_pack_id", "task_id", "swu_id", "attempt_id", "owner_acceptance_request_ref", "owner_acceptance_response_ref", "blocker_fingerprint"):
        if terminal[key] != profile[key]: raise ValueError(f"failure owner binding mismatch: {key}")
    receipt = {
        "schema_version": "invoke.pre-execution-block-owner-receipt.v1", "result": "block", "owner_capability": "invoke",
        "work_pack_id": profile["work_pack_id"], "task_id": profile["task_id"], "swu_id": profile["swu_id"], "attempt_id": profile["attempt_id"],
        "owner_acceptance_request_ref": profile["owner_acceptance_request_ref"],
        "owner_acceptance_response_ref": profile["owner_acceptance_response_ref"],
        "task_session_failure_receipt_ref": exact_ref(root, terminal_path), "blocker_fingerprint": profile["blocker_fingerprint"],
        "owner_closeout_claim": "unavailable-pre-execution",
        "effect_summary": {"material_writes": 0, "external_effects": 0, "selection": False, "admission": False, "execution": False, "successor_executed": False},
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    validate(receipt, owner_schema, "Invoke block owner receipt")
    output = resolve(root, profile["invoke_owner_receipt_path"])
    data = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode(); atomic_create(output, data)
    return {"result": "block", "owner_receipt_ref": exact_ref(root, output), "writes_performed": 1}


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--repo-root", required=True); parser.add_argument("--request", required=True); parser.add_argument("--terminal-receipt", required=True); args=parser.parse_args()
    try:
        root=Path(args.repo_root).resolve(); result=handle(root, resolve(root,args.request), resolve(root,args.terminal_receipt))
    except (OSError,UnicodeError,ValueError) as error:
        print(json.dumps({"result":"block","diagnostics":[str(error)],"writes_performed":0},sort_keys=True)); return 2
    print(json.dumps(result,sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
