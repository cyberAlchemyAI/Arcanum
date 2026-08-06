#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fast_execution_entry_guard import classify_fast_entry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    request = json.loads(args.input.read_text(encoding="utf-8"))
    receipt = classify_fast_entry(request)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if receipt["decision"] != "block" else 2


if __name__ == "__main__":
    raise SystemExit(main())
