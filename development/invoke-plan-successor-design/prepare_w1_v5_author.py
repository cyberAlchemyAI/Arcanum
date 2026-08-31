#!/usr/bin/env python3
"""Create the W1 V5 author bound to snapshot evidence and current Define."""

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
    replacements = {
        'EPOCH = "2026-08-28-plan-successor-design-boundary-v3-out-of-root"': 'EPOCH = "2026-08-28-plan-successor-design-boundary-v5-snapshot"',
        'PLAN-SUCCESSOR-DESIGN-OWNER-DECISION-V3.json': 'PLAN-SUCCESSOR-DESIGN-OWNER-DECISION-V5.json',
        'NO-PRIOR-DESIGN-V3.json': 'NO-PRIOR-DESIGN-V5.json',
        'pick("plan-successor-define/bundle-v4/DEFINITIONS.json")': 'pick("bundle-current/DEFINITIONS.json")',
        'pick("spells/invoke/plan.md")': 'pick("materials/root-invoke/plan.md")',
        'pick("spells/goal/README.md")': 'pick("materials/root-goal/README.md")',
        'arcanum/spells/invoke/development/plan-successor-define/bundle-v4/INVOKE-DEFINE-STAGE-RECEIPT.json': 'arcanum/development/invoke-plan-successor-define-refresh/bundle-current/INVOKE-DEFINE-STAGE-RECEIPT.json',
        'arcanum/spells/invoke/development/plan-successor-define/DEFINE-BUNDLE-ADMISSION-RECEIPT-4.json': 'arcanum/development/invoke-plan-successor-define-refresh/DEFINE-BUNDLE-ADMISSION-RECEIPT-PASS.json',
    }
    for old, new in replacements.items():
        if old not in text:
            raise ValueError(f"missing expected source fragment: {old}")
        text = text.replace(old, new)
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
