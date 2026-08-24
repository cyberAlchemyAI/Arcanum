#!/usr/bin/env python3
"""Bind routed Task Session writes to live controls and optional material evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


MUTATION_MODES = {"routed-mutation", "reusable-mutation"}
PLAN_MANIFEST_SCHEMA_ID = (
    "https://arcanum.dev/schemas/work-pack-readiness-audit/"
    "plan-semantic-manifest/1-0-0"
)
SELECTION_RECEIPT_SCHEMA_ID = (
    "https://arcanum.dev/schemas/work-pack-readiness-audit/"
    "selection-receipt/1-0-0"
)


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


def scopes_overlap(left: str, right: str) -> bool:
    left_path = PurePosixPath(left)
    right_path = PurePosixPath(right)
    return (
        left_path == right_path
        or left_path in right_path.parents
        or right_path in left_path.parents
    )


def transient_output_failures(
    repository_root: Path,
    transient_outputs: set[str],
    material_writes: set[str],
    execution_outputs: set[str],
) -> list[str]:
    failures: list[str] = []
    root = repository_root.resolve()
    transients = sorted(transient_outputs)
    for index, raw in enumerate(transients):
        candidate = (root / raw).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError:
            failures.append(f"transient output path escape: {raw}")
            continue
        current = root
        for part in PurePosixPath(raw).parts:
            current /= part
            if os.path.lexists(current) and current.is_symlink():
                failures.append(f"transient output traverses symbolic link: {raw}")
                break
        if os.path.lexists(root / raw):
            failures.append(f"transient output is not absent: {raw}")
        for other in transients[index + 1 :]:
            if scopes_overlap(raw, other):
                failures.append(f"transient output scopes overlap: {raw} and {other}")
        for durable in sorted(material_writes | (execution_outputs - transient_outputs)):
            if scopes_overlap(raw, durable):
                failures.append(
                    f"transient output overlaps durable scope: {raw} and {durable}"
                )
    return failures


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


def context_contract_failures(
    contract: Any,
    request: dict[str, Any],
    write_profile: str,
    material_writes: set[str],
    execution_outputs: set[str],
    transient_outputs: set[str],
    allowed_writes: set[str],
) -> list[str]:
    if not isinstance(contract, dict):
        return ["context pack execution contract is missing or invalid"]
    failures: list[str] = []
    if contract.get("writeProfile") != write_profile:
        failures.append("context pack write profile mismatch")
    for key, label, expected in (
        ("materialWrites", "material write", material_writes),
        ("executionOutputs", "execution output", execution_outputs),
        ("allowedWrites", "allowed write", allowed_writes),
    ):
        raw = contract.get(key)
        if not isinstance(raw, list) or any(not isinstance(item, str) for item in raw):
            failures.append(f"context pack {label} scope is invalid")
            continue
        normalized, errors = normalized_write_set({key: raw}, key, label)
        failures.extend(f"context pack {error}" for error in errors)
        if normalized != expected:
            failures.append(f"context pack {label} scope mismatch")
    if request.get("schemaVersion") == "1.3.0":
        raw_transients = contract.get("transientOutputs")
        if not isinstance(raw_transients, list) or any(
            not isinstance(item, str) for item in raw_transients
        ):
            failures.append("context pack transient output scope is invalid")
        else:
            normalized, errors = normalized_write_set(
                {"transientOutputs": raw_transients},
                "transientOutputs",
                "transient output",
            )
            failures.extend(f"context pack {error}" for error in errors)
            if normalized != transient_outputs:
                failures.append("context pack transient output scope mismatch")
    commands = contract.get("validationCommands")
    if (
        not isinstance(commands, list)
        or any(not isinstance(item, str) or not item for item in commands)
        or commands != request["validationCommands"]
    ):
        failures.append("context pack validation surface mismatch")
    for key, label in (
        ("lifecycleOwner", "lifecycle owner"),
        ("authorityClass", "authority class"),
        ("publicationClass", "publication class"),
    ):
        if contract.get(key) != request[key]:
            failures.append(f"context pack {label} mismatch")
    return failures


def base_receipt(
    request: dict[str, Any],
    request_digest: str | None,
) -> dict[str, Any]:
    request_version = request.get("schemaVersion")
    receipt_version = request_version if request_version in {"1.2.0", "1.3.0"} else "1.2.0"
    execution_mode = request.get("executionMode", "invalid")
    if execution_mode not in MUTATION_MODES | {"standalone-nonmutating"}:
        execution_mode = "invalid"
    receipt = {
        "schemaVersion": receipt_version,
        "executionMode": execution_mode,
        "writeProfile": (
            "nonmutating"
            if execution_mode == "standalone-nonmutating"
            else "invalid"
        ),
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
    if receipt_version == "1.3.0":
        receipt["transientOutputs"] = sorted(
            {
                item
                for item in request.get("transientOutputs", [])
                if isinstance(item, str) and item
            }
        )
    if request.get("admissionProfile") == "plan-once-selected-unit":
        plan = request.get("planAdmission", {})
        receipt.update(
            {
                "admissionProfile": "plan-once-selected-unit",
                "planEpochId": plan.get("planEpochId"),
                "unitContractDigest": plan.get("unitContractDigest"),
                "attemptId": plan.get("attemptId"),
                "planManifestDigest": None,
                "selectionReceiptDigest": None,
                "targetBaselineDigest": None,
                "targetBaselines": plan.get("targetBaselines"),
                "validationContractDigest": plan.get(
                    "validationContractDigest"
                ),
                "admissionToken": None,
                "singleUse": True,
            }
        )
    return receipt


def live_baseline_failures(
    repository_root: Path, baselines: list[dict[str, Any]]
) -> list[str]:
    failures: list[str] = []
    root = repository_root.resolve()
    observed: set[str] = set()
    for baseline in baselines:
        normalized, path_error = normalized_relative_path(baseline["path"])
        if path_error:
            failures.append(f"target baseline {path_error}")
            continue
        assert normalized is not None
        if normalized != baseline["path"]:
            failures.append(f"non-canonical target baseline path: {baseline['path']}")
        if normalized in observed:
            failures.append(f"duplicate target baseline path: {normalized}")
        observed.add(normalized)
        candidate = (root / normalized).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError:
            failures.append(f"target baseline path escape: {baseline['path']}")
            continue
        if baseline["state"] == "absent":
            if candidate.exists():
                failures.append(f"target baseline changed from absent: {normalized}")
            continue
        if not candidate.is_file():
            failures.append(f"target baseline changed from present: {normalized}")
            continue
        content = candidate.read_bytes()
        if byte_digest(content) != baseline["sha256"]:
            failures.append(f"target baseline digest mismatch: {normalized}")
        if len(content) != baseline["sizeBytes"]:
            failures.append(f"target baseline size mismatch: {normalized}")
    return failures


def validate_plan_admission(
    request: dict[str, Any],
    repository_root: Path,
    material_package: dict[str, Any] | None,
    material_receipt: dict[str, Any] | None,
    result: dict[str, Any],
) -> list[str]:
    if request.get("admissionProfile") != "plan-once-selected-unit":
        return []
    plan = request["planAdmission"]
    failures: list[str] = []
    documents: dict[str, dict[str, Any] | None] = {}
    contents: dict[str, bytes | None] = {}
    for key, label in (
        ("planManifestSchema", "plan manifest schema"),
        ("planManifest", "plan semantic manifest"),
        ("selectionReceiptSchema", "selection receipt schema"),
        ("selectionReceipt", "selection receipt"),
    ):
        content, errors = read_exact_artifact(repository_root, plan[key], label)
        failures.extend(errors)
        document = None
        if content is not None and not errors:
            document, parse_errors = parse_json_bytes(content, label)
            failures.extend(parse_errors)
        contents[key] = content
        documents[key] = document

    manifest = documents["planManifest"]
    manifest_schema = documents["planManifestSchema"]
    selection = documents["selectionReceipt"]
    selection_schema = documents["selectionReceiptSchema"]
    if contents["planManifest"] is not None:
        result["planManifestDigest"] = byte_digest(contents["planManifest"])
    if contents["selectionReceipt"] is not None:
        result["selectionReceiptDigest"] = byte_digest(
            contents["selectionReceipt"]
        )
    if manifest is not None and manifest_schema is not None:
        if manifest_schema.get("$id") != PLAN_MANIFEST_SCHEMA_ID:
            failures.append("plan manifest schema identity mismatch")
        failures.extend(schema_errors(manifest, manifest_schema, "plan manifest"))
    if selection is not None and selection_schema is not None:
        if selection_schema.get("$id") != SELECTION_RECEIPT_SCHEMA_ID:
            failures.append("selection receipt schema identity mismatch")
        failures.extend(
            schema_errors(selection, selection_schema, "selection receipt")
        )

    expected_epoch = plan["planEpochId"]
    expected_unit = plan["unitContractDigest"]
    if manifest is not None:
        if manifest.get("plan_epoch_id") != expected_epoch:
            failures.append("plan manifest epoch mismatch")
        if not (
            manifest.get("authority_effect") == "none"
            and manifest.get("mutation_ready") is False
            and manifest.get("selected_unit") is None
        ):
            failures.append("plan manifest authority ceiling mismatch")
        if expected_unit not in manifest.get("unit_contract_digests", {}).values():
            failures.append("unit contract digest is absent from plan manifest")
    if selection is not None:
        if not (
            selection.get("selectionVerdict") == "select"
            and selection.get("terminalCode") == "SELECTION_READY"
            and selection.get("authorityEffect") == "none"
            and selection.get("mutationReady") is False
        ):
            failures.append("selection receipt does not select a non-authoritative unit")
        for key, expected, label in (
            ("taskId", request["taskId"], "task id"),
            ("swuId", request["swuId"], "SWU id"),
            ("planEpochId", expected_epoch, "plan epoch"),
            ("unitContractDigest", expected_unit, "unit contract digest"),
        ):
            if selection.get(key) != expected:
                failures.append(f"selection receipt {label} mismatch")
        if selection.get("manifestDigest") != result["planManifestDigest"]:
            failures.append("selection receipt manifest digest mismatch")

    request_baselines = plan["targetBaselines"]
    baseline_paths, baseline_path_errors = normalized_write_set(
        {"targetBaselines": [item["path"] for item in request_baselines]},
        "targetBaselines",
        "target baseline",
    )
    failures.extend(baseline_path_errors)
    material_paths, _ = normalized_write_set(
        request, "materialWrites", "material write"
    )
    execution_output_paths, _ = normalized_write_set(
        request, "executionOutputs", "execution output"
    )
    write_profile = result["writeProfile"]
    baseline_target_paths = (
        material_paths
        if write_profile == "material-bound"
        else execution_output_paths
    )
    baseline_target_label = (
        "material writes"
        if write_profile == "material-bound"
        else "execution outputs"
    )
    if baseline_paths != baseline_target_paths:
        failures.append(
            "target baseline inventory does not equal " + baseline_target_label
        )
    failures.extend(live_baseline_failures(repository_root, request_baselines))
    target_digest = canonical_digest(request_baselines)
    result["targetBaselineDigest"] = target_digest

    validation_digest = canonical_digest(plan["structuredValidationContracts"])
    if plan["validationContractDigest"] != validation_digest:
        failures.append("validation contract digest mismatch")

    if write_profile == "material-bound":
        package_binding = (
            material_package.get("plan_binding") if material_package else None
        )
        receipt_binding = (
            material_receipt.get("planBinding") if material_receipt else None
        )
        expected_binding = {
            "task_id": request["taskId"],
            "swu_id": request["swuId"],
            "plan_epoch_id": expected_epoch,
            "unit_contract_digest": expected_unit,
            "selection_receipt_digest": result["selectionReceiptDigest"],
            "attempt_id": plan["attemptId"],
            "validation_contract_digest": plan["validationContractDigest"],
            "validation_contracts": plan["structuredValidationContracts"],
            "target_baselines": [
                {
                    "path": item["path"],
                    "state": item["state"],
                    "sha256": item["sha256"],
                    "size_bytes": item["sizeBytes"],
                }
                for item in request_baselines
            ],
        }
        if package_binding != expected_binding:
            failures.append("material package plan binding mismatch")
        if receipt_binding != expected_binding:
            failures.append("material receipt plan binding mismatch")
    elif write_profile != "execution-output-only":
        failures.append("plan admission write profile is invalid")

    if not failures:
        result["admissionToken"] = canonical_digest(
            {
                "requestDigest": result["requestDigest"],
                "selectionReceiptDigest": result["selectionReceiptDigest"],
                "attemptId": plan["attemptId"],
                "targetBaselineDigest": target_digest,
                "validationContractDigest": validation_digest,
            }
        )
    return failures


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
    transient_outputs: set[str] = set()
    transient_output_errors: list[str] = []
    if request["schemaVersion"] == "1.3.0":
        transient_outputs, transient_output_errors = normalized_write_set(
            request, "transientOutputs", "transient output"
        )
    allowed_writes, allowed_write_errors = normalized_write_set(
        request, "allowedWrites", "allowed write"
    )
    failures.extend(material_write_errors)
    failures.extend(execution_output_errors)
    failures.extend(transient_output_errors)
    failures.extend(allowed_write_errors)
    if material_writes & execution_outputs:
        failures.append("material and execution write scopes overlap")
    if not transient_outputs <= execution_outputs:
        failures.append("transient outputs are not a subset of execution outputs")
    failures.extend(
        transient_output_failures(
            repository_root,
            transient_outputs,
            material_writes,
            execution_outputs,
        )
    )
    if material_writes | execution_outputs != allowed_writes:
        failures.append("allowed write scope partition mismatch")
    if material_writes:
        write_profile = "material-bound"
    elif execution_outputs:
        write_profile = "execution-output-only"
    else:
        write_profile = "invalid"
        failures.append("no writable partition declared")
    result["writeProfile"] = write_profile

    artifacts: dict[str, tuple[bytes | None, dict[str, Any] | None]] = {}
    producer_schema: dict[str, Any] | None = None
    material_receipt: dict[str, Any] | None = None
    material_package: dict[str, Any] | None = None
    if write_profile == "material-bound":
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
                failures.extend(
                    context_contract_failures(
                        context_pack.get("execution_contract"),
                        request,
                        write_profile,
                        material_writes,
                        execution_outputs,
                        transient_outputs,
                        allowed_writes,
                    )
                )

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

    failures.extend(
        validate_plan_admission(
            request,
            repository_root,
            material_package,
            material_receipt,
            result,
        )
    )

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
