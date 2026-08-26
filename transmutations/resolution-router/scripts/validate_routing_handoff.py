#!/usr/bin/env python3
"""Validate a bound lens_packet and resolution_plan as one routing handoff."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LENS_VALIDATOR_PATH = (
    ROOT.parent / "lens-router" / "scripts" / "validate_lens_packet.py"
)
PLAN_VALIDATOR_PATH = ROOT / "scripts" / "validate_resolution_plan.py"


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load validator module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lens_validator = _load_module("arcanum_lens_packet_validator", LENS_VALIDATOR_PATH)
plan_validator = _load_module("arcanum_resolution_plan_validator", PLAN_VALIDATOR_PATH)


def validate_handoff(
    packet: Any,
    plan: Any,
    routes_path: Path = plan_validator.ROUTES_PATH,
) -> list[str]:
    """Validate both artifacts and every cross-artifact binding invariant."""
    errors = [
        f"lens_packet/{error}" for error in lens_validator.validate_packet(packet)
    ]
    errors.extend(
        f"resolution_plan/{error}"
        for error in plan_validator.validate_plan(plan, routes_path)
    )
    if errors or not isinstance(packet, dict) or not isinstance(plan, dict):
        return errors

    if plan["packet_digest"] != packet["packet_digest"]:
        errors.append(
            "handoff: resolution_plan.packet_digest does not bind the supplied lens_packet"
        )

    selected_lenses = packet["selected_lenses"]
    allocation_lenses = [item["lens"] for item in plan["lens_specific_allocation"]]
    if Counter(allocation_lenses) != Counter(selected_lenses):
        errors.append(
            "handoff: require exactly one lens_specific_allocation for every selected lens"
        )

    expected_by_lens: dict[str, set[str]] = {
        lens: {
            finding["id"]
            for finding in packet["per_lens_findings"]
            if finding["lens"] == lens
        }
        for lens in selected_lenses
    }
    allocated_ids: list[str] = []
    for allocation in plan["lens_specific_allocation"]:
        lens = allocation["lens"]
        actual_ids = set(allocation["finding_ids"])
        allocated_ids.extend(allocation["finding_ids"])
        if lens in expected_by_lens and actual_ids != expected_by_lens[lens]:
            missing = sorted(expected_by_lens[lens] - actual_ids)
            extra = sorted(actual_ids - expected_by_lens[lens])
            errors.append(
                f"handoff: allocation for {lens} must bind exactly its packet findings; "
                f"missing={missing}, extra={extra}"
            )
    duplicate_allocations = sorted(
        finding_id
        for finding_id, count in Counter(allocated_ids).items()
        if count > 1
    )
    if duplicate_allocations:
        errors.append(
            "handoff: finding IDs may occur in only one lens allocation; "
            f"duplicates={duplicate_allocations}"
        )

    expected_composed = {item["id"] for item in packet["composed_findings"]}
    actual_composed = set(plan["composed_finding_ids"])
    if actual_composed != expected_composed:
        errors.append(
            "handoff: composed_finding_ids must exactly bind packet compositions; "
            f"missing={sorted(expected_composed - actual_composed)}, "
            f"extra={sorted(actual_composed - expected_composed)}"
        )

    return errors


def _valid_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    packet = lens_validator._valid_fixture()
    plan = plan_validator._valid_fixture()
    plan["packet_digest"] = packet["packet_digest"]
    plan["lens_specific_allocation"] = [
        {
            "lens": "epistemic",
            "emphasis": "Make claim status visible.",
            "finding_ids": ["E1"],
            "activated_guarantee_ids": ["L06-evidence-ceiling"],
        },
        {
            "lens": "systemic",
            "emphasis": "Preserve the consequential transition.",
            "finding_ids": ["S1"],
            "activated_guarantee_ids": ["L09-structure-fidelity"],
        },
    ]
    plan["composed_finding_ids"] = ["C1"]
    return packet, plan


def self_test() -> None:
    packet, plan = _valid_fixture()
    assert not validate_handoff(packet, plan), validate_handoff(packet, plan)

    replay_packet = copy.deepcopy(packet)
    replay_packet["consumer"] = "another consumer"
    replay_packet["packet_digest"] = lens_validator.packet_digest(replay_packet)
    errors = validate_handoff(replay_packet, plan)
    assert any("does not bind" in error for error in errors), errors

    changed_purpose = copy.deepcopy(packet)
    changed_purpose["purpose"] = "a different purpose"
    changed_purpose["packet_digest"] = lens_validator.packet_digest(changed_purpose)
    errors = validate_handoff(changed_purpose, plan)
    assert any("does not bind" in error for error in errors), errors

    changed_boundary = copy.deepcopy(packet)
    changed_boundary["evidence_boundary"][0]["scope"]["end_line"] = 20
    changed_boundary["packet_digest"] = lens_validator.packet_digest(changed_boundary)
    errors = validate_handoff(changed_boundary, plan)
    assert any("does not bind" in error for error in errors), errors

    mismatched_lens = copy.deepcopy(plan)
    mismatched_lens["lens_specific_allocation"][1]["lens"] = "categorical"
    errors = validate_handoff(packet, mismatched_lens)
    assert any("every selected lens" in error for error in errors), errors

    missing_finding = copy.deepcopy(plan)
    missing_finding["lens_specific_allocation"][0]["finding_ids"] = ["S1"]
    errors = validate_handoff(packet, missing_finding)
    assert any("exactly its packet findings" in error for error in errors), errors

    missing_composition = copy.deepcopy(plan)
    missing_composition["composed_finding_ids"] = []
    errors = validate_handoff(packet, missing_composition)
    assert any("exactly bind packet compositions" in error for error in errors), errors

    tampered_packet = copy.deepcopy(packet)
    tampered_packet["reserved_terms"].append("authority")
    errors = validate_handoff(tampered_packet, plan)
    assert any("packet_digest" in error for error in errors), errors


def _load_json(path: str) -> Any:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", nargs="?", help="lens packet JSON file")
    parser.add_argument("plan", nargs="?", help="resolution plan JSON file")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--emit-valid-fixture", action="store_true")
    parser.add_argument(
        "--routes",
        type=Path,
        default=plan_validator.ROUTES_PATH,
        help="route manifest override for isolated validation",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("routing handoff validator self-test: PASS")
        return 0
    if args.emit_valid_fixture:
        packet, plan = _valid_fixture()
        print(json.dumps({"lens_packet": packet, "resolution_plan": plan}, indent=2))
        return 0
    if not args.packet or not args.plan:
        parser.error("packet and plan paths or --self-test are required")
    if args.packet == "-" and args.plan == "-":
        parser.error("only one input may use stdin")

    try:
        packet = _load_json(args.packet)
        plan = _load_json(args.plan)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"input: {exc}", file=sys.stderr)
        return 2

    errors = validate_handoff(packet, plan, args.routes)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("routing handoff: VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
