#!/usr/bin/env python3
"""Create the out-of-root Boundary V3 request from the approved V2 semantics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    request = json.loads(args.source.read_text(encoding="utf-8"))
    request["document"]["observation_epoch"] = (
        "2026-08-28-plan-successor-design-boundary-v3-out-of-root"
    )
    args.output.write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
