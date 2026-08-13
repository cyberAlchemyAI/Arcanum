from __future__ import annotations

import importlib.util
import itertools
import sys
import unittest
from pathlib import Path


TERMINAL_PATH = Path(__file__).resolve().parents[1] / "uev_kernel" / "terminal.py"


def load_terminal():
    spec = importlib.util.spec_from_file_location("uev_terminal_test", TERMINAL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TERMINAL_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


terminal = load_terminal()


def record(**overrides):
    value = {
        "schema_version": "1.0.0",
        "mode": "validate-interface",
        "contract_valid": True,
        "runtime_valid": True,
        "evidence_valid": True,
        "input_complete": True,
        "evidence_status": "PASS",
        "oracle_comparison": "NOT_APPLICABLE",
        "required_repeats_complete": False,
        "repeatability_match": False,
    }
    value.update(overrides)
    return value


class TerminalOutcomeTests(unittest.TestCase):
    def assert_outcome(self, value, status, exit_code):
        actual = terminal.evaluate_terminal(value)
        self.assertEqual((actual.operation_status, actual.exit_code), (status, exit_code))
        self.assertEqual(actual.exit_code, terminal.OPERATION_EXIT_CODES[actual.operation_status])

    def test_validate_interface_table(self):
        for evidence_status, expected in {
            "PASS": ("PASS", 0),
            "PASS_WITH_FLAGS": ("PASS", 0),
            "BLOCK": ("BLOCK", 1),
            "INCONCLUSIVE": ("INCONCLUSIVE", 2),
        }.items():
            with self.subTest(evidence_status=evidence_status):
                self.assert_outcome(record(evidence_status=evidence_status), *expected)

    def test_rt3_known_bad_block_is_calibration_success(self):
        self.assert_outcome(
            record(
                mode="calibrate",
                evidence_status="BLOCK",
                oracle_comparison="MATCH",
                required_repeats_complete=True,
                repeatability_match=True,
            ),
            "PASS",
            0,
        )

    def test_rt6_soft_flag_is_calibration_success(self):
        self.assert_outcome(
            record(
                mode="calibrate",
                evidence_status="PASS_WITH_FLAGS",
                oracle_comparison="MATCH",
                required_repeats_complete=True,
                repeatability_match=True,
            ),
            "PASS",
            0,
        )

    def test_calibration_mismatch_blocks(self):
        self.assert_outcome(
            record(
                mode="calibrate",
                evidence_status="PASS",
                oracle_comparison="MISMATCH",
                required_repeats_complete=True,
                repeatability_match=True,
            ),
            "BLOCK",
            1,
        )

    def test_rt9_repeatability_mismatch_blocks(self):
        self.assert_outcome(
            record(
                mode="calibrate",
                evidence_status="PASS",
                oracle_comparison="MATCH",
                required_repeats_complete=True,
                repeatability_match=False,
            ),
            "BLOCK",
            1,
        )

    def test_incomplete_calibration_is_inconclusive(self):
        self.assert_outcome(
            record(
                mode="calibrate",
                evidence_status="PASS",
                oracle_comparison="MATCH",
                required_repeats_complete=False,
                repeatability_match=True,
            ),
            "INCONCLUSIVE",
            2,
        )

    def test_oracle_inconclusive_is_inconclusive(self):
        self.assert_outcome(
            record(
                mode="calibrate",
                evidence_status="PASS",
                oracle_comparison="INCONCLUSIVE",
                required_repeats_complete=True,
                repeatability_match=True,
            ),
            "INCONCLUSIVE",
            2,
        )

    def test_report_complete_and_incomplete(self):
        complete = record(mode="report", input_complete=True)
        incomplete = record(mode="report", input_complete=False)
        self.assert_outcome(complete, "PASS", 0)
        self.assert_outcome(incomplete, "INCONCLUSIVE", 2)

    def test_dependency_invalid_is_inconclusive(self):
        for field in ("contract_valid", "runtime_valid", "evidence_valid"):
            with self.subTest(field=field):
                self.assert_outcome(record(**{field: False}), "INCONCLUSIVE", 2)

    def test_unqualified_status_is_rejected_and_terminalized(self):
        invalid = record(evidence_status="flag")
        self.assertTrue(terminal.validation_errors(invalid))
        self.assert_outcome(invalid, "INCONCLUSIVE", 2)

    def test_unknown_semantics_bearing_field_is_rejected(self):
        invalid = record(semantic_drift=True)
        self.assertTrue(terminal.validation_errors(invalid))
        self.assert_outcome(invalid, "INCONCLUSIVE", 2)

    def test_impossible_mode_namespace_combination_is_rejected(self):
        invalid = record(oracle_comparison="MATCH")
        self.assertTrue(terminal.validation_errors(invalid))
        self.assert_outcome(invalid, "INCONCLUSIVE", 2)

    def test_missing_input_is_terminalized_inconclusive(self):
        invalid = record()
        del invalid["evidence_status"]
        self.assert_outcome(invalid, "INCONCLUSIVE", 2)

    def test_exhaustive_schema_legal_and_illegal_terminal_table(self):
        """Keep the declared finite input table durable and independent.

        The input schema has a deliberately small finite domain: three modes,
        four evidence states, four oracle states, and six booleans.  This test
        enumerates its entire 3,072-record product rather than sampling it.
        For all 896 schema-legal records, the expected result is calculated by
        this table-side oracle, which does not call ``evaluate_terminal``.  The
        other 2,176 records must be rejected by the schema and terminalized as
        inconclusive by the public evaluator.
        """

        modes = ("validate-interface", "calibrate", "report")
        evidence_states = ("PASS", "PASS_WITH_FLAGS", "BLOCK", "INCONCLUSIVE")
        oracle_states = ("MATCH", "MISMATCH", "NOT_APPLICABLE", "INCONCLUSIVE")

        def expected_legal_outcome(value):
            if not all(
                value[name]
                for name in ("contract_valid", "runtime_valid", "evidence_valid")
            ):
                return ("INCONCLUSIVE", 2)
            if value["mode"] == "validate-interface":
                return {
                    "PASS": ("PASS", 0),
                    "PASS_WITH_FLAGS": ("PASS", 0),
                    "BLOCK": ("BLOCK", 1),
                    "INCONCLUSIVE": ("INCONCLUSIVE", 2),
                }[value["evidence_status"]]
            if value["mode"] == "report":
                return ("PASS", 0) if value["input_complete"] else ("INCONCLUSIVE", 2)

            calibration_incomplete = (
                not value["input_complete"]
                or value["evidence_status"] == "INCONCLUSIVE"
                or not value["required_repeats_complete"]
                or value["oracle_comparison"] == "INCONCLUSIVE"
            )
            if calibration_incomplete:
                return ("INCONCLUSIVE", 2)
            if (
                value["oracle_comparison"] == "MISMATCH"
                or not value["repeatability_match"]
            ):
                return ("BLOCK", 1)
            return ("PASS", 0)

        legal_count = 0
        illegal_count = 0
        for (
            mode,
            evidence_status,
            oracle_comparison,
            contract_valid,
            runtime_valid,
            evidence_valid,
            input_complete,
            required_repeats_complete,
            repeatability_match,
        ) in itertools.product(
            modes,
            evidence_states,
            oracle_states,
            (False, True),
            (False, True),
            (False, True),
            (False, True),
            (False, True),
            (False, True),
        ):
            value = record(
                mode=mode,
                evidence_status=evidence_status,
                oracle_comparison=oracle_comparison,
                contract_valid=contract_valid,
                runtime_valid=runtime_valid,
                evidence_valid=evidence_valid,
                input_complete=input_complete,
                required_repeats_complete=required_repeats_complete,
                repeatability_match=repeatability_match,
            )
            with self.subTest(value=value):
                if terminal.validation_errors(value):
                    illegal_count += 1
                    self.assert_outcome(value, "INCONCLUSIVE", 2)
                else:
                    legal_count += 1
                    expected = expected_legal_outcome(value)
                    self.assert_outcome(value, *expected)

        self.assertEqual((legal_count, illegal_count), (896, 2176))


if __name__ == "__main__":
    unittest.main(verbosity=2)
