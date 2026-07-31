#!/usr/bin/env python3
"""Validate the generic Task Session owner-hook protocol in synthetic repos."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


OWNED = (
    "schemas/owner-hook-request.schema.json",
    "schemas/owner-hook-receipt.schema.json",
    "hook-adapters.json",
    "scripts/run-owner-hook.py",
    "development/fixtures/owner-hook-cases.json",
    "development/validate-owner-hook.py",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON must be an object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def seal_manifest(manifest: dict[str, Any]) -> None:
    payload = {
        key: value for key, value in manifest.items() if key != "manifest_digest"
    }
    manifest["manifest_digest"] = hashlib.sha256(
        canonical_bytes(payload)
    ).hexdigest()


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def tree_manifest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def copy_protocol(source: Path, repo: Path) -> Path:
    target = repo / "arcanum/arcana/task-session"
    for relative in OWNED:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)
    return target


def invoke(repo: Path) -> tuple[int, dict[str, Any], str]:
    runner = repo / "arcanum/arcana/task-session/scripts/run-owner-hook.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(runner),
            "--repo-root",
            str(repo),
            "--manifest",
            "arcanum/arcana/task-session/hook-adapters.json",
            "--request",
            "scenario/request.json",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=8,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(
            f"runner returned non-JSON stdout={completed.stdout!r} "
            f"stderr={completed.stderr!r}"
        ) from error
    return completed.returncode, payload, completed.stderr


def scenario(
    root: Path,
    source: Path,
    case_id: str,
    mutation: str,
) -> tuple[Path, Path]:
    repo = root / case_id
    task_session = copy_protocol(source, repo)
    manifest_path = task_session / "hook-adapters.json"
    manifest = load_json(manifest_path)
    adapter = manifest["adapters"][0]
    scenario_dir = repo / "scenario"
    scenario_dir.mkdir(parents=True)
    output_dir = repo / "runs/owner-hooks"
    output_dir.mkdir(parents=True)
    input_path = scenario_dir / "input.json"
    behavior = mutation if mutation in {
        "missing",
        "timeout",
        "stdout-overflow",
        "stderr-overflow",
        "owner-mismatch",
        "idempotency-mismatch",
        "path-mismatch",
        "malformed",
        "undeclared-output",
        "nonzero",
    } else "pass"
    fixture_input: dict[str, Any] = {"behavior": behavior, "result": "pass"}
    if mutation == "no-op":
        fixture_input["result"] = "no-op"
    if mutation == "pass-output":
        fixture_input["behavior"] = "pass-output"
    write_json(input_path, fixture_input)

    receipt_path = "runs/owner-hooks/receipt.json"
    allowed_outputs = [receipt_path]
    if mutation in ("pass-output", "missing-declared-output"):
        allowed_outputs.append("runs/owner-hooks/auxiliary.json")
    request = {
        "schema_version": "task-session.owner-hook-request.v1",
        "request_id": f"request:{case_id}",
        "adapter_id": adapter["adapter_id"],
        "phase": adapter["phase"],
        "owner_identity": adapter["owner_identity"],
        "manifest_ref": exact_ref(repo, manifest_path),
        "request_schema_ref": adapter["request_schema_ref"],
        "receipt_schema_ref": adapter["receipt_schema_ref"],
        "input_refs": [exact_ref(repo, input_path)],
        "allowed_output_paths": allowed_outputs,
        "expected_receipt_path": receipt_path,
        "timeout_seconds": adapter["timeout_seconds"],
        "max_output_bytes": adapter["max_output_bytes"],
        "idempotency_key": (
            f"{adapter['idempotency_namespace']}:{case_id}"
        ),
    }

    manifest_changed = False
    leave_manifest_digest_stale = False
    stale_request_manifest_ref = False
    if mutation == "stale-manifest-ref":
        stale_request_manifest_ref = True
    elif mutation == "manifest-digest-drift":
        adapter["purpose"] += " drift"
        manifest_changed = True
        leave_manifest_digest_stale = True
    elif mutation == "stale-executable-ref":
        adapter["executable_ref"]["sha256"] = "0" * 64
        manifest_changed = True
    elif mutation == "shell-executable":
        adapter["executable_argv"] = [
            "sh",
            adapter["executable_ref"]["path"],
        ]
        manifest_changed = True
    elif mutation == "output-symlink":
        actual = repo / "runs/owner-hooks-actual"
        actual.mkdir()
        link = repo / "runs/owner-hooks-link"
        link.symlink_to(actual, target_is_directory=True)
        adapter["allowed_output_prefixes"] = ["runs/owner-hooks-link"]
        request["allowed_output_paths"] = [
            "runs/owner-hooks-link/receipt.json"
        ]
        request["expected_receipt_path"] = (
            "runs/owner-hooks-link/receipt.json"
        )
        manifest_changed = True
    elif mutation == "cwd-symlink":
        actual = repo / "scenario/cwd-actual"
        actual.mkdir()
        (repo / "cwd-link").symlink_to(actual, target_is_directory=True)
        adapter["cwd"] = "cwd-link"
        manifest_changed = True
    elif mutation == "executable-symlink":
        original = task_session / "scripts/run-owner-hook.py"
        link = task_session / "scripts/owner-hook-link.py"
        link.symlink_to(original.name)
        adapter["executable_argv"][1] = (
            "arcanum/arcana/task-session/scripts/owner-hook-link.py"
        )
        adapter["executable_ref"] = exact_ref(repo, link)
        manifest_changed = True
    elif mutation == "output-overwrites-input":
        adapter["allowed_output_prefixes"] = ["scenario"]
        request["allowed_output_paths"] = ["scenario/input.json"]
        request["expected_receipt_path"] = "scenario/input.json"
        manifest_changed = True

    if manifest_changed:
        if not leave_manifest_digest_stale:
            seal_manifest(manifest)
        write_json(manifest_path, manifest)
        request["manifest_ref"] = exact_ref(repo, manifest_path)
    if stale_request_manifest_ref:
        request["manifest_ref"]["sha256"] = "0" * 64

    if mutation == "malformed-request":
        del request["phase"]
    elif mutation == "request-owner-mismatch":
        request["owner_identity"] = {
            "capability": "wrong-owner",
            "subject": "wrong-subject",
        }
    elif mutation == "request-schema-ref":
        request["request_schema_ref"]["sha256"] = "0" * 64
    elif mutation == "receipt-schema-ref":
        request["receipt_schema_ref"]["sha256"] = "0" * 64
    elif mutation == "phase-mismatch":
        request["phase"] = "wrong-phase"
    elif mutation == "timeout-mismatch":
        request["timeout_seconds"] += 1
    elif mutation == "capture-mismatch":
        request["max_output_bytes"] += 1
    elif mutation == "namespace-mismatch":
        request["idempotency_key"] = "wrong.namespace:key"
    elif mutation == "output-escape":
        request["allowed_output_paths"] = ["../outside.json"]
        request["expected_receipt_path"] = "../outside.json"
    elif mutation == "output-prefix-mismatch":
        (repo / "runs/outside").mkdir()
        request["allowed_output_paths"] = ["runs/outside/receipt.json"]
        request["expected_receipt_path"] = "runs/outside/receipt.json"
    elif mutation == "input-symlink":
        real_input = scenario_dir / "real-input.json"
        shutil.copy2(input_path, real_input)
        linked_input = scenario_dir / "linked-input.json"
        linked_input.symlink_to(real_input.name)
        request["input_refs"] = [exact_ref(repo, linked_input)]

    request_path = scenario_dir / "request.json"
    write_json(request_path, request)
    return repo, request_path


def schema_errors(value: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        error.message
        for error in sorted(
            Draft202012Validator(schema).iter_errors(value),
            key=lambda item: list(item.absolute_path),
        )
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-session-dir", default=".")
    parser.add_argument("--material-inventory-manifest")
    args = parser.parse_args()
    source = Path(args.task_session_dir).resolve()
    fixtures = load_json(
        source / "development/fixtures/owner-hook-cases.json"
    )
    results: list[tuple[str, bool, str]] = []

    with tempfile.TemporaryDirectory(prefix="task-session-owner-hook-") as raw:
        temporary = Path(raw)
        for case in fixtures["cases"]:
            case_id = case["case_id"]
            mutation = case["mutation"]
            repo, _ = scenario(temporary, source, case_id, mutation)
            receipt_path = repo / "runs/owner-hooks/receipt.json"
            if mutation == "replay":
                code1, payload1, stderr1 = invoke(repo)
                before = tree_manifest(repo)
                code2, payload2, stderr2 = invoke(repo)
                after = tree_manifest(repo)
                passed = (
                    code1 == code2 == 0
                    and payload1.get("result") == "pass"
                    and payload2.get("idempotent_replay") is True
                    and payload2.get("external_receipt_observed") is False
                    and before == after
                    and not stderr1
                    and not stderr2
                )
                details = f"first={code1} replay={code2} stable={before == after}"
            else:
                code, payload, stderr = invoke(repo)
                if case["kind"] == "positive":
                    expected_result = "no-op" if mutation == "no-op" else "pass"
                    receipt = load_json(receipt_path) if receipt_path.is_file() else {}
                    auxiliary = repo / "runs/owner-hooks/auxiliary.json"
                    auxiliary_ok = (
                        mutation != "pass-output"
                        or (
                            auxiliary.is_file()
                            and receipt.get("output_refs")
                            == [exact_ref(repo, auxiliary)]
                        )
                    )
                    passed = (
                        code == 0
                        and payload.get("result") == "pass"
                        and payload.get("external_receipt_observed") is True
                        and receipt.get("result") == expected_result
                        and auxiliary_ok
                        and not stderr
                    )
                    details = (
                        f"code={code} receipt={receipt.get('result')} "
                        f"auxiliary={auxiliary_ok}"
                    )
                else:
                    observed_receipt = bool(
                        payload.get("external_receipt_observed")
                    )
                    passed = (
                        code == 2
                        and payload.get("result") == "block"
                        and payload.get("runner_writes_performed") == 0
                        and observed_receipt == receipt_path.exists()
                        and not stderr
                    )
                    details = (
                        f"code={code} receipt_observed={observed_receipt}"
                    )
            results.append((case_id, passed, details))

    request_schema = load_json(
        source / "schemas/owner-hook-request.schema.json"
    )
    receipt_schema = load_json(
        source / "schemas/owner-hook-receipt.schema.json"
    )
    valid_request = {
        "schema_version": "task-session.owner-hook-request.v1",
        "request_id": "schema-positive",
        "adapter_id": "adapter",
        "phase": "phase",
        "owner_identity": {"capability": "owner", "subject": "subject"},
        "manifest_ref": {"path": "manifest", "sha256": "0" * 64, "size_bytes": 1},
        "request_schema_ref": {"path": "request", "sha256": "0" * 64, "size_bytes": 1},
        "receipt_schema_ref": {"path": "receipt", "sha256": "0" * 64, "size_bytes": 1},
        "input_refs": [{"path": "input", "sha256": "0" * 64, "size_bytes": 1}],
        "allowed_output_paths": ["runs/receipt.json"],
        "expected_receipt_path": "runs/receipt.json",
        "timeout_seconds": 1,
        "max_output_bytes": 256,
        "idempotency_key": "adapter:key"
    }
    invalid_request = copy.deepcopy(valid_request)
    invalid_request["unexpected"] = True
    schema_results = [
        not schema_errors(valid_request, request_schema),
        bool(schema_errors(invalid_request, request_schema)),
    ]
    positive_receipt = next(
        (
            source
            for source in []
        ),
        None,
    )
    del positive_receipt
    valid_receipt = {
        "schema_version": "task-session.owner-hook-receipt.v1",
        "receipt_id": "receipt",
        "request_id": "request",
        "adapter_id": "adapter",
        "phase": "phase",
        "owner_identity": {"capability": "owner", "subject": "subject"},
        "manifest_ref": {"path": "manifest", "sha256": "0" * 64, "size_bytes": 1},
        "request_ref": {"path": "request", "sha256": "0" * 64, "size_bytes": 1},
        "input_refs": [{"path": "input", "sha256": "0" * 64, "size_bytes": 1}],
        "idempotency_key": "adapter:key",
        "result": "pass",
        "output_refs": [],
        "diagnostics": [],
        "terminal_sequence": {
            "receipt_path": "runs/receipt.json",
            "final_owner_write": True
        },
        "receipt_digest": "0" * 64
    }
    invalid_receipt = copy.deepcopy(valid_receipt)
    invalid_receipt["unexpected"] = True
    schema_results.extend(
        [
            not schema_errors(valid_receipt, receipt_schema),
            bool(schema_errors(invalid_receipt, receipt_schema)),
        ]
    )

    inventory_errors: list[str] = []
    for relative in OWNED:
        if not (source / relative).is_file():
            inventory_errors.append(f"missing owned output: {relative}")
    if args.material_inventory_manifest:
        manifest = load_json(Path(args.material_inventory_manifest))
        observed_targets = {
            item["target_path"].split("arcana/task-session/", 1)[-1]
            for item in manifest.get("outputs", [])
            if isinstance(item, dict)
            and isinstance(item.get("target_path"), str)
        }
        if observed_targets != set(OWNED):
            inventory_errors.append("producer manifest output inventory mismatch")
    public_text = "\n".join(
        (source / relative).read_text(encoding="utf-8")
        for relative in OWNED
    ).casefold()
    private_slug = "body" + "-war"
    private_phrase = "suggested" + " track"
    for forbidden in (f"projects/{private_slug}", f"{private_slug}.", private_phrase):
        if forbidden in public_text:
            inventory_errors.append(f"public boundary violation: {forbidden}")
    runner_text = (source / OWNED[3]).read_text(encoding="utf-8")
    for forbidden in ("shell=True", "os.system(", "capture_output=True"):
        if forbidden in runner_text:
            inventory_errors.append(f"runner contains forbidden surface: {forbidden}")
    expected_ids = {case["case_id"] for case in fixtures["cases"]}
    observed_ids = {case_id for case_id, _, _ in results}
    if expected_ids != observed_ids:
        inventory_errors.append(
            f"fixture/result mismatch missing={sorted(expected_ids-observed_ids)} "
            f"extra={sorted(observed_ids-expected_ids)}"
        )
    if not all(schema_results):
        inventory_errors.append("closed schema discrimination failed")

    positive = [
        item
        for item in results
        if next(case for case in fixtures["cases"] if case["case_id"] == item[0])[
            "kind"
        ]
        == "positive"
    ]
    negative = [item for item in results if item not in positive]
    failures = [item for item in results if not item[1]]
    failures.extend((error, False, error) for error in inventory_errors)
    print(
        f"RESULT positive={sum(item[1] for item in positive)}/{len(positive)} "
        f"negative={sum(item[1] for item in negative)}/{len(negative)} "
        f"schema={sum(schema_results)}/{len(schema_results)} "
        f"undeclared_outputs={len(inventory_errors)} "
        f"inventory_mode={'producer-manifest' if args.material_inventory_manifest else 'declared-targets'}"
    )
    for case_id, passed, details in results:
        print(f"{'PASS' if passed else 'FAIL'} {case_id} {details}")
    for error in inventory_errors:
        print(f"FAIL {error}")
    digest = hashlib.sha256(
        canonical_bytes(
            {
                relative: {
                    "sha256": hashlib.sha256(
                        (source / relative).read_bytes()
                    ).hexdigest(),
                    "size_bytes": (source / relative).stat().st_size,
                }
                for relative in OWNED
            }
        )
    ).hexdigest()
    print(f"STAGED_MANIFEST_SHA256 {digest}")
    print(
        "EXPERIMENT_HARNESS not_run owner=SWU-TSGR-010 "
        "reason=protocol-fixtures-only"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
