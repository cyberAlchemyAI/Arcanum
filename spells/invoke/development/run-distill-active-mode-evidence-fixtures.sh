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
from invoke_mode_capabilities import (  # noqa: E402
    ModeCapabilityError,
    evaluate_active_mode_evidence,
    load_capabilities,
)

table = load_capabilities(pathlib.Path(sys.argv[2]))
fixture_dir = pathlib.Path(sys.argv[3])
cases = [
    "mode-evidence-define-pass.json",
    "mode-evidence-design-pass.json",
    "mode-evidence-plan-pass.json",
    "mode-evidence-handoff-pass.json",
    "mode-evidence-refresh-pass.json",
    "mode-evidence-refresh-proposal-pass.json",
    "mode-evidence-refresh-authoring-flag.json",
    "mode-evidence-refresh-invalid-downstream-flag.json",
    "mode-evidence-missing-required.json",
    "mode-evidence-missing-conditional-rationale.json",
    "mode-evidence-missing-validator.json",
    "mode-evidence-authored-handoff.json",
]
failures = []

if set(table["modes"]) != {"define", "design", "plan", "handoff", "refresh", "full", "validate"}:
    failures.append("capability table does not enumerate all Invoke modes")
else:
    print("PASS capability table enumerates all Invoke modes")

for fixture_name in cases:
    case = json.loads((fixture_dir / fixture_name).read_text(encoding="utf-8"))
    try:
        result = evaluate_active_mode_evidence(case["mode"], case, table)
    except ModeCapabilityError as error:
        failures.append(f"{fixture_name}: {error}")
        print(f"FAIL {fixture_name}: {error}")
        continue

    expected_status = case["expected_status"]
    expected_handoff = case["expected_handoff"]
    if result["status"] != expected_status:
        failures.append(f"{fixture_name}: expected {expected_status}, got {result['status']}")
        print(f"FAIL {fixture_name}: {result}")
    elif result["mutation_handoff_allowed"] != expected_handoff:
        failures.append(f"{fixture_name}: unexpected handoff derivation")
        print(f"FAIL {fixture_name}: {result}")
    else:
        print(f"PASS {fixture_name}: status={result['status']}, handoff={result['mutation_handoff_allowed']}")

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} failures)")
    raise SystemExit(1)

print(f"SUMMARY: PASS ({len(cases) + 1} of {len(cases) + 1} checks satisfied expectations)")
print("AUTHORITY: active-mode handoff is derived from evidence and validator output")
PY
