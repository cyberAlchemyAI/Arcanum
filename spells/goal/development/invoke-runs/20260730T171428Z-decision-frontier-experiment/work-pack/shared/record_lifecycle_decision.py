#!/usr/bin/env python3
"""Record the bounded post-fixture Spellcraft lifecycle decision."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--closure", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    spells_root = Path.cwd().resolve()
    closure_path = spells_root / args.closure
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    if closure.get("status") != "pass":
        return 1
    content = closure_path.read_bytes()
    decision = {
        "schema_version": "dfe-lifecycle-decision.v1",
        "unit_id": "READINESS-DFE-001",
        "status": "pass",
        "owner": "spellcraft",
        "source_closure": {
            "path": args.closure,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
        },
        "decision": "authorize-paired-real-workflow-experiment-proposal",
        "rationale": "Synthetic fixtures can justify a paired workflow proposal, not canonical adoption.",
        "experiment_harness_status": "not_applicable",
        "experiment_harness_reason": "The fixture work pack is its own bounded deterministic harness; reusable real-workflow validation is the selected next proposal.",
        "selected_swu": None,
        "promotion": False,
        "publication": False,
        "authority_effect": "none",
        "successor": None,
    }
    output = spells_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
