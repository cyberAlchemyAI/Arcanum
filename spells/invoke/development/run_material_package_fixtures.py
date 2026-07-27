#!/usr/bin/env python3
"""Run causal fixtures for the Invoke material-package validator."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

DEVELOPMENT_DIR = Path(__file__).resolve().parent
INVOKE_DIR = DEVELOPMENT_DIR.parent
REPOSITORY_ROOT = INVOKE_DIR.parents[2]
SCRIPTS_DIR = INVOKE_DIR / "scripts"

import sys

sys.path.insert(0, str(SCRIPTS_DIR))

from material_package_validator import load_json, validate_material_package
from refresh_material_handoff import resolve_refresh_handoff


TARGETS = (
    "arcanum/spells/invoke/refresh.md",
    ".agents/skills/invoke/refresh.md",
    ".claude/skills/invoke/refresh.md",
)

RUNTIME_SUPPORT_PATHS = (
    "refresh.md",
    "scripts/material_package_validator.py",
    "scripts/refresh_material_handoff.py",
    "schemas/material-package.schema.json",
    "schemas/material-package-receipt.schema.json",
)


def write_files(root: Path) -> None:
    files = {
        "sources/accepted-design.md": b"accepted public design\n",
        "outputs/canonical-refresh.md": b"validated refresh contract\n",
        "outputs/codex-refresh.md": b"validated refresh contract\n",
        "outputs/claude-refresh.md": b"validated refresh contract\n",
        "dependencies/invoke-policy.json": b'{"policy":"current"}\n',
    }
    for relative_path, content in files.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def exact_ref(root: Path, relative_path: str) -> dict[str, Any]:
    content = (root / relative_path).read_bytes()
    return {
        "path": relative_path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def base_package(root: Path, case_id: str) -> dict[str, Any]:
    output_paths = (
        "outputs/canonical-refresh.md",
        "outputs/codex-refresh.md",
        "outputs/claude-refresh.md",
    )
    return {
        "schema_version": "1.0.0",
        "package_id": case_id,
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "spellcraft",
        "authority_class": "public",
        "publication_class": "public",
        "source_artifacts": [
            {
                **exact_ref(root, "sources/accepted-design.md"),
                "authority_class": "public",
            }
        ],
        "changes": [
            {
                "target_path": target,
                "operation": "update",
                "output_ref": exact_ref(root, output_path),
            }
            for target, output_path in zip(TARGETS, output_paths, strict=True)
        ],
        "target_inventory": [
            {
                "target_path": target,
                "lifecycle_owner": "spellcraft",
                "authority_class": "public",
                "publication_class": "public",
                "dependency_ids": ["invoke-policy"],
            }
            for target in TARGETS
        ],
        "dependencies": [
            {
                "dependency_id": "invoke-policy",
                "artifact_ref": exact_ref(
                    root, "dependencies/invoke-policy.json"
                ),
            }
        ],
        "mirror_groups": [
            {
                "group_id": "invoke-refresh",
                "parity": "exact",
                "canonical_target": TARGETS[0],
                "generated_targets": list(TARGETS[1:]),
            }
        ],
        "approval": {
            "class": "explicit-apply",
            "owner": "spellcraft",
            "scope_paths": list(TARGETS),
            "authority_classes": ["public"],
            "publication_classes": ["public"],
        },
        "validation_commands": [
            "bash arcanum/spells/invoke/development/run-validation-fixtures.sh"
        ],
    }


def apply_mutation(
    mutation: str, package: dict[str, Any], root: Path
) -> dict[str, Any]:
    if mutation == "none":
        return package
    if mutation == "missing-output":
        (root / package["changes"][1]["output_ref"]["path"]).unlink()
    elif mutation == "empty-change":
        output_path = root / package["changes"][1]["output_ref"]["path"]
        output_path.write_bytes(b"")
        package["changes"][1]["output_ref"] = exact_ref(
            root, package["changes"][1]["output_ref"]["path"]
        )
    elif mutation == "stale-output-digest":
        package["changes"][1]["output_ref"]["sha256"] = "0" * 64
    elif mutation == "path-escape":
        package["changes"][1]["output_ref"]["path"] = "../escaped.md"
    elif mutation == "symlink-escape":
        output_path = root / package["changes"][1]["output_ref"]["path"]
        output_path.unlink()
        output_path.symlink_to("/etc/hosts")
    elif mutation == "owner-escape":
        package["target_inventory"][1]["lifecycle_owner"] = "other-owner"
    elif mutation == "missing-dependency":
        package["dependencies"] = []
    elif mutation == "publication-boundary":
        package["source_artifacts"][0]["authority_class"] = "private"
    elif mutation == "approval-scope":
        package["approval"]["scope_paths"].remove(TARGETS[2])
    elif mutation == "mirror-drift":
        output_path = root / package["changes"][1]["output_ref"]["path"]
        output_path.write_bytes(b"undeclared runtime drift\n")
        package["changes"][1]["output_ref"] = exact_ref(
            root, package["changes"][1]["output_ref"]["path"]
        )
    elif mutation == "structural-invalid":
        package["authority_class"] = "ambient"
    elif mutation == "proposal-only":
        package = {
            "schema_version": "1.0.0",
            "package_id": package["package_id"],
            "mutation_mode": "proposal-only",
            "mutation_state": "proposal-only",
            "lifecycle_owner": "spellcraft",
            "authority_class": "public",
            "publication_class": "public",
            "source_artifacts": [],
            "changes": [],
            "target_inventory": [],
            "dependencies": [],
            "mirror_groups": [],
            "approval": {
                "class": "none",
                "owner": None,
                "scope_paths": [],
                "authority_classes": [],
                "publication_classes": [],
            },
            "validation_commands": [],
        }
    else:
        raise ValueError(f"unknown fixture mutation: {mutation}")
    return package


def run_handoff_cases(
    fixture_document: dict[str, Any],
    package_schema: dict[str, Any],
    receipt_schema: dict[str, Any],
) -> tuple[int, list[str]]:
    passed = 0
    failures: list[str] = []
    for fixture in fixture_document["cases"]:
        receipt: dict[str, Any] | None = None
        expected_package_id: str | None = None
        expected_package_digest: str | None = None
        if fixture["expected_mutation_mode"] == "apply-approved":
            with tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                write_files(root)
                package = base_package(root, fixture["id"])
                if fixture["receipt_source"] == "invalid-stale-output":
                    package = apply_mutation(
                        "stale-output-digest", copy.deepcopy(package), root
                    )
                receipt = validate_material_package(
                    package, root, package_schema, receipt_schema
                )
                expected_package_id = package["package_id"]
                expected_package_digest = receipt["packageDigest"]
                if fixture["receipt_source"] == "stale-receipt-digest":
                    assert receipt["patchVerdict"] == "pass"
                    receipt = copy.deepcopy(receipt)
                    receipt["packageDigest"] = "0" * 64
                elif fixture["receipt_source"] == "missing":
                    receipt = None

        request = {
            "activationSource": fixture["activation_source"],
            "authoredPhaseStatus": "pass",
            "requestedHandoff": fixture["requested_handoff"],
            "materialReceipt": receipt,
            "expectedPackageId": expected_package_id,
            "expectedPackageDigest": expected_package_digest,
        }
        if fixture["mutation_mode"] is not None:
            request["mutationMode"] = fixture["mutation_mode"]
        result = resolve_refresh_handoff(request, receipt_schema)
        expected_blocker = fixture["expected_blocker"]
        matches = (
            result["activationSource"] == fixture["activation_source"]
            and result["mutationMode"] == fixture["expected_mutation_mode"]
            and result["mutationModeSource"] == fixture["expected_mode_source"]
            and result["phaseStatus"] == fixture["expected_phase_status"]
            and result["handoffStatus"] == fixture["expected_handoff_status"]
            and result["mutationReady"] == fixture["expected_mutation_ready"]
            and (
                expected_blocker is None
                or expected_blocker in result["blockers"]
            )
        )
        if matches:
            passed += 1
            print(
                f"PASS {fixture['id']}: "
                f"{result['phaseStatus']}/{result['handoffStatus']} "
                f"mutationReady={str(result['mutationReady']).lower()}"
            )
        else:
            failures.append(fixture["id"])
            print(
                f"FAIL {fixture['id']}: "
                f"received {json.dumps(result, sort_keys=True)}"
            )
    return passed, failures


def check_generated_runtime_parity() -> tuple[bool, list[str]]:
    mismatches: list[str] = []
    for runtime_root in (
        REPOSITORY_ROOT / ".agents/skills/invoke",
        REPOSITORY_ROOT / ".claude/skills/invoke",
    ):
        for relative_path in RUNTIME_SUPPORT_PATHS:
            canonical_path = INVOKE_DIR / relative_path
            generated_path = runtime_root / relative_path
            if not generated_path.is_file():
                mismatches.append(
                    f"missing generated runtime support: {generated_path}"
                )
            elif generated_path.read_bytes() != canonical_path.read_bytes():
                mismatches.append(
                    f"generated runtime drift: {generated_path}"
                )
    return not mismatches, mismatches


def main() -> int:
    schema_dir = INVOKE_DIR / "schemas"
    fixture_path = DEVELOPMENT_DIR / "fixtures/material-package-cases.json"
    fixture_document = load_json(fixture_path)
    handoff_fixture_document = load_json(
        DEVELOPMENT_DIR / "fixtures/refresh-material-handoff-cases.json"
    )
    package_schema = load_json(schema_dir / "material-package.schema.json")
    receipt_schema = load_json(
        schema_dir / "material-package-receipt.schema.json"
    )
    failures: list[str] = []
    passed = 0

    for fixture in fixture_document["cases"]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_files(root)
            package = base_package(root, fixture["id"])
            package = apply_mutation(
                fixture["mutation"], copy.deepcopy(package), root
            )
            receipt = validate_material_package(
                package, root, package_schema, receipt_schema
            )

        reasons = "; ".join(receipt["reasons"])
        expected_reason = fixture["expected_reason"]
        if fixture["expected_patch_verdict"] == "pass":
            receipt_shape_valid = (
                isinstance(receipt["packageDigest"], str)
                and len(receipt["packageDigest"]) == 64
                and receipt["validatedPaths"] == sorted(TARGETS)
                and receipt["dependencyResult"] == "pass"
                and receipt["ownerBoundaryResult"] == "pass"
                and receipt["publicationBoundaryResult"] == "pass"
            )
        elif fixture["expected_patch_verdict"] == "not-applicable":
            receipt_shape_valid = (
                receipt["packageDigest"] is None
                and receipt["validatedPaths"] == []
                and receipt["dependencyResult"] == "not-applicable"
            )
        else:
            receipt_shape_valid = (
                isinstance(receipt["packageDigest"], str)
                and len(receipt["packageDigest"]) == 64
                and receipt["validatedPaths"] == []
            )
        matches = (
            receipt["patchVerdict"] == fixture["expected_patch_verdict"]
            and receipt["mutationHandoff"] == fixture["expected_handoff"]
            and receipt_shape_valid
            and (
                expected_reason is None
                or expected_reason in reasons
            )
        )
        if matches:
            passed += 1
            print(
                f"PASS {fixture['id']}: "
                f"{receipt['patchVerdict']}/{receipt['mutationHandoff']}"
            )
        else:
            failures.append(fixture["id"])
            print(
                f"FAIL {fixture['id']}: expected "
                f"{fixture['expected_patch_verdict']}/"
                f"{fixture['expected_handoff']} reason={expected_reason!r}; "
                f"received {json.dumps(receipt, sort_keys=True)}"
            )

    handoff_passed, handoff_failures = run_handoff_cases(
        handoff_fixture_document, package_schema, receipt_schema
    )
    passed += handoff_passed
    failures.extend(handoff_failures)

    parity_valid, parity_failures = check_generated_runtime_parity()
    if parity_valid:
        passed += 1
        print("PASS canonical-generated-runtime-parity: exact")
    else:
        failures.append("canonical-generated-runtime-parity")
        for parity_failure in parity_failures:
            print(f"FAIL canonical-generated-runtime-parity: {parity_failure}")

    total_cases = (
        len(fixture_document["cases"])
        + len(handoff_fixture_document["cases"])
        + 1
    )
    if failures:
        print(
            f"RESULT failed={len(failures)} passed={passed} "
            f"cases={total_cases}"
        )
        return 1
    print(
        f"RESULT failed=0 passed={passed} "
        f"cases={total_cases}"
    )
    print(
        "AUTHORITY direct-user defaults apply-approved; non-user defaults "
        "proposal-only; approval never overrides invalid material"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
