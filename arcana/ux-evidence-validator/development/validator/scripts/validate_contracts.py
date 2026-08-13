from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


VALIDATOR_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = VALIDATOR_ROOT / "contracts" / "terminal-outcome.schema.json"
TERMINAL_PATH = VALIDATOR_ROOT / "uev_kernel" / "terminal.py"


def load_terminal():
    spec = importlib.util.spec_from_file_location("uev_terminal", TERMINAL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TERMINAL_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    valid_record = {
        "schema_version": "1.0.0",
        "mode": "calibrate",
        "contract_valid": True,
        "runtime_valid": True,
        "evidence_valid": True,
        "input_complete": True,
        "evidence_status": "BLOCK",
        "oracle_comparison": "MATCH",
        "required_repeats_complete": True,
        "repeatability_match": True,
    }
    if list(validator.iter_errors(valid_record)):
        raise RuntimeError("known-good terminal record is not schema-valid")
    invalid_record = {**valid_record, "evidence_status": "flag"}
    if not list(validator.iter_errors(invalid_record)):
        raise RuntimeError("unqualified evidence status was accepted")
    unknown_field = {**valid_record, "semantic_drift": True}
    if not list(validator.iter_errors(unknown_field)):
        raise RuntimeError("unknown semantics-bearing field was accepted")
    terminal = load_terminal()
    outcome = terminal.evaluate_terminal(valid_record)
    if (outcome.operation_status, outcome.exit_code) != ("PASS", 0):
        raise RuntimeError("known-bad calibration mapping drifted")
    print(json.dumps({"checks": 5, "schema": str(SCHEMA_PATH), "status": "pass"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
