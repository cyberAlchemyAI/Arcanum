#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema_dir="$script_dir/../schemas"
fixture_dir="$script_dir/fixtures/distill-evidence"

python3 - "$script_dir" "$schema_dir" "$fixture_dir" <<'PY'
import pathlib
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
from distill_provenance_validator import load_case, validate_provenance_case  # noqa: E402

fixture_dir = pathlib.Path(sys.argv[3])
schema_dir = pathlib.Path(sys.argv[2])
cases = [
    ("provenance-valid.json", True, None),
    ("provenance-changed-content.json", False, "digest mismatch"),
    ("provenance-unresolved-handle.json", False, "unresolved reviewed input"),
    ("provenance-verdict-mismatch.json", False, "verdict mismatch"),
    ("provenance-workpack-mismatch.json", False, "stale Work Pack binding"),
]
failures = []

for fixture_name, should_pass, expected in cases:
    case = load_case(fixture_dir / fixture_name)
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = pathlib.Path(temporary_directory)
        for relative_path, content in case["reviewed_files"].items():
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        result = validate_provenance_case(case, schema_dir, fixture_dir, root)

    if should_pass:
        if result["status"] != "pass" or result["mutation_handoff_allowed"] is not True:
            failures.append(f"{fixture_name}: expected pass with derived handoff")
            print(f"FAIL {fixture_name}: {result}")
        elif case["authored_mutation_handoff_allowed"] is not True:
            failures.append(f"{fixture_name}: fixture authority control missing")
            print(f"FAIL {fixture_name}: authored authority control missing")
        else:
            print(f"PASS {fixture_name}: status=pass, derived_handoff=true")
    else:
        diagnostic_text = "; ".join(result["diagnostics"])
        if result["status"] != "block" or result["mutation_handoff_allowed"] is not False or expected not in diagnostic_text:
            failures.append(f"{fixture_name}: expected block containing {expected}; got {result}")
            print(f"FAIL {fixture_name}: wrong result: {result}")
        else:
            print(f"PASS {fixture_name}: blocked ({expected}), derived_handoff=false")

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} of {len(cases)} cases failed)")
    raise SystemExit(1)

print(f"SUMMARY: PASS ({len(cases)} of {len(cases)} cases satisfied expectations)")
print("AUTHORITY: mutation handoff is derived by the validator; authored handoff fields are ignored")
PY
