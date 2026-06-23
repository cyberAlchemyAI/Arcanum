#!/usr/bin/env python3
"""Run public-safe goal runtime fixtures and validate emitted JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
FIXTURES = ROOT / "validation" / "fixtures"
RESULTS = ROOT / "validation" / "results"
SCHEMAS = ROOT / "schemas"

sys.path.insert(0, str(RUNTIME))
from goal_loop import (  # noqa: E402
    audit_receipt,
    build_telemetry_signal,
    build_dispatch_route,
    build_execution_receipt,
    build_staged_delta,
    classify_risk,
    evaluate_approval_boundary,
    run_gap_discovery,
    run_goal_loop,
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def validate(schema_name: str, payload: dict) -> list[str]:
    schema = load_json(SCHEMAS / schema_name)
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: error.path)
    return [error.message for error in errors]


def main() -> int:
    loop_fixtures = [
        ("read_only_frontier", "PASS", "none"),
        ("protected_frontier", "STOP", "t3-node"),
        ("missing_source", "BLOCK", "source-authority"),
    ]
    delegation_fixtures = [
        ("delegation_staging", True),
        ("audit_veto", False),
    ]
    approval_fixtures = [
        ("approval_exact", "ready-for-craft-apply", "none"),
        ("ambient_approval", "blocked", "ambient-approval"),
    ]
    gap_fixtures = [
        ("gap_discovery", "PASS", "dedupe-complete"),
        ("budget_stop", "STOP", "budget-ceiling"),
    ]
    rows: list[str] = []
    delegation_rows: list[str] = []
    approval_rows: list[str] = []
    gap_rows: list[str] = []
    failures: list[str] = []
    RESULTS.mkdir(parents=True, exist_ok=True)

    for fixture_id, expected_result, expected_stop in loop_fixtures:
        payload = load_json(FIXTURES / f"{fixture_id}.json")
        frontier, result = run_goal_loop(payload)

        if frontier is not None:
            frontier_errors = validate("frontier-snapshot.schema.json", frontier)
            if frontier_errors:
                failures.append(f"{fixture_id} frontier: {'; '.join(frontier_errors)}")
            write_json(RESULTS / f"{fixture_id}.frontier-snapshot.json", frontier)
        else:
            frontier_errors = []

        result_errors = validate("goal-loop-result.schema.json", result)
        if result_errors:
            failures.append(f"{fixture_id} result: {'; '.join(result_errors)}")
        write_json(RESULTS / f"{fixture_id}.goal-loop-result.json", result)

        if result["result"] != expected_result:
            failures.append(f"{fixture_id}: expected result {expected_result}, got {result['result']}")
        if result["stop_reason"] != expected_stop:
            failures.append(f"{fixture_id}: expected stop {expected_stop}, got {result['stop_reason']}")

        rows.append(
            f"| `{fixture_id}` | {result['result']} | {result['stop_reason']} | "
            f"{'pass' if not frontier_errors else 'block'} | {'pass' if not result_errors else 'block'} |"
        )

    for fixture_id, expect_delta in delegation_fixtures:
        payload = load_json(FIXTURES / f"{fixture_id}.json")
        route = build_dispatch_route(payload)
        if route is None:
            failures.append(f"{fixture_id}: route was not built")
            continue
        receipt = build_execution_receipt(payload, route)
        audit = audit_receipt(payload, receipt)
        delta = build_staged_delta(payload, receipt, audit)

        receipt_errors = validate("execution-receipt.schema.json", receipt)
        if receipt_errors:
            failures.append(f"{fixture_id} receipt: {'; '.join(receipt_errors)}")
        if expect_delta and delta is None:
            failures.append(f"{fixture_id}: expected staged delta")
        if not expect_delta and delta is not None:
            failures.append(f"{fixture_id}: expected audit veto to block staged delta")

        delta_state = "n/a"
        if delta is not None:
            delta_errors = validate("staged-delta.schema.json", delta)
            if delta_errors:
                failures.append(f"{fixture_id} delta: {'; '.join(delta_errors)}")
            delta_state = delta["promotion_state"]
            write_json(RESULTS / f"{fixture_id}.staged-delta.json", delta)

        write_json(RESULTS / f"{fixture_id}.dispatch.json", route)
        write_json(RESULTS / f"{fixture_id}.execution-receipt.json", receipt)
        write_json(RESULTS / f"{fixture_id}.audit-verdict.json", audit)
        delegation_rows.append(
            f"| `{fixture_id}` | {receipt['status']} | {audit['verdict']} | "
            f"{delta_state} | {'pass' if not receipt_errors else 'block'} |"
        )

    for fixture_id, expected_state, expected_stop in approval_fixtures:
        payload = load_json(FIXTURES / f"{fixture_id}.json")
        boundary = evaluate_approval_boundary(payload)
        token = payload.get("approval_token")
        token_state = "n/a"
        if isinstance(token, dict):
            token_errors = validate("approval-token.schema.json", token)
            if token_errors:
                failures.append(f"{fixture_id} approval token: {'; '.join(token_errors)}")
                token_state = "block"
            else:
                token_state = "pass"
            write_json(RESULTS / f"{fixture_id}.approval-token.json", token)
        if boundary["state"] != expected_state:
            failures.append(f"{fixture_id}: expected state {expected_state}, got {boundary['state']}")
        if boundary["stop_reason"] != expected_stop:
            failures.append(f"{fixture_id}: expected stop {expected_stop}, got {boundary['stop_reason']}")
        write_json(RESULTS / f"{fixture_id}.apply-boundary.json", boundary)
        approval_rows.append(
            f"| `{fixture_id}` | {boundary['state']} | {boundary['stop_reason']} | {token_state} |"
        )

    for fixture_id, expected_result, expected_stop in gap_fixtures:
        payload = load_json(FIXTURES / f"{fixture_id}.json")
        discovery = run_gap_discovery(payload)
        if discovery["result"] != expected_result:
            failures.append(f"{fixture_id}: expected result {expected_result}, got {discovery['result']}")
        if discovery["stop_reason"] != expected_stop:
            failures.append(f"{fixture_id}: expected stop {expected_stop}, got {discovery['stop_reason']}")
        write_json(RESULTS / f"{fixture_id}.gap-discovery.json", discovery)
        gap_rows.append(
            f"| `{fixture_id}` | {discovery['result']} | {discovery['stop_reason']} | "
            f"{len(discovery['proposals'])} | {len(discovery['duplicates'])} |"
        )

    telemetry_payload = load_json(FIXTURES / "delegation_staging.json")
    risk_counts, _reasons = classify_risk(telemetry_payload)
    telemetry = build_telemetry_signal(
        goal_context_id=str(telemetry_payload["goal_context_id"]),
        round_index=1,
        frontier_size=len(telemetry_payload.get("nodes", [])),
        risk_counts=risk_counts,
        stop_reason="none",
        nodes_dispatched=1,
        staged_deltas=1,
    )
    telemetry_errors = validate("telemetry-signal.schema.json", telemetry)
    if telemetry_errors:
        failures.append("telemetry: " + "; ".join(telemetry_errors))
    write_json(RESULTS / "delegation_staging.telemetry-signal.json", telemetry)

    report = "\n".join(
        [
            "# Goal Runtime Fixture Report",
            "",
            "| Fixture | Result | Stop Reason | Frontier Schema | Result Schema |",
            "| --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Delegation And Staging",
            "",
            "| Fixture | Receipt | Audit | Delta | Receipt Schema |",
            "| --- | --- | --- | --- | --- |",
            *delegation_rows,
            "",
            "## Approval Boundary",
            "",
            "| Fixture | State | Stop Reason | Token Schema |",
            "| --- | --- | --- | --- |",
            *approval_rows,
            "",
            "## Gap Discovery",
            "",
            "| Fixture | Result | Stop Reason | Proposals | Duplicates |",
            "| --- | --- | --- | --- | --- |",
            *gap_rows,
            "",
            "## Telemetry",
            "",
            "| Fixture | Telemetry Schema |",
            "| --- | --- |",
            f"| `delegation_staging` | {'pass' if not telemetry_errors else 'block'} |",
            "",
            f"Overall: {'pass' if not failures else 'block'}",
            "",
        ]
    )
    (RESULTS / "fixture-report.md").write_text(report, encoding="utf-8")

    if failures:
        print("\n".join(failures))
        return 1
    print("goal-fixtures-pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
