#!/usr/bin/env python3
"""Create W2 V6R2 by removing the post-boundary Distill report reference."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    text = args.source.read_text(encoding="utf-8")
    old = (
        '"evidence_ref": exact(repo / '
        '"arcanum/development/invoke-plan-successor-design/'
        'DISTILL-BALANCER-BLOCK-V6.json", repo),'
    )
    new = '"evidence_ref": decision_ref,'
    if text.count(old) != 1:
        raise ValueError("expected exactly one post-boundary Distill evidence reference")
    args.output.write_text(text.replace(old, new), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
