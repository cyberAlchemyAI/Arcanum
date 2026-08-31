#!/usr/bin/env python3
"""Run one exact, manifest-bound Task Session owner hook."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


class HookBlock(ValueError):
    """A fail-closed owner-hook result."""

    def __init__(
        self,
        message: str,
        *,
        external_receipt_observed: bool = False,
    ):
        super().__init__(message)
        self.external_receipt_observed = external_receipt_observed


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def digest_without(value: dict[str, Any], field: str) -> str:
    payload = {key: item for key, item in value.items() if key != field}
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise HookBlock(f"cannot load {label}: {error}") from error
    if not isinstance(value, dict):
        raise HookBlock(f"{label} must be a JSON object")
    return value


def require_closed_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    if set(value) != expected:
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        raise HookBlock(f"{label} is not closed: missing={missing} extra={extra}")


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
        raise HookBlock(f"{label} path escapes repository root: {raw}")
    return str(path)


def resolve_repo_path(repo_root: Path, raw: str, label: str) -> Path:
    normalized = normalized_relative(raw, label)
    lexical = repo_root
    for part in PurePosixPath(normalized).parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise HookBlock(f"{label} path contains a symlink: {raw}")
    candidate = (repo_root / normalized).resolve(strict=False)
    try:
        candidate.relative_to(repo_root)
    except ValueError as error:
        raise HookBlock(f"{label} path escapes repository root: {raw}") from error
    return candidate


def relative_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError as error:
        raise HookBlock(f"path is outside repository root: {path}") from error


def exact_ref(repo_root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": relative_path(repo_root, path),
        "sha256": sha256(data),
        "size_bytes": len(data),
    }


def read_exact_bytes(
    repo_root: Path, reference: dict[str, Any], label: str
) -> tuple[Path, bytes]:
    path = resolve_repo_path(repo_root, str(reference.get("path", "")), label)
    if not path.is_file():
        raise HookBlock(f"missing {label}: {reference.get('path')}")
    data = path.read_bytes()
    if sha256(data) != reference.get("sha256"):
        raise HookBlock(f"stale {label} digest: {reference.get('path')}")
    if len(data) != reference.get("size_bytes"):
        raise HookBlock(f"stale {label} size: {reference.get('path')}")
    return path, data


def validate_schema(
    value: dict[str, Any], schema: dict[str, Any], label: str
) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise HookBlock(f"{label} schema invalid: {details}")


def validate_manifest(
    repo_root: Path, manifest_path: Path, manifest: dict[str, Any]
) -> None:
    require_closed_keys(
        manifest,
        {
            "schema_version",
            "manifest_version",
            "adapters",
            "manifest_digest",
        },
        "owner-hook adapter manifest",
    )
    if not (
        manifest["schema_version"]
        == "task-session.owner-hook-adapter-manifest.v1"
        and manifest["manifest_version"] == "1.0.0"
        and manifest["manifest_digest"] == digest_without(manifest, "manifest_digest")
    ):
        raise HookBlock("owner-hook adapter manifest identity or digest mismatch")
    if not isinstance(manifest["adapters"], list) or not manifest["adapters"]:
        raise HookBlock("owner-hook adapter manifest has no adapters")
    adapter_ids: list[str] = []
    for adapter in manifest["adapters"]:
        require_closed_keys(
            adapter,
            {
                "adapter_id",
                "purpose",
                "phase",
                "owner_identity",
                "executable_argv",
                "executable_ref",
                "cwd",
                "allowed_output_prefixes",
                "request_schema_ref",
                "receipt_schema_ref",
                "timeout_seconds",
                "max_output_bytes",
                "idempotency_namespace",
            },
            "owner-hook adapter",
        )
        if not (
            isinstance(adapter["adapter_id"], str)
            and adapter["adapter_id"]
            and isinstance(adapter["purpose"], str)
            and adapter["purpose"]
            and isinstance(adapter["phase"], str)
            and adapter["phase"]
            and isinstance(adapter["executable_argv"], list)
            and len(adapter["executable_argv"]) >= 2
            and all(
                isinstance(item, str) and item
                for item in adapter["executable_argv"]
            )
            and isinstance(adapter["timeout_seconds"], int)
            and adapter["timeout_seconds"] > 0
            and isinstance(adapter["max_output_bytes"], int)
            and adapter["max_output_bytes"] >= 256
            and isinstance(adapter["idempotency_namespace"], str)
            and adapter["idempotency_namespace"]
            and isinstance(adapter["allowed_output_prefixes"], list)
            and adapter["allowed_output_prefixes"]
            and all(
                isinstance(item, str) and item
                for item in adapter["allowed_output_prefixes"]
            )
        ):
            raise HookBlock("owner-hook adapter fields are invalid")
        require_closed_keys(
            adapter["owner_identity"],
            {"capability", "subject"},
            "owner-hook adapter owner identity",
        )
        executable, _ = read_exact_bytes(
            repo_root, adapter["executable_ref"], "owner-hook executable"
        )
        if relative_path(repo_root, executable) not in adapter["executable_argv"]:
            raise HookBlock("owner-hook executable ref is not bound into argv")
        for key in ("request_schema_ref", "receipt_schema_ref"):
            read_exact_bytes(repo_root, adapter[key], f"owner-hook {key}")
        cwd = (
            repo_root
            if adapter["cwd"] == "."
            else resolve_repo_path(repo_root, adapter["cwd"], "owner-hook cwd")
        )
        if not cwd.is_dir():
            raise HookBlock("owner-hook cwd is missing")
        for prefix in adapter["allowed_output_prefixes"]:
            resolve_repo_path(repo_root, prefix, "owner-hook output prefix")
        executable_name = Path(adapter["executable_argv"][0]).name.casefold()
        if executable_name in {
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
        }:
            raise HookBlock("owner-hook executable may not be a command shell")
        adapter_ids.append(adapter["adapter_id"])
    if len(set(adapter_ids)) != len(adapter_ids):
        raise HookBlock("owner-hook adapter ids are not unique")
    if manifest_path.resolve() != resolve_repo_path(
        repo_root, relative_path(repo_root, manifest_path), "manifest"
    ):
        raise HookBlock("owner-hook manifest path resolution mismatch")


def select_adapter(
    manifest: dict[str, Any], adapter_id: str
) -> dict[str, Any]:
    matched = [
        adapter
        for adapter in manifest["adapters"]
        if adapter["adapter_id"] == adapter_id
    ]
    if len(matched) != 1:
        raise HookBlock("request adapter id is missing or ambiguous")
    return matched[0]


def validate_receipt(
    repo_root: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
    receipt_schema: dict[str, Any],
    request_path: Path,
    request: dict[str, Any],
) -> None:
    validate_schema(receipt, receipt_schema, "owner-hook receipt")
    expected = {
        "request_id": request["request_id"],
        "adapter_id": request["adapter_id"],
        "phase": request["phase"],
        "owner_identity": request["owner_identity"],
        "manifest_ref": request["manifest_ref"],
        "request_ref": exact_ref(repo_root, request_path),
        "input_refs": request["input_refs"],
        "idempotency_key": request["idempotency_key"],
    }
    for key, value in expected.items():
        if receipt[key] != value:
            raise HookBlock(f"owner-hook receipt {key} mismatch")
    if receipt["result"] not in ("pass", "no-op"):
        raise HookBlock(f"owner-hook receipt result is {receipt['result']}")
    if receipt["terminal_sequence"]["receipt_path"] != relative_path(
        repo_root, receipt_path
    ):
        raise HookBlock("owner-hook receipt path mismatch")
    if receipt["receipt_digest"] != digest_without(receipt, "receipt_digest"):
        raise HookBlock("owner-hook receipt digest mismatch")
    observed_output_paths = [
        normalized_relative(reference["path"], "owner-hook output ref")
        for reference in receipt["output_refs"]
    ]
    if len(set(observed_output_paths)) != len(observed_output_paths):
        raise HookBlock("owner-hook receipt output paths are not unique")
    expected_output_paths = {
        normalized_relative(raw, "allowed owner-hook output")
        for raw in request["allowed_output_paths"]
        if normalized_relative(raw, "allowed owner-hook output")
        != normalized_relative(
            request["expected_receipt_path"], "expected owner-hook receipt"
        )
    }
    if set(observed_output_paths) != expected_output_paths:
        raise HookBlock(
            "owner-hook receipt outputs do not exactly cover allowed non-receipt outputs"
        )
    receipt_mtime = receipt_path.stat().st_mtime_ns
    for reference in receipt["output_refs"]:
        output, _ = read_exact_bytes(repo_root, reference, "owner-hook output")
        if output.stat().st_mtime_ns > receipt_mtime:
            raise HookBlock("owner-hook receipt was not the final owner write")


def run_bounded_process(
    argv: list[str],
    *,
    cwd: Path,
    environment: dict[str, str],
    timeout_seconds: int,
    limit: int,
) -> tuple[int | None, int, int, bool, bool, bool]:
    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=environment,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise HookBlock(f"owner-hook launch failed: {error}") from error
    totals = {"stdout": 0, "stderr": 0}
    retained = {"stdout": bytearray(), "stderr": bytearray()}

    def drain(name: str, stream: Any) -> None:
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            totals[name] += len(chunk)
            remaining = limit + 1 - len(retained[name])
            if remaining > 0:
                retained[name].extend(chunk[:remaining])

    assert process.stdout is not None
    assert process.stderr is not None
    threads = [
        threading.Thread(target=drain, args=("stdout", process.stdout)),
        threading.Thread(target=drain, args=("stderr", process.stderr)),
    ]
    for thread in threads:
        thread.start()
    timed_out = False
    try:
        return_code = process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        return_code = process.wait()
    for thread in threads:
        thread.join()
    return (
        return_code,
        totals["stdout"],
        totals["stderr"],
        len(retained["stdout"]) > limit,
        len(retained["stderr"]) > limit,
        timed_out,
    )


def run_owner_hook(
    repo_root: Path, manifest_path: Path, request_path: Path
) -> dict[str, Any]:
    manifest = load_object(manifest_path, "owner-hook adapter manifest")
    validate_manifest(repo_root, manifest_path, manifest)
    request = load_object(request_path, "owner-hook request")
    adapter = select_adapter(manifest, str(request.get("adapter_id", "")))
    _, request_schema_bytes = read_exact_bytes(
        repo_root, adapter["request_schema_ref"], "owner-hook request schema"
    )
    request_schema = json.loads(request_schema_bytes)
    validate_schema(request, request_schema, "owner-hook request")
    actual_manifest_ref = exact_ref(repo_root, manifest_path)
    if request["manifest_ref"] != actual_manifest_ref:
        raise HookBlock("request manifest ref is stale or path-mismatched")
    for key in ("request_schema_ref", "receipt_schema_ref"):
        if request[key] != adapter[key]:
            raise HookBlock(f"request {key} differs from adapter manifest")
    if request["owner_identity"] != adapter["owner_identity"]:
        raise HookBlock("request owner identity differs from adapter manifest")
    if request["phase"] != adapter["phase"]:
        raise HookBlock("request phase differs from adapter manifest")
    if request["timeout_seconds"] != adapter["timeout_seconds"]:
        raise HookBlock("request timeout differs from adapter manifest")
    if request["max_output_bytes"] != adapter["max_output_bytes"]:
        raise HookBlock("request output bound differs from adapter manifest")
    namespace = f"{adapter['idempotency_namespace']}:"
    if not request["idempotency_key"].startswith(namespace):
        raise HookBlock("request idempotency key differs from adapter namespace")
    for reference in request["input_refs"]:
        read_exact_bytes(repo_root, reference, "owner-hook input")
    allowed_paths = [
        normalized_relative(raw, "allowed owner-hook output")
        for raw in request["allowed_output_paths"]
    ]
    if len(set(allowed_paths)) != len(allowed_paths):
        raise HookBlock("allowed owner-hook output paths are not unique")
    expected_receipt_path = normalized_relative(
        request["expected_receipt_path"], "expected owner-hook receipt"
    )
    if expected_receipt_path not in allowed_paths:
        raise HookBlock("expected owner-hook receipt is not an allowed output")
    prefixes = [
        PurePosixPath(normalized_relative(raw, "owner-hook output prefix"))
        for raw in adapter["allowed_output_prefixes"]
    ]
    for raw in allowed_paths:
        path = PurePosixPath(raw)
        if not any(
            path == prefix or path.parts[: len(prefix.parts)] == prefix.parts
            for prefix in prefixes
        ):
            raise HookBlock("allowed owner-hook output is outside adapter prefixes")
        resolve_repo_path(repo_root, raw, "allowed owner-hook output")
    output_path = resolve_repo_path(
        repo_root, request["expected_receipt_path"], "owner-hook output"
    )
    protected = {
        manifest_path.resolve(),
        request_path.resolve(),
        resolve_repo_path(
            repo_root,
            request["request_schema_ref"]["path"],
            "request schema",
        ),
        resolve_repo_path(
            repo_root,
            request["receipt_schema_ref"]["path"],
            "receipt schema",
        ),
    }
    protected.update(
        resolve_repo_path(repo_root, reference["path"], "hook input")
        for reference in request["input_refs"]
    )
    if output_path.resolve() in protected:
        raise HookBlock("owner-hook output path may not overwrite an input")
    if not output_path.parent.is_dir():
        raise HookBlock("owner-hook output parent must already exist")
    _, receipt_schema_bytes = read_exact_bytes(
        repo_root, adapter["receipt_schema_ref"], "owner-hook receipt schema"
    )
    receipt_schema = json.loads(receipt_schema_bytes)
    if output_path.exists():
        receipt = load_object(output_path, "existing owner-hook receipt")
        validate_receipt(
            repo_root,
            output_path,
            receipt,
            receipt_schema,
            request_path,
            request,
        )
        return {
            "schema_version": "task-session.owner-hook-run-status.v1",
            "result": "pass",
            "adapter_id": request["adapter_id"],
            "owner_identity": request["owner_identity"],
            "receipt_ref": exact_ref(repo_root, output_path),
            "idempotent_replay": True,
            "bounded_capture": {
                "max_output_bytes": request["max_output_bytes"],
                "stdout_bytes": 0,
                "stderr_bytes": 0,
                "stdout_truncated": false_value(),
                "stderr_truncated": false_value(),
            },
            "runner_writes_performed": 0,
            "external_receipt_observed": False,
        }

    argv = list(adapter["executable_argv"])
    argv.extend(
        [
            "--repo-root",
            str(repo_root),
            "--request",
            relative_path(repo_root, request_path),
            "--output",
            request["expected_receipt_path"],
        ]
    )
    environment = {}
    if "PATH" in os.environ:
        environment["PATH"] = os.environ["PATH"]
    limit = request["max_output_bytes"]
    (
        return_code,
        stdout_bytes,
        stderr_bytes,
        stdout_overflow,
        stderr_overflow,
        timed_out,
    ) = run_bounded_process(
        argv,
        cwd=(
            repo_root
            if adapter["cwd"] == "."
            else resolve_repo_path(repo_root, adapter["cwd"], "owner-hook cwd")
        ),
        environment=environment,
        timeout_seconds=request["timeout_seconds"],
        limit=limit,
    )
    if timed_out:
        raise HookBlock(
            "owner-hook timed out "
            f"stdout_bytes={stdout_bytes} stderr_bytes={stderr_bytes}",
            external_receipt_observed=output_path.exists(),
        )
    if stdout_overflow or stderr_overflow:
        raise HookBlock(
            "owner-hook bounded output exceeded "
            f"stdout_bytes={stdout_bytes} stderr_bytes={stderr_bytes}",
            external_receipt_observed=output_path.exists(),
        )
    if return_code != 0:
        raise HookBlock(
            f"owner-hook returned nonzero exit status {return_code}",
            external_receipt_observed=output_path.exists(),
        )
    if not output_path.is_file():
        raise HookBlock("owner-hook receipt is missing")
    try:
        receipt = load_object(output_path, "owner-hook receipt")
        validate_receipt(
            repo_root,
            output_path,
            receipt,
            receipt_schema,
            request_path,
            request,
        )
    except HookBlock as error:
        error.external_receipt_observed = True
        raise
    return {
        "schema_version": "task-session.owner-hook-run-status.v1",
        "result": "pass",
        "adapter_id": request["adapter_id"],
        "owner_identity": request["owner_identity"],
        "receipt_ref": exact_ref(repo_root, output_path),
        "idempotent_replay": False,
        "bounded_capture": {
            "max_output_bytes": limit,
            "stdout_bytes": stdout_bytes,
            "stderr_bytes": stderr_bytes,
            "stdout_truncated": False,
            "stderr_truncated": False,
        },
        "runner_writes_performed": 0,
        "external_receipt_observed": True,
    }


def false_value() -> bool:
    return False


def fixture_adapter(repo_root: Path, request_path: Path, output_path: Path) -> int:
    request = load_object(request_path, "fixture owner-hook request")
    _, input_bytes = read_exact_bytes(
        repo_root, request["input_refs"][0], "fixture owner-hook input"
    )
    fixture_input = json.loads(input_bytes)
    behavior = fixture_input.get("behavior", "pass")
    if behavior == "timeout":
        time.sleep(request["timeout_seconds"] + 1)
    if behavior == "missing":
        return 0
    if behavior == "nonzero":
        return 7
    if behavior == "stdout-overflow":
        sys.stdout.write("x" * (request["max_output_bytes"] + 1))
    if behavior == "stderr-overflow":
        sys.stderr.write("x" * (request["max_output_bytes"] + 1))
    if behavior == "malformed":
        output_path.write_text("{malformed", encoding="utf-8")
        return 0
    output_refs = []
    expected_receipt = normalized_relative(
        request["expected_receipt_path"], "fixture expected receipt"
    )
    declared_outputs = [
        raw
        for raw in request["allowed_output_paths"]
        if normalized_relative(raw, "fixture allowed output") != expected_receipt
    ]
    if behavior == "pass-output":
        for raw in declared_outputs:
            output = resolve_repo_path(repo_root, raw, "fixture owner output")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text("fixture-owner-output\n", encoding="utf-8")
            output_refs.append(exact_ref(repo_root, output))
    if behavior == "undeclared-output":
        output = resolve_repo_path(
            repo_root,
            "runs/owner-hooks/undeclared-output.txt",
            "fixture undeclared output",
        )
        output.write_text("undeclared\n", encoding="utf-8")
        output_refs.append(exact_ref(repo_root, output))
    receipt = {
        "schema_version": "task-session.owner-hook-receipt.v1",
        "receipt_id": f"fixture-receipt:{request['request_id']}",
        "request_id": request["request_id"],
        "adapter_id": request["adapter_id"],
        "phase": request["phase"],
        "owner_identity": request["owner_identity"],
        "manifest_ref": request["manifest_ref"],
        "request_ref": exact_ref(repo_root, request_path),
        "input_refs": request["input_refs"],
        "idempotency_key": request["idempotency_key"],
        "result": fixture_input.get("result", "pass"),
        "output_refs": output_refs,
        "diagnostics": [],
        "terminal_sequence": {
            "receipt_path": relative_path(repo_root, output_path),
            "final_owner_write": True,
        },
    }
    if behavior == "owner-mismatch":
        receipt["owner_identity"] = {
            "capability": "wrong-owner",
            "subject": "wrong-subject",
        }
    if behavior == "idempotency-mismatch":
        receipt["idempotency_key"] = "wrong:key"
    if behavior == "path-mismatch":
        receipt["terminal_sequence"]["receipt_path"] = "wrong/receipt.json"
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    output_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-adapter", action="store_true")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--request", required=True)
    parser.add_argument("--output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = Path(args.repo_root).resolve()
        if not repo_root.is_dir():
            raise HookBlock("repository root is missing")
        request_path = resolve_repo_path(
            repo_root, args.request, "owner-hook request"
        )
        if args.fixture_adapter:
            if not args.output:
                raise HookBlock("fixture adapter output is required")
            output_path = resolve_repo_path(
                repo_root, args.output, "fixture owner-hook output"
            )
            return fixture_adapter(repo_root, request_path, output_path)
        if args.output:
            raise HookBlock("runner mode does not accept --output")
        if not args.manifest:
            raise HookBlock("owner-hook manifest is required")
        manifest_path = resolve_repo_path(
            repo_root, args.manifest, "owner-hook manifest"
        )
        result = run_owner_hook(repo_root, manifest_path, request_path)
    except (HookBlock, OSError, UnicodeError) as error:
        external_receipt_observed = bool(
            getattr(error, "external_receipt_observed", False)
        )
        print(
            json.dumps(
                {
                    "schema_version": "task-session.owner-hook-run-status.v1",
                    "result": "block",
                    "diagnostics": [str(error)],
                    "external_receipt_observed": external_receipt_observed,
                    "runner_writes_performed": 0,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
