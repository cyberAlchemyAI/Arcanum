#!/usr/bin/env python3
"""Independently close the bounded DFE fixture experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


CANONICAL_INPUTS = [
    "spells/goal/README.md",
    "spells/goal/runtime/goal_loop.py",
    "spells/goal/schemas/frontier-snapshot.schema.json",
    "spells/invoke/README.md",
    "arcana/craft/SKILL.md",
    "arcana/craft/templates/schemas/ledger-core.schema.yml",
]
DESIGN_MANIFEST = (
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment/"
    "DESIGN-SCOPE-MANIFEST.json"
)


def ref(root: Path, relative: str) -> dict[str, object]:
    path = root / relative
    content = path.read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    spells_root = Path.cwd().resolve()
    arcanum_root = spells_root.parent
    experiment = spells_root / args.experiment_root
    missing = []
    owner_receipts = []
    for index in range(1, 8):
        unit = f"SWU-DFE-{index:03d}"
        owner = experiment / "session-evidence" / unit / "owner-receipt.json"
        if not owner.is_file():
            missing.append(str(owner.relative_to(arcanum_root)))
            continue
        document = json.loads(owner.read_text(encoding="utf-8"))
        if document.get("validation_result") != "pass":
            missing.append(f"{unit}:owner receipt not passing")
        owner_receipts.append(ref(arcanum_root, str(owner.relative_to(arcanum_root))))

    manifest = json.loads(
        (arcanum_root / DESIGN_MANIFEST).read_text(encoding="utf-8")
    )
    before_by_path = {
        item["path"]: item["digest"] for item in manifest["source_contracts"]
    }
    hashes = []
    for path in CANONICAL_INPUTS:
        after = ref(arcanum_root, path)
        before_sha256 = before_by_path.get(path)
        hashes.append(
            {
                "path": path,
                "before_sha256": before_sha256,
                "after_sha256": after["sha256"],
                "size_bytes": after["size_bytes"],
                "match": before_sha256 == after["sha256"],
            }
        )
        if before_sha256 is None or before_sha256 != after["sha256"]:
            missing.append(f"canonical hash drift: {path}")
    output = spells_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "schema_version": "dfe-authority-hashes.v1",
        "status": "pass" if not missing else "block",
        "canonical_inputs": hashes,
        "owner_receipts": owner_receipts,
        "missing_or_blocked": missing,
        "authority_effect": "none",
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
