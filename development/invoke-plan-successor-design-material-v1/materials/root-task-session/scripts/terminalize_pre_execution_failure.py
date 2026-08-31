#!/usr/bin/env python3
"""Emit one truthful Task Session terminal receipt for a pre-execution block."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from control_evidence_partition import canonical_bytes, canonical_digest, load_object, validate_partition


ROOT = Path(__file__).resolve().parent.parent


def rendered(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.resolve().relative_to(root.resolve()).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def resolve(root: Path, raw: str) -> Path:
    path = (root / raw).resolve()
    path.relative_to(root.resolve())
    return path


def read_exact(root: Path, reference: dict[str, Any]) -> dict[str, Any]:
    path = resolve(root, reference["path"])
    if not path.is_file() or exact_ref(root, path) != reference:
        raise ValueError(f"stale exact reference: {reference['path']}")
    return load_object(path)


def validate_schema(value: dict[str, Any], name: str) -> None:
    schema = load_object(ROOT / f"schemas/{name}")
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        raise ValueError(f"{name} invalid at {'/'.join(map(str, first.absolute_path)) or '<root>'}: {first.message}")


def blocker_fingerprint(profile: dict[str, Any]) -> str:
    return canonical_digest({
        "work_pack_id": profile["work_pack_id"],
        "task_id": profile["task_id"],
        "swu_id": profile["swu_id"],
        "attempt_id": profile["attempt_id"],
        "owner_acceptance_request_ref": profile["owner_acceptance_request_ref"],
        "owner_acceptance_response_ref": profile["owner_acceptance_response_ref"],
        "control_evidence_partition_ref": profile["control_evidence_partition_ref"],
        "failure_terminal_schema_ref": profile["failure_terminal_schema_ref"],
        "invoke_owner_schema_ref": profile["invoke_owner_schema_ref"],
        "continuity_schema_ref": profile["continuity_schema_ref"],
        "blocker_refs": sorted(profile["blocker_refs"], key=lambda item: (item["path"], item["sha256"], item["size_bytes"])),
        "control_refs": sorted(profile["control_refs"], key=lambda item: (item["path"], item["sha256"], item["size_bytes"])),
    })


def atomic_create(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ValueError(f"terminal output already exists with different bytes: {path}")
        return
    with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())


def terminalize(repository_root: Path, request_path: Path) -> dict[str, Any]:
    request = load_object(request_path)
    validate_schema(request, "governance-run-request.schema.json")
    profile = request.get("failure_terminalization")
    if not isinstance(profile, dict):
        raise ValueError("pre-execution failure terminalization profile is missing")
    validate_schema(profile, "pre-execution-failure-terminalization-v1.schema.json")
    if profile["attempt_id"] != request["run_id"] or profile["task_id"] != request["task_id"] or profile["swu_id"] != request["swu_id"]:
        raise ValueError("failure terminalization identity differs from Task Session request")
    for reference in [profile["owner_acceptance_request_ref"], profile["owner_acceptance_response_ref"], profile["control_evidence_partition_ref"], profile["failure_terminal_schema_ref"], profile["invoke_owner_schema_ref"], profile["continuity_schema_ref"], *profile["blocker_refs"], *profile["control_refs"]]:
        read_exact(repository_root, reference)
    partition = read_exact(repository_root, profile["control_evidence_partition_ref"])
    if request.get("control_evidence_partition") != partition:
        raise ValueError("failure terminalization partition differs from Task Session request")
    route = request.get("fast_execution_entry", {}).get("route_scope_partition", {})
    if profile["terminal_receipt_path"] != route.get("terminal_receipt_scope"):
        raise ValueError("failure terminal receipt differs from the route terminal scope")
    lifecycle = {item["path"]: (item["owner_capability"], item["write_class"]) for item in route.get("lifecycle_owner_scopes", [])}
    if lifecycle.get(profile["invoke_owner_receipt_path"]) != ("invoke", "owner-closeout-receipt"):
        raise ValueError("failure Invoke owner receipt is outside its typed lifecycle scope")
    if lifecycle.get(profile["continuity_cursor_path"]) != ("task-session", "continuity-cursor"):
        raise ValueError("failure continuity cursor is outside its typed lifecycle scope")
    forbidden = [
        *request["execution_contract"]["allowed_writes"],
        *[item["path"] for item in request["execution_contract"].get("transient_outputs", [])],
        route.get("terminal_receipt_scope", request["closeout_contract"]["terminal_receipt_path"]),
        *[item["path"] for item in route.get("lifecycle_owner_scopes", [])],
    ]
    # Early-block terminalization closes the exact controls that exist at the
    # stop boundary.  Later preparation outputs are deliberately absent, so the
    # whole partition must be shape/authority validated without requiring every
    # future postimage to exist.  The loop below then revalidates every present
    # output and requires ``control_refs`` to equal that exact present subset.
    validate_partition(partition, repository_root=repository_root, attempt_id=request["run_id"], forbidden_scopes=forbidden, revalidate_runtime=False)
    present_control_refs = []
    for item in partition["outputs"]:
        path = resolve(repository_root, item["path"])
        if not path.exists():
            continue
        expected = item.get("expected_postimage_ref")
        if expected is None or exact_ref(repository_root, path) != expected:
            raise ValueError(f"present control output lacks its exact bound postimage: {item['path']}")
        present_control_refs.append(expected)
    if sorted(profile["control_refs"], key=lambda item: item["path"]) != sorted(present_control_refs, key=lambda item: item["path"]):
        raise ValueError("failure control refs do not equal the exact present partition subset")
    derived_fingerprint = blocker_fingerprint(profile)
    if profile["blocker_fingerprint"] != derived_fingerprint:
        raise ValueError("declared blocker fingerprint is not canonical")
    request_reference = exact_ref(repository_root, request_path)
    receipt = {
        "schema_version": "task-session.pre-execution-failure-terminal-receipt.v1",
        "receipt_profile": "pre-execution-failure-terminalization-v1",
        "result": "block",
        "work_pack_id": profile["work_pack_id"],
        "task_id": profile["task_id"],
        "swu_id": profile["swu_id"],
        "attempt_id": profile["attempt_id"],
        "request_ref": request_reference,
        "owner_acceptance_request_ref": profile["owner_acceptance_request_ref"],
        "owner_acceptance_response_ref": profile["owner_acceptance_response_ref"],
        "control_evidence_partition_ref": profile["control_evidence_partition_ref"],
        "failure_terminal_schema_ref": profile["failure_terminal_schema_ref"],
        "invoke_owner_schema_ref": profile["invoke_owner_schema_ref"],
        "continuity_schema_ref": profile["continuity_schema_ref"],
        "blocker_refs": profile["blocker_refs"],
        "control_refs": profile["control_refs"],
        "blocker_fingerprint": derived_fingerprint,
        "terminalization_contract_digest": canonical_digest(profile),
        "phase_availability": {"admission": False, "ticket": False, "executor": False, "reconciliation": False, "commit": False, "successful_owner_closeout": False},
        "effect_summary": {"material_writes": 0, "external_effects": 0, "admission_consumed": False, "publication": False, "deployment": False},
        "successor_executed": False,
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    validate_schema(receipt, "pre-execution-failure-terminal-receipt-v1.schema.json")
    output = resolve(repository_root, profile["terminal_receipt_path"])
    atomic_create(output, rendered(receipt))
    return {"result": "block", "terminal_receipt_ref": exact_ref(repository_root, output), "blocker_fingerprint": derived_fingerprint, "writes_performed": 1}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--request", required=True)
    args = parser.parse_args()
    try:
        root = Path(args.repo_root).resolve()
        result = terminalize(root, resolve(root, args.request))
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"result": "block", "diagnostics": [str(error)], "writes_performed": 0}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
