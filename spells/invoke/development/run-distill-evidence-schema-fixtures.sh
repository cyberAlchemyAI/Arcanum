#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema_dir="$(cd "$script_dir/../schemas" && pwd)"
fixture_dir="$script_dir/fixtures/distill-evidence"

python3 - "$schema_dir" "$fixture_dir" <<'PY'
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

schema_dir = pathlib.Path(sys.argv[1])
fixture_dir = pathlib.Path(sys.argv[2])

cases = [
    ("valid-run-request.json", "distill-run-request.schema.json", True, None),
    ("valid-execution-receipt.json", "distill-execution-receipt.schema.json", True, None),
    ("valid-validation-result.json", "distill-validation-result.schema.json", True, None),
    (
        "invalid-run-request-missing-budget.json",
        "distill-run-request.schema.json",
        False,
        "'round_budget' is a required property",
    ),
    (
        "invalid-receipt-missing-role-trace.json",
        "distill-execution-receipt.schema.json",
        False,
        "'role_trace' is a required property",
    ),
    (
        "invalid-result-missing-handoff-flag.json",
        "distill-validation-result.schema.json",
        False,
        "'mutation_handoff_allowed' is a required property",
    ),
]

generated_omission_cases = [
    ("valid-run-request.json", "distill-run-request.schema.json", "run_id"),
    ("valid-run-request.json", "distill-run-request.schema.json", "requested_techniques"),
    ("valid-execution-receipt.json", "distill-execution-receipt.schema.json", "verdict"),
    ("valid-validation-result.json", "distill-validation-result.schema.json", "checks"),
]

failures = []
for fixture_name, schema_name, should_pass, expected_error in cases:
    schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
    instance = json.loads((fixture_dir / fixture_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))

    if should_pass and errors:
        failures.append(f"{fixture_name}: expected pass; got {errors[0].message}")
        print(f"FAIL valid {fixture_name}: {errors[0].message}")
    elif not should_pass and not errors:
        failures.append(f"{fixture_name}: expected rejection; fixture passed")
        print(f"FAIL invalid {fixture_name}: unexpectedly passed")
    elif not should_pass and expected_error not in [error.message for error in errors]:
        messages = "; ".join(error.message for error in errors)
        failures.append(f"{fixture_name}: expected {expected_error}; got {messages}")
        print(f"FAIL invalid {fixture_name}: wrong rejection: {messages}")
    else:
        expectation = "accepted" if should_pass else f"rejected ({expected_error})"
        print(f"PASS {fixture_name}: {expectation}")

for fixture_name, schema_name, omitted_property in generated_omission_cases:
    schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
    instance = json.loads((fixture_dir / fixture_name).read_text(encoding="utf-8"))
    del instance[omitted_property]
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    expected_error = f"'{omitted_property}' is a required property"
    if expected_error not in [error.message for error in errors]:
        messages = "; ".join(error.message for error in errors) or "fixture passed"
        failures.append(f"generated omission {omitted_property}: expected {expected_error}; got {messages}")
        print(f"FAIL generated omission {omitted_property}: {messages}")
    else:
        print(f"PASS generated omission {omitted_property}: rejected ({expected_error})")

if failures:
    total_cases = len(cases) + len(generated_omission_cases)
    print(f"SUMMARY: FAIL ({len(failures)} of {total_cases} cases failed)")
    raise SystemExit(1)

total_cases = len(cases) + len(generated_omission_cases)
print(f"SUMMARY: PASS ({total_cases} of {total_cases} cases satisfied expectations)")
print("AUTHORITY: structural validation only; execution proof and mutation readiness are not established")
PY
