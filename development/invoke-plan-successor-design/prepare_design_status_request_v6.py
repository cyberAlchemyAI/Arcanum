#!/usr/bin/env python3
"""Build the Design V6 capability-status request from exact W3 receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, type=Path)
    parser.add_argument("--admission", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    request = {
        "schema_version": "invoke.capability-status.request.v1",
        "mode": "design",
        "artifact_receipt": {
            "receipt_id": "artifact:plan-successor-design-v6",
            "axis": "artifact_authored",
            "mode": "design",
            "status": "pass",
            "evidence": [str(args.stage), str(args.admission)],
            "producer_receipt": load(args.stage),
            "producer_admission_receipt": load(args.admission),
        },
        "registry_receipt": None,
        "material_package_receipt": None,
        "runtime_receipt": None,
    }
    args.output.write_text(
        json.dumps(request, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
