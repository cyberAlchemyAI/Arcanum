#!/usr/bin/env python3
"""Run terminal, open, and fog DFE Way Clear fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.way_clear import evaluate_way_clear  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-006/way-clear-validation.json"


def load(name: str) -> object:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def main() -> int:
    clear = evaluate_way_clear(load("way-clear-map.json"))
    expected = json.loads((ROOT / "fixtures/expected/way-clear.json").read_text(encoding="utf-8"))
    open_result = evaluate_way_clear(load("way-clear-open-mutant.json"))
    fog_result = evaluate_way_clear(load("way-clear-fog-mutant.json"))
    passed = (
        clear == expected
        and clear["status"] == "clear"
        and open_result["status"] == "blocked"
        and open_result["remaining"][0]["reason"] == "open_decision"
        and fog_result["status"] == "blocked"
        and fog_result["remaining"][0]["reason"] == "unresolved_fog"
    )
    result = {
        "schema_version": "dfe-way-clear-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-012"],
        "clear": clear,
        "open_mutant": open_result,
        "fog_mutant": fog_result,
        "state_changed": False,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
