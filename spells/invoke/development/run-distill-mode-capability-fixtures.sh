#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
capability_table="$script_dir/../mode-capabilities.json"
fixture_dir="$script_dir/fixtures/distill-evidence"

python3 - "$script_dir" "$capability_table" "$fixture_dir" <<'PY'
import pathlib
import sys

sys.path.insert(0, sys.argv[1])
from invoke_mode_capabilities import ModeCapabilityError, load_capabilities, resolve_mode_capability  # noqa: E402

table = load_capabilities(pathlib.Path(sys.argv[2]))
fixture_dir = pathlib.Path(sys.argv[3])
cases = [
    "mode-capability-deferred-full.json",
    "mode-capability-deferred-validate.json",
    "mode-capability-active-design.json",
    "mode-capability-unknown.json",
]
failures = []

if set(table["modes"]) != {"define", "design", "plan", "handoff", "refresh", "full", "validate"}:
    failures.append("capability table does not enumerate all modes")
    print("FAIL capability table completeness")
else:
    print("PASS capability table enumerates all Invoke modes")

for fixture_name in cases:
    import json

    case = json.loads((fixture_dir / fixture_name).read_text(encoding="utf-8"))
    try:
        result = resolve_mode_capability(case["mode"], table)
    except ModeCapabilityError as error:
        if case["expected_status"] != "block":
            failures.append(f"{fixture_name}: {error}")
            print(f"FAIL {fixture_name}: {error}")
        else:
            print(f"PASS {fixture_name}: blocked ({error})")
        continue

    if result["status"] != case["expected_status"] or result["lifecycle_processed"] != case["expected_processed"]:
        failures.append(f"{fixture_name}: unexpected result {result}")
        print(f"FAIL {fixture_name}: {result}")
    elif result["mutation_handoff_allowed"] is not False:
        failures.append(f"{fixture_name}: capability gate granted handoff")
        print(f"FAIL {fixture_name}: capability gate granted handoff")
    elif case["mode"] in {"full", "validate"} and (result["dispatch_trace"] != "not_evaluated" or result["distill"] != "not_evaluated"):
        failures.append(f"{fixture_name}: deferred mode evaluated lifecycle obligations")
        print(f"FAIL {fixture_name}: deferred mode evaluated lifecycle obligations")
    else:
        print(f"PASS {fixture_name}: status={result['status']}, processed={result['lifecycle_processed']}")

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} failures)")
    raise SystemExit(1)

print(f"SUMMARY: PASS ({len(cases) + 1} of {len(cases) + 1} checks satisfied expectations)")
print("AUTHORITY: capability resolution is not lifecycle execution or mutation handoff")
PY
