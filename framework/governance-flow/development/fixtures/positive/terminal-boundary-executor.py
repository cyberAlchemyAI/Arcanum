#!/usr/bin/env python3
"""Write one declared local fixture output and perform no other effect."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--content", required=True)
    args = parser.parse_args()

    root = Path.cwd().resolve()
    target = (root / args.target).resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise SystemExit(f"target escapes isolated root: {args.target}") from error
    if target.exists():
        raise SystemExit("target must not exist before the fixture effect")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(args.content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
