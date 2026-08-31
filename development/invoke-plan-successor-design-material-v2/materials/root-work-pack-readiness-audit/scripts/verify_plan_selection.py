#!/usr/bin/env python3
"""Select one currently eligible unit from an audited semantic plan epoch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator

from plan_semantics import PlanSemanticError, build_plan_semantics, canonical_digest


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot load {label}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def schema_errors(value: Any, schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} invalid at "
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(value),
            key=lambda item: list(item.absolute_path),
        )
    ]


def resolve_path(root: Path, raw: str, label: str) -> Path:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
        or ".." in path.parts
        or str(path) in ("", ".")
    ):
        raise ValueError(f"{label} path escape: {raw}")
    root = root.resolve()
    candidate = (root / path).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"{label} path escape: {raw}") from error
    return candidate


def read_exact(root: Path, reference: dict[str, Any], label: str) -> bytes:
    path = resolve_path(root, reference["path"], label)
    if not path.is_file():
        raise ValueError(f"missing {label}: {reference['path']}")
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise ValueError(f"{label} digest mismatch: {reference['path']}")
    if len(content) != reference["size_bytes"]:
        raise ValueError(f"{label} size mismatch: {reference['path']}")
    return content


def base_receipt(request: dict[str, Any]) -> dict[str, Any]:
    try:
        request_digest: str | None = canonical_digest(request)
    except PlanSemanticError:
        request_digest = None
    return {
        "schemaVersion": "1.0.0",
        "selectionVerdict": "block",
        "terminalCode": "SELECTION_REQUEST_INVALID",
        "requestDigest": request_digest,
        "manifestDigest": None,
        "planEpochId": None,
        "canonicalSemanticDigest": None,
        "taskId": request.get("taskId"),
        "swuId": request.get("swuId"),
        "unitContractDigest": None,
        "dependencyReceiptDigests": [],
        "lifecycleEligibilityDigest": None,
        "explicitConfirmationDigest": None,
        "selectionIntentSource": "invalid",
        "selectionIntentDigest": None,
        "authorityEffect": "none",
        "mutationReady": False,
        "reasons": [],
    }


def select_unit(
    request: dict[str, Any],
    repository_root: Path,
    request_schema: dict[str, Any],
    manifest_schema: dict[str, Any],
    config_schema: dict[str, Any],
) -> dict[str, Any]:
    receipt = base_receipt(request)
    failures = schema_errors(request, request_schema, "selection request")
    codes: list[str] = []
    if failures:
        receipt["reasons"] = failures
        return receipt

    try:
        manifest_bytes = read_exact(
            repository_root, request["manifestRef"], "plan semantic manifest"
        )
        manifest = json.loads(manifest_bytes)
        failures.extend(schema_errors(manifest, manifest_schema, "plan manifest"))
        receipt["manifestDigest"] = hashlib.sha256(manifest_bytes).hexdigest()
        if isinstance(manifest, dict):
            receipt["planEpochId"] = manifest.get("plan_epoch_id")
            receipt["canonicalSemanticDigest"] = manifest.get(
                "canonical_semantic_digest"
            )
        config_path = resolve_path(
            repository_root, request["auditConfigPath"], "audit config"
        )
        config = load_object(config_path, "audit config")
        config_failures = schema_errors(config, config_schema, "audit config")
        if config_failures:
            codes.append("CURRENT_PLAN_CONFIG_INVALID")
            failures.extend(config_failures)
            semantics = None
        else:
            semantics = build_plan_semantics(config, repository_root)
    except (ValueError, json.JSONDecodeError, PlanSemanticError) as error:
        codes.append("SELECTION_INPUT_INVALID")
        failures.append(str(error))
        manifest = None
        config = None
        semantics = None

    if isinstance(manifest, dict):
        if not (
            manifest.get("authority_effect") == "none"
            and manifest.get("mutation_ready") is False
            and manifest.get("selected_unit") is None
            and manifest.get("selection_required") is True
        ):
            codes.append("MANIFEST_AUTHORITY_CEILING_INVALID")
            failures.append("plan manifest exceeds the non-authoritative selection ceiling")

    selected_unit: dict[str, Any] | None = None
    if isinstance(config, dict):
        matches = [
            unit
            for unit in config["execution_bindings"]
            if unit.get("task_id") == request["taskId"]
            and unit.get("swu_id") == request["swuId"]
        ]
        if len(matches) != 1:
            codes.append("SELECTED_UNIT_NOT_UNIQUE")
            failures.append("task and SWU do not identify exactly one audited unit")
        else:
            selected_unit = matches[0]

    if semantics is not None and isinstance(manifest, dict):
        if semantics["normalizer_version"] != manifest.get("normalizer_version"):
            codes.append("NORMALIZER_VERSION_CHANGED")
            failures.append("semantic normalizer version changed")
        if semantics["canonical_semantic_digest"] != manifest.get(
            "canonical_semantic_digest"
        ):
            codes.append("PLAN_EPOCH_STALE")
            failures.append("current semantic plan differs from the audited epoch")
        if semantics["semantic_component_digests"] != manifest.get(
            "semantic_component_digests"
        ):
            codes.append("PLAN_COMPONENT_CHANGED")
            failures.append("one or more semantic plan components changed")
        if semantics["unit_contract_digests"] != manifest.get(
            "unit_contract_digests"
        ):
            codes.append("UNIT_CONTRACT_CHANGED")
            failures.append("one or more audited unit contracts changed")

    if selected_unit is not None and isinstance(manifest, dict):
        unit_id = selected_unit["unit_id"]
        if unit_id not in manifest.get("ready_frontier", []):
            codes.append("UNIT_OUTSIDE_READY_FRONTIER")
            failures.append("selected unit is outside the audited ready frontier")
        digest = manifest.get("unit_contract_digests", {}).get(unit_id)
        if isinstance(digest, str):
            receipt["unitContractDigest"] = digest
        else:
            codes.append("UNIT_DIGEST_MISSING")
            failures.append("selected unit digest is absent from the manifest")

        dependencies = request["dependencyReceipts"]
        if {item["dependencyId"] for item in dependencies} != set(
            selected_unit["dependencies"]
        ):
            codes.append("DEPENDENCY_FRONTIER_INCOMPLETE")
            failures.append("current dependency receipt inventory is incomplete or extra")

    for item in request["dependencyReceipts"]:
        try:
            content = read_exact(
                repository_root,
                item["artifactRef"],
                f"dependency receipt {item['dependencyId']}",
            )
            receipt["dependencyReceiptDigests"].append(
                hashlib.sha256(content).hexdigest()
            )
        except ValueError as error:
            codes.append("DEPENDENCY_RECEIPT_STALE")
            failures.append(str(error))
    receipt["dependencyReceiptDigests"].sort()

    for reference in request["lifecycleEligibility"]["evidenceRefs"]:
        try:
            read_exact(repository_root, reference, "lifecycle eligibility evidence")
        except ValueError as error:
            codes.append("LIFECYCLE_EVIDENCE_STALE")
            failures.append(str(error))
    receipt["lifecycleEligibilityDigest"] = canonical_digest(
        request["lifecycleEligibility"]
    )
    if "executionIntentBinding" in request:
        intent = request["executionIntentBinding"]
        receipt["selectionIntentSource"] = "execution-intent-binding"
        receipt["selectionIntentDigest"] = canonical_digest(intent)
        if isinstance(manifest, dict) and intent["workPackId"] != manifest.get(
            "work_pack_id"
        ):
            codes.append("EXECUTION_BINDING_WORK_PACK_MISMATCH")
            failures.append("execution intent binding names a different Work Pack")
    else:
        receipt["selectionIntentSource"] = "explicit-confirmation"
        receipt["selectionIntentDigest"] = canonical_digest(
            request["explicitConfirmation"]
        )
        receipt["explicitConfirmationDigest"] = receipt["selectionIntentDigest"]

    failures = sorted(set(failures))
    receipt["reasons"] = failures
    if failures:
        receipt["terminalCode"] = codes[0] if codes else "SELECTION_INPUT_INVALID"
    else:
        receipt["selectionVerdict"] = "select"
        receipt["terminalCode"] = "SELECTION_READY"
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--request-schema", required=True, type=Path)
    parser.add_argument("--receipt-schema", required=True, type=Path)
    parser.add_argument("--manifest-schema", required=True, type=Path)
    parser.add_argument("--config-schema", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    request = load_object(args.request, "selection request")
    receipt = select_unit(
        request,
        args.repository_root,
        load_object(args.request_schema, "selection request schema"),
        load_object(args.manifest_schema, "plan manifest schema"),
        load_object(args.config_schema, "audit config schema"),
    )
    receipt_errors = schema_errors(
        receipt,
        load_object(args.receipt_schema, "selection receipt schema"),
        "selection receipt",
    )
    if receipt_errors:
        raise ValueError("; ".join(receipt_errors))
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if receipt["selectionVerdict"] == "select" else 2


if __name__ == "__main__":
    raise SystemExit(main())
