#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema_dir="$script_dir/../schemas"
fixture_dir="$script_dir/fixtures/distill-evidence"

python3 - "$script_dir" "$schema_dir" "$fixture_dir" <<'PY'
import copy
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
from distill_provenance_validator import load_case, validate_provenance_case  # noqa: E402

schema_dir = pathlib.Path(sys.argv[2])
fixture_dir = pathlib.Path(sys.argv[3])
matrix = load_case(fixture_dir / "fabricated-evidence-matrix.json")
failures = []


def run_case(label, case):
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = pathlib.Path(temporary_directory)
        for relative_path, content in case.get("reviewed_files", {}).items():
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return validate_provenance_case(case, schema_dir, fixture_dir, root)


for entry in matrix["isolated"]:
    case = load_case(fixture_dir / entry["fixture"])
    result = run_case(entry["fixture"], case)
    diagnostics = "; ".join(result["diagnostics"])
    if result["status"] != "block" or result["mutation_handoff_allowed"] is not False:
        failures.append(f"{entry['fixture']}: did not fail closed")
        print(f"FAIL {entry['fixture']}: {result}")
    elif entry["diagnostic"] not in diagnostics:
        failures.append(f"{entry['fixture']}: missing {entry['diagnostic']}")
        print(f"FAIL {entry['fixture']}: {result}")
    else:
        print(f"PASS {entry['fixture']}: schema-complete fabricated case blocked")

combined = load_case(fixture_dir / "provenance-valid.json")
combined["reviewed_files"]["reviewed-input.md"] = "reviewed-input-v2\n"
combined["invoke_result"]["verdict"] = "block"
combined["work_pack_state"] = {"work_pack_id": "stale-work-pack", "selected_swu": "SWU-DEE-004"}
combined_result = run_case("combined", combined)
combined_diagnostics = "; ".join(combined_result["diagnostics"])
if (
    combined_result["status"] != "block"
    or combined_result["mutation_handoff_allowed"] is not False
    or any(expected not in combined_diagnostics for expected in matrix["combined"]["diagnostics"])
):
    failures.append("combined: did not preserve all fail-closed diagnostics")
    print(f"FAIL combined: {combined_result}")
else:
    print("PASS combined: multiple fabricated claims block together")

if failures:
    print(f"SUMMARY: FAIL ({len(failures)} failures)")
    raise SystemExit(1)

print("SUMMARY: PASS (5 of 5 fabricated-evidence cases satisfied expectations)")
print("AUTHORITY: schema-complete fabrication never grants mutation handoff")
PY
