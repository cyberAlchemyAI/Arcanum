#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
capability_table="$script_dir/../mode-capabilities.json"
fixture_dir="$script_dir/fixtures/distill-evidence"

python3 - "$script_dir" "$capability_table" "$fixture_dir" <<'PY'
import json
import pathlib
import sys

sys.path.insert(0, sys.argv[1])
from invoke_mode_capabilities import evaluate_active_mode_evidence, load_capabilities  # noqa: E402

table = load_capabilities(pathlib.Path(sys.argv[2]))
fixture_dir = pathlib.Path(sys.argv[3])
case = json.loads((fixture_dir / "missing-evidence-case.json").read_text(encoding="utf-8"))
payload = json.loads((fixture_dir / case["fixture"]).read_text(encoding="utf-8"))
result = evaluate_active_mode_evidence(payload["mode"], payload, table)

if result["status"] != case["expected_status"]:
    print(f"FAIL missing evidence status: {result}")
    raise SystemExit(1)
if result["mutation_handoff_allowed"] != case["expected_handoff"]:
    print(f"FAIL missing evidence handoff: {result}")
    raise SystemExit(1)
if case["expected_diagnostic"] not in result["diagnostics"]:
    print(f"FAIL missing evidence diagnostic: {result}")
    raise SystemExit(1)

print("PASS missing required plan evidence blocks")
print("PASS diagnostic names work_pack")
print("PASS mutation handoff remains false")
print("SUMMARY: PASS (3 of 3 checks satisfied expectations)")
print("AUTHORITY: missing evidence blocks before mutation handoff")
PY
