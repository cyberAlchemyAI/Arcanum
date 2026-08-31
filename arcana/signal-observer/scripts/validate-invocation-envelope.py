#!/usr/bin/env python3
"""Validate one invocation envelope without appending observability state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def reject_constant(value: str) -> None: raise ValueError(f"non-finite JSON value is forbidden: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result: raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--envelope", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[1] / "schemas" / "invocation-envelope-v1.schema.json")
    args = parser.parse_args()
    try: envelope = load(args.envelope); schema = load(args.schema)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error: print(f"ERROR: {error}", file=sys.stderr); return 2
    errors = sorted(Draft202012Validator(schema).iter_errors(envelope), key=lambda item: (list(item.absolute_path), item.message))
    if errors:
        for error in errors: print(f"ERROR: /{'/'.join(map(str, error.absolute_path))}: {error.message}", file=sys.stderr)
        return 1
    print("OBSERVATION_ENVELOPE=valid\nAUTHORITY_EFFECT=none\nAPPEND_ATTEMPT_COUNT=0"); return 0


if __name__ == "__main__": raise SystemExit(main())
