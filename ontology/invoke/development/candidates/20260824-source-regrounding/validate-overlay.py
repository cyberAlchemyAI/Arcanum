#!/usr/bin/env python3
"""Validate the Invoke source re-grounding candidate in a temporary overlay."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
REPOSITORY_ROOT = HERE.parents[4]
MANIFEST_PATH = HERE / "CANDIDATE-MANIFEST.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate_inventory() -> list[str]:
    return sorted(
        path.relative_to(HERE).as_posix()
        for path in HERE.rglob("*")
        if path.is_file() and "__pycache__" not in path.relative_to(HERE).parts
    )


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("candidate_id") != "20260824-source-regrounding":
        errors.append("candidate identity mismatch")
    if manifest.get("status") != "candidate" or manifest.get("authority_effect") != "none":
        errors.append("candidate authority ceiling mismatch")
    if manifest.get("ontology_type") != "business-system-bridge":
        errors.append("ontology type mismatch")
    if manifest.get("affected_branches") != ["business", "system", "bridge"]:
        errors.append("branch traversal mismatch")
    if manifest.get("expected_inventory") != candidate_inventory():
        errors.append("candidate directory inventory mismatch")

    targets = manifest.get("targets", [])
    target_paths = [record.get("target_path") for record in targets]
    if len(targets) != 13 or len(target_paths) != len(set(target_paths)):
        errors.append("target inventory must contain thirteen unique targets")
    for record in targets:
        target_path = REPOSITORY_ROOT / record.get("target_path", "")
        candidate_path = HERE / record.get("candidate_path", "")
        if not target_path.is_file() or target_path.is_symlink():
            errors.append(f"live target missing or symbolic: {record.get('target_path')}")
            continue
        if not candidate_path.is_file() or candidate_path.is_symlink():
            errors.append(f"candidate target missing or symbolic: {record.get('candidate_path')}")
            continue
        if sha256(target_path) != record.get("input_sha256") or target_path.stat().st_size != record.get("input_bytes"):
            errors.append(f"live input drift: {record.get('target_path')}")
        if sha256(candidate_path) != record.get("candidate_sha256") or candidate_path.stat().st_size != record.get("candidate_bytes"):
            errors.append(f"candidate target drift: {record.get('candidate_path')}")

    for record in manifest.get("bound_sidecars", []):
        path = HERE / record.get("path", "")
        if not path.is_file() or path.is_symlink():
            errors.append(f"bound sidecar missing or symbolic: {record.get('path')}")
        elif sha256(path) != record.get("sha256") or path.stat().st_size != record.get("bytes"):
            errors.append(f"bound sidecar drift: {record.get('path')}")

    manifest_digest = sha256(MANIFEST_PATH)
    for relative in manifest.get("derived_controls", []):
        path = HERE / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"derived control missing or symbolic: {relative}")
            continue
        document = load_json(path)
        if document.get("candidate_manifest_sha256") != manifest_digest:
            errors.append(f"derived control manifest binding mismatch: {relative}")
    return errors


def validate_overlay() -> tuple[list[str], dict[str, Any], str]:
    manifest = load_json(MANIFEST_PATH)
    errors = validate_manifest(manifest)
    test_output = ""
    counts: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="invoke-source-regrounding-") as temporary_directory:
        package_overlay = Path(temporary_directory) / "invoke"
        shutil.copytree(
            REPOSITORY_ROOT / "ontology/invoke",
            package_overlay,
            ignore=shutil.ignore_patterns("development"),
        )
        shutil.copytree(HERE / "targets/ontology/invoke", package_overlay, dirs_exist_ok=True)

        validator_path = HERE / "targets/arcana/ontology-vault/scripts/ontology_package.py"
        validator = load_module("candidate_ontology_package", validator_path)
        package_errors, counts = validator.validate_ontology_package(
            package_overlay,
            REPOSITORY_ROOT,
        )
        errors.extend(package_errors)

        if not package_errors:
            test_path = HERE / (
                "targets/arcana/ontology-vault/development/package-materialization/"
                "test_invoke_package.py"
            )
            tests = load_module("candidate_test_invoke_package", test_path)
            tests.SCRIPT = validator_path
            tests.PACKAGE = package_overlay
            tests.BUSINESS_NODES = package_overlay / "nodes/business.json"
            tests.MIGRATION = package_overlay / "migration/preserved-identities.json"
            tests.ARCANUM_ROOT = REPOSITORY_ROOT
            tests.PUBLIC_CONTRACTS = (
                REPOSITORY_ROOT
                / "arcana/ontology-vault/contracts/cav2-ontology-contracts.json"
            )
            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    tests.main()
            except AssertionError as error:
                errors.append(f"candidate regression tests failed: {error}")
            test_output = output.getvalue()
    return errors, counts, test_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    errors, counts, test_output = validate_overlay()
    report = {
        "authority_effect": "none",
        "candidate_manifest_sha256": sha256(MANIFEST_PATH),
        "checks": [
            "exact_inventory",
            "live_input_binding",
            "candidate_target_binding",
            "bound_sidecar_binding",
            "temporary_overlay_package_validation",
            "selector_bounds_and_slice_digests",
            "negative_source_insertion",
            "negative_moved_selector",
            "negative_mandatory_gate_drift",
        ],
        "command": "PYTHONDONTWRITEBYTECODE=1 python3 ontology/invoke/development/candidates/20260824-source-regrounding/validate-overlay.py",
        "counts": counts,
        "errors": errors,
        "status": "pass" if not errors else "block",
        "test_output": test_output.strip().splitlines(),
    }
    if args.write_report:
        (HERE / "VALIDATION-REPORT.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
