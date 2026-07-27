#!/usr/bin/env python3
"""Validate deterministic task-session-until-blocker chain semantics."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def evaluate(case: dict[str, Any]) -> tuple[str, list[str]]:
    frontier = case["captured_frontier"]
    scope = case["scope"]
    if not isinstance(frontier, list) or not frontier or len(frontier) != len(set(frontier)):
        return "BLOCK", []

    expected = frontier[0]
    invoked: list[str] = []
    cursors: set[str] = set()

    for step in case["steps"]:
        swu_id = step.get("swu_id")
        if swu_id != expected or swu_id in invoked:
            return "BLOCK", invoked
        invoked.append(swu_id)

        cursor = step.get("cursor")
        if not isinstance(cursor, str) or not cursor or cursor in cursors:
            return "BLOCK", invoked
        cursors.add(cursor)

        if step.get("execution") not in {"PASS", "FLAG"}:
            return "BLOCK", invoked

        closeout = step.get("closeout")
        if closeout == "PASS":
            if step.get("owner_joined") is not True:
                return "BLOCK", invoked
        elif closeout == "NO_OP":
            if step.get("no_op_evidence") is not True:
                return "BLOCK", invoked
        else:
            return "BLOCK", invoked

        successor = step.get("next")
        if successor is None:
            if len(invoked) == len(frontier):
                return "COMPLETE", invoked
            return "BLOCK", invoked
        if not isinstance(successor, dict):
            return "BLOCK", invoked
        if not (
            successor.get("scope") == scope
            and successor.get("declared") is True
            and successor.get("dependency_ready") is True
            and successor.get("candidate_count") == 1
        ):
            return "BLOCK", invoked

        next_id = successor.get("swu_id")
        if next_id not in frontier or next_id in invoked:
            return "BLOCK", invoked
        if next_id != frontier[len(invoked)]:
            return "BLOCK", invoked
        expected = next_id

    return "BLOCK", invoked


def main() -> int:
    fixture_path = Path(__file__).parent / "fixtures" / "chain-cases.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in payload["cases"]:
        result, invoked = evaluate(case)
        if result != case["expected_result"] or invoked != case["expected_invoked"]:
            failures.append(
                f"{case['id']}: expected "
                f"{case['expected_result']}/{case['expected_invoked']}, "
                f"received {result}/{invoked}"
            )
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print(f"RESULT passed={len(payload['cases']) - len(failures)} failed={len(failures)}")
        return 1
    print(f"RESULT passed={len(payload['cases'])} failed=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
