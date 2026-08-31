#!/usr/bin/env python3
"""Deterministically render the human criterion view from CRITERION.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def bullet_lines(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values]


def numbered_lines(values: list[str]) -> list[str]:
    return [f"{index}. {value}" for index, value in enumerate(values, start=1)]


def render_criterion(criterion: dict[str, Any]) -> str:
    state = criterion["state"]
    freeze = criterion["freeze_policy"]
    design = criterion["design"]
    observable = criterion["observable"]
    outcome = criterion["outcome_rule"]
    discrimination = criterion["discrimination"]

    lines = [
        "<!-- Generated from CRITERION.json by render_criterion.py. Do not edit this view directly. -->",
        "",
        "# Pre-Registered Criterion: Define v2 Documentation Order",
        "",
        "## State",
        "",
        f"- Status: `{state['status']}`",
        f"- Freeze owner: {state['freeze_owner']}",
        f"- Run status: `{state['run_status']}`",
        f"- Criterion version: `{criterion['criterion_version']}`",
        "",
        freeze["prefreeze_rule"],
        "",
        freeze["change_rule"],
        "",
        "A freeze record must bind these inputs by SHA-256 and byte size:",
        "",
        *bullet_lines(freeze["required_bindings"]),
        "",
        "## One Falsifiable Hypothesis",
        "",
        criterion["hypothesis"],
        "",
        "## Fixed Candidates",
        "",
        "The three candidate structures are:",
        "",
        *numbered_lines(design["candidate_structures"]),
        "",
        (
            f"There are exactly {design['case_count']} cases, "
            f"{design['trials_per_candidate']} trials per candidate, and "
            f"{design['sources_per_trial']} source records per trial. This yields "
            f"{design['total_trials']} total trials, {design['total_source_records']} "
            f"source records, and {design['candidate_aggregate_count']} candidate aggregates."
        ),
        "",
        design["blind_map_policy"],
        "",
        "## Observable",
        "",
        "Each candidate aggregate is an ordered four-metric tuple:",
        "",
        *numbered_lines(
            [f"{metric['label']} ({metric['direction']})" for metric in observable["metrics"]]
        ),
        "",
        observable["compile_rule"],
        "",
        observable["scorecard_rule"],
        "",
        "## Mechanical Outcome Rule",
        "",
        (
            "Apply invalidation before ranking. Otherwise compare the three candidate "
            "aggregate tuples lexicographically across the four stated metrics in this order:"
        ),
        "",
        *numbered_lines(outcome["metric_order"]),
        "",
        f"- `SURVIVED`: {outcome['survived']}",
        f"- `FALSIFIED`: {outcome['falsified']}",
        f"- `INVALID`: {outcome['invalid']}",
        "",
        "Render `INVALID` if any of the following holds:",
        "",
        *numbered_lines(criterion["invalidation_conditions"]),
        "",
        "## Discrimination Check",
        "",
        f"- `SURVIVED`: {discrimination['SURVIVED']}",
        f"- `FALSIFIED`: {discrimination['FALSIFIED']}",
        f"- `INVALID`: {discrimination['INVALID']}",
        "",
        "## Non-Goals",
        "",
        *bullet_lines(criterion["non_goals"]),
        "",
    ]
    return "\n".join(lines)


def load_criterion(root: Path) -> dict[str, Any]:
    return json.loads((root / "CRITERION.json").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    rendered = render_criterion(load_criterion(root))
    output = root / "CRITERION.md"
    if args.write:
        output.write_text(rendered, encoding="utf-8")
        print("CRITERION_RENDER=written")
        return 0
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != rendered:
            print("CRITERION_RENDER=drift")
            return 2
        print("CRITERION_RENDER=pass")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
