#!/usr/bin/env python3
"""Materialize the out-of-root W1 author from the historical V2 candidate."""

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
    text = text.replace(
        'EPOCH = "2026-08-28-plan-successor-design-boundary-v2"',
        'EPOCH = "2026-08-28-plan-successor-design-boundary-v3-out-of-root"',
    )
    text = text.replace(
        'BASE = "arcanum/spells/invoke/development/plan-successor-design"',
        'BASE = "arcanum/development/invoke-plan-successor-design"',
    )
    text = text.replace(
        'PLAN-SUCCESSOR-DESIGN-OWNER-DECISION.json',
        'PLAN-SUCCESSOR-DESIGN-OWNER-DECISION-V3.json',
    )
    text = text.replace('NO-PRIOR-DESIGN.json', 'NO-PRIOR-DESIGN-V3.json')
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
