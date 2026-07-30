#!/usr/bin/env python3
"""Validate receipt identity and semantic bindings after JSON Schema validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--step", required=True)
    parser.add_argument("--work-pack-sha256", required=True)
    parser.add_argument("--successor", required=True)
    args = parser.parse_args()

    document = json.loads(args.receipt.read_text(encoding="utf-8"))
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    reasons = [
        f"schema:{'/'.join(map(str, error.absolute_path)) or '<root>'}:{error.message}"
        for error in errors
    ]
    expected_successor = None if args.successor == "none" else args.successor
    expected = {
        "unit_id": args.unit,
        "step_id": args.step,
        "work_pack_sha256": args.work_pack_sha256,
    }
    for key, value in expected.items():
        if document.get(key) != value:
            reasons.append(f"{key}:expected={value!r}:actual={document.get(key)!r}")
    successor = document.get("successor", {})
    if successor.get("unit_id") != expected_successor:
        reasons.append("successor unit mismatch")
    if successor.get("selected") is not False:
        reasons.append("successor must remain unselected")
    material = set(document.get("material_writes", []))
    outputs = set(document.get("execution_outputs", []))
    allowed = set(document.get("allowed_writes", []))
    if material & outputs or material | outputs != allowed:
        reasons.append("write partition mismatch")
    print(json.dumps({"status": "pass" if not reasons else "block", "reasons": reasons}, sort_keys=True))
    return 0 if not reasons else 1


if __name__ == "__main__":
    raise SystemExit(main())
