#!/usr/bin/env python3
"""Validate MOGT experiment run JSONL fixtures.

This validator intentionally avoids third-party dependencies so the first MOGT
schema proof can run in a fresh local checkout. It enforces the project-specific
contract documented in experiments/schema/mogt-run.schema.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


COMMON_REQUIRED = [
    "experiment_id",
    "run_id",
    "timestamp",
    "project_id",
    "scenario_id",
    "policy_regime",
    "model",
    "model_temperature",
    "system_prompt_hash",
    "operator",
    "objective_vector",
    "candidate_actions",
    "selected_action",
    "policy_trace",
    "reviewer_scores",
    "token_cost",
    "latency_ms",
    "turn_count",
    "tool_calls",
    "protocol_deviations",
]

OBJECTIVE_KEYS = [
    "quality",
    "cost",
    "latency",
    "safety",
    "escalation_risk",
]

POLICY_REGIMES = {
    "heuristic",
    "weighted_sum",
    "pareto_guided",
    "bargaining_guided",
}

EXPERIMENT_FIELDS = {
    "E1": ["traceability_coverage", "acceptance_score"],
    "E2": [
        "dominated_selection",
        "decision_quality_score",
        "regret_or_proxy",
        "frontier_membership",
    ],
    "E3": [
        "convergence_status",
        "cycle_count",
        "escalation_events",
        "conflict_resolution_quality",
    ],
    "E4": [
        "overhead_acceptability_ratio",
        "quality_retention",
        "reviewer_burden",
    ],
}

SCORE_FIELDS = {
    "traceability_coverage",
    "acceptance_score",
    "decision_quality_score",
    "conflict_resolution_quality",
    "quality_retention",
}


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_score(value: Any, path: str, errors: list[str]) -> None:
    if not is_number(value) or value < 0 or value > 1:
        errors.append(f"{path}: expected number between 0 and 1")


def validate_non_negative_number(value: Any, path: str, errors: list[str]) -> None:
    if not is_number(value) or value < 0:
        errors.append(f"{path}: expected non-negative number")


def validate_non_negative_int(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        errors.append(f"{path}: expected non-negative integer")


def validate_objective_vector(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return
    for key in OBJECTIVE_KEYS:
        if key not in value:
            errors.append(f"{path}.{key}: missing required objective")
        else:
            validate_score(value[key], f"{path}.{key}", errors)
    for key, score in value.items():
        if key in OBJECTIVE_KEYS:
            continue
        validate_score(score, f"{path}.{key}", errors)


def validate_row(row: dict[str, Any], line_no: int) -> list[str]:
    errors: list[str] = []
    prefix = f"line {line_no}"

    for field in COMMON_REQUIRED:
        if field not in row:
            errors.append(f"{prefix}.{field}: missing required field")

    experiment_id = row.get("experiment_id")
    if experiment_id not in EXPERIMENT_FIELDS:
        errors.append(f"{prefix}.experiment_id: expected one of E1, E2, E3, E4")
    else:
        for field in EXPERIMENT_FIELDS[experiment_id]:
            if field not in row:
                errors.append(f"{prefix}.{field}: missing required {experiment_id} field")

    if row.get("project_id") != "mogt-agentic-conversation":
        errors.append(f"{prefix}.project_id: expected mogt-agentic-conversation")

    if row.get("policy_regime") not in POLICY_REGIMES:
        errors.append(
            f"{prefix}.policy_regime: expected one of {', '.join(sorted(POLICY_REGIMES))}"
        )

    timestamp = row.get("timestamp")
    if isinstance(timestamp, str):
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"{prefix}.timestamp: expected ISO 8601 date-time")
    elif "timestamp" in row:
        errors.append(f"{prefix}.timestamp: expected string")

    if "objective_vector" in row:
        validate_objective_vector(row["objective_vector"], f"{prefix}.objective_vector", errors)

    candidate_actions = row.get("candidate_actions")
    if "candidate_actions" in row:
        if not isinstance(candidate_actions, list) or not candidate_actions:
            errors.append(f"{prefix}.candidate_actions: expected non-empty array")
        else:
            action_ids = set()
            for idx, action in enumerate(candidate_actions):
                action_path = f"{prefix}.candidate_actions[{idx}]"
                if not isinstance(action, dict):
                    errors.append(f"{action_path}: expected object")
                    continue
                action_id = action.get("action_id")
                if not isinstance(action_id, str) or not action_id:
                    errors.append(f"{action_path}.action_id: expected non-empty string")
                else:
                    action_ids.add(action_id)
                if "objective_vector" not in action:
                    errors.append(f"{action_path}.objective_vector: missing required field")
                else:
                    validate_objective_vector(
                        action["objective_vector"], f"{action_path}.objective_vector", errors
                    )
        selected_action = row.get("selected_action")
        if isinstance(selected_action, dict) and candidate_actions:
            selected_id = selected_action.get("action_id")
            if selected_id not in {a.get("action_id") for a in candidate_actions if isinstance(a, dict)}:
                errors.append(f"{prefix}.selected_action.action_id: not present in candidate_actions")

    selected_action = row.get("selected_action")
    if "selected_action" in row:
        if not isinstance(selected_action, dict):
            errors.append(f"{prefix}.selected_action: expected object")
        else:
            if not isinstance(selected_action.get("action_id"), str) or not selected_action.get("action_id"):
                errors.append(f"{prefix}.selected_action.action_id: expected non-empty string")
            if not isinstance(selected_action.get("selection_reason"), str) or not selected_action.get("selection_reason"):
                errors.append(f"{prefix}.selected_action.selection_reason: expected non-empty string")

    reviewer_scores = row.get("reviewer_scores")
    if "reviewer_scores" in row:
        if not isinstance(reviewer_scores, dict) or not reviewer_scores:
            errors.append(f"{prefix}.reviewer_scores: expected non-empty object")
        else:
            for key, value in reviewer_scores.items():
                validate_score(value, f"{prefix}.reviewer_scores.{key}", errors)

    if "model_temperature" in row:
        validate_non_negative_number(row["model_temperature"], f"{prefix}.model_temperature", errors)
    for field in ["token_cost", "latency_ms", "turn_count", "tool_calls"]:
        if field in row:
            validate_non_negative_int(row[field], f"{prefix}.{field}", errors)

    if "policy_trace" in row and not isinstance(row["policy_trace"], list):
        errors.append(f"{prefix}.policy_trace: expected array")
    if "protocol_deviations" in row and not isinstance(row["protocol_deviations"], list):
        errors.append(f"{prefix}.protocol_deviations: expected array")

    for field in SCORE_FIELDS:
        if field in row:
            validate_score(row[field], f"{prefix}.{field}", errors)

    if "dominated_selection" in row and not isinstance(row["dominated_selection"], bool):
        errors.append(f"{prefix}.dominated_selection: expected boolean")
    if "frontier_membership" in row and not isinstance(row["frontier_membership"], bool):
        errors.append(f"{prefix}.frontier_membership: expected boolean")
    if "regret_or_proxy" in row:
        validate_non_negative_number(row["regret_or_proxy"], f"{prefix}.regret_or_proxy", errors)
    for field in ["cycle_count", "escalation_events"]:
        if field in row:
            validate_non_negative_int(row[field], f"{prefix}.{field}", errors)
    if "overhead_acceptability_ratio" in row:
        validate_non_negative_number(
            row["overhead_acceptability_ratio"], f"{prefix}.overhead_acceptability_ratio", errors
        )
    if "reviewer_burden" in row:
        validate_non_negative_number(row["reviewer_burden"], f"{prefix}.reviewer_burden", errors)

    return errors


def validate_jsonl(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    rows = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            rows += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(row, dict):
                errors.append(f"line {line_no}: expected JSON object")
                continue
            errors.extend(validate_row(row, line_no))
    if rows == 0:
        errors.append("file: expected at least one JSONL row")
    return rows, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MOGT run JSONL rows.")
    parser.add_argument("jsonl", nargs="+", type=Path, help="JSONL file(s) to validate")
    args = parser.parse_args()

    total_errors: list[str] = []
    for path in args.jsonl:
        if not path.exists():
            total_errors.append(f"{path}: file does not exist")
            continue
        rows, errors = validate_jsonl(path)
        if errors:
            print(f"FAIL {path} ({rows} row(s))")
            for error in errors:
                print(f"  - {error}")
            total_errors.extend(f"{path}: {error}" for error in errors)
        else:
            print(f"PASS {path} ({rows} row(s))")

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
