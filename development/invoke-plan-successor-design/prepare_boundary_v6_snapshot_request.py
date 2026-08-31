#!/usr/bin/env python3
"""Create stable Boundary V6 from a verified selected-file snapshot."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


EPOCH = "2026-08-28-plan-successor-design-boundary-v6-evidence-repair"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--snapshot-root", required=True)
    parser.add_argument("--verification-root", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")

    request = json.loads(args.source.read_text(encoding="utf-8"))
    document = request["document"]
    inventory = json.loads(
        (Path(args.snapshot_root) / "SOURCE-INVENTORY.json").read_text(
            encoding="utf-8"
        )
    )
    forbidden = [
        entry["origin_path"]
        for entry in inventory["entries"]
        if "/__pycache__/" in entry["origin_path"]
        or entry["origin_path"].endswith((".pyc", ".pyo", ".pyd"))
        or entry["origin_path"].endswith(
            "development/fixtures/define-intent-coverage/results/latest-summary.json"
        )
    ]
    if forbidden:
        raise ValueError(f"V6 snapshot contains generated evidence: {forbidden}")

    define_root = next(
        item for item in document["roots"] if item["root_id"] == "root:define-refresh"
    )
    define_rules = [
        rule
        for rule in document["discovery_rules"]
        if rule["root_id"] == "root:define-refresh"
    ]
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for entry in inventory["entries"]:
        grouped[(entry["rule_id"], entry["input_class"])].append(
            entry["snapshot_relative_path"]
        )
    snapshot_rules = [
        {
            "rule_id": rule_id,
            "root_id": "root:material-snapshot",
            "input_class": input_class,
            "include_globs": sorted(paths),
        }
        for (rule_id, input_class), paths in sorted(grouped.items())
    ]
    snapshot_rules.append(
        {
            "rule_id": "rule:selected-material-origin-inventory",
            "root_id": "root:material-snapshot",
            "input_class": "authority-policy",
            "include_globs": ["SOURCE-INVENTORY.json"],
        }
    )
    snapshot_rules.append(
        {
            "rule_id": "rule:selected-material-origin-verification",
            "root_id": "root:material-verification",
            "input_class": "interface-contract",
            "include_globs": ["VERIFICATION-RECEIPT.json"],
        }
    )

    document["observation_epoch"] = EPOCH
    document["roots"] = [
        {"root_id": "root:material-snapshot", "path": args.snapshot_root},
        {"root_id": "root:material-verification", "path": args.verification_root},
        define_root,
    ]
    document["discovery_rules"] = snapshot_rules + define_rules
    request["evidence_paths"] = [
        {"pointer": "/roots/0", "path": args.snapshot_root, "kind": "directory"},
        {
            "pointer": "/roots/1",
            "path": args.verification_root,
            "kind": "directory",
        },
        {"pointer": "/roots/2", "path": define_root["path"], "kind": "directory"},
    ]
    args.output.write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
