#!/usr/bin/env python3
"""Validate criterion schema, arithmetic invariants, and generated-view parity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from render_criterion import render_criterion


ROOT = Path(__file__).resolve().parent


def validate(root: Path) -> dict[str, Any]:
    blockers: list[str] = []
    try:
        schema = json.loads((root / "criterion.schema.json").read_text(encoding="utf-8"))
        criterion = json.loads((root / "CRITERION.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "block", "blockers": [f"criterion input is not readable JSON: {exc}"], "writes": 0}

    for error in sorted(Draft202012Validator(schema).iter_errors(criterion), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "$"
        blockers.append(f"schema:{location}: {error.message}")

    design = criterion.get("design", {})
    metrics = criterion.get("observable", {}).get("metrics", [])
    metric_ids = [metric.get("metric_id") for metric in metrics if isinstance(metric, dict)]
    expected = {
        "candidate_count": (len(design.get("candidate_structures", [])), 3),
        "case_count": (design.get("case_count"), 3),
        "trials_per_candidate": (design.get("trials_per_candidate"), 2),
        "sources_per_trial": (design.get("sources_per_trial"), 3),
        "total_trials": (design.get("total_trials"), 6),
        "total_source_records": (design.get("total_source_records"), 18),
        "candidate_aggregate_count": (design.get("candidate_aggregate_count"), 3),
        "metric_count": (len(metrics), 4),
    }
    for name, (actual, required) in expected.items():
        if actual != required:
            blockers.append(f"invariant:{name}: expected {required}, got {actual!r}")

    candidates = len(design.get("candidate_structures", []))
    trials_per_candidate = design.get("trials_per_candidate")
    sources_per_trial = design.get("sources_per_trial")
    if isinstance(trials_per_candidate, int) and design.get("total_trials") != candidates * trials_per_candidate:
        blockers.append("invariant: total_trials must equal candidate_count * trials_per_candidate")
    if isinstance(sources_per_trial, int) and isinstance(design.get("total_trials"), int):
        if design.get("total_source_records") != design["total_trials"] * sources_per_trial:
            blockers.append("invariant: total_source_records must equal total_trials * sources_per_trial")
    if design.get("case_count") != sources_per_trial:
        blockers.append("invariant: case_count must equal sources_per_trial")
    if design.get("candidate_aggregate_count") != candidates:
        blockers.append("invariant: candidate_aggregate_count must equal candidate_count")
    if len(metric_ids) != len(set(metric_ids)):
        blockers.append("invariant: metric IDs must be unique")
    if criterion.get("outcome_rule", {}).get("metric_order") != metric_ids:
        blockers.append("invariant: outcome metric_order must exactly match observable metric order")

    try:
        rendered = render_criterion(criterion)
        committed = (root / "CRITERION.md").read_text(encoding="utf-8")
        if committed != rendered:
            blockers.append("render: CRITERION.md differs from a clean in-memory render")
        if "four candidate aggregate tuples" in committed.lower():
            blockers.append("render: stale four-candidate aggregate wording is forbidden")
        if "three candidate aggregate tuples" not in committed.lower():
            blockers.append("render: exact three-candidate aggregate wording is missing")
    except (KeyError, TypeError, OSError) as exc:
        blockers.append(f"render: cannot render or compare criterion view: {exc}")

    return {
        "status": "pass" if not blockers else "block",
        "criterion_id": criterion.get("criterion_id"),
        "criterion_version": criterion.get("criterion_version"),
        "counts": {name: actual for name, (actual, _) in expected.items()},
        "writes": 0,
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.root.resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"CRITERION_VALIDATION={result['status']}")
        for blocker in result["blockers"]:
            print(f"BLOCK: {blocker}")
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
