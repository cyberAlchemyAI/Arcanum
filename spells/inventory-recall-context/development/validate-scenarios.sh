#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
scenario_path="$script_dir/L0-SCENARIOS.json"

python3 - "$scenario_path" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
document = json.loads(path.read_text(encoding="utf-8"))

expected_ids = [
    "positive",
    "stale",
    "missing",
    "contradictory",
    "unsafe",
    "over-budget",
    "blocked-index",
]
expected_reasons = {
    "positive": "allowed",
    "stale": "stale-source",
    "missing": "missing-source",
    "contradictory": "contradictory-source",
    "unsafe": "unsafe-source",
    "over-budget": "over-budget",
    "blocked-index": "blocked-index",
}

assert document.get("schema_version") == "1.0.0"
assert document.get("scenario_pack_id") == "inventory-recall-context-l0"
assert document.get("authority_effect") == "none"
assert document.get("claim_ceiling") == "fixture-contract-only"

cases = document.get("cases")
assert isinstance(cases, list) and len(cases) == 7
assert [case.get("id") for case in cases] == expected_ids

required = {
    "lookup_ready",
    "source_states",
    "contradiction",
    "source_scope_safe",
    "obligations_complete",
    "pack_within_budget",
    "expected",
}
allowed_states = {"current", "stale", "missing", "unsafe"}

for case in cases:
    case_id = case["id"]
    assert required <= set(case), case_id
    assert isinstance(case["lookup_ready"], bool), case_id
    assert isinstance(case["contradiction"], bool), case_id
    assert isinstance(case["source_scope_safe"], bool), case_id
    assert isinstance(case["obligations_complete"], bool), case_id
    assert isinstance(case["pack_within_budget"], bool), case_id
    assert isinstance(case["source_states"], list), case_id
    assert set(case["source_states"]) <= allowed_states, case_id
    expected = case["expected"]
    assert expected["reason_code"] == expected_reasons[case_id], case_id
    assert expected["injection_allowed"] is (case_id == "positive"), case_id

print("scenario-contract: pass (7 frozen cases; runtime not executed)")
PY
