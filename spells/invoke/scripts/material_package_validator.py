#!/usr/bin/env python3
"""Validate one staged Invoke material mutation package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(
    document: dict[str, Any], schema: dict[str, Any], label: str
) -> list[str]:
    return [
        f"{label} schema invalid at {'/'.join(map(str, error.path)) or '<root>'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def canonical_digest(document: Any) -> str:
    payload = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def resolve_staged_path(
    package_root: Path, raw_path: str
) -> tuple[Path | None, str | None]:
    normalized, error = normalized_relative_path(raw_path)
    if error:
        return None, error
    root = package_root.resolve()
    candidate = (root / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, f"path escape: {raw_path}"
    return candidate, None


def validate_exact_ref(
    package_root: Path,
    reference: dict[str, Any],
    label: str,
) -> tuple[bytes | None, list[str]]:
    errors: list[str] = []
    target, path_error = resolve_staged_path(package_root, reference["path"])
    if path_error:
        return None, [f"{label} {path_error}"]
    assert target is not None
    if not target.is_file():
        return None, [f"missing {label}: {reference['path']}"]
    content = target.read_bytes()
    actual_digest = hashlib.sha256(content).hexdigest()
    if actual_digest != reference["sha256"]:
        errors.append(f"{label} digest mismatch: {reference['path']}")
    if len(content) != reference["size_bytes"]:
        errors.append(f"{label} size mismatch: {reference['path']}")
    return content, errors


def proposal_only_receipt(document: dict[str, Any]) -> dict[str, Any]:
    metadata = receipt_metadata(document)
    receipt = {
        "schemaVersion": "1.0.0",
        "packageId": metadata["packageId"],
        "patchVerdict": "not-applicable",
        "mutationHandoff": "deferred",
        "packageDigest": None,
        "validatedPaths": [],
        "dependencyResult": "not-applicable",
        "ownerBoundaryResult": "pass",
        "publicationBoundaryResult": "pass",
        "validationCommands": metadata["validationCommands"],
        "lifecycleOwner": metadata["lifecycleOwner"],
        "authorityClass": metadata["authorityClass"],
        "publicationClass": metadata["publicationClass"],
        "reasons": [],
    }
    if metadata["planBinding"] is not None:
        receipt["planBinding"] = metadata["planBinding"]
    return receipt


def receipt_metadata(document: dict[str, Any]) -> dict[str, Any]:
    package_id = document.get("package_id")
    lifecycle_owner = document.get("lifecycle_owner")
    validation_commands = document.get("validation_commands")
    receipt = {
        "packageId": (
            package_id
            if isinstance(package_id, str) and package_id
            else "invalid-package"
        ),
        "lifecycleOwner": (
            lifecycle_owner
            if isinstance(lifecycle_owner, str) and lifecycle_owner
            else None
        ),
        "authorityClass": (
            document.get("authority_class")
            if document.get("authority_class") in ("public", "private")
            else None
        ),
        "publicationClass": (
            document.get("publication_class")
            if document.get("publication_class")
            in ("public", "private", "internal")
            else None
        ),
        "validationCommands": (
            sorted(
                {
                    command
                    for command in validation_commands
                    if isinstance(command, str) and command
                }
            )
            if isinstance(validation_commands, list)
            else []
        ),
        "planBinding": (
            document.get("plan_binding")
            if isinstance(document.get("plan_binding"), dict)
            else None
        ),
    }
    return receipt


def rejected_receipt(
    document: dict[str, Any],
    reasons: list[str],
    package_digest: str | None,
    dependency_result: str = "reject",
    owner_result: str = "reject",
    publication_result: str = "reject",
) -> dict[str, Any]:
    metadata = receipt_metadata(document)
    receipt = {
        "schemaVersion": "1.0.0",
        "packageId": metadata["packageId"],
        "patchVerdict": "reject",
        "mutationHandoff": "blocked",
        "packageDigest": package_digest,
        "validatedPaths": [],
        "dependencyResult": dependency_result,
        "ownerBoundaryResult": owner_result,
        "publicationBoundaryResult": publication_result,
        "validationCommands": metadata["validationCommands"],
        "lifecycleOwner": metadata["lifecycleOwner"],
        "authorityClass": metadata["authorityClass"],
        "publicationClass": metadata["publicationClass"],
        "reasons": sorted(set(reasons)),
    }
    if metadata["planBinding"] is not None:
        receipt["planBinding"] = metadata["planBinding"]
    return receipt


def validate_material_package(
    document: dict[str, Any],
    package_root: Path,
    package_schema: dict[str, Any],
    receipt_schema: dict[str, Any],
) -> dict[str, Any]:
    structural_errors = schema_errors(document, package_schema, "material package")
    if structural_errors:
        receipt = rejected_receipt(document, structural_errors, canonical_digest(document))
        receipt_errors = schema_errors(receipt, receipt_schema, "material receipt")
        if receipt_errors:
            raise ValueError("; ".join(receipt_errors))
        return receipt

    if document["mutation_state"] == "proposal-only":
        receipt = proposal_only_receipt(document)
        receipt_errors = schema_errors(receipt, receipt_schema, "material receipt")
        if receipt_errors:
            raise ValueError("; ".join(receipt_errors))
        return receipt

    reasons: list[str] = []
    dependency_reasons: list[str] = []
    owner_reasons: list[str] = []
    publication_reasons: list[str] = []
    output_by_target: dict[str, bytes] = {}
    normalized_targets: list[str] = []

    for source in document["source_artifacts"]:
        _, source_errors = validate_exact_ref(package_root, source, "source artifact")
        reasons.extend(source_errors)
        if (
            document["publication_class"] == "public"
            and source["authority_class"] != "public"
        ):
            publication_reasons.append(
                f"publication boundary violation: private source {source['path']} "
                "cannot feed public output"
            )

    dependency_by_id: dict[str, dict[str, Any]] = {}
    for dependency in document["dependencies"]:
        dependency_id = dependency["dependency_id"]
        if dependency_id in dependency_by_id:
            dependency_reasons.append(
                f"duplicate dependency id: {dependency_id}"
            )
            continue
        dependency_by_id[dependency_id] = dependency
        _, dependency_errors = validate_exact_ref(
            package_root, dependency["artifact_ref"], "dependency"
        )
        dependency_reasons.extend(dependency_errors)

    inventory_by_target: dict[str, dict[str, Any]] = {}
    for entry in document["target_inventory"]:
        target, target_error = normalized_relative_path(entry["target_path"])
        if target_error:
            reasons.append(f"target {target_error}")
            continue
        assert target is not None
        if target in inventory_by_target:
            reasons.append(f"duplicate target inventory path: {target}")
            continue
        inventory_by_target[target] = entry

    plan_binding = document.get("plan_binding")
    if plan_binding is not None:
        baseline_paths: list[str] = []
        for baseline in plan_binding["target_baselines"]:
            normalized, baseline_error = normalized_relative_path(baseline["path"])
            if baseline_error:
                reasons.append(f"target baseline {baseline_error}")
                continue
            assert normalized is not None
            if normalized != baseline["path"]:
                reasons.append(f"non-canonical target baseline path: {baseline['path']}")
            baseline_paths.append(normalized)
        if len(baseline_paths) != len(set(baseline_paths)):
            reasons.append("duplicate target baseline path")
        if set(baseline_paths) != set(inventory_by_target):
            reasons.append("target baseline inventory mismatch")
        if plan_binding["validation_contract_digest"] != canonical_digest(
            plan_binding["validation_contracts"]
        ):
            reasons.append("validation contract digest mismatch")

    approval = document["approval"]
    approved_scope: set[str] = set()
    for raw_path in approval["scope_paths"]:
        normalized, approval_path_error = normalized_relative_path(raw_path)
        if approval_path_error:
            owner_reasons.append(
                f"approval scope {approval_path_error}"
            )
            continue
        assert normalized is not None
        if normalized != raw_path:
            owner_reasons.append(
                f"non-canonical approval scope path: {raw_path}"
            )
        if normalized in approved_scope:
            owner_reasons.append(
                f"duplicate normalized approval scope path: {raw_path}"
            )
        approved_scope.add(normalized)
    if approval["owner"] != document["lifecycle_owner"]:
        owner_reasons.append(
            "approval owner mismatch: approval owner does not equal lifecycle owner"
        )

    for change in document["changes"]:
        target, target_error = normalized_relative_path(change["target_path"])
        if target_error:
            reasons.append(f"target {target_error}")
            continue
        assert target is not None
        if target in normalized_targets:
            reasons.append(f"duplicate change target: {target}")
            continue
        normalized_targets.append(target)

        inventory = inventory_by_target.get(target)
        if inventory is None:
            reasons.append(f"target inventory missing: {target}")
            continue

        output, output_errors = validate_exact_ref(
            package_root, change["output_ref"], "output"
        )
        reasons.extend(output_errors)
        if output is not None:
            if len(output) == 0:
                reasons.append(f"empty declared change: {target}")
            output_by_target[target] = output

        if inventory["lifecycle_owner"] != document["lifecycle_owner"]:
            owner_reasons.append(f"lifecycle owner mismatch: {target}")
        if inventory["authority_class"] != document["authority_class"]:
            owner_reasons.append(f"authority class mismatch: {target}")
        if inventory["publication_class"] != document["publication_class"]:
            publication_reasons.append(f"publication class mismatch: {target}")
        if inventory["authority_class"] not in approval["authority_classes"]:
            owner_reasons.append(f"approval authority scope mismatch: {target}")
        if inventory["publication_class"] not in approval["publication_classes"]:
            publication_reasons.append(
                f"approval publication scope mismatch: {target}"
            )
        for dependency_id in inventory["dependency_ids"]:
            if dependency_id not in dependency_by_id:
                dependency_reasons.append(
                    f"missing dependency: {dependency_id} required by {target}"
                )

    material_targets = set(normalized_targets)
    inventory_targets = set(inventory_by_target)
    if material_targets != inventory_targets:
        reasons.append(
            "material target inventory mismatch: changes and target inventory "
            "must contain exactly the same paths"
        )
    if not approved_scope == material_targets == inventory_targets:
        owner_reasons.append(
            "approval scope mismatch: approval scope, changes, and target "
            "inventory must contain exactly the same paths"
        )

    for mirror_group in document["mirror_groups"]:
        canonical_target, canonical_error = normalized_relative_path(
            mirror_group["canonical_target"]
        )
        if canonical_error:
            reasons.append(f"mirror canonical {canonical_error}")
            continue
        assert canonical_target is not None
        canonical_output = output_by_target.get(canonical_target)
        if canonical_output is None:
            reasons.append(
                f"mirror canonical target not materialized: {canonical_target}"
            )
            continue
        for generated_raw in mirror_group["generated_targets"]:
            generated_target, generated_error = normalized_relative_path(
                generated_raw
            )
            if generated_error:
                reasons.append(f"mirror generated {generated_error}")
                continue
            assert generated_target is not None
            generated_output = output_by_target.get(generated_target)
            if generated_output is None:
                reasons.append(
                    f"mirror generated target not materialized: {generated_target}"
                )
            elif generated_output != canonical_output:
                reasons.append(
                    f"mirror parity mismatch: {mirror_group['group_id']} "
                    f"{generated_target}"
                )

    reasons.extend(dependency_reasons)
    reasons.extend(owner_reasons)
    reasons.extend(publication_reasons)
    package_digest = canonical_digest(document)
    dependency_result = "reject" if dependency_reasons else "pass"
    owner_result = "reject" if owner_reasons else "pass"
    publication_result = "reject" if publication_reasons else "pass"

    if reasons:
        receipt = rejected_receipt(
            document,
            reasons,
            package_digest,
            dependency_result,
            owner_result,
            publication_result,
        )
    else:
        receipt = {
            "schemaVersion": "1.0.0",
            "packageId": document["package_id"],
            "patchVerdict": "pass",
            "mutationHandoff": "ready",
            "packageDigest": package_digest,
            "validatedPaths": sorted(normalized_targets),
            "dependencyResult": "pass",
            "ownerBoundaryResult": "pass",
            "publicationBoundaryResult": "pass",
            "validationCommands": document["validation_commands"],
            "lifecycleOwner": document["lifecycle_owner"],
            "authorityClass": document["authority_class"],
            "publicationClass": document["publication_class"],
            "reasons": [],
        }
        if document.get("plan_binding") is not None:
            receipt["planBinding"] = document["plan_binding"]

    receipt_errors = schema_errors(receipt, receipt_schema, "material receipt")
    if receipt_errors:
        raise ValueError("; ".join(receipt_errors))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package")
    parser.add_argument("--root", required=True)
    parser.add_argument("--schema-dir", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    schema_dir = Path(args.schema_dir)
    document = load_json(Path(args.package))
    receipt = validate_material_package(
        document,
        Path(args.root),
        load_json(schema_dir / "material-package.schema.json"),
        load_json(schema_dir / "material-package-receipt.schema.json"),
    )
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if receipt["patchVerdict"] != "reject" else 1


if __name__ == "__main__":
    raise SystemExit(main())
