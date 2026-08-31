#!/usr/bin/env python3
"""Resolve Invoke Refresh handoff readiness from a material-package receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from material_package_validator import canonical_digest, validate_material_package

MUTATION_MODES = ("proposal-only", "apply-approved")
ACTIVATION_SOURCES = ("direct-user", "delegated", "continuation")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def receipt_schema_errors(
    receipt: dict[str, Any], receipt_schema: dict[str, Any]
) -> list[str]:
    return [
        "material receipt schema invalid at "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(receipt_schema).iter_errors(receipt),
            key=lambda item: list(item.path),
        )
    ]


def material_binding(
    required: bool,
    receipt: dict[str, Any] | None,
    schema_valid: bool | None,
    expected_package_id: str | None,
    expected_package_digest: str | None,
) -> dict[str, Any]:
    return {
        "required": required,
        "receiptPresent": receipt is not None,
        "schemaValid": schema_valid,
        "patchVerdict": (
            receipt.get("patchVerdict")
            if receipt is not None
            else ("not-applicable" if not required else None)
        ),
        "mutationHandoff": (
            receipt.get("mutationHandoff") if receipt is not None else None
        ),
        "packageId": receipt.get("packageId") if receipt is not None else None,
        "packageDigest": (
            receipt.get("packageDigest") if receipt is not None else None
        ),
        "expectedPackageId": expected_package_id,
        "expectedPackageDigest": expected_package_digest,
        "validatedPaths": (
            receipt.get("validatedPaths", []) if receipt is not None else []
        ),
        "dependencyResult": (
            receipt.get("dependencyResult")
            if receipt is not None
            else ("not-applicable" if not required else None)
        ),
        "ownerBoundaryResult": (
            receipt.get("ownerBoundaryResult") if receipt is not None else None
        ),
        "publicationBoundaryResult": (
            receipt.get("publicationBoundaryResult")
            if receipt is not None
            else None
        ),
        "validationCommands": (
            receipt.get("validationCommands", []) if receipt is not None else []
        ),
        "lifecycleOwner": (
            receipt.get("lifecycleOwner") if receipt is not None else None
        ),
        "authorityClass": (
            receipt.get("authorityClass") if receipt is not None else None
        ),
        "publicationClass": (
            receipt.get("publicationClass") if receipt is not None else None
        ),
    }


def resolve_mutation_mode(
    request: dict[str, Any],
) -> tuple[str, str | None, str]:
    explicit_mode = request.get("mutationMode")
    activation_source = request.get("activationSource")

    if activation_source is not None and activation_source not in ACTIVATION_SOURCES:
        raise ValueError(
            "activationSource must be direct-user, delegated, or continuation"
        )
    if explicit_mode is not None:
        if explicit_mode not in MUTATION_MODES:
            raise ValueError(
                "mutationMode must be proposal-only or apply-approved"
            )
        return explicit_mode, activation_source, "explicit"
    if activation_source == "direct-user":
        return "apply-approved", activation_source, "default-direct-user"
    if activation_source in ("delegated", "continuation"):
        return "proposal-only", activation_source, "default-non-user"
    raise ValueError(
        "activationSource is required when mutationMode is omitted"
    )


def resolve_refresh_handoff(
    request: dict[str, Any], receipt_schema: dict[str, Any]
) -> dict[str, Any]:
    mutation_mode, activation_source, mutation_mode_source = (
        resolve_mutation_mode(request)
    )
    authored_phase_status = request.get("authoredPhaseStatus")
    requested_handoff = request.get("requestedHandoff")
    receipt = request.get("materialReceipt")
    expected_package_id = request.get("expectedPackageId")
    expected_package_digest = request.get("expectedPackageDigest")

    if authored_phase_status not in ("pass", "flag", "block", "no-op"):
        raise ValueError("authoredPhaseStatus is invalid")
    if requested_handoff not in (
        "ready",
        "gated",
        "deferred",
        "blocked",
        "not-needed",
    ):
        raise ValueError("requestedHandoff is invalid")
    if receipt is not None and not isinstance(receipt, dict):
        raise ValueError("materialReceipt must be an object or null")

    if mutation_mode == "proposal-only":
        handoff_status = (
            requested_handoff
            if requested_handoff in ("gated", "deferred", "not-needed")
            else "gated"
        )
        return {
            "schemaVersion": "1.0.0",
            "activationSource": activation_source,
            "mutationMode": mutation_mode,
            "mutationModeSource": mutation_mode_source,
            "phaseStatus": authored_phase_status,
            "handoffStatus": handoff_status,
            "mutationReady": False,
            "materialPackage": material_binding(
                False, receipt, None, expected_package_id, expected_package_digest
            ),
            "blockers": [],
        }

    blockers: list[str] = []
    schema_valid: bool | None = None
    if authored_phase_status != "pass":
        blockers.append("authored Refresh phase is not pass")
    if requested_handoff != "ready":
        blockers.append("apply-approved handoff request is not ready")
    if not isinstance(expected_package_id, str) or not expected_package_id:
        blockers.append("expected material package id missing")
    if (
        not isinstance(expected_package_digest, str)
        or len(expected_package_digest) != 64
    ):
        blockers.append("expected material package digest missing or invalid")

    if receipt is None:
        blockers.append("material receipt missing")
    else:
        schema_failures = receipt_schema_errors(receipt, receipt_schema)
        schema_valid = not schema_failures
        blockers.extend(schema_failures)
        if schema_valid:
            if receipt["packageId"] != expected_package_id:
                blockers.append("material package id mismatch")
            if receipt["packageDigest"] != expected_package_digest:
                blockers.append("material package digest mismatch")
            if receipt["patchVerdict"] != "pass":
                blockers.append("material patch verdict is not pass")
            if receipt["mutationHandoff"] != "ready":
                blockers.append("material mutation handoff is not ready")
            if receipt["reasons"]:
                blockers.append("material receipt contains rejection reasons")
            if receipt["dependencyResult"] != "pass":
                blockers.append("material dependency result is not pass")
            if receipt["ownerBoundaryResult"] != "pass":
                blockers.append("material owner boundary result is not pass")
            if receipt["publicationBoundaryResult"] != "pass":
                blockers.append(
                    "material publication boundary result is not pass"
                )
            if not receipt["validatedPaths"]:
                blockers.append("material validated paths are empty")
            if not receipt["validationCommands"]:
                blockers.append("material validation commands are empty")

    blockers = sorted(set(blockers))
    mutation_ready = not blockers
    return {
        "schemaVersion": "1.0.0",
        "activationSource": activation_source,
        "mutationMode": mutation_mode,
        "mutationModeSource": mutation_mode_source,
        "phaseStatus": "pass" if mutation_ready else "block",
        "handoffStatus": "ready" if mutation_ready else "blocked",
        "mutationReady": mutation_ready,
        "materialPackage": material_binding(
            True,
            receipt,
            schema_valid,
            expected_package_id,
            expected_package_digest,
        ),
        "blockers": blockers,
    }


def resolve_file_bound_refresh_handoff(
    request: dict[str, Any],
    receipt_schema: dict[str, Any],
    material_package: dict[str, Any] | None,
    package_root: Path | None,
    package_schema: dict[str, Any] | None,
    material_receipt: dict[str, Any] | None,
    material_receipt_bytes: bytes | None,
) -> dict[str, Any]:
    """Revalidate current material bytes and reject stale embedded handoffs."""
    mutation_mode, _, _ = resolve_mutation_mode(request)
    if mutation_mode != "apply-approved":
        return resolve_refresh_handoff(request, receipt_schema)

    coherence_blockers: list[str] = []
    expected_package_id = request.get("expectedPackageId")
    expected_package_digest = request.get("expectedPackageDigest")
    expected_receipt_digest = request.get("expectedMaterialReceiptSha256")
    if (
        not isinstance(expected_receipt_digest, str)
        or len(expected_receipt_digest) != 64
        or any(character not in "0123456789abcdef" for character in expected_receipt_digest)
    ):
        coherence_blockers.append(
            "expected material receipt file digest missing or invalid"
        )
    if material_package is None or package_root is None or package_schema is None:
        coherence_blockers.append("current material package validation inputs missing")
        current_receipt = None
    else:
        if material_package.get("package_id") != expected_package_id:
            coherence_blockers.append("current material package id mismatch")
        current_package_digest = canonical_digest(material_package)
        if current_package_digest != expected_package_digest:
            coherence_blockers.append("current material package digest mismatch")
        current_receipt = validate_material_package(
            material_package, package_root, package_schema, receipt_schema
        )
    if material_receipt is None or material_receipt_bytes is None:
        coherence_blockers.append("current material receipt file missing")
    else:
        actual_receipt_digest = hashlib.sha256(material_receipt_bytes).hexdigest()
        if expected_receipt_digest != actual_receipt_digest:
            coherence_blockers.append("material receipt file digest mismatch")
        if current_receipt != material_receipt:
            coherence_blockers.append(
                "material receipt does not match current package/source validation"
            )
        if current_receipt is not None:
            fresh_receipt_bytes = (
                json.dumps(current_receipt, indent=2, sort_keys=True) + "\n"
            ).encode("utf-8")
            if material_receipt_bytes != fresh_receipt_bytes:
                coherence_blockers.append(
                    "material receipt bytes do not equal fresh validator output"
                )
        if request.get("materialReceipt") != material_receipt:
            coherence_blockers.append(
                "material handoff request embeds stale material receipt"
            )

    effective_request = dict(request)
    effective_request["materialReceipt"] = material_receipt
    result = resolve_refresh_handoff(effective_request, receipt_schema)
    blockers = sorted(set(result["blockers"] + coherence_blockers))
    if blockers:
        result["phaseStatus"] = "block"
        result["handoffStatus"] = "blocked"
        result["mutationReady"] = False
        result["blockers"] = blockers
    result["materialReceiptBinding"] = {
        "expectedSha256": request.get("expectedMaterialReceiptSha256"),
        "actualSha256": (
            hashlib.sha256(material_receipt_bytes).hexdigest()
            if material_receipt_bytes is not None
            else None
        ),
        "currentPackageRevalidated": current_receipt is not None,
        "receiptMatchesCurrentValidation": (
            current_receipt is not None
            and material_receipt is not None
            and current_receipt == material_receipt
        ),
        "requestEmbedsCurrentReceipt": (
            material_receipt is not None
            and request.get("materialReceipt") is not None
            and request.get("materialReceipt") == material_receipt
        ),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--receipt-schema", required=True)
    parser.add_argument("--material-package")
    parser.add_argument("--package-root")
    parser.add_argument("--package-schema")
    parser.add_argument("--material-receipt")
    parser.add_argument("--output")
    args = parser.parse_args()

    request = load_json(Path(args.request))
    mutation_mode, _, _ = resolve_mutation_mode(request)
    if mutation_mode == "proposal-only":
        result = resolve_refresh_handoff(
            request, load_json(Path(args.receipt_schema))
        )
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0 if result["phaseStatus"] in ("pass", "no-op") else 1

    material_package_path = (
        Path(args.material_package) if args.material_package else None
    )
    package_schema_path = Path(args.package_schema) if args.package_schema else None
    material_receipt_path = Path(args.material_receipt) if args.material_receipt else None
    material_receipt_bytes = None
    material_receipt = None
    if material_receipt_path is not None and material_receipt_path.is_file():
        material_receipt_bytes = material_receipt_path.read_bytes()
        try:
            material_receipt = json.loads(material_receipt_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            material_receipt = None
    material_package = None
    if material_package_path is not None and material_package_path.is_file():
        try:
            material_package = load_json(material_package_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            material_package = None
    package_schema = None
    if package_schema_path is not None and package_schema_path.is_file():
        try:
            package_schema = load_json(package_schema_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            package_schema = None
    result = resolve_file_bound_refresh_handoff(
        request,
        load_json(Path(args.receipt_schema)),
        material_package,
        Path(args.package_root) if args.package_root else None,
        package_schema,
        material_receipt,
        material_receipt_bytes,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["phaseStatus"] in ("pass", "no-op") else 1


if __name__ == "__main__":
    raise SystemExit(main())
