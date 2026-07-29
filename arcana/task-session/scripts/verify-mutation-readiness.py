#!/usr/bin/env python3
"""Bind an Invoke material receipt to live Task Session mutation controls."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


MUTATION_MODES = {"routed-mutation", "reusable-mutation"}


def canonical_digest(document: Any) -> str:
    payload = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def byte_digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def schema_errors(
    document: dict[str, Any], schema: dict[str, Any], label: str
) -> list[str]:
    return [
        f"{label} schema invalid at "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def normalized_relative_path(raw_path: str) -> tuple[str | None, str | None]:
    normalized = raw_path.replace("\\", "/")
    posix_path = PurePosixPath(normalized)
    if (
        not normalized
        or posix_path.is_absolute()
        or PureWindowsPath(raw_path).is_absolute()
        or ".." in posix_path.parts
    ):
        return None, f"path escape: {raw_path}"
    cleaned = str(posix_path)
    if cleaned in ("", "."):
        return None, f"path escape: {raw_path}"
    return cleaned, None


def normalized_write_set(
    request: dict[str, Any],
    key: str,
    label: str,
) -> tuple[set[str], list[str]]:
    normalized_paths: set[str] = set()
    errors: list[str] = []
    for raw_path in request.get(key, []):
        normalized, path_error = normalized_relative_path(raw_path)
        if path_error:
            errors.append(f"{label} {path_error}")
            continue
        assert normalized is not None
        if normalized in normalized_paths:
            errors.append(f"duplicate normalized {label} path: {raw_path}")
        if normalized != raw_path:
            errors.append(f"non-canonical {label} path: {raw_path}")
        normalized_paths.add(normalized)
    return normalized_paths, errors


def read_exact_artifact(
    repository_root: Path,
    reference: dict[str, Any],
    label: str,
) -> tuple[bytes | None, list[str]]:
    normalized, path_error = normalized_relative_path(reference["path"])
    if path_error:
        return None, [f"{label} {path_error}"]
    assert normalized is not None
    root = repository_root.resolve()
    candidate = (root / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, [f"{label} path escape: {reference['path']}"]
    if not candidate.is_file():
        return None, [f"missing {label}: {reference['path']}"]
    content = candidate.read_bytes()
    errors: list[str] = []
    if byte_digest(content) != reference["sha256"]:
        errors.append(f"{label} digest mismatch: {reference['path']}")
    if len(content) != reference["sizeBytes"]:
        errors.append(f"{label} size mismatch: {reference['path']}")
    return content, errors


def parse_json_bytes(content: bytes, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        value = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, [f"{label} is not valid JSON: {error}"]
    if not isinstance(value, dict):
        return None, [f"{label} must be a JSON object"]
    return value, []


def producer_source_tuple(source: dict[str, Any]) -> tuple[Any, ...]:
    return (
        source.get("path"),
        source.get("sha256"),
        source.get("size_bytes"),
        source.get("authority_class"),
    )


def request_source_tuple(source: dict[str, Any]) -> tuple[Any, ...]:
    return (
        source.get("path"),
        source.get("sha256"),
        source.get("sizeBytes"),
        source.get("authorityClass"),
    )


def producer_dependency_tuple(dependency: dict[str, Any]) -> tuple[Any, ...]:
    reference = dependency.get("artifact_ref", {})
    return (
        dependency.get("dependency_id"),
        reference.get("path"),
        reference.get("sha256"),
        reference.get("size_bytes"),
    )


def request_dependency_tuple(dependency: dict[str, Any]) -> tuple[Any, ...]:
    reference = dependency.get("artifactRef", {})
    return (
        dependency.get("dependencyId"),
        reference.get("path"),
        reference.get("sha256"),
        reference.get("sizeBytes"),
    )


def base_receipt(
    request: dict[str, Any],
    request_digest: str | None,
) -> dict[str, Any]:
    execution_mode = request.get("executionMode", "invalid")
    if execution_mode not in MUTATION_MODES | {"standalone-nonmutating"}:
        execution_mode = "invalid"
    return {
        "schemaVersion": "1.1.0",
        "executionMode": execution_mode,
        "admissionVerdict": "block",
        "mutationReady": False,
        "taskId": request.get("taskId"),
        "swuId": request.get("swuId"),
        "requestDigest": request_digest,
        "producerSchemaDigest": None,
        "materialReceiptDigest": None,
        "materialPackageDigest": None,
        "controllingPaths": sorted(
            {
                item.get("path")
                for item in request.get("controlArtifacts", [])
                if isinstance(item, dict)
                and isinstance(item.get("path"), str)
                and item["path"]
            }
        ),
        "dependencyIds": sorted(
            {
                item.get("dependencyId")
                for item in request.get("dependencyFrontier", [])
                if isinstance(item, dict)
                and isinstance(item.get("dependencyId"), str)
                and item["dependencyId"]
            }
        ),
        "materialWrites": sorted(
            {
                item
                for item in request.get("materialWrites", [])
                if isinstance(item, str) and item
            }
        ),
        "executionOutputs": sorted(
            {
                item
                for item in request.get("executionOutputs", [])
                if isinstance(item, str) and item
            }
        ),
        "allowedWrites": sorted(
            {
                item
                for item in request.get("allowedWrites", [])
                if isinstance(item, str) and item
            }
        ),
        "validationCommands": sorted(
            {
                item
                for item in request.get("validationCommands", [])
                if isinstance(item, str) and item
            }
        ),
        "lifecycleOwner": request.get("lifecycleOwner"),
        "authorityClass": request.get("authorityClass"),
        "publicationClass": request.get("publicationClass"),
        "liveValidationRequired": execution_mode in MUTATION_MODES,
        "reasons": [],
    }


def resolve_mutation_admission(
    request: dict[str, Any],
    repository_root: Path,
    request_schema: dict[str, Any],
) -> dict[str, Any]:
    result = base_receipt(request, canonical_digest(request))
    failures = schema_errors(request, request_schema, "admission request")
    if failures:
        result["reasons"] = sorted(set(failures))
        return result

    if request["executionMode"] == "standalone-nonmutating":
        result["admissionVerdict"] = "not-applicable"
        result["liveValidationRequired"] = False
        return result

    material_writes, material_write_errors = normalized_write_set(
        request, "materialWrites", "material write"
    )
    execution_outputs, execution_output_errors = normalized_write_set(
        request, "executionOutputs", "execution output"
    )
    allowed_writes, allowed_write_errors = normalized_write_set(
        request, "allowedWrites", "allowed write"
    )
    failures.extend(material_write_errors)
    failures.extend(execution_output_errors)
    failures.extend(allowed_write_errors)
    if material_writes & execution_outputs:
        failures.append("material and execution write scopes overlap")
    if material_writes | execution_outputs != allowed_writes:
        failures.append("allowed write scope partition mismatch")

    artifacts: dict[str, tuple[bytes | None, dict[str, Any] | None]] = {}
    for key, label in (
        ("producerReceiptSchema", "producer receipt schema"),
        ("materialReceipt", "material receipt"),
        ("materialPackage", "material package"),
    ):
        content, errors = read_exact_artifact(repository_root, request[key], label)
        failures.extend(errors)
        document: dict[str, Any] | None = None
        if content is not None and not errors:
            document, parse_errors = parse_json_bytes(content, label)
            failures.extend(parse_errors)
        artifacts[key] = (content, document)

    schema_content, producer_schema = artifacts["producerReceiptSchema"]
    receipt_content, material_receipt = artifacts["materialReceipt"]
    _, material_package = artifacts["materialPackage"]
    if schema_content is not None:
        result["producerSchemaDigest"] = byte_digest(schema_content)
    if receipt_content is not None:
        result["materialReceiptDigest"] = byte_digest(receipt_content)

    for control in request["controlArtifacts"]:
        _, errors = read_exact_artifact(repository_root, control, "control artifact")
        failures.extend(errors)
    roles = [item["role"] for item in request["controlArtifacts"]]
    for required_role in ("task-contract", "work-pack", "context-pack"):
        if roles.count(required_role) != 1:
            failures.append(f"exactly one {required_role} control artifact required")

    context_controls = [
        item for item in request["controlArtifacts"] if item["role"] == "context-pack"
    ]
    if len(context_controls) == 1:
        content, errors = read_exact_artifact(
            repository_root, context_controls[0], "context pack"
        )
        failures.extend(errors)
        if content is not None and not errors:
            context_pack, parse_errors = parse_json_bytes(content, "context pack")
            failures.extend(parse_errors)
            if context_pack is not None:
                if context_pack.get("task_id") != request["taskId"]:
                    failures.append("context pack task id mismatch")
                if context_pack.get("swu_id") != request["swuId"]:
                    failures.append("context pack SWU id mismatch")
                if context_pack.get("strict_coverage") is not True:
                    failures.append("context pack strict coverage is not true")

    for dependency in request["dependencyFrontier"]:
        _, errors = read_exact_artifact(
            repository_root, dependency["artifactRef"], "dependency"
        )
        failures.extend(errors)

    if producer_schema is not None and material_receipt is not None:
        failures.extend(
            schema_errors(material_receipt, producer_schema, "material receipt")
        )

    if material_receipt is not None and material_package is not None:
        package_digest = canonical_digest(material_package)
        result["materialPackageDigest"] = package_digest
        if material_receipt.get("packageDigest") != package_digest:
            failures.append("material package digest mismatch")
        if material_receipt.get("packageId") != material_package.get("package_id"):
            failures.append("material package id mismatch")
        if material_receipt.get("patchVerdict") != "pass":
            failures.append("material patch verdict is not pass")
        if material_receipt.get("mutationHandoff") != "ready":
            failures.append("material mutation handoff is not ready")
        if material_receipt.get("dependencyResult") != "pass":
            failures.append("material dependency result is not pass")
        if material_receipt.get("ownerBoundaryResult") != "pass":
            failures.append("material owner boundary result is not pass")
        if material_receipt.get("publicationBoundaryResult") != "pass":
            failures.append("material publication boundary result is not pass")
        if material_receipt.get("reasons"):
            failures.append("material receipt contains rejection reasons")

        package_sources = {
            producer_source_tuple(item)
            for item in material_package.get("source_artifacts", [])
            if isinstance(item, dict)
        }
        request_sources = {
            request_source_tuple(item) for item in request["controlArtifacts"]
        }
        if package_sources != request_sources:
            failures.append("controlling source frontier mismatch")

        package_dependencies = {
            producer_dependency_tuple(item)
            for item in material_package.get("dependencies", [])
            if isinstance(item, dict)
        }
        request_dependencies = {
            request_dependency_tuple(item) for item in request["dependencyFrontier"]
        }
        if package_dependencies != request_dependencies:
            failures.append("dependency frontier mismatch")

        change_targets = {
            item.get("target_path")
            for item in material_package.get("changes", [])
            if isinstance(item, dict) and isinstance(item.get("target_path"), str)
        }
        inventory_targets = {
            item.get("target_path")
            for item in material_package.get("target_inventory", [])
            if isinstance(item, dict) and isinstance(item.get("target_path"), str)
        }
        receipt_targets = set(material_receipt.get("validatedPaths", []))
        if not (
            material_writes
            == change_targets
            == inventory_targets
            == receipt_targets
        ):
            failures.append("material write scope mismatch")

        request_commands = set(request["validationCommands"])
        package_commands = set(material_package.get("validation_commands", []))
        receipt_commands = set(material_receipt.get("validationCommands", []))
        if not request_commands == package_commands == receipt_commands:
            failures.append("validation surface mismatch")

        boundary_checks = (
            ("lifecycleOwner", "lifecycle_owner", "lifecycle owner"),
            ("authorityClass", "authority_class", "authority class"),
            ("publicationClass", "publication_class", "publication class"),
        )
        for request_key, package_key, label in boundary_checks:
            expected = request[request_key]
            if material_package.get(package_key) != expected:
                failures.append(f"material package {label} mismatch")
            if material_receipt.get(request_key) != expected:
                failures.append(f"material receipt {label} mismatch")

    failures = sorted(set(failures))
    result["reasons"] = failures
    if not failures:
        result["admissionVerdict"] = "admit"
        result["mutationReady"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--request-schema", required=True)
    parser.add_argument("--receipt-schema", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    request = load_json(Path(args.request))
    request_schema = load_json(Path(args.request_schema))
    receipt_schema = load_json(Path(args.receipt_schema))
    result = resolve_mutation_admission(
        request, Path(args.repository_root), request_schema
    )
    receipt_failures = schema_errors(
        result, receipt_schema, "admission receipt"
    )
    if receipt_failures:
        raise ValueError("; ".join(receipt_failures))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["admissionVerdict"] in ("admit", "not-applicable") else 1


if __name__ == "__main__":
    raise SystemExit(main())
