from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


OPERATION_EXIT_CODES = {"PASS": 0, "BLOCK": 1, "INCONCLUSIVE": 2}


@dataclass(frozen=True)
class TerminalOutcome:
    operation_status: str
    exit_code: int
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "operation_status": self.operation_status,
            "exit_code": self.exit_code,
            "reason": self.reason,
        }


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "contracts"
        / "terminal-outcome.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validation_errors(record: object) -> list[str]:
    if not isinstance(record, Mapping):
        return ["terminal input must be a JSON object"]
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(
            _validator().iter_errors(dict(record)),
            key=lambda item: list(item.path),
        )
    ]


def _outcome(operation_status: str, reason: str) -> TerminalOutcome:
    return TerminalOutcome(
        operation_status,
        OPERATION_EXIT_CODES[operation_status],
        reason,
    )


def evaluate_terminal(record: object) -> TerminalOutcome:
    """Map only a schema-qualified terminal record to an operation/exit pair.

    Invalid input becomes INCONCLUSIVE for callers. ``validation_errors`` is the
    strict rejection surface for a caller that needs to report malformed input.
    """

    if validation_errors(record):
        return _outcome("INCONCLUSIVE", "INPUT_INVALID")
    assert isinstance(record, Mapping)
    if not (
        record["contract_valid"]
        and record["runtime_valid"]
        and record["evidence_valid"]
    ):
        return _outcome("INCONCLUSIVE", "DEPENDENCY_INVALID")

    mode = record["mode"]
    if mode == "validate-interface":
        evidence_status = record["evidence_status"]
        if evidence_status in {"PASS", "PASS_WITH_FLAGS"}:
            return _outcome("PASS", "EVIDENCE_ACCEPTED")
        if evidence_status == "BLOCK":
            return _outcome("BLOCK", "EVIDENCE_BLOCKED")
        return _outcome("INCONCLUSIVE", "EVIDENCE_INCONCLUSIVE")

    if mode == "calibrate":
        if not record["input_complete"] or record["evidence_status"] == "INCONCLUSIVE":
            return _outcome("INCONCLUSIVE", "CALIBRATION_EVIDENCE_INCOMPLETE")
        if not record["required_repeats_complete"]:
            return _outcome("INCONCLUSIVE", "REQUIRED_REPEATS_INCOMPLETE")
        oracle_comparison = record["oracle_comparison"]
        if oracle_comparison == "INCONCLUSIVE":
            return _outcome("INCONCLUSIVE", "ORACLE_INCONCLUSIVE")
        if oracle_comparison == "MISMATCH" or not record["repeatability_match"]:
            return _outcome("BLOCK", "CALIBRATION_MISMATCH")
        return _outcome("PASS", "CALIBRATION_MATCH")

    if mode == "report":
        if record["input_complete"]:
            return _outcome("PASS", "REPORT_COMPLETE")
        return _outcome("INCONCLUSIVE", "REPORT_INCOMPLETE")

    return _outcome("INCONCLUSIVE", "MODE_INVALID")
