#!/usr/bin/env python3
"""Compile one canonical Plan v2 source into an atomic deterministic bundle."""

import argparse
import sys
from pathlib import Path

from plan_successor_support import compile_bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--schema-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    errors = compile_bundle(args.source.resolve(), args.output_dir, args.repo_root.resolve(), args.schema_dir.resolve())
    if errors:
        for error in errors: print(f"BLOCK: {error}", file=sys.stderr)
        return 1
    print(f"PLAN_BUNDLE={args.output_dir}")
    print("RESULT=pass")
    print("AUTHORITY_EFFECT=none")
    return 0


if __name__ == "__main__": raise SystemExit(main())
