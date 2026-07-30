#!/usr/bin/env python3
"""Run DFE frontier goldens and deterministic replay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.frontier import canonical_bytes, derive_frontier  # noqa: E402
from validate_contracts import validate_decision_map  # noqa: E402


CASES = ["diamond", "fog", "scope", "invalidated"]
INPUTS = {
    "diamond": "diamond-map.json",
    "fog": "fog-map.json",
    "scope": "scope-map.json",
    "invalidated": "invalidated-map.json",
}
EVIDENCE = ROOT / "session-evidence/SWU-DFE-002/frontier-validation.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", type=int, default=2)
    args = parser.parse_args()
    observations = {}
    passed = True
    for case in CASES:
        document = load(ROOT / "fixtures" / INPUTS[case])
        errors = validate_decision_map(document)
        if errors:
            observations[case] = {"status": "block", "errors": errors}
            passed = False
            continue
        expected = load(ROOT / "fixtures/expected" / f"{case}-frontier.json")
        replays = [canonical_bytes(derive_frontier(document)) for _ in range(args.replay)]
        actual = json.loads(replays[0])
        case_pass = actual == expected and len(set(replays)) == 1
        passed = passed and case_pass
        observations[case] = {
            "status": "pass" if case_pass else "block",
            "frontier_ids": actual["frontier_ids"],
            "replay_identical": len(set(replays)) == 1,
        }
    result = {
        "schema_version": "dfe-frontier-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-001", "DFE-FIX-006", "DFE-FIX-009"],
        "observations": observations,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
