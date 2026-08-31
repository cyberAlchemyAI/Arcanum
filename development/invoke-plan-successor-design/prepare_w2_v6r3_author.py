#!/usr/bin/env python3
"""Create W2 V6R3 by making bundle production an explicit workflow stage."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"expected one source fragment, found {count}: {old[:120]}")
    return text.replace(old, new)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    text = args.source.read_text(encoding="utf-8")
    text = text.replace(
        '"next_id": "workflow:admit-plan-bundle"',
        '"next_id": "workflow:produce-plan-bundle"',
    )
    text = replace_once(
        text,
        '"action": "Evaluate every row in the consumer applicability matrix, produce each true-branch projection, and record exact negative evidence for each false branch.", "next_step_ids": ["workflow:admit-plan-bundle"]}},',
        '"action": "Evaluate every row in the consumer applicability matrix, produce each true-branch projection, and record exact negative evidence for each false branch.", "next_step_ids": ["workflow:produce-plan-bundle"]}},\n'
        '        {"fact_id": "workflow:produce-plan-bundle", "fact_kind": "workflow-step", "name": "Produce complete Plan bundle", "owner": "invoke-plan-owner", "attributes": {"actor_or_component_id": "component:plan-bundle-producer", "action": "Write the source, normalized graph, human views, consumer projections, and negative applicability evidence into one absent staging directory, validate the complete inventory, and publish the candidate atomically.", "next_step_ids": ["workflow:admit-plan-bundle"]}},',
    )
    text = replace_once(
        text,
        '"architecture:persistence-concurrency": ["component:plan-bundle-producer", "component:plan-bundle-admission-validator", "contract:plan-bundle-admission"],',
        '"architecture:persistence-concurrency": ["component:plan-bundle-producer", "component:plan-bundle-admission-validator", "contract:plan-bundle-admission", "workflow:produce-plan-bundle"],',
    )
    text = replace_once(
        text,
        '"workflow:project-consumer-contracts"],',
        '"workflow:project-consumer-contracts", "workflow:produce-plan-bundle"],',
    )
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
