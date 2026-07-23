#!/usr/bin/env python3
"""Causal fixtures for Invoke's three independent capability ceilings."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


INVOKE = Path(__file__).parents[1]
SCRIPT = INVOKE / "scripts" / "capability_status_resolver.py"
SPEC = importlib.util.spec_from_file_location("capability_status_resolver", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CapabilityStatusResolverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capability_path = INVOKE / "mode-capabilities.json"
        cls.capabilities = json.loads(cls.capability_path.read_text(encoding="utf-8"))
        cls.capability_sha = hashlib.sha256(cls.capability_path.read_bytes()).hexdigest()
        cls.request_schema = json.loads(
            (INVOKE / "schemas" / "capability-status-request.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.result_schema = json.loads(
            (INVOKE / "schemas" / "capability-status-result.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.material_schema = json.loads(
            (INVOKE / "schemas" / "material-package-receipt.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def artifact(self, mode, status="pass"):
        return {
            "receipt_id": f"artifact-{mode}",
            "axis": "artifact_authored",
            "mode": mode,
            "status": status,
            "evidence": [f"{mode}.md"],
        }

    def registry(self, mode, digest=None):
        return {
            "receipt_id": f"registry-{mode}",
            "axis": "registry_released",
            "mode": mode,
            "status": "released",
            "owner": "invoke-owner",
            "capability_sha256": digest or self.capability_sha,
            "deterministic_validation": {
                "status": "pass",
                "evidence": "deterministic-validation.json",
            },
            "live_regime": {
                "status": "pass",
                "evidence": "live-regime.json",
            },
        }

    def material(self):
        return {
            "schemaVersion": "1.0.0",
            "packageId": "package-1",
            "patchVerdict": "pass",
            "mutationHandoff": "ready",
            "packageDigest": "a" * 64,
            "validatedPaths": ["target.md"],
            "dependencyResult": "pass",
            "ownerBoundaryResult": "pass",
            "publicationBoundaryResult": "pass",
            "validationCommands": ["test target"],
            "lifecycleOwner": "invoke-owner",
            "authorityClass": "public",
            "publicationClass": "public",
            "reasons": [],
        }

    def runtime(self, mode, digest=None, gates=None):
        required = self.capabilities["modes"][mode]["runtime_required_gates"]
        return {
            "receipt_id": f"runtime-{mode}",
            "axis": "mutation_runtime_ready",
            "mode": mode,
            "status": "ready",
            "capability_sha256": digest or self.capability_sha,
            "material_package_id": "package-1",
            "material_package_digest": "a" * 64,
            "gates": gates or [
                {"gate": gate, "status": "pass", "evidence": f"{gate}.json"}
                for gate in required
            ],
        }

    def resolve(self, request):
        return MODULE.resolve_capability_status(
            request,
            self.capabilities,
            self.capability_sha,
            self.request_schema,
            self.result_schema,
            self.material_schema,
        )

    def base(self, mode):
        return {
            "schema_version": "invoke.capability-status.request.v1",
            "mode": mode,
        }

    def test_all_active_modes_support_artifact_only_without_later_axes(self):
        for mode in ("define", "design", "plan", "handoff", "refresh"):
            with self.subTest(mode=mode):
                request = self.base(mode)
                request["artifact_receipt"] = self.artifact(mode)
                result = self.resolve(request)
                self.assertEqual("pass", result["artifact_authored"]["status"])
                self.assertFalse(result["registry_released"]["status"])
                self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_all_active_modes_open_all_axes_only_from_matching_receipts(self):
        for mode in ("define", "design", "plan", "handoff", "refresh"):
            with self.subTest(mode=mode):
                request = self.base(mode)
                request.update({
                    "artifact_receipt": self.artifact(mode),
                    "registry_receipt": self.registry(mode),
                    "material_package_receipt": self.material(),
                    "runtime_receipt": self.runtime(mode),
                })
                result = self.resolve(request)
                self.assertEqual("pass", result["artifact_authored"]["status"])
                self.assertTrue(result["registry_released"]["status"])
                self.assertTrue(result["mutation_runtime_ready"]["status"])

    def test_deferred_modes_remain_unsupported_with_all_receipts(self):
        for mode in ("full", "validate"):
            with self.subTest(mode=mode):
                request = self.base(mode)
                request.update({
                    "artifact_receipt": self.artifact(mode),
                    "registry_receipt": self.registry(mode),
                    "material_package_receipt": self.material(),
                    "runtime_receipt": {
                        "receipt_id": f"runtime-{mode}",
                        "axis": "mutation_runtime_ready",
                        "mode": mode,
                        "status": "ready",
                        "capability_sha256": self.capability_sha,
                        "material_package_id": "package-1",
                        "material_package_digest": "a" * 64,
                        "gates": [{"gate": "fabricated", "status": "pass", "evidence": "x"}],
                    },
                })
                result = self.resolve(request)
                self.assertEqual("unsupported", result["artifact_authored"]["status"])
                self.assertFalse(result["registry_released"]["status"])
                self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_registry_receipt_opens_only_registry_axis(self):
        request = self.base("plan")
        request["registry_receipt"] = self.registry("plan")
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertTrue(result["registry_released"]["status"])
        self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_runtime_receipts_open_only_runtime_axis(self):
        request = self.base("plan")
        request.update({
            "material_package_receipt": self.material(),
            "runtime_receipt": self.runtime("plan"),
        })
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertFalse(result["registry_released"]["status"])
        self.assertTrue(result["mutation_runtime_ready"]["status"])

    def test_artifact_flag_does_not_open_later_axes(self):
        request = self.base("plan")
        request["artifact_receipt"] = self.artifact("plan", "flag")
        result = self.resolve(request)
        self.assertEqual("flag", result["artifact_authored"]["status"])
        self.assertFalse(result["registry_released"]["status"])
        self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_stale_registry_digest_does_not_release(self):
        request = self.base("plan")
        request["registry_receipt"] = self.registry("plan", "b" * 64)
        self.assertFalse(self.resolve(request)["registry_released"]["status"])

    def test_stale_runtime_digest_does_not_open_runtime(self):
        request = self.base("plan")
        request.update({
            "material_package_receipt": self.material(),
            "runtime_receipt": self.runtime("plan", "b" * 64),
        })
        self.assertFalse(self.resolve(request)["mutation_runtime_ready"]["status"])

    def test_missing_mode_gate_does_not_open_runtime(self):
        request = self.base("plan")
        request.update({
            "material_package_receipt": self.material(),
            "runtime_receipt": self.runtime(
                "plan",
                gates=[{
                    "gate": "material_package",
                    "status": "pass",
                    "evidence": "material.json",
                }],
            ),
        })
        self.assertFalse(self.resolve(request)["mutation_runtime_ready"]["status"])

    def test_material_receipt_alone_does_not_open_runtime(self):
        request = self.base("plan")
        request["material_package_receipt"] = self.material()
        self.assertFalse(self.resolve(request)["mutation_runtime_ready"]["status"])

    def test_cross_mode_receipt_does_not_open_artifact_axis(self):
        request = self.base("plan")
        request["artifact_receipt"] = self.artifact("design")
        self.assertEqual("block", self.resolve(request)["artifact_authored"]["status"])

    def test_legacy_collapsed_status_request_fails_explicitly(self):
        request = self.base("plan")
        request["status"] = "ready"
        with self.assertRaisesRegex(
            MODULE.CapabilityStatusError, "Additional properties are not allowed"
        ):
            self.resolve(request)

    def test_result_has_no_collapsed_capability_field(self):
        request = self.base("plan")
        result = self.resolve(request)
        self.assertEqual(
            {
                "schema_version",
                "mode",
                "capability_sha256",
                "artifact_authored",
                "registry_released",
                "mutation_runtime_ready",
            },
            set(result),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
