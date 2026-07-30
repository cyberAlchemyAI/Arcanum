#!/usr/bin/env python3
"""Run current, stale, and competing DFE claim fixtures."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.claims import canonical_digest, claim_decision  # noqa: E402
from runtime.frontier import derive_frontier  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-003/claim-validation.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    decision_map = load(ROOT / "fixtures/diamond-map.json")
    initial_store = load(ROOT / "fixtures/active-claim.json")
    frontier = derive_frontier(decision_map, initial_store["claims"])
    expected_accepted = load(ROOT / "fixtures/expected/claim-accepted.json")
    expected_stale = load(ROOT / "fixtures/expected/claim-rejected-stale.json")
    with tempfile.TemporaryDirectory(prefix="dfe-claim-") as temporary:
        store_path = Path(temporary) / "claim-store.json"
        shutil.copyfile(ROOT / "fixtures/active-claim.json", store_path)
        request = {
            "claim_id": "claim-B",
            "decision_id": "B",
            "source_digest": frontier["source_digest"],
            "owner": "resolver:test",
            "claimed_at": "2026-07-30T00:00:00Z",
            "expected_store_digest": canonical_digest(initial_store),
        }
        accepted = claim_decision(request, frontier, store_path)
        competing = claim_decision(request, frontier, store_path)
        competing_store_digest = canonical_digest(load(store_path))

        shutil.copyfile(ROOT / "fixtures/active-claim.json", store_path)
        stale_request = load(ROOT / "fixtures/stale-claim.json")
        stale_request["expected_store_digest"] = canonical_digest(initial_store)
        stale = claim_decision(stale_request, frontier, store_path)
        unchanged_after_stale = canonical_digest(load(store_path)) == canonical_digest(initial_store)

    active_reasons = {
        item["id"]: item["exclusion_reasons"] for item in frontier["nodes"]
    }
    passed = (
        accepted == expected_accepted
        and stale == expected_stale
        and competing["code"] == "CAS_MISMATCH"
        and competing_store_digest == accepted["after_store_digest"]
        and unchanged_after_stale
        and "active_claim" in active_reasons["A"]
    )
    result = {
        "schema_version": "dfe-claim-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-002", "DFE-FIX-004"],
        "accepted": accepted,
        "stale": stale,
        "competing_code": competing["code"],
        "active_claim_reason": active_reasons["A"],
        "fixture_store_unchanged": unchanged_after_stale,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
