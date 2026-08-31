#!/usr/bin/env python3
"""Verify shared observer validation is reusable and no-effect."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "arcana/signal-observer/scripts/validate-invocation-envelope.py"
OBSERVER = ROOT / "framework/observability/scripts/observe-invocation.sh"


def valid() -> dict:
    return {
        "timestamp": "2026-08-28T00:00:00Z", "run_id": "test-run",
        "capability": {"id": "invoke", "kind": "spell", "mode": "plan"},
        "request": {"summary": "Validate without append."},
        "execution": {"status": "projected", "outputs": [], "files_changed": [], "validation": []},
        "observer": {"quality_bar_status": "not_checked", "anti_pattern_hits": [], "workflow_gaps": [], "reflection_trigger": "none", "recommendation": "none"}
    }


class EnvelopeValidatorTest(unittest.TestCase):
    def test_valid_and_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw); envelope = root / "envelope.json"; envelope.write_text(json.dumps(valid()), encoding="utf-8")
            completed = subprocess.run([sys.executable, str(VALIDATOR), "--envelope", str(envelope)], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0); self.assertIn("APPEND_ATTEMPT_COUNT=0", completed.stdout)
            payload = valid(); del payload["observer"]["recommendation"]; envelope.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, str(VALIDATOR), "--envelope", str(envelope)], check=False).returncode, 1)

    def test_invalid_append_creates_no_observability_state(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw); envelope = root / "invalid.json"; envelope.write_text("{}\n", encoding="utf-8"); state = root / "observability"
            completed = subprocess.run([str(OBSERVER), "--envelope", str(envelope), "--observability-dir", str(state)], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 1); self.assertFalse(state.exists())


if __name__ == "__main__": unittest.main()
