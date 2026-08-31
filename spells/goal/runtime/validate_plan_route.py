#!/usr/bin/env python3
"""Validate a projected Goal route without starting the Goal loop."""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[1] / "schemas" / "plan-route-contract-v1.schema.json")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: (list(item.absolute_path), item.message))
    if errors:
        for error in errors:
            print(f"ERROR: /{'/'.join(map(str, error.absolute_path))}: {error.message}", file=sys.stderr)
        return 1
    print("GOAL_PLAN_ROUTE=valid")
    print("GOAL_LOOP_ATTEMPT_COUNT=0")
    print("AUTHORITY_EFFECT=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
