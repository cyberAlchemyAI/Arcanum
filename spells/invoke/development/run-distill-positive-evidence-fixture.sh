#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema_dir="$script_dir/../schemas"
fixture_dir="$script_dir/fixtures/distill-evidence"
reviewed_root="$(mktemp -d)"
trap 'rm -rf "$reviewed_root"' EXIT

python3 - "$script_dir" "$schema_dir" "$fixture_dir" "$reviewed_root" <<'PY'
import json
import pathlib
import sys

script_dir, schema_dir, fixture_dir, reviewed_root = map(pathlib.Path, sys.argv[1:])
sys.path.insert(0, str(script_dir))

from distill_provenance_validator import load_case, validate_provenance_case  # noqa: E402

positive = load_case(fixture_dir / "positive-evidence-case.json")
provenance = load_case(fixture_dir / positive["provenance_case"])
reviewed_root.mkdir(parents=True, exist_ok=True)
(reviewed_root / "reviewed-input.md").write_text("reviewed-input-v1\n", encoding="utf-8")

result = validate_provenance_case(provenance, schema_dir, fixture_dir, reviewed_root)
if result["status"] != positive["expected_status"]:
    print(f"FAIL positive evidence status: {result}")
    raise SystemExit(1)
if result["mutation_handoff_allowed"] is not positive["expected_mutation_handoff_allowed"]:
    print(f"FAIL positive evidence handoff derivation: {result}")
    raise SystemExit(1)

print("PASS request, events, receipt, semantic result, and provenance agree")
print("PASS reviewed-input digest and size resolve")
print("PASS validator derives mutation_handoff_allowed=true")
print("SUMMARY: PASS (3 of 3 checks satisfied expectations)")
print("AUTHORITY: positive evidence composes existing validators; it does not create authority")
PY
