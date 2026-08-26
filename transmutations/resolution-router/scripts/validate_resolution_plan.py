#!/usr/bin/env python3
"""Validate resolution_plan structure and routing semantics."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError as exc:
    if exc.name != "jsonschema":
        raise
    requirement = Path(__file__).resolve().parents[1] / "requirements.txt"
    print(
        "missing runtime dependency 'jsonschema'; install the declared requirement "
        f"with: python -m pip install -r {requirement}",
        file=sys.stderr,
    )
    raise SystemExit(3) from exc


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
SCHEMA_PATH = REFERENCES / "resolution-plan.schema.json"
GUARANTEES_PATH = REFERENCES / "resolution-guarantees.md"
ROUTES_PATH = REFERENCES / "routes.md"
RANK = {"low": 0, "medium": 1, "high": 2}
ROLE_FOR_TIER = {
    "low": "low writer",
    "medium": "medium writer",
    "high": "high writer",
}


def _guarantee_sets() -> dict[str, set[str]]:
    ids = re.findall(
        r"^- `([LMH][0-9]{2}-[a-z0-9-]+)`:",
        GUARANTEES_PATH.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    low = {item for item in ids if item.startswith("L")}
    medium = low | {item for item in ids if item.startswith("M")}
    high = medium | {item for item in ids if item.startswith("H")}
    if not low or medium == low or high == medium:
        raise ValueError("could not derive cumulative guarantee sets")
    return {"low": low, "medium": medium, "high": high}


def _route_manifest(routes_path: Path = ROUTES_PATH) -> dict[str, dict[str, str]]:
    routes: dict[str, dict[str, str]] = {}
    for line in routes_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] not in ROLE_FOR_TIER.values():
            continue
        routes[cells[0]] = {
            "skill_id": cells[1],
            "path": cells[2],
            "status": cells[3],
        }
    if set(routes) != set(ROLE_FOR_TIER.values()):
        raise ValueError("route manifest is missing a resolution writer")
    return routes


def validate_plan(plan: Any, routes_path: Path = ROUTES_PATH) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = [
        "schema: " + error.message
        for error in sorted(
            Draft202012Validator(schema).iter_errors(plan),
            key=lambda item: list(item.absolute_path),
        )
    ]
    if errors or not isinstance(plan, dict):
        return errors

    guarantees = _guarantee_sets()
    routes = _route_manifest(routes_path)
    selected = plan["selected_resolution"]
    requested = plan["requested_resolution"]
    actual_ids = set(plan["guarantee_ids"])
    expected_ids = guarantees[selected]
    if actual_ids != expected_ids:
        missing = sorted(expected_ids - actual_ids)
        extra = sorted(actual_ids - expected_ids)
        errors.append(
            f"semantic: guarantee_ids must exactly match {selected}; missing={missing}, extra={extra}"
        )

    if requested is not None and RANK[selected] < RANK[requested]:
        errors.append(
            f"semantic: selected resolution {selected} silently downgrades requested {requested}"
        )

    promotion = plan["promotion"]
    if requested is not None and RANK[selected] > RANK[requested] and promotion is None:
        errors.append("semantic: promoted requested resolution requires a promotion record")
    if requested is None and promotion is not None:
        errors.append("semantic: promotion must be null when there is no requested baseline")
    if requested == selected and promotion is not None:
        errors.append("semantic: promotion must be null when selected equals requested")
    if promotion is not None:
        if requested is not None and promotion["from"] != requested:
            errors.append("semantic: promotion.from must equal requested_resolution")
        if promotion["to"] != selected:
            errors.append("semantic: promotion.to must equal selected_resolution")
        if RANK[promotion["to"]] <= RANK[promotion["from"]]:
            errors.append("semantic: promotion must move to a higher tier")
        if promotion["activating_guarantee_id"] not in actual_ids:
            errors.append("semantic: activating guarantee must occur in guarantee_ids")
        required_prefix = {"medium": "M", "high": "H"}.get(selected)
        if required_prefix and not promotion["activating_guarantee_id"].startswith(required_prefix):
            errors.append(
                f"semantic: promotion to {selected} requires an activating {required_prefix} guarantee"
            )

    seen_lenses: set[str] = set()
    for allocation in plan["lens_specific_allocation"]:
        lens = allocation["lens"]
        if lens in seen_lenses:
            errors.append(f"semantic: duplicate allocation for lens {lens}")
        seen_lenses.add(lens)
        unknown = set(allocation["activated_guarantee_ids"]) - actual_ids
        if unknown:
            errors.append(
                f"semantic: allocation for {lens} activates guarantees outside selected tier: {sorted(unknown)}"
            )

    expected_target = routes[ROLE_FOR_TIER[selected]]
    if plan["target_writer"] != expected_target:
        errors.append(
            f"semantic: target_writer must match manifest entry {expected_target}"
        )
    elif expected_target["status"] == "available":
        resolved = (ROOT / expected_target["path"]).resolve()
        if not resolved.is_file():
            errors.append(f"semantic: available target is missing: {resolved}")

    return errors


def _valid_fixture() -> dict[str, Any]:
    guarantees = sorted(_guarantee_sets()["low"])
    target = _route_manifest()["low writer"]
    return {
        "plan_version": "2.0",
        "packet_digest": "sha256:" + "0" * 64,
        "requested_resolution": "low",
        "selected_resolution": "low",
        "reason": "Low is sufficient for the stated purpose.",
        "guarantee_ids": guarantees,
        "promotion": None,
        "lens_specific_allocation": [
            {
                "lens": "epistemic",
                "emphasis": "Make claim status visible.",
                "finding_ids": ["E1"],
                "activated_guarantee_ids": ["L06-evidence-ceiling"],
            }
        ],
        "composed_finding_ids": [],
        "target_writer": target,
    }


def self_test() -> None:
    valid = _valid_fixture()
    assert not validate_plan(valid), validate_plan(valid)

    mutations = []
    case = copy.deepcopy(valid)
    case["requested_resolution"] = "high"
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["guarantee_ids"] = ["L99-fake"]
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["promotion"] = {
        "from": "low",
        "to": "medium",
        "activating_guarantee_id": "M01-operational-model",
        "reason": "Needs operational reasoning.",
    }
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["target_writer"] = {
        "skill_id": "attacker-writer",
        "path": "../../evil/SKILL.md",
        "status": "available",
    }
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["lens_specific_allocation"][0]["activated_guarantee_ids"] = ["H99-fake"]
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["requested_resolution"] = "low"
    case["selected_resolution"] = "high"
    case["guarantee_ids"] = sorted(_guarantee_sets()["high"])
    case["target_writer"] = _route_manifest()["high writer"]
    case["promotion"] = {
        "from": "medium",
        "to": "high",
        "activating_guarantee_id": "H01-mechanisms-interfaces",
        "reason": "Needs high-tier mechanisms.",
    }
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["requested_resolution"] = "high"
    case["selected_resolution"] = "high"
    case["guarantee_ids"] = sorted(_guarantee_sets()["high"])
    case["target_writer"] = _route_manifest()["high writer"]
    case["promotion"] = {
        "from": "low",
        "to": "high",
        "activating_guarantee_id": "H01-mechanisms-interfaces",
        "reason": "Spurious promotion.",
    }
    mutations.append(case)
    case = copy.deepcopy(valid)
    case["requested_resolution"] = "low"
    case["selected_resolution"] = "high"
    case["guarantee_ids"] = sorted(_guarantee_sets()["high"])
    case["target_writer"] = _route_manifest()["high writer"]
    case["promotion"] = {
        "from": "low",
        "to": "high",
        "activating_guarantee_id": "M01-operational-model",
        "reason": "Medium-only evidence cannot justify high.",
    }
    mutations.append(case)

    for index, mutation in enumerate(mutations, start=1):
        assert validate_plan(mutation), f"invalid fixture {index} unexpectedly passed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", nargs="?", help="JSON file or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--emit-valid-fixture", action="store_true")
    parser.add_argument(
        "--routes",
        type=Path,
        default=ROUTES_PATH,
        help="route manifest override for isolated validation",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("resolution plan validator self-test: PASS")
        return 0
    if args.emit_valid_fixture:
        print(json.dumps(_valid_fixture(), indent=2, ensure_ascii=False))
        return 0
    if not args.plan:
        parser.error("plan path or --self-test is required")

    try:
        raw = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
        plan = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"input: {exc}", file=sys.stderr)
        return 2

    errors = validate_plan(plan, args.routes)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("resolution plan: VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
