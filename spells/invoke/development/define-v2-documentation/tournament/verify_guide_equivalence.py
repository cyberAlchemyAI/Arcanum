#!/usr/bin/env python3
"""Read-only verifier for section-order-only tournament guide equivalence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from render_candidates import ORDERS, build_expected


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root: Path) -> dict[str, Any]:
    blockers: list[str] = []
    try:
        expected_guides, expected_manifest = build_expected(root)
    except (OSError, UnicodeError, ValueError, SystemExit) as exc:
        return {"status": "block", "blockers": [f"cannot reconstruct expected guides: {exc}"], "writes": 0}

    manifest_path = root / "GUIDE-MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        manifest = None
        blockers.append(f"manifest is not readable JSON: {exc}")
    if manifest != expected_manifest:
        blockers.append("GUIDE-MANIFEST.json does not exactly match the in-memory reconstruction")

    actual_guide_paths = {
        path.relative_to(root).as_posix()
        for path in (root / "guides").glob("guide-*.md")
        if path.is_file()
    }
    if actual_guide_paths != set(expected_guides):
        blockers.append("guide inventory is not exactly alpha, beta, and gamma")
    for relative_path, expected_bytes in expected_guides.items():
        path = root / relative_path
        if not path.is_file():
            blockers.append(f"missing rendered guide: {relative_path}")
        elif path.read_bytes() != expected_bytes:
            blockers.append(f"rendered guide bytes differ from shared-section reconstruction: {relative_path}")

    section_inventory = sorted(path.name for path in (root / "content").glob("*.md"))
    if len(section_inventory) != 9 or set(section_inventory) != set(ORDERS["alpha"]):
        blockers.append("shared section inventory must contain exactly the nine declared sections")
    if len({tuple(order) for order in ORDERS.values()}) != 3:
        blockers.append("candidate section orders must be distinct")
    for candidate, order in ORDERS.items():
        if len(order) != 9 or len(set(order)) != 9 or set(order) != set(section_inventory):
            blockers.append(f"{candidate} order is not a permutation of the shared section inventory")

    return {
        "status": "pass" if not blockers else "block",
        "controlled_variable": "section-order-only",
        "guide_count": len(expected_guides),
        "section_count": len(section_inventory),
        "guide_sha256": {
            candidate: digest(root / f"guides/guide-{candidate}.md")
            for candidate in sorted(ORDERS)
            if (root / f"guides/guide-{candidate}.md").is_file()
        },
        "writes": 0,
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(args.root.resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"GUIDE_EQUIVALENCE={result['status']}")
        for blocker in result["blockers"]:
            print(f"BLOCK: {blocker}")
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
