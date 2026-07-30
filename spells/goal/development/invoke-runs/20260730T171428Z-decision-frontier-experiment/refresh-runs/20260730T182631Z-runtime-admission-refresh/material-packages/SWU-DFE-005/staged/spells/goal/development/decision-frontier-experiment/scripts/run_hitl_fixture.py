#!/usr/bin/env python3
"""Run the DFE HITL route and forbidden auto-resolution mutant."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.hitl import route_hitl  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-005/hitl-validation.json"


def main() -> int:
    document = json.loads((ROOT / "fixtures/hitl-map.json").read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "fixtures/expected/hitl-route.json").read_text(encoding="utf-8"))
    actual = route_hitl(document, "H1")
    mutant_blocked = False
    try:
        route_hitl(document, "H1", auto_resolution=True)
    except ValueError as error:
        mutant_blocked = str(error) == "HITL_AUTO_RESOLUTION_FORBIDDEN"
    passed = actual == expected and mutant_blocked and actual["resolution"] is None and actual["reconciliation"] is None
    result = {
        "schema_version": "dfe-hitl-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-011"],
        "route": actual,
        "auto_resolution_mutant": "blocked" if mutant_blocked else "unexpected-pass",
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
