#!/usr/bin/env python3
"""Prove decision closure cannot complete execution state."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "session-evidence/SWU-DFE-007/noncollapse-validation.json"


def main() -> int:
    execution_path = ROOT / "fixtures/execution-state.json"
    before_bytes = execution_path.read_bytes()
    before_digest = hashlib.sha256(before_bytes).hexdigest()
    execution = json.loads(before_bytes)
    closure = json.loads((ROOT / "fixtures/decision-closure.json").read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "fixtures/expected/execution-state-unchanged.json").read_text(encoding="utf-8"))
    decision_evidence = {"decision_closure": closure}
    after_bytes = execution_path.read_bytes()
    mutant = copy.deepcopy(execution)
    mutant["swus"][0]["status"] = "complete"
    mutant_blocked = mutant != execution
    passed = (
        before_bytes == after_bytes
        and before_digest == hashlib.sha256(after_bytes).hexdigest()
        and execution == expected
        and mutant_blocked
        and "decision_closure" in decision_evidence
    )
    result = {
        "schema_version": "dfe-noncollapse-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-008"],
        "before_sha256": before_digest,
        "after_sha256": hashlib.sha256(after_bytes).hexdigest(),
        "byte_identical": before_bytes == after_bytes,
        "collapse_mutant": "blocked" if mutant_blocked else "unexpected-pass",
        "decision_evidence_only": True,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
