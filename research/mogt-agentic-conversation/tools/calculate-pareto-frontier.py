#!/usr/bin/env python3
"""Calculate Pareto frontier metrics for MOGT JSONL fixture rows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


OBJECTIVE_KEYS = ["quality", "cost", "latency", "safety", "escalation_risk"]


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            row = json.loads(line)
            if isinstance(row, dict):
                rows.append(row)
    return rows


def dominates(left: dict[str, float], right: dict[str, float]) -> bool:
    return all(left[key] >= right[key] for key in OBJECTIVE_KEYS) and any(
        left[key] > right[key] for key in OBJECTIVE_KEYS
    )


def action_vectors(row: dict[str, Any]) -> dict[str, dict[str, float]]:
    vectors: dict[str, dict[str, float]] = {}
    for action in row.get("candidate_actions", []):
        action_id = action.get("action_id")
        vector = action.get("objective_vector")
        if not isinstance(action_id, str) or not isinstance(vector, dict):
            continue
        if all(isinstance(vector.get(key), (int, float)) for key in OBJECTIVE_KEYS):
            vectors[action_id] = {key: float(vector[key]) for key in OBJECTIVE_KEYS}
    return vectors


def analyze_row(row: dict[str, Any]) -> dict[str, Any]:
    vectors = action_vectors(row)
    dominated_by: dict[str, list[str]] = {action_id: [] for action_id in vectors}
    for action_id, vector in vectors.items():
        for challenger_id, challenger_vector in vectors.items():
            if action_id == challenger_id:
                continue
            if dominates(challenger_vector, vector):
                dominated_by[action_id].append(challenger_id)

    frontier = sorted(action_id for action_id, challengers in dominated_by.items() if not challengers)
    dominated_actions = sorted(action_id for action_id, challengers in dominated_by.items() if challengers)
    selected_id = (row.get("selected_action") or {}).get("action_id")
    selected_frontier = selected_id in frontier
    selected_dominated = bool(selected_id and dominated_by.get(selected_id))

    weights = {key: 1.0 / len(OBJECTIVE_KEYS) for key in OBJECTIVE_KEYS}
    scalar_scores = {
        action_id: round(sum(vector[key] * weights[key] for key in OBJECTIVE_KEYS), 6)
        for action_id, vector in vectors.items()
    }
    best_scalar = max(scalar_scores.values()) if scalar_scores else None
    selected_scalar = scalar_scores.get(selected_id)
    scalarization_sensitivity = "not_applicable"
    if best_scalar is not None and selected_scalar is not None:
        scalarization_sensitivity = (
            "selected_equal_weight_best"
            if abs(best_scalar - selected_scalar) < 0.000001
            else "selected_differs_from_equal_weight_best"
        )

    return {
        "run_id": row.get("run_id"),
        "experiment_id": row.get("experiment_id"),
        "scenario_id": row.get("scenario_id"),
        "policy_regime": row.get("policy_regime"),
        "selected_action": selected_id,
        "selected_frontier_member": selected_frontier,
        "selected_dominated": selected_dominated,
        "frontier_actions": frontier,
        "dominated_actions": dominated_actions,
        "dominated_by": dominated_by,
        "equal_weight_scalar_scores": scalar_scores,
        "scalarization_sensitivity": scalarization_sensitivity,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate MOGT Pareto/frontier metrics.")
    parser.add_argument("jsonl", type=Path, help="MOGT fixture JSONL")
    parser.add_argument("--experiment", default=None, help="Optional experiment id filter")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path")
    args = parser.parse_args()

    if not args.jsonl.exists():
        print(f"FAIL {args.jsonl}: file does not exist", file=sys.stderr)
        return 1

    analyses = [
        analyze_row(row)
        for row in load_rows(args.jsonl)
        if args.experiment is None or row.get("experiment_id") == args.experiment
    ]
    if not analyses:
        print("FAIL no rows matched input", file=sys.stderr)
        return 1

    payload = {"source": str(args.jsonl), "row_count": len(analyses), "analyses": analyses}
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"PASS wrote {args.output} ({len(analyses)} row(s))")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
