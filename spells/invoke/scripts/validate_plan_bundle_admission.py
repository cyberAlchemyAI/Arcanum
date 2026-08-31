#!/usr/bin/env python3
"""Independently replay and admit one exact Invoke Plan v2 bundle."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

from plan_successor_support import (
    compile_bundle,
    digest,
    file_ref,
    inventory,
    load_json,
    sha_bytes,
    validate_schema,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--bundle-root", required=True, type=Path)
    parser.add_argument("--schema-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--prior-admission", type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve(); bundle = args.bundle_root.resolve(); schema_dir = args.schema_dir.resolve()
    if args.output.exists() or args.output.is_symlink():
        print("ERROR: output must be absent", file=sys.stderr); return 2
    blockers: list[str] = []
    try:
        bundle.relative_to(repo_root)
    except ValueError:
        print("ERROR: bundle escapes repository root", file=sys.stderr); return 2
    if not bundle.is_dir() or bundle.is_symlink():
        print("ERROR: bundle must be a regular directory", file=sys.stderr); return 2
    try:
        submitted_inventory = inventory(bundle)
        stage_path = bundle / "PLAN-STAGE-RECEIPT.json"
        source_path = bundle / "PLAN-SOURCE.json"
        stage = load_json(stage_path)
        blockers.extend(validate_schema(stage, schema_dir / "plan-stage-receipt-v2.schema.json", "Plan stage receipt"))
        if stage.get("receipt_digest") != digest({key: value for key, value in stage.items() if key != "receipt_digest"}): blockers.append("stage receipt digest mismatch")
        expected_outputs = inventory(bundle, exclude_stage=True)
        if stage.get("outputs") != expected_outputs: blockers.append("stage output inventory does not match bundle bytes")
        if stage.get("source_ref") != file_ref(source_path, "PLAN-SOURCE.json"): blockers.append("stage source reference does not match PLAN-SOURCE.json")
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: cannot inspect bundle: {error}", file=sys.stderr); return 2

    replay_inventory: list[dict] = []
    with tempfile.TemporaryDirectory(prefix=".plan-admission-", dir=bundle.parent) as temporary:
        replay = Path(temporary) / "bundle"
        if not blockers:
            blockers.extend(compile_bundle(source_path, replay, repo_root, schema_dir))
        if replay.is_dir():
            replay_inventory = inventory(replay)
            if [row["path"] for row in submitted_inventory] != [row["path"] for row in replay_inventory]: blockers.append("replay inventory paths differ")
            else:
                for left, right in zip(submitted_inventory, replay_inventory):
                    if left != right: blockers.append(f"replay bytes differ: {left['path']}")
        if args.prior_admission:
            try:
                prior = load_json(args.prior_admission)
                if prior.get("result") != "pass": blockers.append("prior admission is not PASS")
                elif prior.get("bundle_inventory") != submitted_inventory: blockers.append("prior admission binds different bundle bytes")
            except (OSError, UnicodeError, ValueError) as error: blockers.append(f"prior admission cannot be evaluated: {error}")

    validator_path = Path(__file__).resolve()
    consumer_results = stage.get("consumer_results", []) if isinstance(stage, dict) else []
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/plan-bundle-admission-receipt/v1",
        "schema_version": "invoke.plan-bundle-admission-receipt.v1",
        "receipt_id": f"plan-admission-v1:{digest(submitted_inventory)[:24]}",
        "validator": {"identity": "invoke.validate-plan-bundle-admission.v1", "path": validator_path.relative_to(repo_root).as_posix(), "sha256": sha_bytes(validator_path.read_bytes())},
        "stage_receipt_ref": file_ref(bundle / "PLAN-STAGE-RECEIPT.json", (bundle / "PLAN-STAGE-RECEIPT.json").relative_to(repo_root).as_posix()),
        "bundle_inventory": submitted_inventory,
        "replay_inventory": replay_inventory,
        "consumer_results": consumer_results,
        "blockers": sorted(set(blockers)),
        "result": "block" if blockers else "pass",
        "authority_effect": "none",
    }
    receipt["receipt_digest"] = digest(receipt)
    schema_errors = validate_schema(receipt, schema_dir / "plan-bundle-admission-receipt-v1.schema.json", "Plan admission receipt")
    if schema_errors:
        for error in schema_errors: print(f"ERROR: {error}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        from plan_successor_support import canonical_bytes
        handle.write(canonical_bytes(receipt))
    if blockers:
        for blocker in receipt["blockers"]: print(f"BLOCK: {blocker}", file=sys.stderr)
        return 1
    print(f"PLAN_ADMISSION={args.output}")
    print("RESULT=pass")
    print("AUTHORITY_EFFECT=none")
    return 0


if __name__ == "__main__": raise SystemExit(main())
