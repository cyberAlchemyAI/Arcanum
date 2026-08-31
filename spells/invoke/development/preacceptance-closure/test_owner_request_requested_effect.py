#!/usr/bin/env python3
"""Regression coverage for manifest-bound owner-request requested effects."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
RUNNER = ROOT / "arcanum/spells/invoke/scripts/preacceptance_closure.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("requested_effect_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RequestedEffectBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = load_runner()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.effect = {"effect_id": "fixture-effect", "authority_write_ceiling": []}
        self.paths = {}
        for name, value in {
            "base.json": {}, "manifest.json": {"requested_effect": self.effect},
            "receipt.json": {}, "review.json": {}, "adoption.json": {},
        }.items():
            path = self.root / name
            path.write_text(json.dumps(value) + "\n", encoding="utf-8")
            self.paths[name] = path

    def tearDown(self) -> None:
        self.temp.cleanup()

    def ref(self, name: str) -> dict:
        data = self.paths[name].read_bytes()
        return {"path": name, "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}

    def request(self, effect=...) -> dict:
        request = {
            "schema_version": "invoke.owner-acceptance-request.v2",
            "request_id": "fixture-request",
            "base_request_ref": self.ref("base.json"),
            "base_request": {},
            "preacceptance_closure": {
                "manifest_ref": self.ref("manifest.json"),
                "closure_receipt_ref": self.ref("receipt.json"),
                "independent_review_ref": self.ref("review.json"),
                "adoption_ref": self.ref("adoption.json"),
                "closure_graph_digest": "0" * 64,
            },
            "emission_gate": "pass",
            "authority_effect": "none",
            "claim_ceiling": "fixture only",
        }
        if effect is not ...:
            request["requested_effect"] = effect
        request["request_digest"] = self.runner.canonical_digest(request)
        return request

    def validate(self, request: dict) -> list[str]:
        path = self.root / "request.json"
        path.write_text(json.dumps(request) + "\n", encoding="utf-8")
        with mock.patch.object(self.runner, "schema_errors", return_value=[]), mock.patch.object(
            self.runner, "emit_request", return_value=request
        ):
            return self.runner.validate_emitted_request(self.root, path)

    def test_missing_requested_effect_reproduces_attempt_004_block(self) -> None:
        self.assertIn("owner request lacks a requested-effect binding", self.validate(self.request()))

    def test_tampered_or_mismatched_requested_effect_blocks(self) -> None:
        blockers = self.validate(self.request({"effect_id": "tampered", "authority_write_ceiling": []}))
        self.assertIn("owner request requested-effect binding differs from bound manifest", blockers)

    def test_exact_manifest_requested_effect_passes(self) -> None:
        self.assertEqual(self.validate(self.request(self.effect)), [])


if __name__ == "__main__":
    unittest.main()
