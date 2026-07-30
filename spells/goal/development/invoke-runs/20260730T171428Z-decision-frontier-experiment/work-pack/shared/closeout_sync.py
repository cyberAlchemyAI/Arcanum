#!/usr/bin/env python3
"""Run the bounded Invoke Refresh closeout owner hop for one DFE unit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--source-receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = args.repository_root.resolve()
    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    by_id = {unit["unit_id"]: unit for unit in matrix["units"]}
    unit = by_id[args.unit]
    source_path = root / args.source_receipt
    source = json.loads(source_path.read_text(encoding="utf-8"))
    blockers = []
    if source.get("status") != "pass" or source.get("validation_result") != "pass":
        blockers.append("source terminal receipt is not passing")

    evidence = []
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for spec in unit["validation_commands"]:
        result = subprocess.run(
            spec["argv"],
            cwd=root / spec["cwd"],
            env={**env, **spec["environment"]},
            timeout=spec["timeout_seconds"],
            check=False,
            capture_output=True,
            text=True,
        )
        evidence.append(
            f"argv={json.dumps(spec['argv'], separators=(',', ':'))};exit={result.returncode}"
        )
        if result.returncode != spec["expected_exit_code"]:
            blockers.append(f"owner validation failed: {spec['argv']}")

    validated_targets = []
    for item in source.get("artifacts", []):
        target = root / item["path"]
        if not target.is_file() or digest(target) != item["sha256"]:
            blockers.append(f"target drift: {item['path']}")
        else:
            validated_targets.append(item["path"])

    source_ref = {
        "path": args.source_receipt,
        "sha256": digest(source_path),
        "size_bytes": source_path.stat().st_size,
    }
    successor = source.get("successor", {"unit_id": None, "eligible": False, "selected": False})
    receipt = {
        "schema_version": "invoke-refresh-closeout-receipt.v1",
        "unit_id": args.unit,
        "owner": "invoke:refresh:apply-approved",
        "lifecycle_owner": "spellcraft",
        "source_receipt": source_ref,
        "validation_result": "pass" if not blockers else "block",
        "validated_targets": sorted(validated_targets),
        "evidence": evidence or ["source receipt identity validated"],
        "delta_classes": ["evidence_added", "route_changed"],
        "blockers": blockers,
        "successor": successor,
        "lifecycle_effect": "none",
        "authority_effect": "none",
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
