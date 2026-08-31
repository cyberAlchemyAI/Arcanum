#!/usr/bin/env python3
"""Independently replay and admit one exact W3 Invoke Design bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from compile_design_source_v2 import (  # noqa: E402
    OUTPUTS,
    STAGE_NAME,
    atomic_write_json,
    canonical_bytes,
    compile_bundle,
    safe_absent_destination,
)
from design_stage_contract import digest_without, validate_stage_receipt  # noqa: E402


IDENTITY = "invoke.validate-design-bundle-admission.v1"
OWNER = "invoke-design-bundle-admission-validator"
VALIDATOR_PATH = "arcanum/spells/invoke/scripts/validate_design_bundle_admission.py"
CHECK_IDS = (
    "stage-receipt-validation",
    "producer-identity",
    "bundle-closure-binding",
    "output-inventory",
    "projection-replay",
    "distill-evidence",
    "authority-ceiling",
)


class AdmissionBlock(ValueError):
    def __init__(self, code: str, message: str, check_index: int, selector: str | None = None, route: str = "repair-design-bundle"):
        super().__init__(message)
        self.code = code
        self.check_index = check_index
        self.selector = selector
        self.route = route


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def exact_ref(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def output_inventory(bundle: Path, root: Path) -> list[dict[str, Any]]:
    inventory = []
    for kind, name in OUTPUTS:
        inventory.append({"kind": kind, **exact_ref(bundle / name, root)})
    inventory.append({"kind": "stage-receipt", **exact_ref(bundle / STAGE_NAME, root)})
    return inventory


def safe_bundle(path: Path, root: Path) -> Path:
    if not path.is_absolute():
        raise ValueError("bundle directory must be absolute")
    lexical = Path(os.path.abspath(path))
    try:
        label = lexical.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("bundle directory must be inside --repo-root") from error
    current = root.resolve()
    for part in label.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"bundle path contains a symlink: {current}")
    if not lexical.is_dir():
        raise ValueError("bundle directory is unavailable")
    return lexical


def inventory_differences(expected: Path, observed: Path) -> list[dict[str, Any]]:
    expected_names = {item.name for item in expected.iterdir()}
    observed_names = {item.name for item in observed.iterdir()}
    differences: list[dict[str, Any]] = []
    for name in sorted(expected_names - observed_names):
        differences.append({"kind": "missing", "path": name, "expected": name, "observed": None})
    for name in sorted(observed_names - expected_names):
        differences.append({"kind": "unexpected", "path": name, "expected": None, "observed": name})
    for name in sorted(expected_names & observed_names):
        left, right = expected / name, observed / name
        if not left.is_file() or left.is_symlink() or not right.is_file() or right.is_symlink():
            differences.append({"kind": "content-mismatch", "path": name, "expected": "regular-file", "observed": "non-regular"})
            continue
        left_data, right_data = left.read_bytes(), right.read_bytes()
        if len(left_data) != len(right_data):
            differences.append({"kind": "size-mismatch", "path": name, "expected": len(left_data), "observed": len(right_data)})
        elif left_data != right_data:
            differences.append({"kind": "digest-mismatch", "path": name, "expected": hashlib.sha256(left_data).hexdigest(), "observed": hashlib.sha256(right_data).hexdigest()})
    return differences


def make_receipt(
    bundle: Path,
    root: Path,
    stage: dict[str, Any],
    stage_ref: dict[str, Any],
    inventory: list[dict[str, Any]],
    validator_digest: str,
    result: str,
    differences: list[dict[str, Any]],
    error: AdmissionBlock | None = None,
) -> dict[str, Any]:
    closure_ref = copy.deepcopy(stage["bindings"]["bundle_closure_ref"])
    candidate_ref = copy.deepcopy(stage["bindings"]["candidate_production_receipt_ref"])
    blocker_id = f"w3-admission:{error.code.lower()}" if error else None
    checks = []
    for index, check_id in enumerate(CHECK_IDS):
        if error is None or index < error.check_index:
            status, evidence, causes = "pass", [copy.deepcopy(stage_ref)], []
        elif index == error.check_index:
            status, evidence, causes = "block", [], [blocker_id]
        else:
            status, evidence, causes = "not_evaluable", [], [blocker_id]
        checks.append({"check_id": check_id, "status": status, "evidence_refs": evidence, "causal_blocker_ids": causes})
    blockers = [] if error is None else [{
        "blocker_id": blocker_id,
        "code": error.code,
        "message": str(error),
        "check_id": CHECK_IDS[error.check_index],
        "selector": error.selector,
        "repair_route": error.route,
    }]
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v1",
        "schema_version": "invoke.design-bundle-admission-receipt.v1",
        "receipt_id": f"design-admission:{stage_ref['sha256'][:24]}",
        "validator": {"identity": IDENTITY, "owner": OWNER, "path": VALIDATOR_PATH, "sha256": validator_digest},
        "bundle_root": bundle.relative_to(root).as_posix(),
        "stage_receipt_ref": copy.deepcopy(stage_ref),
        "producer_binding": {
            "receipt_id": stage["receipt_id"],
            "receipt_digest": stage["receipt_digest"],
            "profile_id": stage["profile_id"],
            "producer": copy.deepcopy(stage["producer"]),
        },
        "output_inventory": copy.deepcopy(inventory),
        "checks": checks,
        "replay": {
            "bundle_closure_ref": closure_ref,
            "candidate_receipt_ref": candidate_ref,
            "comparison": "pass" if error is None else ("block" if error.check_index >= 4 else "not-evaluable"),
            "output_inventory_digest": hashlib.sha256(canonical_bytes(inventory)).hexdigest(),
            "differences": copy.deepcopy(differences),
        },
        "result": result,
        "blockers": blockers,
        "evidence_ceiling": {
            "artifact_authored": result == "pass",
            "registry_released": False,
            "mutation_runtime_ready": False,
            "acceptance": False,
            "execution": False,
            "publication": False,
            "deployment": False,
            "external_effect": False,
        },
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    return receipt


def validate_bundle(bundle: Path, root: Path, output: Path, schema_dir: Path) -> int:
    root = root.resolve()
    bundle = safe_bundle(bundle, root)
    output = safe_absent_destination(output)
    if output == bundle or bundle in output.parents:
        raise ValueError("admission receipt must remain outside the submitted bundle")
    schema_path = schema_dir / "design-bundle-admission-receipt-v1.schema.json"
    if not schema_path.is_file():
        raise ValueError("installed Design admission schema unavailable")
    admission_schema = load_json(schema_path)
    validator_digest = hashlib.sha256((root / VALIDATOR_PATH).read_bytes()).hexdigest()
    stage_path = bundle / STAGE_NAME
    if not stage_path.is_file() or stage_path.is_symlink():
        raise ValueError("canonical Design stage receipt unavailable; valid admission evidence cannot be issued")
    try:
        stage = load_json(stage_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise ValueError(f"Design stage receipt malformed; valid admission evidence cannot be issued: {error}") from error
    if not all(key in stage for key in ("receipt_id", "receipt_digest", "profile_id", "producer", "bindings")):
        raise ValueError("Design stage receipt lacks the fields required for a valid admission receipt")
    stage_ref = exact_ref(stage_path, root)
    before = {item.name: hashlib.sha256(item.read_bytes()).hexdigest() for item in bundle.iterdir() if item.is_file() and not item.is_symlink()}
    try:
        diagnostics = validate_stage_receipt(stage, root, schema_dir, bundle)
        if diagnostics:
            raise AdmissionBlock("STAGE_RECEIPT_INVALID", "; ".join(diagnostics[:8]), 0, STAGE_NAME)
        expected_names = {name for _, name in OUTPUTS} | {STAGE_NAME}
        names = {item.name for item in bundle.iterdir()}
        if names != expected_names or any(not item.is_file() or item.is_symlink() for item in bundle.iterdir()):
            raise AdmissionBlock("OUTPUT_INVENTORY_MISMATCH", "submitted bundle inventory is not exactly fifteen regular files", 3, bundle.as_posix())
        inventory = output_inventory(bundle, root)
        if stage["bindings"]["distill_evidence"]["execution_receipt_ref"]["sha256"] != inventory[8]["sha256"]:
            raise AdmissionBlock("DISTILL_EVIDENCE_INVALID", "bundle Distill receipt differs from the bound execution receipt", 5, "DISTILL-RECEIPT.json", "repair-distill-evidence")
        ceiling = stage["evidence_ceiling"]
        if not ceiling["artifact_authored"] or any(ceiling[key] for key in ("plan_evidence", "registry_released", "mutation_runtime_ready", "acceptance", "execution", "publication", "deployment", "external_effect")):
            raise AdmissionBlock("AUTHORITY_CEILING_INVALID", "Design stage evidence ceiling overclaims or omits artifact authorship", 6, "evidence_ceiling")

        replay_parent = Path(tempfile.mkdtemp(prefix=".design-w3-admission-", dir=root))
        try:
            replay_bundle = replay_parent / "bundle"
            replay_attempt = replay_parent / "attempt.json"
            closure_path = root / stage["bindings"]["bundle_closure_ref"]["path"]
            code = compile_bundle(closure_path, root, replay_bundle, replay_attempt, schema_dir)
            if code != 0:
                raise AdmissionBlock("PROJECTION_REPLAY_MISMATCH", "clean replay did not produce a passing bundle", 4, stage["bindings"]["bundle_closure_ref"]["path"], "recompile-design-bundle")
            differences = inventory_differences(replay_bundle, bundle)
            if differences:
                raise AdmissionBlock("PROJECTION_REPLAY_MISMATCH", "submitted bundle differs from clean deterministic replay", 4, differences[0]["path"], "recompile-design-bundle")
        finally:
            shutil.rmtree(replay_parent, ignore_errors=True)
        after = {item.name: hashlib.sha256(item.read_bytes()).hexdigest() for item in bundle.iterdir() if item.is_file() and not item.is_symlink()}
        if before != after:
            raise AdmissionBlock("PROJECTION_REPLAY_MISMATCH", "submitted bundle changed during admission", 4, bundle.as_posix(), "recompile-design-bundle")
        receipt = make_receipt(bundle, root, stage, stage_ref, inventory, validator_digest, "pass", [])
        errors = [error.message for error in Draft202012Validator(admission_schema).iter_errors(receipt)]
        if errors:
            raise ValueError(f"cannot issue schema-valid Design admission receipt: {'; '.join(errors[:8])}")
        atomic_write_json(output, receipt)
        return 0
    except AdmissionBlock as error:
        names = {item.name for item in bundle.iterdir()}
        expected_names = {name for _, name in OUTPUTS} | {STAGE_NAME}
        if names != expected_names or any(not (bundle / name).is_file() or (bundle / name).is_symlink() for name in names):
            raise ValueError(f"bundle shape prevents schema-valid failure evidence: {error}") from error
        inventory = output_inventory(bundle, root)
        differences = []
        if error.code == "PROJECTION_REPLAY_MISMATCH":
            differences = [{"kind": "content-mismatch", "path": error.selector or STAGE_NAME, "expected": "clean-replay", "observed": "submitted-bundle"}]
        receipt = make_receipt(bundle, root, stage, stage_ref, inventory, validator_digest, "block", differences, error)
        errors = [item.message for item in Draft202012Validator(admission_schema).iter_errors(receipt)]
        if errors:
            raise ValueError(f"cannot issue schema-valid Design admission failure receipt: {'; '.join(errors[:8])}") from error
        atomic_write_json(output, receipt)
        print(f"BLOCK [{error.code}]: {error}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_dir")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--schema-dir")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    schema_dir = Path(args.schema_dir).resolve() if args.schema_dir else root / "arcanum/spells/invoke/schemas"
    try:
        return validate_bundle(Path(args.bundle_dir), root, Path(args.output), schema_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
