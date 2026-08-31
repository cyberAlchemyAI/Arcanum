#!/usr/bin/env python3
"""Stateless deterministic command surface for Invoke Define and Design."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver


INVOKE_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = INVOKE_ROOT / "schemas"
CATALOG_PATH = INVOKE_ROOT / "invoke-cli-stage-catalog.json"
RESULT_SCHEMA_URI = "https://arcanum.dev/schemas/invoke/cli-command-result/v1"
PROTECTED_AUTHORED_KEYS = {"sha256", "size", "receipt_digest", "producer", "validator"}


class CliFailure(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        status: str = "error",
        location: str | None = None,
        causes: list[str] | None = None,
        repair_route: str = "invoke-cli-input",
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.location = location
        self.causes = causes or []
        self.repair_route = repair_route

    def diagnostic(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "location": self.location,
            "message": self.message,
            "causes": self.causes,
            "repair_route": self.repair_route,
        }


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON value is forbidden: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_load(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise CliFailure(
            "STRICT_JSON_INVALID",
            f"cannot load strict JSON from {path}: {error}",
            location=str(path),
            repair_route="repair-json-input",
        ) from error


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def build_schema_store() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    schemas: dict[str, dict[str, Any]] = {}
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        document = strict_load(path)
        if not isinstance(document, dict) or not isinstance(document.get("$id"), str):
            continue
        schema_id = document["$id"]
        if schema_id in schemas:
            raise CliFailure(
                "SCHEMA_ID_DUPLICATE",
                f"duplicate installed schema id: {schema_id}",
                location=str(path),
                repair_route="repair-installed-invoke-package",
            )
        schemas[schema_id] = document
    return schemas, schemas


def schema_errors(
    document: Any,
    schema: dict[str, Any],
    registry: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    try:
        errors = sorted(
            Draft202012Validator(
                schema,
                resolver=RefResolver.from_schema(schema, store=registry),
            ).iter_errors(document),
            key=lambda error: (list(error.absolute_path), error.message),
        )
    except Exception as error:  # schema/reference failure is invocation failure
        raise CliFailure(
            "SCHEMA_EVALUATION_FAILED",
            f"installed schema could not be evaluated: {error}",
            repair_route="repair-installed-invoke-package",
        ) from error
    for error in errors:
        pointer = "".join(f"/{escape_pointer(str(part))}" for part in error.absolute_path)
        diagnostics.append(
            {
                "code": "SCHEMA_INVALID",
                "location": pointer or "/",
                "message": error.message,
                "causes": [],
                "repair_route": "repair-authoring-request",
            }
        )
    return diagnostics


def load_catalog(
    schemas: dict[str, dict[str, Any]], registry: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    catalog = strict_load(CATALOG_PATH)
    schema = schemas.get("https://arcanum.dev/schemas/invoke/cli-stage-catalog/v1")
    if schema is None:
        raise CliFailure(
            "CATALOG_SCHEMA_MISSING",
            "Invoke CLI stage-catalog schema is not installed",
            repair_route="repair-installed-invoke-package",
        )
    diagnostics = schema_errors(catalog, schema, registry)
    if diagnostics:
        first = diagnostics[0]
        raise CliFailure(
            "CATALOG_INVALID",
            first["message"],
            location=first["location"],
            causes=[item["message"] for item in diagnostics[1:]],
            repair_route="repair-installed-invoke-package",
        )
    return catalog


def escape_pointer(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise CliFailure(
            "JSON_POINTER_INVALID",
            f"JSON Pointer must begin with '/': {pointer}",
            location=pointer,
            repair_route="repair-authoring-request",
        )
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def pointer_exists(document: Any, pointer: str) -> bool:
    try:
        pointer_get(document, pointer)
        return True
    except CliFailure:
        return False


def pointer_get(document: Any, pointer: str) -> Any:
    current = document
    for part in pointer_parts(pointer):
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise CliFailure(
                "JSON_POINTER_MISSING",
                f"JSON Pointer does not resolve: {pointer}",
                location=pointer,
                status="block",
                repair_route="repair-authoring-request",
            )
    return current


def pointer_set(document: Any, pointer: str, value: Any) -> None:
    parts = pointer_parts(pointer)
    current = document
    for part in parts[:-1]:
        if not isinstance(current, dict):
            raise CliFailure(
                "JSON_POINTER_PARENT_INVALID",
                f"JSON Pointer parent is not an object: {pointer}",
                location=pointer,
                status="block",
                repair_route="repair-authoring-request",
            )
        if part not in current:
            current[part] = {}
        current = current[part]
    if not isinstance(current, dict):
        raise CliFailure(
            "JSON_POINTER_PARENT_INVALID",
            f"JSON Pointer parent is not an object: {pointer}",
            location=pointer,
            status="block",
            repair_route="repair-authoring-request",
        )
    current[parts[-1]] = value


def pointer_remove(document: Any, pointer: str) -> None:
    parts = pointer_parts(pointer)
    current = document
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            return
        current = current[part]
    if isinstance(current, dict):
        current.pop(parts[-1], None)


def walk_protected(value: Any, pointer: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}/{escape_pointer(key)}"
            if key in PROTECTED_AUTHORED_KEYS:
                hits.append(child_pointer)
            hits.extend(walk_protected(child, child_pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(walk_protected(child, f"{pointer}/{index}"))
    return hits


def confined_root(path_value: str) -> Path:
    root = Path(path_value).resolve()
    if not root.is_dir():
        raise CliFailure(
            "REPOSITORY_ROOT_INVALID",
            f"repository root is not a directory: {path_value}",
            location=path_value,
            repair_route="provide-repository-root",
        )
    return root


def within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def confined_file(path_value: str, root: Path, *, label: str) -> Path:
    lexical = Path(path_value)
    if not lexical.is_absolute():
        lexical = root / lexical
    path = lexical.resolve()
    if not within_root(path, root):
        raise CliFailure(
            "PATH_ESCAPE",
            f"{label} escapes the repository root: {path_value}",
            location=path_value,
            repair_route="provide-confined-path",
        )
    if not path.is_file() or lexical.is_symlink():
        raise CliFailure(
            "INPUT_FILE_INVALID",
            f"{label} is not a regular non-symlink file: {path_value}",
            location=path_value,
            repair_route="provide-exact-input",
        )
    return path


def confined_directory(path_value: str, root: Path, *, label: str) -> Path:
    lexical = Path(path_value)
    if not lexical.is_absolute():
        lexical = root / lexical
    path = lexical.resolve()
    if not within_root(path, root):
        raise CliFailure(
            "PATH_ESCAPE",
            f"{label} escapes the repository root: {path_value}",
            location=path_value,
            repair_route="provide-confined-path",
        )
    if not path.is_dir() or lexical.is_symlink():
        raise CliFailure(
            "INPUT_DIRECTORY_INVALID",
            f"{label} is not a regular non-symlink directory: {path_value}",
            location=path_value,
            repair_route="provide-exact-input",
        )
    return path


def absent_output(path_value: str, root: Path) -> Path:
    lexical = Path(path_value)
    if not lexical.is_absolute():
        lexical = root / lexical
    parent = lexical.parent.resolve()
    if not within_root(parent, root):
        raise CliFailure(
            "OUTPUT_PATH_ESCAPE",
            f"output escapes the repository root: {path_value}",
            location=path_value,
            repair_route="provide-confined-output",
        )
    if not parent.is_dir():
        raise CliFailure(
            "OUTPUT_PARENT_MISSING",
            f"output parent must already exist: {lexical.parent}",
            location=path_value,
            repair_route="create-output-parent",
        )
    if lexical.exists() or lexical.is_symlink():
        raise CliFailure(
            "OUTPUT_EXISTS",
            f"output must be absent: {path_value}",
            location=path_value,
            repair_route="choose-absent-output",
        )
    return lexical


def relative_label(path: Path, root: Path) -> str:
    resolved = path.resolve()
    if within_root(resolved, root):
        return resolved.relative_to(root).as_posix()
    return str(resolved)


def file_ref(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": relative_label(path, root),
        "kind": "file",
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def directory_ref(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": relative_label(path, root),
        "kind": "directory",
        "sha256": None,
        "size": None,
    }


def exact_directory_material(path: Path) -> tuple[str, int]:
    records: list[dict[str, Any]] = []
    for child in sorted(path.rglob("*")):
        if child.is_symlink():
            raise CliFailure(
                "SYMLINK_UNSUPPORTED",
                f"directory evidence contains a symlink: {child}",
                location=str(child),
                status="block",
                repair_route="repair-evidence-boundary",
            )
        if child.is_file():
            data = child.read_bytes()
            records.append(
                {
                    "relative_path": child.relative_to(path).as_posix(),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                }
            )
    return canonical_digest(records), sum(item["size"] for item in records)


def atomic_write(path: Path, data: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists() or path.is_symlink():
            raise CliFailure(
                "OUTPUT_RACE",
                f"output appeared during exclusive publication: {path}",
                location=str(path),
                repair_route="choose-absent-output",
            )
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def stage_contract(catalog: dict[str, Any], mode: str, stage: str) -> dict[str, Any]:
    mode_contract = catalog["modes"].get(mode)
    if mode_contract is None:
        raise CliFailure(
            "MODE_UNKNOWN",
            f"unknown Invoke mode: {mode}",
            location=mode,
            repair_route="invoke-modes",
        )
    if mode_contract["status"] != "active":
        raise CliFailure(
            "MODE_UNSUPPORTED",
            mode_contract["reason"],
            status="block",
            location=mode,
            repair_route=mode_contract["native_skill_route"],
        )
    contract = mode_contract["stages"].get(stage)
    if contract is None:
        raise CliFailure(
            "STAGE_UNKNOWN",
            f"unknown {mode} stage: {stage}",
            location=stage,
            repair_route=f"invoke-{mode}-describe",
        )
    return contract


def require_operation(contract: dict[str, Any], operation: str, mode: str, stage: str) -> None:
    if operation not in contract["operations"]:
        raise CliFailure(
            "OPERATION_UNSUPPORTED",
            f"operation {operation!r} is not valid for {mode}/{stage}",
            location=stage,
            repair_route=f"invoke-{mode}-describe",
        )


def author_document(
    request_path: Path,
    root: Path,
    mode: str,
    stage: str,
    contract: dict[str, Any],
    schemas: dict[str, dict[str, Any]],
    registry: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    request = strict_load(request_path)
    request_schema_name = contract.get("request_schema")
    output_schema_name = contract.get("output_schema")
    if not request_schema_name or not output_schema_name:
        raise CliFailure(
            "AUTHORING_CONTRACT_MISSING",
            f"{mode}/{stage} does not declare an authoring contract",
            repair_route="repair-installed-invoke-package",
        )
    request_schema = strict_load(SCHEMA_DIR / request_schema_name)
    diagnostics = schema_errors(request, request_schema, registry)
    if diagnostics:
        return None, diagnostics
    if request["mode"] != mode or request["stage"] != stage:
        return None, [
            {
                "code": "REQUEST_ROUTE_MISMATCH",
                "location": "/mode",
                "message": f"request declares {request['mode']}/{request['stage']} but command selects {mode}/{stage}",
                "causes": [],
                "repair_route": "repair-authoring-request",
            }
        ]

    authored = copy.deepcopy(request["document"])
    protected = walk_protected(authored)
    fixed_pointers = [item["pointer"] for item in contract["fixed_fields"]]
    derived_pointers = [item["pointer"] for item in contract["derived_ids"]]
    digest_pointers = [item["pointer"] for item in contract["derived_digests"]]
    protected.extend(
        pointer
        for pointer in fixed_pointers + derived_pointers + digest_pointers
        if pointer_exists(authored, pointer)
    )
    if protected:
        return None, [
            {
                "code": "PROTECTED_FIELD_AUTHORED",
                "location": pointer,
                "message": "field is compiler-owned and must not be supplied by the author",
                "causes": [],
                "repair_route": "remove-protected-field",
            }
            for pointer in sorted(set(protected))
        ]

    evidence_diagnostics: list[dict[str, Any]] = []
    for binding in request["evidence_paths"]:
        pointer = binding["pointer"]
        try:
            target = pointer_get(authored, pointer)
            if not isinstance(target, dict):
                raise CliFailure(
                    "EVIDENCE_TARGET_INVALID",
                    "evidence pointer must select an object",
                    location=pointer,
                    status="block",
                    repair_route="repair-authoring-request",
                )
            if "path" in target and target["path"] != binding["path"]:
                raise CliFailure(
                    "EVIDENCE_PATH_MISMATCH",
                    f"pointer path {target['path']!r} differs from binding path {binding['path']!r}",
                    location=pointer,
                    status="block",
                    repair_route="repair-authoring-request",
                )
            binding_kind = binding.get("kind", "file")
            target["path"] = binding["path"]
            if binding_kind == "directory":
                source = confined_directory(binding["path"], root, label="evidence path")
                digest, size = exact_directory_material(source)
                target["sha256"] = digest
                target["size"] = size
            else:
                source = confined_file(binding["path"], root, label="evidence path")
                data = source.read_bytes()
                target["sha256"] = hashlib.sha256(data).hexdigest()
                target["size"] = len(data)
        except CliFailure as failure:
            evidence_diagnostics.append(failure.diagnostic())
    if evidence_diagnostics:
        return None, evidence_diagnostics

    for fixed in contract["fixed_fields"]:
        pointer_set(authored, fixed["pointer"], copy.deepcopy(fixed["value"]))
    request_identity = canonical_digest(
        {
            "mode": mode,
            "stage": stage,
            "document": request["document"],
            "evidence_paths": request["evidence_paths"],
        }
    )[:20]
    for derived in contract["derived_ids"]:
        pointer_set(authored, derived["pointer"], f"{derived['prefix']}{request_identity}")
    for derived in contract["derived_digests"]:
        projection_pointers = derived["projection"]
        if projection_pointers is None:
            projection = copy.deepcopy(authored)
            pointer_remove(projection, derived["pointer"])
        else:
            projection = {}
            for pointer in projection_pointers:
                pointer_set(
                    projection,
                    pointer,
                    copy.deepcopy(pointer_get(authored, pointer)),
                )
        pointer_set(authored, derived["pointer"], canonical_digest(projection))

    output_schema = strict_load(SCHEMA_DIR / output_schema_name)
    diagnostics = schema_errors(authored, output_schema, registry)
    if diagnostics:
        return None, diagnostics
    return authored, []


def subprocess_diagnostic(
    returncode: int, stdout: str, stderr: str, *, repair_route: str
) -> list[dict[str, Any]]:
    messages = [line.strip() for line in (stderr + "\n" + stdout).splitlines() if line.strip()]
    if not messages:
        messages = [f"producer exited with status {returncode}"]
    code = "CONSUMER_BLOCKED" if returncode == 1 else "CONSUMER_INVOCATION_FAILED"
    return [
        {
            "code": code,
            "location": None,
            "message": message,
            "causes": [],
            "repair_route": repair_route,
        }
        for message in messages
    ]


def run_consumer(
    command: list[str],
    output: Path,
    root: Path,
    *,
    repair_route: str,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    diagnostics = subprocess_diagnostic(
        completed.returncode, completed.stdout, completed.stderr, repair_route=repair_route
    ) if completed.returncode else []
    status = "pass" if completed.returncode == 0 else ("block" if completed.returncode == 1 else "error")
    outputs: list[dict[str, Any]] = []
    if output.is_file():
        outputs.append(file_ref(output, root))
    elif output.is_dir():
        outputs.append(directory_ref(output, root))
    data = {
        "consumer_exit": completed.returncode,
        "consumer_stdout": completed.stdout,
        "consumer_stderr": completed.stderr,
    }
    return status, diagnostics, outputs, data


def parse_common_stage_args(
    argv: list[str], operation: str
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=f"invoke <mode> {operation}")
    if operation != "status":
        parser.add_argument("stage")
    parser.add_argument("--repo-root", required=True)
    if operation in {"check", "author", "status"}:
        parser.add_argument("--request", required=True)
    if operation != "check":
        parser.add_argument("--output", required=True)
    if operation == "produce":
        parser.add_argument("--context")
        parser.add_argument("--source")
        parser.add_argument("--closure")
        parser.add_argument("--discovery-root", action="append", default=[])
        parser.add_argument("--public-root", action="append", default=[])
    if operation == "admit":
        parser.add_argument("--bundle", required=True)
        parser.add_argument("--prior-admission")
    return parser.parse_args(argv)


def resolve_input_option(
    value: str | None, root: Path, label: str
) -> Path:
    if not value:
        raise CliFailure(
            "REQUIRED_INPUT_MISSING",
            f"required option is missing: {label}",
            location=label,
            repair_route="invoke-describe",
        )
    return confined_file(value, root, label=label)


def handle_produce(
    mode: str,
    stage: str,
    args: argparse.Namespace,
    contract: dict[str, Any],
    root: Path,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    output = absent_output(args.output, root)
    runner = INVOKE_ROOT / "scripts" / str(contract["runner"])
    if not runner.is_file():
        raise CliFailure(
            "RUNNER_MISSING",
            f"installed runner is missing: {runner.name}",
            repair_route="repair-installed-invoke-package",
        )
    inputs: list[dict[str, Any]] = []
    command = [sys.executable, str(runner)]
    if mode == "define" and stage == "semantic-closure":
        context = resolve_input_option(args.context, root, "--context")
        inputs.append(file_ref(context, root))
        if not args.discovery_root:
            raise CliFailure(
                "DISCOVERY_ROOT_MISSING",
                "semantic closure requires at least one --discovery-root",
                location="--discovery-root",
                repair_route="invoke-define-describe",
            )
        command.extend(
            [
                str(context),
                "--repository-root",
                str(root),
                "--context-schema",
                str(SCHEMA_DIR / "define-semantic-context-v1.schema.json"),
                "--receipt-schema",
                str(SCHEMA_DIR / "define-semantic-closure-receipt-v1.schema.json"),
            ]
        )
        for discovery_root in args.discovery_root:
            command.extend(["--discovery-root", discovery_root])
        for public_root in args.public_root:
            command.extend(["--public-root", public_root])
        command.extend(["--output", str(output)])
    elif mode == "define" and stage == "bundle":
        source = resolve_input_option(args.source, root, "--source")
        inputs.append(file_ref(source, root))
        if not args.discovery_root:
            raise CliFailure(
                "DISCOVERY_ROOT_MISSING",
                "Define bundle compilation requires at least one --discovery-root",
                location="--discovery-root",
                repair_route="invoke-define-describe",
            )
        command.extend(
            [
                str(source),
                "--output-dir",
                str(output),
                "--repo-root",
                str(root),
                "--schema-dir",
                str(SCHEMA_DIR),
            ]
        )
        for discovery_root in args.discovery_root:
            command.extend(["--discovery-root", discovery_root])
        for public_root in args.public_root:
            command.extend(["--public-root", public_root])
    elif mode == "plan" and stage == "bundle":
        source = resolve_input_option(args.source, root, "--source")
        inputs.append(file_ref(source, root))
        command.extend([
            str(source), "--repo-root", str(root), "--schema-dir", str(SCHEMA_DIR),
            "--output-dir", str(output),
        ])
    elif mode == "design" and stage in {"input-bundle", "final-bundle"}:
        closure = resolve_input_option(args.closure, root, "--closure")
        inputs.append(file_ref(closure, root))
        with tempfile.TemporaryDirectory(
            prefix=".invoke-design-attempt-", dir=output.parent
        ) as temporary:
            attempt = Path(temporary) / "attempt.json"
            command.extend(
                [
                    str(closure),
                    "--repo-root",
                    str(root),
                    "--output-dir",
                    str(output),
                    "--attempt-receipt",
                    str(attempt),
                    "--schema-dir",
                    str(SCHEMA_DIR),
                ]
            )
            status, diagnostics, outputs, data = run_consumer(
                command, output, root, repair_route=f"repair-design-{stage}"
            )
            return status, diagnostics, outputs, inputs, data
    elif mode == "design" and stage == "candidate":
        source = resolve_input_option(args.source, root, "--source")
        inputs.append(file_ref(source, root))
        with tempfile.TemporaryDirectory(
            prefix=".invoke-design-attempt-", dir=output.parent
        ) as temporary:
            attempt = Path(temporary) / "attempt.json"
            command.extend(
                [
                    str(source),
                    "--repo-root",
                    str(root),
                    "--output-dir",
                    str(output),
                    "--attempt-receipt",
                    str(attempt),
                    "--schema-dir",
                    str(SCHEMA_DIR),
                ]
            )
            status, diagnostics, outputs, data = run_consumer(
                command, output, root, repair_route="repair-design-candidate"
            )
            return status, diagnostics, outputs, inputs, data
    else:
        raise CliFailure(
            "PRODUCER_ROUTE_MISSING",
            f"no deterministic producer route is installed for {mode}/{stage}",
            repair_route="repair-installed-invoke-package",
        )
    status, diagnostics, outputs, data = run_consumer(
        command, output, root, repair_route=f"repair-{mode}-{stage}"
    )
    return status, diagnostics, outputs, inputs, data


def handle_admit(
    mode: str,
    args: argparse.Namespace,
    contract: dict[str, Any],
    root: Path,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    output = absent_output(args.output, root)
    bundle = confined_directory(args.bundle, root, label="--bundle")
    runner = INVOKE_ROOT / "scripts" / str(contract["runner"])
    if not runner.is_file():
        raise CliFailure(
            "RUNNER_MISSING",
            f"installed runner is missing: {runner.name}",
            repair_route="repair-installed-invoke-package",
        )
    inputs = [directory_ref(bundle, root)]
    if mode in {"define", "plan"}:
        command = [
            sys.executable,
            str(runner),
            "--repo-root",
            str(root),
            "--bundle-root",
            str(bundle),
            "--schema-dir",
            str(SCHEMA_DIR),
            "--output",
            str(output),
        ]
        if args.prior_admission:
            prior = confined_file(args.prior_admission, root, label="--prior-admission")
            inputs.append(file_ref(prior, root))
            command.extend(["--prior-admission", str(prior)])
    else:
        if args.prior_admission:
            raise CliFailure(
                "OPTION_UNSUPPORTED",
                "Design admission does not accept --prior-admission",
                location="--prior-admission",
                repair_route="invoke-design-describe",
            )
        command = [
            sys.executable,
            str(runner),
            str(bundle),
            "--repo-root",
            str(root),
            "--schema-dir",
            str(SCHEMA_DIR),
            "--output",
            str(output),
        ]
    status, diagnostics, outputs, data = run_consumer(
        command, output, root, repair_route=f"repair-{mode}-admission"
    )
    return status, diagnostics, outputs, inputs, data


def handle_status(
    mode: str,
    args: argparse.Namespace,
    root: Path,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    output = absent_output(args.output, root)
    request = confined_file(args.request, root, label="--request")
    command = [
        sys.executable,
        str(INVOKE_ROOT / "scripts" / "capability_status_resolver.py"),
        str(request),
        "--capabilities",
        str(INVOKE_ROOT / "mode-capabilities.json"),
        "--request-schema",
        str(SCHEMA_DIR / "capability-status-request.schema.json"),
        "--result-schema",
        str(SCHEMA_DIR / "capability-status-result.schema.json"),
        "--material-receipt-schema",
        str(SCHEMA_DIR / "material-package-receipt.schema.json"),
        "--output",
        str(output),
    ]
    status, diagnostics, outputs, data = run_consumer(
        command, output, root, repair_route=f"repair-{mode}-status"
    )
    return status, diagnostics, outputs, [file_ref(request, root)], data


def result_document(
    *,
    mode: str | None,
    operation: str,
    stage: str | None,
    status: str,
    inputs: list[dict[str, Any]] | None = None,
    outputs: list[dict[str, Any]] | None = None,
    diagnostics: list[dict[str, Any]] | None = None,
    data: Any = None,
) -> dict[str, Any]:
    return {
        "$schema": RESULT_SCHEMA_URI,
        "schema_version": "invoke.cli-command-result.v1",
        "command": "invoke",
        "mode": mode,
        "operation": operation,
        "stage": stage,
        "status": status,
        "inputs": inputs or [],
        "outputs": outputs or [],
        "diagnostics": diagnostics or [],
        "authority_effect": "none",
        "data": data,
    }


def emit_result(
    document: dict[str, Any],
    schemas: dict[str, dict[str, Any]],
    registry: dict[str, dict[str, Any]],
) -> int:
    internal_errors = schema_errors(document, schemas[RESULT_SCHEMA_URI], registry)
    if internal_errors:
        fallback = {
            "$schema": RESULT_SCHEMA_URI,
            "schema_version": "invoke.cli-command-result.v1",
            "command": "invoke",
            "mode": document.get("mode"),
            "operation": document.get("operation", "describe"),
            "stage": document.get("stage"),
            "status": "error",
            "inputs": [],
            "outputs": [],
            "diagnostics": [
                {
                    "code": "INTERNAL_RESULT_INVALID",
                    "location": item["location"],
                    "message": item["message"],
                    "causes": [],
                    "repair_route": "repair-installed-invoke-package",
                }
                for item in internal_errors
            ],
            "authority_effect": "none",
            "data": None,
        }
        sys.stdout.buffer.write(canonical_bytes(fallback))
        return 2
    sys.stdout.buffer.write(canonical_bytes(document))
    return {"pass": 0, "block": 1, "error": 2}[document["status"]]


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    schemas: dict[str, dict[str, Any]] = {}
    registry: dict[str, dict[str, Any]] = {}
    mode: str | None = None
    operation = "describe"
    stage: str | None = None
    try:
        schemas, registry = build_schema_store()
        catalog = load_catalog(schemas, registry)
        if arguments == ["--legacy-adapter-error"] or any(
            argument in {"--print-prompt", "--exec", "--adapter", "--timeout"}
            for argument in arguments
        ):
            return emit_result(
                result_document(
                    mode=None,
                    operation="describe",
                    stage=None,
                    status="error",
                    diagnostics=[
                        {
                            "code": "LEGACY_INVOKE_ADAPTER_RETIRED",
                            "location": None,
                            "message": "Invoke no longer supports --print-prompt, --exec, --adapter, adapter --output, or adapter --timeout; use `tools/arcanum invoke modes` or the native Invoke skill for free-form work.",
                            "causes": [],
                            "repair_route": "invoke-modes",
                        }
                    ],
                ),
                schemas,
                registry,
            )
        if not arguments:
            raise CliFailure(
                "COMMAND_MISSING",
                "Invoke requires `modes` or `<mode> <operation>`",
                repair_route="invoke-modes",
            )
        if arguments[0] == "modes":
            if len(arguments) != 1:
                raise CliFailure(
                    "ARGUMENT_COUNT_INVALID",
                    "`invoke modes` accepts no additional arguments",
                    repair_route="invoke-modes",
                )
            return emit_result(
                result_document(
                    mode=None,
                    operation="modes",
                    stage=None,
                    status="pass",
                    data={
                        name: {
                            "status": value["status"],
                            "stages": list(value.get("stages", {})),
                            "native_skill_route": value["native_skill_route"],
                            "reason": value.get("reason"),
                        }
                        for name, value in catalog["modes"].items()
                    },
                ),
                schemas,
                registry,
            )

        mode = arguments.pop(0)
        if not arguments:
            raise CliFailure(
                "OPERATION_MISSING",
                f"Invoke mode {mode!r} requires an operation",
                location=mode,
                repair_route="invoke-modes",
            )
        operation = arguments.pop(0)
        if operation == "describe":
            if len(arguments) > 1:
                raise CliFailure(
                    "ARGUMENT_COUNT_INVALID",
                    "describe accepts at most one stage",
                    repair_route=f"invoke-{mode}-describe",
                )
            mode_contract = catalog["modes"].get(mode)
            if mode_contract is None:
                raise CliFailure(
                    "MODE_UNKNOWN",
                    f"unknown Invoke mode: {mode}",
                    location=mode,
                    repair_route="invoke-modes",
                )
            stage = arguments[0] if arguments else None
            if stage is not None:
                data = stage_contract(catalog, mode, stage)
            else:
                data = mode_contract
            return emit_result(
                result_document(
                    mode=mode,
                    operation="describe",
                    stage=stage,
                    status="pass",
                    data=data,
                ),
                schemas,
                registry,
            )
        if operation not in {"check", "author", "produce", "admit", "status"}:
            raise CliFailure(
                "OPERATION_UNKNOWN",
                f"unknown Invoke operation: {operation}",
                location=operation,
                repair_route=f"invoke-{mode}-describe",
            )

        parsed = parse_common_stage_args(arguments, operation)
        stage = "status" if operation == "status" else parsed.stage
        contract = stage_contract(catalog, mode, stage)
        require_operation(contract, operation, mode, stage)
        root = confined_root(parsed.repo_root)

        if operation in {"check", "author"}:
            request = confined_file(parsed.request, root, label="--request")
            document, diagnostics = author_document(
                request, root, mode, stage, contract, schemas, registry
            )
            inputs = [file_ref(request, root)]
            if diagnostics:
                return emit_result(
                    result_document(
                        mode=mode,
                        operation=operation,
                        stage=stage,
                        status="block",
                        inputs=inputs,
                        diagnostics=diagnostics,
                    ),
                    schemas,
                    registry,
                )
            if operation == "check":
                return emit_result(
                    result_document(
                        mode=mode,
                        operation=operation,
                        stage=stage,
                        status="pass",
                        inputs=inputs,
                        data={"canonical_sha256": hashlib.sha256(canonical_bytes(document)).hexdigest()},
                    ),
                    schemas,
                    registry,
                )
            output = absent_output(parsed.output, root)
            atomic_write(output, canonical_bytes(document))
            return emit_result(
                result_document(
                    mode=mode,
                    operation=operation,
                    stage=stage,
                    status="pass",
                    inputs=inputs,
                    outputs=[file_ref(output, root)],
                ),
                schemas,
                registry,
            )

        if operation == "produce":
            status, diagnostics, outputs, inputs, data = handle_produce(
                mode, stage, parsed, contract, root
            )
        elif operation == "admit":
            status, diagnostics, outputs, inputs, data = handle_admit(
                mode, parsed, contract, root
            )
        else:
            status, diagnostics, outputs, inputs, data = handle_status(mode, parsed, root)
        return emit_result(
            result_document(
                mode=mode,
                operation=operation,
                stage=stage,
                status=status,
                inputs=inputs,
                outputs=outputs,
                diagnostics=diagnostics,
                data=data,
            ),
            schemas,
            registry,
        )
    except CliFailure as failure:
        if schemas and RESULT_SCHEMA_URI in schemas:
            return emit_result(
                result_document(
                    mode=mode,
                    operation=operation if operation in {"modes", "describe", "check", "author", "produce", "admit", "status"} else "describe",
                    stage=stage,
                    status=failure.status,
                    diagnostics=[failure.diagnostic()],
                ),
                schemas,
                registry,
            )
        sys.stdout.buffer.write(
            canonical_bytes(
                {
                    "status": "error",
                    "diagnostics": [failure.diagnostic()],
                    "authority_effect": "none",
                }
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
