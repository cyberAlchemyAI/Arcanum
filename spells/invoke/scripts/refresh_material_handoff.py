#!/usr/bin/env python3
"""Resolve Invoke Refresh handoff readiness from a material-package receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


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


def resolve_refresh_handoff(
    request: dict[str, Any], receipt_schema: dict[str, Any]
) -> dict[str, Any]:
    mutation_mode = request.get("mutationMode")
    authored_phase_status = request.get("authoredPhaseStatus")
    requested_handoff = request.get("requestedHandoff")
    receipt = request.get("materialReceipt")
    expected_package_id = request.get("expectedPackageId")
    expected_package_digest = request.get("expectedPackageDigest")

    if mutation_mode not in ("proposal-only", "apply-approved"):
        raise ValueError("mutationMode must be proposal-only or apply-approved")
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
            "mutationMode": mutation_mode,
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
        "mutationMode": mutation_mode,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--receipt-schema", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    result = resolve_refresh_handoff(
        load_json(Path(args.request)),
        load_json(Path(args.receipt_schema)),
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["phaseStatus"] in ("pass", "no-op") else 1


if __name__ == "__main__":
    raise SystemExit(main())
