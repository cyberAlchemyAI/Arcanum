#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema_dir="$script_dir/../schemas"
fixture_dir="$script_dir/fixtures/distill-evidence"

python3 - "$script_dir" "$schema_dir" "$fixture_dir" <<'PY'
import pathlib
import sys

sys.path.insert(0, sys.argv[1])
from distill_semantic_validator import SemanticValidationError, load_case, validate_semantic_case  # noqa: E402

schema_dir = pathlib.Path(sys.argv[2])
fixture_dir = pathlib.Path(sys.argv[3])
cases = [
    ("semantic-valid.json", True, None),
    ("semantic-missing-objection-category.json", False, "objection category required"),
    ("semantic-unreconciled-objection.json", False, "exactly one reconciliation required"),
    ("semantic-missing-technique-trace.json", False, "missing technique trace"),
    ("semantic-round-budget-exceeded.json", False, "termination round_count exceeds round budget"),
]
failures = []

for fixture_name, should_pass, expected in cases:
    try:
        result = validate_semantic_case(load_case(fixture_dir / fixture_name), schema_dir, fixture_dir)
        if not should_pass:
            failures.append(f"{fixture_name}: unexpectedly passed")
            print(f"FAIL {fixture_name}: unexpectedly passed")
        elif "mutation_handoff_allowed" in result:
            failures.append(f"{fixture_name}: returned forbidden handoff authority")
            print(f"FAIL {fixture_name}: returned forbidden handoff authority")
        else:
            print(f"PASS {fixture_name}: semantic_status={result['semantic_status']}")
    except SemanticValidationError as error:
        if should_pass:
            failures.append(f"{fixture_name}: {error}")
            print(f"FAIL {fixture_name}: {error}")
        elif expected not in str(error):
            failures.append(f"{fixture_name}: expected {expected}; got {error}")
            print(f"FAIL {fixture_name}: wrong diagnostic: {error}")
        else:
            print(f"PASS {fixture_name}: blocked ({expected})")

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} of {len(cases)} cases failed)")
    raise SystemExit(1)

print(f"SUMMARY: PASS ({len(cases)} of {len(cases)} cases satisfied expectations)")
print("AUTHORITY: semantic evidence only; provenance and mutation handoff remain deferred")
PY
