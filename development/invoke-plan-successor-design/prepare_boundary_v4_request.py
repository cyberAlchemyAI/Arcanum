#!/usr/bin/env python3
"""Create Boundary V4 against the confirmed current Define predecessor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EPOCH = "2026-08-28-plan-successor-design-boundary-v4-current-define"
DEFINE_ROOT = "arcanum/development/invoke-plan-successor-define-refresh"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    request = json.loads(args.source.read_text(encoding="utf-8"))
    document = request["document"]
    document["observation_epoch"] = EPOCH
    document["roots"].append({
        "root_id": "root:define-refresh",
        "path": DEFINE_ROOT,
    })
    document["discovery_rules"] = [
        rule
        for rule in document["discovery_rules"]
        if rule["rule_id"] != "rule:admitted-plan-definitions"
    ]
    document["discovery_rules"][:0] = [
        {
            "rule_id": "rule:admitted-plan-definitions-current",
            "root_id": "root:define-refresh",
            "input_class": "define-artifact",
            "include_globs": ["bundle-current/DEFINITIONS.json"],
        },
        {
            "rule_id": "rule:define-refresh-stage-admission",
            "root_id": "root:define-refresh",
            "input_class": "interface-contract",
            "include_globs": [
                "bundle-current/INVOKE-DEFINE-STAGE-RECEIPT.json",
                "DEFINE-BUNDLE-ADMISSION-RECEIPT-PASS.json",
            ],
        },
        {
            "rule_id": "rule:define-refresh-reassessment",
            "root_id": "root:define-refresh",
            "input_class": "owner-decision",
            "include_globs": ["OWNER-SEMANTIC-REASSESSMENT.json"],
        },
    ]
    if "owner-decision" not in document["required_input_classes"]:
        document["required_input_classes"].append("owner-decision")
    request["evidence_paths"].append({
        "pointer": f"/roots/{len(document['roots']) - 1}",
        "path": DEFINE_ROOT,
        "kind": "directory",
    })
    args.output.write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
