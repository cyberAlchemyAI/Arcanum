#!/usr/bin/env python3
"""Evaluate one self-contained Work-Pack route request."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from work_pack_route import evaluate_work_pack_route


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    request = json.loads(args.request.read_text(encoding="utf-8"))
    receipt = evaluate_work_pack_route(request)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if receipt["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
