#!/usr/bin/env python3
"""Run the five typed DFE reconciliation fixtures."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.frontier import canonical_digest  # noqa: E402
from runtime.reconcile import reconcile  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-004/reconciliation-validation.json"
CASES = ["fog", "invalidation", "add", "supersede", "unblock"]


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    observations = {}
    passed = True
    for case in CASES:
        map_path = ROOT / "fixtures" / ("fog-map.json" if case == "fog" else "diamond-map.json")
        document = load(map_path)
        before = file_digest(map_path)
        resolution = load(ROOT / "fixtures" / f"{case}-resolution.json")
        claim = {
            "claim_id": f"claim-{resolution['decision_id']}",
            "decision_id": resolution["decision_id"],
            "source_digest": canonical_digest(document),
            "owner": resolution["owner"],
            "status": "active",
        }
        actual = reconcile(document, claim, resolution)
        expected = load(ROOT / "fixtures/expected" / f"{case}-reconciliation.json")
        unchanged = before == file_digest(map_path)
        case_pass = actual == expected and unchanged and actual["authority"] == "proposal"
        passed = passed and case_pass
        observations[case] = {
            "status": "pass" if case_pass else "block",
            "source_unchanged": unchanged,
            "proposal_digest": actual["proposed_map_digest"],
        }
    result = {
        "schema_version": "dfe-reconciliation-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-005", "DFE-FIX-007"],
        "observations": observations,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
